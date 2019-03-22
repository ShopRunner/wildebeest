import cv2 as cv
import numpy as np

from creevey.constants import PathOrStr
from creevey.load_funcs import get_response


def load_image_from_url(inpath: str, **kwargs) -> np.array:
    """
    Download an image

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Parameters
    ----------
    inpath
        Image URL

    Returns
    -------
    Image as NumPy array
    """
    response = get_response(inpath)
    image = _load_image_from_response(response)
    return image


def _load_image_from_response(response):
    image = np.asarray(bytearray(response.content), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f'{response.url} failed to load')
    _convert_to_rgb_if_needed(image)

    return image


def load_image_from_disk(inpath: PathOrStr, **kwargs) -> np.array:
    """
    Load image from disk

    Assumes that image is RGB(A) if it has at least three channels.

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Parameters
    ----------
    inpath
        Path to local image file

    Returns
    -------
    Image file contents as a NumPy array

    Raises
    ------
    ValueError if image fails to load
    """
    # As of mid-2018 OpenCV is faster than Matplotlib or Pillow for IO
    image = cv.imread(str(inpath), cv.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f'{inpath} failed to load')
    _convert_to_rgb_if_needed(image)
    return image


def _convert_to_rgb_if_needed(image: np.array) -> np.array:
    """
    Reverse order of first three channels if image has at least three

    Used as a helper function when loading images with OpenCV, which
    uses BGR channel ordering rather than the more common RGB.
    """
    num_channels = 1 if len(image.shape) == 2 else image.shape[2]
    if num_channels >= 3:
        # OpenCV loads as BGR, so reverse order of first three channels
        image[:, :, :3] = image[:, :, 2::-1]
    return image
