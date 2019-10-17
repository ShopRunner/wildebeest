from collections import defaultdict
import operator

import cv2 as cv
import numpy as np
import pytest

from creevey.load_funcs.image import load_image_from_disk
from creevey.ops.image import centercrop, record_mean_brightness, resize, trim_padding
from tests.conftest import SAMPLE_DATA_DIR


@pytest.fixture
def sample_image_square_rgb():
    filename = 'creevey_rgb.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_tall_grayscale():
    filename = 'creevey_gray.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgba():
    filename = 'creevey_rgba.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


def test_resize_validation(sample_image_square_rgb):
    with pytest.raises(ValueError):
        resize(sample_image_square_rgb, shape=(10, 10), min_dim=5)


def test_resize_with_shape(sample_image_square_rgb):
    expected_shape = (5, 8)
    image = resize(sample_image_square_rgb, shape=expected_shape)
    actual_shape = image.shape[:2]
    assert actual_shape == expected_shape


def test_resize_square_with_min_dim(sample_image_square_rgb):
    image = resize(sample_image_square_rgb, min_dim=50)
    actual_shape = image.shape[:2]
    expected_shape = (50, 50)
    assert actual_shape == expected_shape


def test_resize_tall_with_min_dim(sample_image_tall_grayscale):
    image = resize(sample_image_tall_grayscale, min_dim=50)
    actual_shape = image.shape
    expected_shape = (68, 50)
    assert actual_shape == expected_shape


def test_resize_wide_with_min_dim(sample_image_tall_grayscale):
    sample_image_wide = sample_image_tall_grayscale.transpose()
    image = resize(sample_image_wide, min_dim=50)
    actual_shape = image.shape
    expected_shape = (50, 68)
    assert actual_shape == expected_shape


def test_resize_accepts_custom_reporting_args(sample_image_square_rgb):
    resize(sample_image_square_rgb, shape=(5, 8), inpath='fake', log_dict={})


def test_mean_brightness_grayscale(sample_image_tall_grayscale):
    log_dict = defaultdict(dict)
    image_path = SAMPLE_DATA_DIR / 'creevey_rgb.jpg'
    record_mean_brightness(
        sample_image_tall_grayscale, inpath=image_path, log_dict=log_dict
    )
    assert isinstance(log_dict[image_path]['mean_brightness'], float)


def test_mean_brightness_all_black(sample_image_tall_grayscale):
    log_dict = defaultdict(dict)
    image_path = 'foo'
    black_image = np.zeros(sample_image_tall_grayscale.shape, dtype='uint8')
    record_mean_brightness(black_image, inpath=image_path, log_dict=log_dict)
    assert log_dict[image_path]['mean_brightness'] == 0


def test_mean_brightness_rgb(sample_image_square_rgb):
    log_dict = defaultdict(dict)
    image_path = SAMPLE_DATA_DIR / 'creevey_rgb.jpg'
    record_mean_brightness(
        sample_image_square_rgb, inpath=image_path, log_dict=log_dict
    )
    assert isinstance(log_dict[image_path]['mean_brightness'], float)


def test_mean_brightness_rgba(sample_image_square_rgba):
    log_dict = defaultdict(dict)
    image_path = SAMPLE_DATA_DIR / 'creevey_rgba.png'
    record_mean_brightness(
        sample_image_square_rgba, inpath=image_path, log_dict=log_dict
    )
    assert isinstance(log_dict[image_path]['mean_brightness'], float)


def test_centercrop_square_rgb(sample_image_square_rgb):
    expected_shape = (16, 16, 3)
    actual_shape = centercrop(sample_image_square_rgb, reduction_factor=0.5).shape
    assert expected_shape == actual_shape


def test_centercrop_tall_greyscale(sample_image_tall_grayscale):
    expected_shape = (17, 12)
    actual_shape = centercrop(sample_image_tall_grayscale, reduction_factor=0.5).shape
    assert expected_shape == actual_shape


def test_centercrop_square_rgba(sample_image_square_rgba):
    expected_shape = (16, 16, 4)
    actual_shape = centercrop(sample_image_square_rgba, reduction_factor=0.5).shape
    assert expected_shape == actual_shape


def test_centercrop_reduction_factor(sample_image_square_rgb):
    expected_shape = (19, 19, 3)
    actual_shape = centercrop(sample_image_square_rgb, reduction_factor=0.6).shape
    assert expected_shape == actual_shape


def test_centercrop_accepts_custom_reporting_args(sample_image_square_rgb):
    centercrop(
        sample_image_square_rgb, reduction_factor=0.5, inpath='fake', log_dict={}
    )


def test_trim_padding_no_padding(sample_image_square_rgb):
    image = trim_padding(
        sample_image_square_rgb, thresh=0.95, comparison_op=operator.gt
    )
    np.testing.assert_almost_equal(image, sample_image_square_rgb)


def test_trim_padding_rgb(sample_image_square_rgb):
    im_padded = cv.copyMakeBorder(
        src=sample_image_square_rgb,
        top=np.random.randint(1, 100),
        bottom=np.random.randint(1, 100),
        left=np.random.randint(1, 100),
        right=np.random.randint(1, 100),
        borderType=cv.BORDER_CONSTANT,
        value=[251, 252, 253],
    )
    actual = trim_padding(im_padded, thresh=0.95, comparison_op=operator.gt)
    np.testing.assert_almost_equal(actual, sample_image_square_rgb)


def test_trim_padding_rgba(sample_image_square_rgba):
    im_padded = cv.copyMakeBorder(
        src=sample_image_square_rgba,
        top=np.random.randint(1, 100),
        bottom=np.random.randint(1, 100),
        left=np.random.randint(1, 100),
        right=np.random.randint(1, 100),
        borderType=cv.BORDER_CONSTANT,
        value=[251, 252, 253],
    )
    actual = trim_padding(im_padded, thresh=0.95, comparison_op=operator.gt)
    np.testing.assert_almost_equal(actual, sample_image_square_rgba)


def test_trim_padding_grayscale(sample_image_tall_grayscale):
    im_padded = cv.copyMakeBorder(
        src=sample_image_tall_grayscale,
        top=np.random.randint(1, 100),
        bottom=np.random.randint(1, 100),
        left=np.random.randint(1, 100),
        right=np.random.randint(1, 100),
        borderType=cv.BORDER_CONSTANT,
        value=251,
    )
    actual = trim_padding(im_padded, thresh=0.95, comparison_op=operator.gt)
    np.testing.assert_almost_equal(actual, sample_image_tall_grayscale)


def test_trim_black_padding_rgb(sample_image_square_rgb):
    im_padded = _add_black_padding(sample_image_square_rgb)
    actual = trim_padding(im_padded, thresh=0.05, comparison_op=operator.lt)
    np.testing.assert_almost_equal(actual, sample_image_square_rgb)


def _add_black_padding(im):
    l_pad = np.random.randint(1, 100)
    r_pad = np.random.randint(1, 100)
    t_pad = np.random.randint(1, 100)
    b_pad = np.random.randint(1, 100)
    im_padded = np.zeros(
        (t_pad + im.shape[0] + b_pad, l_pad + im.shape[1] + r_pad, 3), dtype=np.float32
    )
    im_padded[t_pad : t_pad + im.shape[0], l_pad : l_pad + im.shape[1]] = im
    return im_padded
