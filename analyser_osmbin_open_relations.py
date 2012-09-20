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

import sys, urllib2, time, os, urllib
from modules import OsmBin, OsmSax

###########################################################################

def data2dict(data):
    res = {"node":{}, "way":{}, "relation":{}}
    for x in data:
        res[x["type"]][x["data"]["id"]] = x["data"]
    return res

def get_ways(relid):
    data = bin.RelationFullRecur(relid, WayNodes = False, RaiseOnLoop = False, RemoveSubarea = True)
    ways = []
    for x in data:
        if x["type"] == "way":
            ways.append(x["data"])
    return ways

def ways_bounds(ways):
    nodes = []
    for w in ways:
        if not w[u"nd"]:
            continue
        nodes.append(w[u"nd"][0])
        nodes.append(w[u"nd"][-1])
    err = []
    for n in set(nodes):
        if (nodes.count(n) % 2) == 1:
            err.append((n, nodes.count(n)))
    return err

###########################################################################

class SaxAnalyse:

    def __init__(self, dst):
        self.outxml = OsmSax.OsmSaxWriter(open(dst, "w"), "UTF-8")
        self.outxml.startDocument()
        self.outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        self.outxml.startElement("class", {"id":"1", "item":"6010"})
        self.outxml.Element("classtext", {"lang":"fr", "title":"Relation ouverte"})
        self.outxml.Element("classtext", {"lang":"en", "title":"Open relation"})
        self.outxml.endElement("class")

    def __del__(self):
        self.outxml.endElement("analyser")
        self.outxml._out.close()

    def RelationCreate(self, data):

        if data[u"tag"].get(u"boundary", None) <> u"administrative":
            return
        if data[u"tag"].get(u"type", None) == u"boundary_segment":
            return
        if data[u"tag"].get(u"type", None) == u"multilinestring":
            return

        try:
            ways = get_ways(data["id"])
        except OsmBin.MissingDataError, e:
            print e, "on relation", data["id"]
            return
        except OsmBin.RelationLoopError, e:
            print e, "on relation", data["id"]
            return

        bnds = ways_bounds(ways)

        for nid, cpt in bnds:
            ndata = bin.NodeGet(nid)
            if ndata:
                self.outxml.startElement("error", {"class":"1"})
                data["member"] = []
                self.outxml.RelationCreate(data)
                self.outxml.NodeCreate(ndata)
                self.outxml.Element("location", {"lat":str(ndata["lat"]),"lon":str(ndata["lon"])})
                self.outxml.endElement("error")
            else:
                raise SystemError(data)

###########################################################################
## analyse

bin = OsmBin.OsmBin("/data/work/osmbin/data/")
out = SaxAnalyse("/var/www/osmose/analyser_mega_relation-world.xml")
bin.CopyRelationTo(out)
del out

###########################################################################
## update

tmp_req = urllib2.Request("http://osmose.openstreetmap.fr/cgi-bin/update.py")
tmp_url = "http://osm3.crans.org/osmose/analyser_mega_relation-world.xml"
tmp_dat = urllib.urlencode([('url', tmp_url), ('code', 'xxx')])
fd = urllib2.urlopen(tmp_req, tmp_dat)
dt = fd.read().decode("utf8").strip()
if dt[-2:] <> "OK":
    print "Error updating:\n"+dt.strip()

