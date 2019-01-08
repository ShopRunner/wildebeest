import os

import cv2 as cv
import pytest

from creevey import resize_image, resize_multiple_files
from .conftest import (SAMPLE_DATA_DIR,
                       STABLE_LOCAL_MADEYE_IMAGE_FILENAME,
                       STABLE_LOCAL_MADEYE_IMAGE_PATH,
                       STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME,
                       STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH
                       )


@pytest.fixture
def sample_image():
    # Image is 396 x 255 x 3
    return cv.imread(STABLE_LOCAL_MADEYE_IMAGE_PATH)


def test_upsize(sample_image):
    expected_spatial_shape = (400, 500)
    upsized_image = resize_image(sample_image, shape=expected_spatial_shape)
    expected_shape = expected_spatial_shape + (3,)
    assert upsized_image.shape == expected_shape


def test_downsize(sample_image):
    expected_spatial_shape = (300, 100)
    upsized_image = resize_image(sample_image, shape=expected_spatial_shape)
    expected_shape = expected_spatial_shape + (3,)
    assert upsized_image.shape == expected_shape


@pytest.fixture
def sample_image_gray():
    image = cv.imread(STABLE_LOCAL_MADEYE_IMAGE_PATH)
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return image_gray


def test_grayscale(sample_image_gray):
    expected_shape = (400, 500)
    resized_image = resize_image(sample_image_gray, shape=expected_shape)
    assert resized_image.shape == expected_shape


@pytest.fixture
def resized_files():
    outdir = os.path.join(SAMPLE_DATA_DIR, 'tmp')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    paths = STABLE_LOCAL_MADEYE_IMAGE_PATH, STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH
    resize_multiple_files(paths=paths,
                          shape=(224, 224),
                          outdir=outdir,
                          n_jobs=20,
                          )
    outpaths = [os.path.join(outdir, STABLE_LOCAL_MADEYE_IMAGE_FILENAME),
                os.path.join(outdir, STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME)
                ]

    yield outpaths

    for path in outpaths:
        print(path)
        os.remove(path)
    os.rmdir(outdir)


def test_resize_multiple_files(resized_files):
    for path in resized_files:
        image = cv.imread(path)
        assert image.shape == (224, 224, 3)
