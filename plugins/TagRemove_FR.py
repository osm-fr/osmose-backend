#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2012                                      ##
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


class TagRemove_FR(Plugin):

    only_for = ["FR", "NC"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[41001] = { "item": 4100, "level": 3, "tag": ["tag", "fix:chair"], "desc": T_(u"Misused tag in this country") }

    def node(self, data, tags):
        if "designation" in tags:
            return [(41001, 1,{"en": "designation=*"})]
        if "highway" in tags and tags["highway"] == "emergency_access_point":
            return [(41001, 2, {"en": "highway=emergency_access_point"})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_FR(None)
        a.init(None)
        assert not a.way(None, {"highway": "trunk"}, None)
        self.check_err(a.node(None, {"designation": "yes", "highway": "primary"}))
        self.check_err(a.way(None, {"designation": "yes", "highway": "primary"}, None))
        self.check_err(a.relation(None, {"designation": "yes", "highway": "primary"}, None))
        self.check_err(a.way(None, {"highway": "emergency_access_point", "name": "toto"}, None))
