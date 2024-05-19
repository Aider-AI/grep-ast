#!/bin/bash

##
## Bump the version in setup.py first
##

# exit when any command fails
set -e

old dist build

python3 -m build

python3 -m twine upload dist/*
