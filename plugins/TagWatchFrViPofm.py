#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
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
from modules.downloader import urlread
from modules.Stablehash import stablehash
import re
from collections import defaultdict


class TagWatchFrViPofm(Plugin):

    def quoted(self, string):
        return len(string) >= 2 and string[0] == u"`" and string[-1] == u"`"

    def quoted2re(self, string):
        return re.compile(u"^"+string[1:-1]+u"$")

    def init(self, logger):
        Plugin.init(self, logger)

        country = self.father.config.options.get("country") if self.father else None
        language = self.father.config.options.get("language") if self.father else None
        if isinstance(language, list):
            language = None

        self._update_ks = {}
        self._update_kr = {}
        self._update_ks_vs = defaultdict(dict)
        self._update_kr_vs = defaultdict(dict)
        self._update_ks_vr = defaultdict(dict)
        self._update_kr_vr = defaultdict(dict)

        reline = re.compile("^\|([^|]*)\|\|([^|]*)\|\|([^|]*)\|\|([^|]*).*")

        # récupération des infos depuis https://wiki.openstreetmap.org/index.php?title=User:FrViPofm/TagwatchCleaner
        data = urlread(u"https://wiki.openstreetmap.org/index.php?title=User:FrViPofm/TagwatchCleaner&action=raw", 1)
        data = data.split("\n")
        for line in data:
            for res in reline.findall(line):
                only_for = res[3].strip()
                if only_for in (None, '', country, language) or (country and country.startswith(only_for)):
                    r = res[1].strip()
                    c0 = res[2].strip()
                    tags = ["fix:chair"] if c0 == "" else [c0, "fix:chair"]
                    c = stablehash(c0)
                    self.errors[c] = { "item": 3030, "level": 2, "tag": tags, "desc": {"en": c0} }
                    if u"=" in res[0]:
                        k = res[0].split(u"=")[0].strip()
                        v = res[0].split(u"=")[1].strip()
                        if self.quoted(k):
                            k = self.quoted2re(k)
                            if self.quoted(v):
                                self._update_kr_vr[k][self.quoted2re(v)] = [r, c]
                            else:
                                self._update_kr_vs[k][v] = [r, c]
                        else:
                            if self.quoted(v):
                                self._update_ks_vr[k][self.quoted2re(v)] = [r, c]
                            else:
                                self._update_ks_vs[k][v] = [r, c]
                    else:
                        if self.quoted(res[0]):
                            self._update_kr[self.quoted2re(res[0])] = [r, c]
                        else:
                            self._update_ks[res[0]] = [r, c]

    def node(self, data, tags):
        err = []
        for k in tags:
            if k in self._update_ks:
                err.append({"class": self._update_ks[k][1], "subclass": stablehash(u"%s|%s" % (self._update_ks, k)), "text": T_f(u"tag key: {0} => {1} (rule ks)", k, self._update_ks[k][0])})
            if k in self._update_ks_vs and tags[k] in self._update_ks_vs[k]:
                err.append({"class": self._update_ks_vs[k][tags[k]][1], "subclass": stablehash(u"%s|%s" % (self._update_ks, k)), "text": T_f(u"tag value: {0}={1} => {2} (rule ks_vs)", k, tags[k],self._update_ks_vs[k][tags[k]][0])})
            if k in self._update_ks_vr:
                for v in self._update_ks_vr[k]:
                    if v.match(tags[k]):
                        err.append({"class": self._update_ks_vr[k][v][1], "subclass": stablehash(u"%s|%s" % (self._update_ks_vr, k)), "text": T_f(u"tag value: {0}={1} => {2} (rule ks_vr)", k, tags[k],self._update_ks_vr[k][v][0])})

        for kk in tags:
            for k in self._update_kr:
                if k.match(kk):
                    err.append({"class": self._update_kr[k][1], "subclass": stablehash(u"%s|%s" % (kk, k)), "text": T_f(u"tag key: {0} => {1} (rule kr)", kk, self._update_kr[k][0])})
            for k in self._update_kr_vs:
                if k.match(kk):
                    if tags[kk] in self._update_kr_vs[k]:
                        err.append({"class": self._update_kr_vs[k][tags[kk]][1], "subclass": stablehash(u"%s|%s" % (kk, k)), "text": T_f(u"tag value: {0}={1} => {2} (rule kr_vs)", kk, tags[kk], self._update_kr_vs[k][tags[kk]][0])})
            for k in self._update_kr_vr:
                if k.match(kk):
                    for v in self._update_kr_vr[k]:
                        if v.match(tags[kk]):
                            err.append({"class": self._update_kr_vr[k][v][1], "zsubclass": stablehash(u"%s|%s" % (kk, k)), "text": T_f(u"tag value: {0}={1} => {2} (rule ks_vr)", kk, tags[kk], self._update_kr_vr[k][v][0])})
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagWatchFrViPofm(None)
        class _config:
            options = {}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        self.check_err(a.node(None, {"aera": "plop"}))
        self.check_err(a.way(None, {"aera": "plop"}, None))
        self.check_err(a.relation(None, {"aera": "plop"}, None))
        self.check_err(a.node(None, {"administrative": "boundary"}))
        self.check_err(a.node(None, {"name": "FIXME"}))
        self.check_err(a.node(None, {"trafic_calming ": "yes"}))
        self.check_err(a.node(None, {"Fixme": "yes"}))
        self.check_err(a.node(None, {"voltage": "10kV"}))
        assert not a.node(None, {"area": "plop"})
        assert not a.node(None, {"boundary": "administrative"})
        assert not a.node(None, {"name": "Belleville"})
        assert not a.node(None, {"traffic_calming ": "yes"})

    def test_only_for_none(self):
        a = TagWatchFrViPofm(None)
        class _config:
            options = {}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        self.check_err(a.node(None, {"aera": "plop"}))               # No only_for
        self.check_err(a.node(None, {"administrative": "boundary"})) # No only_for
        assert not a.node(None, {"School:FR": "plop"})   # only_for FR
        assert not a.node(None, {"amenity": "Chapelle"}) # only for fr
        assert not a.node(None, {"amenity": u"Collège"}) # only_for fr


    def test_only_for_FR(self):
        a = TagWatchFrViPofm(None)
        class _config:
            options = {"country": "FR"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        self.check_err(a.node(None, {"aera": "plop"}))               # No only_for
        self.check_err(a.node(None, {"administrative": "boundary"})) # No only_for
        self.check_err(a.node(None, {"School:FR": "plop"})) # only_for FR
        assert not a.node(None, {"amenity": "Chapelle"})    # only for fr
        assert not a.node(None, {"amenity": u"Collège"})    # only_for fr

    def test_only_for_fr(self):
        a = TagWatchFrViPofm(None)
        class _config:
            options = {"language": "fr"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        self.check_err(a.node(None, {"aera": "plop"}))               # No only_for
        self.check_err(a.node(None, {"administrative": "boundary"})) # No only_for
        assert not a.node(None, {"School:FR": "plop"})        # only_for FR
        self.check_err(a.node(None, {"amenity": "Chapelle"})) # only for fr
        self.check_err(a.node(None, {"amenity": u"Collège"})) # only_for fr
