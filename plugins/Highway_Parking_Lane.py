#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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

from plugins.Plugin import Plugin
from modules.Stablehash import stablehash

class Highway_Parking_Lane(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.parking_lane = "parking:lane:"
        self.parking_condition = "parking:condition:"
        self.errors[31611] = { "item": 3161, "level": 3, "tag": ["highway", "parking", "fix:imagery"], "desc": T_(u"Bad parking:lane:[side]") }
        self.errors[31614] = { "item": 3161, "level": 3, "tag": ["highway", "parking", "fix:imagery"], "desc": T_(u"Too many parking:lane:[side]") }
        self.errors[31615] = { "item": 3161, "level": 3, "tag": ["highway", "parking", "fix:chair"], "desc": T_(u"Bad parking:lane:[side] value") }
        self.errors[31616] = { "item": 3161, "level": 3, "tag": ["highway", "parking", "fix:survey"], "desc": T_(u"parking:condition:[side] without parking:lane:[side] value") }

    def way(self, data, tags, nds):
        if not "highway" in tags:
            return

        err = []

        sides = list(map(lambda tag: tag[len(self.parking_lane):].split(":")[0], filter(lambda tag: tag.startswith(self.parking_lane), tags)))
        n_sides = len(sides)
        sides = [i for i in sides if i not in ("left", "right", "both")]

        conditions = map(lambda tag: ":".join(tag.split(":")[0:3]).replace(":condition:", ":lane:"), filter(lambda tag: tag.startswith(self.parking_condition), tags))
        for c in conditions:
            if c not in tags:
                err.append({"class": 31616})
                break

        if n_sides == 0:
            return err

        if len(sides) > 0:
            err.append({"class": 31611})

        if ("parking:lane:right" in tags or "parking:lane:left" in tags) and "parking:lane:both" in tags:
            err.append({"class": 31614})

        for side in ("parking:lane:right", "parking:lane:left", "parking:lane:both"):
            if side in tags and tags[side] not in ("parallel", "diagonal", "perpendicular", "marked", "no_parking", "no_stopping", "fire_lane"):
                err.append({"class": 31615, "subclass": stablehash(side)})

        return err


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Highway_Parking_Lane(None)
        a.init(None)

        for t in [{"highway": "r", "parking:lane:side": "t"},
                  {"highway": "r", "parking:lane:right": "parallel", "parking:lane:both": "parallel"},
                  {"highway": "r", "parking:lane:right": "p"},
                  {"highway": "r", "parking:condition:right": "parallel"},
                 ]:
            self.check_err(a.way(None, t, None), t)
            del t["highway"]
            assert not a.way(None, t, None), t

        for t in [{"highway": "r", "parking:lane:both:parallel": "t"},
                  {"highway": "r", "parking:condition:both": "private", "parking:lane:both": "perpendicular"},
                  {"highway": "r", "parking:lane:right": "perpendicular", "parking:condition:right": "customers", "parking:condition:right:capacity": "19"},
                 ]:
            assert not a.way(None, t, None), t
