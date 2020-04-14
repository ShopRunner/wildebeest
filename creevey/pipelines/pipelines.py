"""Pipeline class definitions"""
from collections import defaultdict
import concurrent.futures
from datetime import datetime
import logging
from typing import Any, Callable, Iterable, Optional, Union

from numpy import iterable
import pandas as pd
from tqdm import tqdm

from creevey.constants import PathOrStr


RUN_REPORT_COLS = ['outpath', 'skipped', 'error', 'time_finished']


class Pipeline:
    """
    Class for defining file processing pipelines.

    Attributes
    ----------
    load_func
        Callable that takes a string or `Path` object as single
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
    check_existing_func
        Callable that takes an output path and checks whether a file
        exists at that path.
    write_func
        Callable that takes the output of the last element of `ops` (or
        the output of `load_func` if `ops` is `None` or empty) and a
        string or `Path` object and writes the former to the location
        specified by the latter.
    run_report_
    """

    def __init__(
        self,
        load_func: Callable[[PathOrStr], Any],
        write_func: Callable[[Any, PathOrStr], None],
        ops: Optional[
            Union[Callable[[Any], Any], Iterable[Callable[[Any], Any]]]
        ] = None,
    ) -> None:
        self.load_func = load_func
        if callable(ops):
            self.ops = [ops]
        elif iterable(ops):
            self.ops = ops
        elif ops is None:
            self.ops = []
        else:
            raise TypeError('ops must be callable, an iterable of callables, or `None`')
        self._run_report_ = None
        self.write_func = write_func

        self._log_dict = defaultdict(dict)

    @property
    def run_report_(self):
        """
        Pandas DataFrame of information about the most recent run.

        Stores input path in the index, output path as "outpath", 0/1
        indicating whether processing was skipped because a file already
        existed at the output path as "skipped_existing", whether
        processing failed due to a handled exception as
        "exception_handled", and a timestamp indicating when processing
        completed as "time_finished".

        Raises
        ------
        AttributeError
            If no run report is available because pipeline has not been
            run.
        """
        if self._run_report_ is None:
            raise AttributeError(
                'Pipeline has not been run, so there is no run report.'
            )
        return self._run_report_

    def __call__(
        self,
        inpaths: Iterable[PathOrStr],
        path_func: Callable[[PathOrStr], PathOrStr],
        n_jobs: int,
        skip_func: Optional[Callable[[PathOrStr, Any], bool]] = None,
    ) -> pd.DataFrame:
        """
        Run the pipeline.

        Across `n_jobs` threads, for each path in `inpaths`, if
        `skip_existing` and `self.check_existing_func(path_func(path))`
        are both `True`, do not do anything. Otherwise, use `load_func`
        to get the resource from that path, pipe its output through
        `ops`, and write out the result with `write_func`.

        Parameters
        ----------
        inpaths
            Iterable of string or Path objects pointing to resources to
            be processed and written out.
        path_func
            Function that takes each input path and returns the desired
            corresponding output path.
        n_jobs
            Number of threads to use.
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
        CreeveyProcessingError
            If any unhandled errors arise during file processing

        Notes
        -----
        Logs a warning when `skip_existing` is `True`.

        Stores a run report in `self.run_report_`
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = [
                executor.submit(self._pipeline_func, path, path_func, skip_func)
                for path in inpaths
            ]
            for inpath, future in zip(
                tqdm(inpaths), concurrent.futures.as_completed(futures)
            ):
                try:
                    future.result()
                    self._log_dict[inpath]['error'] = None
                except Exception as e:
                    self._log_dict[inpath]['error'] = e

        run_report = pd.DataFrame.from_dict(self._log_dict, orient='index')
        # breakpoint()
        self._run_report_ = run_report.loc[
            :,
            RUN_REPORT_COLS + [col for col in run_report if col not in RUN_REPORT_COLS],
        ]
        self._log_dict = defaultdict(dict)

    def _pipeline_func(
        self, inpath: PathOrStr, outpath_func: PathOrStr, skip_func
    ) -> None:
        """
        Process one file

        Use `self.load_func` to load the file at `inpath` into memory,
        pipe the result through the functions in `self.ops`, and use
        `self.write_func` to write it to `outpath_func(inpath)`.

        If `skip_existing` is `True`, check up front whether
        `self.check_existing_func(outpath_func(inpath))` exists. If it
        does, skip the file.

        Catch `exceptions_to_catch` if they arise during file
        processing.

        Parameters
        ----------
        inpath
            Input path
        outpath_func
            Function that takes input path and returns output path
        skip_existing
            Whether or not to skip processing if output path is occupied
        exceptions_to_catch
            Exception types to catch

        Note
        ----
        Records results in a dict within `self._log_dict[inpath]` with
        the following keys

        outpath
            output path
        skipped_existing
            0/1 indicating whether existing file was skipped
        time_finished
            Timestamp indicating when processing finished
        """
        self._log_dict[inpath]['outpath'] = outpath_func(inpath)
        if skip_func is not None and skip_func(
            inpath, self._log_dict[inpath]['outpath']
        ):
            self._log_dict[inpath]['skipped'] = True
            logging.debug(
                f'Skipping {inpath} because there is already a file at corresponding '
                f'output path {self._log_dict[inpath]["outpath"]}'
            )
            self._log_dict[inpath]['time_finished'] = datetime.now()
        else:
            self._log_dict[inpath]['skipped'] = False
            try:
                self._run_pipeline_func(inpath, self._log_dict[inpath]['outpath'])
            finally:
                self._log_dict[inpath]['time_finished'] = datetime.now()

    def _run_pipeline_func(self, inpath, outpath):
        stage = self.load_func(inpath)
        for op in self.ops:
            stage = op(stage)
        self.write_func(stage, outpath)


class CustomReportingPipeline(Pipeline):
    """
    Class for defining file processing pipelines with custom run
    recording.

    Differences from Pipeline parent class:

        `load_func`, each element of `ops`, and `write_func` must each
        accept the string or `Path` object indicating the input item's
        location as an additional positional argument.

        Each element of `ops` and `write_func` must each accept a
        `defaultdict(dict)` object as an additional positional argument.
        Functions defined in Creevey call this item `log_dict`.

    Inside those functions, adding items to `log_dict[inpath]` causes
    them to be added to the "run record" DataFrame that the pipeline
    returns. See Creevey's README for further explanation.
    """

    def _run_pipeline_func(self, inpath, outpath):
        stage = self.load_func(inpath, log_dict=self._log_dict)
        for op in self.ops:
            stage = op(stage, inpath=inpath, log_dict=self._log_dict)
        self.write_func(stage, outpath, inpath=inpath, log_dict=self._log_dict)
