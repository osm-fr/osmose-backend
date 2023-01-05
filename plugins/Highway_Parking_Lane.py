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

        # Tagging scheme until Dec 8, 2022 (still very common)
        self.parkingLaneValues = ["parallel", "diagonal", "perpendicular", "marked", "yes", "no", "separate"]
        self.parkingConditionValues = ["free", "ticket", "disc", "residents", "customers", "private", "disabled", "loading", "no_parking", "no_standing", "no_stopping", "no"] # or custom
        self.parkingConditionReasonValues = ["bus_stop", "crossing", "driveway", "dual_carriage", "fire_lane", "junction", "loading_zone", "narrow", "passenger_loading_zone", "priority_road", "street_cleaning", "turnaround", "turn_lane"] # or custom

        self.errors[31611] = self.def_class(item = 3161, level = 2, tags = ['highway', 'parking', 'fix:imagery'],
            title = T_('Bad parking:lane:[side]'),
            detail = T_(
'''The side was not recognized, see
[`parking:lane=*`](https://wiki.openstreetmap.org/wiki/Key:parking:lane).'''),
            fix = T_(
'''Consider switching to the new [street parking tagging scheme]("https://wiki.openstreetmap.org/wiki/Street_parking).'''))
        self.errors[31614] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:imagery'],
            title = T_('Too many parking:lane:[side]'),
            detail = T_(
'''The key `parking:lane:both` was used together with `parking:lane:left` and/or `parking:lane:right`.
However, `both` already covers both sides of a street, so the latter are redundant.'''),
            fix = T_(
'''Consider switching to the new [street parking tagging scheme]("https://wiki.openstreetmap.org/wiki/Street_parking).'''))
        self.errors[31615] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:chair'],
            title = T_('Bad parking:lane:[side] value'),
            fix = T_(
'''Consider switching to the new [street parking tagging scheme]("https://wiki.openstreetmap.org/wiki/Street_parking).'''),
            resource = "https://wiki.openstreetmap.org/wiki/Key:parking:lane")
        self.errors[31616] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:condition:[side] without parking:lane:[side] value'),
            detail = T_(
'''A parking condition is present but without parking kind.'''),
            fix = T_(
'''Consider switching to the new [street parking tagging scheme]("https://wiki.openstreetmap.org/wiki/Street_parking).'''))
        self.errors[31617] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:condition:[side] not applicable'),
            detail = T_(
'''A parking condition is set for a parking:lane:[side] value that forbids parking.'''),
            fix = T_(
'''Consider switching to the new [street parking tagging scheme]("https://wiki.openstreetmap.org/wiki/Street_parking).'''))
        self.errors[31618] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:condition:[side] should be mapped on separately mapped parking area'),
            detail = T_(
'''A parking condition is set for a parking:lane:[side] value that indicates
that the parking area is mapped separately. Any parking conditions should
be tagged on that object instead.'''),
            fix = T_(
'''Consider switching to the new [street parking tagging scheme]("https://wiki.openstreetmap.org/wiki/Street_parking).'''))
        self.errors[31619] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('Bad parking:condition:[side] value'),
            fix = T_(
'''Consider switching to the new [street parking tagging scheme]("https://wiki.openstreetmap.org/wiki/Street_parking).'''),
            resource = "https://wiki.openstreetmap.org/wiki/Key:parking:condition")


        # Tagging scheme as of Dec 8, 2022
        self.parkingValues = ["lane", "street_side", "on_kerb", "half_on_kerb", "shoulder", "no", "separate", "yes"]
        self.orientationValues = ["parallel", "diagonal", "perpendicular"]
        self.directionValues = ["back_in", "head_in"]
        self.restrictionValues = ["no_parking", "no_standing", "no_stopping", "loading_only", "charging_only"]
        self.reasonValues = ["bus_lane", "rails", "bus_stop", "crossing", "cycleway", "driveway", "dual_carriage",
                             "fire_lane", "junction", "loading_zone", "markings", "narrow",
                             "passenger_loading_zone", "priority_road", "street_cleaning", "turnaround", "turn_lane"]
        self.errors[31621] = self.def_class(item = 3161, level = 2, tags = ['highway', 'parking', 'fix:imagery'],
            title = T_('Bad parking:[side]'),
            detail = T_(
'''The side was not recognized, expected was either `left`, `right` or `both`.'''),
            fix = T_(
'''Use `parking:left`, `parking:right` or `parking:both`.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Street_parking",
            example = T_(
'''To specify that you can only park for 2 hours in the street, you should use
`parking:both:maxstay=2 hours`, and not `parking:maxstay=2 hours`.'''))
        self.errors[31622] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:[side]:* without parking:[side] value'),
            detail = T_(
'''A parking tag adding details, such as `parking:[side]:fee`, is present without primary `parking:[side]` key.'''))
        self.errors[31623] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:imagery'],
            title = T_('Duplicated values'),
            detail = T_(
'''The key `parking:both` (possibly with a suffix, such as `:maxstay`) was used together with `parking:left`
and/or `parking:right` (with the same suffix).
However, `parking:both` already covers both sides of a street, so the latter are redundant.'''))
        self.errors[31624] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:chair'],
            title = T_('Bad value for parking:[side]=*'),
            fix = T_('''Use any of the following values: `{0}`.''', "`, `".join(self.parkingValues)),
            resource = "https://wiki.openstreetmap.org/wiki/Street_parking")
        self.errors[31625] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('parking:[side]:* not applicable'),
            detail = T_(
'''A parking key is set for a `parking:[side]` value that forbids parking.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Street_parking")
        self.errors[31626] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('Property of parking should be mapped on separately mapped parking area'),
            detail = T_(
'''A parking property is set for a `parking:[side]` value that indicates that the parking area is mapped separately.
Any parking details should be tagged on that object instead.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Street_parking")
        self.errors[31627] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('Bad parking:[side]:{0} value', 'orientation'),
            fix = T_('''Use any of the following values: `{0}`.''', ", ".join(self.orientationValues)),
            resource = "https://wiki.openstreetmap.org/wiki/Street_parking")
        self.errors[31628] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('Bad parking:[side]:{0} value', 'restriction'),
            fix = T_('''Use any of the following values: `{0}`.''', ", ".join(self.restrictionValues)),
            resource = "https://wiki.openstreetmap.org/wiki/Street_parking")
        self.errors[31629] = self.def_class(item = 3161, level = 3, tags = ['highway', 'parking', 'fix:survey'],
            title = T_('Bad parking:[side]:{0} value', 'direction'),
            fix = T_('''Use any of the following values: `{0}`.''', ", ".join(self.directionValues)),
            resource = "https://wiki.openstreetmap.org/wiki/Street_parking")

    def way(self, data, tags, nds):
        if not "highway" in tags:
            return

        err = []

        parking_keys = list(filter(lambda tag: tag.startswith("parking:"), tags))
        if len(parking_keys) == 0:
            return err

        sides = list(map(lambda tag: tag[len("parking:"):].split(":")[0], parking_keys))
        if ("condition" in sides or "lane" in sides) and not ("right" in sides or "left" in sides or "both" in sides):
            # Deprecated scheme (as of Dec 8, 2022) but currently (Dec 2022) still more common
            # Warned for by TagFix_Deprecated

            if (("parking:condition:right" in tags and tags["parking:condition:right"][0:2] != "no" and not "parking:lane:right" in tags and not "parking:lane:both" in tags) or
                ("parking:condition:left" in tags and tags["parking:condition:left"][0:2] != "no" and not "parking:lane:left" in tags and not "parking:lane:both" in tags) or
                ("parking:condition:both" in tags and tags["parking:condition:both"][0:2] != "no" and not "parking:lane:both" in tags and not ("parking:lane:left" in tags and "parking:lane:right" in tags))):
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

        # ------------------------------------------
        # New parking:* scheme, approved Dec 8, 2022

        # Unknown [side] of parking:[side]
        # Allows 'condition' and 'lane' to avoid duplicate warnings with TagFix_Deprecated
        sides = [i for i in sides if i not in ("left", "right", "both", "condition", "lane")]
        for side in sides:
            err.append({"class": 31621, "subclass": stablehash64(side), "text": {"en": "parking:" + side}})

        # Parking:[side]:*=* without parking:[side]=* or parking:[side]:restriction=no_*
        if ((not "parking:both" in parking_keys and not "parking:left" in parking_keys and any(map(lambda key: key.startswith("parking:left:") and (not key.startswith("parking:left:restriction") or (key == "parking:left:restriction" and tags[key][0:3] != 'no_')), parking_keys))) or
           (not "parking:both" in parking_keys and not "parking:right" in parking_keys and any(map(lambda key: key.startswith("parking:right:") and (not key.startswith("parking:right:restriction") or (key == "parking:right:restriction" and tags[key][0:3] != 'no_')), parking_keys))) or
           (not "parking:both" in parking_keys and not ("parking:right" in parking_keys and "parking:left" in parking_keys) and any(map(lambda key: key.startswith("parking:both:") and (not key.startswith("parking:both:restriction") or (key == "parking:both:restriction" and tags[key][0:3] != 'no_')), parking_keys)))):
           err.append({"class": 31622})

        # parking:left/right(:*) together with parking:both(:*) and equal values
        for leftrightkey in filter(lambda key: key.startswith("parking:left") or key.startswith("parking:right"), parking_keys):
            bothkey = leftrightkey.replace(":left", ":both", 1).replace(":right", ":both", 1)
            if bothkey in parking_keys and tags[bothkey] == tags[leftrightkey]:
                # Note: conflicting values are dealt with in Highway_Sides
                err.append({
                    "class": 31623,
                    "text": {"en": "{0} = {1}".format(bothkey, leftrightkey)},
                    "fix": {"-": [leftrightkey]}
                })

        for side in ("parking:right", "parking:left", "parking:both"):
            if side in parking_keys and tags[side] not in self.parkingValues:
                # Bad value for the primary key
                if tags[side] in self.orientationValues:
                    err.append({"class": 31624, "subclass": stablehash64(side), "text": T_("`{0}` is a value for key `{1}`", tags[side], "parking:[side]:orientation")})
                elif tags[side] in self.directionValues:
                    err.append({"class": 31624, "subclass": stablehash64(side), "text": T_("`{0}` is a value for key `{1}`", tags[side], "parking:[side]:direction")})
                elif tags[side] in self.restrictionValues:
                    err.append({"class": 31624, "subclass": stablehash64(side), "text": T_("`{0}` is a value for key `{1}`", tags[side], "parking:[side]:restriction")})
                elif tags[side] in self.reasonValues:
                    err.append({"class": 31624, "subclass": stablehash64(side), "text": T_("`{0}` is a value for key `{1}`", tags[side], "parking:[side]:reason / parking:[side]:restriction:reason")})
                else:
                    err.append({"class": 31624, "subclass": stablehash64(side)})
            elif side in parking_keys and tags[side] in ("no", "separate"):
                # Bad combinations of tags together with 'no' or 'separate'
                for s in {side, side.replace("left", "both", 1).replace("right", "both", 1)}:
                    for k in parking_keys:
                        if ((k == s + ":restriction" and (tags[k][0:3] != "no_" or tags[side] == 'separate')) or
                          (k.startswith(s + ":") and k != s + ":restriction" and ((not ":reason" in k and tags[k] != 'no') or tags[side] == 'separate'))):
                            err.append({
                                "class": 31625 if tags[side] == 'no' else 31626,
                                "subclass": stablehash64(s + k),
                                "text": {"en": "{0}={1} + {2}".format(side, tags[side], k)}
                            })
            # Mixup of other 'subkeys' of parking:side
            elif (side + ":orientation" in parking_keys and tags[side + ":orientation"] not in self.orientationValues and
              (tags[side + ":orientation"] in self.directionValues or tags[side + ":orientation"] in self.restrictionValues
              or tags[side + ":orientation"] in self.reasonValues or tags[side + ":orientation"] in self.parkingValues)):
                err.append({"class": 31627, "subclass": stablehash64(side), "text": {"en": "{0}={1}".format(side + ":orientation", tags[side + ":orientation"])}})
            elif (side + ":restriction" in parking_keys and tags[side + ":restriction"] not in self.restrictionValues and
              (tags[side + ":restriction"] in self.directionValues or tags[side + ":restriction"] in self.orientationValues
              or tags[side + ":restriction"] in self.reasonValues or tags[side + ":restriction"] in self.parkingValues)):
                err.append({"class": 31628, "subclass": stablehash64(side), "text": {"en": "{0}={1}".format(side + ":restriction", tags[side + ":restriction"])}})
            elif (side + ":direction" in parking_keys and tags[side + ":direction"] not in self.directionValues and
              (tags[side + ":direction"] in self.restrictionValues or tags[side + ":direction"] in self.orientationValues
              or tags[side + ":direction"] in self.reasonValues or tags[side + ":direction"] in self.parkingValues)):
                err.append({"class": 31629, "subclass": stablehash64(side), "text": {"en": "{0}={1}".format(side + ":direction", tags[side + ":direction"])}})

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
                  {"highway": "r", "parking:lane:left": "perpendicular", "parking:condition:both": "free"},
                  {"highway": "r", "parking:lane:both": "no", "parking:condition:both": "free"},
                  {"highway": "r", "parking:lane:left": "no", "parking:lane:right": "parallel", "parking:condition:both": "free"},
                  {"highway": "r", "parking:lane:both": "separate", "parking:condition:both": "free"},
                  {"highway": "r", "parking:lane:both": "yes", "parking:condition:both": "parallel"},

                  {"highway": "road", "parking:side": "street_side"},
                  {"highway": "road", "parking:right": "street_side", "parking:both": "street_side"},
                  {"highway": "road", "parking:both": "street_side", "parking:both:maxstay": "14 days", "parking:right:maxstay": "14 days"},
                  {"highway": "road", "parking:both": "street_side", "parking:both:capacity": "14", "parking:left:capacity": "14"},
                  {"highway": "road", "parking:both": "custom_value"},
                  {"highway": "road", "parking:both": "loading_only"},
                  {"highway": "road", "parking:both": "perpendicular"},
                  {"highway": "road", "parking:both": "back_in"},
                  {"highway": "road", "parking:both": "street_side", "parking:both:restriction": "street_side"},
                  {"highway": "road", "parking:both": "yes", "parking:both:restriction": "fire_lane"},
                  {"highway": "road", "parking:both": "yes", "parking:both:orientation": "back_in"},
                  {"highway": "road", "parking:both": "yes", "parking:both:direction": "diagonal"},
                  {"highway": "road", "parking:left": "half_on_kerb", "parking:both:orientation": "parallel"},
                  {"highway": "road", "parking:right": "half_on_kerb", "parking:both:direction": "back_in"},
                  {"highway": "road", "parking:both": "no", "parking:both:direction": "back_in"},
                  {"highway": "road", "parking:both": "no", "parking:both:restriction": "loading_only"},
                  {"highway": "road", "parking:left": "no", "parking:right": "lane", "parking:both:restriction": "loading_only"},
                  {"highway": "road", "parking:both": "separate", "parking:both:fee": "yes"},
                  {"highway": "road", "parking:both": "no", "parking:both:restriction": "loading_only"},
                  {"highway": "road", "parking:both": "separate", "parking:both:restriction": "no_parking"},
                  {"highway": "road", "parking:right": "separate", "parking:left": "lane", "parking:both:fee": "yes"},
                  {"highway": "road", "parking:right": "separate", "parking:right:reason": "fire_lane"},
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
                  {"highway": "r", "parking:condition:both": "no_parking"},

                  {"highway": "road", "parking:right": "street_side", "parking:lane:left": "parallel"}, # Checked for by TagFix_Deprecated
                  {"highway": "road", "parking:right": "street_side"},
                  {"highway": "road", "parking:right": "street_side", "parking:right:access": "private", "parking:right:fee": "no", "parking:right:capacity": "14", "parking:right:maxstay": "1 hour"},
                  {"highway": "road", "parking:right": "street_side", "parking:right:orientation": "parallel", "parking:right:direction": "back_in"},
                  {"highway": "road", "parking:right": "no"},
                  {"highway": "road", "parking:right": "no", "parking:right:reason": "fire_lane"},
                  {"highway": "road", "parking:both": "no", "parking:right:reason": "fire_lane", "parking:left:reason": "custom_value"},
                  {"highway": "road", "parking:right": "no", "parking:right:reason": "fire_lane", "parking:right:restriction": "no_stopping"},
                  {"highway": "road", "parking:right": "no", "parking:right:restriction:reason": "fire_lane", "parking:right:restriction": "no_stopping"},
                  {"highway": "road", "parking:right:restriction": "no_stopping"},
                  {"highway": "road", "parking:right:restriction": "no_parking", "parking:right:restriction:reason": "fire_lane"},
                  {"highway": "road", "parking:right:restriction": "no_parking", "parking:right:access": "no", "parking:right": "no"},
                  {"highway": "road", "parking:right": "separate"},
                  {"highway": "road", "parking:right": "street_side", "parking:both": "no"}, # Checked by Highway_Sides plugin
                  {"highway": "road", "parking:right:access": "private", "parking:left:access": "private", "parking:both": "on_kerb"},
                  {"highway": "road", "parking:both:access": "private", "parking:left": "half_on_kerb", "parking:right": "on_kerb"},
                  {"highway": "road", "parking:left": "half_on_kerb", "parking:right": "no"},
                  {"highway": "road", "parking:left": "separate", "parking:right": "half_on_kerb", "parking:right:orientation": "parallel"},
                 ]:
            assert not a.way(None, t, None), t
