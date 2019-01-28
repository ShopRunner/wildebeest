from typing import Optional, Tuple, Union

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


def group_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
    test_size: Optional[Union[float, int]],
    random_state: Optional[int] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Do a train/test split that keeps items with the same value in a
    specified column together.

    Parameters
    ----------
    X
        DataFrame of features
    y
        Series of labels
    groups
        Group labels to split on, with shape (n_samples,)
    test_size
        Desired number (int) or proportion (float between 0.0 and 1.0)
        of *groups* to place in `valid`. Unlike `sklearn`'s
        `train_test_split`, this function does not provide a default
        `test_size`. This lack of a default value is a deliberate design
        choice: Creevey is designed for deep learning workflows that
        often involve datasets with millions of items, but it should
        also be able to handle smaller datasets (including tiny datasets
        created for debugging purposes), and there does not seem to be a
        simple default that is sensible across that range of use cases.
    random_state
        `train`/`valid` split is randomized. Specifying a consistent
        value for this parameter will yield consistent results.

    Returns
    -------
    X_train, X_test, y_train, y_test
    """
    splitter = GroupShuffleSplit(
        n_splits=1, test_size=test_size, random_state=random_state
    )
    train_indices, test_indices = list(splitter.split(X, y, groups))[0]

    X_train = X.iloc[train_indices, :]
    X_test = X.iloc[test_indices, :]
    y_train = y.iloc[train_indices]
    y_test = y.iloc[test_indices]

    return X_train, X_test, y_train, y_test
