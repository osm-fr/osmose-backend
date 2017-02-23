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


class Source(Plugin):

    not_for = ["HT"] # Google made drone imagery for after-earthquake in Haiti

    def init(self, logger):
        Plugin.init(self, logger)
        if self.father.config.options.get("project") != 'openstreetmap':
            return False
        self.errors[706] = { "item": 3020, "level": 1, "tag": ["source", "fix:chair"], "desc": T_(u"Illegal or incomplete source tag") }
        self.errors[707] = { "item": 2040, "level": 3, "tag": ["source", "fix:chair"], "desc": T_(u"Missing source tag") }
        self.Country = self.father.config.options.get("country")

    def check(self, tags):
        if u"source" not in tags and u"ref" not in tags:
            return

        for tag in (u"source", u"ref"):
            if tag in tags:
                value = tags[tag].lower()
                if u"google" in value:
                    return {"class": 706, "subclass": 2, "text": {"en": u"Google %s=%s".format(tag, value)}}

    def node(self, data, tags):
        return self.check(tags)

    def way(self, data, tags, nds):
        return self.check(tags)

    def relation(self, data, tags, members):
        return self.check(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Source(None)
        class _config:
            options = {"country": "MD", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        for d in [{u"name": u"Free"},
                  {u"source": u"Free"},
                 ]:
            assert not a.node(None, d), d

        for d in [{u"source":u"google maps"}]:
             self.check_err(a.node(None, d), d)
             self.check_err(a.way(None, d, None), d)
             self.check_err(a.relation(None, d, None), d)
