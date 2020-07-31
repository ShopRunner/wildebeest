"""Pipeline class definitions"""
from collections import defaultdict
from datetime import datetime
import logging
from typing import Any, Callable, Iterable, Optional, Tuple, Union

from joblib import delayed, Parallel
from numpy import iterable
import pandas as pd
from tqdm import tqdm

from wildebeest.constants import PathOrStr


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
    write_func
        Callable that takes the output of the last element of `ops` (or
        the output of `load_func` if `ops` is `None` or empty) and a
        string or `Path` object and writes the former to the location
        specified by the latter.
    ops
        Iterable of callables each of which takes a single positional
        argument. The first element of `ops` must accept the output of
        `load_func`, and each subsequent element must accept the output
        of the immediately preceding element. It is recommended that
        every element of `ops` take and return one common data structure
        (e.g. NumPy arrays for image data) so that those elements can
        be recombined easily.
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
        self.write_func = write_func
        self.ops = self._process_ops(ops)
        self._run_report_ = None
        self._log_dict = defaultdict(dict)

    def _process_ops(self, ops):
        if iterable(ops):
            return ops
        elif callable(ops):
            return [ops]
        elif ops is None:
            return []
        else:
            raise TypeError('ops must be callable, an iterable of callables, or `None`')

    @property
    def run_report_(self):
        """
        Pandas DataFrame of information about the most recent run.

        Stores input path in the index, output path as "outpath",
        Boolean indicating whether the file was skipped as "skipped",
        the repr of an exception object that was handled during
        processing if any as "error" (`np.nan` if no exception was
        handled), and a timestamp indicating when processing completed
        as "time_finished".

        May include additional custom fields in a
        `CustomReportingPipeline`.

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
        exceptions_to_catch: Optional[Union[Exception, Tuple[Exception]]] = Exception,
    ) -> pd.DataFrame:
        """
        Run the pipeline.

        Across `n_jobs` threads, for each path in `inpaths`, if
        `skip_func(path, path_func(path))` is `True`, skip that path.
        Otherwise, use `load_func` to get the resource from that path,
        pipe its output through `ops`, and write out the result with
        `write_func`.

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
        skip_func
            Callable that takes an input path and a prospective output
            path and returns a Boolean indicating whether or not that
            file should be skipped; for instance, use
            `lambda inpath, outpath: Path(outpath).is_file()` to avoid
            overwriting existing files.
        exceptions_to_catch
            Tuple of exception types to catch. An exception of one of
            these types will be logged with logging level ERROR and
            added to the run report, but the pipeline will continue to
            execute.

        Note
        ----
        Stores a run report in `self.run_report_`
        """
        Parallel(n_jobs=n_jobs, prefer='threads')(
            delayed(self._pipeline_func)(
                path, path_func, skip_func, exceptions_to_catch
            )
            for path in tqdm(inpaths)
        )

        logging.info('Processing finished. Creating run report.')
        self._run_report_ = pd.DataFrame.from_dict(self._log_dict, orient='index')
        self._log_dict = defaultdict(dict)
        # Default ns precision is overkill for most applications and
        # gives an error when writing to parquet.
        self._run_report_.loc[:, 'time_finished'] = self._run_report_.loc[
            :, 'time_finished'
        ].astype('datetime64[ms]')
        self._run_report_ = self._run_report_.reindex(
            columns=(
                RUN_REPORT_COLS
                + [col for col in self._run_report_ if col not in RUN_REPORT_COLS]
            )
        )
        self._run_report_.loc[:, "skipped"] = self._run_report_.loc[
            :, "skipped"
        ].fillna(False)

    def _pipeline_func(
        self,
        inpath: PathOrStr,
        outpath_func: PathOrStr,
        skip_func: Callable,
        exceptions_to_catch: Optional[Union[Exception, Tuple[Exception]]] = Exception,
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

        class _DummyException(Exception):
            pass

        if exceptions_to_catch is None:
            exceptions_to_catch = _DummyException

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
            try:
                self._run_pipeline_func(inpath, self._log_dict[inpath]['outpath'])
            except exceptions_to_catch as e:
                self._log_dict[inpath]['error'] = repr(e)
                logging.error(f'{type(e)} exception on {inpath}: {e}')
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
        Functions defined in Wildebeest call this item `log_dict`.

    Inside those functions, adding items to `log_dict[inpath]` causes
    them to be added to the "run record" DataFrame that the pipeline
    returns.
    """

    def _run_pipeline_func(self, inpath, outpath):
        stage = self.load_func(inpath, log_dict=self._log_dict)
        for op in self.ops:
            stage = op(stage, inpath=inpath, log_dict=self._log_dict)
        self.write_func(stage, outpath, inpath=inpath, log_dict=self._log_dict)
