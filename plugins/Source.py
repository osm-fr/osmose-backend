#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
## Copyrights Frédéric Rodrigo 2011-2014                                 ##
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


class Source(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[706] = { "item": 3020, "level": 1, "tag": ["source", "fix:chair"], "desc": T_(u"Illegal or incomplete source tag") }
        self.errors[707] = { "item": 2040, "level": 3, "tag": ["source", "fix:chair"], "desc": T_(u"Missing source tag") }

    def check(self, tags):
        source = tags[u"source"].lower()
        if u"google" in source:
            return [(706,2,{"en":u"Google"})]

    def node(self, data, tags):
        if u"source" not in tags:
            return
        return self.check(tags)

    def way(self, data, tags, nds):
        if u"source" not in tags:
            return
        return self.check(tags)

    def relation(self, data, tags, members):
        if u"source" not in tags:
            return
        return self.check(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Source(None)
        a.init(None)
        for d in [{u"source":u"Free"},
                 ]:
            assert not a.node(None, d), d

        for d in [{u"source":u"google maps"}]:
             self.check_err(a.node(None, d), d)
