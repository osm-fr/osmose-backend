#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Thomas O. 2016                                             ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, GeoJSON, Load, Conflate, Select, Mapping


class Analyser_Merge_Recycling_FR_nm_glass(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8120, id = 21, level = 3, tags = ['merge', 'recycling'],
            title = T_('{0} glass recycling not integrated', 'NM'))
        self.def_class_possible_merge(item = 8121, id = 23, level = 3, tags = ['merge', 'recycling'],
            title = T_('{0} glass recycling, integration suggestion', 'NM'))
        self.def_class_update_official(item = 8122, id = 24, level = 3, tags = ['merge', 'recycling'],
            title = T_('{0} glass recycling update', 'NM'))

        self.init(
            "https://data.nantesmetropole.fr/explore/dataset/244400404_colonnes-aeriennes-nantes-metropole",
            "Colonnes aériennes de Nantes Métropole",
            GeoJSON(SourceOpenDataSoft(
                attribution="Nantes Métropole {0}",
                url="https://data.nantesmetropole.fr/explore/dataset/244400404_colonnes-aeriennes-nantes-metropole",
                format="geojson")),
            Load(
                "geom_x", "geom_y",
                select={"type_dechet": "Verre"}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                osmRef = "ref:FR:NM",
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "recycling",
                        "recycling:glass_bottles": "yes",
                        "recycling_type": "container"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:NM": "id_colonne"},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x is not None, [fields["type_dechet"], fields["adresse"], fields["observation"]]))} )))
