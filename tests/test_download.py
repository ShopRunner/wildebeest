import filecmp
from functools import partial
import logging
import os

import pytest

from creevey.download import download_images_as_png
from .conftest import (
    MADEYE_IMAGE_URL,
    PHILOSOPHERS_STONE_IMAGE_URL,
    SAMPLE_DATA_DIR,
    STABLE_LOCAL_MADEYE_IMAGE_PATH,
    STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH,
    TEMP_LOCAL_MADEYE_IMAGE_PATH_CUSTOM,
    TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT,
    TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_CUSTOM,
    TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT,
)


def _delete_file_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)


@pytest.fixture
def download_two_images_as_png_specified_outdir(scope='session'):
    for path in [TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT, TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT]:
        _delete_file_if_exists(path)
    download_images_as_png(urls=[MADEYE_IMAGE_URL, PHILOSOPHERS_STONE_IMAGE_URL],
                           outdir=SAMPLE_DATA_DIR,
                           n_jobs=20,
                           )
    yield
    for path in [TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT, TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT]:
        _delete_file_if_exists(path)


def test_download_multiple_files_as_png(download_two_images_as_png_specified_outdir):
    assert filecmp.cmp(STABLE_LOCAL_MADEYE_IMAGE_PATH, TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT)
    assert filecmp.cmp(STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH,
                       TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT
                       )


def test_download_two_images_as_png_specified_path_func(scope='session'):
    expected_paths = [TEMP_LOCAL_MADEYE_IMAGE_PATH_CUSTOM, TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_CUSTOM]
    for path in expected_paths:
        _delete_file_if_exists(path)
    path_func = partial(_combine_outdir_with_dirname_and_extension, outdir=SAMPLE_DATA_DIR, extension='.png')
    download_images_as_png(urls=[MADEYE_IMAGE_URL, PHILOSOPHERS_STONE_IMAGE_URL],
                           path_func=path_func,
                           )
    for path in expected_paths:
        assert os.path.exists(path)
    for path in expected_paths:
        _delete_file_if_exists(path)


def _combine_outdir_with_dirname_and_extension(url, outdir, extension):
    filename = os.path.basename(os.path.dirname(url))
    extension = extension if extension.startswith('.') else '.' + extension
    filename_with_ext = os.path.splitext(filename)[0] + extension
    outpath = os.path.join(outdir, filename_with_ext)
    return outpath


def test_download_multiple_files_as_png_raise_with_both_outdir_and_path_func():
    with pytest.raises(ValueError):
        download_images_as_png(urls=[MADEYE_IMAGE_URL, PHILOSOPHERS_STONE_IMAGE_URL],
                               outdir='.',
                               path_func=os.path.basename
                               )


def test_broken_link_logged_as_error(caplog):
    with caplog.at_level(logging.ERROR):
        download_images_as_png(
            urls=[url + 'xyz' for url in [MADEYE_IMAGE_URL, PHILOSOPHERS_STONE_IMAGE_URL]],
            outdir=SAMPLE_DATA_DIR,
            n_jobs=20,
        )
        assert len(caplog.records) == 2
