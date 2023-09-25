#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe 2022                                      ##
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


class Analyser_Merge_Power_Branch_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_osm(item = 7190, id = 22, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power line branch not known by the operator'))
        self.def_class_possible_merge(item = 8281, id = 23, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power line branch, integration suggestion'))
        self.def_class_update_official(item = 8282, id = 24, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power line branch update'))
        self.def_class_missing_official(item = 8280, id = 21, level = 3, tags = ['merge', 'power', 'fix:survey', 'fix:picture', 'fix:imagery'],
            title = T_('Power line branch is missing in OSM or without tag "ref:FR:RTE"'))

        self.init(
            "https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte",
            "Points de piquage RTE",
            CSV(SourceOpenDataSoft(
                url="https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte",
                attribution="data.gouv.fr:RTE")),
            Load_XY("Longitude poste (DD)", "Latitude poste (DD)",
                select = {"FONCTION DU POSTE": "Poste de piquage"}),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = [{"power": ["tower", "pole", "portal", "insulator", "connection"], "operator": "RTE", "line_management": {"regex": r"(^|\(|\|)branch(\||\)|$)"}}]),
                osmRef = "ref:FR:RTE",
                conflationDistance = 200,
                mapping = Mapping(
                    static1 = {
                        "power": "tower",
                        "operator": "RTE",
                        "operator:wikidata": "Q2178795"},
                    static2 = {
                        "source": self.source,
                        "line_management": "branch"},
                    mapping1 = {
                        "ref:FR:RTE": "Code poste"},
                    text = lambda tags, fields: T_("Power branch of {0}", fields["Code poste"]))))
