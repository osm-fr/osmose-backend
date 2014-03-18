#! /bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)

python $SCRIPTPATH/get-polygons.py > osmose.list

wget -O osmose-cover.json "http://polygons.openstreetmap.fr/get_geojson.py?id=$(cat osmose.list)"
wget -O osmose-cover.png "http://polygons.openstreetmap.fr/get_image_union.py?id=$(cat osmose.list)"
