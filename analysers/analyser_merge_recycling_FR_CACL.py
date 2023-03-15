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


class Analyser_Merge_Recycling_FR_CACL(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8120, id = 40, level = 3, tags = ['merge', 'recycling', 'fix:survey'],
            title = T_('{0} recycling not integrated', 'CACL'))
        self.def_class_possible_merge(item = 8121, id = 41, level = 3, tags = ['merge', 'recycling', 'fix:chair'],
            title = T_('{0} recycling, integration suggestion', 'CACL'))

        self.init(
            "https://data.cacl-guyane.fr/explorateur/donnees/environnement-positions-pav-verre",
            "Points d'apport volontaire",
            CSV(Source(attribution = "CACL",
                    fileUrl = "https://api-data.cacl-guyane.fr/v1/environnement-positions-pav-verre?format=csv"),
                separator = ";"),
            Load_XY("lon", "lat"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                conflationDistance = 100,
                osmRef = "",
                mapping = Mapping(
                    static1 = {
                        "amenity": "recycling",
                        "recycling_type": "container"},
                        "recycling_glass_bottles": "yes"
                        "operator": "CACL"
                    static2 = {"source": self.source},
                    mapping1 = {
                        
                    text = lambda tags, fields: {"en": fields["name"]} )))
