#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Stéphane Péneau           2020                             ##
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


class Analyser_Merge_Recycling_FR_csma(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8120, id = 30, level = 3, tags = ['merge', 'recycling', 'fix:survey', 'fix:picture'],
            title = T_('{0} recycling not integrated', 'CSMA'))
        self.def_class_possible_merge(item = 8121, id = 31, level = 3, tags = ['merge', 'recycling', 'fix:chair'],
            title = T_('{0} recycling, integration suggestion', 'CSMA'))

        self.init(
            "https://environnement.clissonsevremaine.fr/",
            "Points d'apport volontaire",
            CSV(Source(attribution = "Clisson Sèvre et Maine Agglo", millesime = "05/2019",
                    file = "PAV_CSMA.csv.bz2", bz2 = True)),
            Load_XY("X", "Y",
                 xFunction = Load_XY.float_comma,
                 yFunction = Load_XY.float_comma,
                 select = {"detail": ["Verre", "Papier", "Vêtements"]}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {
                        "amenity": "recycling",
                        "recycling_type": "container"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "recycling:glass_bottles": lambda fields: "yes" if fields["detail"] == "Verre" else None,
                        "recycling:paper": lambda fields: "yes" if fields["detail"] == "Papier" else None,
                        "recycling:clothes": lambda fields: "yes" if fields["detail"] == "Vêtements" else None,
                        "location": lambda fields: "underground" if fields["type"] == "Colonne enterrée" else None,
                        "operator": lambda fields: "Clisson Sèvre et Maine Agglo" if fields["detail"] != "Vêtements" else "le Relais",
                        "opening_hours": lambda fields: "24/7" if "Déchèterie" not in fields["adresse"] and "Pôle environnement" not in fields["adresse"] else None,},
                    text = lambda tags, fields: {"en": "{0} - {1}".format(fields["detail"], fields["adresse"])} )))
