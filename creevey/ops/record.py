import functools
from typing import Any, Callable, Hashable

from creevey.constants import PathOrStr


def record(
    key: Hashable, func: Callable, func_input: Any, inpath: PathOrStr, log_dict: dict
):
    log_dict[inpath][key] = func(func_input)


def get_record_decorator(key: Hashable, log_dict: dict) -> Callable:
    def record_decorator(func, func_input, inpath):
        @functools.wraps(func)
        def _inner_record_wrapper(func, func_input, inpath):
            return record(
                key=key,
                func=func,
                func_input=func_input,
                inpath=inpath,
                log_dict=log_dict,
            )

        return _inner_record_wrapper

    return record_decorator
