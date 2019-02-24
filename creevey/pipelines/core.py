from functools import partial, reduce
import os
from typing import Any, Callable, Iterable, Optional

from creevey.constants import PathOrStr
from joblib import delayed, Parallel
from tqdm import tqdm


class Pipeline:
    def __init__(
        self,
        load_func: Callable[[PathOrStr], Any],
        ops: Optional[Iterable[Callable]],
        write_func: Callable[[Any, PathOrStr, Callable[[PathOrStr], PathOrStr]], None],
    ):
        self.load_func = load_func
        self.ops = ops if ops is not None else []
        self.write_func = write_func
        self.pipeline_func = self._build_pipeline_func()

    def _build_pipeline_func(self):
        def pipeline_func(
            inpath: PathOrStr, outpath_func: PathOrStr, skip_existing: bool
        ):
            outpath = outpath_func(inpath)
            if skip_existing and os.path.isfile(outpath):
                pass
            else:
                thing = self.load_func(inpath)
                for op in self.ops:
                    thing = op(thing)
                self.write_func(thing, outpath)

        return pipeline_func

    def run(
        self,
        inpaths: Iterable[PathOrStr],
        outpath_func: Callable[[PathOrStr], PathOrStr],
        n_jobs: int,
        skip_existing: bool = True,
    ):
        Parallel(n_jobs=n_jobs, prefer='threads')(
            delayed(self.pipeline_func)(path, outpath_func, skip_existing)
            for path in tqdm(inpaths)
        )


def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)
