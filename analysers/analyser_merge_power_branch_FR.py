#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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


class Analyser_Merge_Power_Substation_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_osm(item = 7190, id = 3, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power transmission branch without tag "ref:FR:RTE" or invalid'))
        self.def_class_possible_merge(item = 8281, id = 4, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power transmission branch, integration suggestion'))
        self.def_class_update_official(item = 8282, id = 5, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power transmission branch update'))
        self.def_class_missing_official(item = 8280, id = 2, level = 3, tags = ['merge', 'power', 'fix:survey', 'fix:picture', 'fix:imagery'],
            title = T_('Power transmission branch not integrated'))

        self.init(
            "https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte",
            "Points de piquage RTE",
            CSV(SourceOpenDataSoft(
                url="https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte",
                attribution="data.gouv.fr:RTE")),
            Load("Longitude poste (DD)", "Latitude poste (DD)",
                select = {"Fonction": "POINT DE PIQUAGE"}),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = [
                        {"power": ["tower", "pole", "portal", "insulator", "connection"], "operator": False},
                        {"power": ["tower", "pole", "portal", "insulator", "connection"], "operator": "RTE"}]),
                osmRef = "ref:FR:RTE",
                conflationDistance = 200,
                mapping = Mapping(
                    static1 = {
                        "power": "tower",
                        "operator": "RTE"},
                    static2 = {
                        "source": self.source,
                        "line_management": "branch"},
                    mapping1 = {
                        "ref:FR:RTE": "Code poste",
                    text = lambda tags, fields: T_("Power branch of {0}", fields["Code poste"]))))
