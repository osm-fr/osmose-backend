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
import psycopg2
from modules import OsmSax
from modules import OsmOsis

###########################################################################

sql10 = """
SELECT
    st_x(st_centroid(geom)),
    st_y(st_centroid(geom))
FROM (
    SELECT
	(ST_Dump(ST_Polygonize(linestring))).geom AS geom
    FROM (
	SELECT
	    linestring
	FROM
	    ways
		JOIN relation_members ON ways.id = relation_members.member_id AND relation_members.member_type = 'W'
		JOIN relations ON relations.id = relation_members.relation_id AND relations.tags ? 'admin_level' AND relations.tags -> 'admin_level' = '%d'
	WHERE
	    NOT ways.is_polygon -- retire les polygones (îles et communes isolés)
	GROUP BY
	    ways.id,
	    ways.linestring
	HAVING
	    COUNT(ways.id) = 1
    ) AS foo
) AS bar
WHERE
  ST_NPoints(geom) < 100 -- Valeur exp. determiné sur l'Aquitaine pour ne pas avoir de faux positifs
;
"""

###########################################################################

def analyser(config, logger = None):

    gisconn = psycopg2.connect(config.dbs)
    giscurs = gisconn.cursor()
    apiconn = OsmOsis.OsmOsis(config.dbs, config.dbp)
    
    ## output headers
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"6060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Trou entre les limites administratives"})
    outxml.Element("classtext", {"lang":"en", "title":"Hole between administrative boundarie"})
    outxml.endElement("class")

    ## querries        
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)

    if config.options:
        admin_level = config.options["admin_level"]
    else:
        admin_level = 8

    giscurs.execute(sql10 % (admin_level))
        
    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
	outxml.startElement("error", {"class":"1", "subclass":str(abs(int(hash(res[0]*res[1]))))})
	outxml.Element("location", {"lat":str(res[1]), "lon":str(res[0])})
	outxml.endElement("error")
	
    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()

    ## close database connections
    giscurs.close()
    gisconn.close()
    del apiconn
