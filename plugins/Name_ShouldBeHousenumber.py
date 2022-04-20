#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights arrival-spring 2022                                        ##
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
import regex as re

class Name_ShouldBeHousenumber(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[50101] = self.def_class(item = 5010, level = 2, tags = ['name', 'fix:chair'],
            title = T_('Name with only numbers'),
            detail = T_(
'''This building is tagged with a name which contains only numbers
and does not appear to have a main feature key.
For the majority of buildings this should be tagged with `addr:housenumber`.'''),
            fix = T_(
'''If this `name` is in fact the housenumber, it should be tagged with
`addr:housenumber` + `addr:street` (or other `addr:*`), alternatively a
relation can be used.'''),
            trap = T_(
'''While uncommon, it is possible for a name to be only numbers.
This is particularly the case for some brands or amenities.

Additionally, it could also be an apartment block number or building
number (not an official house number with a postal address, but for
example "beach cabin #1"); in these cases, ref would be the appropriate
tag.

Always check with your local community about the preferred tagging style
of house numbers: in some regions, a separate node inside the building is
preferred over a tag on the building itself.''')
        )
        self.Numerical = re.compile(r"^[0-9]+$")
        self.feature_keys = ["amenity", "craft", "emergency", "leisure", "military", "office", "railway", "shop", "tourism"]

    def node(self, data, tags):
        err = []
        if "building" in tags:
            if not any(feature in tags for feature in self.feature_keys):
                if "name" in tags:
                    if self.Numerical.match(tags["name"]):
                        err.append({"class": 50101,
                            "text": T_("Concerns tag: `{0}`", '='.join(['name', tags['name']])) })
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_ShouldBeHousenumber(None)
        a.init(None)
        for t in [{"building": "yes", "name": "123"},
                  {"building": "residential", "name": "5"},
                  {"building": "detached", "name": "5637"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)

        for t in [{"building": "yes", "name": "12 Flats"},
                  {"building": "yes", "name": "21", "shop": "yes"},
                  {"building": "commercial", "name": "1", "office": "yes"},
                 ]:
            assert not a.node(None, t), t
