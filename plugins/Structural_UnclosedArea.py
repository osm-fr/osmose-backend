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

class Structural_UnclosedArea(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[1100] = { "item": 1100, "level": 3, "tag": ["geom", "fix:imagery"], "desc": T_(u"Unclosed area") }

    def way(self, data, tags, nds):
        if "area" not in tags or tags["area"] == "no":
            return

        if nds[0] != nds[-1]:
            return {"class": 1100}

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_UnclosedArea(None)
        a.init(None)
        for n in [[1, 2, 3, 4],
                  [1, 4, 1, 2],
                  [1] * 10 + [2],
                 ]:
            self.check_err(a.way(None, {"area": "yes"}, n), n)
            self.check_err(a.way(None, {"area": "farm"}, n), n)
            assert not a.way(None, {"oneway": "no"}, n), n
            assert not a.way(None, {"area": "no"}, n), n

        for n in [[1, 2, 3, 4, 1],
                  [1, 4, 1, 2, 1],
                  [1] * 10 + [2] * 10 + [1],
                 ]:
            assert not a.way(None, {"area": "yes"}, n), n
