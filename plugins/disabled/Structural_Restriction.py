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

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[31801] = {"item": 3180, "level": 2, "tag": ["relation", "restriction"], "desc": T_(u"Useless turn restriction") }
        self.Country = self.father.config.options.get("country")

    def relation(self, data, tags, members):
        # Check for "from" equals to "to"
        if tags.get('type') == 'restriction' and tags.get('restriction') and tags.get('restriction') not in ('no_u_turn', 'only_u_turn'):
            from_ = set()
            to = set()
            for member in members:
                if member['role'] == 'from':
                    from_.add(member['ref'])
                elif member['role'] == 'to':
                    to.add(member['ref'])
            if len(from_) > 0 and from_ == to:
                return {"class": 31801}


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_Restriction(None)
        class _config:
            options = {}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role': 'to', 'ref': 229614650, 'type': 'way'}, {'role': 'via', 'ref': 160840160, 'type': 'way'}, {'role': 'from', 'ref': 229614674, 'type': 'way'}])
        assert not a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role':'from', 'ref': 1}, {'role': 'to', 'ref': 2}])
        self.check_err(a.relation(None, {'type': 'restriction', 'restriction': 'text'}, [{'role':'from', 'ref': 1}, {'role': 'to', 'ref': 1}]))
        assert not a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role':'from', 'ref': 1}, {'role': 'to', 'ref': 1}])

    def test_BR(self):
        a = Structural_Restriction(None)
        class _config:
            options = {"country": "BR"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role': 'to', 'ref': 229614650, 'type': 'way'}, {'role': 'via', 'ref': 160840160, 'type': 'way'}, {'role': 'from', 'ref': 229614674, 'type': 'way'}])
        assert not a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role':'from', 'ref': 1}, {'role': 'to', 'ref': 2}])
        self.check_err(a.relation(None, {'type': 'restriction', 'restriction': 'text'}, [{'role':'from', 'ref': 1}, {'role': 'to', 'ref': 1}]))
        self.check_err(a.relation(None, {'type': 'restriction', 'restriction': 'no_u_turn'}, [{'role':'from', 'ref': 1}, {'role': 'to', 'ref': 1}]))
