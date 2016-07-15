#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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


class Analyser_Merge_Recycling_FR_cub(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8120", "class": 1, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"CUB glass recycling not integrated") }
        self.possible_merge   = {"item":"8121", "class": 3, "level": 3, "tag": ["merge", "recycling"], "desc": T_(u"CUB glass recycling, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            "http://data.lacub.fr/data.php?themes=5",
            u"Emplacements d'apport volontaire",
            SHP(Source(fileUrl = "http://data.bordeaux-metropole.fr/files.php?gid=69&format=2", zip = "EN_EMPAC_P.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 3945,
                select = {"IDENT": "%"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "recycling"}),
                osmRef = "ref:FR:CUB",
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "recycling",
                        "recycling:glass": "yes",
                        "recycling:glass_bottles": "yes",
                        "recycling_type": "container"},
                    static2 = {"source": u"Communauté Urbaine de Bordeaux - 03/2014"},
                    mapping1 = {"ref:FR:CUB": "IDENT"} )))
