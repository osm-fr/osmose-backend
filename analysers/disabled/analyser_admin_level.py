#! /usr/bin/env python
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

from analyser_sax import Analyser_Sax

from modules import OsmoseLog

###########################################################################

class DataHandler:
    def __init__(self):
        self.ways = {}
        self.rels = {}

    def WayCreate(self, data):
        if data["tag"].get("boundary", None) != "administrative":
            return
        if not "admin_level" in data["tag"]:
            return
        self.ways[data["id"]] = data["tag"]["admin_level"]

    def RelationCreate(self, data):
        if data["tag"].get("boundary", None) != "administrative":
            return
        if not "admin_level" in data["tag"]:
            return
        self.rels[data["id"]] = data["tag"]["admin_level"]

###########################################################################

class Analyser_Admin_Level(Analyser_Sax):

    def __init__(self, config, logger = OsmoseLog.logger()):
        Analyser_Sax.__init__(self, config, logger)

    ################################################################################

    def _load_plugins(self):
        self._Err = {}
        self._Err[1] = { "item": 6050,
                         "level": 3,
                         "desc": { "en": "Wrong administrative level", "fr": "Mauvais niveau administratif", "es": "Nivel administrativo incorrecto"},
                         "tag": ["boundary", "fix:chair"]
                       }
        self._Err[2] = { "item": 6050,
                         "level": 3,
                         "desc": { "en": "admin_level unreadable", "fr": "admin_level illisible", "es": "admin_level ilegible"},
                         "tag": ["boundary", "value", "fix:chair"]
                       }

    ################################################################################

    def _run_analyse(self):

        o = DataHandler()

        ## get relations
        self.logger.log("get ways data")
        self.parser.CopyWayTo(o)
        wdta = o.ways

        ## get ways id
        self.logger.log("get relations data")
        self.parser.CopyRelationTo(o)
        rdta = o.rels

        del o

        ## find admin level
        way_to_level = {}
        rel_to_level = {}
        for wid in wdta:
            way_to_level[wid] = 99
        for rid in rdta:
            rel_to_level[rid] = 99

        self.logger.log("check admin level - relations")
        for rid in rdta:

            rta = self.RelationGet(rid)
            if not rta:
                continue

            try:
                level = int(rdta[rid])
            except:
                # find node in relation
                wid = [x["ref"] for x in rta["member"] if x["type"]=="way"]
                if not wid:
                    continue
                wid = wid[0]
                wta = self.WayGet(wid)
                if not wta["nd"]:
                    continue
                nid = wta["nd"][0]
                nta = self.NodeGet(nid)
                if not nta:
                    continue
                # add error to output file
                self.error_file.error(2, None, {"fr": "admin_level illisible", "en": "admin_level unreadable", "es": "admin_level ilegible"}, None, None, None, {
                    "position": [nta],
                    "relation": [rta]
                })
                continue

            for m in rta["member"]:
                if m["type"] == "way":
                    if m["ref"] in way_to_level:
                        way_to_level[m["ref"]] = min(way_to_level[m["ref"]], level)
                if m["type"] == "relation":
                    if m["ref"] in rel_to_level:
                        rel_to_level[m["ref"]] = min(rel_to_level[m["ref"]], level)

        ##
        self.logger.log("check admin level - ways")
        for wid in wdta:

            try:
                level = int(wdta[wid])
            except:
                wta = self.WayGet(wid)
                if not wta:
                    continue

                wta["tag"]["admin_level"] = wdta[wid]
                n = self.NodeGet(wta["nd"][0])
                if not n:
                    continue

                self.error_file.error(2, None, {"fr": "admin_level illisible", "en": "admin_level unreadable", "es": "admin_level ilegible"}, None, None, None, {
                    "position": [n],
                    "way": [wta]
                })
                continue

            if way_to_level[wid] not in [99, level]:
                wta = self.WayGet(wid)
                if not wta:
                    continue

                wta["tag"]["admin_level"] = wdta[wid]
                n = self.NodeGet(wta["nd"][0])
                if not n:
                    continue

                self.error_file.error(1, None, {"fr": "admin_level devrait être %d"%way_to_level[wid], "en": "admin_level should be %d"%way_to_level[wid], "es": "admin_level debería ser %d" %way_to_level[wid]}, None, None, None, {
                    "position": [n],
                    "way": [wta]
                })
                continue

    ################################################################################

    def _close_plugins(self):
        pass

    ################################################################################
