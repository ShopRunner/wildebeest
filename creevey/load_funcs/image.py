from typing import DefaultDict, Optional

import cv2 as cv
import numpy as np

from creevey.constants import PathOrStr
from creevey.load_funcs import get_response


def download_image(
    url: str, log_dict: Optional[DefaultDict[str, dict]] = None
) -> np.array:
    """
    Download an image

    Parameters
    ----------
    url
        Image URL
    log_dict
        Unused optional argument included in signature so that function
        can be used in a `CustomReportingPipeline`

    Returns
    -------
    Image as NumPy array
    """
    response = get_response(url)
    image = _load_image_from_response(response)
    return image


def _load_image_from_response(response):
    image = np.asarray(bytearray(response.content), dtype="uint8")
    image = cv.imdecode(image, -1)  # load as-is, e.g. including alpha channel
    return image


def load_image(
    path: PathOrStr, log_dict: Optional[DefaultDict[str, dict]] = None
) -> np.array:
    """
    Load image from disk

    Assumes that image is RGB(A) if it has at least three channels.

    Parameters
    ----------
    path
        Path to local image file
    log_dict
        Unused optional argument included in signature so that function
        can be used in a `CustomReportingPipeline`

    Returns
    -------
    Image file contents as a NumPy array

    Raises
    ------
    ValueError if image fails to load
    """
    # As of mid-2018 OpenCV is faster than Matplotlib or Pillow for IO
    image = cv.imread(str(path), cv.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f'{path} failed to load')

    num_channels = 1 if len(image.shape) == 2 else image.shape[2]
    if num_channels >= 3:
        # OpenCV loads as BGR, so reverse order of first three channels
        image[:, :, :3] = image[:, :, 2::-1]
    return image
