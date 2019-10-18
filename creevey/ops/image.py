from typing import Callable, DefaultDict, Optional, Tuple

import cv2 as cv
import numpy as np

from creevey.constants import PathOrStr


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

    Returns
    -------
    Slice of input image corresponding to a cropped area around the center
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

    Assumptions
    -----------
    - Image is grayscale, RGB, or RGBA.
    - Pixel values are scaled between either 0 and 1 or 0 and 255. If
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

    Returns
    -------
    Slice of input image corresponding to a cropped area with padding
    removed
    """
    im_gray = _convert_to_grayscale(image)
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


def _convert_to_grayscale(image: np.array) -> np.array:
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


def record_dhash(
    image: np.array,
    inpath: PathOrStr,
    log_dict: DefaultDict[str, dict],
    sqrt_hash_size: int = 8,
) -> np.array:
    """
    Record difference hash of image.

    As a rule of thumb, hashes from two images should typically have a
    Hamming distance less than 10 if and only if those images are
    "duplicates", with some robustness to sources of noise such as
    resizing and JPEG artifacts, where the Hamming distance between two
    hashes `a` and `b` is computed as follows.

    ```
    bin(int(a) ^ int(b)).count("1")
    ```

    Assumes image is grayscale, RGB, or RGBA.

    Source
    ------
    Adrian Rosebrock, "Building an Image Hashing Search Engine with
    VP-Trees and OpenCV", *PyImageSearch*,
    https://www.pyimagesearch.com/2019/08/26/building-an-image-hashing-search-engine-with-vp-trees-and-opencv/,
    accessed on 18 October 2019.

    Parameters
    ----------
    image
    inpath
        Image input path
    log_dict
        Dictionary of image metadata
    sqrt_hash_size
        Side length of 2D array used to compute hash, so that hash will
        be up to `sqrt_hash_size`^2 bits long.
    """
    im_mod = _convert_to_grayscale(image)
    im_mod = cv.resize(im_mod, (sqrt_hash_size + 1, sqrt_hash_size))
    diff = im_mod[:, 1:] > im_mod[:, :-1]
    log_dict[inpath]['dhash'] = sum(
        [2 ** i for (i, v) in enumerate(diff.flatten()) if v]
    )
    return image
