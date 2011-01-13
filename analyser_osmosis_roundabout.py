#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo <****@free.fr> 2010                       ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

import sys, re, popen2, urllib, time
from pyPgSQL import PgSQL
from modules import OsmSax
from modules import OsmOsis

###########################################################################

sql10 = """
SELECT
	ways.id,
	st_x(st_centroid(geom)),
	st_y(st_centroid(geom))
FROM
	ways
		JOIN way_tags AS wth ON ways.id = wth.way_id AND wth.k = 'highway' AND wth.v IN ('primary','secondary','tertiary','residential') -- c'est une route pour voiture
		LEFT JOIN way_tags AS wtj ON ways.id = wtj.way_id AND wtj.k = 'junction' AND wtj.v='roundabout'
		LEFT JOIN way_tags AS wta ON ways.id = wta.way_id AND wta.k = 'area'
		LEFT JOIN way_tags AS wtn ON ways.id = wtn.way_id AND wtn.k = 'name'
		JOIN way_geometry ON ways.id = way_geometry.way_id AND
			ST_IsClosed(way_geometry.geom) AND -- C'est un polygone
			ST_NPoints(geom) > 3  AND
			ST_NPoints(geom) < 24 AND
			ST_MaxDistance(st_Transform(geom,26986),st_Transform(geom,26986)) < 80 AND -- Le way fait moind de 80m(?) de diamÃ¨tre
			ST_Area(ST_Transform(geom,26986))/ST_Area(ST_MinimumBoundingCircle(ST_Transform(geom,26986))) > 0.7 -- 90% de rp recouvrent plus 70% du cercle englobant
WHERE
	wtj.k IS NULL AND -- pas de tag junction=roundabout
	wta.k IS NULL AND -- pas de tag area=*
	(wtn.k IS NULL OR wtn.v LIKE 'Rond%') -- pas de nom ou commence par 'Rond'
;
"""

###########################################################################

def analyser(config, logger = None):

    gisconn = PgSQL.Connection(config.dbs)
    giscurs = gisconn.cursor()
    apiconn = OsmOsis.OsmOsis(config.dbs)
    
    ## output headers
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"2010"})
    outxml.Element("classtext", {"lang":"fr", "title":"Rond-point non valide (osmosis)"})
    outxml.Element("classtext", {"lang":"en", "title":"Bad roundabout (osmosis)"})
    outxml.endElement("class")

    ## querries        
    logger.log(u"requête osmosis")
    giscurs.execute(sql10)
        
    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
	outxml.startElement("error", {"class":"1"})
	outxml.Element("text", {"lang":"fr", "value":"Manque junction=roundabout"})
	outxml.Element("text", {"lang":"en", "value":"Missing junction=roundabout"})
	outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
	outxml.WayCreate(apiconn.WayGet(res[0]))
	outxml.endElement("error")	
	
    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
