from creevey.load_funcs.image import load_image_from_disk
from tests.conftest import SAMPLE_DATA_DIR


def test_load_image_grayscale():
    filename = 'creevey_gray.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)

    expected_shape = (34, 25)
    actual_shape = image.shape

    assert actual_shape == expected_shape


def test_load_image_rgb():
    filename = 'creevey_rgb.jpg'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)

    expected_shape = (32, 32, 3)
    actual_shape = image.shape

    assert actual_shape == expected_shape


def test_load_image_rgba():
    filename = 'creevey_rgba.png'
    path = SAMPLE_DATA_DIR / filename
    image = load_image_from_disk(path)

    expected_shape = (32, 32, 4)
    actual_shape = image.shape

    assert actual_shape == expected_shape
