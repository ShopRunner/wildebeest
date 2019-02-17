from functools import partial, reduce
import os
from typing import Any, Callable, Iterable, Optional

from creevey.util.constants import PathOrStr
from joblib import delayed, Parallel
from tqdm import tqdm


class Pipeline:
    def __init__(
        self,
        load_func: Callable[[PathOrStr], Any],
        ops: Optional[Iterable[Callable]],
        write_func: Callable[[Any, PathOrStr, Callable[[PathOrStr], PathOrStr]], None],
        parallel_strategy: Optional[str] = None,
    ):
        self.pipeline_func = _build_pipeline_func(load_func, ops, write_func)

        self.parallel_strategy = parallel_strategy
        self._validate_parallel_strategy()

    def _validate_parallel_strategy(self):
        supported_parallel_strategies = (None, 'threads', 'processes')
        if self.parallel_strategy not in supported_parallel_strategies:
            raise ValueError(
                f'parallel_strategy must be one of {supported_parallel_strategies}'
            )

    def _build_pipeline_func(self, load_func, ops, write_func):
        def pipeline_func(
            inpath: PathOrStr, outpath_func: PathOrStr, skip_existing: bool
        ):
            outpath = outpath_func(inpath)
            if skip_existing and os.path.isfile(outpath):
                pass
            else:
                pipeline = compose(
                    load_func, *ops, partial(write_func, outpath=outpath)
                )
                pipeline(inpath)

        return pipeline_func

    def run(
        self,
        inpaths: Iterable[PathOrStr],
        outpath_func: Callable[[PathOrStr], PathOrStr],
        n_jobs: int,
        skip_existing: bool = True,
    ):
        Parallel(n_jobs=n_jobs, prefer=prefer)(
            delayed(self.pipeline_func)(path, outpath_func, skip_existing)
            for path in tqdm(inpaths)
        )


def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)
