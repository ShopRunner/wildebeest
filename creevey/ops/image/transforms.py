"""Functions that take an image and return a transformed image"""
from typing import Callable, Optional, Tuple

import cv2 as cv
import numpy as np


def resize(
    image: np.array,
    shape: Optional[Tuple[int, int]] = None,
    min_dim: Optional[int] = None,
    **kwargs,
) -> np.array:
    """
    Resize input image

    `shape` or `min_dim` needs to be specified with `partial` before
    this function can be used in a Wildebeest pipeline.

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
    """
    _validate_resize_inputs(shape, min_dim)
    if min_dim is not None:
        shape = _find_min_dim_shape(image, min_dim)
    return cv.resize(image, dsize=shape[::-1])


def _validate_resize_inputs(shape, min_dim) -> None:
    if (shape is None) + (min_dim is None) != 1:
        raise ValueError('Exactly one of `shape` and `min_dim` must be None')


def centercrop(image: np.array, reduction_factor: float, **kwargs) -> np.array:
    """
    Crop the center out of an image

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Parameters
    ----------
    image
        Numpy array of an image. Function will handle 2D greyscale
        images, RGB, and RGBA image arrays
    reduction_factor
        scale of center cropped box, 1.0 would be the full image
        value of .4 means a box of .4*width and .4*height
    """
    height, width, *channels = image.shape

    w_scale = width * reduction_factor
    h_scale = height * reduction_factor

    left = int((width - w_scale) // 2)
    top = int((height - h_scale) // 2)
    right = int((width + w_scale) // 2)
    bottom = int((height + h_scale) // 2)

    return image[top:bottom, left:right]


def trim_padding(
    image: np.array, comparison_op: Callable, thresh: int, **kwargs
) -> np.array:
    """
    Remove padding from an image

    Remove rows and columns on the edges of the input image where the
    brightness on a scale of 0 to 1 satisfies `comparison_op` with
    respect to `thresh`. Brightness is evaluated by converting to
    grayscale and normalizing if necessary. For instance, using
    `thresh=.95` and `comparison_op=operator.gt` will result in removing
    near-white padding, while using using `thresh=.05` and
    `comparison_op=operator.lt` will remove near-black padding.

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Assumes:

        Image is grayscale, RGB, or RGBA.

        Pixel values are scaled between either 0 and 1 or 0 and 255. If
        image is scaled between 0 and 255, then some pixel has a value
        greater than 1.

    Parameters
    ----------
    image
        Numpy array of an image.
    comparison_op
        How to compare pixel values to `thresh`
    thresh
        Value to compare pixel values against
    """
    im_gray = convert_to_grayscale(image)
    im_gray = normalize_pixel_values(im_gray)
    keep = ~comparison_op(im_gray, thresh)
    x, y, w, h = cv.boundingRect(cv.findNonZero(keep.astype(int)))
    return image[y : y + h, x : x + w]


def normalize_pixel_values(image: np.array) -> np.array:
    """
    Normalize image so that pixel values are between 0 and 1

    Assumes pixel values are scaled between either 0 and 1 or 0 and 255.
    """
    if image.max() > 1:
        return image / 255
    else:
        return image


def convert_to_grayscale(image: np.array) -> np.array:
    """
    Convert image to grayscale.

    Assumes image is grayscale, RGB, or RGBA.
    """
    grayscale = image.ndim == 2
    if grayscale:
        im_gray = image
    else:
        rgba = image.shape[2] == 4
        if rgba:
            im_gray = cv.cvtColor(image, cv.COLOR_RGBA2GRAY)
        else:
            im_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    return im_gray


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


def flip_horiz(image: np.array) -> np.array:
    """Flip an image horizontally"""
    return cv.flip(image, flipCode=1)


def flip_vert(image: np.array) -> np.array:
    """Flip an image vertically"""
    return cv.flip(image, flipCode=0)


def rotate_90(image: np.array) -> np.array:
    """
    Rotate an image 90 degrees counterclockwise

    This function takes an image as numpy array and
    and outputs the image rotated 90 degrees counterclockwise.

    Assumes that the image is going to be rotated around center, and size of image
    will remain unchanged.

    This function takes numpy array of an image. Function will handle 2D greyscale
    images, RGB, and RGBA image arrays.
    """
    return cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)


def rotate_180(image: np.array) -> np.array:
    """
    Rotate an image 180 degrees

    This function takes an image as numpy array and
    and outputs the image rotated 180 degrees.

    Assumes that the image is going to be rotated around center, and size of image
    will remain unchanged.

    This function takes numpy array of an image. Function will handle 2D greyscale
    images, RGB, and RGBA image arrays.
    """
    return cv.rotate(image, cv.ROTATE_180)


def rotate_270(image: np.array) -> np.array:
    """
    Rotate an image 270 degrees counterclockwise

    This function takes an image as numpy array and
    and outputs the image rotated 270 degrees counterclockwise.

    Assumes that the image is going to be rotated around center, and size of image
    will remain unchanged.

    This function takes numpy array of an image. Function will handle 2D greyscale
    images, RGB, and RGBA image arrays.
    """
    return cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
