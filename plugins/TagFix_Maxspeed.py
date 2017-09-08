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
        'ch:rural': ['80'],
        'ch:trunk': ['100'],
        'ch:motorway': ['120'],
        'de:living_street': ['7'],
        'dk:rural': ['80'],
        'ru:living_street': ['20'],
        'ru:urban': ['60'],
        'ua:urban': ['60'],
        'at:rural': ['100'],
        'de:rural': ['100'],
        'at:trunk': ['100'],
        'cz:trunk': ['80', '130'],
        'ro:trunk': ['100'],
        'cz:motorway': ['80', '130'],
        'de:motorway': [],
        'ru:motorway': ['110'],
        'gb:nsl_single': ['60 mph'],
        'gb:nsl_dual': ['70 mph'],
        'gb:motorway': ['70 mph'],
        'uk:nsl_single': ['60 mph'],
        'uk:nsl_dual': ['70 mph'],
        'uk:motorway': ['70 mph'],
        'nl:rural': ['80'],
        'nl:trunk': ['100'],
    }


    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[303241] = { 'item': 3032, 'level': 1, 'tag': ['tag', 'highway'], 'desc': T_(u'Discordant maxspeed and source:maxspeed') }


    def way(self, data, tags, nds):
        if not tags.get('highway') or not tags.get('maxspeed') or not tags['maxspeed'][0] in "0123456789" or not tags.get('source:maxspeed') or not ':' in tags['source:maxspeed']:
            return

        source_maxspeed = self.maxspeed_table.get(tags['source:maxspeed'].lower()) or self.maxspeed_table_default.get(tags['source:maxspeed'].split(':')[1])
        if not source_maxspeed or len(source_maxspeed) == 0:
            return

        if tags['maxspeed'] not in source_maxspeed:
            return [{'class': 303241, 'subclass': 0, 'text': T_('Discordant %s and %s' % (tags['maxspeed'], tags['source:maxspeed']))}]


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Maxspeed(None)
        a.init(None)

        assert not a.way(None, {'name': 'foo'}, None)
        assert not a.way(None, {'highway': 'primary'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'source:maxspeed': 'FR:urban'}, None)

        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '30', 'source:maxspeed': 'FR:urban'}, None))
