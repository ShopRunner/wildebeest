from typing import Tuple

import cv2 as cv
import numpy as np


def resize(image: np.array, shape: Tuple[int, int]) -> np.array:
    """
    Resize input image to the specified shape.
    Parameters
    ----------
    image:
        NumPy array with two spatial dimensions and optionally an
        additional channel dimension
    shape:
        Desired output shape in the form (height, width)
    Returns
    -------
    NumPy array with specified shape
    """
    resized = cv.resize(image, dsize=shape[::-1])
    return resized
