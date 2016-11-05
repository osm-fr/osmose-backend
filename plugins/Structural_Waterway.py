#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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

class Structural_Waterway(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[12200] = { "item": 1220, "level": 2, "tag": ["geom", "waterway", "fix:imagery"], "desc": T_(u"Closed waterway") }

    def way(self, data, tags, nds):
        if "waterway" not in tags or tags["waterway"] in ("riverbank", "dock", "dam", "boatyard", "lock", "reflecting_pool", "offshore_field"):
            return

        if nds[0] == nds[-1]:
            return {"class": 12200}

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_Waterway(None)
        a.init(None)
        for n in [[1, 2, 3, 4, 1],
                  [1, 4, 1, 2, 1],
                  [1] * 10 + [2] * 10 + [1],
                 ]:
            self.check_err(a.way(None, {"waterway": "river"}, n), n)
            self.check_err(a.way(None, {"waterway": "stream"}, n), n)
            assert not a.way(None, {"oneway": "no"}, n), n
            assert not a.way(None, {"waterway": "dock"}, n), n

        for n in [[1, 2, 3, 4],
                  [1, 4, 1, 2],
                  [1] * 10 + [2],
                 ]:
            assert not a.way(None, {"waterway": "river"}, n), n
