#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015-2018                                 ##
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

from __future__ import unicode_literals
from plugins.Plugin import Plugin
from modules.languages import language2scripts, gen_regex
import regex
from modules.py3 import ilen


class Name_Multilingual(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        language = self.father.config.options.get("language")
        if not(language and self.father.config.options.get("multilingual-style")):
            return False

        self.errors[50604] = {"item": 5060, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Multilingual not matching") }
        self.lang = lang = self.father.config.options.get("language")
        style = self.father.config.options.get("multilingual-style")
        self.present = lambda tags: tags.get("name:" + lang[0]) and tags.get("name:" + lang[1])
        if style == "be":
            self.aggregator = lambda tags: [
              {"name": tags["name:"+lang[0]].strip() + " - " + tags["name:"+lang[1].strip()]},
              {"name": tags["name:"+lang[1]].strip() + " - " + tags["name:"+lang[0].strip()]},
            ] if tags.get("name:"+lang[0]) and tags.get("name:"+lang[1]) and tags["name:"+lang[0]].strip() != tags["name:"+lang[1]].strip() else [{"name": tags.get("name:"+lang[0], tags.get("name:"+lang[1])).strip()}]
            self.split = self.split_be
        elif style == "xk":
            self.aggregator = lambda tags: [
              {"name": tags["name:"+lang[0]].strip()},
              {"name": tags["name:"+lang[1]].strip()},
              {"name": tags["name:"+lang[0]].strip() + " - " + tags["name:"+lang[1].strip()]},
              {"name": tags["name:"+lang[1]].strip() + " - " + tags["name:"+lang[0].strip()]},
            ] if tags.get("name:"+lang[0]) and tags.get("name:"+lang[1]) and tags["name:"+lang[0]].strip() != tags["name:"+lang[1]].strip() else [{"name": tags.get("name:"+lang[0], tags.get("name:"+lang[1])).strip()}]
            self.split = self.split_be
        elif style == "ma":
            self.aggregator = lambda tags: [
              {"name": " ".join(map(lambda a: a.strip(), filter(lambda a: a, [tags.get("name:fr"), tags.get("name:zgh", tags.get("name:ber")), tags.get("name:ar")])))}
            ]
            self.split = self.split_ma
        elif style == "dj":
            self.aggregator = lambda tags: [
              {"name": " / ".join(map(lambda a: a.strip(), filter(lambda a: a, [tags.get("name:fr"), tags.get("name:ar")])))}
            ] if tags.get("name:fr") and tags.get("name:fr")[-1] in '0123456789' else [
              {"name": " ".join(map(lambda a: a.strip(), filter(lambda a: a, [tags.get("name:fr"), tags.get("name:ar")])))}
            ]
            self.split = self.split_dj

        self.lang_regex_script = list(map(lambda l: [l, regex.compile(r"^[\p{Common}%s]+$" % gen_regex(language2scripts[l]), flags=regex.V1)], lang))

    def filter_fix_already_existing(self, names, s):
        return list(filter(
            lambda d: len(d) > 0,
            map(
                lambda z: dict(filter(
                    lambda kv: kv[1] not in names,
                    z.items()
                )),
                s
           )
        ))

    def node(self, data, tags):
        name = tags.get("name")
        names = list(map(lambda a: (a and a.strip()) or None, map(lambda a: tags.get("name:" + a), self.lang)))
        names_counts = ilen(filter(lambda a: a, names))

        if not name and names_counts == 0:
            return

        fix = []

        s = self.split(name) if name else None

        # Split: name -> name:xx
        if s:
            ss = self.filter_fix_already_existing(names, s)

            # Remove the uniq fix, if does not change an already existing tag
            if names_counts == 0:
                ss = list(filter(lambda d: len(d) > 1 or tags.get(list(d.items())[0]), ss))

            fix = fix + ss

        # Aggregate: name:xx -> name
        if names_counts > 0:
            if s:
                for z in s:
                    s_tags = dict(z, **tags)
                    a = self.aggregator(s_tags)
                    if {"name": name} not in a:
                        fix = fix + a
            else:
                a = self.aggregator(tags)
                if {"name": name} not in a:
                    fix = fix + a

        if fix:
            fix_ = []
            for f in fix:
                if f not in fix_:
                    fix_.append(f)
            return [{"class": 50604, "subclass": 0, "fix": fix_}]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

    def split_be(self, name):
        s = list(map(lambda a: a.strip(), name.split(' - ')))
        ret = []
        if len(s) == 1:
            for (lang, regex_) in self.lang_regex_script:
                if regex_.match(s[0]):
                    ret.append({"name:" + lang: s[0]})
        elif len(s) == 2:
            if self.lang_regex_script[0][1].match(s[0]) and self.lang_regex_script[1][1].match(s[1]):
                ret.append({"name:" + self.lang[0]: s[0], "name:" + self.lang[1]: s[1]})
            if self.lang_regex_script[1][1].match(s[0]) and self.lang_regex_script[0][1].match(s[1]):
                ret.append({"name:" + self.lang[0]: s[1], "name:" + self.lang[1]: s[0]})
        return ret

    char_common = regex.compile(r"[\p{Common}]", flags=regex.V1)
    char_ma = {
        'fr': regex.compile(r"[%s]" % gen_regex(language2scripts['fr']), flags=regex.V1),
        'ar': regex.compile(r"[%s]" % gen_regex(language2scripts['ar']), flags=regex.V1),
        'zgh': regex.compile(r"[%s]" % gen_regex(language2scripts['zgh']), flags=regex.V1),
    }.items()

    def split_ma(self, name):
        return self.split_diff_alphabets(name, ['ar', 'fr', 'zgh'])

    def split_dj(self, name):
        ret = self.split_diff_alphabets(name, ['ar', 'fr'])
        return list(map(lambda r:
            dict(map(lambda kv: (kv[0], kv[1].strip(' /')), r.items())),
            ret)) if ret else None

    def split_diff_alphabets(self, name, languages):
        min_max = dict(map(lambda l: [l, {'min': None, 'max': None}], languages))

        for i, c in enumerate(name):
            if not self.char_common.match(c):
                for (l, re) in self.char_ma:
                    if re.match(c):
                        if min_max[l]['min'] is None:
                            min_max[l]['min'] = i
                        min_max[l]['max'] = i

        min_max_filtered = list(filter(lambda l_mm: l_mm[1]['min'] is not None, min_max.items()))
        if len(min_max_filtered) == 0:
            return # No text detected
        min_max_sorted = sorted(min_max_filtered, key = lambda v: v[1]['min'])
        min_max_sorted_ = list(map(lambda a: [a[1]['min'], a[1]['max']], min_max_sorted))
        min_max_sorted_ = sum(min_max_sorted_, []) # Flatten the list
        if min_max_sorted_ != sorted(min_max_sorted_):
            return # Abort, there is overlap

        # Expend
        min_max_sorted[0][1]['min'] = 0
        min_max_sorted[-1][1]['max'] = len(name) - 1
        for i in range(1, len(min_max_sorted)):
            min_max_sorted[i - 1][1]['max'] = min_max_sorted[i][1]['min'] - 1

        # Split
        z = dict(map(lambda l_mm: ["name:" + l_mm[0], name[l_mm[1]['min']:l_mm[1]['max'] + 1].strip()], min_max_sorted))
        if len(z) > 0:
            return [z]

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

        assert not self.p.node(None, {"foo": u"bar"})

        e = self.p.node(None, {"name": u"a - b", "name:fr": u"fr", "name:nl": u"nl"})
        assert 4 == len(e[0]["fix"])
        self.check_err(e)

        e = self.p.node(None, {"name": u"fr - nl"})
        self.check_err(e)

        e = self.p.node(None, {"name:fr": u"fr", "name:nl": u"nl"})
        self.check_err(e)

        assert not self.p.way(None, {"name": u"fr - nl", "name:fr": u"fr", "name:nl": u"nl"}, None)
        assert not self.p.way(None, {"name": u"nl - fr", "name:fr": u"fr", "name:nl": u"nl"}, None)
        assert not self.p.way(None, {"name": u"foo", "name:fr": u"foo", "name:nl": u"foo"}, None)

        e = self.p.node(None, {"name": u"fr", "name:nl": u"nl"})
        assert 5 == len(e[0]["fix"])
        self.check_err(e)

        e = self.p.node(None, {"name:fr": u"fr", "name": u"nl"})
        assert 5 == len(e[0]["fix"])
        self.check_err(e)

        e = self.p.node(None, {"name": u"Kruidtuin", "name:nl": u"Kruidtuin", "name:fr": u"Botanique"})
        assert 2 == len(e[0]["fix"])

        e = self.p.split_be(u"(œ)")
        assert 1 == len(e)

        e = self.p.split_be(u"(í)")
        assert 1 == len(e)

        e = self.p.split_be(u"(œ) - (í)")
        assert 1 == len(e)

    def test_ma(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Multilingual(None)
        class _config:
            options = {"language": ["fr", "ar", "zgh", "ber"], "multilingual-style": "ma"}
        class father:
            config = _config()
        self.p.father = father()
        self.p.init(None)

        e = self.p.node(None, {"name": u"Troch", "name:fr": u"Kasbat Troch", "name:ar": u"قصبة الطرش"})
        self.check_err(e)

        e = self.p.node(None, {"name": u"Kasbat Troch قصبة الطرش"})
        self.check_err(e)

        e = self.p.node(None, {"name:fr": u"Kasbat Troch", "name:ar": u"قصبة الطرش"})
        self.check_err(e)

        assert not self.p.way(None, {"name": u"Kasbat Troch قصبة الطرش", "name:fr": u"Kasbat Troch", "name:ar": u"قصبة الطرش"}, None)
        assert not self.p.way(None, {"name": u"Kasbat Troch"}, None)

        e = self.p.node(None, {"name": u"Derb Al Bire", "name:ar": u"درب البير"})
        self.check_err(e)

        r = self.p.split_ma(u"Tizi n'Tichka ⵜⵉⵣⵉ ⵏ ⵜⵉⵛⴽⴰ تيزي ن تيشكا")
        assert u"Tizi n'Tichka" == r[0]["name:fr"]
        assert u"ⵜⵉⵣⵉ ⵏ ⵜⵉⵛⴽⴰ" == r[0]["name:zgh"]
        assert u"تيزي ن تيشكا" == r[0]["name:ar"]

        r = self.p.split_ma(u"Bab Atlas ⴱⴰⴱ ⴰⵟⵍⴰⵙ")
        assert u"Bab Atlas" == r[0]["name:fr"]
        assert u"ⴱⴰⴱ ⴰⵟⵍⴰⵙ" == r[0]["name:zgh"]
        assert None == r[0].get("name:ar")

        r = self.p.split_ma(u"Avenue Mohammed V 2 (Beau Gosse) شارع محمد الخامس 2")
        assert u"Avenue Mohammed V 2 (Beau Gosse)" == r[0]["name:fr"]
        assert u"شارع محمد الخامس 2" == r[0]["name:ar"]

        assert not self.p.node(None, {"name": u"Bab Atlas ⴱⴰⴱ ⴰⵟⵍⴰⵙ", "name:fr": u"Bab Atlas", "name:zgh": u"ⴱⴰⴱ ⴰⵟⵍⴰⵙ"})
        assert self.p.node(None, {"name": u"Bab Atlas ⴱⴰⴱ ⴰⵟⵍⴰⵙ", "name:fr": u"Bab PAS Atlas", "name:zgh": u"ⴱⴰⴱ ⴰⵟⵍⴰⵙ"})

        assert not self.p.node(None, {"name": u"Agdal ⴰⴳⴷⴰⵍ أگدال", "name:ar": u"أگدال", "name:zgh": u"ⴰⴳⴷⴰⵍ", "name:fr": u"Agdal "})

    def test_dj(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Multilingual(None)
        class _config:
            options = {"language": ["fr", "ar"], "multilingual-style": "dj"}
        class father:
            config = _config()
        self.p.father = father()
        self.p.init(None)

        e = self.p.node(None, {"name": u"Avenue 17 / جادة 17", "name:fr": u"Avenue", "name:ar": u"جادة"})
        self.check_err(e)

        assert not self.p.way(None, {"name": u"Avenue جادة", "name:fr": u"Avenue", "name:ar": u"جادة"}, None)
        assert not self.p.way(None, {"name": u"Avenue 17 / جادة 17", "name:fr": u"Avenue 17", "name:ar": u"جادة 17"}, None)
