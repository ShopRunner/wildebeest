import logging
import os
from typing import List, Tuple

import cv2 as cv
from joblib import delayed, Parallel
import numpy as np
from tqdm import tqdm


def resize_multiple_files(paths: List[str],
                          shape: Tuple[int, int],
                          outdir: str,
                          n_jobs: int
                          ) -> None:
    """
    Resize image files and write them to specified output directory

    Parameters
    ----------
    inpaths
        Paths to image files
    shape
        Desired output shape in the form (height, width)
    outdir
        Desired output path
    n_jobs
        Number of jobs to run in parallel
    """
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    Parallel(n_jobs=n_jobs)(
        delayed(_resize_file_catch_cv_errors)(
            inpath=path,
            shape=shape,
            outpath=os.path.join(outdir, os.path.basename(path))
        ) for path in tqdm(paths)
    )


def _resize_file_catch_cv_errors(inpath: str, shape: Tuple[int, int], outpath: str) -> None:
    try:
        resize_file(inpath, shape, outpath)
    except cv.error as e:
        logging.error(f'Error on {inpath}', e)


def resize_file(inpath: str, shape: Tuple[int, int], outpath: str) -> None:
    """
    Resize a single image file and write it to the specified output path

    Parameters
    ----------
    inpath
        Path to image file
    shape
        Desired output shape in the form (height, width)
    outpath
        Desired output path
    """
    image_in = cv.imread(inpath)
    image_out = resize_image(image_in, shape)
    cv.imwrite(outpath, image_out)


def resize_image(image: np.array, shape: Tuple[int, int]) -> np.array:
    """
    Resize input image to the specified shape.

    Parameters
    ----------
    image:
        NumPy array with two spatial dimensions and optionally an
        additional channel dimension
    shape:
        Desired output shape in the form (height, width)

    Returns
    -------
    NumPy array with specified shape
    """
    resized = cv.resize(image, dsize=shape[::-1])
    return resized
