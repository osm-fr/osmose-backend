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
import re
from collections import defaultdict


class TagWatchFrViPofm(Plugin):

    _update_ks = {}
    _update_kr = {}
    _update_ks_vs = defaultdict(dict)
    _update_kr_vs = defaultdict(dict)
    _update_ks_vr = defaultdict(dict)
    _update_kr_vr = defaultdict(dict)

    def quoted(self, string):
        return len(string)>=2 and string[0]==u"`" and string[-1]==u"`"

    def quoted2re(self, string):
        return re.compile(u"^"+string[1:-1]+u"$")

    def init(self, logger):
        Plugin.init(self, logger)

        reline = re.compile("^\|([^|]*)\|\|([^|]*)\|\|([^|]*)\|\|.*")

        # récupération des infos depuis http://wiki.openstreetmap.org/index.php?title=User:FrViPofm/TagwatchCleaner
        data = urlread("http://wiki.openstreetmap.org/index.php?title=User:FrViPofm/TagwatchCleaner&action=raw", 1)
        data = data.split("\n")
        for line in data:
            line = line.decode("utf8")
            for res in reline.findall(line):
                r = res[1].strip()
                c0 = res[2].strip()
                c = abs(hash(c0.encode("utf8")))%2147483647
                self.errors[c] = { "item": 3030, "level": 2, "tag": [c0, "fix:chair"], "desc": {"en": c0} }
                #of = res[3].strip()
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
                err.append((self._update_ks[k][1], abs(hash(k.encode("utf8"))), {"en": u"tag key: %s => %s (rule ks)"%(k,self._update_ks[k][0])}))
            if k in self._update_ks_vs and tags[k] in self._update_ks_vs[k]:
                err.append((self._update_ks_vs[k][tags[k]][1], abs(hash((u"%s=%s"%(k,tags[k])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule ks_vs)"%(k,tags[k],self._update_ks_vs[k][tags[k]][0])}))
            if k in self._update_ks_vr:
                for v in self._update_ks_vr[k]:
                    if v.match(tags[k]):
                        err.append((self._update_ks_vr[k][v][1], abs(hash((u"%s=%s"%(k,tags[k])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule ks_vr)"%(k,tags[k],self._update_ks_vr[k][v][0])}))

        for kk in tags:
            for k in self._update_kr:
                if k.match(kk):
                    err.append((self._update_kr[k][1], abs(hash(kk.encode("utf8"))), {"en": u"tag key: %s => %s (rule kr)"%(kk,self._update_kr[k][0])}))
            for k in self._update_kr_vs:
                if k.match(kk):
                    if tags[kk] in self._update_kr_vs[k]:
                        err.append((self._update_kr_vs[k][tags[kk]][1], abs(hash((u"%s=%s"%(kk,tags[kk])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule kr_vs)"%(kk,tags[kk],self._update_kr_vs[k][tags[kk]][0])}))
            for k in self._update_kr_vr:
                if k.match(kk):
                    for v in self._update_kr_vr[k]:
                        if v.match(tags[kk]):
                            err.append((self._update_kr_vr[k][v][1], abs(hash((u"%s=%s"%(kk,tags[kk])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule ks_vr)"%(kk,tags[kk],self._update_kr_vr[k][v][0])}))
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
        a.init(None)
        print a._update_ks
        print a._update_kr
        print a._update_ks_vs
        print a._update_kr_vs
        print a._update_ks_vr
        print a._update_kr_vr
        # TODO: add tests
