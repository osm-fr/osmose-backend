#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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
DROP VIEW IF EXISTS monuments_osm CASCADE;
CREATE TEMP VIEW monuments_osm AS
(
SELECT
    'W' AS type,
    id,
    tags->'ref:mhs' AS ref
FROM
    ways
WHERE
    tags?'heritage' AND
    tags?'heritage:operator' AND
    tags?'ref:mhs'
)
UNION
(
SELECT
    'N' AS type,
    id,
    tags->'ref:mhs' AS ref
FROM
    nodes
WHERE
    tags?'heritage' AND
    tags?'heritage:operator' AND
    tags?'ref:mhs'
)
;

SELECT
    osmose.monuments_fr.notice, -- 0
    osmose.monuments_fr.lat2, -- 1
    osmose.monuments_fr.long2, -- 2
    osmose.monuments_fr.adresse, -- 3
    osmose.monuments_fr.commune, -- 4
    osmose.monuments_fr.monument, -- 5
    osmose.monuments_fr.protection, -- 6
    osmose.monuments_fr.date, -- 7
    osmose.monuments_fr.image -- 8
FROM
    osmose.monuments_fr
    LEFT JOIN monuments_osm ON
        osmose.monuments_fr.notice = monuments_osm.ref
WHERE
    monuments_osm.ref IS NULL
;

"""

###########################################################################

def analyser(config, logger = None):

    gisconn = PgSQL.Connection(config.dbs)
    giscurs = gisconn.cursor()
    apiconn = OsmOsis.OsmOsis(config.dbs, config.dbp)

    ## output headers
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"7011"})
    outxml.Element("classtext", {"lang":"fr", "title":"Monument historique"})
    outxml.endElement("class")

    ## querries
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1", "subclass":str(abs(int(hash(res[0]))))})
        outxml.Element("location", {"lat":str(res[1]), "lon":str(res[2])})
        outxml.Element("text", {"lang":"fr", "value":"Manque monument historique name=%s heritage=* (%s); heritage:operator=mhs; ref:mhs=<a href='http://www.culture.gouv.fr/public/mistral/merimee_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1=%s'>%s</a> mhs:inscription_date=%s (%s, %s)" % (res[5], res[6], res[0], res[0], res[7],res[3], res[4])})
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
