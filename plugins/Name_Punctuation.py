#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2018                                      ##
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


class Name_Punctuation(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[50705] = self.def_class(item = 5070, level = 2, tags = ['name', 'fix:chair'],
            title = T_('Unexpected punctuation in name'))

    def node(self, data, tags):
        if 'name' not in tags:
            return

        for q in [u"?", u"¿", u"؟", u"՞", u";", u"？", u"፧", u"꘏"]:
            if q in tags["name"]:
                return [{"class": 50705, "subclass": 0, "text": T_f("Unexpected character: `{0}`", q)}]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Punctuation(None)
        self.p.init(None)

        assert not self.p.node(None, {"foo": u"bar"})
        assert self.p.node(None, {"name": u"here ?"})
