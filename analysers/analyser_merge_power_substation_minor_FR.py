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
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Power_Substation_minor_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8280, id = 11, level = 3, tags = ['merge', 'power', 'fix:survey', 'fix:picture'],
            title = T_('Minor distribution power substation missing in OSM'),
            detail = T_('A power substation that directly feeds consumers, known from operator, does not exist in OSM.'))
        self.def_class_possible_merge(item = 8281, id = 13, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power minor distribution substation, integration suggestion'),
            detail = T_('This existing power substation can be integrated with official values.'))

        self.init(
            "https://opendata.agenceore.fr/explore/dataset/postes-de-distribution-publique-postes-htabt/",
            "Postes HTA/BT",
            CSV(SourceOpenDataSoft(
                attribution="Exploitants contributeurs de l'Agence ORE",
                url="https://opendata.agenceore.fr/explore/dataset/postes-de-distribution-publique-postes-htabt/"),
                fields=["Geo Point", "GRD", "Nom poste"]),
            Load_XY("Geo Point", "Geo Point",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [
                        {"power": "substation", "substation": "minor_distribution"},
                        {"power": None, "transformer": ["distribution", "main"]},
                        {"power": "substation", "substation": "distribution"}]),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {
                        "power": "substation",
                        "voltage": "20000"},
                    static2 = {
                        "substation": "minor_distribution"},
                    mapping2 = {
                        "operator": "GRD",
                        "source": lambda fields: self.source() + " - " + fields["GRD"],
                        "name": lambda fields: fields["Nom poste"] if fields["Nom poste"] != "" else None},
                )))
