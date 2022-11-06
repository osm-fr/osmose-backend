#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2011-2015                                 ##
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

import re
import itertools
from modules.Stablehash import stablehash64
from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin

class TagFix_DuplicateValue(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        doc = dict(
            detail = T_(
'''The tag contains two values (separated by ';') which are very
similar.'''),
            fix = T_(
'''Delete one value.'''),
            trap = T_(
'''In some cases all values may be required.

Ensure the interpretation of the tag does not change when you delete one item.'''))
        self.errors[3060]  = self.def_class(item = 3060, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Duplicated values'),
            **doc)
        self.errors[30601] = self.def_class(item = 3060, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Similar values'),
            resource = 'https://en.wikipedia.org/wiki/Levenshtein_distance',
            **doc)

        self.WhitelistSimilarEqual = set(( # Keys that can have similar and even equal values
            'CLC:id', 'GNS:id', 'tmc', 'tiger:cfcc', 'statscan:rbuid', 'nysgissam:nysaddresspointid',
            'ref',
            'source:date',
            'source:geometry:date', # Belgium, Flanders
            'technology',
            'cables',
            'position',
            'couplings:diameters',
            'voltage',
            'addr:flats', 'addr:housenumber', 'addr:unit', 'addr:floor', 'addr:block', 'addr:door',
            'note', 'description', 'inscription', # Text; not ;-separated values
        ))
        self.WhitelistSimilar = set(( # Keys that can have similar, but not equal values
            'source:geometry:ref', # Belgium, Flanders
            'gnis:id', 'gnis:feature_id', # USA
            'network:guid',
            'created_by',
            'is_in',
            'service_times', 'collection_times',
            'phone', 'fax', 'emergency:phone',
            'email',
            'url', 'website',
            'destination',
            'passenger',
            'healthcare:speciality',
            'traffic_sign', 'traffic_sign:forward', 'traffic_sign:backward',
            'sport',
            'communication:mobile_phone',
            'cuisine',
            'operator',
            'changing_table:location',
            'furniture',
            'seamark:berth:category',
            'seamark:restricted_area:restriction',
            'historic:period',
            'charge',
            'social_facility:for',
        ))
        self.WhitelistSimilarEqualRegex = set(( # Regexes for keys that can have similar and even equal values
            re.compile('seamark:.+:colour'),
            re.compile('.+_ref'), re.compile('ref:.+'),
            re.compile('destination:.+'),
            re.compile('AND_.+'), re.compile('AND:.+'), # Netherlands
            re.compile('[Nn][Hh][Dd]:.+'),
            re.compile('massgis:.+'),
            re.compile('lacounty:.+'),
            re.compile('turn:lanes.*'),
        ))
        self.WhitelistSimilarRegex = set(( # Regexes for keys that can have similar, but not equal values
            re.compile('.+_name'),
            re.compile('.+:conditional'),
            re.compile('.+:date'),
            re.compile('.+:colour'),
            re.compile('opening_hours(:.+)?'),
            re.compile('(.+:)?wikidata'),
            re.compile('railway:signal:.+'),
            re.compile('contact:.+'),
        ))

    # http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    def levenshtein(self, s1, s2):
        if len(s1) < len(s2):  # pragma: no cover
            return self.levenshtein(s2, s1)
        if not s1:  # pragma: no cover
            return len(s2)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1 # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def anyRegexMatch(self, set_of_regexes, key):
        for r in set_of_regexes:
            if r.match(key):
                return True
        return False

    def node(self, data, tags):
        err = []
        keys = tags.keys()

        for k in keys:
            if k in self.WhitelistSimilarEqual:
                continue # Key may have equal or similar values
            v = tags[k]
            if not ';' in v:
                continue
            if self.anyRegexMatch(self.WhitelistSimilarEqualRegex, k):
                continue # Key may have equal or similar values
            if k == 'source':
                v = v.replace('Cadastre ; mise', 'Cadastre, mise') # France
                v = v.replace('GSImaps/ort', 'GSImaps/std') # Japan
            vs = list(filter(lambda w: len(w) > 0, map(lambda w: w.strip(), v.split(';'))))

            if len(vs) != len(set(vs)):
                err.append({"class": 3060, "subclass": stablehash64(k),
                            "text": T_("Duplicated values {key}={val}", key = k, val = tags[k]),
                            "fix": {k: ";".join(set(vs))} })
            else:
                if k in self.WhitelistSimilar:
                    continue # Key may have similar values
                if self.anyRegexMatch(self.WhitelistSimilarRegex, k):
                    continue # Key may have similar values

                vs_long = filter(lambda w: len(w) > 6, vs)
                for v1,v2 in itertools.combinations(vs_long, 2):
                    if abs(len(v1)-len(v2)) < 4 and self.levenshtein(v1, v2) < 4:
                        err.append({"class": 30601, "subclass": stablehash64(k),
                                    "text": T_("Similar values {v1} and {v2} in {key}={val}", v1 = v1, v2 = v2, key = k, val = tags[k])})
                        break

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

        for t in [{"oneway":"yes;yes"},
                  {"oneway":"yes;yes;no"},
                  {"oneway":"yes;yes;yes;yes;-1;-1;no;no"},
                  {"passenger":"national;national"},
                  {"opening_hours": "Mo 14:00-19:00; Tu-Fr 10:00-14:00,15:00-19:00; Mo 14:00-19:00"},
                  {"source":u"cadastre-dgi-fr source : Direction Générale des Impôts - Cadastre ; mise à jour : 2013;cadastre-dgi-fr source : Direction Générale des Impôts - Cadastre ; mise à jour : 2013"},
                  {"source":u"cadastre-dgi-fr source : Direction Générale des Impôts - Cadastre ; mise à jour : 2010;cadastre-dgi-fr source : Direction Générale des Impôts - Cadastre ; mise à jour : 2013"},
                  {"source":"GSImaps/ort;GSImaps/std"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)
            self.check_err(a.relation(None, t, None), t)

        for t in [{"ref":"E 05; E 70; E 05;E 70; E 05;E 70; E 05;E 70; E 05;E 70"},
                  {"seamark:buoy_lateral:colour":"red;white;red;white"},
                  {"ref:mhs":"IA00070520; IA00070492"},
                  {"opening_hours": "Mo 14:00-19:00; Tu-Fr 10:00-14:00,15:00-19:00; Sa 10:00-19:00"},
                  {"oneway":"yes;no"},
                  {"passenger":"national;international;regional"},
                  {"AND_toto":"121;121;121"},
                  {"NHD:ComID":"141725410;141725411"},
                  {"massgis:OS_ID":"305-735;305-764"},
                 ]:
            assert not a.node(None, t), t
