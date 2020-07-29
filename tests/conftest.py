from functools import partial
from pathlib import Path
import sys

from wildebeest.path_funcs import join_outdir_filename_extension

TEST_DIR = Path(__file__).parent
SAMPLE_DATA_DIR = Path(TEST_DIR) / 'sample_data'
TEMP_DATA_DIR = SAMPLE_DATA_DIR / 'tmp'
IMAGE_FILENAMES = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
IMAGE_URLS = [f'https://bit.ly/{filename}' for filename in IMAGE_FILENAMES]

from tests.fixtures import *

sys.path.append(TEST_DIR / 'fixtures')

keep_filename_save_png_in_tempdir = partial(
    join_outdir_filename_extension, outdir=TEMP_DATA_DIR, extension='.png'
)


def delete_file_if_exists(path: Path):
    if path.is_file():
        path.unlink()
