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


class TagFix_MultipleTag_Lang_es(Plugin):

    only_for = ["es"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30326] = self.def_class(item = 3032, level = 1, tags = ['tag', 'fix:chair'],
            title = T_('Watch multiple tags'))

        import re
        self.Panaderia = re.compile(u"panader.a (.*)", re.IGNORECASE)

    def node(self, data, tags):
        err = []

        if not "name" in tags:
            return err

        if not "shop" in tags:
            panaderia = self.Panaderia.match(tags["name"])
            if panaderia:
                err.append({"class": 30326, "subclass": 0, "fix": {"+": {"shop": "bakery"}, "~": {"name": panaderia.group(1)} }})

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_MultipleTag_Lang_es(None)
        class _config:
            options = {"language": "es"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        for t in [{"name": u"Panadería Doña Neli"},
                 ]:
            self.check_err(a.node(None, t), t)

        for t in [{"name": u"Panadería Doña Neli", "shop": "b"},
                 ]:
            assert not a.way(None, t, None), t
