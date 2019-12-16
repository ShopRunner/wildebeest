from collections import defaultdict
import logging
from pathlib import Path
import time
from typing import Any, Callable, DefaultDict, Iterable, Optional, Tuple, Union
import warnings

from joblib import delayed, Parallel
from numpy import iterable
import pandas as pd
from tqdm import tqdm

from creevey.constants import PathOrStr


class Pipeline:
    """
    Class for defining file processing pipelines.

    See Creevey's README for an example.

    Attributes
    ----------
    load_func
        Callable that takes a string or `Path` object as a single
        positional argument, reads from the corresponding location, and
        returns some representation of its contents.
    ops
        Iterable of callables each of which takes a single positional
        argument. The first element of `ops` must accept the output of
        `load_func`, and each subsequent element must accept the output
        of the immediately preceding element. It is recommended that
        every element of `ops` take and return one common data structure
        (e.g. NumPy arrays for image data) so that those elements can
        be recombined easily.
    write_func
        Callable that takes the output of the last element of `ops` (or
        the output of `load_func` if `ops` is `None` or empty) and a
        string or `Path` object and writes the former to the location
        specified by the latter.
    """

    def __init__(
        self,
        load_func: Callable[[PathOrStr], Any],
        ops: Optional[
            Union[Callable[[Any], Any], Iterable[Callable[[Any], Any]]]
        ] = None,
        write_func: Optional[Callable[[Any, PathOrStr], None]] = None,
    ) -> None:
        self.load_func = load_func

        if callable(ops):
            self.ops = [ops]
        elif iterable(ops):
            self.ops = ops
        elif ops is None:
            self.ops = []
        else:
            raise TypeError(
                'ops must be callable, an iterable of ' 'callables, or `None`'
            )

        self.write_func = write_func

    def run(
        self,
        inpaths: Iterable[PathOrStr],
        n_jobs: int,
        path_func: Optional[Callable[[PathOrStr], PathOrStr]] = None,
        skip_existing: Optional[bool] = None,
        exceptions_to_catch: Optional[Union[Exception, Tuple[Exception]]] = None,
    ) -> pd.DataFrame:
        """
        Run the pipeline.

        Across `n_jobs` threads, for each path in `inpaths`, if
        `skip_existing` is `True`, `path_func` is not `None`, and
        `path_func` of that path exists, do not do anything. Otherwise,
        use `load_func` to get the resource from that path and pipe its
        output through `ops`; and if `write_func` is not `None`, write
        the result to `path_func` of that path.

        Parameters
        ----------
        inpaths
            Iterable of string or Path objects pointing to resources to
            be processed and written out.
        n_jobs
            Number of threads to use.
        path_func
            Function that takes each input path and returns the desired
            corresponding output path.
        skip_existing
            Boolean indicating whether to skip items that would result
            in overwriting an existing file or to overwrite any such
            files.
        exceptions_to_catch
            Tuple of exception types to catch. An exception of one of
            these types will be logged with logging level ERROR and the
            relevant file will be skipped.

        Raises
        ------
        ValueError
            If `path_func` is `None` but `self.write_func` is not.

        Warns
        -----
        UserWarning
            When `skip_existing` is `True`.

        Returns
        -------
        Pandas DataFrame "run report" with the values from `inpaths` in
        its index and a "time_finished" column containing timestamps
        indicating when processing was completed for each file.
        If `self.write_func` is not `None`, also includes columns
        "outpath"; "skipped_existing" indicating whether processing was
        skipped because a file already existed at the output path; and
        "exception_handled" indicating whether processing failed due to
        an exception of a type included in `exceptions_to_catch`.
        """
        if skip_existing is None:
            skip_existing = True if self.write_func else False
        self._check_run_params(path_func=path_func, skip_existing=skip_existing)
        if skip_existing:
            warnings.warn(
                'Skipping files where a file exists at the output '
                'location. Pass `skip_existing=False` to overwrite '
                'existing files instead.'
            )

        log_dict = defaultdict(dict)

        Parallel(n_jobs=n_jobs, prefer='threads')(
            delayed(self.pipeline_func)(
                inpath=path,
                log_dict=log_dict,
                path_func=path_func,
                skip_existing=skip_existing,
                exceptions_to_catch=exceptions_to_catch,
            )
            for path in tqdm(inpaths)
        )

        run_report = pd.DataFrame.from_dict(log_dict, orient='index')

        return run_report

    def _check_run_params(self, path_func, skip_existing):
        if skip_existing and path_func is None:
            raise ValueError('`skip_existing` must be `False` if `path_func` is `None`')
        if path_func is None and self.write_func is not None:
            raise ValueError(
                '`path_func` can be `None` only if `self.write_func` is `None`.'
            )
        return skip_existing

    def pipeline_func(
        self,
        inpath: PathOrStr,
        log_dict: DefaultDict[str, dict],
        path_func: Optional[Callable[[PathOrStr], PathOrStr]] = None,
        skip_existing: Optional[bool] = None,
        exceptions_to_catch: Optional[Union[Tuple, Tuple[Exception]]] = None,
    ) -> None:
        """
        Process one file

        Use `self.load_func` to load the file at `inpath` into memory,
        and pipe the result through the functions in `self.ops`. If
        `self.write_func` is not `None`, write the result to
        `outpath_func(inpath)`.

        If `skip_existing` is `True`, check up front whether
        `outpath_func(inpath)` exists. If it does, skip the file.

        Catch `exceptions_to_catch` if they arise during file processing.

        Parameters
        ----------
        inpath
            Input path
        path_func
            See `self.run` docstring.
        skip_existing
            See `self.run` docstring.
        log_dict
            Dictionary used to store information for `run_report`.
        exceptions_to_catch
            See `self.run` docstring.

        Raises
        ------
        ValueError
            If `skip_existing` is `True` and `path_func` is `None`.

        Notes
        -----
        Records results in a dict within `log_dict[inpath]`:

        - `path_func(inpath)` as "outpath", if `path_func` is not `None`
        - bool indicating whether existing file was skipped as
        "skipped_existing"
        - bool indicating whether exception of a type specified in
        `exceptions_to_catch` was handled during processing as
        "exception_handled"
        - Timestamp indicating when processing finished as
        "time_finished"
        """
        self._check_run_params(path_func=path_func, skip_existing=skip_existing)

        skipped_existing = False
        exception_handled = False

        if skip_existing and Path(path_func(inpath)).is_file():
            skipped_existing = True
            logging.debug(
                f'Skipping {inpath} because there is already a file at '
                f'corresponding output path {path_func(inpath)}'
            )
        else:
            if exceptions_to_catch:
                try:
                    self._run_pipeline_func(
                        inpath=inpath, path_func=path_func, log_dict=log_dict
                    )
                except exceptions_to_catch as e:
                    exception_handled = True
                    logging.error(e, inpath)
            if not exceptions_to_catch:
                self._run_pipeline_func(
                    inpath=inpath, path_func=path_func, log_dict=log_dict
                )

        inpath_logs = log_dict[inpath]
        if path_func is not None:
            inpath_logs['outpath'] = path_func(inpath)
        inpath_logs['skipped_existing'] = int(skipped_existing)
        inpath_logs['exception_handled'] = int(exception_handled)
        inpath_logs['time_finished'] = time.time()

    def _run_pipeline_func(
        self,
        inpath: PathOrStr,
        path_func: Optional[Callable[[PathOrStr], PathOrStr]],
        **kwargs,
    ):
        # `kwargs` included to handle unused `log_dict` so that
        # `pipeline_func` does not have to change in
        # `CustomReportingPipeline`
        stage = self.load_func(inpath)
        for op in self.ops:
            stage = op(stage)
        if self.write_func:
            self.write_func(stage, path_func(inpath))


class CustomReportingPipeline(Pipeline):
    """
    Class for defining file processing pipelines with custom run
    recording.

    Differences from Pipeline parent class:

    - `load_func`, each element of `ops`, and `write_func` must each
    accept the string or `Path` object indicating the input item's
    location as an additional positional argument.
    - Each element of `ops` and `write_func` must each accept a
    `defaultdict(dict)` object as an additional positional argument.
    Functions defined in Creevey call this item `log_dict`.

    Inside those functions, adding items to `log_dict[inpath]` causes
    them to be added to the "run record" DataFrame that `self.run`
    returns. See Creevey's README for further explanation.
    """

    def _run_pipeline_func(
        self,
        inpath: PathOrStr,
        path_func: Optional[Callable[[PathOrStr], PathOrStr]],
        log_dict: DefaultDict[str, dict],
    ):
        stage = self.load_func(inpath, log_dict=log_dict)
        for op in self.ops:
            stage = op(stage, inpath=inpath, log_dict=log_dict)
        if self.write_func:
            self.write_func(stage, path_func(inpath), inpath=inpath, log_dict=log_dict)
