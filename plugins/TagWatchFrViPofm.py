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
import urllib, re


class TagWatchFrViPofm(Plugin):
    
    err_222    = 3030
    err_222_fr = u"TagwatchCleaner par FrViPofm"
    err_222_en = u"TagwatchCleaner by FrViPofm"

    _update_ks = {}
    _update_kr = {}
    _update_ks_vs = {}
    _update_kr_vs = {}
    _update_ks_vr = {}
    _update_kr_vr = {}
    
    def init(self, logger):
                
        reline = re.compile("^\|(.*)\|\|(.*)\|\|(.*)$")
        
        # récupération des infos depuis http://wiki.openstreetmap.org/index.php?title=User:FrViPofm/TagwatchCleaner&action=raw
        data = urllib.urlopen("http://wiki.openstreetmap.org/index.php?title=User:FrViPofm/TagwatchCleaner&action=raw").read()
        data = data.split("\n")
        for line in data:
            line = line.decode("utf8")
            for res in reline.findall(line):
                if u"=" in res[0]:
                    k = res[0].split(u"=")[0].strip()
                    v = res[0].split(u"=")[1].strip()
                    r = res[1].strip()
                    if k[0]==u"`" and k[-1]==u"`":
                        k = re.compile(u"^"+k[1:-1]+u"$")
                        if v[0]==u"`" and v[-1]==u"`":
                            if k not in self._update_kr_vr:
                                self._update_kr_vr[k]={}
                            self._update_kr_vr[k][re.compile(u"^"+v[1:-1]+u"$")] = r
                        else:
                            if k not in self._update_kr_vs:
                                self._update_kr_vs[k]={}
                            self._update_kr_vs[k][v] = r
                    else:
                        if v[0]==u"`" and v[-1]==u"`":
                            if k not in self._update_ks_vr:
                                self._update_ks_vr[k]={}
                            self._update_ks_vr[k][re.compile(u"^"+v[1:-1]+u"$")] = r
                        else:
                            if k not in self._update_ks_vs:
                                self._update_ks_vs[k]={}
                            self._update_ks_vs[k][v] = r
                else:
                    if res[0][0]==u"`" and res[0][-1]==u"`":
                        self._update_kr[re.compile(u"^"+res[0][1:-1]+u"$")] = res[1]
                    else:
                        self._update_ks[res[0]] = res[1]
        
    def node(self, data, tags):
        err = []
        for k in self._update_ks:
            if k in tags:
                err.append((222, abs(hash(k.encode("utf8"))), {"en": u"tag key: %s => %s (rule ks)"%(k,self._update_ks[k])}))
        for k in self._update_kr:
            for kk in tags:
                if k.match(kk):
                    err.append((222, abs(hash(kk.encode("utf8"))), {"en": u"tag key: %s => %s (rule kr)"%(kk,self._update_kr[k])}))
        for k in self._update_ks_vs:
            if k not in tags:
                continue
            if tags[k] in self._update_ks_vs[k]:
                err.append((222, abs(hash((u"%s=%s"%(k,tags[k])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule ks_vs)"%(k,tags[k],self._update_ks_vs[k][tags[k]])}))
        for k in self._update_kr_vs:
            for kk in tags:
                if k.match(kk):
                    if tags[kk] in self._update_kr_vs[k]:
                        err.append((222, abs(hash((u"%s=%s"%(kk,tags[kk])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule kr_vs)"%(kk,tags[kk],self._update_kr_vs[k][tags[kk]])}))
        for k in self._update_ks_vr:
            if k not in tags:
                continue
            for v in self._update_ks_vr[k]:
                if v.match(tags[k]):
                    err.append((222, abs(hash((u"%s=%s"%(k,tags[k])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule ks_vr)"%(k,tags[k],self._update_ks_vr[k][v])}))
        for k in self._update_kr_vr:
            for kk in tags:
                if k.match(kk):
                    for v in self._update_kr_vr[k]:
                        if v.match(tags[kk]):
                            err.append((222, abs(hash((u"%s=%s"%(kk,tags[kk])).encode("utf8"))), {"en": u"tag value: %s=%s => %s (rule ks_vr)"%(kk,tags[kk],self._update_kr_vr[k][v])}))
        return err
    
    def way(self, data, tags, nds):
        return self.node(data, tags)
    
    def relation(self, data, tags, members):
        return self.node(data, tags)

if __name__ == "__main__":
    a = TagWatchFrViPofm()
    a.init(None)
    print a._update_ks
    print a._update_kr
    print a._update_ks_vs
    print a._update_kr_vs
    print a._update_ks_vr
    print a._update_kr_vr
