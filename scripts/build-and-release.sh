#!/bin/bash

# exit when any command fails
set -e

old dist build

python3 -m build

python3 -m twine upload dist/*
