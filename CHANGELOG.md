# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

# [0.4.0] - 2019-02-13
### Added
- Added hosted docs for readthedocs. 

# [0.3.1] - 2019-01-29
### Added
- Added boto3 to setup.py requirements

# [0.3.0] - 2019-01-29
### Added
- Added dataset module

# [0.2.0] - 2019-01-26
### Changed
- Elevated `group_train_test_split` to a public function in its own module.

# [0.1.16] - 2019-01-22
### Changed
- Trivial change to debug Jenkins webhook.

# [0.1.15] - 2019-01-22
### Changed
- Use `black` to format code.

# [0.1.14] - 2019-01-17
### Changed
- Trivial change to test Jenkins changes.

# [0.1.13] - 2019-01-17
### Changed
- Trivial change to test Jenkins changes.

# [0.1.12] - 2019-01-17
### Changed
- Trivial change to test Jenkins changes.

# [0.1.11] - 2019-01-17
### Fixed
- Address flake8 complaints.

# [0.1.10] - 2019-01-17
### Changed
- Used black to format code.

# [0.1.10] - 2019-01-17
### Fixed
- Remove download instructions from README now that a simple pip install should work.

# [0.1.9] - 2019-01-17
### Added
- Added functionality to save_response_content_as_png() to allow resize on download

# [0.1.8] - 2019-01-17
### Added
- Fill in more type hints.

# [0.1.7] - 2019-01-17
### Added
- Fill in some missing type hints.

# [0.1.6] - 2019-01-17
### Added
- Test Jenkins PyPI push again.

# [0.1.5] - 2019-01-17
### Added
- Modify Jenkins job to avoid trying to push old versions to PyPI.

# [0.1.4] - 2019-01-17
### Added
- Attempt to set up Jenkins job to push to PyPI.

# [0.1.3] - 2019-01-15
### Fixed
- Catch `FileExistsError` in case in which another thread creates directory after we check for it.

# [0.1.2] - 2019-01-11
### Fixed
- Another try to configure PyPI Markdown rendering.

# [0.1.1] - 2019-01-11
### Fixed
- Configure PyPI Markdown rendering.

# [0.1.0] - 2019-01-07
### Added
- Functions for downloading, resizing, and creating imagenet-style symlinks.
- Basic docs.
