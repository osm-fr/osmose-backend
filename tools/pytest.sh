#!/bin/bash
set -e

cd $(dirname $0)
cd ..

# pytest is configured by pytest.ini and conftest.py

python $(which pytest)
