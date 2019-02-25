from pathlib import Path

import cv2 as cv
import numpy as np

from creevey.constants import PathOrStr


def write_image(image: np.array, path: PathOrStr) -> None:
    """
    Write image to specified path

    Create output directory if it does not exist, with try/except for
    thread safety.

    Parameters
    ----------
    image
        Image as a NumPy array
    path
        Desired output path
    """
    outdir = Path(path).parent
    if not outdir.exists():
        # need try/except in case directory does not exist but at this
        # point process switches to another thread that creates it
        # before coming back to this one
        try:
            outdir.mkdir(parents=True)
        except OSError:
            pass
    cv.imwrite(str(path), image)
