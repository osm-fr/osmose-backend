#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Andrea Decorte 2020                                        ##
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


class TagFix_Pharmacy(Plugin):

    only_for = ["FR", "NC", "BE"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30326] = self.def_class(item = 2100, level = 3, tags = ['fix:chair'],
            title = T_('In the country all pharmacies deliver drugs under prescription'),
            detail = T_(
'''All pharmacies in the country sell on prescription by a doctor. It requires a
tag `dispensing=yes` in addition to `amenity=pharmacy`.'''),
            fix = T_(
'''Add tag `dispensing=yes`.'''),
            trap = T_(
'''Chemist shops ("parapharmacie" in French) do not fall into this
classification. They do not have a specific tag for the moment.'''))

    def node(self, data, tags):
        err = []
        if tags.get("amenity") == "pharmacy" and tags.get("dispensing") != "yes":
            err.append({"class": 30326, "subclass": 7, "fix": [{"+": {"dispensing": "yes"}}, {"-": ["amenity"], "+": {"shop": "chemist"}}]})

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_FR(self):
        a = TagFix_Pharmacy(None)
        class _config:
            options = {"country": "FR", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert a.node(None, {"amenity":"pharmacy"})
        assert not a.node(None, {"amenity":"pharmacy", "dispensing": "yes"})
        assert not a.node(None, {"shop":"chemist"})
