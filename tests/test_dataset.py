import os
import shutil

from creevey import S3TarfileDataset
from .conftest import SAMPLE_DATA_DIR


def test_S3TarfileDataset():
    dataset = S3TarfileDataset(
        s3_bucket='autofocus',
        s3_key='creevey_dummy_dataset.tar',
        base_dir=SAMPLE_DATA_DIR,
    )
    dataset.get_raw()
    assert os.path.isdir(dataset.raw_dir)
    assert os.path.isdir(os.path.join(dataset.raw_dir, 'creevey_dummy_dataset'))
    assert os.path.isfile(
        os.path.join(dataset.raw_dir, 'creevey_dummy_dataset', 'creevey.csv')
    )
    assert os.path.isfile(
        os.path.join(dataset.raw_dir, 'creevey_dummy_dataset', 'creevey.jpeg')
    )
    shutil.rmtree(dataset.raw_dir)
