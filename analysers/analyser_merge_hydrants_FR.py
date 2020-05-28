#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Antonin Delpeuch 2020                                      ##
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

from dateutil.parser import parse
from .Analyser_Merge import Analyser_Merge, Source, GeoJSON, Load, Mapping, Select, Generate


class _Analyser_Merge_Afigeo_Hydrants(Analyser_Merge):
    def __init__(self, config, source_url, dataset_name, source, osmRef, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8090, id = 11, level = 3, tags = ['merge', 'emergency'],
            title = T_('Fire hydrant not integrated'))
        self.def_class_possible_merge(item = 8091, id = 13, level = 3, tags = ['merge', 'emergency'],
            title = T_('Fire hydrant integration suggestion'))
        self.def_class_update_official(item = 8092, id = 14, level = 3, tags = ['merge', 'emergency'],
            title = T_('Fire hydrant update'))

        def extract_water_source(res):
            if res.get('SOURCE_PEI') == 'piscine':
                return 'swimming_pool'
            elif res.get('SOURCE_PEI') == 'puits':
                return 'well'
            elif res.get('SOURCE_PEI') == 'reseau_irrigation':
                return 'groundwater'
            elif res.get('SOURCE_PEI') == 'citerne' or res.get('TYPE_PEI') == 'CI':
                return 'water_tank'
            elif res.get('SOURCE_PEI') == 'reseau_aep':
                return 'main'

        def clean_numerical_tag(name):
            """
            If this can be parsed as a number, ensures it is printed as
            an integer, otherwise return the string unchanged.
            Returns None for 0.
            """
            def mapper(res):
                v = res.get(name)
                if v:
                    try:
                        num_value = int(float(v))
                        if num_value:
                            return str(num_value)
                    except ValueError:
                        return v
            return mapper

        self.init(
            source_url,
            dataset_name,
            GeoJSON(source,
                extractor = lambda geojson: geojson),
            Load("geom_x", "geom_y"),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "fire_hydrant"}),
                osmRef = osmRef,
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "fire_hydrant"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        osmRef: "ID_SDIS",
                        "water_source": extract_water_source,
                        "fire_hydrant:type": lambda res: "pillar" if res.get('TYPE_PEI') == 'PI' else None,
                        "fire_hydrant:diameter": clean_numerical_tag("DIAM_PEI"),
                        "pressure": clean_numerical_tag("PRESS_STAT"),
                        "water_volume": clean_numerical_tag("VOLUME"),
                        "ref": clean_numerical_tag("REF_TERR"),
                        "start_date": lambda res: parse(res.get('DATE_MES')).date() if res.get('DATE_MES') else None,
                        "survey:date": lambda res: parse(res.get('DATE_RO')).date() if res.get('DATE_RO') else None,
                        "operator": "NOM_GEST"},
                text = lambda tags, fields: {"en": fields['SITUATION']} )))

class Analyser_Merge_PEI_SDIS_71(_Analyser_Merge_Afigeo_Hydrants):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Afigeo_Hydrants.__init__(self, config,
            source_url='https://trouver.ternum-bfc.fr/dataset/points-deau-incendie-repertories-en-saone-et-loire',
            dataset_name="Points d'eau incendie répertoriés en Saône-et-Loire",
            source=Source(attribution="Service départemental d'incendie et de secours 71",
                millesime='2020-04',
                fileUrl='https://trouver.ternum-bfc.fr/dataset/59d07ea2-ca9a-444a-b977-0e32b280af1c/resource/ddfa8db8-0cf5-4e72-9504-072c96b2c328/service_proxy?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAME=pei71_acbdd5c&OUTPUTFORMAT=geojson&CRSNAME=EPSG:4326'),
            osmRef='ref:FR:SDIS71',
            logger=logger)
