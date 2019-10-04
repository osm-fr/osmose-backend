#!/bin/bash
set -e

cd $(dirname $0)
cd ..

EXCLUDE_FILES=("plugins/Josm_de_openrailwaymap.py" "plugins/Josm_territories.py")

for dir in "plugins" "plugins/tests" "modules" "analysers"; do
  PYTHON_FILES=($(ls $dir/*.py))

  for del in ${EXCLUDE_FILES[@]}; do
    # remove $del from array PYTHON_FILES
    PYTHON_FILES=("${PYTHON_FILES[@]/$del}")
  done

  python $(which nosetests) --testmatch='(?:\b)[Tt]est' ${PYTHON_FILES[@]}
done
