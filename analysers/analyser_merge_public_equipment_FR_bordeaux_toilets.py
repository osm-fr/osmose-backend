#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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


class Analyser_Merge_Public_Equipment_FR_Bordeaux_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8180, id = 1, level = 3, tags = ['merge', 'public equipment'],
            title = T_('{0} toilets not integrated', 'Bordeaux'))

        self.init(
            "https://opendata.bordeaux-metropole.fr/explore/dataset/bor_sigsanitaire",
            "Toilettes publiques",
            GeoJSON(SourceOpenDataSoft(attribution = "Ville de Bordeaux", format="geojson",
                    url = "https://opendata.bordeaux-metropole.fr/explore/dataset/bor_sigsanitaire")),
            Load("geom_x", "geom_y"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "toilets",
                        "fee": "no",
                        "access": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "toilets:wheelchair": lambda res: "yes" if res["handi"] == "OUI" else "no",
                        "toilets:position": lambda res: "urinal" if res["type"] == "URINOIR" else None} )))
