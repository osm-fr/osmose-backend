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
import re


class Name_Local(Plugin):

    not_for = ["JP"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.Language = self.father.config.options.get("language")
        if not self.Language:
            # no language
            return False
        elif isinstance(self.Language, list):
            # more than one language
            return False # Checked by Name_Multilingual

        self.errors[50601] = self.def_class(item = 5060, level = 1, tags = ['name', 'fix:chair'],
            title = T_('Default and local language name not the same'))
        self.errors[50602] = self.def_class(item = 5060, level = 1, tags = ['name', 'fix:chair'],
            title = T_('Local language name without default name'))
        self.errors[50603] = self.def_class(item = 5060, level = 1, tags = ['name', 'fix:chair'],
            title = T_('Language name without default name'))

        self.Language = self.father.config.options.get("language")
        self.LocalName = re.compile("^name:[a-z][a-z](_.*$|$)")

    def node(self, data, tags):
        if "boundary" in tags:
            return

        if "name" in tags:
            local_name = tags.get("name:%s" % self.Language)
            if local_name and local_name != tags.get("name"):
                return {"class": 50601, "subclass": 0}
        else:
            local_name = tags.get("name:%s" % self.Language)
            if local_name:
                return {"class": 50602, "subclass": 0, "fix": {"+": {"name": local_name}}}
            else:
                locales = list(map(lambda y: [{"+": {"name": tags[y]}}], filter(lambda x: self.LocalName.match(x), tags.keys())))
                if locales:
                    return {"class": 50603, "subclass":0, "fix": locales}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_fr(self):
        a = Name_Local(None)
        class _config:
            options = {"language": "fr"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {"name": "Plop"})
        assert not a.node(None, {"name": "Plop", "name:fr": "Plop"})
        assert a.node(None, {"name": "Plop", "name:fr": "Zip"})
        assert a.node(None, {"name:fr": "Plop"})
        assert a.node(None, {"name:it": "Plop"})
        assert not a.node(None, {"name:left": "Plop"})
        assert a.node(None, {"name:zh_pinyin": "Plop"})

    def test_fr_nl(self):
        a = Name_Local(None)
        class _config:
            options = {"language": ["fr", "nl"]}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {"name": "Plop", "name:fr": "Zip"})
