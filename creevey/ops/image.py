from typing import DefaultDict, Optional, Tuple

import cv2 as cv
import numpy as np

from creevey.constants import PathOrStr


def record_mean_brightness(
    image: np.array, inpath: PathOrStr, log_dict: DefaultDict[str, dict]
) -> np.array:
    """
    Calculate mean image brightness

    Image is assumed to be grayscale if it has a single channel, RGB if
    it has three channels, RGBA if it has four. Brightness is calculated
    by converting to grayscale if necessary and then taking the mean
    pixel value.

    Parameters
    ----------
    image
    inpath
        Image input path
    log_dict
        Dictionary of image metadata

    Side effect
    -----------
    Adds a "mean_brightness" items to log_dict[inpath]
    """
    if len(image.shape) == 3:
        num_bands = image.shape[2]
    elif len(image.shape) == 2:
        num_bands = 1
    else:
        raise ValueError('Image array must have two or three dimensions')

    if num_bands == 1:
        image_gray = image
    elif num_bands == 3:
        image_gray = cv.cvtColor(src=image, code=cv.COLOR_RGB2GRAY)
    elif num_bands == 4:
        image_gray = cv.cvtColor(src=image, code=cv.COLOR_RGBA2GRAY)
    else:
        raise ValueError(
            f'{inpath} image has {num_bands} channels. Only 1-channel '
            f'grayscale, 3-channel RGB, and 4-channel RGBA images are '
            f'supported.'
        )
    log_dict[inpath]['mean_brightness'] = image_gray.mean()

    return image


def resize(
    image: np.array,
    shape: Optional[Tuple[int, int]] = None,
    min_dim: Optional[int] = None,
    **kwargs,
) -> np.array:
    """
    Resize input image

    `shape` or `min_dim` needs to be specified with `partial` before
    this function can be used in a Creevey pipeline.

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Parameters
    ----------
    image
        NumPy array with two spatial dimensions and optionally an
        additional channel dimension
    shape
        Desired output shape in pixels in the form (height, width)
    min_dim
        Desired minimum spatial dimension in pixels; image will be
        resized so that it has this length along its smaller spatial
        dimension while preseving aspect ratio as closely as possible.
        Exactly one of `shape` and `min_dim` must be `None`.

    Returns
    -------
    NumPy array with specified shape
    """
    _validate_resize_inputs(shape, min_dim)
    if min_dim is not None:
        shape = _find_min_dim_shape(image, min_dim)
    resized = cv.resize(image, dsize=shape[::-1])
    return resized


def _validate_resize_inputs(shape, min_dim) -> None:
    if (shape is None) + (min_dim is None) == 1:
        pass
    else:
        raise ValueError('Exactly one of `shape` and `min_dim` must be None')


def _find_min_dim_shape(image, min_dim):
    in_height, in_width = image.shape[:2]
    aspect_ratio = in_width / in_height
    format = 'tall' if aspect_ratio < 1 else 'wide'
    if format == 'tall':
        out_width = min_dim
        out_height = round(out_width / aspect_ratio, 1)
    else:
        out_height = min_dim
        out_width = round(out_height * aspect_ratio, 1)
    return (int(out_height), int(out_width))
