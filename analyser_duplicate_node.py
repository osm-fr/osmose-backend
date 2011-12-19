#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

###########################################################################

def analyser(config, logger = None):

    ## result file    
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    
    outxml.startElement("class", {"id":"1", "item":"0"})
    outxml.Element("classtext", {"lang":"fr", "title":"TEST : Plusieurs nœuds à la même position", "menu": "test : plusieurs nœuds"})
    outxml.endElement("class")

    ## loop on results
    conn = psycopg2.connect(config.dbs)
    curs = conn.cursor()
    curs.execute("SELECT node_accum(id,tags),lat,lon FROM france_nodes GROUP BY lat,lon HAVING count(*) <> 1;")
    while True:
        all = curs.fetchmany(1000)
        if not all:
            break
        for res in all:
            outxml.startElement("error", {"class":"1"})
            outxml.Element("location", {"lat":str(float(res["lat"])/1000000),"lon":str(float(res["lon"])/1000000)})
            for i in range(len(res[0])/2):
                if res[0][2*i]=="#new#":
                    if i:
                        outxml.endElement("node")
                    outxml.startElement("node", {"id":res[0][2*i+1]})
                else:
                    outxml.Element("tag", {"k":res[0][2*i], "v":res[0][2*i+1]})
            outxml.endElement("node")
            outxml.endElement("error")

    outxml.endElement("analyser")
    outxml._out.close()

    ## update front-end
    #if config.updt:
    #    logger.log("update front-end")
    #    urllib.urlretrieve(config.updt, "/dev/null")

    ## close database connections
    curs.close()
    conn.close()
