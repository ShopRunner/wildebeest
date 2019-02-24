from creevey.load_funcs.image import load_image
from creevey.ops.image import resize
import pytest

from tests.conftest import SAMPLE_DATA_DIR


@pytest.fixture
def sample_image():
    filename = 'creevey_rgb.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image(path)
    return image


@pytest.fixture
def sample_image_tall():
    filename = 'creevey_gray.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image(path)
    return image


def test_resize_validation(sample_image):
    with pytest.raises(ValueError):
        resize(sample_image, shape=(10, 10), min_dim=5)


def test_resize_with_shape(sample_image):
    expected_shape = (5, 8)
    image = resize(sample_image, shape=expected_shape)
    actual_shape = image.shape[:2]
    assert actual_shape == expected_shape


def test_resize_square_with_min_dim(sample_image):
    image = resize(sample_image, min_dim=50)
    actual_shape = image.shape[:2]
    expected_shape = (50, 50)
    assert actual_shape == expected_shape


def test_resize_tall_with_min_dim(sample_image_tall):
    image = resize(sample_image_tall, min_dim=50)
    actual_shape = image.shape
    expected_shape = (50, 68)
    assert actual_shape == expected_shape


def test_resize_wide_with_min_dim(sample_image_tall):
    sample_image_wide = sample_image_tall.transpose()
    image = resize(sample_image_wide, min_dim=50)
    actual_shape = image.shape
    expected_shape = (68, 50)
    assert actual_shape == expected_shape
