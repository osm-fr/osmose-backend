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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from modules.Stablehash import stablehash64

class Highway_Parking_Lane(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)

        self.parkingLaneValues = ["parallel", "diagonal", "perpendicular", "marked", "yes", "no", "separate"]
        self.parkingConditionValues = ["free", "ticket", "disc", "residents", "customers", "private", "disabled", "loading", "no_parking", "no_standing", "no_stopping", "no"] # or custom
        self.parkingConditionReasonValues = ["bus_stop", "crossing", "driveway", "dual_carriage", "fire_lane", "junction", "loading_zone", "narrow", "passenger_loading_zone", "priority_road", "street_cleaning", "turnaround", "turn_lane"] # or custom

        self.errors[31611] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:imagery'],
            title = T_('Bad parking:lane:[side]'),
            detail = T_(
'''The side was not recognized, see
[`parking:lane=*`](https://wiki.openstreetmap.org/wiki/Key:parking:lane).'''),
            fix = T_(
'''Use `left`, `right` or `both`.'''))
        self.errors[31614] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:imagery'],
            title = T_('Too many parking:lane:[side]'),
            detail = T_(
'''There are more types of parking for sides than a street have
sides.'''))
        self.errors[31615] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:chair'],
            title = T_('Bad parking:lane:[side] value'),
            fix = T_('''Use any of the following values: `{0}`.''', "`, `".join(self.parkingLaneValues)),
            resource = "https://wiki.openstreetmap.org/wiki/Key:parking:lane")
        self.errors[31616] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:condition:[side] without parking:lane:[side] value'),
            detail = T_(
'''A parking condition is present but without parking kind.'''))
        self.errors[31617] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:condition:[side] not applicable'),
            detail = T_(
'''A parking condition is set for a parking:lane:[side] value that forbids parking.'''))
        self.errors[31618] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:condition:[side] should be mapped on separately mapped parking area'),
            detail = T_(
'''A parking condition is set for a parking:lane:[side] value that indicates
that the parking area is mapped separately. Any parking conditions should
be tagged on that object instead.'''))
        self.errors[31619] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('Bad parking:condition:[side] value'),
            fix = T_('''Use any of the following values: `{0}`.''', ", ".join(self.parkingConditionValues)),
            resource = "https://wiki.openstreetmap.org/wiki/Key:parking:condition")

    def way(self, data, tags, nds):
        if not "highway" in tags:
            return

        err = []

        if (("parking:condition:right" in tags and not "parking:lane:right" in tags and not "parking:lane:both" in tags) or
            ("parking:condition:left" in tags and not "parking:lane:left" in tags and not "parking:lane:both" in tags) or
            ("parking:condition:both" in tags and not "parking:lane:both" in tags and not ("parking:lane:left" in tags and "parking:lane:right" in tags))):
            err.append({"class": 31616})

        sides = list(map(lambda tag: tag[len("parking:lane:"):].split(":")[0], filter(lambda tag: tag.startswith("parking:lane:"), tags)))
        if len(sides) == 0:
            return err
        sides = [i for i in sides if i not in ("left", "right", "both")]

        if len(sides) > 0:
            err.append({"class": 31611})

        if "parking:lane:both" in tags and (("parking:lane:right" in tags and tags["parking:lane:right"] == tags["parking:lane:both"]) or
                                            ("parking:lane:left" in tags and tags["parking:lane:left"] == tags["parking:lane:both"])):
            # Conflicting values are dealt with in Highway_Sides
            err.append({"class": 31614})

        for side in ("parking:lane:right", "parking:lane:left", "parking:lane:both"):
            if side in tags:
                if tags[side] not in self.parkingLaneValues:
                    # Unknown value of parking:lane:[side]
                    if tags[side] in self.parkingConditionValues:
                        err.append({"class": 31615, "subclass": stablehash64(side), "text": T_("`{0}` is a value for key `{1}`", tags[side], "parking:condition:[side]")})
                    elif tags[side] in self.parkingConditionReasonValues:
                        err.append({"class": 31615, "subclass": stablehash64(side), "text": T_("`{0}` is a value for key `{1}`", tags[side], "parking:condition:[side]:reason")})
                    else:
                        err.append({"class": 31615, "subclass": stablehash64(side)})
                condition = side.replace("lane", "condition")
                if not condition in tags:
                    condition = "parking:condition:both"
                if condition in tags:
                    if tags[side] == "no" and tags[condition][0:2] != "no":
                        # parking:lane:[side] = no together with parking:condition:[side]
                        err.append({"class": 31617, "subclass": stablehash64(side)})
                    elif tags[side] == "separate":
                        # parking:lane:[side] = separate together with parking:condition:[side]
                        err.append({"class": 31618, "subclass": stablehash64(side)})
                    elif tags[condition] in self.parkingLaneValues and tags[condition] not in self.parkingConditionValues:
                        # A value for parking:lane:[side] was used as condition
                        err.append({"class": 31619, "subclass": stablehash64(side), "text": T_("`{0}` is a value for key `{1}`", tags[condition], "parking:lane:[side]")})

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
                  {"highway": "r", "parking:lane:right": "free"},
                  {"highway": "r", "parking:lane:right": "bus_stop"},
                  {"highway": "r", "parking:condition:right": "parallel"},
                  {"highway": "r", "parking:lane:left": "no", "parking:condition:both": "no"},
                  {"highway": "r", "parking:lane:both": "no", "parking:condition:both": "free"},
                  {"highway": "r", "parking:lane:left": "no", "parking:lane:right": "parallel", "parking:condition:both": "free"},
                  {"highway": "r", "parking:lane:both": "separate", "parking:condition:both": "free"},
                  {"highway": "r", "parking:lane:both": "yes", "parking:condition:both": "parallel"},
                 ]:
            self.check_err(a.way(None, t, None), t)
            del t["highway"]
            assert not a.way(None, t, None), t

        for t in [{"highway": "r", "parking:lane:both:parallel": "t"},
                  {"highway": "r", "parking:condition:both": "private", "parking:lane:both": "perpendicular"},
                  {"highway": "r", "parking:lane:right": "parallel", "parking:lane:both": "no"}, # Checked by Highway_Sides plugin
                  {"highway": "r", "parking:condition:right": "private", "parking:condition:left": "private", "parking:lane:both": "perpendicular"},
                  {"highway": "r", "parking:lane:right": "perpendicular", "parking:condition:right": "customers", "parking:condition:right:capacity": "19"},
                  {"highway": "r", "parking:lane:left": "separate", "parking:lane:right": "parallel"},
                  {"highway": "r", "parking:lane:left": "parallel", "parking:lane:right": "separate"},
                  {"highway": "r", "parking:lane:both": "separate"},
                  {"highway": "r", "parking:lane:left": "parallel", "parking:condition:left": "free", "parking:lane:right": "separate"},
                  {"highway": "r", "parking:lane:both": "no", "parking:condition:both": "no_stopping"},
                  {"highway": "r", "parking:condition:both": "private", "parking:lane:left": "parallel", "parking:lane:right": "perpendicular"},
                 ]:
            assert not a.way(None, t, None), t
