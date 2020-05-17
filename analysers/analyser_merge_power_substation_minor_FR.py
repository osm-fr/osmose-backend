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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Power_Substation_minor_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8280, id = 11, level = 3, tags = ['merge', 'power'],
            title = T_('Power minor_distribution substation not integrated'))
        self.def_class_possible_merge(item = 8281, id = 13, level = 3, tags = ['merge', 'power'],
            title = T_('Power minor_distribution substation, integration suggestion'))

        self.init(
            u"https://data.enedis.fr/explore/dataset/poste-electrique/",
            u"Postes HTA/BT",
            CSV(Source(attribution = u"Enedis", millesime = "06/2018",
                    fileUrl = u"https://data.enedis.fr/explore/dataset/poste-electrique/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = u";"),
            Load("Geo Point", "Geo Point",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [
                        {"power": "substation", "substation": "minor_distribution", "operator": False},
                        {"power": "substation", "substation": "minor_distribution", "operator": "EDF"},
                        {"power": "substation", "substation": "minor_distribution", "operator": "ERDF"},
                        {"power": "substation", "substation": "minor_distribution", "operator": "Enedis"},
                        {"power": None, "transformer": "distribution", "operator": False},
                        {"power": None, "transformer": "distribution", "operator": "EDF"},
                        {"power": None, "transformer": "distribution", "operator": "ERDF"},
                        {"power": None, "transformer": "distribution", "operator": "Enedis"}]),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {
                        "power": "substation",
                        "substation": "minor_distribution",
                        "voltage": "20000;400",
                        "operator": "Enedis"},
                    static2 = {"source": self.source},
                )))
