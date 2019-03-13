import os
from pathlib import Path
from typing import Iterable, List

from creevey.constants import PathOrStr


def find_files_with_extensions(
    search_dir: PathOrStr, extensions: Iterable[str]
) -> List[Path]:
    """
    Find files with one of the specified extensions.

    Extension matching is case-insensitive.

    Parameters
    ----------
    search_dir
        Directory to search
    img_extensions
        Extensions to search for. The initial "." can be included or
        not.

    Returns
    -------
    List of `Path` objects specifying locations of all files recursively
    within `search_dir` that have one of the extensions in `extensions`.
    """
    extensions = [item if item.startswith('.') else '.' + item for item in extensions]
    file_list = [
        Path(dirpath) / fn
        for dirpath, dirname, filenames in os.walk(str(search_dir))
        for fn in filenames
        if Path(fn).suffix.lower() in extensions
    ]
    return file_list
