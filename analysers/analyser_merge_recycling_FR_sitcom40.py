#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2023                                      ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Recycling_FR_sitcom40(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8120, id = 40, level = 3, tags = ['merge', 'recycling', 'fix:survey'],
            title = T_('{0} recycling not integrated', 'SITCOM40'))
        self.def_class_possible_merge(item = 8121, id = 41, level = 3, tags = ['merge', 'recycling', 'fix:chair'],
            title = T_('{0} recycling, integration suggestion', 'SITCOM40'))

        self.init(
            "https://www.sitcom40.fr/",
            "Points d'apport volontaire",
            CSV(Source(attribution = "SITCOM - Côte sud des Landes",
                    fileUrl = "https://publicsitcom.z28.web.core.windows.net/OSM/ExportForOSM.csv",
                    fileUrlCache = 1), # Qucik update asked by data provider
                separator = ";"),
            Load_XY("LON", "LAT"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                conflationDistance = 100,
                osmRef = "ref:FR:SITCOM",
                mapping = Mapping(
                    static1 = {
                        "amenity": "recycling",
                        "recycling_type": "container"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "operator": "operator",
                        "ref:FR:SITCOM": "ref:FR:SITCOM",
                        "recycling:plastic_bottles": lambda fields: "yes" if fields["recycling:plastic_bottles"] == "true" else None,
                        "recycling:glass_bottles": lambda fields: "yes" if fields["recycling:glass_bottles"] == "true" else None,
                        "recycling:beverage_cartons": lambda fields: "yes" if fields["recycling:beverage_cartons"] == "true" else None,
                        "recycling:paper": lambda fields: "yes" if fields["recycling:paper"] == "true" else None,
                        "recycling:newspaper": lambda fields: "yes" if fields["recycling:newspaper"] == "true" else None,
                        "recycling:magazines": lambda fields: "yes" if fields["recycling:magazines"] == "true" else None,
                        "recycling:paper_packaging": lambda fields: "yes" if fields["recycling:paper_packaging"] == "true" else None,
                        "recycling:cans": lambda fields: "yes" if fields["recycling:cans"] == "true" else None,
                        "recycling:batteries": lambda fields: "yes" if fields["recycling:batteries"] == "true" else None,
                        "recycling:clothes": lambda fields: "yes" if fields["recycling:clothes"] == "true" else None,
                        "recycling:waste": lambda fields: "yes" if fields["recycling:waste"] == "true" else None,},
                    text = lambda tags, fields: {"en": fields["name"]} )))
