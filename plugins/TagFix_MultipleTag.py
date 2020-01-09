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
        self.country = self.father.config.options.get("country")
        main_tags = ('type', 'aerialway', 'aeroway', 'amenity', 'barrier', 'boundary', 'building', 'craft', 'entrance', 'emergency', 'geological', 'highway', 'historic', 'landuse', 'leisure', 'man_made', 'military', 'natural', 'office', 'place', 'power', 'public_transport', 'railway', 'route', 'shop', 'sport', 'tourism', 'waterway', 'mountain_pass', 'traffic_sign', 'mountain_pass', 'golf', 'piste:type', 'junction', 'healthcare', 'health_facility:type', 'indoor', 'club', 'seamark:type', 'attraction', 'information')

        self.errors[30320] = self.def_class(item = 3032, level = 1, tags = ['tag', 'highway', 'fix:chair'],
            title = T_('Watch multiple tags'))
        self.errors[30323] = self.def_class(item = 3032, level = 3, tags = ['tag', 'fix:chair'],
            title = T_('Watch multiple tags'))
        self.errors[30327] = self.def_class(item = 3032, level = 2, tags = ['tag', 'fix:chair'],
            title = T_('Waterway with level'))
        self.errors[303210] = self.def_class(item = 3032, level = 1, tags = ['tag', 'highway', 'fix:chair'],
            title = T_('Fence with material tag, better use fence_type tag'))
        self.errors[20800] = self.def_class(item = 2080, level = 1, tags = ['tag', 'highway', 'roundabout', 'fix:chair'],
            title = T_('Tag highway missing on junction'),
            detail = T_(
'''The way have a tag `junction=*` but without `highway=*`.'''),
            trap = T_(
'''Check if it is really an highway and it is not already mapped.'''))
        self.errors[20801] = self.def_class(item = 2080, level = 1, tags = ['tag', 'highway', 'fix:chair'],
            title = T_('Tag highway missing on oneway'),
            detail = T_(
'''The way have a tag `oneway=*` but without `highway=*`.'''),
            trap = T_(
'''Check if it is really an highway and it is not already mapped.'''))
        self.errors[20803] = self.def_class(item = 2080, level = 2, tags = ['tag', 'highway', 'fix:chair'],
            title = T_('Tag highway missing for tracktype or lanes'))
        self.errors[71301] = self.def_class(item = 7130, level = 3, tags = ['tag', 'highway', 'maxheight', 'fix:survey'],
            title = T_('Missing maxheight tag'),
            detail = T_(
'''Missing `maxheight=*` or `maxheight:*` for a tunnel or a way under a
bridge.'''))
        self.errors[21101] = self.def_class(item = 2110, level = 2, tags = ['tag'],
            title = T_('Name present but missing main tag'),
            detail = self.merge_doc(T_(
'''The object is missing any tag which defines what kind of feature is
it. Considered main tags are (with derived `disused:` and
`abandoned:`):''',
              {'en': ', '.join(main_tags)})),
            fix = T_(
'''Add a top level tag to state what kind of thing is it.'''))
        self.errors[21102] = self.def_class(item = 2110, level = 2, tags = ['tag'],
            title = T_('Missing relation type'))
        self.errors[1050] = self.def_class(item = 1050, level = 1, tags = ['highway', 'roundabout', 'fix:chair'],
            title = T_('Reverse roundabout'),
            detail = T_(
'''The circulation of the roundabout is draw clockwise, but in countries
where they drive on the right the sense of roundabouts is
counterclockwise, and vice versa for the other countries.'''),
            fix = T_(
'''For the mini roundabouts `highway=mini_roundabout`: the tag
`direction=*` indicates the direction, in countries driven on the right,
the default is `direction=anticlockwise`, in this case it is useless as
tag.'''),
            trap = T_(
'''Make sure that it is a roundabout (for example, no a side way in
oposite direction around a square or a central roundabout, ordriveways
separated by traffic islands at an intersection without cross).'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/6/68/Osmose-eg-error-1050.png)

Clockwise rotation.'''))
        self.errors[40201] = self.def_class(item = 4020, level = 1, tags = ['highway', 'roundabout'],
            title = T_('Roundabout as area'))
        self.errors[21201] = self.def_class(item = 2120, level = 3, tags = ['indoor'],
            title = T_('Level or repeat_on tag missing'))
        self.errors[21202] = self.def_class(item = 2120, level = 3, tags = ['indoor'],
            title = T_('Indoor or buildingpart tag missing'))
        self.errors[20802] = self.def_class(item = 2080, level = 2, tags = ['highway'],
            title = T_('Missing tag ref for emergency access point'))
#        self.errors[70401] = self.def_class(item = 7040, level = 2, tags = ['tag', 'power', 'fix:chair'],
#            title = T_('Bad power line kind'))
        self.errors[32200] = self.def_class(item = 3220, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('access=yes|permissive allow all transport modes'),
            detail = T_(
'''`access=yes` means wide open to all transport mode, look at [access](https://wiki.openstreetmap.org/wiki/Key:access#Transport_mode_restrictions).'''))
        self.errors[32201] = self.def_class(item = 3220, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('access=yes|permissive allow all transport modes'),
            detail = T_(
'''`access=yes` means wide open to all transport mode, look at [access](https://wiki.openstreetmap.org/wiki/Key:access#Transport_mode_restrictions).'''))

        if not self.country or not self.country.startswith("CZ"):
            self.errors[32301] = self.def_class(item = 3230, level = 2, tags = ['highway', 'fix:chair'],
                title = T_('Probably only for bottles, not any type of glass'))
        self.errors[32302] = self.def_class(item = 3230, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Suspicious name for a container'))

        self.driving_side_right = not(self.father.config.options.get("driving_side") == "left")
        self.driving_direction = "anticlockwise" if self.driving_side_right else "clockwise"
        name_parent = []
        for i in main_tags:
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

        if not self.country or not self.country.startswith("CZ"):
            if tags.get("amenity") == "recycling" and tags.get("recycling_type") != "centre" and tags.get("recycling:glass") == "yes":
                err.append({"class": 32301, "fix": {"-": ["recycling:glass"], "+": {"recycling:glass_bottles": "yes"}}})
        if tags.get("amenity") == "recycling" and tags.get("recycling_type") != "centre" and tags.get("name"):
            err.append({"class": 32302})

        if tags.get("barrier") == "fence" and "fence_type" not in tags and "material" in tags:
            err.append({"class": 303210})

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
        assert not a.node(None, {"name": "foo", "disused:highway": "bar"})
        assert not a.node(None, {"name": "foo", "abandoned:highway": "bar"})

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

        assert a.node(None, {"barrier": "fence", "material": "wood"})
