#! /bin/sh

#f1=/data/work/geodesie/xapi-$(date +%Y-%m-%d).osm
f1=/tmp/xapi.osm
f2=~/public_html/geodesie/check-$(date +%Y-%m-%d).html

./01-download.sh $f1
./02-check.py $f1 $f2

#rm $f1
