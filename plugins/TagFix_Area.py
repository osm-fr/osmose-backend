#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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


class TagFix_Area(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.area_yes_good = set(('aerialway', 'aeroway', 'amenity', 'barrier', 'highway', 'historic', 'leisure', 'man_made', 'military', 'power', 'public_transport', 'sport', 'tourism', 'waterway'))
        self.area_yes_bad = set(('boundary', 'building', 'craft', 'geological', 'landuse', 'natural', 'office', 'place', 'shop', 'indoor'))
        self.errors[32001] = self.def_class(item = 3200, level = 3, tags = ['tag', 'fix:chair'],
            title = T_('Redundant area tagging'),
            detail = T_('This feature is already implicitly an area due to another tag.'),
            fix = T_f('Remove the `{0}` tag.', 'area=yes')
        )
        self.errors[32002] = self.def_class(item = 3200, level = 3, tags = ['tag', 'fix:chair'],
            title = T_('Untagged area object'),
            detail = T_('The object is missing any tag which defines what kind of feature it is. This is unexpected for something tagged with `area=yes`.'),
            fix = self.merge_doc(
              T_('Add a top level tag to state what this feature is. Considered acceptable `area=yes` features are:'),
              {'en': ', '.join(map(lambda x: '`{}`'.format(x), self.area_yes_good))}
            ),
            trap = T_('It may be more appropriate to remove the object completely if it isn\'t useful.')
        )
        self.errors[32003] = self.def_class(item = 3200, level = 3, tags = ['tag', 'fix:chair'],
            title = T_('Redundant area negation'),
            detail = T_('This feature is already implicitly not an area.'),
            fix = T_f('Remove the `{0}` tag.', 'area=no')
        )

    def way(self, data, tags, nds):
        err = []
        key_set = set(tags.keys())
        if tags.get("area") == "yes":
            tagged_as_bad = set(key_set & self.area_yes_bad)
            if len(tagged_as_bad) > 0:
                err.append({
                    "class": 32001,
                    "subclass": 1,
                    "text": T_f('Tags, {0}, already make this an area.', '/'.join(map(lambda x: '`{}`'.format(x), tagged_as_bad)))
                })
            elif not (len(key_set & self.area_yes_good) > 0 or tags.get("railway") == "platform"):
                err.append({"class": 32002, "subclass": 1})
        if tags.get("area") == "no" and not "aeroway" in tags and not "building" in tags and not "landuse" in tags and not "leisure" in tags and not "natural" in tags:
            err.append({"class": 32003, "subclass": 1})

        return err

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Area(None)
        a.init(None)

        for t in [{"area":"yes", "railway": "rail"},
                  {"area":"yes", "building": "yes"},
                  {"area":"yes", "landuse": "farm"},
                  {"area":"no", "amenity": "bakery"},
                  {"area":"yes", "indoor": "room"},
                 ]:
            self.check_err(a.way(None, t, None), t)

        for t in [{"area":"yes", "railway": "platform"},
                  {"area":"yes", "amenity": "bakery"},
                  {"area":"no", "building": "yes"},
                 ]:
            assert not a.way(None, t, None), t
