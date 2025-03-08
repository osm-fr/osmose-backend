#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe - 2025                                    ##
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


class Analyser_Merge_power_pole_FR_spec_fibre5962 (Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        classs = 1080
        self.def_class_missing_official(item = 8290, id = classs + 1, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole not integrated'))
        self.def_class_possible_merge(item = 8291, id = classs + 3, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole integration suggestion'))
        self.def_class_update_official(item = 8292, id = classs + 4, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole update'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/appuis-aeriens-enedis-utilises-dans-le-cadre-du-deploiement-de-la-fibre-sur-le-rip-du-nord-pas-de-calais/",
            "Appuis aériens ENEDIS utilisés dans le cadre du déploiement de la Fibre sur le RIP du Nord-Pas-de-Calais",
            GDAL(SourceDataGouv(
                attribution="La fibre numérique 59-62",
                dataset="67af2cfd90c839851a1d932f",
                resource="b4c2a50d-4c24-41cf-a124-a6f2524b6406"),
                zip="*.shp"),
            LoadGeomCentroid(),
            Conflate(
                select = Select(
                    types = ['nodes'],
                    tags = [
                        {"power": "pole"},
                        {"disused:power": "pole"},
                        {"removed:power": "pole"},
                        {"demolished:power": "pole"},
                    ]),
                conflationDistance = 5,
                mapping = Mapping(
                    static1 = {'power': 'pole'},
                    static2 = {'source': self.source},
                    mapping1 = {
                        'material': lambda res: self.extract_material.get(res['t_ptech__2']),
                        'operator': lambda res: self.extract_operator.get(res['t_organism'])[0] if res['t_organism'] in self.extract_operator else None},
                    mapping2 = {
                        'operator:wikidata': lambda res: self.extract_operator.get(res['t_organism'])[1] if res['t_organism'] in self.extract_operator else None},
                text = lambda tags, fields: {} )))

    extract_operator = {
        'ERDF': ['Enedis', 'Q3587594']
    }

    extract_material = {
        'PBOI': 'wood',
        'PBET': 'concrete',
        'PCMP': 'epoxy',
        'PMET': 'steel'
    }
