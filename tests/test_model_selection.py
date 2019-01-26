import pandas as pd

import pytest

from creevey import group_train_test_split


@pytest.fixture
def grouped_dataset():
    df = pd.DataFrame(
        {'x': [1, 2, 3, 4], 'y': ['a', 'b', 'c', 'd'], 'group': [0, 0, 0, 1]}
    )
    return df


def test_group_train_test_split(grouped_dataset):
    X = grouped_dataset.loc[:, ['x']]
    y = grouped_dataset.loc[:, 'y']
    groups = grouped_dataset.loc[:, 'group']
    X_train, X_test, y_train, y_test = group_train_test_split(
        X=X, y=y, groups=groups, test_size=1
    )
    assert (X_train.index == y_train.index).all()
    assert (X_test.index == y_test.index).all()
    assert len(X_test) + len(X_train) == 4
    assert len(y_test) == 1 or len(y_test) == 3
    if len(y_test) == 1:
        assert y_test.index[0] == 3
    else:
        assert y_train.index[0] == 3
