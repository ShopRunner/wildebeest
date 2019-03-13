from pathlib import Path

from creevey.constants import PathOrStr


def join_outdir_filename_extension(
    path: PathOrStr, outdir: PathOrStr, extension: str
) -> Path:
    """
    Join `outdir`, `path` filename, and `extension`

    Parameters
    ----------
    path
        Path with desired filename
    outdir
        Desired output directory
    extension
        Desired output file extension

    Returns
    -------
    Path object that results from joining input `outdir` with filename
    from input `path` with input `extension`.
    """
    filename = Path(Path(path).name)
    extension = extension if extension.startswith('.') else '.' + extension
    filename_with_ext = filename.stem + extension
    outpath = Path(outdir) / filename_with_ext
    return outpath


def replace_dir(path: PathOrStr, outdir: PathOrStr) -> Path:
    return Path(outdir) / Path(path).name
