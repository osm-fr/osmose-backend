#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

from datetime import datetime

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, GeoJSON, Load_XY, Conflate, Select, Mapping

class Analyser_Merge_Bicycle_Parking_FR_Grenoble(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 1, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking not integrated'))
        self.def_class_possible_merge(item = 8151, id = 3, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking integration suggestion'))
        self.def_class_update_official(item = 8152, id = 4, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking update'))
        self.init(
            "https://www.data.gouv.fr/fr/datasets/parcs-de-stationnement-velos-de-la-metropole-de-lyon/",
            "Localisation des stationnements vélos connus sur le territoire de la Métropole de Lyon",
            GeoJSON(
                SourceDataGouv(
                    attribution="data.gouv.fr:Grenoble-Alpes Métropole",
                    dataset="658053a53e68b91a5a3a5a21",
                    resource="c9723a83-0ae4-4266-9fbe-ec01da2bb8b8"),
            ),
            Load_XY("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 10,
                mapping = Mapping(
                    static1 = {
                        "amenity": "bicycle_parking",
                        "bicycle_parking": "stands",
                    },
                    static2 = {
                        "source": self.source,
                        "operator": "Grenoble-Alpes Métropole",
                    },
                    mapping1 = {
                        "capacity": lambda res: int(res.get("mob_arce_nb"))*2,
                    },
                    mapping2 = {
                        "start_date": lambda res: datetime.strptime(res.get("mob_arce_datecre"), "%Y%m%d%H%M%S").strftime("%Y-%m-%d"),
                        "ref:FR:GrenobleAlpesMetropole": "mob_arce_id",
                    }
                )
            )
        )
