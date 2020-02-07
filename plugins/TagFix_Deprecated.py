#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2012                                      ##
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


class TagFix_Deprecated(Plugin):

    def cleanWiki(self, src):
        if src is None:
            return src

        # Remove bold and newlines
        src = src.replace("'''", "").replace("<br/>", " ").replace("<br />", " ")

        # Remove excess whitespace
        return " ".join(src.split())

    def deprecated_list(self):
        wikiRoot = 'https://wiki.openstreetmap.org/wiki'
        data = urlread(f'{wikiRoot}/Template:Deprecated_features?action=raw', 1)
        data = data.split(r'{{Deprecated features/item')

        dataMult = []
        for feature in data[1:]:
            # Eliminate any whitespace around pipe characters (this also eliminates newlines)
            feature = re.sub(r'\s*\|\s*', '|', feature)

            # Eliminate templates to prevent unexpected pipe characters
            feature = re.sub(r'{{{lang\|}}}', '', feature, flags=re.I)
            # Tag template can take one or two params, with trailing | possible
            feature = re.sub(
                r'{{Tag\|(.+?)\|?}}',
                lambda x : f'`{ x[1].replace("|", "=") }`',
                feature,
                flags=re.I
            )

            # Resolve interwiki links now
            feature = re.sub(
                r'\[\[(.+?)\]\]',
                lambda x : f'[{x[1]}]({wikiRoot}/{x[1].replace(" ", "_")})',
                feature
            )

            extracted = [None, None, None]
            for param in feature.split('|'):
                if '=' not in param:
                    continue

                k, v = param.split('=', 1)
                if (k == 'dkey'):
                    extracted[0] = v
                elif (k == 'dvalue'):
                    extracted[1] = v
                elif (k == 'suggestion'):
                    extracted[2] = v

            dataMult.append(extracted)

        deprecated = {}
        for line in dataMult:
            src_key = self.cleanWiki(line[0])
            src_val = self.cleanWiki(line[1])
            dest = self.cleanWiki(line[2])
            if src_key not in deprecated:
                deprecated[src_key] = {}
            deprecated[src_key][src_val] = dest
        return deprecated

    def init(self, logger):
        Plugin.init(self, logger)
        detail = T_(
'''The tag or combination key/value is no longer used. List of deprecated
features comes from [Deprecated
features](https://wiki.openstreetmap.org/wiki/Deprecated_features)''')
        self.errors[4010] = self.def_class(item = 4010, level = 2, tags = ['deprecated', 'tag', 'fix:chair'],
            title = T_('Deprecated tag'),
            detail = detail)
        self.errors[40102] = self.def_class(item = 4010, level = 2, tags = ['deprecated', 'value', 'fix:chair'],
            title = T_('Deprecated value'),
            detail = detail)

        self.Deprecated = self.deprecated_list()
        self.DeprecatedSet = set(self.Deprecated)

    def node(self, data, tags):
        err = []
        for k in set(tags).intersection(self.DeprecatedSet):
            if None in self.Deprecated[k]:
                err.append({
                    "class": 4010,
                    "subclass": stablehash(k),
                    "text": T_f('The tag `{0}` is deprecated in favour of {1}', k, self.Deprecated[k][None])
                })
            elif tags[k] in self.Deprecated[k]:
                err.append({
                    "class": 40102,
                    "subclass": stablehash(k),
                    "text": T_f('The tag `{0}` is deprecated in favour of {1}', "=".join([k, tags[k]]), self.Deprecated[k][tags[k]])
                })
        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Deprecated(None)
        a.init(None)
        for d in [{"amenity":"ev_charging"},
                  {"highway":"incline_steep"},
                  {"power_source":"pedalier"},
                  {"highway":"ford"},
                 ]:
            self.check_err(a.node(None, d), d)
            self.check_err(a.way(None, d, None), d)
            self.check_err(a.relation(None, d, None), d)

        for d in [{"onway":"yes"},
                  {"waterway":"stream"},
                  {"highway":"primary"}]:
            assert not a.node(None, d), d
