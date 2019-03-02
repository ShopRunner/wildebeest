from collections import defaultdict
import logging
from pathlib import Path
import time
from typing import Any, Callable, Iterable, Optional, Tuple, Union

from joblib import delayed, Parallel
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
    write_func
        Callable that takes the output of the last element of `ops` (or
        the output of `load_func` if `ops` is `None` or empty) and a
        string or `Path` object and writes the former to the location
        specified by the latter.
    """

    def __init__(
        self,
        load_func: Callable[[PathOrStr], Any],
        ops: Optional[Iterable[Callable[[Any], Any]]],
        write_func: Callable[[Any, PathOrStr], None],
    ) -> None:
        """
        Compose the provided functions, and store them as attributes.

        Store `load_func`, `ops`, and `write_func` as attributes with
        the corresponding names. Create an additional attribute
        `pipeline_func` that composes those functions for when `run`
        is called.

        See the `Pipeline` docstring for information about the form that
        `load_func`, `ops`, and `write_func` are expected to take.
        """
        self.load_func = load_func
        self.ops = ops if ops is not None else []
        self.write_func = write_func
        self.pipeline_func = self._build_pipeline_func()

    def _build_pipeline_func(self) -> Callable:
        def pipeline_func(
            inpath: PathOrStr,
            outpath_func: PathOrStr,
            skip_existing: bool,
            log_dict: dict,
            exceptions_to_catch: Optional[Tuple[Exception]] = None,
        ):
            outpath = outpath_func(inpath)
            skipped_existing = False
            exception_handled = False

            if skip_existing and Path(outpath).is_file():
                skipped_existing = True
                logging.warning(
                    f'Skipping {inpath} because there is already a file at corresponding '
                    f'output path {outpath}'
                )
            else:
                try:
                    stage = self.load_func(inpath)
                    for op in self.ops:
                        stage = op(stage)
                    self.write_func(stage, outpath)
                except exceptions_to_catch as e:
                    exception_handled = True
                    logging.error(e, inpath)

            inpath_logs = log_dict[inpath]
            inpath_logs['time_finished'] = time.time()
            inpath_logs['outpath'] = outpath
            inpath_logs['skipped_existing'] = int(skipped_existing)
            inpath_logs['exception_handled'] = int(exception_handled)

        return pipeline_func

    def run(
        self,
        inpaths: Iterable[PathOrStr],
        path_func: Callable[[PathOrStr], PathOrStr],
        n_jobs: int,
        skip_existing: bool = True,
        exceptions_to_catch: Optional[Union[Exception, Tuple[Exception]]] = None,
    ) -> None:
        """
        Run the pipeline.

        Across `n_jobs` threads, for each path in `inpaths`, if
        `skip_existing` is `True` and `path_func` of that path exists,
        do not do anything. Otherwise, use `load_func` to get the
        resource from that path, pipe its output through `ops`, and
        write out the result with `write_func`.

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
            files. Log a warning for any files that are skipped.
        exceptions_to_catch
            Tuple of exception types to catch. An exception of one of
            these types will be logged with logging level ERROR and the
            relevant file will be skipped.
        """
        log_dict = defaultdict(dict)

        Parallel(n_jobs=n_jobs, prefer='threads')(
            delayed(self.pipeline_func)(
                path, path_func, skip_existing, log_dict, exceptions_to_catch
            )
            for path in tqdm(inpaths)
        )

        run_report = pd.DataFrame.from_dict(log_dict, orient='index')

        return run_report
