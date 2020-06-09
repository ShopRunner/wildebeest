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


@pytest.fixture
def sample_image_square_rgba_flipped_horiz():
    filename = 'creevey_rgba_flipped_horiz.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgba_flipped_vert():
    filename = 'creevey_rgba_flipped_vert.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgb_flipped_horiz():
    filename = 'creevey_rgb_flipped_horiz.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgb_flipped_vert():
    filename = 'creevey_rgb_flipped_vert.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_grayscale_flipped_horiz():
    filename = 'creevey_gray_flipped_horiz.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image

@pytest.fixture
def sample_image_grayscale_flipped_vert():
    filename = 'creevey_gray_flipped_vert.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image
  
  
@pytest.fixture
def sample_image_tall_grayscale_rotated_90():
    filename = 'creevey_gray_rotated_90.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgb_rotated_90():
    filename = 'creevey_rgb_rotated_90.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgba_rotated_90():
    filename = 'creevey_rgba_rotated_90.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_tall_grayscale_rotated_180():
    filename = 'creevey_gray_rotated_180.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgb_rotated_180():
    filename = 'creevey_rgb_rotated_180.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgba_rotated_180():
    filename = 'creevey_rgba_rotated_180.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_tall_grayscale_rotated_270():
    filename = 'creevey_gray_rotated_270.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgb_rotated_270():
    filename = 'creevey_rgb_rotated_270.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image


@pytest.fixture
def sample_image_square_rgba_rotated_270():
    filename = 'creevey_rgba_rotated_270.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)
    return image
