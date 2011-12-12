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

sql_users = """
SELECT count({0}.id) as count, user_id, users.name,
       min(tstamp) AS tstamp_min, max(tstamp) AS tstamp_max
FROM {0}
JOIN users ON users.id = user_id
GROUP BY user_id, users.name
ORDER BY count desc;
"""

sql_count = """
SELECT count(*)
FROM {0}
WHERE {1};
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

    ## querries
    logger.log(u"requête osmosis")
    giscurs.execute("SET search_path TO %s,public;" % config.dbp)

    for t in ("nodes", "ways", "relations"):
      outxml.startElement("stat_users", {"type": t})

      giscurs.execute(sql_users.format(t))
      for res in giscurs.fetchall():
        outxml.startElement("user", {"user_id":str(res[1]), "user_name":str(res[2])})
        outxml.Element("count", {"value":str(res[0])})
        outxml.Element("timestamp", {"min":str(res[3]), "max":str(res[4])})
        outxml.endElement("user")

      outxml.endElement("stat_users")

    ## output footers
    outxml.endElement("analyser")
    outxml._out.close()

if __name__=="__main__":
  country = "france_limousin"
  class config:
    dbs = "dbname=osmose"
    dst = country + ".xml"
    dbp = country

  from modules import OsmoseLog
  a = OsmoseLog.logger()
  analyser(config, a)
