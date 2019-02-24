from typing import Optional, Tuple

import cv2 as cv
import numpy as np


def resize(
    image: np.array,
    shape: Optional[Tuple[int, int]] = None,
    min_dim: Optional[int] = None,
) -> np.array:
    """
    Resize input image

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
    return (int(out_width), int(out_height))
