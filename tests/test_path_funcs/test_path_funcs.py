from pathlib import Path

from creevey.path_funcs import (
    join_outdir_filename_extension,
    join_outdir_hashed_path_extension,
    replace_dir,
)


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


def test_join_outdir_filename_extension_extension_none():
    inpath = Path('./foo.png')
    actual_outpath = join_outdir_filename_extension(inpath, outdir='bar')
    expected_outpath = Path('bar/foo.png')
    assert actual_outpath == expected_outpath


def test_join_outdir_hashed_path_extension():
    inpath = Path('./foo.png')
    actual_outpath = join_outdir_hashed_path_extension(
        inpath, outdir='bar', extension='jpg'
    )
    expected_pardir = Path('bar')
    expected_extension = '.jpg'
    assert actual_outpath.parent == expected_pardir
    assert actual_outpath.suffix == expected_extension
    assert actual_outpath.stem != 'foo'

    # check consistency in repeated applications
    actual_outpath2 = join_outdir_hashed_path_extension(
        inpath, outdir='bar', extension='jpg'
    )
    assert actual_outpath2 == actual_outpath


def test_join_outdir_hashed_path_no_extension():
    inpath = Path('./foo.png')
    actual_outpath = join_outdir_hashed_path_extension(inpath, outdir='bar')
    expected_pardir = Path('bar')
    expected_extension = '.png'
    assert actual_outpath.parent == expected_pardir
    assert actual_outpath.suffix == expected_extension
    assert actual_outpath.stem != 'foo'

    # check consistency in repeated applications
    actual_outpath2 = join_outdir_hashed_path_extension(inpath, outdir='bar')
    assert actual_outpath2 == actual_outpath


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
