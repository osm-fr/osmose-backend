#! /bin/sh

#wget -O $1 "http://osmxapi.hypercube.telascience.org/api/0.6/node[man_made=survey_point][bbox=-6,41,10,52]"
#wget -O $1 "http://xapi.openstreetmap.org/api/0.6/node[man_made=survey_point][bbox=-6,41,10,52]"
wget -O $1 "http://www.overpass-api.de/api/xapi?node[man_made=survey_point][bbox=-6,41,10,52]"
