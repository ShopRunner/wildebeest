from functools import partial
from pathlib import Path
from shutil import rmtree

import pytest

from creevey.path_funcs import join_outdir_filename_extension


TEST_DIR = Path(__file__).parent
SAMPLE_DATA_DIR = Path(TEST_DIR) / 'sample_data'
TEMP_DATA_DIR = SAMPLE_DATA_DIR / 'tmp'
IMAGE_FILENAMES = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
IMAGE_URLS = [f'https://bit.ly/{filename}' for filename in IMAGE_FILENAMES]

keep_filename_save_png_in_tempdir = partial(
    join_outdir_filename_extension, outdir=TEMP_DATA_DIR, extension='.png'
)


@pytest.fixture
def generate_file_tree(scope='session'):
    if TEMP_DATA_DIR.exists():
        rmtree(str(TEMP_DATA_DIR))
    level0_dirs = ['tmp00', 'tmp01']
    level0_files = ['fake00.txt', 'fake01.png', 'fake02.JPG']
    for temp_dir in level0_dirs:
        dirpath = TEMP_DATA_DIR / temp_dir
        dirpath.mkdir(parents=True)
    for filename in level0_files:
        filepath = TEMP_DATA_DIR / filename
        filepath.touch()
    level2_dirpath = TEMP_DATA_DIR / level0_dirs[0] / 'temp10' / 'temp20'
    level2_dirpath.mkdir(parents=True)
    level3_files = ['fake30.pdf', 'fake31.BMP', 'fake32.txt']
    for filename in level3_files:
        filepath = level2_dirpath / filename
        filepath.touch()
    yield
    rmtree(str(TEMP_DATA_DIR))


def delete_file_if_exists(path: Path):
    if path.is_file():
        path.unlink()
