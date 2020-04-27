#!/bin/bash

# guarantee script exits with non-zero code
# the first time any of these commands fail
set -e

pytest
flake8 creevey tests
black creevey tests --skip-string-normalization --check
sphinx-build docs docs/_html
