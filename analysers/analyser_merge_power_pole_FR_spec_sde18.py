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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, GDAL, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_power_pole_FR_spec_sde18 (Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        classs = 1050
        self.def_class_missing_official(item = 8290, id = classs + 1, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole not integrated'))
        self.def_class_possible_merge(item = 8291, id = classs + 3, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole integration suggestion'))
        self.def_class_update_official(item = 8290, id = classs + 4, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole update'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/supports-eclairage-public-du-sde18/",
            "Supports Eclairage Public du SDE18",
            GDAL(SourceDataGouv(
                attribution="SDE 18",
                dataset="673b1255be2baa1d2a71c950",
                resource="3d617c33-05e1-4190-a3ca-802d94dad509"
            ),
            zip="*.shp"),
            LoadGeomCentroid(select = {"_type": ["poteau", "Poteau", "POTEAU"]} ),
            Conflate(
                select = Select(
                    types = ['nodes'],
                    tags = {'power': 'pole'}),
                conflationDistance = 5,
                mapping = Mapping(
                    static1 = {'power': 'pole'},
                    static2 = {'source': self.source, 'highway': 'street_lamp', 'operator':'Enedis', 'operator:wikidata':'Q3587594'},
                    mapping1 = {
                        'material': lambda res: self.extract_material.get(res['_matiere']),
                        'height': lambda res: res['hauteur'] if res['hauteur'] and res['hauteur'] > 6.0 else None},
                text = lambda tags, fields: {} )))

    extract_material = {
        'Bois': 'wood',
        'Béton': 'concrete'
    }
