from unittest import mock

import numpy as np
import pytest
import responses
from requests.exceptions import HTTPError

from creevey.load_funcs.image import load_image_from_disk, load_image_from_url
from tests.conftest import SAMPLE_DATA_DIR

SAMPLE_DATA_BASE_URL = (
    'https://github.com/ShopRunner/creevey/raw/master/tests/sample_data'
)


@responses.activate
def test_load_error_406():
    filename = 'creevey_gray.jpg'
    url = f'{SAMPLE_DATA_BASE_URL}/{filename}'

    responses.add(
        responses.GET,
        url,
        status=406,
    )

    with pytest.raises(HTTPError):
        with mock.patch(
            'requests.Response',
        ):
            result = load_image_from_url(
                inpath=url,
            )

        assert result.status_code == 406


@pytest.fixture
def creevey_gray_local():
    filename = 'creevey_gray.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def creevey_gray_remote():
    filename = 'creevey_gray.jpg'
    url = f'{SAMPLE_DATA_BASE_URL}/{filename}'
    image = load_image_from_url(url)
    return image


@pytest.fixture
def creevey_rgb_local():
    filename = 'creevey_rgb.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def creevey_rgb_remote():
    filename = 'creevey_rgb.jpg'
    url = f'{SAMPLE_DATA_BASE_URL}/{filename}'
    image = load_image_from_url(url)
    return image


@pytest.fixture
def creevey_rgba_local():
    filename = 'creevey_rgba.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def creevey_rgba_remote():
    filename = 'creevey_rgba.png'
    url = f'{SAMPLE_DATA_BASE_URL}/{filename}'
    image = load_image_from_url(url)
    return image


def test_load_image_from_disk_grayscale_shape(creevey_gray_local):
    image = creevey_gray_local

    expected_shape = (34, 25)
    actual_shape = image.shape

    assert actual_shape == expected_shape


def test_load_image_from_disk_rgb_shape(creevey_rgb_local):
    image = creevey_rgb_local

    expected_shape = (32, 32, 3)
    actual_shape = image.shape

    assert actual_shape == expected_shape


def test_load_image_from_disk_rgba_shape(creevey_rgba_local):
    image = creevey_rgba_local

    expected_shape = (32, 32, 4)
    actual_shape = image.shape

    assert actual_shape == expected_shape


def test_load_image_from_disk_red():
    filename = 'red.png'
    path = SAMPLE_DATA_DIR / filename

    actual_image = load_image_from_disk(path)[:, :, :3]
    expected_image = np.zeros((32, 32, 3), dtype='uint8')
    expected_image[:, :, 0] = 255

    np.testing.assert_equal(actual_image, expected_image)


def test_load_image_from_disk_green():
    filename = 'green.png'
    path = SAMPLE_DATA_DIR / filename

    actual_image = load_image_from_disk(path)[:, :, :3]
    expected_image = np.zeros((32, 32, 3), dtype='uint8')
    expected_image[:, :, 1] = 255

    np.testing.assert_equal(actual_image, expected_image)


def test_load_image_from_disk_blue():
    filename = 'blue.png'
    path = SAMPLE_DATA_DIR / filename

    actual_image = load_image_from_disk(path)[:, :, :3]
    expected_image = np.zeros((32, 32, 3), dtype='uint8')
    expected_image[:, :, 2] = 255

    np.testing.assert_equal(actual_image, expected_image)


def test_load_image_from_url_gray(creevey_gray_local, creevey_gray_remote):
    np.testing.assert_equal(creevey_gray_remote, creevey_gray_local)


def test_load_image_from_url_rgb(creevey_rgb_local, creevey_rgb_remote):
    np.testing.assert_equal(creevey_rgb_local, creevey_rgb_remote)


def test_load_image_from_url_rgba(creevey_rgba_local, creevey_rgba_remote):
    np.testing.assert_equal(creevey_rgba_local, creevey_rgba_remote)
