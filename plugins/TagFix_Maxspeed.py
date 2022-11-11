#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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


class TagFix_Maxspeed(Plugin):

    maxspeed_table_default = {
        'urban': ['50'],
        'rural': ['90'],
        'trunk': ['110'],
        'motorway': ['130'],
    }

    # List only exceptions
    maxspeed_table = {
        'at:rural': ['100'],
        'at:trunk': ['100'],
        'at:urban40': ['40'],
        'at:urban30': ['30'],
        'be-bru:rural': ['70'],
        'be-bru:urban': ['30'],
        'be:motorway': ['120'],
        'be-vlg:rural': ['70'],
        'by:urban': ['60'],
        'by:motorway': ['110'],
        'ca-on:rural': ['80'],
        'ch:rural': ['80'],
        'ch:trunk': ['100'],
        'ch:motorway': ['120'],
        'cz:trunk': ['80', '130'],
        'cz:motorway': ['80', '130'],
        'de:living_street': ['walk'],
        'de:rural': ['100'],
        'de:motorway': [],
        'dk:rural': ['80'],
        'es:urban': ['20', '30', '50'],
        'es:trunk': ['90'],
        'fr:rural': ['80', '90'],
        'fr:urban': ['30', '50'],
        'gb:nsl_single': ['60 mph'],
        'gb:nsl_dual': ['70 mph'],
        'gb:motorway': ['70 mph'],
        'nl:rural': ['80'],
        'nl:trunk': ['100'],
        'no:rural': ['80'],
        'no:motorway': ['110'],
        'pl:rural': ['90', '100'],
        'pl:trunk': ['100', '120'],
        'pl:motorway': ['140'],
        'ro:trunk': ['100'],
        'ru:living_street': ['20'],
        'ru:urban': ['60'],
        'ru:motorway': ['110'],
        'uk:nsl_single': ['60 mph'],
        'uk:nsl_dual': ['70 mph'],
        'uk:motorway': ['70 mph'],
        'za:urban': ['60'],
        'za:rural': ['100'],
    }


    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[303241] = self.def_class(item = 3032, level = 1, tags = ['tag', 'highway'],
            title = T_('Discordant maxspeed and source:maxspeed or maxspeed:type'))


    def way(self, data, tags, nds):
        if not tags.get('highway') or not tags.get('maxspeed') or not tags['maxspeed'][0] in "0123456789":
            return
        other_maxspeed = tags.get('source:maxspeed', tags.get('maxspeed:type'))
        if other_maxspeed is None or ':' not in other_maxspeed:
            return

        source_maxspeed = self.maxspeed_table.get(other_maxspeed.lower()) or self.maxspeed_table_default.get(other_maxspeed.split(':')[1])
        if not source_maxspeed or len(source_maxspeed) == 0:
            return

        if tags['maxspeed'] not in source_maxspeed:
            return [{'class': 303241, 'subclass': 0, 'text': T_('Discordant {0} and {1}', tags['maxspeed'], other_maxspeed)}]


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Maxspeed(None)
        a.init(None)

        assert not a.way(None, {'name': 'foo'}, None)
        assert not a.way(None, {'highway': 'primary'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'source:maxspeed': 'FR:urban'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:type': 'FR:urban'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '30', 'source:maxspeed': 'FR:urban'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '30', 'maxspeed:type': 'FR:urban'}, None)

        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '35', 'source:maxspeed': 'FR:urban'}, None))
        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '35', 'maxspeed:type': 'FR:urban'}, None))
