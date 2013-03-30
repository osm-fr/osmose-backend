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

from analyser_sax import Analyser_Sax

from modules import OsmoseLog

###########################################################################

class DataHandler:
    def __init__(self):
        self.ways = {}
        self.rels = {}

    def WayCreate(self, data):
        if data[u"tag"].get(u"boundary", None) <> u"administrative":
            return
        if not "admin_level" in data[u"tag"]:
            return
        self.ways[data["id"]] = data[u"tag"]["admin_level"]

    def RelationCreate(self, data):
        if data[u"tag"].get(u"boundary", None) <> u"administrative":
            return
        if not "admin_level" in data[u"tag"]:
            return
        self.rels[data["id"]] = data[u"tag"]["admin_level"]

###########################################################################

class Analyser_Admin_Level(Analyser_Sax):

    def __init__(self, config, logger = OsmoseLog.logger()):
        Analyser_Sax.__init__(self, config, logger)

    ################################################################################

    def _load_plugins(self):
        self._Err = {}
        self._Err[1] = { "item": 6050,
                         "level": 3,
                         "desc": { "en": u"Wrong administrative level",
                                   "fr": u"Mauvais niveau administratif"}
                       }
        self._Err[2] = { "item": 6050,
                         "level": 3,
                         "desc": { "en": u"admin_level unreadable",
                                   "fr": u"admin_level illisible"}
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
                self.error_file.error(2, None, {"fr": u"admin_level illisible", "en": u"admin_level unreadable"}, None, None, None, {
                    "position": [nta],
                    "relation": [rta]
                })
                continue

            for m in rta[u"member"]:
                if m[u"type"] == u"way":
                    if m[u"ref"] in way_to_level:
                        way_to_level[m[u"ref"]] = min(way_to_level[m[u"ref"]], level)
                if m[u"type"] == u"relation":
                    if m[u"ref"] in rel_to_level:
                        rel_to_level[m[u"ref"]] = min(rel_to_level[m[u"ref"]], level)

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

                self.error_file.error(2, None, {"fr": u"admin_level illisible", "en": u"admin_level unreadable"}, None, None, None, {
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

                self.error_file.error(1, None, {"fr": u"admin_level devrait être %d"%way_to_level[wid], "en": u"admin_level should be %d"%way_to_level[wid]}, None, None, None, {
                    "position": [n],
                    "way": [wta]
                })
                continue

    ################################################################################

    def _close_plugins(self):
        pass
 
    ################################################################################
