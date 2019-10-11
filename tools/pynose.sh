#!/bin/bash
set -e

cd $(dirname $0)
cd ..

EXCLUDE_FILES=("plugins/Josm_de_openrailwaymap.py" "plugins/Josm_territories.py")

for dir in "plugins" "plugins/tests" "modules" "analysers"; do
  echo "Testing $dir"
  PYTHON_FILES=($(ls $dir/*.py))

  for del in ${EXCLUDE_FILES[@]} analysers/analyser_sax.py; do
    # remove $del from array PYTHON_FILES
    PYTHON_FILES=("${PYTHON_FILES[@]/$del}")
  done

  python $(which nosetests) --testmatch='(?:\b)[Tt]est' ${PYTHON_FILES[@]}
done

# Run analyser_sax separately to remove strange issues with nosetests analysers/*.py
echo "Testing analysers/analyser_sax.py"
python $(which nosetests) --testmatch='(?:\b)[Tt]est' analysers/analyser_sax.py
