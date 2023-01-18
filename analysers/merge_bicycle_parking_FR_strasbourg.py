#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights LeJun 2023                                                 ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping

tag_mapping = {
    "ref": (
        lambda res["id_local"]
    ),
    "capacity": (
        lambda res: None if res["capacite"] in (None, "0") else res["capacite"]
    ),
    "capacity:cargo_bike": (
        lambda res: None if res["capacite_cargo"] in (None, "0") else res["capacite_cargo"]
    ),
#    "bicycle_parking": (
#      type_accroche
#      mobilier
#      protection
#    ),
#    "access": (
#        acces      
#    ),
    "fee": (
        lambda res: "no" if res["gratuit"] == "vrai" else None
    ),
    "covered": (
        lambda res: "yes" if res["couverture"] == "vrai" else None
    ),
    "surveillance": (
        lambda res: "yes" if res["surveillance"] == "vrai" else None
    ),
    "lit": (
        lambda res: "yes" if res["lumiere"] == "vrai" else None
    ),
    "website": (
        lambda res["url_info"]
    ),
    "start_date": (
        lambda res["d_service"]
    ),
    "owner": (
        lambda res["proprietaire"]
    ),
    "operator": (
        lambda res: "Eurométropole de Strasbourg" if res["gestionnaire"] == "eurometropole" else None
    ),
    "note": (
        lambda res["commentaires"]
    )
}

class Analyser_Merge_Bicycle_Parking_FR_Strasbourg(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 21, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Strasbourg bicycle parking not integrated'))

        self.init(
            "https://data.strasbourg.eu/explore/dataset/stationnementcyclable_ville_et_eurometropole_de_strasbourg/information/",
            "Stationnement cyclable au format BNSC",
            CSV(SourceOpenDataSoft(
                attribution="Ville et eurométropole de Strasbourg",
                url="https://data.strasbourg.eu/explore/dataset/stationnementcyclable_ville_et_eurometropole_de_strasbourg/")),
            Load_XY("geo_point_2d", "geo_point_2d",
                xFunction = lambda x: Load_XY.float_comma(x.split(',')[1]),
                yFunction = lambda y: Load_XY.float_comma(y.split(',')[0])
            ),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source},
                    mapping1 = tag_mapping )))
