#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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


class Name_Local_JP(Plugin):

    only_for = ["JA"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[50604] = { "item": 5060, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Default and local language name not the same") }
        self.errors[50605] = { "item": 5060, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Local language name without default name") }
        self.errors[50606] = { "item": 5060, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Language name without default name") }

        self.LocalName = re.compile("^name:[a-z][a-z](_.*$|$)")

    def node(self, data, tags):
        if "boundary" in tags:
            return

        default = tags.get("name")
        ja = tags.get("name:ja")
        en = tags.get("name:en")

        if default or ja or en:
            if default:
                if (ja or en) and not (default == ja or default == en or (ja and en and default == u"%s (%s)" % (ja, en))):
                    return {"class": 50604, "subclass": 0}
            elif (ja or en):
                return {"class": 50605, "subclass": 0, "fix": [{"+": {"name": ja}}, {"+": {"name": en}}]}
        else:
            locales = map(lambda y: [{"+": {"name": tags[y]}}], filter(lambda x: self.LocalName.match(x), tags.keys()))
            if locales:
                return {"class": 50606, "subclass":0, "fix": locales}

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_ja(self):
        a = Name_Local_JP(None)
        class _config:
            options = {"country": "JP"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert a.node(None, {"name": u"沖浦 (Okiura)", "name:ja": u"沖浦"})
        assert a.node(None, {"name": u"セブン−イレブン東城川東店", "name:ja": u"セブン-イレブン", "name:en": u"Seven-Eleven"})
        assert a.node(None, {"name:ja": u"沖浦"})
        assert a.node(None, {"name:it": u"Plop"})
        assert not a.node(None, {"name": u"広島県道75号三原竹原線 (Route Mihara Takehara)", "name:ja": u"広島県道75号三原竹原線", "name:en": u"Route Mihara Takehara"})
        assert not a.node(None, {"name": u"ENEOS", "name:ja": u"エネオス", "name:en": u"ENEOS"})
        assert not a.node(None, {"name": u"沖浦", "name:ja": u"沖浦"})
        assert not a.node(None, {"name": u"沖浦"})
