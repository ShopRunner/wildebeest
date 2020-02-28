from pathlib import Path

import cv2 as cv
import numpy as np

from creevey.constants import PathOrStr


def write_image(image: np.array, path: PathOrStr, **kwargs) -> None:
    """
    Write image to specified path

    Create output directory if it does not exist, with try/except for
    thread safety.

    `kwargs` is included only for compatibility with the
    `CustomReportingPipeline` class.

    Parameters
    ----------
    image
        Image as a NumPy array
    path
        Desired output path
    """
    outdir = Path(path).parent
    outdir.mkdir(parents=True, exist_ok=True)
    num_channels = 1 if len(image.shape) == 2 else image.shape[2]
    if num_channels >= 3:
        # OpenCV wants to write BGR, so reverse order of first three
        # channels
        image[:, :, :3] = image[:, :, 2::-1]
    cv.imwrite(str(path), image)
