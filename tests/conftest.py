from pathlib import Path
from shutil import rmtree

import pytest


TEST_DIR = Path(__file__).parent
SAMPLE_DATA_DIR = Path(TEST_DIR) / 'sample_data'
TEMP_DATA_DIR = SAMPLE_DATA_DIR / 'tmp'


@pytest.fixture
def generate_file_tree(scope='session'):
    if TEMP_DATA_DIR.exists():
        rmtree(TEMP_DATA_DIR)
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
    rmtree(TEMP_DATA_DIR)
