from pathlib import Path
from typing import Optional
import uuid

from creevey.constants import PathOrStr


def join_outdir_filename_extension(
    path: PathOrStr, outdir: PathOrStr, extension: Optional[str] = None
) -> Path:
    """
    Construct path by combining specified `outdir`, filename from
    `path`, and (optionally) specified extension

    Parameters
    ----------
    path
        Path with desired filename
    outdir
        Desired output directory
    extension
        Desired output file extension. If `None`, keep extension from
        `path`.
    """
    filename = Path(Path(path).name)
    if extension is not None:
        extension = extension if extension.startswith('.') else '.' + extension
        filename = filename.stem + extension
    outpath = Path(outdir) / filename
    return outpath


def join_outdir_hashed_path_extension(
    path: PathOrStr, outdir: PathOrStr, extension: Optional[str] = None
) -> Path:
    """
    Construct path by combining specified `outdir`, filename derived by
    hashing `path`, and (optionally) specified extension.

    Parameters
    ----------
    path
        Input path to be hashed to generate output filename
    outdir
        Desired output directory
    extension
        Desired output extension. If `None`, keep extension from `path`.
    """
    filename = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(path)))
    filename = filename.replace('-', '')
    if extension is None:
        extension = path.suffix
    outpath = join_outdir_filename_extension(filename, outdir, extension)
    return outpath


def replace_dir(path: PathOrStr, outdir: PathOrStr) -> Path:
    return Path(outdir) / Path(path).name
