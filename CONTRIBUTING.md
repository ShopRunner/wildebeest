# Contributing

## How to Contribute

We welcome contributions in the form of issues or pull requests! 

We want this to be a place where all are welcome to discuss and contribute, so please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. Find the code of conduct in the ``CONDUCT.md`` file on GitHub.

If you have a problem using Creevey or see a possible improvement, open an issue in the GitHub issue tracker. Please be as specific as you can.

If you see an open issue you'd like to be fixed, take a stab at it and open a PR!

## Steps for Making a Pull Request

1. Fork the project from GitHub. (Internal ShopRunner contributors can skip this step.)
2. Clone the forked repo to your local disk. 

```bash
git clone https://github.com/<your_github_user_name>/creevey.git
```

3. `cd` into the directory.
4. Create a new branch.

```bash
git checkout -b my_awesome_new_feature
```

5. Install the library. (We recommend using a virtual environment.)
    
```bash
pip install -e . 
```

6. Make your changes.
7. Update the unit tests, _version.py, and CHANGELOG.
8. Run `black creevey tests --skip-string-normalization` to format code.
9. Run `./.ci/test.sh` to check that unit tests pass and the linter doesn't complain.
10. Submit your PR against the `wip` branch.

We prefer single quotes for strings unless using double quotes allows us to avoid escaping internal single quotes. We use numpy style for docstrings and run code using CPython 3.6+.
