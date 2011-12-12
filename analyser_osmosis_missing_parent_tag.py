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
import psycopg2
from modules import OsmSax
from modules import OsmOsis

###########################################################################

sql10 = """
SELECT
    ways.id,
    ST_X(ST_Centroid(linestring)),
    ST_Y(ST_Centroid(linestring)),
    t0,
    t1
FROM
    ways,
    (
    SELECT
        base as t0,
        ways.tags->base AS t1,
        ways.tags->(ways.tags->base) AS t2,
        COUNT(*) AS c
    FROM
        ways,
        (VALUES ('highway'), ('cycleway'), ('waterway'), ('railway'), ('power'), ('man_made'), ('leisure'), ('amenity'), ('shop'), ('craft'), ('emergency'), ('tourism'), ('historic'), ('landuse'), ('military'), ('natural'), ('route'), ('boundary'), ('sport')) as t(base)
    WHERE
        ways.tags->base NOT IN ('cycleway', 'wood') AND
        ways.tags?base AND
        ways.tags?(ways.tags->base)
    GROUP BY
        base,
        t1,
        t2
    HAVING
        COUNT(*) > 50
    ) AS ref
WHERE
    NOT tags?t0 AND
    tags?t1 AND
    tags->t1 = t2
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
    outxml.startElement("class", {"id":"1", "item":"2050"})
    outxml.Element("classtext", {"lang":"fr", "title":"Tag parent manquant"})
    outxml.Element("classtext", {"lang":"en", "title":"Missing parent tag"})
    outxml.endElement("class")

    ## querries
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)
    giscurs.execute(sql10)

    ## output data
    logger.log(u"génération du xml")
    for res in giscurs.fetchall():
        outxml.startElement("error", {"class":"1"})
        outxml.Element("text", {"lang":"fr", "value":"Manque %s=%s" % (res[3],res[4])})
        outxml.Element("text", {"lang":"en", "value":"Missing %s=%s" % (res[3],res[4])})
        outxml.Element("location", {"lat":str(res[2]), "lon":str(res[1])})
        outxml.WayCreate(apiconn.WayGet(res[0]))
        outxml.endElement("error")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()
