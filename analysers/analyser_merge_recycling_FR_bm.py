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

from .Analyser_Merge import Analyser_Merge, Source, SHP, Load, Mapping, Select, Generate


class Analyser_Merge_Recycling_FR_bm(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item = 8120, id = 1, level = 3, tags = ['merge', 'recycling'],
            title = T_('BM glass recycling not integrated'))
        self.possible_merge   = self.def_class(item = 8121, id = 3, level = 3, tags = ['merge', 'recycling'],
            title = T_('BM glass recycling, integration suggestion'))
        self.update_official  = self.def_class(item = 8122, id = 4, level = 3, tags = ['merge', 'recycling'],
            title = T_('BM glass recycling update'))

        self.init(
            u"http://data.bordeaux-metropole.fr/data.php?themes=5",
            u"Emplacements d'apport volontaire",
            SHP(Source(attribution = u"Bordeaux Métropole", millesime = "08/2016",
                    fileUrl = u"http://data.bordeaux-metropole.fr/files.php?gid=69&format=2", zip = "EN_EMPAC_P.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154,
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
                        "recycling:glass_bottles": "yes",
                        "recycling_type": "container"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:CUB": "IDENT"} )))
