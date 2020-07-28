"""Functions that record information about an image"""
import cv2 as cv
import numpy as np

from wildebeest.ops.helpers.report import get_report_output_decorator
from wildebeest.ops.image.transforms import convert_to_grayscale


def calculate_mean_brightness(image: np.array) -> float:
    """
    Calculate mean image brightness

    Brightness is calculated by converting to grayscale if necessary and
    then taking the mean pixel value. Assumes image is grayscale, RGB,
    or RGBA.
    """
    return convert_to_grayscale(image).mean()


@get_report_output_decorator(key='mean_brightness')
def report_mean_brightness(image):  # noqa: D103
    return calculate_mean_brightness(image)


def calculate_dhash(image: np.array, sqrt_hash_size: int = 8) -> np.array:
    """
    Calculate difference hash of image.

    As a rule of thumb, with `sqrt_hash_size=8`, hashes from two images
    should typically have a Hamming distance less than 10 if and only if
    those images are "duplicates", with some robustness to sources of
    noise such as resizing and JPEG artifacts, where the Hamming
    distance between two hashes `a` and `b` is computed as
    `bin(a ^ b).count("1")`.

    Assumes image is grayscale, RGB, or RGBA.

    Note
    ----
    Based on Adrian Rosebrock, "Building an Image Hashing Search Engine
    with VP-Trees and OpenCV", *PyImageSearch*,
    https://www.pyimagesearch.com/2019/08/26/building-an-image-hashing-search-engine-with-vp-trees-and-opencv/,
    accessed on 18 October 2019.

    Parameters
    ----------
    image
    sqrt_hash_size
        Side length of 2D array used to compute hash, so that hash will
        be up to `sqrt_hash_size`^2 bits long.
    """
    im_mod = convert_to_grayscale(image)
    im_mod = cv.resize(im_mod, (sqrt_hash_size + 1, sqrt_hash_size))
    diff = im_mod[:, 1:] > im_mod[:, :-1]
    return sum(2 ** i for (i, v) in enumerate(diff.flatten()) if v)


@get_report_output_decorator(key='dhash')
def report_dhash(image, sqrt_hash_size: int = 8):  # noqa: D103
    return calculate_dhash(image=image, sqrt_hash_size=sqrt_hash_size)
