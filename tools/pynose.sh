#!/bin/bash
cd $(dirname $0)
cd ..

nosetests plugins/*.py modules/*.py analysers/*.py
