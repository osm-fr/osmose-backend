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
  st_x(st_centroid(geom)),
  st_y(st_centroid(geom))
FROM
  (
    SELECT
      (ST_Dump(ST_Polygonize(geom))).geom AS geom
    FROM
      (
        SELECT
          id
        FROM
          ways
        JOIN
          relation_members
        ON
          id=member_id AND
          member_type='W'
        JOIN
          relation_tags
        ON
          relation_tags.relation_id=relation_members.relation_id
          AND relation_tags.k='admin_level'
          AND relation_tags.v='8'
        GROUP BY
          id
        HAVING
          COUNT(id)=1
      ) AS foo
    JOIN
      way_geometry
    ON
      id=way_id AND NOT ST_IsClosed(geom) --  retire les polygones (îles et communes isolés)
  ) AS bar
WHERE
  ST_NPoints(geom) < 100 -- Valeur exp. determiné sur l'Aquitaine pour ne pas avoir de faux positifs
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
    outxml.startElement("class", {"id":"1", "item":"6060"})
    outxml.Element("classtext", {"lang":"fr", "title":"Incohérence de limites administratives"})
    outxml.Element("classtext", {"lang":"en", "title":"Administrative boundarie inconsistencies"})
    outxml.endElement("class")

    ## querries        
    logger.log(u"requête osmosis")
    giscurs.execute(sql10)
        
    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
	outxml.startElement("error", {"class":"1", "subclass":str(abs(int(hash(res[0]*res[1]))))})
	outxml.Element("text", {"lang":"fr", "value":"Trou entre les limites administratives"})
	outxml.Element("text", {"lang":"en", "value":"Hole between administrative boundarie"})
	outxml.Element("location", {"lat":str(res[1]), "lon":str(res[0])})
	#outxml.WayCreate(apiconn.WayGet(res[0]))
	outxml.endElement("error")
	
    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
