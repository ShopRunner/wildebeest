import datetime
from functools import partial
import io
import logging
import os
from typing import Callable, Iterable, Optional

from joblib import delayed, Parallel
from PIL import Image
import requests
from retrying import retry
from tqdm import tqdm


def download_images_as_png(urls: Iterable[str],
                           outdir: Optional[str] = None,
                           path_func: Optional[Callable[[str], str]] = None,
                           skip_existing: bool = True,
                           write_log_path: Optional[str] = None,
                           n_jobs: int = 1,
                           ) -> None:
    """
    Download images and save as PNGs

    By default, each file is written to the working directory, with
    the filename in the URL and a ".png" extension. The `outdir`
    argument can be used to change to output directory while still using
    the filename in the URL and a ".png" extension. Alternatively, the
    `path_func` argument can be used to construct the output path from
    the input URL in any way you wish.

    Parameters
    ----------
    urls
        URLs of images to download
    outdir
        Desired output directory. Must be `None` if `path_func` is not
        `None`.
    path_func
        Function that takes a URL and returns the desired path for a
        local copy of the associated resource. Must be `None` if
        `outdir` is not `None`.
    skip_existing
        If True, skip any file for which the output path matches an
        existing file path. If False, overwrite such files. Either way,
        log an appropriate warning.
    write_log_path
        Desired path for logs of successful writes
    n_jobs
        Number of jobs to run in parallel

    Raises
    ------
    ValueError if neither `outdir` nor `path_func` is `None`.
    """
    if outdir is not None and path_func is not None:
        raise ValueError('At least one of `path_func` and `outdir` must be `None`.')
    elif path_func is None and outdir is None:
        outdir = '.'
    if outdir is not None:
        path_func = partial(replace_directory_and_extension, extension='.png', outdir=outdir)

    write_func = partial(write_response_as_png, write_log_path=write_log_path)

    download_files(urls,
                   path_func=path_func,
                   write_func=write_func,
                   skip_existing=skip_existing,
                   n_jobs=n_jobs,
                   )


def download_files(urls: Iterable[str],
                   path_func: Callable[[str], str],
                   write_func: Callable[[requests.Response, str], None],
                   skip_existing: bool = True,
                   n_jobs: int = 1,
                   ) -> None:
    """
    Make GET requests to the specified URLs and write the responses
    to disk.

    This function can be used directly, but it is primarily intended as
    a template for more specific functions such as
    `download_images_as_png`.

    Adds parallelization to `download_single_file`.

    Parameters
    ----------
    urls
        URLs of files to download
    path_func
        Function that takes a URL and returns the desired path for a
        local copy of the associated resource
    write_func
        Function that takes a `requests.Response` object and the desired
        path for a local copy of the associated resource and writes a
        copy of that resource to that location
    skip_existing
        If True, skip any file for which the output path matches an
        existing file path. If False, overwrite such files. Either way,
        log an appropriate warning.
    n_jobs
        Number of jobs to run in parallel
    """
    download_single_file_func = partial(download_single_file,
                                        path_func=path_func,
                                        write_func=write_func,
                                        skip_existing=skip_existing,
                                        )
    Parallel(n_jobs=n_jobs, prefer='threads')(
        delayed(download_single_file_func)(url) for url in tqdm(urls)
    )


def _is_connection_error(exception):
    return isinstance(
        exception, (requests.exceptions.ConnectionError, _HTTPErrorToRetry)
    )


@retry(retry_on_exception=_is_connection_error,
       wait_exponential_multiplier=1000,
       wait_exponential_max=10000,
       stop_max_attempt_number=10,
       )
def download_single_file(
        url: str,
        path_func: Callable[[str], str],
        write_func: Callable[[requests.Response, str], None],
        skip_existing: bool = True,
) -> None:
    """
    Make a GET request to the specified URL and write the response
    to disk.

    This function can be used directly, but it is primarily intended as
    a helper for `download_files`, which is in turn primarily intended
    as a template for more specific functions such as
    `download_images_as_png`.

    Error Handling
    --------------
    Retry up to ten times on `requests.exceptions.ConnectionError`
    instances and 5xx status codes, waiting 2^x seconds between each
    retry, up to 10 seconds.

    Log an error without retrying or raising for 403 and 404 status
    codes.

    Raise `requests.exceptions.HTTPError` for other non-200 status
    codes.

    Parameters
    ----------
    url
        URL of file to download
    path_func
        Function that takes a URL and returns the desired path for a
        local copy of the associated resource
    write_func
        Function that takes a requests.Response object and the desired
        path for a local copy of the associated resource and writes a
        copy of that resource to that location
    skip_existing
        If True, skip download if the output path matches an existing
        file path. If False, overwrite such files. Either way, log an
        appropriate warning.
    """
    outpath = path_func(url)
    skip_download = os.path.isfile(outpath) and skip_existing
    if skip_download:
        logging.warning(f'Skipping {url} download because there is already a file at {outpath}')
    else:
        if os.path.isfile(outpath):
            logging.warning(f'Overwriting existing file at {outpath}')
        response = requests.get(url)
        if _log_as_error_on_status_code(response.status_code):
            logging.error(f'Failed to download {url} with status code {response.status_code}')
        elif _retry_on_status_code(response.status_code):
            logging.debug(f'Retrying {url} with status code {response.status_code}')
            raise _HTTPErrorToRetry
        elif _raise_on_status_code(response.status_code):
            raise requests.exceptions.HTTPError
        elif response.status_code == 200:
            write_func(response, outpath)
        else:
            requests.raise_for_status()


def _log_as_error_on_status_code(status_code: int):
    return status_code in [403, 404]


def _retry_on_status_code(status_code: int):
    return status_code >= 500


def _raise_on_status_code(status_code: int):
    return status_code == 400


class _HTTPErrorToRetry(requests.exceptions.HTTPError):
    pass


def replace_directory_and_extension(
        inpath: str,
        extension: str,
        outdir: str = '.'
) -> str:
    """
    Construct path for local file by taking `outdir` as the directory,
    the filename of `inpath` as the filename, and `extension` as the file
    extension.

    Parameters
    ----------
    inpath
        Current file path
    extension
        Desired file extension. Can include the initial period (e.g.
        ".png") or not (e.g. "png").
    outdir
        Desired output directory

    Returns
    -------
    Path object for path constructed by concatenating `outdir`, the
    filename from `url`, and `extension`, with a period between the
    filename and the extension.
    """
    filename = os.path.basename(inpath)
    extension = extension if extension.startswith('.') else '.' + extension
    filename_with_ext = os.path.splitext(filename)[0] + extension
    outpath = os.path.join(outdir, filename_with_ext)
    return outpath


def write_response_as_png(response: requests.Response,
                          outpath: str,
                          write_log_path: Optional[str] = None,
                          ) -> None:
    """
    Write response contents to `path` as a PNG file.

    Creates output directory if necessary.

    Appends a record of successful writes to a CSV at
    `csv_write_log_path` if that argument is not `None`.

    Parameters
    ----------
    response
    outpath
        Desired output path ending with ".png"
    write_log_path
        Path to CSV file to which logs of successful writes are to be
        appended. That file is assumed to have headings "timestamp,"
        "url," and "local_path." If no file exists at that location,
        then one is created with those headings.

    Raises
    ------
    - ValueError if `outpath` does not end with ".png".
    - ValueError if `write_log_path` does not end with ".csv" and is not
        None.
    """
    if not outpath.endswith('png'):
        raise ValueError('`outpath` argument must end with .png')
    if write_log_path is not None and not write_log_path.endswith('csv'):
        raise ValueError('`write_log_path` argument must end with .csv if it is not `None`')

    outdir = os.path.dirname(outpath)
    if not os.path.isdir(outdir):
        # Will get a FileExistsError if another thread creates the
        # directory after we check for it here
        try:
            os.makedirs(outdir)
        except FileExistsError:
            pass

    if write_log_path is not None and not os.path.exists(write_log_path):
        _initialize_write_log(write_log_path)

    _save_response_content_as_png(response, outpath)

    if write_log_path is not None:
        _append_to_write_log(write_log_path, response.url, outpath)


def _initialize_write_log(path):
    with open(path, 'w') as write_log:
        write_log.write('timestamp,url,local_path\n')


def _save_response_content_as_png(response, path):
    image = Image.open(io.BytesIO(response.content))
    image_rgb = image.convert("RGB")
    image_rgb.save(path, format='PNG')


def _append_to_write_log(write_log_path, url, outpath):
    current_time = datetime.datetime.now()
    outpath = os.path.abspath(outpath)
    with open(write_log_path, 'a') as write_log:
        write_log.write(f'{current_time},{url},{outpath}\n')
