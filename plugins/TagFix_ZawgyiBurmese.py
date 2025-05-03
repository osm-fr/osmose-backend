#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Sascha Brawer 2025                                         ##
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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin

import myanmartools
import icu


# https://en.wikipedia.org/wiki/Zawgyi_font

class TagFix_ZawgyiBurmese(Plugin):

    only_for = ['MM']

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[50706] = self.def_class(
            item = 5070,
            level = 2,
            tags = ['value', 'fix:chair'],
            title = T_('Value contains Zawgyi-encoded Burmese characters'),
            detail = T_(
'''Tag values should be stored in Unicode. However, this
value contains Burmese characters in the obsolete “Zawgyi” font encoding.
As long as this value is stored in a non-standard way, modern devices cannot
display it correctly. Please change the text to be encoded in Unicode.'''),
        )
        self.detector = myanmartools.ZawgyiDetector()
        self.converter = icu.Transliterator.createInstance('Zawgyi-my')

    def node(self, data, tags):
        errs = []
        for key, value in tags.items():
            if not any(0x1000 <= ord(c) <= 0x109F for c in value):
                continue
            score = self.detector.get_zawgyi_probability(value)
            if score < 0.8:
                continue
            fixed_value = self.converter.transliterate(value)
            if value == fixed_value:
                continue
            errs.append({'class': 50706, 'subclass': 0, 'fix': {key: fixed_value}})
        return errs

    def way(self, data, tags, nodes):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        a = TagFix_ZawgyiBurmese(None)
        a.init(None)
        for name in [
                '',
                'foo',
                'ဘားအံ',
                'ကျိုက်မရော အဝေးပြေးလမ်း',
        ]:
            assert not a.node(None, {'name': name}), name
            assert not a.way(None, {'name': name}, nodes=None), name
            assert not a.relation(None, {'name': name}, members=None), name

        for zawgyi, uni in [('မ္း', 'မ်း'), ('က္ေ', 'က်ေ')]:
            self.check_err(
                a.node(None, {'addr:street': zawgyi}),
                {'class': 50706, 'subclass': 0, 'fix': {'addr:street': uni}},
            )
            self.check_err(
                a.way(None, {'addr:city': zawgyi}, nodes=None),
                {'class': 50706, 'subclass': 0, 'fix': {'addr:city': uni}},
            )
            self.check_err(
                a.relation(None, {'fixme': zawgyi}, members=None),
                {'class': 50706, 'subclass': 0, 'fix': {'fixme': uni}},
            )
