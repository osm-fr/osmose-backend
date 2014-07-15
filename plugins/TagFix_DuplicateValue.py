#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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

import itertools
from plugins.Plugin import Plugin

class TagFix_DuplicateValue(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3060] = { "item": 3060, "level": 3, "tag": ["value", "fix:chair"], "desc": T_(u"Duplicated similar values") }
        self.BlackList = set(('ref', 'created_by', 'CLC:id', 'opening_hours', 'phone', 'url', 'GNS:id', 'technology', 'cables'))
        import re
        self.BlackListRegex = set((re.compile('seamark:.+:colour'), re.compile('.+_ref'), re.compile('ref:.+'), re.compile('destination:.+'), re.compile('AND_.+'), re.compile('AND:.+')))

    # http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    def levenshtein(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)
        if not s1:
            return len(s2)

        previous_row = xrange(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1 # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def node(self, data, tags):
        err = []
        keys = tags.keys()
        for k in keys:
            if k in self.BlackList:
                continue
            else:
                try:
                    for blr in self.BlackListRegex:
                        if blr.match(k):
                            raise Exception
                except Exception:
                    continue

            v = tags[k]
            if k == 'source':
                v = v.replace('Cadastre ; mise', 'Cadastre, mise')
            if ';' in v:
                vs = map(lambda w: w.strip(), v.split(';'))
                if len(vs) != len(set(vs)):
                    err.append((3060, 4, {"fr": "Valeur double %s=%s" % (k, tags[k]), "en": "Duplicated values %s=%s" % (k, tags[k]), "fix": {k: ";".join(set(vs))} }))
                else:
                    vs_long = filter(lambda w: len(w) > 6, vs)
                    for v1,v2 in itertools.combinations(vs_long, 2):
                        if abs(len(v1)-len(v2)) < 4 and self.levenshtein(v1, v2) < 4:
                            err.append((3060, 0, {"fr": "Valeur similaire en double %s=%s" % (k, tags[k]), "en": "Duplicated similar values %s=%s" % (k, tags[k])}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_DuplicateValue(None)
        a.init(None)
        t = {"ref":"E 05; E 70; E 05;E 70; E 05;E 70; E 05;E 70; E 05;E 70"}
        assert not a.node(None, t), t

        t = {"seamark:buoy_lateral:colour":"red;white;red;white"}
        assert not a.node(None, t), t

        t = {"ref:mhs":"IA00070520; IA00070492"}
        assert not a.node(None, t), t

        t = {"opening_hours": "Mo 14:00-19:00; Tu-Fr 10:00-14:00,15:00-19:00; Sa 10:00-19:00"}
        assert not a.node(None, t), t
