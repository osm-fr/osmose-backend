#! /bin/bash

MAPSHAPER=~/.npm/mapshaper/0.2.14/package/bin/mapshaper
JSON2GEOBUF=~/.npm/geobuf/1.0.1/package/bin/json2geobuf

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)

python $SCRIPTPATH/get-polygons.py > osmose.list

wget -O osmose-cover.json "http://polygons.openstreetmap.fr/get_geojson.py?id=$(cat osmose.list)"

rm -f osmose-cover-simplified.topojson
$MAPSHAPER osmose-cover.json -simplify 1% keep-shapes -o osmose-cover-simplified.topojson
$JSON2GEOBUF osmose-cover-simplified.topojson > osmose-cover-simplified.topojson.pbf
