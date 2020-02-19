#!/bin/bash
set -e

cd $(dirname $0)
cd ..

# pytest is configured by pytest.ini and conftest.py

if [ "x$1" = "x" ]; then
  TEST_SUITE="all"
else
  TEST_SUITE="$1"
fi

case $TEST_SUITE in
  sax)   PYTEST_PARAM="analysers/analyser_sax.py";;
  merge) PYTEST_PARAM="analysers/Analyser_Merge.py";;
  other) PYTEST_PARAM="--ignore=analysers/analyser_sax.py --ignore=analysers/Analyser_Merge.py";;
  *)     PYTEST_PARAM="";;
esac

python3 $(which pytest) $PYTEST_PARAM
