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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin


class TagFix_Area(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.area_yes_good = set(('aerialway', 'aeroway', 'amenity', 'barrier', 'highway', 'historic', 'leisure', 'man_made', 'military', 'playground', 'power', 'public_transport', 'sport', 'tourism', 'traffic_calming', 'waterway'))
        self.area_yes_default = set(('boundary', 'building', 'craft', 'geological', 'indoor', 'landuse', 'natural', 'office', 'place', 'shop'))
        self.errors[32002] = self.def_class(item = 3200, level = 3, tags = ['tag', 'fix:chair'],
            title = T_('Untagged area object'),
            detail = T_('The object is missing any tag which defines what kind of feature it is. This is unexpected for something tagged with `area=yes`.'),
            fix = self.merge_doc(
                T_('Add a top level tag to state what this feature is. Considered acceptable `area=yes` features are:'),
                {'en': ', '.join(map(lambda x: '`{}`'.format(x), sorted(self.area_yes_good)))} ),
            trap = T_('It may be more appropriate to remove the object completely if it isn\'t useful.')
        )
        self.errors[32003] = self.def_class(item = 3200, level = 3, tags = ['tag', 'fix:chair'],
            title = T_('Redundant area negation'),
            detail = T_('This feature is already implicitly not an area.'),
            fix = T_('Remove the `{0}` tag.', 'area=no')
        )

    def way(self, data, tags, nds):
        err = []
        if not "area" in tags:
            return err
        key_set = set(tags.keys())
        if tags.get("area") == "yes":
            if len(key_set & self.area_yes_default) == 0 and len(key_set & self.area_yes_good) == 0 and tags.get("railway") != "platform":
                err.append({"class": 32002, "subclass": 1})
        elif tags.get("area") == "no" and not "aeroway" in tags and not "building" in tags and not "landuse" in tags and not "leisure" in tags and not "natural" in tags:
            err.append({"class": 32003, "subclass": 1})

        return err

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Area(None)
        a.init(None)

        for t in [{"area":"yes", "railway": "rail"},
                  {"area":"no", "amenity": "bakery"},
                 ]:
            self.check_err(a.way(None, t, None), t)

        for t in [{"area":"yes", "railway": "platform"},
                  {"area":"yes", "amenity": "bakery"},
                  {"area":"no", "building": "yes"},
                 ]:
            assert not a.way(None, t, None), t

        # Unnecessary area=yes, dealt with by JOSM mapcss rules instead
        for t in [{"area":"yes", "building": "yes"},
                 ]:
            assert not a.way(None, t, None), t
