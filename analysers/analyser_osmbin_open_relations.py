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

from Analyser import Analyser
from modules import OsmoseErrorFile

import sys, urllib2, time, os, urllib
from modules import OsmBin, OsmSax, OsmoseLog

###########################################################################

def data2dict(data):
    res = {"node":{}, "way":{}, "relation":{}}
    for x in data:
        res[x["type"]][x["data"]["id"]] = x["data"]
    return res

def get_ways(relid, bin):
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

    def __init__(self, config, bin):
        self.bin = bin
        self.error_file = OsmoseErrorFile.ErrorFile(config)
        self.error_file.begin()
        self.error_file.analyser()
        self.error_file.classs(1, 6010, 3, ["geom","boundary"],
                               {"fr": "Relation ouverte type=boundary",
                                "en": "Open relation type=boundary"})
        self.error_file.classs(2, 6010, 3, ["geom"],
                               {"fr": "Relation ouverte type=multipolygon",
                                "en": "Open relation type=multipolygon"})
        for admin_level in xrange(0, 15):
            if i <= 6:
                level= 1
            elif i <= 8:
                level = 2
            else:
                level = 3
            self.error_file.classs(100 + admin_level, 6010, level, ["geom","boundary"],
                                   {"fr": "Relation ouverte type=boundary admin_level=%d" % admin_level,
                                    "en": "Open relation type=boundary admin_level=%d" % admin_level})

        self.classs = {"boundary": 1, "multipolygon": 2}

    def __del__(self):
        self.error_file.analyser_end()
        self.error_file.end()

    def RelationCreate(self, data):

        if data[u"tag"].get(u"type", None) != u"boundary" and data[u"tag"].get(u"type", None) != u"multipolygon":
            return

        try:
            ways = get_ways(data["id"], self.bin)
        except OsmBin.MissingDataError, e:
            print e, "on relation", data["id"]
            return
        except OsmBin.RelationLoopError, e:
            print e, "on relation", data["id"]
            return

        bnds = ways_bounds(ways)

        classs = self.classs[data["tag"]["type"]]

        if "admin_level" in data["tag"]:
            try:
                admin_level = int(data["tag"]["admin_level"])
                if admin_level >= 0 and admin_level < 15:
                    classs = 100 + admin_level
            except:
                pass

        for nid, cpt in bnds:
            ndata = self.bin.NodeGet(nid)
            if ndata:
                self.error_file.error(classs, None, None, None, None, None, {
                    "position": [ndata],
                    "node": [ndata],
                    "relation": [data]
                })
            else:
                raise SystemError(data)

###########################################################################
## analyse

class Analyser_OsmBin_Open_Relations(Analyser):

    def __init__(self, config, logger = OsmoseLog.logger()):
        Analyser.__init__(self, config, logger)

    def analyser(self):
        bin = OsmBin.OsmBin("/data/work/osmbin/data/")
        out = SaxAnalyse(self.config, bin)
        bin.CopyRelationTo(out)
        del out
        del bin
