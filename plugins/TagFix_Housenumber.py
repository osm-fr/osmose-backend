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
        self.errors[14] = { "item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"On interpolation addr:* go to object with addr:housenumber") }
        self.errors[15] = { "item": 2060, "level": 3, "tag": ["addr", "fix:chair"], "desc": T_(u"Invalid addr:interpolation value") }

    def node(self, data, tags):
        err = []
        if "addr:housenumber" in tags and (len(tags["addr:housenumber"]) == 0 or not tags["addr:housenumber"][0].isdigit()):
            err.append((10, 1, {}))

        return err

    def way(self, data, tags, nds):
        err = self.node(data, tags)
        interpolation = tags.get("addr:interpolation")
        if interpolation:
            if len(filter(lambda x: x.startswith("addr:") and x != "addr:interpolation", tags.keys())) > 0:
                err.append((14, 1, {}))
            if interpolation not in ('even', 'odd', 'all', 'alphabetic') and not interpolation.isdigit():
                err.append((15, 1, {}))

        return err

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
        assert not a.relation(None, {"addr:housenumber": "33"}, None)

        assert a.node(None, {"addr:housenumber": ""})
        assert a.node(None, {"addr:housenumber": "?"})
        assert a.relation(None, {"addr:housenumber": "?"}, None)


        assert a.way(None, {"addr:stret": "Lomlim", "addr:interpolation": "even"}, None)
        assert not a.way(None, {"addr:interpolation": "even"}, None)
        assert not a.way(None, {"addr:interpolation": "4"}, None)
        assert a.way(None, {"addr:interpolation": "invalid"}, None)
