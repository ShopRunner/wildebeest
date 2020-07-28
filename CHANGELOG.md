# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

#[3.0.0] - 2020-7-28
### Changed
 - Rename library "wildebeest"
 - Use GitHub Actions for CI/CD.

#[2.3.0] - 2020-7-24
### Added 
 - Use `pip-tools`.

#[2.2.0] - 2020-6-15
### Added 
 - Function rotate() that takes an image and an angle and ouputs the rotated image.
 - warning about upcoming rename of library

# [2.1.0] - 2020-6-3
### Added
 - Function to flip an image horizontally.
 - Function to flip an image vertically.

# [2.0.0] - 2020-4-21
### Changed
 - Pipelines now take a function to decide whether to skip a file based on its input and output paths, rather than just providing the option to skip files whose outpath points to a local file. "skipped_existing" field of run report has been renamed to "skipped" accordingly.
 - Run report is now stored in `<Pipeline object>.run_report_` rather than being returned.
 - All exceptions that inherit from `Exception` that arise during file processing are now handled by default.
 - Rather than noting whether an exception was handled in processing a particular file in an "exception_handled" field, the run report now contains either the exception object itself or `np.nan` in a field called "error."
 - "time_finished" field in run reports now uses human-readable timestamps.
 - `Pipeline.run()` method has been removed; now pipelines can only be called directly.
 - `Pipeline.ops` is now `None` by default.
 - Moved most of the README content to readthedocs, improved the examples, and added docstrings.
 - `log_dict` is now a Pipeline attribute.
 - `pipelines/core.py` has been renamed to `pipelines/pipelines.py`

# [1.7.2] - 2020-4-2
### Added
 - Example text scraping application.

# [1.7.1] - 2020-4-1
### Changed
 - Have `flake8` check for docstrings in library functions and classes.

# [1.7.0] - 2020-3-27
### Added
 - Pipelines can now be called directly rather than through a `.run()` method; `.run()` still exists as an alias for backwards compatibility.

# [1.6.3] - 2020-3-2
### Fixed
 - `write_image` writes to a tempfile in a ".tmp" subdirectory in the output directory rather than in an arbitrary location to avoid issues when writing to a mounted volume.

# [1.6.2] - 2020-2-28
### Changed
 - `write_image` writes to a tempfile and then renames it to ensure that it does not create partial image files if writing is interrupted.

# [1.6.1] - 2020-1-14
### Changed
 - Downloads timeout after 5s by default if no response received.

# [1.6.0] - 2019-10-17
### Added
 - `record_dhash` function
 
# [1.5.0] - 2019-10-17
### Added
 - `trim_padding` function

# [1.4.4] - 2019-10-16
### Fixed
 - `centercrop` can now be used within a `CustomReportingPipeline`.

# [1.4.3] - 2019-9-16
### Fixed
 - Bug in error response when loading an image with unusual errors

# [1.4.2] - 2019-6-17
### Changed
 - provide one script to run pre-merge checks
 - refine PR checklist
### Fixed
 - typo in README
 - typo in `skip_existing=True` warning message

# [1.4.1] - 2019-5-31
### Fixed
 - Sort actual and expected DataFrames by column name in `test_custom_reporting_pipeline` to avoid uninteresting indeterministic failure.

# [1.4.0] - 2019-5-31
### Added
 - Centercrop function into ops/image.py

# [1.3.3] - 2019-5-17
### Changed
 - Revert reading version number from CHANGELOG.md in setup.py and _version.py

# [1.3.2] - 2019-5-10
### Changed
 - Read version number from CHANGELOG.md in setup.py and _version.py

# [1.3.1] - 2019-5-6
### Changed
 - Instead of logging a warning for every file skipped, warn once up front and log with level DEBUG.

# [1.3.0] - 2019-4-9
### Added
 - Function to generate unique filenames from input paths, outdir, extension
 - Ability to keep original extension with using `join_outdir_filename_extension`

# [1.2.3] - 2019-3-17
### Fixed
 - Load color channels from URL in RGB order

# [1.2.2] - 2019-3-10
### Fixed
 - Added empty `__init__.py` files, the absence of which seems to be causing problems when installing from PyPI.
 - Converted some `Path` objects to strings where required in Python 3.6.

# [1.2.1] - 2019-3-10
### Fixed
 - Handled string path inputs in `replace_dir`
### Added
 - Added simple unit tests for `path_funcs` module

# [1.2.0] - 2019-3-7
### Added
 - Added hosted docs for readthedocs.

# [1.1.0] - 2019-3-2
### Added
 - `Pipeline` runs return "run reports"
 - `CustomReportingPipeline` class allows custom run report fields

# [1.0.0] - 2019-2-23
### Changed
 - Redesigned library around `Pipeline` abstraction

# [0.3.2] - 2019-2-15
### Changed
 - Switched to using one requests session in each download thread.

# [0.3.1] - 2019-1-29
### Added
 - Added boto3 to setup.py requirements.

# [0.3.0] - 2019-1-29
### Added
 - Added dataset module

# [0.2.0] - 2019-1-26
### Changed
 - Elevated `group_train_test_split` to a public function in its own module.

# [0.1.15] - 2019-1-22
### Changed
 - Use `black` to format code.

# [0.1.11] - 2019-1-17
### Fixed
 - Address flake8 complaints.

# [0.1.10] - 2019-1-17
### Changed
 - Used black to format code.
 - Remove download instructions from README now that a simple pip install should work.

# [0.1.9] - 2019-1-17
### Added
 - Added functionality to save_response_content_as_png() to allow resize on download

# [0.1.8] - 2019-1-17
### Added
 - Fill in some missing type hints.

# [0.1.5] - 2019-1-17
### Added
 - Modify Jenkins job to avoid trying to push old versions to PyPI.

# [0.1.3] - 2019-1-15
### Fixed
 - Catch `FileExistsError` in case in which another thread creates directory after we check for it.

# [0.1.2] - 2019-1-11
### Fixed
 - Configure PyPI Markdown rendering.

# [0.1.0] - 2019-1-7
### Added
 - Functions for downloading, resizing, and creating imagenet-style symlinks.
 - Basic docs.
