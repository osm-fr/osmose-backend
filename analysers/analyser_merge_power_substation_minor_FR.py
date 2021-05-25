#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2018                                      ##
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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Power_Substation_minor_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8280, id = 11, level = 3, tags = ['merge', 'power', 'fix:survey', 'fix:picture'],
            title = T_('Power minor_distribution substation not integrated'))
        self.def_class_possible_merge(item = 8281, id = 13, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power minor_distribution substation, integration suggestion'))

        self.init(
            "https://data.enedis.fr/explore/dataset/poste-electrique/",
            "Postes HTA/BT",
            CSV(SourceOpenDataSoft(
                attribution="Enedis",
                url="https://data.enedis.fr/explore/dataset/poste-electrique")),
            Load("Geo Point", "Geo Point",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [
                        {"power": "substation", "substation": "minor_distribution", "operator": [False, "EDF", "ERDF", "Enedis"]},
                        {"power": None, "transformer": "distribution", "operator": [False, "EDF", "ERDF", "Enedis"]},
                        {"power": "substation", "substation": "distribution", "operator": [False, "EDF", "ERDF", "Enedis"]}]),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {
                        "power": "substation",
                        "voltage": "20000",
                        "operator": "Enedis"},
                    static2 = {
                        "substation": "minor_distribution",
                        "source": self.source},
                )))
