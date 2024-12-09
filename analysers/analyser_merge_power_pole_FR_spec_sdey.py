#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe - 2024                                    ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, GDAL, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_power_pole_FR_spec_sdey (Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8290, id = 1001, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole not integrated'))
        self.def_class_possible_merge(item = 8291, id = 1003, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole integration suggestion'))
        self.def_class_update_official(item = 8290, id = 1004, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole update'))

        self.init(
            "https://trouver.ternum-bfc.fr/dataset/support-poteau-des-luminaires",
            "Support poteau des luminaires",
            GDAL(Source(
                attribution="Syndicat Départemental d'Energies de l'Yonne",
                fileUrl="https://trouver.ternum-bfc.fr/dataset/bd94f0e8-b76b-4135-828f-c84e9711e348/resource/e21e39bc-5b51-4c23-b737-1e698ad41d0c/download/pt_lum_89_support_poteau.zip"),
                zip="*.shp"),
            LoadGeomCentroid(select = {"natursupor": ["EP+BT", "EP+BT+FT"]} ),
            Conflate(
                select = Select(
                    types = ['nodes'],
                    tags = {'power': 'pole'}),
                conflationDistance = 5,
                mapping = Mapping(
                    static1 = {'power': 'pole'},
                    static2 = {'source': self.source, 'highway': 'street_lamp'},
                    mapping1 = {
                        'material': lambda res: self.extract_material.get(res['matieresup']),
                        'operator': lambda res: self.extract_operator.get(res['natursupor']),
                        'height': lambda res: res['haut_mat_m'] if res['haut_mat_m'] and res['haut_mat_m'].isnumeric() and float(res['haut_mat_m']) > 6.0 else None},
                text = lambda tags, fields: {} )))

    extract_operator = {
        'EP+BT': 'Enedis',
        'EP+BT+FT': 'Enedis'
    }

    extract_material = {
        'BOIS': 'wood',
        'BETON': 'concrete',
        'ACIER': 'steel'
    }
