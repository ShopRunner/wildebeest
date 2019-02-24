from functools import partial

import logging
import matplotlib.pyplot as plt
import pytest

from creevey import Pipeline
from creevey.load_funcs.image import download_image
from creevey.ops.image import resize
from creevey.write_funcs.image import write_image
from creevey.path_funcs import combine_outdir_basename_extension
from tests.conftest import SAMPLE_DATA_DIR

IMAGE_FILENAMES = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
IMAGE_URLS = [f'https://bit.ly/{filename}' for filename in IMAGE_FILENAMES]
IMAGE_SHAPE = (224, 224)

keep_filename_png_in_cwd = partial(
    combine_outdir_basename_extension, outdir=SAMPLE_DATA_DIR, extension='.png'
)


@pytest.fixture
def trim_resize_pipeline():
    for url in IMAGE_URLS:
        outpath = keep_filename_png_in_cwd(url)
        _delete_file_if_exists(outpath)

    trim_bottom_100 = lambda image: image[:-100, :]
    resize_224 = partial(resize, shape=IMAGE_SHAPE)

    trim_resize_pipeline = Pipeline(
        load_func=download_image,
        ops=[trim_bottom_100, resize_224],
        write_func=write_image,
    )
    yield trim_resize_pipeline
    for url in IMAGE_URLS:
        outpath = keep_filename_png_in_cwd(url)
        _delete_file_if_exists(outpath)


def _delete_file_if_exists(path):
    if path.is_file():
        path.unlink()


def test_trim_resize_pipeline(trim_resize_pipeline):
    trim_resize_pipeline.run(
        inpaths=IMAGE_URLS,
        path_func=keep_filename_png_in_cwd,
        n_jobs=10,
        skip_existing=False,
    )
    for path in SAMPLE_DATA_DIR.iterdir():
        if path.suffix == '.png':
            image = plt.imread(str(path))
            assert image.shape[:2] == IMAGE_SHAPE


def test_skip_existing(trim_resize_pipeline, caplog):
    trim_resize_pipeline.run(
        inpaths=IMAGE_URLS,
        path_func=keep_filename_png_in_cwd,
        n_jobs=10,
        skip_existing=False,
    )
    with caplog.at_level(logging.WARNING):
        trim_resize_pipeline.run(
            inpaths=IMAGE_URLS,
            path_func=keep_filename_png_in_cwd,
            n_jobs=10,
            skip_existing=True,
        )
        assert len(caplog.records) == len(IMAGE_URLS)
        assert caplog.records[0].levelname == 'WARNING'
