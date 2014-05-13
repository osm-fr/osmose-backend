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
        self.errors[101] = { "item": 4020, "level": 2, "tag": ["highway", "roundabout", "fix:chair"], "desc": T_(u"Unneeded tag on junction=roundabout") }
        self.no_ref_on_junction = self.father.config.options.get("no_ref_on_junction")

    def way(self, data, tags, nds):
        if u"junction" not in tags or tags["junction"] != "roundabout":
            return
        err = []
        if u"oneway" in tags:
            err.append((101, 0, {"fr": u"Tag oneway inutile", "en": u"Unecessary tag oneway", "fix": {"-": ["oneway"]}}))
        if self.no_ref_on_junction and u"ref" in tags:
            err.append((101, 1, {"fr": u"Ne doit pas contenir de tag ref=%s" % tags[u"ref"], "en": u"Should not contains tag ref=%s" % tags[u"ref"], "fix": {"-": ["ref"]} }))
        return err


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_Roundabout(None)
        class _config:
            options = {"no_ref_on_junction": True}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert not a.way(None, {"junction": "roundabout"}, None)
        self.check_err(a.way(None, {"junction": "roundabout", "ref": "1"}, None))
