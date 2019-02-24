import cv2 as cv
import numpy as np

from creevey.load_funcs.load_funcs import get_response


def download_image(url: str) -> None:
    response = get_response(url)
    image = _load_image_from_response(response)
    return image


def _load_image_from_response(response):
    image = np.asarray(bytearray(response.content), dtype="uint8")
    image = cv.imdecode(image, -1)  # load as-is, e.g. including alpha channel
    return image
