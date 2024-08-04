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
from plugins.modules.units import parseNumberUnitString, convertToUnit
import re

class Number(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3091] = self.def_class(item = 3091, level = 2, tags = ['value', 'fix:chair'],
            title = T_('Invalid numerical value'),
            detail = T_(
'''The tag expects a numeric value with decimals using a period character
and not a comma. For guidelines on numeric values with units see [the
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
        self.errors[30915] = self.def_class(item = 3091, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Discouraged unit alias'),
            detail = T_(
'''The tag uses an unexpected unit.'''),
            fix = T_(
'''Check that you have used the correct unit and a supported abbreviation of the unit.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Map_features/Units"
        )

        # Syntax ("tag", "default unit"), except for integer tags (those are converted automatically)
        self.tag_number = [("diameter", 'mm'), ("distance", 'km'), ("ele", 'm'), ("height", 'm'), ("length", 'm'), ("width", 'm'), ("diameter_crown", 'm'), ("circumference", 'm'), ("depth", 'm')]
        self.tag_number_integer = ["admin_level", "capital", "heritage", "population", "step_count"] # Only positive integers (no units) allowed
        tag_number_directional = [("maxaxleload", 't'), ("maxheight", 'm'), ("maxheight:physical", 'm'), ("maxlength", 'm'), ("maxspeed", 'km/h'), ("maxspeed:advisory", 'km/h'), ("maxweight", 't'), ("maxwidth", 'm'), ("minspeed", 'km/h')]

        # Add suffixes to the directional tags, add everything to tag_number
        for i in ["", ":forward", ":backward"]:
            self.tag_number.extend(list(map(lambda t: (t[0] + i, t[1]), tag_number_directional)))
        self.tag_number.extend(list(map(lambda t: (t, None), self.tag_number_integer)))

        self.units = [# length units via convertToUnit, the others are yet to be implemented there
                      "km/h", "mph", "knots", # speed
                      "t", "kg", "st", "lbs", "lt", "cwt"] # weight

        self.MaxspeedExtraValue = ["none", "default", "signals", "national", "no", "unposted", "walk", "urban", "variable"]
        self.MaxspeedClassValue = re.compile(u'^[A-Z]*:')
        self.MaxheightExtraValue = ["default", "below_default", "no_indications", "no_sign", "none", "unsigned"]

    def node(self, data, tags):
        for i in self.tag_number:
            tag = i[0]
            if tag in tags:
                m = parseNumberUnitString(tags[tag])
                if (not m and
                    not (tag == "width" and tags[tag] == "narrow") and
                    not (tag == "capital" and tags[tag] == "yes") and
                    not (tag == "heritage" and tags[tag] == "yes") and
                    not (("maxspeed" in tag or "minspeed" in tag) and (
                        tags[tag] in self.MaxspeedExtraValue or
                        self.MaxspeedClassValue.match(tags[tag]) or
                        (tags[tag] == "implicit" and ("traffic_sign" in tags) and "maxspeed" in tags["traffic_sign"].split(";"))
                    )) and
                    not (tag == "maxheight" and tags[tag] in self.MaxheightExtraValue)
                ):
                    return {"class": 3091, "subclass": 1, "text": T_("Concerns tag: `{0}`", '='.join([tag, tags[tag]])) }
                if not m:
                    continue

                if m["unit"] and (any(x in m["unit"] for x in (',', '-', ';', '.', '~')) or m["unit"][0].strip() == ''):
                    # Invalid numbers, or multiple values
                    return {"class": 3091, "subclass": 8, "text": T_("Concerns tag: `{0}`", '='.join([tag, tags[tag]])) }

                # Below here only tags containing numbers with/without unit remain
                if tag in self.tag_number_integer and str(int(abs(m["value"]))) != tags[tag]:
                    # Expected: positive integer, found: decimal number or number with unit
                    return {"class": 3093, "subclass": 4, "text": T_("Concerns tag: `{0}`", '='.join([tag, tags[tag]])) }
                if m["unit"] and not m["unit"] in self.units:
                    try:
                        convertToUnit(m, i[1]) # Will throw in case conversion to the default unit (i[1]) isn't possible
                    except NotImplementedError:
                        return {"class": 3094, "subclass": 6, "text": T_("Concerns tag: `{0}`", '='.join([tag, tags[tag]])) }
                if tag == "height":
                    try:
                        if convertToUnit(m, 'm') > 500:
                            return {"class": 3092, "subclass": 2, "text": T_("`height={0}` is really tall, consider changing to `ele=*`", tags[tag]),
                                 "fix": {"-": ["height"], "+": {"ele": tags["height"]}} }
                    except: # E.g. height in speed units; TODO: remove try/except once all units of self.unit are dealt with in convertToUnit
                        return {"class": 3094, "subclass": 7, "text": T_("Concerns tag: `{0}`", '='.join([tag, tags[tag]])) }
                elif "maxspeed" in tag and m["value"] < 5 and not "waterway" in tags:
                    return {"class": 3092, "subclass": 3, "text": T_('`{0}` is really slow', 'maxspeed=' + tags[tag])}
                elif tag == "width" and m["value"] <= 0 and "highway" in tags: # seems to be an old iD bug
                    return {"class": 3092, "subclass": 5, "text": T_("Concerns tag: `{0}`", '='.join([tag, tags[tag]]))}

                # Warn about "highly discouraged" aliases from the wiki, like 'kilometer' instead of 'km'
                if m["unit"] and (
                        (len(m["unit"].replace('/', '')) >= 4 and m["unit"] not in ("l/min", "knots")) or
                        (m["unit"] in ("m3/s", "m3/h", "kph", "kmh", "ST", "T", "ton", "lb", "ft", "in"))):
                    return {"class": 30915, "subclass": 9, "text": T_("Concerns tag: `{0}`", '='.join([tag, tags[tag]]))}

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

        for d in ["3,75", "foo", "18,4m", "4.8 cars", "12 km/h", "12 t", "4810", "４"]:
            self.check_err(a.node(None, {"height":d}), ("height='{0}'".format(d)))
            self.check_err(a.way(None, {"height":d}, None), ("height='{0}'".format(d)))
            self.check_err(a.relation(None, {"height":d}, None), ("height='{0}'".format(d)))
        assert not a.node(None, {"height": "650 mm"})

        for d in ["foo", "18kph", "1", "30 c", "30 m", "70;80 km/h", "70-80", "42.5.5"]:
            self.check_err(a.node(None, {"maxspeed":d}), ("maxspeed='{0}'".format(d)))
            self.check_err(a.node(None, {"maxspeed:backward":d}), ("maxspeed:backward='{0}'".format(d)))

        for d in ["50", "FR:urban", "35 mph", "10 knots", "default"]:
            assert not a.node(None, {"maxspeed":d}), ("maxspeed='{0}'".format(d))
            assert not a.node(None, {"minspeed:forward":d}), ("minspeed:forward='{0}'".format(d))

        for d in ["50 millimeters", "40 metre", "30 feet", "30 in", "10 mile", "6ft 6in"]:
            self.check_err(a.node(None, {"distance": d}), ("distance='{0}'".format(d)))

        assert not a.node(None, {"maxspeed":"1", "waterway": "river"})

        assert not a.node(None, {"maxspeed": "implicit", "traffic_sign": "maxspeed"})

        assert not a.node(None, {"maxheight": "default"})

        assert not a.node(None, {"capital":"yes"})
        assert not a.node(None, {"capital":"2"})

        assert not a.node(None, {"width": "4.5", "highway": "residential"})
        assert a.node(None, {"width": "0", "highway": "residential"})

        assert not a.node(None, {"population":"5000"})
        for d in ["-50", "many", "20 km", "4.5", "4.0"]:
            assert a.node(None, {"population": d})
