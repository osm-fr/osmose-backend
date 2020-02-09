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
    def deprecated_list(self):
        wikiRoot = 'https://wiki.openstreetmap.org/wiki'
        data = urlread(wikiRoot + '/Template:Deprecated_features?action=raw', 1)

        # Tidy data up for processing
        # Eliminate wiki bold formatting
        data = data.replace("'''", "")

        # Remove HTML newlines
        data = re.sub(r'<br\s*/>', ' ', data)

        # Remove excess whitespace (also removes all newlines)
        data = " ".join(data.split())

        # Eliminate any whitespace around pipe characters
        # This makes reading the template parameters simple
        data = re.sub(r'\s?\|\s?', '|', data)

        # Eliminate templates to prevent unexpected pipe characters
        data = re.sub(r'{{{\s?lang\s?\|?\s?}}}', '', data, flags=re.I)
        # Tag template can take one or two params, with trailing | possible
        data = re.sub(
            r'{{Tag\s?\|(.+?)\|?\s?}}',
            lambda x : '`{}`'.format(x[1].replace("|", "=")),
            data,
            flags=re.I
        )

        # Resolve interwiki links now
        data = re.sub(
            r'\[\[(.+?)\]\]',
            lambda x : '[{}]({}/{})'.format(x[1], wikiRoot, x[1].replace(" ", "_")),
            data
        )

        deprecated = {}
        for feature in data.split(r'{{Deprecated features/item')[1:]:
            src_key, src_val, dest = None, None, None
            for param in feature.split('|'):
                if '=' not in param:
                    continue

                k, v = param.split('=', 1)
                # k will always start with the param because we removed whitespace around | earlier
                # We don't use == because there could be space before the = character
                if (k.startswith('dkey')):
                    src_key = v
                elif (k.startswith('dvalue')):
                    src_val = v
                elif (k.startswith('suggestion')):
                    dest = v

            # Sanity check in case formatting changes or something
            if any((src_key, src_val, dest)):
                deprecated.setdefault(src_key, {})[src_val] = dest

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
