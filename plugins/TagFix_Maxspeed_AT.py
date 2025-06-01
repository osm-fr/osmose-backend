# -*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Wolfgang Schreiter 2025                                    ##
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


class TagFix_Maxspeed_AT(Plugin):
    """
    Checks for Austrian highway maxspeed tagging.
    """

    only_for = ["AT"]

    valid_maxspeed_types = {
        # Agreed
        'sign': '',
        'AT:motorway': '130', 'AT:trunk': '100', 'AT:rural': '100', 'AT:urban': '50',
        'AT:city_limit30': '30', 'AT:city_limit40': '40',
        'AT:zone15': '15', 'AT:zone20': '20', 'AT:zone30': '30', 'AT:zone40': '40', 'AT:zone50': '50', 'AT:zone70': '70',
        'AT:shared_zone20': '20', 'AT:shared_zone30': '30',
        'AT:bicycle_road': '30',
        # Alternatives
        'AT:zone:20': '20', 'AT:zone:30': '30', 'AT:zone:40': '40', 'AT:zone:50': '50',
        'AT:zone': ''
    }

    def init(self, logger):
        Plugin.init(self, logger)

        self.errors[1] = self.def_class(item=3032, level=2, tags=['maxspeed'],
            title=T_('Speed limit type without speed limit'),
            detail=T_(
'''A speed limit type is given in `maxspeed:type` or `source:maxspeed`, but no speed limit is set in `maxspeed`.'''),
            fix=T_(
'''Set `maxspeed` and either `maxspeed:type` or `source:maxspeed` as appropriate. For a list of values, 
see [Implicit maxspeed values](https://wiki.openstreetmap.org/wiki/Key:maxspeed#Implicit_maxspeed_values).'''),
            trap=T_(
'''Do not just add a `maxspeed` value suitable for the type. The type may be incorrect too!
Always check `highway`, all other tags related to speed and verify on the ground.'''),
            resource='https://wiki.openstreetmap.org/wiki/Key:maxspeed')

        self.errors[2] = self.def_class(item=3091, level=1, tags=['value', 'maxspeed'],
            title=T_('Invalid speed limit value'),
            detail=T_(
'''The speed limit in `maxspeed` must be either numeric or `walk`. Do not specify a unit, km/h is the default.'''),
            fix=T_(
'''Set `maxspeed` as appropriate and set speed limit type in either `maxspeed:type` or `source:maxspeed`. For a list of values, 
see [Implicit maxspeed values](https://wiki.openstreetmap.org/wiki/Key:maxspeed#Implicit_maxspeed_values).'''),
            trap=T_(
'''If a speed limit type (e.g. `AT:*`) is set in `maxspeed`, do not assume it's correct!
Always check `highway`, all other tags related to speed and verify on the ground.'''),
            resource='https://wiki.openstreetmap.org/wiki/Key:maxspeed')

        self.errors[3] = self.def_class(item=3091, level=2, tags=['maxspeed'],
            title=T_('Low speed limit value'),
            detail=T_(
'''The speed limit in `maxspeed` is very low and no type is given in `maxspeed:type` or `source:maxspeed`.'''),
            fix=T_(
'''For pedestrian areas and living streets (except shared zones), walking speed is the default and no
speed limit or type should be set. If walking speed is signposted, set `maxspeed=walk`, `maxspeed:type=sign`
and `traffic_sign=AT:54[text]` or `traffic_sign=AT:..,54[text]`. If a low speed is signposted,
set `maxspeed` to the speed, `maxspeed:type=sign`.'''),
            trap=T_(
'''Do not assume any of the data present is correct!
Always check `highway`, all other tags related to speed and verify on the ground.'''),
            resource='https://wiki.openstreetmap.org/wiki/DE:Verkehrszeichen_in_Österreich')

        self.errors[4] = self.def_class(item=3091, level=2, tags=['value', 'maxspeed'],
            title=T_('Invalid speed limit type'),
            detail=T_(
'''The speed limit type in `maxspeed:type` or `source:maxspeed` is not valid.'''),
            fix=T_(
'''Set the appropriate speed limit type. For a list of values,
see [Implicit maxspeed values](https://wiki.openstreetmap.org/wiki/Key:maxspeed#Implicit_maxspeed_values)'''),
            trap=T_(
'''Do not assume any of the data present is correct!
Always check `highway`, all other tags related to speed and verify on the ground.'''),
            resource='https://wiki.openstreetmap.org/wiki/DE:Key:maxspeed:type')

        self.errors[5] = self.def_class(item=3032, level=2, tags=['maxspeed'],
            title=T_('Multiple speed limit types'),
            detail=T_(
'''`maxspeed:type` and `source:maxspeed` are both set. This may cause confusion for mappers and data consumers
if the values are different.'''),
            fix=T_(
'''Set either `maxspeed:type` or `source:maxspeed`. For a list of values,
see [Implicit maxspeed values](https://wiki.openstreetmap.org/wiki/Key:maxspeed#Implicit_maxspeed_values).'''),
            trap=T_(
'''Do not assume any of the data present is correct!
Always check `highway`, all other tags related to speed and verify on the ground.'''),
            resource='https://wiki.openstreetmap.org/wiki/DE:Key:maxspeed:type')

        self.errors[6] = self.def_class(item=3032, level=1, tags=['maxspeed'],
            title=T_('Speed limit and type mismatch'),
            detail=T_(
'''The speed limit in `maxspeed` is not consistent with the speed limit type in `maxspeed:type` or `source:maxspeed`.'''),
            fix=T_(
'''Adjust `maxspeed`, `maxspeed:type` or `source:maxspeed` as appropriate. For a list of values,
see [Implicit maxspeed values](https://wiki.openstreetmap.org/wiki/Key:maxspeed#Implicit_maxspeed_values).'''),
            trap=T_(
'''Do not assume any of the data present is correct!
Always check `highway`, all other tags related to speed and verify on the ground.'''),
            resource='https://wiki.openstreetmap.org/wiki/DE:Key:maxspeed:type')


    def way(self, data, tags, nds):
        err = []

        if tags.get('highway') is None:
            return err

        # Checks apply only to these tags
        maxspeed = tags.get('maxspeed')
        maxspeed_type = tags.get('maxspeed:type')
        source_maxspeed = tags.get('source:maxspeed')

        # Error: maxspeed type without maxspeed
        if not maxspeed:
            if maxspeed_type or source_maxspeed:
                err.append({'class': 1, 'text': T_('{0} without maxspeed',
                                                   maxspeed_type if maxspeed_type else source_maxspeed)})
            return err

        # Error: maxspeed not numeric or 'walk'
        if not maxspeed.isdigit() and maxspeed != 'walk':
            return {'class': 2, 'text': T_('Invalid maxspeed: `{0}`', maxspeed)}

        # Error: maxspeed suspiciously low, probably 'walk'; needs verification
        # except for speeds < 5 (covered in Number.py) and if signposted
        if maxspeed.isdigit():
            maxspeed_num = int(maxspeed)
            if (maxspeed_num > 4) and (maxspeed_num < 15) and (maxspeed_type != 'sign') and (source_maxspeed != 'sign'):
                return {'class': 3, 'text': T_('Low maxspeed: `{0}`', maxspeed)}

        valid_type = None
        if maxspeed_type:
            # Error: maxspeed:type is invalid
            if maxspeed_type in self.valid_maxspeed_types.keys():
                valid_type = maxspeed_type
            else:
                err.append({'class': 4,
                            'text': T_('Invalid maxspeed:type: `{0}`', maxspeed_type)})
            if source_maxspeed:
                # Error: source:maxspeed equal to maxspeed:type
                # Disabled for now to avoid excessive warnings; perform bulk cleanup first
                if maxspeed_type == source_maxspeed:
                    # err.append({'class': 5,
                    #            'text': T_('Duplicate speed limit type: `{0}`', maxspeed_type)})
                    pass
                # Error: source:maxspeed contains different maxspeed type
                elif source_maxspeed.startswith('AT:') or source_maxspeed in {'zone', 'sign', 'walk'}:
                    err.append({'class': 5,
                                'text': T_('Conflicting speed limit types: `{0}`<>`{1}`', maxspeed_type, source_maxspeed)})
        elif source_maxspeed:
            # Error: source:maxspeed is invalid
            if source_maxspeed in self.valid_maxspeed_types.keys():
                valid_type = source_maxspeed
            elif source_maxspeed.startswith('AT:') or source_maxspeed in {'zone', 'walk'}:
                err.append({'class': 4,
                            'text': T_('Invalid source:maxspeed: `{0}`', source_maxspeed)})

        # Error: maxspeed type doesn't match maxspeed
        # except for types covered in TagFix_Maxspeed plugin and types without specific speed
        if valid_type and valid_type not in {'AT:motorway', 'AT:trunk', 'AT:rural', 'AT:urban'}:
            if self.valid_maxspeed_types.get(valid_type) and (self.valid_maxspeed_types.get(valid_type) != maxspeed):
                err.append({'class': 6,
                            'text': T_('maxspeed and type mismatch: `{0}`<>`{1}`', maxspeed, valid_type)})

        return err

###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        plugin = TagFix_Maxspeed_AT(None)
        plugin.init(None)

        # No error if not a highway
        assert not plugin.way(None, {'maxspeed_type': 'dont know', 'source:maxspeed': 'unknown'}, None)

        # No error if valid
        assert not plugin.way(None, {'highway': 'primary'}, None)

        assert not plugin.way(None, {'highway': 'primary', 'maxspeed': '100'}, None)

        assert not plugin.way(None, {'highway': 'living_street', 'maxspeed': 'walk'}, None)

        assert not plugin.way(None, {'highway': 'residential', 'maxspeed': '5', 'source:maxspeed': 'sign'}, None)

        assert not plugin.way(None, {'highway': 'secondary', 'maxspeed': '70', 'maxspeed:type': 'sign'}, None)

        assert not plugin.way(None, {'highway': 'tertiary', 'maxspeed': '50', 'source:maxspeed': 'AT:urban'}, None)

        assert not plugin.way(None, {'highway': 'unclassified', 'maxspeed': '100', 'maxspeed:type': 'AT:rural',
                                               'source:maxspeed': 'read it in the news'}, None)

        # Error when maxspeed type without maxspeed
        self.check_err(plugin.way(None, {'highway': 'secondary', 'maxspeed:type': 'sign'}, None))

        self.check_err(plugin.way(None, {'highway': 'secondary', 'source:maxspeed': 'sign'}, None))

        # Error when maxspeed not numeric or walk
        self.check_err(plugin.way(None, {'highway': 'tertiary', 'maxspeed': 'fast'}, None))

        # Error when maxspeed too low
        self.check_err(plugin.way(None, {'highway': 'residential', 'maxspeed': '5'}, None))

        # Error when invalid speed limit type
        self.check_err(plugin.way(None, {'highway': 'residential', 'maxspeed': '50',
                                                   'source:maxspeed': 'AT:city'}, None))

        self.check_err(plugin.way(None, {'highway': 'secondary', 'maxspeed': '70', 'maxspeed:type': 'yes'}, None))

        # Error when speed limit type duplication
        self.check_err(plugin.way(None, {'highway': 'unclassified', 'maxspeed': '100',
                                                   'maxspeed:type': 'AT:zone40', 'source:maxspeed': 'AT:rural'}, None))

        self.check_err(plugin.way(None, {'highway': 'unclassified', 'maxspeed': '100',
                                                   'maxspeed:type': 'AT:rural', 'source:maxspeed': 'AT:urban'}, None))

        # Error when speed and type mismatch
        self.check_err(plugin.way(None, {'highway': 'secondary', 'maxspeed': '70',
                                                   'maxspeed:type': 'AT:city_limit30'}, None))

        self.check_err(plugin.way(None, {'highway': 'tertiary', 'maxspeed': '50',
                                                   'source:maxspeed': 'AT:rural'}, None))
