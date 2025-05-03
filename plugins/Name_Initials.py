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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from plugins.modules.name_suggestion_index import whitelist_from_nsi
import re


class Name_Initials(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[902] = self.def_class(item = 5010, level = 3, tags = ['name', 'fix:chair'],
            title = T_('Initial stuck to the name'))

        self.ReInitColleNom  = re.compile(r"^(.*[A-Z]\.)([A-Z][a-z].*)$")

        self.whitelist = []
        if "country" in self.father.config.options:
            country = self.father.config.options.get("country")
            self.whitelist = list(filter(lambda name: "." in name.replace(". ", ""), whitelist_from_nsi(country)))

    def node(self, data, tags):
        if "name" in tags:
            name = tags["name"]
            r = self.ReInitColleNom.match(name)
            if r and not any(map(lambda whitelist: whitelist in name, self.whitelist)):
                return {"class":902, "subclass": 0, "text":{"en":tags["name"]}, "fix":{"name": "{0} {1}".format(r.group(1), r.group(2))}}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_Initials(None)
        class _config:
            options = {"country": "NL"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        self.check_err(a.node(None, {"name": "A.Bsuaeuae"}))
        self.check_err(a.way(None, {"name": "C.Dkuaeu"}, None))
        assert not a.relation(None, {"name": "E. Fiuaeuie"}, None)
        assert not a.node(None, {"name": "G.H."})
        assert not a.node(None, {"name": "GeHaueue"})
        assert not a.node(None, {"name": "Station Service E.Leclerc"}) # NSI-whitelisted (global)
        assert not a.node(None, {"name": "Station Service E.Leclerc Paris"}) # NSI-whitelisted with suffix
