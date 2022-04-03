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
        self.def_class_missing_osm(item = 7190, id = 2, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power substation is not known from operator'))
        self.def_class_possible_merge(item = 8281, id = 3, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power substation, integration suggestion'),
            detail = T_('This existing power substation can be integrated with official attributes.'))
        self.def_class_update_official(item = 8282, id = 4, level = 3, tags = ['merge', 'power', 'fix:chair'],
            title = T_('Power substation update'),
            detail = T_('This existing power substation can be updated with following values.'))
        self.def_class_missing_official(item = 8280, id = 1, level = 3, tags = ['merge', 'power', 'fix:survey', 'fix:picture', 'fix:imagery'],
            title = T_('Power substation missing in OSM or without tag "ref:FR:RTE"'),
            detail = T_('This power substation is missing in OSM or lacks a national identifier known from operator.'))

        self.init(
            "https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte",
            "Postes électriques RTE",
            CSV(SourceOpenDataSoft(
                url="https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte",
                attribution="data.gouv.fr:RTE")),
            Load("Longitude poste (DD)", "Latitude poste (DD)",
                select = {"Fonction": "POSTE DE TRANSFORMATION"}),
            Conflate(
                select = Select(
                    types = ["ways"],
                    tags = [
                        {"power": "substation", "operator": [False, "RTE"], "substation": [False, "transmission", "distribution", "industrial"]}]),
                osmRef = "ref:FR:RTE",
                conflationDistance = 200,
                tag_keep_multiple_values = ["voltage"],
                mapping = Mapping(
                    static1 = {
                        "power": "substation",
                        "operator": "RTE"},
                    static2 = {
                        "source": self.source},
                    mapping1 = {
                        "ref:FR:RTE": "Code poste",
                        "ref:FR:RTE_nom": "Nom poste"},
                    mapping2 = {
                        "voltage": lambda fields: str((int(float(fields["Tension (kV)"].replace("kV", "")) * 1000))) if fields["Tension (kV)"] not in ("HORS TENSION", "<45kV", "COURANT CONTINU") else None},
                    text = lambda tags, fields: T_("Power substation of {0}", fields["Nom poste"]))))
