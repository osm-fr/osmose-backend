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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin


class Structural_Multipolygon(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[11701] = self.def_class(item = 1170, level = 2, tags = ['relation', 'multipolygon', 'fix:chair'],
            title = T_('Inadequate role for multipolygon'),
            detail = T_(
'''Possible roles are `outer`, `inner` or nothing (not recommended).'''))
        self.errors[11702] = self.def_class(item = 1170, level = 2, tags = ['relation', 'multipolygon', 'fix:chair'],
            title = T_('Inadequate member for multipolygon'),
            detail = T_(
'''Members must be ways.'''))
        self.errors[11703] = self.def_class(item = 1170, level = 1, tags = ['relation', 'multipolygon', 'fix:imagery'],
            title = T_('Missing outer way with role `outer` for multipolygon'),
            detail = T_(
'''At least one outer ring must be present.'''),
            fix = T_(
'''Find the outer way, and add it to the relation with role `outer`. Multiple outer ways are also possible as long as they form one or more closed rings.
The previous outer way may have been deleted, check the history.'''))
        self.errors[11704] = self.def_class(item = 1170, level = 2, tags = ['relation', 'multipolygon', 'fix:chair'],
            title = T_('This multipolygon is a simple polygon'),
            detail = T_(
'''Multipolygon relation actually defines a simple polygon.'''))

    def relation(self, data, tags, members):
        if tags.get('type') != 'multipolygon':
            return

        outer = 0
        inner = 0
        err_roles = []
        err_members = []
        for member in members:
            if member['type'] == 'way':
                if member['role'] not in ('', 'outer', 'inner'):
                    err_roles.append(member['role'])
                if member['role'] in ('', 'outer'):
                    outer += 1
                elif member['role'] == 'inner':
                    inner += 1
            else:
                err_members.append(u"{0} - {1}".format(member['type'], member['role']))

        err = []
        if len(err_roles) > 0:
            err.append({"class": 11701, "subclass": 1, "text": {"en": ', '.join(err_roles)}})
        if len(err_members) > 0:
            err.append({"class": 11702, "subclass": 1, "text": {"en": ', '.join(err_members)}})

        if outer == 0:
            err.append({"class": 11703, "subclass": 1})
        elif outer == 1 and inner == 0 and len(err_roles) == 0:
            err.append({"class": 11704, "subclass": 1})

        return err

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_Multipolygon(None)
        a.init(None)
        for m in [[{"type": "way", "role": "xxx"}],
                  [{"type": "node", "role": u"éù"}],
                  [{"type": "way", "role": "inner"}],
                  [{"type": "way", "role": "outer"}],
                  [{"type": "node", "role": "outer"}],
                  [{"type": "relation", "role": "outer"}],
                  [{"type": "way", "role": "outer"}, {"type": "node", "role": "outer"}],
                 ]:
            self.check_err(a.relation(None, {"type": "multipolygon"}, m), m)
            assert not a.relation(None, {"t": "multipolygon"}, m), m
            assert not a.relation(None, {"type": "arf"}, m), m

        for m in [[{"type": "way", "role": "outer"}] * 2,
                  [{"type": "way", "role": "outer"}] * 20,
                  [{"type": "way", "role": "outer"}] * 2 + [{"type": "way", "role": "inner"}],
                  [{"type": "way", "role": ""}] * 2 + [{"type": "way", "role": "inner"}],
                 ]:
            assert not a.relation(None, {"type": "multipolygon"}, m), m
