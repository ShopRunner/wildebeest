"""Functions that take an image and write it out"""
import os
from pathlib import Path
import uuid

import cv2 as cv
import numpy as np

from wildebeest.constants import PathOrStr


def write_image(image: np.array, path: PathOrStr, **kwargs) -> None:
    """
    Write image to specified path.

    Create output directory if it does not exist.

    Write to a temporary in a directory ".tmp" inside the output
    directory and then rename the file so that we don't create a partial
    image file if write process is interrupted. ".tmp" directory is not
    deleted, but temporary files are deleted even if there is an
    exception during writing or renaming.

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Parameters
    ----------
    image
        Image as a NumPy array
    path
        Desired output path
    """
    num_channels = 1 if len(image.shape) == 2 else image.shape[2]
    if num_channels >= 3:
        # OpenCV wants to write BGR, so reverse order of first three
        # channels
        image[:, :, :3] = image[:, :, 2::-1]

    path = Path(path)
    outdir = path.parent

    tmp_dir = outdir / '.tmp'
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / (str(uuid.uuid4()) + path.suffix)
    try:
        cv.imwrite(str(tmp_path), image)
        assert (
            tmp_path.exists()
        ), f"Attempt to write image temporarily to {tmp_path} failed."
        os.rename(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
