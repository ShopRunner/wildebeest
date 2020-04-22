from functools import partial
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


@pytest.fixture(scope='function')
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
    trim_resize_pipeline(inpaths=inpaths, path_func=path_func, n_jobs=6)
    for path in inpaths:
        outpath = path_func(path)
        image = plt.imread(str(outpath))
        assert image.shape[:2] == IMAGE_RESIZE_SHAPE


def test_logging(trim_resize_pipeline):
    inpaths = IMAGE_URLS
    outpaths = [
        TEMP_DATA_DIR / Path(filename).with_suffix('.png')
        for filename in IMAGE_FILENAMES
    ]
    expected_run_report = pd.DataFrame(
        {
            'outpath': outpaths,
            'skipped': [False] * len(inpaths),
            'error': [None] * len(inpaths),
        },
        index=inpaths,
    )
    trim_resize_pipeline(
        inpaths=inpaths, path_func=keep_filename_save_png_in_tempdir, n_jobs=6,
    )
    pd.testing.assert_frame_equal(
        trim_resize_pipeline.run_report_.sort_index().drop(
            'time_finished', axis='columns'
        ),
        expected_run_report.sort_index(),
    )


@pytest.fixture
def error_pipeline():
    error_pipeline = Pipeline(
        load_func=load_image_from_url, ops=[_raise_TypeError], write_func=write_image
    )
    return error_pipeline


def _raise_TypeError(*args, **kwargs):
    raise ValueError('Sample error for testing purposes')


def test_catches(error_pipeline):
    inpaths = IMAGE_URLS
    outpaths = [
        TEMP_DATA_DIR / Path(filename).with_suffix('.png')
        for filename in IMAGE_FILENAMES
    ]
    expected_run_report = pd.DataFrame(
        {'outpath': outpaths, 'skipped': [False] * len(inpaths),}, index=inpaths,
    )
    error_pipeline(
        inpaths=inpaths, path_func=keep_filename_save_png_in_tempdir, n_jobs=1,
    )
    pd.testing.assert_frame_equal(
        error_pipeline.run_report_.sort_index().drop(
            ['time_finished', 'error'], axis='columns'
        ),
        expected_run_report.sort_index(),
    )
    expected_error = ValueError('Sample error for testing purposes')
    for actual_error in error_pipeline.run_report_.loc[:, 'error']:
        assert type(actual_error) is type(expected_error)
        assert actual_error.args == expected_error.args


def test_raises_with_different_catch(error_pipeline):
    with pytest.raises(ValueError):
        error_pipeline(
            inpaths=IMAGE_URLS,
            path_func=keep_filename_save_png_in_tempdir,
            n_jobs=6,
            exceptions_to_catch=AttributeError,
        )


def test_raises_with_different_catch_tuple(error_pipeline):
    with pytest.raises(ValueError):
        error_pipeline(
            inpaths=IMAGE_URLS,
            path_func=keep_filename_save_png_in_tempdir,
            n_jobs=6,
            exceptions_to_catch=(AttributeError, TypeError),
        )


def test_raises_with_no_catch(error_pipeline):
    with pytest.raises(ValueError):
        error_pipeline(
            inpaths=IMAGE_URLS,
            path_func=keep_filename_save_png_in_tempdir,
            n_jobs=6,
            exceptions_to_catch=None,
        )
