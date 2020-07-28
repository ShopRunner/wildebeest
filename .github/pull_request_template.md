# Pull Request Checklist

Contributors from outside ShopRunner should feel free to submit a PR without having completed all of the items below. See [CONTRIBUTING.md](https://github.com/ShopRunner/creevey/blob/master/CONTRIBUTING.md) for additional information.

## General

- [ ] Pull request includes a description of the change and the reason behind it.
- [ ] Pull request [uses keywords](https://help.github.com/en/articles/closing-issues-using-keywords) to close relevant [issues](https://github.com/ShopRunner/creevey/issues).
- [ ] Pull request includes unit tests for any bug fixes and new functionality.
- [ ] `./.ci/test.sh` passes locally.
- [ ] Docs have been updated as needed. (`./.ci/test.sh` rebuilds the docs. Open `docs/_html/index.html` to check them.)

## ShopRunner Contributors

The maintainer will complete the following steps for external contributions.

- [ ] `CHANGELOG.md` has been updated.
- [ ] `_version.py` has been updated.
- [ ] Version number has been updated in `docs/conf.py`.
