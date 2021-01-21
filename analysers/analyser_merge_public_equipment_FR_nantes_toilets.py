#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien Pavie 2017                                          ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, JSON, Load, Conflate, Select, Mapping
import json


class Analyser_Merge_Public_Equipment_FR_Nantes_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 5, level = 3, tags = ['merge', 'public equipment'],
            title = T_('{0} toilets not integrated', 'Nantes Métropole'))

        self.init(
            "https://data.nantesmetropole.fr/explore/dataset/244400404_toilettes-publiques-nantes-metropole",
            "Toilettes publiques de Nantes Métropole",
            JSON(
                SourceOpenDataSoft(
                    attribution="Nantes Métropole",
                    base_url="https://data.nantesmetropole.fr",
                    dataset="244400404_toilettes-publiques-nantes-metropole",
                    format="json"),
                extractor = lambda json: map(lambda j: j['fields'], json)),
            Load("geo_shape.coordinates", "geo_shape.coordinates",
                xFunction = lambda c: c and json.loads(c)[0],
                yFunction = lambda c: c and json.loads(c)[1]),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "toilets",
                        "access": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": 'nom',
                        "ref": 'id',
                        "operator": 'exploitant',
                        "opening_hours": lambda res: "24/7" if res['horaire_d_ouverture'] == u'24/24' else None,
                        "wheelchair": lambda res: "yes" if res['accessible_pmr'] == u'oui' else "no" if res['accessible_pmr'] == u'non' else None } )))
