from pathlib import Path

from creevey.path_funcs import join_outdir_filename_extension, replace_dir


def test_join_outdir_filename_extension_str_input():
    inpath = './foo.png'
    actual_outpath = join_outdir_filename_extension(
        inpath, outdir='bar', extension='jpg'
    )
    expected_outpath = Path('bar/foo.jpg')
    assert actual_outpath == expected_outpath


def test_join_outdir_filename_extension_path_input():
    inpath = Path('./foo.png')
    actual_outpath = join_outdir_filename_extension(
        inpath, outdir='bar', extension='jpg'
    )
    expected_outpath = Path('bar/foo.jpg')
    assert actual_outpath == expected_outpath


def test_replace_dir_str_input():
    inpath = './foo.png'
    actual_outpath = replace_dir(inpath, '/Users/username/Desktop')
    expected_outpath = Path('/Users/username/Desktop/foo.png')
    assert actual_outpath == expected_outpath


def test_replace_dir_path_input():
    inpath = Path('./foo.png')
    actual_outpath = replace_dir(inpath, '/Users/username/Desktop')
    expected_outpath = Path('/Users/username/Desktop/foo.png')
    assert actual_outpath == expected_outpath
