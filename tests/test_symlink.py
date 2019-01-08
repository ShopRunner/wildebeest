from collections import defaultdict
import os
import shutil

import pandas as pd
import pytest

from creevey import create_imagenet_style_symlinks
from .conftest import SAMPLE_DATA_DIR, STABLE_LOCAL_MADEYE_IMAGE_PATH


TEMP_INDIR = os.path.join(SAMPLE_DATA_DIR, 'tmp_flat')
TEMP_OUTDIR = os.path.join(SAMPLE_DATA_DIR, 'tmp_imagenet')
TEMP_TRAIN_DIR = os.path.join(TEMP_OUTDIR, 'train')
TEMP_VALID_DIR = os.path.join(TEMP_OUTDIR, 'valid')

NUM_TEST_IMAGES = 20


@pytest.fixture
def dataset():
    dataset = defaultdict(list)
    if not os.path.isdir(TEMP_INDIR):
        os.makedirs(TEMP_INDIR)
    for copynum in range(NUM_TEST_IMAGES):
        outpath = os.path.join(TEMP_INDIR, f'madeye_copy{copynum}.png')
        shutil.copyfile(STABLE_LOCAL_MADEYE_IMAGE_PATH, outpath)
        dataset['path'].append(outpath)
        dataset['label'].append('fake1' if copynum < 5 else 'fake2')
        dataset['group'].append('a' if copynum % 3 == 0 else 'b' if copynum % 3 == 1 else 'c')
    dataset = pd.DataFrame(dataset)
    create_imagenet_style_symlinks(df=dataset,
                                   label_colname='label',
                                   path_colname='path',
                                   valid_size=.2,
                                   outdir=TEMP_OUTDIR,
                                   groupby_colname='group',
                                   )
    yield dataset
    shutil.rmtree(TEMP_INDIR)
    shutil.rmtree(TEMP_OUTDIR)


def test_create_imagenet_style_symlinks(dataset):
    train_filenames = sum([os.listdir(os.path.join(TEMP_TRAIN_DIR, directory))
                           for directory in os.listdir(TEMP_TRAIN_DIR)
                           ], [])
    dataset.loc[:, 'dataset_name'] = dataset.loc[:, 'path'].apply(
        lambda path: 'train' if os.path.basename(path) in train_filenames else 'valid'
    )
    train_df = dataset.loc[dataset.loc[:, 'dataset_name'] == 'train', :]
    valid_df = dataset.loc[dataset.loc[:, 'dataset_name'] == 'valid', :]
    train_groups = set(train_df.loc[:, 'group'].unique())
    valid_groups = set(valid_df.loc[:, 'group'].unique())
    groups_overlap = any([group in valid_groups for group in train_groups])

    assert not groups_overlap

    assert len(valid_df) in (NUM_TEST_IMAGES//3, NUM_TEST_IMAGES//3 + 1)
    assert len(train_df) == NUM_TEST_IMAGES - len(valid_df)
