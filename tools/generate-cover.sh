#! /bin/bash

MAPSHAPER=~/.npm/mapshaper/0.2.14/package/bin/mapshaper
JSON2GEOBUF=~/.npm/geobuf/1.0.1/package/bin/json2geobuf

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)

python $SCRIPTPATH/get-polygons.py > osmose.list

mkdir generated-polygons

# Make sure that all polygons are present on polygons website
IFS=','; for i in $(cat osmose.list) ; do
  if [ ! -e generated-polygons/$i.poly ]; then
    wget -O generated-polygons/$i.poly http://polygons.openstreetmap.fr/index.py?id=$i
  fi
done

wget -O osmose-cover.json "http://polygons.openstreetmap.fr/get_geojson.py?id=$(cat osmose.list)"

rm -f osmose-cover-simplified.topojson
$MAPSHAPER osmose-cover.json -simplify 1% keep-shapes -o osmose-cover-simplified.topojson
$JSON2GEOBUF osmose-cover-simplified.topojson > osmose-cover-simplified.topojson.pbf
