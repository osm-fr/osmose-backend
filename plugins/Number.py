#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
import re

class Number(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3091] = self.def_class(item = 3091, level = 2, tags = ['value', 'fix:chair'],
            title = T_('Invalid numerical value'),
            detail = T_(
'''The tag expects a numeric value with decimals using a period character
and not a comma. \\ For guidelines on numeric values with units see [the
wiki](https://wiki.openstreetmap.org/wiki/Map_Features/Units).'''),
            fix = T_(
'''Make sure the relevant tag value is numeric and in the expected format
(with valid units if required).''')
        )
        self.errors[3092] = self.def_class(item = 3091, level = 2, tags = ['value', 'fix:chair'],
            title = T_('Suspicious numerical value'),
            detail = T_(
'''The feature is tagged with an uncommonly high or low numeric value for
the specified tag.'''),
            fix = T_(
'''Check that the value is accurate. Consider whether another tag should
be used if the value is valid.''')
        )
        self.errors[3093] = self.def_class(item = 3091, level = 2, tags = ['value', 'fix:chair'],
            title = T_('Suspicious value'),
            detail = T_(
'''The tag expects a positive, round number without unit.'''),
            fix = T_(
'''Check that the value is accurate. Consider whether another tag should
be used if the value is valid.''')
        )
        self.errors[3094] = self.def_class(item = 3091, level = 2, tags = ['value', 'fix:chair'],
            title = T_('Unknown unit'),
            detail = T_(
'''The tag uses an unexpected unit.'''),
            fix = T_(
'''Check that you have used the correct unit and a supported abbreviation of the unit.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Map_features/Units"
        )

        self.tag_number = ["diameter", "distance", "ele", "height", "length", "width", "diameter_crown", "circumference", "depth"]
        self.tag_number_integer = ["admin_level", "capital", "heritage", "population", "step_count"] # Only positive integers (no units) allowed
        tag_number_directional = ["maxaxleload", "maxheight", "maxheight:physical", "maxlength", "maxspeed", "maxspeed:advisory", "maxweight", "maxwidth", "minspeed"]

        # Add suffixes to the directional tags, add everything to tag_number
        for i in ["", ":forward", ":backward"]:
            self.tag_number.extend(list(map(lambda tag: tag + i, tag_number_directional)))
        self.tag_number.extend(self.tag_number_integer)

        self.units = ["m", "cm", "mm", "km", "mi", "nmi", # distance excluding feet'inch"
                      "km/h", "mph", "knots", # speed
                      "t", "kg", "st", "lbs", "lt", "cwt"] # weight

        self.Number = re.compile(u"^((?:-?[0-9]+(?:[.][0-9]+)?)|(?:[.][0-9]+))(?: ?([a-zA-Z23/]{1,5})|'(?:[0-9]*(?:[.][0-9]+)?\")?|\")?$")
        self.MaxspeedExtraValue = ["none", "default", "signals", "national", "no", "unposted", "walk", "urban", "variable"]
        self.MaxspeedClassValue = re.compile(u'^[A-Z]*:')
        self.MaxheightExtraValue = ["default", "below_default", "no_indications", "no_sign", "none", "unsigned"]

    def node(self, data, tags):
        for i in self.tag_number:
            if i in tags:
                m = self.Number.match(tags[i])
                if (not m and
                    not (i == "width" and tags[i] == "narrow") and
                    not (i == "capital" and tags[i] == "yes") and
                    not (i == "heritage" and tags[i] == "yes") and
                    not (("maxspeed" in i or "minspeed" in i) and (
                        tags[i] in self.MaxspeedExtraValue or
                        self.MaxspeedClassValue.match(tags[i]) or
                        (tags[i] == "implicit" and ("traffic_sign" in tags) and "maxspeed" in tags["traffic_sign"].split(";"))
                    )) and
                    not (i == "maxheight" and tags[i] in self.MaxheightExtraValue)
                ):
                    return {"class": 3091, "subclass": 1, "text": T_("Concerns tag: `{0}`", '='.join([i, tags[i]])) }
                if not m:
                    continue

                # Below here only tags containing numbers with/without unit remain
                if i in self.tag_number_integer and str(int(abs(float(m.group(1))))) != tags[i]:
                    # Expected: positive integer, found: decimal number or number with unit
                    return {"class": 3093, "subclass": 4, "text": T_("Concerns tag: `{0}`", '='.join([i, tags[i]])) }
                elif m.group(2) and not m.group(2) in self.units:
                    return {"class": 3094, "subclass": 6, "text": T_("Concerns tag: `{0}`", '='.join([i, tags[i]])) }
                elif i == "height" and float(m.group(1)) > 500:
                    return {"class": 3092, "subclass": 2, "text": T_("`height={0}` is really tall, consider changing to `ele=*`", m.group(1)),
                             "fix": {"-": ["height"], "+": {"ele": tags["height"]}} }
                elif "maxspeed" in i and float(m.group(1)) < 5 and not "waterway" in tags:
                    return {"class": 3092, "subclass": 3, "text": T_('`{0}` is really slow', 'maxspeed=' + m.group(1))}
                elif i == "width" and float(m.group(1)) <= 0 and "highway" in tags: # seems to be an old iD bug
                    return {"class": 3092, "subclass": 5, "text": T_("Concerns tag: `{0}`", '='.join([i, tags[i]]))}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Number(None)
        a.init(None)
        for d in ["194", "14 m", "0.6m", "1cm", "narrow", "8 km", "400m", "10'", "10'11\"", "1'9.8\"", "1.18\"", "-6"]:
            assert not a.node(None, {"width":d}), ("width='{0}'".format(d))

        for d in ["3,75", "foo", "18,4m", "4.8 cars", "4810"]:
            self.check_err(a.node(None, {"height":d}), ("height='{0}'".format(d)))
            self.check_err(a.way(None, {"height":d}, None), ("height='{0}'".format(d)))
            self.check_err(a.relation(None, {"height":d}, None), ("height='{0}'".format(d)))

        for d in ["foo", "18kph", "1", "30 c"]:
            self.check_err(a.node(None, {"maxspeed":d}), ("maxspeed='{0}'".format(d)))
            self.check_err(a.node(None, {"maxspeed:backward":d}), ("maxspeed:backward='{0}'".format(d)))

        for d in ["50", "FR:urban", "35 mph", "10 knots", "default"]:
            assert not a.node(None, {"maxspeed":d}), ("maxspeed='{0}'".format(d))
            assert not a.node(None, {"minspeed:forward":d}), ("minspeed:forward='{0}'".format(d))

        t = {"maxspeed":"1", "waterway": "river"}
        assert not a.node(None, {"maxspeed":"1", "waterway": "river"}), t

        assert not a.node(None, {"maxspeed": "implicit", "traffic_sign": "maxspeed"})

        assert not a.node(None, {"maxheight": "default"})

        assert not a.node(None, {"capital":"yes"})
        assert not a.node(None, {"capital":"2"})

        assert not a.node(None, {"width": "4.5", "highway": "residential"})
        assert a.node(None, {"width": "0", "highway": "residential"})

        assert not a.node(None, {"population":"5000"})
        for d in ["-50", "many", "20 km", "4.5", "4.0"]:
            assert a.node(None, {"population": d})
