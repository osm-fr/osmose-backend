#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe 2023                                      ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Power_Tower_LineMngt_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_possible_merge(item = 8290, id = 2, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power support, line management suggestion'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/reseau-de-transport-delectricite-pylones-speciaux/",
            "Pylones spéciaux RTE",
            CSV(SourceDataGouv(
                attribution="data.gouv.fr:RTE",
                dataset="64ee6705f1cbf615408adae3",
                resource="3823a4e7-d8a3-4822-8162-57fd4dff1de7")),
            Load_XY("X", "Y"),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = [{"power": ["tower", "pole", "terminal", "portal", "insulator"], "operator": [False, "RTE"]}]),
                conflationDistance = 10,
                mapping = Mapping(
                    static1 = {
                        "operator": "RTE"},
                    static2 = {
                        "power": "tower", # Currently default value, we're not able to destinguish tower, pole, terminal, portal and insulator in opendata
                        "operator:wikidata": "Q2178795",
                        "source": self.source},
                    mapping1 = {
                        "location:transition": "location_transition",
                        "line_management": "line_management"})))
