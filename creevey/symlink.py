import os
from typing import Optional, Tuple, Union

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split


def create_imagenet_style_symlinks(df: pd.DataFrame,
                                   valid_size: Union[int, float],
                                   outdir: str,
                                   label_colname: str,
                                   path_colname: str,
                                   groupby_colname: Optional[str] = None,
                                   random_state: Optional[int] = None,
                                   ) -> None:
    """
    Create image symlinks organized into `train` and `valid`
    directories each containing one subdirectory per label value,
    optionally grouping by one or more variables.

    When `groupby_colname` is specified, `valid_size` is understood as
    a count or proportion of *groups* rather than individual samples.

    Groups or samples (if `groupby_colname` is not specified) are
    randomly placed in `valid` until `valid_size` is exceeded, so the
    number or proportion of groups or samples in `valid` will be
    greater than or equal to `valid_size`.

    Parameters
    ----------
    df
        DataFrame containing image paths and labels
    label_colname
        Name of the column in `df` that contains image labels
    path_colname
        Name of the column in `df` that contains paths to images
    valid_size
        Desired number (int) or proportion (float between 0.0 and 1.0)
        of *groups* (or samples if `groupby_colname` is `None`) to place
        in `valid`
    outdir
        Desired output directory
    groupby_colname
        Name of column to group by, so that items with the same value in
        this column stay on the same side of the `train`/`valid` split
    random_state
        `train`/`valid` split is randomized. Specifying a consistent
        value for this parameter will yield consistent results.

    Raises
    ------
    ValueError if outdir is not empty
    """
    if os.path.exists(outdir) and os.listdir(outdir):
        raise ValueError('outdir must be empty')

    X = df.loc[:, [label_colname, groupby_colname]]
    y = df.loc[:, path_colname]

    if groupby_colname is None:
        X_train, X_valid, y_train, y_valid = (
            train_test_split(X=X, y=y, test_size=valid_size, random_state=random_state)
        )
    else:
        groups = df.loc[:, groupby_colname]
        X_train, X_valid, y_train, y_valid = (
            _group_train_test_split(X=X, y=y, groups=groups, test_size=valid_size, random_state=random_state)
        )

    df_train = pd.concat([X_train, y_train], axis='columns')
    df_valid = pd.concat([X_valid, y_valid], axis='columns')
    datasets = {'train': df_train, 'valid': df_valid}

    train_groups = set(df_train.loc[:, groupby_colname].unique())
    valid_groups = set(df_valid.loc[:, groupby_colname].unique())
    groups_overlap = any([group in valid_groups for group in train_groups])
    if groups_overlap:
        raise AssertionError('Groups overlap across training and validation sets')

    df_train = df_train.drop(groupby_colname, axis='columns')
    df_valid = df_valid.drop(groupby_colname, axis='columns')

    for dataset_name, dataset_df in datasets.items():
        dataset_dir = os.path.join(outdir, dataset_name)
        dataset_df.apply(
            lambda row: _make_symlink(row, label_colname, path_colname, dataset_dir),
            axis='columns'
        )

    # fastai v0.7 at least assumes that the nth directory in "valid"
    # alphabetically corresponds to the nth directory alphabetically in
    # "train", so it will misinterpret labels if the train and valid
    # subdirectories don't match.
    train_dir = os.path.join(outdir, 'train')
    valid_dir = os.path.join(outdir, 'valid')
    reconcile_subdirectories(train_dir, valid_dir)
    reconcile_subdirectories(valid_dir, train_dir)


def reconcile_subdirectories(dir1, dir2):
    for subdir in os.listdir(os.path.join(dir2)):
        corresponding_dir = os.path.join(dir1, subdir)
        if not os.path.isdir(corresponding_dir):
            os.makedirs(corresponding_dir)


def _make_symlink(row: pd.Series,
                  label_colname: str,
                  path_colname: str,
                  base_dir: str
                  ):
    label = row.loc[label_colname]
    row_dir = os.path.join(base_dir, label)
    if not os.path.exists(row_dir):
        os.makedirs(row_dir)
    image_path = row.loc[path_colname]
    image_filename = os.path.basename(image_path)
    symlink_path = os.path.join(row_dir, image_filename)
    if not os.path.islink(symlink_path):
        os.symlink(image_path, symlink_path)


def _group_train_test_split(X: pd.DataFrame,
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
        of *groups* to place in `valid`
    random_state
        `train`/`valid` split is randomized. Specifying a consistent
        value for this parameter will yield consistent results.

    Returns
    -------
    X_train, X_test, y_train, y_test
    """
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_indices, test_indices = list(splitter.split(X, y, groups))[0]

    X_train = X.iloc[train_indices, :]
    X_test = X.iloc[test_indices, :]
    y_train = y.iloc[train_indices]
    y_test = y.iloc[test_indices]

    return X_train, X_test, y_train, y_test
