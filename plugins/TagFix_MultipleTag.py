#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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


class TagFix_MultipleTag(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30320] = { "item": 3032, "level": 1, "tag": ["tag", "highway", "fix:chair"], "desc": T_(u"Watch multiple tags") }
        self.errors[30323] = { "item": 3032, "level": 3, "tag": ["tag", "fix:chair"], "desc": T_(u"Watch multiple tags") }
        self.errors[30327] = { "item": 3032, "level": 2, "tag": ["tag", "fix:chair"], "desc": T_(u"Waterway with level") }
        self.errors[20800] = { "item": 2080, "level": 1, "tag": ["tag", "highway", "roundabout", "fix:chair"], "desc": T_(u"Tag highway missing on junction") }
        self.errors[20801] = { "item": 2080, "level": 1, "tag": ["tag", "highway", "fix:chair"], "desc": T_(u"Tag highway missing on oneway") }
        self.errors[20803] = { "item": 2080, "level": 2, "tag": ["tag", "highway", "fix:chair"], "desc": T_(u"Tag highway missing for tracktype or lanes") }
        self.errors[71301] = { "item": 7130, "level": 3, "tag": ["tag", "highway", "maxheight", "fix:survey"], "desc": T_(u"Missing maxheight tag") }
        self.errors[21101] = { "item": 2110, "level": 2, "tag": ["tag"], "desc": T_(u"Name present but missing main tag") }
        self.errors[21102] = { "item": 2110, "level": 2, "tag": ["tag"], "desc": T_(u"Missing relation type") }
        self.errors[1050] = { "item": 1050, "level": 1, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Reverse roundabout") }
        self.errors[40201] = { "item": 4020, "level": 1, "tag": ["highway", "roundabout"], "desc": T_(u"Roundabout as area") }
        self.errors[21201] = { "item": 2120, "level": 3, "tag": ["indoor"], "desc": T_(u"Level or repeat_on tag missing") }
        self.errors[21202] = { "item": 2120, "level": 3, "tag": ["indoor"], "desc": T_(u"Indoor or buildingpart tag missing") }
        self.errors[20802] = { "item": 2080, "level": 2, "tag": ["highway"], "desc": T_(u"Missing tag ref for emergency access point") }
#        self.errors[70401] = { "item": 7040, "level": 2, "tag": ["tag", "power", "fix:chair"], "desc": T_(u"Bad power line kind") }
        self.errors[32200] = { "item": 3220, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"access=yes|permissive allow all transport modes") }
        self.errors[32201] = { "item": 3220, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"access=yes|permissive allow all transport modes") }
        self.errors[32301] = { "item": 3230, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Probably only for bottles, not any type of glass") }
        self.errors[32302] = { "item": 3230, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Suspicious name for a container") }
        self.driving_side_right = not(self.father.config.options.get("driving_side") == "left")
        self.driving_direction = "anticlockwise" if self.driving_side_right else "clockwise"
        name_parent = []
        for i in ('type', 'aerialway', 'aeroway', 'amenity', 'barrier', 'boundary', 'building', 'craft', 'entrance', 'emergency', 'geological', 'highway', 'historic', 'landuse', 'leisure', 'man_made', 'military', 'natural', 'office', 'place', 'power', 'public_transport', 'railway', 'route', 'shop', 'sport', 'tourism', 'waterway', 'mountain_pass', 'traffic_sign', 'mountain_pass', 'golf', 'piste:type', 'junction', 'healthcare', 'health_facility:type', 'indoor'):
            name_parent.append(i)
            name_parent.append("disused:" + i)
            name_parent.append("abandoned:" + i)
        self.name_parent = set(name_parent)

    def common(self, tags, key_set):
        err = []
        if tags.get("name") and len(key_set & self.name_parent) == 0 and tags.get("naptan:verified") != "no":
            err.append({"class": 21101, "subclass": 1})

        if tags.get("indoor") not in [None, "yes", "no"] and not tags.get("level") and not tags.get("repeat_on"):
            err.append({"class": 21201, "subclass": 1})

        if tags.get("room") and not tags.get("indoor") and not tags.get("buildingpart"):
            err.append({"class": 21202, "subclass": 2, "fix":[{"+": {"indoor": "room"}}, {"+": {"buildingpart": "room"}}]})

        if tags.get('highway') == 'emergency_access_point' and not tags.get('ref'):
            err.append({"class": 20802, "subclass": 1})

        if tags.get("amenity") == "recycling" and tags.get("recycling_type") != "centre" and tags.get("recycling:glass") == "yes":
            err.append({"class": 32301, "fix": {"-": ["recycling:glass"], "+": {"recycling:glass_bottles": "yes"}}})
        if tags.get("amenity") == "recycling" and tags.get("recycling_type") != "centre" and tags.get("name"):
            err.append({"class": 32302})

        return err

    def node(self, data, tags):
        err = self.common(tags, set(tags.keys()))
        if tags.get("highway") == "mini_roundabout" and "direction" in tags:
            clockwise = tags["direction"] == "clockwise"
            anticlockwise = tags["direction"] in ["anticlockwise", "anti_clockwise"]
            if (self.driving_side_right and clockwise) or (not self.driving_side_right and anticlockwise):
                err.append({"class": 1050, "subclass": 1000, "text": T_(u"mini roundabout direction in this country is usually \"%s\"", self.driving_direction),
                            "fix": {"-": ["direction"]}})
#            if (self.driving_side_right and anticlockwise) or (not self.driving_side_right and clockwise):
#                err.append({"class": 1050, "subclass": 1001, "text": T_(u"Mini roundabout direction in this country is \"%s\" by default, useless direction tag", self.driving_direction),
#                            "fix": {"-": ["direction"]}})

        return err

    def way(self, data, tags, nds):
        key_set = set(tags.keys())
        err = self.common(tags, key_set)
        if "highway" in tags and "fee" in tags:
            err.append({"class": 30320, "subclass": 1000, "text": T_(u"Use tag \"toll\" instead of \"fee\""),
                        "fix": {"-": ["fee"], "+": {"toll": tags["fee"]}} })

        if tags.get("junction") not in (None, "yes") and u"highway" not in tags:
            err.append({"class": 20800, "subclass": 0})

        if u"oneway" in tags and not (u"highway" in tags or u"railway" in tags or u"aerialway" in tags or u"waterway" in tags or u"aeroway" in tags or u"piste:type" in tags):
            err.append({"class": 20801, "subclass": 0})

        if tags.get("highway") in ("motorway_link", "trunk_link", "primary", "primary_link", "secondary", "secondary_link") and not "maxheight" in tags and not "maxheight:physical" in tags and (("tunnel" in tags and tags["tunnel"] != "no") or tags.get("covered") not in (None, "no")):
            err.append({"class": 71301, "subclass": 0})

        if "waterway" in tags and "level" in tags:
            err.append({"class": 30327, "subclass": 0, "fix": [{"-": ["level"]}, {"-": ["level"], "+": {"layer": tags["level"]}}]})

        if "highway" in tags and tags.get('junction') == 'roundabout' and tags.get('area') not in (None, 'no', 'false'):
            err.append({"class": 40201, "subclass": 0, "fix": [{"-": ["area"]}, {"-": ["junction"]}]})

#        if tags.get("power") in ("line", "minor_line") and "voltage" in tags:
#            voltage = map(int, filter(lambda x: x.isdigit(), map(lambda x: x.strip(), tags["voltage"].split(";"))))
#            if voltage:
#                voltage = max(voltage)
#                if voltage > 45000 and tags["power"] == "minor_line":
#                    err.append({"class": 70401, "subclass": 0, "fix": {"~": {"power": "line"}}})
#                elif voltage <= 45000 and tags["power"] == "line":
#                    err.append({"class": 70401, "subclass": 1, "fix": {"~": {"power": "minor_line"}}})

        if tags.get("access") in ("yes", "permissive"):
            if tags.get("highway") in ("motorway", "trunk"):
                err.append({"class": 32200, "subclass": 0, "text": T_("Including ski, horse, moped, hazmat and so on, unless explicitly excluded")})
            if tags.get("highway") in ("footway", "bridleway", "steps", "path", "cycleway", "pedestrian", "track", "bus_guideway", "raceway"):
                err.append({"class": 32201, "subclass": 0, "text": T_("Including car, horse, moped, hazmat and so on, unless explicitly excluded")})

        if (tags.get("tracktype") or tags.get("lanes")) and not tags.get("highway") and not tags.get("disused:highway") and not tags.get("abandoned:highway") and not tags.get("construction:highway") and not tags.get("proposed:highway") and not tags.get("planned:highway") and not tags.get("leisure") == "track":
            err.append({"class": 20803})

        return err

    def relation(self, data, tags, members):
        err = self.common(tags, set(tags.keys()))

        if not "type" in tags:
            err.append({"class": 21102})

        return err

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_MultipleTag(None)
        class _config:
            options = {}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        for d in ["clockwise"]:
            t = {"highway":"mini_roundabout", "direction":d}
            self.check_err(a.node(None, t), t)

        a.father.config.options["driving_side"] = "left"
        for d in ["clockwise"]:
            t = {"highway":"mini_roundabout", "direction":d}
            self.check_err(a.node(None, t), t)

        for t in [{"highway":"primary", "tunnel": "yes"},
                  {"highway":"primary", "fee": "yes"},
                  {"junction":"roundabout", "waterway": "river"},
                  {"oneway":"yes", "building": "yes"},
#                  {"power":"line", "voltage": "1"},
                 ]:
            self.check_err(a.way(None, t, None), t)

        for t in [{"highway":"", "cycleway": "opposite", "oneway": "yes"},
                  {"junction": "yes"},
                 ]:
            assert not a.way(None, t, None), t

        assert a.node(None, {"name": "foo"})
        assert not  a.node(None, {"name": "foo", "disused:highway": "bar"})
        assert not  a.node(None, {"name": "foo", "abandoned:highway": "bar"})

        self.check_err(a.way(None, {"waterway": "stream", "level": "-1"}, None))

        assert a.way(None, {"area": "yes", "highway": "secondary", "junction": "roundabout"}, None)

        assert a.node(None, {"indoor": "room"})

        assert a.node(None, {"room": "office"})

        assert a.way(None, {"highway": "track", "access": "yes"}, None)
        assert a.way(None, {"highway": "trunk", "access": "yes"}, None)

        assert a.way(None, {"tracktype": "foo"}, None)
        assert not a.way(None, {"tracktype": "foo", "leisure": "track"}, None)

        assert a.relation(None, {}, None)

        assert a.node(None, {"amenity": "recycling", "recycling_type": "container", "recycling:glass": "yes"})
        assert a.node(None, {"amenity": "recycling", "recycling_type": "container", "name": "My nice awesome container"})
