#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jocelyn Jaubert 2013                                       ##
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


class Structural_WayOneNode(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[12401] = { "item": 1240, "level": 2, "tag": ["geom", "fix:chair"], "desc": T_(u"Way with one node") }

    def way(self, data, tags, nds):
        if len(nds) == 1:
            return {"class": 12401}

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_WayOneNode(None)
        a.init(None)
        for n in [[1],
                  [2],
                 ]:
            self.check_err(a.way(None, {}, n), n)

        for n in [[1, 2],
                  [1, 4, 1, 2],
                  [1] * 10 + [2],
                 ]:
            assert not a.way(None, {}, n), n
