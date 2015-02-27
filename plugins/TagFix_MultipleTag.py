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
        self.errors[20301] = { "item": 2030, "level": 1, "tag": ["tag", "highway", "cycleway", "fix:survey"], "desc": T_(u"Opposite cycleway without oneway") }
        self.errors[71301] = { "item": 7130, "level": 3, "tag": ["tag", "highway", "maxheight", "fix:survey"], "desc": T_(u"Missing maxheight tag") }
        self.errors[21101] = { "item": 2110, "level": 3, "tag": ["tag"], "desc": T_(u"Missing object kind") }
        self.errors[1050] = { "item": 1050, "level": 1, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Reverse roundabout") }
#        self.errors[70401] = { "item": 7040, "level": 2, "tag": ["tag", "power", "fix:chair"], "desc": T_(u"Bad power line kind") }
        self.driving_side_right = not(self.father.config.options.get("driving_side") == "left")
        self.driving_direction = "anticlockwise" if self.driving_side_right else "clockwise"
        name_parent = []
        for i in ('type', 'aerialway', 'aeroway', 'amenity', 'barrier', 'boundary', 'building', 'craft', 'entrance', 'emergency', 'geological', 'highway', 'historic', 'landuse', 'leisure', 'man_made', 'military', 'natural', 'office', 'place', 'power', 'public_transport', 'railway', 'route', 'shop', 'sport', 'tourism', 'waterway', 'mountain_pass', 'traffic_sign', 'mountain_pass', 'golf', 'piste:type', 'junction', 'health_facility:type'):
            name_parent.append(i)
            name_parent.append("disused:" + i)
            name_parent.append("abandonned:" + i)
        self.name_parent = set(name_parent)

    def common(self, tags, key_set):
        err = []
        if tags.get("name") and len(key_set & self.name_parent) == 0:
            err.append((21101, 1, {}))

        return err

    def node(self, data, tags):
        err = self.common(tags, set(tags.keys()))
        if "highway" in tags and tags["highway"] == "mini_roundabout" and "direction" in tags:
            clockwise = tags["direction"] == "clockwise"
            anticlockwise = tags["direction"] in ["anticlockwise", "anti_clockwise"]
            if (self.driving_side_right and clockwise) or (not self.driving_side_right and anticlockwise):
                err.append({"class": 1050, "subclass": 1000,
                            "text": T_(u"mini roundabout direction in this country is usually \"%s\"", self.driving_direction),
                            "fix": {"-": ["direction"]}})
            if (self.driving_side_right and anticlockwise) or (not self.driving_side_right and clockwise):
                err.append({"class": 1050, "subclass": 1001,
                            "text": T_(u"Mini roundabout direction in this country is \"%s\" by default, useless direction tag", self.driving_direction),
                            "fix": {"-": ["direction"]}})

        return err

    def way(self, data, tags, nds):
        key_set = set(tags.keys())
        err = self.common(tags, key_set)
        if "highway" in tags and "fee" in tags:
            err.append({"class": 30320, "subclass": 1000,
                        "text": T_(u"Use tag \"toll\" instead of \"fee\""),
                        "fix": {"-": ["fee"], "+": {"toll": tags["fee"]}} })

        if u"junction" in tags and tags[u"junction"] != "yes" and u"highway" not in tags:
            err.append((20800, 0, {}))

        if u"oneway" in tags and not (u"highway" in tags or u"railway" in tags or u"aerialway" in tags or u"waterway" in tags or u"aeroway" in tags):
            err.append((20801, 0, {}))

        if "highway" in tags and "cycleway" in tags and tags["cycleway"] in ("opposite", "opposite_lane") and ("oneway" not in tags or ("oneway" in tags and tags["oneway"] == "no")):
            err.append((20301, 0, {}))

        if "highway" in tags and tags["highway"] in ("motorway_link", "trunk_link", "primary", "primary_link", "secondary", "secondary_link") and not "maxheight" in tags and not "maxheight:physical" in tags and (("tunnel" in tags and tags["tunnel"] != "no") or ("covered" in tags and tags["covered"] != "no")):
            err.append((71301, 0, {}))

        if "waterway" in tags and "level" in tags:
            err.append((30327, 0, {"fix": [{"-": "level"}, {"-": ["level"], "+": {"layer": tags["level"]}}]}))

#        if "power" in tags and tags["power"] in ("line", "minor_line") and "voltage" in tags:
#            voltage = map(int, filter(lambda x: x.isdigit(), map(lambda x: x.strip(), tags["voltage"].split(";"))))
#            if voltage:
#                voltage = max(voltage)
#                print voltage
#                if voltage > 45000 and tags["power"] == "minor_line":
#                    err.append((70401, 0, {"fix": {"~": {"power": "line"}}}))
#                elif voltage <= 45000 and tags["power"] == "line":
#                    err.append((70401, 1, {"fix": {"~": {"power": "minor_line"}}}))

        return err

    def relation(self, data, tags, members):
        return self.common(tags, set(tags.keys()))

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
        for d in ["clockwise", "anticlockwise"]:
            t = {"highway":"mini_roundabout", "direction":d}
            self.check_err(a.node(None, t), t)

        a.father.config.options["driving_side"] = "left"
        for d in ["clockwise", "anticlockwise"]:
            t = {"highway":"mini_roundabout", "direction":d}
            self.check_err(a.node(None, t), t)

        for t in [{"highway":"", "cycleway": "opposite"},
                  {"highway":"primary", "tunnel": "yes"},
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

        self.check_err(a.way(None, {"waterway": "stream", "level": "-1"}, None))
