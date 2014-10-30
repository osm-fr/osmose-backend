#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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


class Structural_DuplicateNodes(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[103] = { "item": 1010, "level": 2, "tag": ["geom", "fix:chair"], "desc": T_(u"Duplicated nodes") }

    def way(self, data, tags, nds):
        if len(nds) > len(set(nds))+2:
            rep = []
            for n in set(nds):
                if nds.count(n) > 1:
                    rep.append(u"nœud #" + str(n) + u" x " + str(nds.count(n)))
            return [(103, 0, {"en": u", ".join(rep)})]

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_DuplicateNodes(None)
        a.init(None)
        for nds in [[1, 2],
                    [2, 4, 189, 100909, 3898932],
                    [2^32, 4, 189, 100909, 3898932, 0, 2^32-1],
                    [1, 2, 1, 1],
                    [1, 1, 1],
                    [1, 1],
                   ]:
            assert not a.way(None, {}, nds), nds

        for nds in [[1, 2, 1, 1, 2],
                    [2, 4, 189, 100909, 3898932, 100909, 189, 189],
                    [2**32, 4, 4, 4, 4, 4, 4, 189, 100909, 3898932, 0, 2**32-1],
                    [2**32, 2**32, 0, 0, 2**60, 2**60],
                   ]:
            self.check_err(a.way(None, {}, nds), nds)

