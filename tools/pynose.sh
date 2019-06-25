#!/bin/bash
cd $(dirname $0)
cd ..

EXCLUDE_FILES=("plugins/Josm_de_openrailwaymap.py" "plugins/Josm_territories.py")

PYTHON_FILES=($(ls plugins/*.py modules/*.py analysers/*.py))

for del in ${EXCLUDE_FILES[@]}; do
  # remove $del from array PYTHON_FILES
  PYTHON_FILES=("${PYTHON_FILES[@]/$del}")
done

python $(which nosetests) --testmatch='(?:\b)[Tt]est' ${PYTHON_FILES[@]}
