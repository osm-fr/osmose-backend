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

import re
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Power_Substation_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8280", "class": 1, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power substation not integrated") }
        self.missing_osm      = {"item":"7190", "class": 2, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power substation without ref:FR:RTE") }
        self.possible_merge   = {"item":"8281", "class": 3, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power substation, integration suggestion") }
        self.update_official  = {"item":"8282", "class": 4, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power substation update") }

        Analyser_Merge.__init__(self, config, logger,
            "https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte/",
            u"Postes électriques RTE",
            CSV(Source(attribution = u"data.gouv.fr:RTE", millesime = "12/2017",
                    fileUrl = "https://opendata.reseaux-energies.fr/explore/dataset/postes-electriques-rte/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = ";"),
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
                        "voltage": lambda fields: (int(float(fields["Tension (kV)"].split(" ")[0]) * 1000)) if fields["Tension (kV)"] not in ("HORS TENSION", "INF 45 kV", "COURANT CONTINU") else None},
                    tag_keep_multiple_values = ["voltage"],
                    text = lambda tags, fields: T_(u"Power substation of %s", fields["Nom poste"]))))
