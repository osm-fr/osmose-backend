#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights Paul Bonaud 2023                                           ##
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


class Analyser_Merge_Recycling_FR_ampm(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8120, id = 30, level = 3, tags = ['merge', 'recycling', 'fix:survey', 'fix:picture'],
            title = T_('{0} recycling not integrated', 'AMPM'))
        self.def_class_possible_merge(item = 8121, id = 31, level = 3, tags = ['merge', 'recycling', 'fix:chair'],
            title = T_('{0} recycling, integration suggestion', 'AMPM'))

        self.init(
            "https://data.ampmetropole.fr/explore/dataset/ol-pav-harmonise",
            "Points d'apport volontaire",
            CSV(SourceOpenDataSoft(
                attribution="Métropole Aix-Marseille Provence",
                url="https://data.ampmetropole.fr/explore/dataset/ol-pav-harmonise")),
            Load_XY("geo_point_2d", "geo_point_2d",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                select = {"Type de flux": ["Verre", "Biflux", "Textile"]}),
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
                        "recycling:glass_bottles": lambda fields: "yes" if fields["Type de flux"] == "Verre" else None,
                        "recycling:paper": lambda fields: "yes" if fields["Type de flux"] == "Biflux" else None,
                        "recycling:plastic": lambda fields: "yes" if fields["Type de flux"] == "Biflux" else None,
                        "recycling:packaging": lambda fields: "yes" if fields["Type de flux"] == "Biflux" else None,
                        "recycling:clothes": lambda fields: "yes" if fields["Type de flux"] == "Textile" else None,
                        "location": lambda fields: "underground" if fields["Type de colonne"] == "Enterré" else None,},
                    text = lambda tags, fields: {"en": "{0} - {1}".format(fields["Type de flux"], fields["adresse"])} )))
