# Pull Request Process

Contributors from outside ShopRunner should feel free to submit a PR without having completed all of the items below. See [CONTRIBUTING.md](https://github.com/ShopRunner/wildebeest/blob/main/CONTRIBUTING.md) for additional information.

You can run `./.ci/test.sh` locally to check for style issues, run tests, rebuild docs, etc. before submitting changes.

## Description

DESCRIBE THE CHANGE AND EXPLAIN THE REASON BEHIND IT

## Checklist

### General

- [ ] Pull request [uses keywords](https://help.github.com/en/articles/closing-issues-using-keywords) to close relevant [issues](https://github.com/ShopRunner/wildebeest/issues).
- [ ] Pull request includes unit tests for any bug fixes and new functionality.
- [ ] Docs have been updated as needed. (`sphinx-build docs docs/_html` rebuilds the docs. Open `docs/_html/index.html` to check them.)

### ShopRunner Contributors

The maintainer will complete the following steps for contributions from outside ShopRunner.

- [ ] `CHANGELOG.md` has been updated.
- [ ] `_version.py` has been updated.
- [ ] Version number has been updated in `docs/conf.py`.
