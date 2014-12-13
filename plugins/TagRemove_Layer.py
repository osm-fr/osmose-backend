#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2014                                      ##
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


class TagRemove_Layer(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[41101] = {"item": 4110, "level": 3, "tag": ["landuse", "fix:chair"], "desc": T_(u"Landuse feature not on ground") }
        self.errors[41102] = {"item": 4110, "level": 3, "tag": ["natural", "fix:chair"], "desc": T_(u"Natural feature underground") }

    def way(self, data, tags, nds):
        if tags.get(u"layer"):
            if tags.get(u"layer") != "0" and tags.get(u"landuse"):
                return [{"class": 41101, "subclass": 0}]
            elif tags.get(u"natural") and tags.get(u"layer")[0] == '-':
                return [{"class": 41102, "subclass": 0}]


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_Layer(None)
        a.init(None)
        assert not a.way(None, {"layer": "-1"}, None)
        self.check_err(a.way(None, {"layer": "-1", "landuse": "forest"}, None))
        assert not a.way(None, {"layer": "1", "natural": "water"}, None)
        self.check_err(a.way(None, {"layer": "-1", "natural": "water"}, None))
