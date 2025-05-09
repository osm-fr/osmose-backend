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
from plugins.modules.units import convertToUnit
from modules.Stablehash import stablehash64


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
        'be-bru:rural': ['70'],
        'be-bru:urban': ['30'],
        'be:motorway': ['120'],
        'be-vlg:rural': ['70'],
        'bg:motorway': ['140'],
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
        'ph:motorway': ['100'],
        'ph:rural': ['80'],
        'ph:urban': ['40'],
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
        self.errors[303240] = self.def_class(item = 3032, level = 2, tags = ['tag', 'highway'],
            title = T_('Advisory or practical maxspeed exceeds legal speed limit'))
        self.errors[303241] = self.def_class(item = 3032, level = 1, tags = ['tag', 'highway'],
            title = T_('Discordant maxspeed and source:maxspeed or maxspeed:type'))


    def way(self, data, tags, nds):
        err = []
        maxspeed_tags = list(filter(lambda t: t.startswith('maxspeed') and tags[t] and tags[t][0] in "0123456789", tags))

        # Check that maxspeed:advisory/practical <= maxspeed
        for t in maxspeed_tags:
            if not (":advisory" in t or ":practical" in t):
                continue
            t_normal = t.replace(":advisory", "", 1).replace(":practical", "", 1)
            if not t_normal in maxspeed_tags:
                t_normal = t_normal.replace(":backward", "", 1).replace(":forward", "", 1).replace(":both_ways", "", 1)
            if t_normal in maxspeed_tags:
                try:
                    if convertToUnit(tags[t], 'km/h') > convertToUnit(tags[t_normal], 'km/h'):
                        err.append({
                            'class': 303240,
                            'subclass': stablehash64(t + "|" + t_normal),
                            'text': {"en": "`{0}={1}` > `{2}={3}`".format(t, tags[t], t_normal, tags[t_normal])}
                        })
                except NotImplementedError:
                    pass # Invalid number, checked in Number.py

        if not "highway" in tags or not "maxspeed" in maxspeed_tags:
            return err

        # Check maxspeed vs. source:maxspeed / maxspeed:type
        other_maxspeed = tags.get('source:maxspeed', tags.get('maxspeed:type'))
        if other_maxspeed is None or ':' not in other_maxspeed:
            return err

        source_maxspeed = self.maxspeed_table.get(other_maxspeed.lower()) or self.maxspeed_table_default.get(other_maxspeed.split(':')[1])
        if not source_maxspeed or len(source_maxspeed) == 0:
            return err

        if tags['maxspeed'] not in source_maxspeed:
            err.append({'class': 303241, 'subclass': 0, 'text': T_('Discordant {0} and {1}', tags['maxspeed'], other_maxspeed)})
        return err


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Maxspeed(None)
        a.init(None)

        # Check maxspeed vs. source:maxspeed / maxspeed:type
        assert not a.way(None, {'name': 'foo'}, None)
        assert not a.way(None, {'highway': 'primary'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'source:maxspeed': 'FR:urban'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:type': 'FR:urban'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '30', 'source:maxspeed': 'FR:urban'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '30', 'maxspeed:type': 'FR:urban'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': 'none', 'source:maxspeed': 'DE:motorway'}, None)

        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '35', 'source:maxspeed': 'FR:urban'}, None))
        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '35', 'maxspeed:type': 'FR:urban'}, None))


        # Check that maxspeed:advisory/practical <= maxspeed
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:advisory': '40'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50 mph', 'maxspeed:advisory': '9 mph'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': 'none', 'maxspeed:advisory': '100'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:emergency:practical': '100'}, None)
        assert not a.way(None, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:backward:advisory': '40'}, None)

        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:advisory': '60'}, None))
        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '50', 'maxspeed:backward:advisory': '60'}, None))
        self.check_err(a.way(None, {'highway': 'primary', 'maxspeed': '50 mph', 'maxspeed:practical': '60 mph'}, None))
