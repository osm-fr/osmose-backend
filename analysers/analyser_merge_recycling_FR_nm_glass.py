#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Thomas O. 2016                                             ##
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


class Analyser_Merge_Recycling_FR_nm_glass(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8120", "class": 21, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"NM glass recycling not integrated") }
        self.possible_merge   = {"item":"8121", "class": 23, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"NM glass recycling, integration suggestion") }
        self.update_official  = {"item":"8122", "class": 24, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"NM glass recycling update") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://data.nantesmetropole.fr/explore/dataset/244400404_colonnes-aeriennes-nantes-metropole",
            u"Colonnes aériennes de Nantes Métropole",
            CSV(Source(attribution = u"Nantes Métropole %s", millesime = "08/2018",
                    fileUrl = u"https://data.nantesmetropole.fr/explore/dataset/244400404_colonnes-aeriennes-nantes-metropole/download/?format=csv"), separator = u";"),
            Load(u"location", u"location",
                xFunction = lambda geo: float(geo.split(',')[1].strip()),
                yFunction = lambda geo: float(geo.split(',')[0]),
                select = {u"type_dechets": u"verre"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                osmRef = "ref:FR:NM",
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "recycling",
                        "recycling:glass_bottles": "yes",
                        "recycling_type": "container"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:NM": u"id_colonne"},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x != "None", [fields[u"type_dechets"], fields[u"voie"], fields[u"obs"]]))} )))
