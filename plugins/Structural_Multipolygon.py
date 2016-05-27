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


class Structural_Multipolygon(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[11701] = { "item": 1170, "level": 2, "tag": ["relation", "multipolygon", "fix:chair"], "desc": T_(u"Inadequate role for multipolygon") }
        self.errors[11702] = { "item": 1170, "level": 2, "tag": ["relation", "multipolygon", "fix:chair"], "desc": T_(u"Inadequate member for multipolygon") }
        self.errors[11703] = { "item": 1170, "level": 1, "tag": ["relation", "multipolygon", "fix:imagery"], "desc": T_(u"Missing outer role for multipolygon") }
        self.errors[11704] = { "item": 1170, "level": 3, "tag": ["relation", "multipolygon", "fix:chair"], "desc": T_(u"This multipolygon is a simple polygon") }

    def relation(self, data, tags, members):
        if tags.get('type') != 'multipolygon':
            return

        outer = 0
        inner = 0
        err = []
        for member in members:
            if member['type'] == 'way':
                if member['role'] not in ('', 'outer', 'inner'):
                    err.append((11701, 1, {"en": member['role']}))
                if member['role'] in ('', 'outer'):
                    outer += 1
                elif member['role'] == 'inner':
                    inner += 1
            else:
                err.append((11702, 1, {"en": "%s - %s" %(member['type'], member['role'])}))

        if outer == 0:
            err.append((11703, 1, {}))
        elif outer == 1 and inner == 0:
            err.append((11704, 1, {}))

        return err

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_Multipolygon(None)
        a.init(None)
        for m in [[{"type": "way", "role": "xxx"}],
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
