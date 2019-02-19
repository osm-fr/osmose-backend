#!/bin/bash
cd $(dirname $0)
cd ..

nosetests --testmatch='(?:\b)[Tt]est' plugins/*.py modules/*.py analysers/*.py
