from functools import partial
import filecmp

import pytest

from creevey.pipelines.image import download_image_pipeline
from creevey.path_funcs.path_funcs import combine_outdir_dirname_extension

from tests.conftest import (
    MADEYE_IMAGE_URL,
    PHILOSOPHERS_STONE_IMAGE_URL,
    SAMPLE_DATA_DIR,
    STABLE_LOCAL_MADEYE_IMAGE_PATH,
    STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH,
    TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT,
    TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT,
)


URLS = [MADEYE_IMAGE_URL, PHILOSOPHERS_STONE_IMAGE_URL]


@pytest.fixture
def download_two_images_as_png(scope='session'):
    for path in [
        TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT,
        TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT,
    ]:
        _delete_file_if_exists(path)
    outpath_func = partial(
        combine_outdir_dirname_extension, outdir=SAMPLE_DATA_DIR, extension='.png'
    )
    download_image_pipeline.run(inpaths=URLS, path_func=outpath_func, n_jobs=10)
    yield
    for path in [
        TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT,
        TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT,
    ]:
        _delete_file_if_exists(path)


def _delete_file_if_exists(path):
    if path.is_file():
        path.unlink()


def test_download_png_pipeline(download_two_images_as_png):
    assert filecmp.cmp(
        STABLE_LOCAL_MADEYE_IMAGE_PATH, TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT
    )
    assert filecmp.cmp(
        STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH,
        TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT,
    )
