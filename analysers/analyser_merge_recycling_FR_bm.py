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
        self.def_class_missing_official(item = 8120, id = 1, level = 3, tags = ['merge', 'recycling'],
            title = T_f('{0} glass recycling not integrated', 'BM'))
        self.def_class_possible_merge(item = 8121, id = 3, level = 3, tags = ['merge', 'recycling'],
            title = T_f('{0} glass recycling, integration suggestion', 'BM'))
        self.def_class_update_official(item = 8122, id = 4, level = 3, tags = ['merge', 'recycling'],
            title = T_f('{0} glass recycling update', 'BM'))

        self.init(
            'https://opendata.bordeaux-metropole.fr/explore/dataset/en_empac_p',
            'Emplacements d''apport volontaire',
            SHP(Source(attribution = 'Bordeaux Métropole', millesime = '02/2020',
                    fileUrl = 'https://opendata.bordeaux-metropole.fr/explore/dataset/en_empac_p/download/?format=shp&timezone=Europe/Berlin&lang=fr', zip = 'en_empac_p.shp')),
            Load(("ST_X(geom)",), ("ST_Y(geom)",),
                select = {"ident": "%"}),
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
                    mapping1 = {"ref:FR:CUB": "ident"} )))
