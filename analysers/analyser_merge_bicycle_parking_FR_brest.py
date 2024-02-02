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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, SHP, LoadGeomCentroid, Conflate, Select, Mapping

class Analyser_Merge_Bicycle_Parking_FR_Brest(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 1, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking not integrated'))
        self.def_class_possible_merge(item = 8151, id = 3, level = 3, tags = ['merge'],
            title = T_('Bicycle parking integration suggestion'))
        self.def_class_update_official(item = 8412, id = 4, level = 3, tags = ['merge'],
            title = T_('Bicycle parking update'))
        self.init(
            "https://www.data.gouv.fr/fr/datasets/stationnement-velos-1/",
            "Localisation des stationnements vélos connus sur le territoire de Brest métropole",
            SHP(
                SourceDataGouv(
                    attribution="data.gouv.fr:Brest Métropole",
                    dataset="64809542ee39c6b7774817bb",
                    resource="16da3c74-e885-4563-94ef-a9b59d600d8e"),
                zip="DEP_ACT_StationnementVelo.shp"),
            LoadGeomCentroid(select = {"ETAT": 'Existant'}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 10,
                mapping = Mapping(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "capacity": "NB_PLACES",
                        "bicycle_parking": lambda res: self.bicycle_parking.get(res.get("TYPE_STAT")),
                    },
                    mapping2 = {
                        "access": lambda res: "yes" if res.get("ACCES_PUBL") == "OUI" else None,
                        "locked": lambda res: "yes" if res.get("CTRLACCES") == "KorriGo" else None,
                        "start_date": "DATE_POSE",
                        "covered": lambda res: self.covered.get(res.get("TYPE_STAT")),
                        "operator": lambda res: "Brest Métropole" if res.get("DOM_PRIVE") == "Public" else None,
                    })))

    covered = {
        None: None,
        'Abri tram': 'yes',
        'Arceau': 'no',
        'Arceau abri': "yes",
        'Autre': None,
        'Box': 'yes',
        'Rack provisoire': 'no',
        'Ratelier': 'no',
        'Ratelier couvert': 'yes',
    }
    bicycle_parking = {
        None: None,
        'Abri tram': 'shed',
        'Arceau': 'stands',
        'Arceau abri': 'stands',
        'Autre': None,
        'Box': None,
        'Rack provisoire': None,
        'Ratelier': 'wall_loops',
        'Ratelier couvert': 'wall_loops',
    }
