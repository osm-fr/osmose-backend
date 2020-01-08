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

from plugins.Plugin import Plugin


class Structural_Useless_Relation(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[12001] = self.def_class(item = 1200, level = 2, tags = ['relation', 'fix:chair'],
            title = T_('1-member relation'),
            detail = T_(
'''The relation only contains one member.'''),
            fix = T_(
'''Check if no member is missing, check the history, check if there is
another similar relation with more members. A one-member relation may
sometimes be justified.'''),
            trap = T_(
'''Do not remove a relation without understanding why it is there.'''))

    def relation(self, data, tags, members):
        if len(members) == 1:
            if tags.get("site") == "geodesic":
                return
            if tags.get("type") in ("defaults", "route", "route_master", "associatedStreet"):
                return
            return {"class": 12001, "subclass": 1}


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def setUp(self):
        TestPluginCommon.setUp(self)
        self.p = Structural_Useless_Relation(None)
        self.p.init(None)

    def test(self):
        w1 = { "ref": 1, "role": "yy", "type": "way"}
        w2 = { "ref": 2, "role": "xx", "type": "way"}
        for t in [({"type": "waterway"}, True),
                  ({"type": "defaults"}, False),
                  ({"type": "defaults_toto"}, True),
                  ({"type": "route"}, False),
                  ({"type": "route_master"}, False),
                  ({"type": "associatedStreet"}, False),
                  ({"type": "test"}, True),
                  ({"site": "geodesic"}, False),
                 ]:
            if t[1]:
                self.check_err(self.p.relation(None, t[0], [w1]), t[0])
            else:
                assert not self.p.relation(None, t[0], [w1]), t[0]

            assert not self.p.relation(None, t[0], [w1, w2]), t[0]
