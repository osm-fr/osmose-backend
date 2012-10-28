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

from Analyser import Analyser

from modules import OsmSaxAlea, OsmSax, OsmoseLog
import sys, commands, os, urllib, time

###########################################################################

class DataHandler:
    def __init__(self):
        self.ways = {}
        self.rels = {}        
    def WayCreate(self, data):
        if data[u"tag"].get(u"boundary", None) <> u"administrative":
            return
        self.ways[data["id"]] = data
    def RelationCreate(self, data):
        if data[u"tag"].get(u"boundary", None) <> u"administrative":
            return
        self.rels[data["id"]] = data

###########################################################################

class Analyser_Admin_Level(Analyser):

  def __init__(self, config, logger = OsmoseLog.logger()):
    Analyser_Osmosis.__init__(self, config, logger)

  def analyser(self):
    
    o = DataHandler()
    i = OsmSaxAlea.OsmSaxReader(self.config.src)
    
    ## get relations
    self.logger.log("get ways data")
    i.CopyWayTo(o)
    wdta = o.ways
    
    ## get ways id
    self.logger.log("get relations data")
    i.CopyRelationTo(o)
    rdta = o.rels    

    del i, o
    
    ## start output
    outxml = OsmSax.OsmSaxWriter(open(self.config.dst, "w"), "UTF-8")
    outxml.startDocument()
    outxml.startElement("analyser", {"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    outxml.startElement("class", {"id":"1", "item":"6050"})
    outxml.Element("classtext", {"lang":"fr", "title":"Mauvais niveau administratif", "menu":"admin_level"})
    outxml.Element("classtext", {"lang":"en", "title":"Wrong administrative level", "menu":"admin_level"})
    outxml.endElement("class")
    api = OsmSaxAlea.OsmSaxReader(self.config.src)

    ## find admin level
    way_to_level = {}
    rel_to_level = {}
    for wid in wdta:
        way_to_level[wid] = 99
    for rid in rdta:
        rel_to_level[rid] = 99
    
    for rid in rdta:
        
        try:
            level = int(rdta[rid]["tag"]["admin_level"])
        except:
            # find node in relation
            wid = [x["ref"] for x in rdta[rid]["member"] if x["type"]=="way"]
            if not wid:
                continue
            wid = wid[0]
            wta = api.WayGet(wid)
            if not wta["nd"]:
                continue
            nid = wta["nd"][0]
            nta = api.NodeGet(nid)
            if not nta:
                continue
            # add error to xml
            outxml.startElement("error", {"class":"1"})
            outxml.Element("text", {"lang":"fr", "value":"admin_level illisible"})
            outxml.Element("text", {"lang":"en", "value":"admin_level unreadable"})
            outxml.RelationCreate(rdta[rid])
            outxml.Element("location", {"lat":str(nta["lat"]),"lon":str(nta["lon"])})
            outxml.endElement("error")            
            continue
        
        for m in rdta[rid][u"member"]:
            if m[u"type"] == u"way":
                if m[u"ref"] in way_to_level:
                    way_to_level[m[u"ref"]] = min(way_to_level[m[u"ref"]], level)
            if m[u"type"] == u"relation":
                if m[u"ref"] in rel_to_level:
                    rel_to_level[m[u"ref"]] = min(rel_to_level[m[u"ref"]], level)

    ##
    for wid in wdta:
        
        try:
            level = int(wdta[wid]["tag"]["admin_level"])
        except:
            outxml.startElement("error", {"class":"1"})
            outxml.Element("text", {"lang":"fr", "value":"admin_level illisible"})
            outxml.Element("text", {"lang":"en", "value":"admin_level unreadable"})
            outxml.WayCreate(wdta[wid])
            n =  api.NodeGet(wdta[wid]["nd"][0])
            if n:
                outxml.Element("location", {"lat":str(n["lat"]),"lon":str(n["lon"])})
            outxml.endElement("error")
            continue
        
        if way_to_level[wid] not in [99, level]:
            outxml.startElement("error", {"class":"1"})
            outxml.Element("text", {"lang":"fr", "value":"admin_level devrait être %d"%way_to_level[wid]})
            outxml.Element("text", {"lang":"en", "value":"admin_level should be %d"%way_to_level[wid]})
            outxml.WayCreate(wdta[wid])
            n = api.NodeGet(wdta[wid]["nd"][0])
            if n:
                outxml.Element("location", {"lat":str(n["lat"]),"lon":str(n["lon"])})
            outxml.endElement("error")
            continue

    outxml.endElement("analyser")
    outxml._out.close()
    del api

    ## update front-end
    #if self.config.updt:
    #    self.logger.log("update front-end")
    #    urllib.urlretrieve(self.config.updt,"/dev/null")

###########################################################################

