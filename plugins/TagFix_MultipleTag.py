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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin


class TagFix_MultipleTag(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.country = self.father.config.options.get("country")
        main_tags = ('type', 'aerialway', 'aeroway', 'amenity', 'barrier', 'boundary', 'building', "building:part", 'craft', 'disc_golf', 'entrance', 'emergency', 'geological', 'highway', 'historic', 'landuse', 'leisure', 'man_made', 'military', 'natural', 'office', 'place', 'playground', 'power', 'public_transport', 'railway', 'route', 'shop', 'sport', 'tourism', 'waterway', 'mountain_pass', 'traffic_sign', 'golf', 'piste:type', 'junction', 'healthcare', 'health_facility:type', 'indoor', 'club', 'seamark:type', 'attraction', 'information', 'advertising', 'ford', 'cemetery', 'area:highway', 'checkpoint', 'telecom', 'airmark')

        self.errors[30323] = self.def_class(item = 3032, level = 3, tags = ['tag', 'fix:chair'],
            title = T_('Watch multiple tags'))
        self.errors[20803] = self.def_class(item = 2080, level = 2, tags = ['tag', 'highway', 'fix:chair'],
            title = T_('Tag highway missing for tracktype or lanes'))
        self.errors[21101] = self.def_class(item = 2110, level = 2, tags = ['tag'],
            title = T_('Untagged named object'),
            detail = T_('The object is missing any tag which defines what kind of feature it is. This is unexpected for something with a `name` tag.'),
            fix = self.merge_doc(
                T_('Add a top level tag to state what this feature is. Considered top level tags are (with derived `disused:`, `abandoned:` and `historic:` variants):'),
                {'en': ', '.join(map(lambda x: '`{}`'.format(x), sorted(main_tags)))} ),
            trap = T_('It may be more appropriate to remove the object completely if it isn\'t useful.')
        )
        self.errors[1050] = self.def_class(item = 1050, level = 1, tags = ['highway', 'roundabout', 'fix:chair'],
            title = T_('Reverse roundabout'),
            detail = T_(
'''The circulation of the roundabout is drawn clockwise, but in countries
where they drive on the right, the circulation of roundabouts is
counterclockwise, and vice versa for other countries.'''),
            fix = T_(
'''For the mini roundabouts `highway=mini_roundabout`: the tag
`direction=*` indicates the direction, in countries driven on the right,
the default is `direction=anticlockwise`, in this case it is useless as
tag.'''),
            trap = T_(
'''Make sure that it is a roundabout (for example, not a side way in
opposite direction around a square or a central roundabout, or a driveway
separated by traffic islands at an intersection without cross).'''),
            example = T_(
'''![](https://wiki.openstreetmap.org/w/images/6/68/Osmose-eg-error-1050.png)

Clockwise rotation.'''))
        self.errors[32200] = self.def_class(item = 3220, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Overly permissive access'),
            detail = T_(
'''The tags `access=yes` and `access=permissive` mark a feature as wide open to all transport modes. \
This is almost never the case and more specific tags should be used instead. \
For further detail, see [the wiki](https://wiki.openstreetmap.org/wiki/Key:access#Transport_mode_restrictions).'''))
        self.errors[32201] = self.def_class(item = 3220, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Overly permissive access'),
            detail = T_(
'''The tags `access=yes` and `access=permissive` mark a feature as wide open to all transport modes. \
This is almost never the case and more specific tags should be used instead. \
For further detail, see [the wiki](https://wiki.openstreetmap.org/wiki/Key:access#Transport_mode_restrictions).'''))

        self.driving_side_right = not (self.father.config.options.get("driving_side") == "left")
        self.driving_direction = "anticlockwise" if self.driving_side_right else "clockwise"
        name_parent = []
        for i in main_tags:
            name_parent.append(i)
            name_parent.append("disused:" + i)
            name_parent.append("abandoned:" + i)
            name_parent.append("historic:" + i)
            name_parent.append("proposed:" + i)
            name_parent.append("planned:" + i)
            name_parent.append("construction:" + i)
            name_parent.append("abandoned:" + i)
            name_parent.append("demolished:" + i)
            name_parent.append("removed:" + i)
            name_parent.append("razed:" + i)
            name_parent.append("was:" + i)
            name_parent.append("ruins:" + i)
            name_parent.append("destroyed:" + i)
            name_parent.append(i + ":backward")
            name_parent.append(i + ":forward")
        self.name_parent = set(name_parent)

    def common(self, tags, key_set):
        err = []
        if tags.get("name") and len(key_set & self.name_parent) == 0 and tags.get("naptan:verified") != "no":
            err.append({"class": 21101, "subclass": 1})

        return err

    def node(self, data, tags):
        err = self.common(tags, set(tags.keys()))
        if tags.get("highway") == "mini_roundabout" and "direction" in tags:
            clockwise = tags["direction"] == "clockwise"
            anticlockwise = tags["direction"] in ["anticlockwise", "anti_clockwise"]
            if (self.driving_side_right and clockwise) or (not self.driving_side_right and anticlockwise):
                err.append({"class": 1050, "subclass": 1000, "text": T_("mini roundabout direction in this country is usually \"{0}\"", self.driving_direction),
                            "fix": {"-": ["direction"]}})

        return err

    def way(self, data, tags, nds):
        key_set = set(tags.keys())
        err = self.common(tags, key_set)

        if tags.get("access") in ("yes", "permissive"):
            if tags.get("highway") in ("motorway", "trunk"):
                err.append({"class": 32200, "subclass": 0, "text": T_("Including ski, horse, moped, hazmat and so on, unless explicitly excluded")})
            if tags.get("highway") in ("footway", "bridleway", "steps", "path", "cycleway", "pedestrian", "track", "bus_guideway", "busway", "raceway"):
                err.append({"class": 32201, "subclass": 0, "text": T_("Including car, horse, moped, hazmat and so on, unless explicitly excluded")})

        if (tags.get("tracktype") or tags.get("lanes")) and not tags.get("highway") and not tags.get("disused:highway") and not tags.get("abandoned:highway") and not tags.get("construction:highway") and not tags.get("proposed:highway") and not tags.get("planned:highway") and not tags.get("leisure") == "track":
            err.append({"class": 20803})

        return err

    def relation(self, data, tags, members):
        err = self.common(tags, set(tags.keys()))

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

        assert a.node(None, {"name": "foo"})
        assert not a.node(None, {"name": "foo", "disused:highway": "bar"})
        assert not a.node(None, {"name": "foo", "abandoned:highway": "bar"})
        assert not a.node(None, {"name": "foo", "historic:railway": "station"})
        assert not a.node(None, {"name": "foo", "building:part": "yes"})
        assert not a.node(None, {"name": "foo", "traffic_sign:forward": "city_limit;DE:310", "traffic_sign:backward": "city_limit;DE:311"})

        assert a.way(None, {"highway": "track", "access": "yes"}, None)
        assert a.way(None, {"highway": "trunk", "access": "yes"}, None)

        assert a.way(None, {"tracktype": "foo"}, None)
        assert not a.way(None, {"tracktype": "foo", "leisure": "track"}, None)
