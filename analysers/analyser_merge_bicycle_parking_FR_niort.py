#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights XioNoX 2024                                                ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, GeoJSON, Load_XY, Conflate, Select, Mapping

class Analyser_Merge_Bicycle_Parking_FR_Niort(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 1, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking not integrated'))
        self.init(
            "https://www.data.gouv.fr/fr/datasets/parking-a-velos/",
            "Emplacement des parkings à vélos sur la commune de Niort",
            GeoJSON(
                SourceDataGouv(
                    attribution="data.gouv.fr:Ville de Niort",
                    dataset="653da2bc403f62ddb14090d9",
                    resource="b1dee3d6-e07c-46cb-b7e4-1e4f1f13d1d6")),
            Load_XY("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source,
                               "access": "yes",
                               "operator": "Communauté d'Agglomération du Niortais",
                    },
                    mapping1 = {
                        "capacity": "CAPACITE",
                    },
                    mapping2 = {
                        "ref:FR:NiortAgglo": "OBJECTID",
                    })))
