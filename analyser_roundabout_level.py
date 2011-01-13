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

from modules import OsmSaxAlea, OsmSax, OsmoseLog
import sys, commands, os, urllib, time

###########################################################################

class DataHandlerRoundabout:
    def __init__(self):
        self.ways = {}
    def WayCreate(self, data):
        if data[u"tag"].get(u"junction", None) <> u"roundabout":
            return
        if "highway" not in data[u"tag"]:
            return
        if data["nd"][0] <> data["nd"][-1]:
            return
        self.ways[data["id"]] = data

class DataHandlerWays:
    def __init__(self, nids):
        self.nids = nids
        self.ways = {}
        for nid in self.nids:
            self.ways[nid] = []
    def WayCreate(self, data):
        if not self.nids.intersection(data["nd"]):
            return
        for nid in data["nd"]:
            if nid in self.nids:
                self.ways[nid].append(data)

levels = {}
levels[u"motorway"]       = 50
levels[u"trunk"]          = 50
levels[u"primary"]        = 50
levels[u"secondary"]      = 40
levels[u"tertiary"]       = 30
levels[u"unclassified"]   = 20
levels[u"residential"]    = 20
levels[u"road"]           = 10

need_oneway = [u"primary", u"secondary", u"tertiary", u"unclassified", u"residential", u"road"]

###########################################################################

def analyser(config, logger = OsmoseLog.logger()):
        
    ## get closed roundabouts
    logger.log("get closed roundabout")
    o = DataHandlerRoundabout()
    i = OsmSaxAlea.OsmSaxReader(config.src_small)
    i.CopyWayTo(o)
    clrb = o.ways

    logger.log("create nids set")
    nids = set()
    for wid in clrb:
        for nid in clrb[wid]["nd"]:
            nids.add(nid)
            
    ## get highways
    logger.log("get highways")
    o = DataHandlerWays(nids)
    i = OsmSaxAlea.OsmSaxReader(config.src_small)
    i.CopyWayTo(o)
    ways = o.ways
    del i, o
        
    ## start output
    outxml = OsmSax.OsmSaxWriter(open(config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"3010"})
    outxml.Element("classtext", {"lang":"fr", "title":"Mauvais highway sur roundabout", "menu":"highway roundabout"})
    outxml.Element("classtext", {"lang":"en", "title":"Wrong highway on roundabout", "menu":"highway roundabout"})
    outxml.endElement("class")
    outxml.startElement("class", {"id":"2", "item":"2030"})
    outxml.Element("classtext", {"lang":"fr", "title":"oneway manquant sur insertion Rond-Point", "menu":"oneway manquant"})
    outxml.Element("classtext", {"lang":"en", "title":"Missing oneway", "menu":"missing oneway"})
    outxml.endElement("class")
    api = OsmSaxAlea.OsmSaxReader(config.src_small)

    ## analyse oneway
    logger.log("analyse level")    
    for wid in clrb:
        level = 0
        for nid in clrb[wid]["nd"]:
            for wdta in ways[nid]:
                if wdta["id"]==wid:
                    continue
                if levels.get(wdta["tag"].get(u"highway", None), 0) > level:
                    level   = levels.get(wdta["tag"].get(u"highway", None), 0)
                    highway = wdta["tag"][u"highway"]
        if level and level <> levels.get(clrb[wid]["tag"]["highway"], 0):
            outxml.startElement("error", {"class":"1", "subclass":str(level)})
            outxml.Element("text", {"lang":"en", "value":"%s => %s"%(clrb[wid]["tag"]["highway"], highway)})
            outxml.WayCreate(clrb[wid])
            n = api.NodeGet(clrb[wid]["nd"][len(clrb[wid]["nd"])/2])
            if n:
                outxml.Element("location", {"lat":str(n["lat"]),"lon":str(n["lon"])})
            outxml.endElement("error")
    
    ## analyse oneway
    logger.log("analyse oneway")
    for wid in clrb:
        insertion_ways = []
        for nid in clrb[wid]["nd"]:
            insertion_ways += ways[nid]
        #insertion_ways = [x for x in insertion_ways if x["id"]<>wid]
        insertion_ways = dict([(x["id"], x) for x in insertion_ways])
        insertion_ways.pop(wid)
        insertion_ways = insertion_ways.values()
        
        fin = {}
        for x in insertion_ways:
            if x["nd"][0] in clrb[wid]["nd"]:
                fin[x["id"]] = x["nd"][-1]
            else:
                fin[x["id"]] = x["nd"][0]
        
        for i in range(len(insertion_ways)):
            for j in range(i+1, len(insertion_ways)):
                w1 = insertion_ways[i]
                w2 = insertion_ways[j]
                if fin[w1["id"]] != fin[w2["id"]]:
                    continue
                if len(w1["nd"]) > 4 or len(w2["nd"]) > 4:
                    continue
                for w in [w1, w2]:
                    if u"oneway" in w["tag"]:
                        continue
                    if u"junction" in w["tag"]:
                        continue
                    if w["tag"].get("highway", None) not in need_oneway:
                        continue
                    outxml.startElement("error", {"class":"2"})
                    outxml.WayCreate(w)
                    n = api.NodeGet(w["nd"][len(w["nd"])/2])
                    if n:
                        outxml.Element("location", {"lat":str(n["lat"]),"lon":str(n["lon"])})
                    outxml.endElement("error")
        
    ## end output
    outxml.endElement("analyser")
    outxml._out.close()
    del api

    ## update front-end
    #if config.updt:
    #    logger.log("update front-end")
    #    urllib.urlretrieve(config.updt,"/dev/null")
