#!/bin/bash

# guarantee script exits with non-zero code
# the first time any of these commands fail
set -e

pytest --cov=./ --cov-report=xml
flake8 wildebeest tests
black wildebeest tests --skip-string-normalization --check
sphinx-build docs docs/_html
