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
#from plugins.Plugin import Plugin
from Plugin import Plugin

class TagACorriger_DuplicateValue(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3060] = { "item": 3060, "desc": {"en": u"Twice similar values", "fr": u"Valeur similaire en double"} }
        self.BlackList = set(('ref', 'old_ref', 'int_ref', 'created_by', 'CLC:id', 'opening_hours', 'phone', 'url', 'AND_a_nosr_r', 'AND_nosr_r'))
        import re
        self.BlackListRegex = set((re.compile('seamark:.+:colour'),))

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
        keys = set(keys) - self.BlackList
        for k in keys:
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
                vs_long = filter(lambda w: len(w) > 6, vs)
                for v1,v2 in itertools.combinations(vs_long, 2):
                    if abs(len(v1)-len(v2)) < 4 and self.levenshtein(v1, v2) < 4:
                        err.append((3060, 0, {"fr": "Valeur similaire en double %s=%s" % (k, tags[k]), "en": "Twice similar values %s=%s" % (k, tags[k])}))
                vs_short = filter(lambda w: len(w) <= 6, vs)
                if len(vs_short) != len(set(vs_short)):
                    err.append((3060, 4, {"fr": "Valeur double %s=%s" % (k, tags[k]), "en": "Twice values %s=%s" % (k, tags[k])}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
