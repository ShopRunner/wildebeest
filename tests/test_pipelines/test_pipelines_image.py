from functools import partial
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from creevey import Pipeline
from creevey.load_funcs.image import load_image_from_url
from creevey.ops.image import resize
from creevey.write_funcs.image import write_image
from tests.conftest import (
    delete_file_if_exists,
    IMAGE_FILENAMES,
    IMAGE_URLS,
    keep_filename_save_png_in_tempdir,
    TEMP_DATA_DIR,
)

IMAGE_RESIZE_SHAPE = (224, 224)


@pytest.fixture(scope='session')
def trim_resize_pipeline():
    for url in IMAGE_URLS:
        outpath = keep_filename_save_png_in_tempdir(url)
        delete_file_if_exists(outpath)

    trim_bottom_100 = lambda image: image[:-100, :]  # noqa: 29
    resize_224 = partial(resize, shape=IMAGE_RESIZE_SHAPE)

    trim_resize_pipeline = Pipeline(
        load_func=load_image_from_url,
        ops=[trim_bottom_100, resize_224],
        write_func=write_image,
    )
    yield trim_resize_pipeline
    for url in IMAGE_URLS:
        outpath = keep_filename_save_png_in_tempdir(url)
        delete_file_if_exists(outpath)


def test_trim_resize_pipeline(trim_resize_pipeline):
    path_func = keep_filename_save_png_in_tempdir
    inpaths = IMAGE_URLS
    trim_resize_pipeline(
        inpaths=inpaths, path_func=path_func, n_jobs=6, skip_existing=False
    )
    for path in inpaths:
        outpath = path_func(path)
        image = plt.imread(str(outpath))
        assert image.shape[:2] == IMAGE_RESIZE_SHAPE


def test_skip_existing(trim_resize_pipeline, caplog):
    inpaths = IMAGE_URLS

    trim_resize_pipeline(
        inpaths=inpaths,
        path_func=keep_filename_save_png_in_tempdir,
        n_jobs=6,
        skip_existing=False,
    )
    with caplog.at_level(logging.WARNING):
        outpaths = [
            TEMP_DATA_DIR / Path(filename).with_suffix('.png')
            for filename in IMAGE_FILENAMES
        ]
        skipped_existing = [1] * len(inpaths)
        exception_handled = [0] * len(inpaths)
        expected_run_report = pd.DataFrame(
            {
                'outpath': outpaths,
                'skipped_existing': skipped_existing,
                'exception_handled': exception_handled,
            },
            index=inpaths,
        )
        actual_run_report = trim_resize_pipeline(
            inpaths=IMAGE_URLS,
            path_func=keep_filename_save_png_in_tempdir,
            n_jobs=6,
            skip_existing=True,
        )
        pd.testing.assert_frame_equal(
            actual_run_report.sort_index().drop('time_finished', axis='columns'),
            expected_run_report.sort_index(),
        )
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == 'WARNING'


def test_logging(trim_resize_pipeline):
    inpaths = IMAGE_URLS
    outpaths = [
        TEMP_DATA_DIR / Path(filename).with_suffix('.png')
        for filename in IMAGE_FILENAMES
    ]
    exception_handled = skipped_existing = [0] * len(inpaths)
    expected_run_report = pd.DataFrame(
        {
            'outpath': outpaths,
            'skipped_existing': skipped_existing,
            'exception_handled': exception_handled,
        },
        index=inpaths,
    )
    actual_run_report = trim_resize_pipeline(
        inpaths=inpaths,
        path_func=keep_filename_save_png_in_tempdir,
        n_jobs=6,
        skip_existing=False,
    )
    pd.testing.assert_frame_equal(
        actual_run_report.sort_index().drop('time_finished', axis='columns'),
        expected_run_report.sort_index(),
    )


@pytest.fixture
def error_pipeline():
    error_pipeline = Pipeline(
        load_func=load_image_from_url, ops=[_raise_TypeError], write_func=write_image
    )
    return error_pipeline


def _raise_TypeError(*args, **kwargs):
    raise TypeError('Sample error for testing purposes')


def test_raises_without_catch(error_pipeline):
    with pytest.raises(TypeError):
        error_pipeline(
            inpaths=IMAGE_URLS,
            path_func=keep_filename_save_png_in_tempdir,
            n_jobs=6,
            skip_existing=False,
        )


def test_raises_with_different_catch(error_pipeline):
    with pytest.raises(TypeError):
        error_pipeline(
            inpaths=IMAGE_URLS,
            path_func=keep_filename_save_png_in_tempdir,
            n_jobs=6,
            skip_existing=False,
            exceptions_to_catch=(AttributeError,),
        )


def test_catches(error_pipeline):
    inpaths = IMAGE_URLS
    outpaths = [
        TEMP_DATA_DIR / Path(filename).with_suffix('.png')
        for filename in IMAGE_FILENAMES
    ]
    skipped_existing = [0] * len(inpaths)
    exception_handled = [1] * len(inpaths)
    expected_run_report = pd.DataFrame(
        {
            'outpath': outpaths,
            'skipped_existing': skipped_existing,
            'exception_handled': exception_handled,
        },
        index=inpaths,
    )
    actual_run_report = error_pipeline(
        inpaths=inpaths,
        path_func=keep_filename_save_png_in_tempdir,
        n_jobs=1,
        skip_existing=False,
        exceptions_to_catch=(TypeError,),
    )
    pd.testing.assert_frame_equal(
        actual_run_report.sort_index().drop('time_finished', axis='columns'),
        expected_run_report.sort_index(),
    )
