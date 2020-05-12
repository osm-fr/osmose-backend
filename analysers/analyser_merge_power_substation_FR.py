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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Power_Substation_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_osm(item = 7190, id = 2, level = 3, tags = ['merge', 'power'],
            title = T_('Power substation without tag "ref:FR:RTE" or invalid'))
        self.def_class_possible_merge(item = 8281, id = 3, level = 3, tags = ['merge', 'power'],
            title = T_('Power substation, integration suggestion'))
        self.def_class_update_official(item = 8282, id = 4, level = 3, tags = ['merge', 'power'],
            title = T_('Power substation update'))
        self.def_class_missing_official(item = 8280, id = 1, level = 3, tags = ['merge', 'power'],
            title = T_('Power substation not integrated'))

        self.init(
            u"https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte",
            u"Postes électriques RTE",
            CSV(Source(attribution = u"data.gouv.fr:RTE", millesime = "12/2018",
                    fileUrl = u"https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = u";"),
            Load("Longitude poste (DD)", "Latitude poste (DD)"),
            Mapping(
                select = Select(
                    types = ["ways"],
                    tags = [
                        {"power": "substation", "operator": False, "substation": False},
                        {"power": "substation", "operator": False, "substation": ["transmission", "distribution"]},
                        {"power": "substation", "operator": "RTE", "substation": False},
                        {"power": "substation", "operator": "RTE", "substation": ["transmission", "distribution"]}]),
                osmRef = "ref:FR:RTE",
                conflationDistance = 200,
                generate = Generate(
                    static1 = {
                        "power": "substation",
                        "operator": "RTE"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:RTE": "Code poste",
                        "ref:FR:RTE_nom": "Nom poste"},
                    mapping2 = {
                        "voltage": lambda fields: str((int(float(fields["Tension (kV)"].replace("kV", "")) * 1000))) if fields["Tension (kV)"] not in ("HORS TENSION", "<45kV", "COURANT CONTINU") else None},
                    tag_keep_multiple_values = ["voltage"],
                    text = lambda tags, fields: T_(u"Power substation of %s", fields["Nom poste"]))))
