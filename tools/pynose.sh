#!/bin/bash
cd $(dirname $0)
cd ..

python $(which nosetests) --testmatch='(?:\b)[Tt]est' plugins/*.py modules/*.py analysers/*.py
