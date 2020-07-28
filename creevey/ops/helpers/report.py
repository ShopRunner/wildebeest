"""Code for reporting information calculating during processing."""
from functools import partial
from typing import Any, Callable, DefaultDict, Hashable

from wildebeest.constants import PathOrStr


def report_output(
    func_input: Any,
    func: Callable,
    inpath: PathOrStr,
    log_dict: DefaultDict[str, dict],
    key: Hashable,
) -> Any:
    """
    Add the output of a function to `log_dict[inpath][key]`.

    Return the input to that function in order to pass it along within a
    pipeline.

    Intended to be used within a `CustomReportingPipeline` to add the
    output of the function to the run report.

    Examples
    --------
    >>> from functools import partial
    >>>
    >>> from wildebeest import CustomReportingPipeline
    >>> from wildebeest.load_funcs.image import load_image_from_url
    >>> from wildebeest.ops import report_output
    >>> from wildebeest.ops.image import calculate_mean_brightness
    >>> from wildebeest.path_funcs import join_outdir_filename_extension
    >>> from wildebeest.write_funcs.image import write_image
    >>>
    >>> report_mean_brightness = partial(
    >>>     report_output, func=calculate_mean_brightness, key='mean_brightness'
    >>> )
    >>>
    >>> report_brightness_pipeline = CustomReportingPipeline(
    >>>     load_func=load_image_from_url, ops=[report_mean_brightness], write_func=write_image
    >>> )
    >>>
    >>> image_filenames = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
    >>> image_urls = [f'https://bit.ly/{filename}' for filename in image_filenames]
    >>>
    >>> keep_filename_png_in_cwd = partial(
    >>>     join_outdir_filename_extension, outdir='.', extension='.png'
    >>> )
    >>> report_brightness_pipeline(
    >>>     inpaths=image_urls,
    >>>     path_func=keep_filename_png_in_cwd,
    >>>     n_jobs=1,
    >>>     skip_existing=False,
    >>> )
    >>> print(report_brightness_pipeline.run_report_)
                                mean_brightness  ... time_finished
    https://bit.ly/2RsJ8EQ        78.570605  ...  1.571842e+09
    https://bit.ly/2SCv0q7       130.348113  ...  1.571842e+09
    https://bit.ly/2TqoToT        82.677745  ...  1.571842e+09
    https://bit.ly/2TsO6Pc       151.596546  ...  1.571842e+09
    https://bit.ly/2VocS58        72.072578  ...  1.571842e+09
    https://bit.ly/2scKPIp       117.491313  ...  1.571842e+09

    Parameters
    ----------
    func_input
        Input to `func`
    func
        Function whose output is to be reported
    inpath
        Input path associated with `func_input`
    log_dict
        Dictionary for storing function output (in
        `log_dict[inpath][key]`)
    key
        Dictionary key in which to store function output for each
        inpath

    Returns
    -------
    Any
        func_input

    Note
    ----
    Assigns `func(func_input)` to `log_dict[inpath][key]`
    """
    result = func(func_input)
    log_dict[inpath][key] = result
    return func_input


def get_report_output_decorator(key: Hashable) -> Callable:
    """
    Get a decorator that modifies a function to add its output to
    `log_dict[inpath][key]` and return its input.

    Intended to be used to adapt a function for use within a
    `CustomReportingPipeline`.

    Examples
    --------
    >>> from functools import partial
    >>>
    >>> from wildebeest import CustomReportingPipeline
    >>> from wildebeest.load_funcs.image import load_image_from_url
    >>> from wildebeest.ops import get_report_output_decorator
    >>> from wildebeest.ops.image import calculate_mean_brightness
    >>> from wildebeest.path_funcs import join_outdir_filename_extension
    >>> from wildebeest.write_funcs.image import write_image
    >>>
    >>>
    >>> @get_report_output_decorator(key='mean_brightness')
    >>> def report_mean_brightness(image):
    >>>     return calculate_mean_brightness(image)
    >>>
    >>>
    >>> report_brightness_pipeline = CustomReportingPipeline(
    >>>     load_func=load_image_from_url, ops=[report_mean_brightness], write_func=write_image
    >>> )
    >>>
    >>> image_filenames = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
    >>> image_urls = [f'https://bit.ly/{filename}' for filename in image_filenames]
    >>>
    >>> keep_filename_png_in_cwd = partial(
    >>>     join_outdir_filename_extension, outdir='.', extension='.png'
    >>> )
    >>> report_brightness_pipeline(
    >>>     inpaths=image_urls,
    >>>     path_func=keep_filename_png_in_cwd,
    >>>     n_jobs=1,
    >>>     skip_existing=False,
    >>> )
    >>> print(report_brightness_pipeline.run_report_)
                                mean_brightness  ... time_finished
    https://bit.ly/2RsJ8EQ        78.570605  ...  1.571843e+09
    https://bit.ly/2SCv0q7       130.348113  ...  1.571843e+09
    https://bit.ly/2TqoToT        82.677745  ...  1.571843e+09
    https://bit.ly/2TsO6Pc       151.596546  ...  1.571843e+09
    https://bit.ly/2VocS58        72.072578  ...  1.571843e+09
    https://bit.ly/2scKPIp       117.491313  ...  1.571843e+09


    Parameters
    ----------
    key
        Dictionary key in which to store function output for each
        inpath
    """
    # noqa: D202
    def report_output_decorator(func):
        return partial(report_output, func=func, key=key)

    return report_output_decorator
