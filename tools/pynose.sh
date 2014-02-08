#!/bin/bash
cd $(dirname $0)
cd ..

nosetests --with-xunit plugins/*.py modules/*.py
