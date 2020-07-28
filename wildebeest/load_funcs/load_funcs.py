"""Functions for loading generic data"""
import logging
import threading

import requests
from retrying import retry

threadLocal = threading.local()


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
def get_response(url: str, timeout: int = 5, **kwargs) -> requests.models.Response:
    """
    Make a GET request to the specified URL and return the response.

    Maintain a common session within each thread to reduce request
    overhead.

    Note
    ----
    Retry up to ten times on `requests.exceptions.ConnectionError`
    instances and 5xx status codes, waiting 2^x seconds between each
    retry, with a max of 10 seconds.

    Log an error without retrying or raising for 403 and 404 status
    codes.

    Raise `requests.exceptions.HTTPError` for other non-200 status
    codes.

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Parameters
    ----------
    url
        URL of file to download
    timeout
        Number of seconds to wait before timing out if server has not
        issued a response.
    """
    session = _get_session()
    response = session.get(url, timeout=timeout)
    _check_status(url, response)
    return response


def _get_session():
    if getattr(threadLocal, 'session', None) is None:
        threadLocal.session = requests.Session()
    return threadLocal.session


def _check_status(url, response):
    if response.status_code == 200:
        pass
    elif 600 > response.status_code > 499:
        logging.debug(f'Retrying {url} with status code {response.status_code}')
        raise _HTTPErrorToRetry
    elif response.status_code in [403, 404]:
        logging.error(
            f'Failed to download {url} with status code {response.status_code}'
        )
    else:
        response.raise_for_status()


class _HTTPErrorToRetry(requests.exceptions.HTTPError):
    pass
