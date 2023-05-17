#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe - 2023                                    ##
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
from dateutil.parser import parse
from .Analyser_Merge import Analyser_Merge_Point, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_street_lamp_FR_eclext (Analyser_Merge_Point):
    def __init__(self, config, source_url, dataset_name, source, srid, osmRef, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8090, id = 11, level = 3, tags = ['merge', 'street_lamp', 'fix:chair', 'fix:survey'],
            title = T_('Street light not integrated'))
        self.def_class_possible_merge(item = 8091, id = 13, level = 3, tags = ['merge', 'street_lamp', 'fix:chair', 'fix:picture'],
            title = T_('Street light integration suggestion'))
        self.def_class_update_official(item = 8092, id = 14, level = 3, tags = ['merge', 'street_lamp', 'fix:chair', 'fix:survey'],
            title = T_('Street light update'))

        self.init(
            source_url,
            dataset_name,
            CSV(source, srid = srid),
            Load_XY("X", "Y"),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"highway": "street_lamp"}),
                osmRef = osmRef,
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"highway": "street_lamp", "operator": "Syane"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "light:method":lambda res: self.extract_light_method[res.get('typeSource')] if self.extract_light_method[res.get('typeSource')] else None,
                        "light:colour":self.extract_temperature,
                        "light:flux":self.clean_float_tag("fluxSource"),
                        "light:height":self.clean_float_tag("hauteurFeu"),
                        "light:power":self.clean_float_tag("puissance"),
                        "light:lit":lambda res: self.extract_adaptatif[res.get('eclairageAdaptatif')] if self.extract_adaptatif[res.get('eclairageAdaptatif')] else None,
                        "support":lambda res: self.extract_support[res.get('support')] if self.extract_support[res.get('support')] else None,
                        "manufacturer":self.clean_string_tag("fabricant"),
                        "model":self.clean_string_tag("model"),
                        "power": lambda res: "pole" if (res.get('typeSource') == 'POT') else None,
                        "start_date": lambda res: parse(res.get('datePremieInstallation')).date() if res.get('datePremieInstallation') else None},

                text = lambda tags, fields: {} )))
        
    extract_light_method = {
        'FLUO': 'fluorescent',
        'HAL': 'halogen',
        'IM': 'metal-iodide',
        'INC': 'incandescent',
        'IND': 'induction',
        'LED': 'LED',
        'SBP': 'low_pressure_sodium',
        'SHP': 'high_pressure_sodium',
        'VM': 'mercury',
        'XEN': 'xenon'
    }

    extract_support = {
        'CAT': 'catenary',
        'MUR': 'wall',
        'SOL': 'ground'
    }

    def extract_temperature(res):
        v = res.get('TemperatureCouleur')
        if v:
            try:
                num_value = int(float(v))
                if num_value > 0:
                    return str(num_value)+" K"
                else:
                    return None
            except ValueError:
                return None

    extract_adaptatif = {
        'EN': 'dusk_dawn',
        'CO': 'motion',
        'AV': 'demand'
    }

    def clean_string_tag(name):
        def mapper(res):
            v = res.get(name)
            if v:
                if v != "INCONNU":
                    return v.lower()
                else:
                    return None
            else:
                return None
        return mapper

    def clean_float_tag(name):
        """
        If this can be parsed as a number, ensures it is printed as
        an integer, otherwise return the string unchanged.
        Returns None for 0.
        """
        def mapper(res):
            v = res.get(name)
            if v:
                try:
                    num_value = float(v)
                    if num_value:
                        return str(num_value)
                except ValueError:
                    return v
        return mapper
