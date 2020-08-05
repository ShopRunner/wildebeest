from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import requests

from tests.conftest import (
    delete_file_if_exists,
    IMAGE_FILENAMES,
    IMAGE_URLS,
    keep_filename_save_png_in_tempdir,
    TEMP_DATA_DIR,
)
from wildebeest import CustomReportingPipeline, Pipeline
from wildebeest.load_funcs.image import load_image_from_url
from wildebeest.ops import get_report_output_decorator
from wildebeest.ops.image import calculate_mean_brightness
from wildebeest.write_funcs.image import write_image


@get_report_output_decorator(key='mean_brightness')
def report_mean_brightness(image):
    return calculate_mean_brightness(image)


@pytest.fixture(scope='function')
def report_mean_brightness_pipeline():
    for url in IMAGE_URLS:
        outpath = keep_filename_save_png_in_tempdir(url)
        delete_file_if_exists(outpath)

    report_mean_brightness_pipeline = CustomReportingPipeline(
        load_func=load_image_from_url,
        ops=report_mean_brightness,
        write_func=write_image,
    )
    yield report_mean_brightness_pipeline
    for url in IMAGE_URLS:
        outpath = keep_filename_save_png_in_tempdir(url)
        delete_file_if_exists(outpath)


def test_custom_reporting_pipeline(report_mean_brightness_pipeline):
    outpaths = [
        TEMP_DATA_DIR / Path(filename).with_suffix('.png')
        for filename in IMAGE_FILENAMES
    ]
    expected_run_report = pd.DataFrame(
        {
            'outpath': outpaths,
            'skipped': [False] * len(IMAGE_URLS),
            'error': [np.nan] * len(IMAGE_URLS),
        },
        index=IMAGE_URLS,
    )
    report_mean_brightness_pipeline(
        inpaths=IMAGE_URLS, path_func=keep_filename_save_png_in_tempdir, n_jobs=6,
    )
    pd.testing.assert_frame_equal(
        report_mean_brightness_pipeline.run_report_.sort_index(axis='index')
        .sort_index(axis='columns')
        .drop(['time_finished', 'mean_brightness'], axis='columns'),
        expected_run_report.sort_index(axis='index').sort_index(axis='columns'),
    )
    assert np.issubdtype(
        report_mean_brightness_pipeline.run_report_.loc[:, 'mean_brightness'], np.number
    )


@pytest.fixture(scope='function')
def custom_check_existing_pipeline():
    for url in IMAGE_URLS:
        outpath = keep_filename_save_png_in_tempdir(url)
        delete_file_if_exists(outpath)

    yield Pipeline(
        load_func=load_image_from_url, write_func=write_image,
    )
    for url in IMAGE_URLS:
        outpath = keep_filename_save_png_in_tempdir(url)
        delete_file_if_exists(outpath)


def test_custom_check_existing_func(custom_check_existing_pipeline):
    custom_check_existing_pipeline(
        inpaths=IMAGE_URLS,
        path_func=lambda x: x,
        n_jobs=6,
        skip_func=lambda url, outpath: requests.head(outpath).status_code < 400,
    )
    assert custom_check_existing_pipeline.run_report_.loc[:, 'skipped'].all()
