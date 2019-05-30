from collections import defaultdict

import numpy as np
import pytest

from creevey.load_funcs.image import load_image_from_disk
from creevey.ops.image import centercrop, record_mean_brightness, resize
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
