#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015                                      ##
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


class Name_Multilingual(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        language = self.father.config.options.get("language")
        if not(language and len(language) == 2 and self.father.config.options.get("multilingual-style")):
            return False

        self.errors[50604] = {"item": 5060, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Multilingual not matching") }
        self.errors[50605] = {"item": 5060, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Multilingual missing detailed name") }
        self.errors[50606] = {"item": 5060, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Multilingual missing main name") }
        self.lang = lang = self.father.config.options.get("language")
        style = self.father.config.options.get("multilingual-style")
        self.present = lambda tags: tags.get("name:" + lang[0]) and tags.get("name:" + lang[1])
        if style == "be":
            self.aggregator = lambda tags: (
              tags.get("name:"+lang[0]) + " - " + tags.get("name:"+lang[1]),
              tags.get("name:"+lang[1]) + " - " + tags.get("name:"+lang[0]),
            )
            self.split = self.split_be
        elif style == "ma":
            self.aggregator = lambda tags: (
              tags.get("name:"+lang[0]) + " " + tags.get("name:"+lang[1]),
              tags.get("name:"+lang[1]) + " " + tags.get("name:"+lang[0]),
            )
            self.split = self.split_ma

    def node(self, data, tags):
        err = []

        p = self.present(tags)
        if tags.get("name"):
            s = self.split(tags)
            if p:
                a = self.aggregator(tags)
                if tags.get("name") not in a:
                    if s:
                        err.append((50604, 0, {"fix": s + [{"name": a[0]}]}))
                    else:
                        err.append((50604, 0, {}))
            else:
                if s:
                    err.append((50605, 0, {"fix": s}))
        else:
            if p:
                a = self.aggregator(tags)
                err.append((50606, 0, {"fix": a[0]}))

        return err


    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

    def split_be(self, tags):
        s = tags.get("name").split(' - ')
        if len(s) == 2:
            return [
                {"name:" + self.lang[0]: s[0], "name:" + self.lang[1]: s[1]},
                {"name:" + self.lang[0]: s[1], "name:" + self.lang[1]: s[0]},
            ]

    def split_ma(self, tags):
        name = tags.get("name")
        min_latin = max_latin = False
        min_arabic = max_arabic = False
        i = 0
        for c in name:
            if not re.match('[\W0-9]', c, flags=re.UNICODE):
                o = ord(c)
                if (0x0600 <= o and o <= 0x06FF) or (0x0750 <= o and o <= 0x077F) or (0x08A0 <= o and o <= 0x08FF) or (0xFB50 <= o and o <= 0xFDFF) or (0xFE70 <= o and o <= 0xFEFF) or (0x10E60 <= o and o <= 0x10E7F) or (0x1EE00 <= o and o <= 0x1EEFF):
                    if min_arabic == False:
                        min_arabic = i
                    max_arabic = i
                else:
                    if min_latin == False:
                        min_latin = i
                    max_latin = i
            i += 1
        if min_latin == False:
            return [{"name:ar": name}]
        elif min_arabic == False:
            return [{"name:fr": name}]
        else:
            if max_latin <= min_arabic:
                return [{"name:fr": name[0:min_arabic - 1].strip(), "name:ar": name[min_arabic:].strip()}]
            elif max_arabic <= min_latin:
                return [{"name:ar": name[0:min_latin - 1].strip(), "name:ar": name[min_latin:].strip()}]


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Multilingual(None)
        class _config:
            options = {}
        class father:
            config = _config()
        self.p.father = father()
        assert False == self.p.init(None)

    def test_be(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Multilingual(None)
        class _config:
            options = {"language": ["fr", "nl"], "multilingual-style": "be"}
        class father:
            config = _config()
        self.p.father = father()
        self.p.init(None)

        e = self.p.node(None, {"name": u"a - b", "name:fr": u"fr", "name:nl": u"nl"})
        assert 50604 == e[0][0]
        self.check_err(e)

        e = self.p.node(None, {"name": u"fr - nl"})
        assert 50605 == e[0][0]
        self.check_err(e)

        e = self.p.node(None, {"name:fr": u"fr", "name:nl": u"nl"})
        assert 50606 == e[0][0]
        self.check_err(e)

        assert not self.p.way(None, {"name": u"fr - nl", "name:fr": u"fr", "name:nl": u"nl"}, None)
        assert not self.p.way(None, {"name": u"nl - fr", "name:fr": u"fr", "name:nl": u"nl"}, None)

    def test_ma(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Multilingual(None)
        class _config:
            options = {"language": ["fr", "ar"], "multilingual-style": "ma"}
        class father:
            config = _config()
        self.p.father = father()
        self.p.init(None)

        e = self.p.node(None, {"name": u"Troch", "name:fr": u"Kasbat Troch", "name:ar": u"قصبة الطرش"})
        assert 50604 == e[0][0]
        self.check_err(e)

        e = self.p.node(None, {"name": u"Kasbat Troch قصبة الطرش"})
        assert 50605 == e[0][0]
        self.check_err(e)

        e = self.p.node(None, {"name:fr": u"Kasbat Troch", "name:ar": u"قصبة الطرش"})
        assert 50606 == e[0][0]
        self.check_err(e)

        assert not self.p.way(None, {"name": u"Kasbat Troch قصبة الطرش", "name:fr": u"Kasbat Troch", "name:ar": u"قصبة الطرش"}, None)
