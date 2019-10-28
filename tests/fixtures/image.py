import pytest

from creevey.load_funcs.image import load_image_from_disk
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
