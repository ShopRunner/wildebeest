import pytest

from tests.conftest import SAMPLE_DATA_DIR
from wildebeest.load_funcs.image import load_image_from_disk


@pytest.fixture
def sample_image_square_rgb():
    filename = 'wildebeest_rgb.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_tall_grayscale():
    filename = 'wildebeest_gray.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgba():
    filename = 'wildebeest_rgba.png'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgba_flipped_horiz():
    filename = 'wildebeest_rgba_flipped_horiz.png'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgba_flipped_vert():
    filename = 'wildebeest_rgba_flipped_vert.png'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgb_flipped_horiz():
    filename = 'wildebeest_rgb_flipped_horiz.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgb_flipped_vert():
    filename = 'wildebeest_rgb_flipped_vert.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_grayscale_flipped_horiz():
    filename = 'wildebeest_gray_flipped_horiz.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_grayscale_flipped_vert():
    filename = 'wildebeest_gray_flipped_vert.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_tall_grayscale_rotated_90():
    filename = 'wildebeest_gray_rotated_90.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgb_rotated_90():
    filename = 'wildebeest_rgb_rotated_90.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgba_rotated_90():
    filename = 'wildebeest_rgba_rotated_90.png'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_tall_grayscale_rotated_180():
    filename = 'wildebeest_gray_rotated_180.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgb_rotated_180():
    filename = 'wildebeest_rgb_rotated_180.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgba_rotated_180():
    filename = 'wildebeest_rgba_rotated_180.png'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_tall_grayscale_rotated_270():
    filename = 'wildebeest_gray_rotated_270.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgb_rotated_270():
    filename = 'wildebeest_rgb_rotated_270.jpg'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)


@pytest.fixture
def sample_image_square_rgba_rotated_270():
    filename = 'wildebeest_rgba_rotated_270.png'
    path = SAMPLE_DATA_DIR / filename
    return load_image_from_disk(path)
