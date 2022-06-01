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

from modules.OsmoseTranslation import T_
from dateutil.parser import parse
from .Analyser_Merge import Analyser_Merge_Point, GeoJSON, Load_XY, Conflate, Select, Mapping


class _Analyser_Merge_Afigeo_Hydrants(Analyser_Merge_Point):
    def __init__(self, config, source_url, dataset_name, source, osmRef, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8090, id = 11, level = 3, tags = ['merge', 'emergency', 'fix:imagery', 'fix:picture', 'fix:survey'],
            title = T_('Fire hydrant not integrated'))
        self.def_class_possible_merge(item = 8091, id = 13, level = 3, tags = ['merge', 'emergency', 'fix:chair', 'fix:picture'],
            title = T_('Fire hydrant integration suggestion'))
        self.def_class_update_official(item = 8092, id = 14, level = 3, tags = ['merge', 'emergency', 'fix:imagery', 'fix:picture', 'fix:survey'],
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
            Load_XY("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "fire_hydrant"}),
                osmRef = osmRef,
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {"emergency": "fire_hydrant"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        osmRef: "id_sdis",
                        "water_source": extract_water_source,
                        "fire_hydrant:type": lambda res: "pillar" if res.get('type_pei') == 'PI' else None,
                        "fire_hydrant:diameter": clean_numerical_tag("diam_pei"),
                        "pressure": clean_numerical_tag("press_stat"),
                        "water_volume": clean_numerical_tag("volume"),
                        "ref": clean_numerical_tag("ref_terr"),
                        "start_date": lambda res: parse(res.get('date_ct')).date() if res.get('date_ct') else None,
                        "survey:date": lambda res: parse(res.get('date_ro')).date() if res.get('date_ro') else None,
                        "operator": lambda res: res.get("nom_gest")},
                text = lambda tags, fields: {"en": fields['situation']} )))
