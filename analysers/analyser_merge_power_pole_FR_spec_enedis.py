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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_power_pole_FR_spec_enedis (Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        classs = 1070
        self.def_class_missing_official(item = 8290, id = classs + 1, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole not integrated'))
        self.def_class_possible_merge(item = 8291, id = classs + 3, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole integration suggestion'))
        self.def_class_update_official(item = 8290, id = classs + 4, level = 3, tags = ['merge', 'power', 'fix:chair', 'fix:survey'],
            title = T_('Power pole update'))

        dep_code = config.options.get('dep_code') or config.options.get('country').split('-')[1]

        self.init(
            "https://www.data.gouv.fr/fr/datasets/position-geographique-des-poteaux-hta-et-bt/",
            "Position géographique des poteaux électriques HTA et BT Enedis",
            CSV(SourceDataGouv(
                attribution="Enedis",
                dataset="60b9a555532a9939f42fcb3b",
                resource="93186d05-f283-421c-8534-a92149a01a36"
            ), fields=['Code Département', 'Geo Point', 'PREC'], separator=';'),
            Load_XY("Geo Point", "Geo Point",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                select = {
                    "Code Département": dep_code,
                    "PREC": ["A : 0 - 50cm", "B : 50cm - 1m 50"]
                }),
            Conflate(
                select = Select(
                    types = ['nodes'],
                    tags = {'power': 'pole'}),
                conflationDistance = 3,
                mapping = Mapping(
                    static1 = {'power': 'pole'},
                    static2 = {'source': self.source, 'operator':'Enedis', 'operator:wikidata':'Q3587594'},
                text = lambda tags, fields: {} )))
