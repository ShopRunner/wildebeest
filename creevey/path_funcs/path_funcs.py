from pathlib import Path


def combine_outdir_dirname_extension(url, outdir, extension):
    filename = Path(Path(url).name)
    extension = extension if extension.startswith('.') else '.' + extension
    filename_with_ext = filename.stem + extension
    outpath = Path(outdir) / filename_with_ext
    return outpath
