#! /usr/bin/env python
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

import sys, commands, os, urllib, time, tempfile, bz2, popen2, urllib2
sys.path.append("..")
from modules import OsmSaxAlea, OsmSax, OsmoseLog

###########################################################################

class ConverterTo:
    def __init__(self, dst):
        self.dst = dst
    def NodeCreate(self, data):
        if data["tag"]["type"] <> u"0":
            return
        self.dst.startElement("error", {"class":"1", "subclass":str(data["id"])})
        self.dst.Element("text", {"lang":"en", "value":data["tag"]["text"]})
        self.dst.Element("location", {"lat":str(data["lat"]),"lon":str(data["lon"])})
        self.dst.endElement("error")
        
def run(logger = OsmoseLog.logger()):
        
    xml_loc = "/data/work/osmose/tmp/osb.xml"
    xml_url = "http://osm102.openstreetmap.fr/osmose/osb.xml"
    
    front_code = "xxx"
    front_id   = 62
    front_url  = "http://osmose.openstreetmap.fr/cgi-bin/update.py"
    
    src_url = "http://openstreetbugs.schokokeks.org/dumps/osbdump_latest.sql.bz2"
    src_cmd = "wget -o /dev/null -O - %s | bunzip2 | ./osbsql2osm" % src_url
    src     = popen2.popen2(src_cmd)[0]
    
    ## streams
    i = OsmSax.OsmSaxReader(src)
    o = ConverterTo(OsmSax.OsmSaxWriter(open(xml_loc, "w"), "UTF-8"))
    
    ## headers
    o.dst.startDocument()
    o.dst.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    o.dst.startElement("class", {"id":"1", "item":"7030"})
    o.dst.Element("classtext", {"lang":"en", "title":"OpenStreetBugs"})
    o.dst.endElement("class")
    
    ## content
    logger.log("generate xml report")
    i.CopyTo(o)
        
    ## footers
    o.dst.endElement("analyser")
    o.dst._out.close()
    
    ## update
    logger.log("update front-end")
    tmp_req = urllib2.Request(front_url)
    tmp_dat = urllib.urlencode([('url', xml_url), ('code', front_code)])
    fd = urllib2.urlopen(tmp_req, tmp_dat)
    dt = fd.read().decode("utf8").strip()
    if dt <> "OK":
        sys.stderr.write("error: %s"%(dt.encode("utf8")))
        logger.sub().log(dt)
        
    logger.log("done")
    
###########################################################################

if __name__=="__main__":
    run()
