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

from Analyser_Merge import Analyser_Merge, Source, SHP, Load, Mapping, Select, Generate


class Analyser_Merge_Recycling_FR_nm_glass(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8120", "class": 21, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"NM glass recycling not integrated") }
        self.possible_merge   = {"item":"8121", "class": 23, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"NM glass recycling, integration suggestion") }
        self.update_official  = {"item":"8122", "class": 24, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"NM glass recycling update") }
        Analyser_Merge.__init__(self, config, logger,
            "http://data.nantes.fr/donnees/detail/localisation-des-colonnes-aeriennes-de-nantes-metropole/",
            u"Localisation des colonnes aériennes de Nantes Métropole",
            SHP(Source(attribution = u"Nantes Métropole", millesime = "07/2016",
                    fileUrl = "http://data.nantes.fr/fileadmin/data/datastore/nm/environnement/24440040400129_NM_NM_00119/COLONNES_AERIENNES_NM_shp_l93.zip", zip = "COLONNES_AERIENNES_NM.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154,
                select = {"TYPE_DECHE": "verre"}),
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
                    mapping1 = {"ref:FR:NM": "ID_COLONNE"},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x != "None", [fields["TYPE_DECHE"], fields["VOIE"], fields["OBS"]]))} )))
