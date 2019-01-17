# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

# [0.1.8] - 2019-01-17
### Added
- Added functionality to save_response_content_as_png() to allow resize on download

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
