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

import datetime

from Analyser import Analyser

from modules import OsmBin

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

class Analyser_OsmBin_Open_Relations(Analyser):

    def analyser(self, osmbin_path="/data/work/osmbin/data/"):
        timestamp = datetime.datetime.now()
        self.error_file.analysers(timestamp)
        self.error_file.analyser(timestamp)
        self.error_file.classs(1, 6010, 3, ["geom","boundary"], {"fr": u"Relation type=boundary ouverte", "en": u"Open relation type=boundary", "es": u"Relación abierta type=boundary"})
        self.error_file.classs(2, 6010, 3, ["geom"], {"fr": u"Relation type=multipolygon ouverte", "en": u"Open relation type=multipolygon", "es": u"Relación abierta type=multipolygon"})
        for admin_level in xrange(0, 15):
            if admin_level <= 6:
                level= 1
            elif admin_level <= 8:
                level = 2
            else:
                level = 3
            self.error_file.classs(100 + admin_level, 6010, level, ["geom","boundary"], {"fr": u"Relation ouverte type=boundary admin_level=%d" % admin_level, "en": u"Open relation type=boundary admin_level=%d" % admin_level})

        self.classs = {"boundary": 1, "multipolygon": 2}

        self.bin = OsmBin.OsmBin(osmbin_path)
        self.bin.CopyRelationTo(self)
        del self.bin

        self.error_file.analyser_end()
        self.error_file.analysers_end()


    def RelationCreate(self, data):

        if data[u"tag"].get(u"type", None) != u"boundary" and data[u"tag"].get(u"type", None) != u"multipolygon":
            return

        try:
            ways = get_ways(data["id"], self.bin)
        except OsmBin.MissingDataError as e:
            print(e, "on relation", data["id"])
            return
        except OsmBin.RelationLoopError as e:
            print(e, "on relation", data["id"])
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
                if ndata["lat"] > 90 or ndata["lat"] < -90:
                    print("Incorrect node found on relation", data["id"])
                    print(ndata)
                    continue

                self.error_file.error(classs, None, None, None, None, None, {
                    "position": [ndata],
                    "node": [ndata],
                    "relation": [data]
                })
            else:
                raise SystemError(data)

###########################################################################
from Analyser import TestAnalyser

class Test(TestAnalyser):
    def setUp(self):
        import shutil
        shutil.rmtree("tmp-osmbin/", True)
        OsmBin.InitFolder("tmp-osmbin/")
        self.o = OsmBin.OsmBin("tmp-osmbin/", "w")
        self.o.Import("tests/osmbin_open_relations.osm")
        del self.o
        self.xml_res_file = "tests/out/osmbin_open_relations.test.xml"
        (self.conf, self.analyser_config) = self.init_config(dst=self.xml_res_file)

    def test(self):
        with Analyser_OsmBin_Open_Relations(self.analyser_config, self.logger) as a:
            a.analyser("tmp-osmbin/")

        self.root_err = self.load_errors()
        self.check_err(cl="108", lat="33.9062245", lon="-117.9765383", elems=[("relation", "2312655"), ("node", "2681302646")])
        self.check_err(cl="108", lat="33.895318",  lon="-117.985422",  elems=[("relation", "2312655"), ("node", "373549994")])
        self.check_num_err(2)
