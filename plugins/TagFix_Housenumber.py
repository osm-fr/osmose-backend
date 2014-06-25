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


class TagFix_Housenumber(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[10] = { "item": 2060, "level": 3, "tag": ["addr", "fix:survey"], "desc": T_(u"addr:housenumber does not start by a number") }

    def node(self, data, tags):
        if "addr:housenumber" in tags and (len(tags["addr:housenumber"]) == 0 or not tags["addr:housenumber"][0].isdigit()):
            return [(10, 1, {})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Housenumber(None)
        a.init(None)

        assert not a.node(None, {})
        assert not a.node(None, {"addr:housenumber": "33"})

        assert a.node(None, {"addr:housenumber": ""})
        assert a.node(None, {"addr:housenumber": "?"})
