#!/bin/bash
set -e

cd $(dirname $0)
cd ..

# pytest is configured by pytest.ini and conftest.py

PYTEST=$(which pytest || true)
if [ "x$PYTEST" = "x" ]; then
  PYTEST=$(which pytest-3 || true)
fi
if [ "x$PYTEST" = "x" ]; then
  echo "Couldn't find pytest or pytest-3"
  exit 1
fi

if [ "x$1" = "x" ]; then
  TEST_SUITE="all"
else
  TEST_SUITE="$1"
fi

case $TEST_SUITE in
  lint)  pylama; exit $?;;
  mypy)  mypy .; exit $?;;
  sax)   PYTEST_PARAM="analysers/analyser_sax.py";;
  merge) PYTEST_PARAM="analysers/Analyser_Merge.py";;
  other) PYTEST_PARAM="--ignore=analysers/analyser_sax.py --ignore=analysers/Analyser_Merge.py";;
  *)     PYTEST_PARAM="";;
esac

python3 $PYTEST $PYTEST_PARAM
