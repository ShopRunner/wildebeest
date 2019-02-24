import io
import logging
from retrying import retry
import threading

import cv2 as cv
import numpy as np
import requests


threadLocal = threading.local()


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
def get_response(url: str) -> None:
    session = _get_session()
    response = session.get(url)
    _check_status(response)
    return response


def _get_session():
    if getattr(threadLocal, "session", None) is None:
        threadLocal.session = requests.Session()
    return threadLocal.session


def _check_status(response):
    if response.status_code == 200:
        pass
    elif _log_as_error_on_status_code(response.status_code):
        logging.error(
            f'Failed to download {url} with status code {response.status_code}'
        )
    elif _retry_on_status_code(response.status_code):
        logging.debug(f'Retrying {url} with status code {response.status_code}')
        raise _HTTPErrorToRetry
    elif _raise_on_status_code(response.status_code):
        raise requests.exceptions.HTTPError
    else:
        requests.raise_for_status()
