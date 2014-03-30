#! /bin/bash

MAPSHAPER=~/.npm/mapshaper/0.1.17/package/bin/mapshaper

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)

python $SCRIPTPATH/get-polygons.py > osmose.list

wget -O osmose-cover.json "http://polygons.openstreetmap.fr/get_geojson.py?id=$(cat osmose.list)"
wget -O osmose-cover.png "http://polygons.openstreetmap.fr/get_image_union.py?id=$(cat osmose.list)"

rm osmose-cover-simplified.json
$MAPSHAPER --keep-shapes --auto-snap -p 0.001 osmose-cover.json -f geojson -o osmose-cover-simplified.json
