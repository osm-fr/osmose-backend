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
import regex


class Name_Script(Plugin):

    lang = {
      "ar": u"\p{Arabic}",
      "az": u"\p{Arabic}\p{Cyrillic}\p{Latin}",
      "bg": u"\p{Cyrillic}",
      "bn": u"\p{Bengali}",
      "ca": u"\p{Latin}",
      "cs": u"\p{Latin}",
      "da": u"\p{Latin}",
      "de": u"\p{Latin}",
      "dv": None, #Divehi
      "el": u"\p{Greek}",
      "en": u"\p{Latin}",
      "es": u"\p{Latin}",
      "et": u"\p{Latin}",
      "fa": u"\p{Arabic}",
      "fo": u"\p{Latin}",
      "fr": u"\p{Latin}",
      "hr": u"\p{Latin}",
      "hu": u"\p{Latin}",
      "hy": u"\p{Armenian}",
      "id": u"\p{Latin}",
      "is": u"\p{Latin}",
      "it": u"\p{Latin}",
      "ja": None, # u"\p{Hiragana}\p{Katakana}" and Kanji
      "ka": u"\p{Georgian}",
      "kl": u"\p{Latin}",
      "km": u"\p{Khmer}",
      "ko": u"\p{Hangul}",
      "lt": u"\p{Latin}",
      "lv": u"\p{Latin}",
      "mn": None, # Cyrillic + Manchu
      "ms": u"\p{Latin}",
      "my": None, # Birman
      "ne": u"\p{Devanagari}",
      "nl": u"\p{Latin}",
      "no": u"\p{Latin}",
      "pl": u"\p{Latin}",
      "pt": u"\p{Latin}",
      "ro": u"\p{Latin}",
      "ru": u"\p{Cyrillic}",
      "sk": u"\p{Latin}",
      "so": u"\p{Latin}",
      "sq": u"\p{Latin}",
      "sr": u"\p{Cyrillic}",
      "sv": u"\p{Latin}",
      "tg": u"\p{Arabic}\p{Cyrillic}",
      "th": u"\p{Thai}",
      "tk": u"\p{Cyrillic}\p{Latin}",
      "tr": u"\p{Latin}",
      "uk": u"\p{Cyrillic}",
      "vi": u"\p{Latin}",
      "zh": None, # Bopomofo and other
    }

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[50701] = { "item": 5070, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Value does not match language charset") }

        for l, s in self.lang.items():
            if s == None:
                del(self.lang[l])
            else:
                self.lang[l] = regex.compile(u"[\p{Common}IVXLDCM%s]" % s)

        self.name_langs = {"name:%s" % k: v for k, v in self.lang.items()}


    def node(self, data, tags):
        err = []
        for name, r in self.name_langs.items():
            if name in tags:
                s = r.sub(u"", tags[name])
                if s != "":
                    err.append((50701, 1, {"en": "\"%s\"=\"%s\" unexpected \"%s\"" % (name, tags[name], s)}))
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_Script(None)
        class _config:
            options = {"language": "fr"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {u"name:uk": u"кодувань"})
        assert not a.node(None, {u"name:tg": u"Париж"})
        self.check_err(a.node(None, {u"name:uk": u"Sacré-Cœur"}))
