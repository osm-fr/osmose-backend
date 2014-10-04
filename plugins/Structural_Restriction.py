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


class Structural_Restriction(Plugin):

    # Check for no u-turn on same road on countries where is forbidden
    only_for = ["BR"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[31801] = {"item": 3180, "level": 2, "tag": ["relation", "restriction"], "desc": T_(u"Useless non u-turn restriction, it's forbidden by local law") }

    def relation(self, data, tags, members):
        if tags.get('type') == 'restriction' and tags.get('restriction') == 'no_u_turn':
            from_ = set()
            to = set()
            for member in members:
                if member['role'] == 'from':
                    from_.add(member['id'])
                elif member['role'] == 'to':
                    to.add(member['id'])
            if from_ == to:
                return [(31801, 0, {})]


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_Restriction(None)
        a.init(None)

        assert not a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role':'from', 'id': 1}, {'role': 'to', 'id': 2}])
        assert not a.relation(None, {'type': 'restriction', 'restriction': 'text'}, [{'role':'from', 'id': 1}, {'role': 'to', 'id': 1}])

        self.check_err(a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role':'from', 'id': 1}, {'role': 'to', 'id': 1}]))
