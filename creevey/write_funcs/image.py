from pathlib import Path

import cv2 as cv
import numpy as np

from creevey.constants import PathOrStr


def write_image(image: np.array, path: PathOrStr):
    outdir = Path(path).parent
    if not outdir.exists():
        # need try/except in case directory does not exist but at this
        # point process switches to another thread that creates it
        # before coming back to this one
        try:
            outdir.mkdir()
        except OSError:
            pass
    cv.imwrite(str(path), image)
