import logging
import os
from retrying import retry
from typing import Callable

import requests


def _log_as_error_on_status_code(status_code: int):
    return status_code in [403, 404]


def _retry_on_status_code(status_code: int):
    return status_code >= 500


def _raise_on_status_code(status_code: int):
    return status_code == 400


class _HTTPErrorToRetry(requests.exceptions.HTTPError):
    pass


def _is_connection_error(exception):
    return isinstance(
        exception, (requests.exceptions.ConnectionError, _HTTPErrorToRetry)
    )


@retry(
    retry_on_exception=_is_connection_error,
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
    stop_max_attempt_number=10,
)
def download(
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
    retry, with a max of 10 seconds.

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
        logging.warning(
            f'Skipping {url} download because there is already a file at {outpath}'
        )
    else:
        if os.path.isfile(outpath):
            logging.warning(f'Overwriting existing file at {outpath}')
        response = requests.get(url)
        if _log_as_error_on_status_code(response.status_code):
            logging.error(
                f'Failed to download {url} with status code {response.status_code}'
            )
        elif _retry_on_status_code(response.status_code):
            logging.debug(f'Retrying {url} with status code {response.status_code}')
            raise _HTTPErrorToRetry
        elif _raise_on_status_code(response.status_code):
            raise requests.exceptions.HTTPError
        elif response.status_code == 200:
            write_func(response, outpath)
        else:
            requests.raise_for_status()
