#!/bin/bash
cd $(dirname $0)
cd ..

# grep will return 0 only if it founds something, but our script
# wants to return 0 when it founds nothing!
pyflakes . | grep -vE "\('T_'\|/disabled/\)" && exit 1 || exit 0
