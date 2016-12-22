#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Yoann Arnaud <yarnaud@crans.org> 2009                      ##
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


class TagRemove_Roundabout(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[101] = { "item": 4020, "level": 3, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Unneeded tag on junction=roundabout") }

    def way(self, data, tags, nds):
        if tags.get("junction") != "roundabout":
            return
        err = []
        if u"oneway" in tags:
            err.append({"class": 101, "subclass": 0, "text": T_(u"Unnecessary tag oneway"),
                       "fix": {"-": ["oneway"]}})
        return err


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_Roundabout(None)
        a.init(None)
        assert not a.way(None, {"junction": "roundabout"}, None)
        assert not a.way(None, {"junction": "yes", "oneway": "true"}, None)
        self.check_err(a.way(None, {"junction": "roundabout", "oneway": "true"}, None))
