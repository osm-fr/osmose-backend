#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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


class Analyser_Merge_Bicycle_Rental_FR_bm(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = self.def_class(item = 8160, id = 1, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('BM bicycle rental not integrated'))
        self.possible_merge   = self.def_class(item = 8161, id = 3, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('BM bicycle rental integration suggestion'))
        self.update_official  = self.def_class(item = 8162, id = 4, level = 3, tags = ['merge', 'public equipment', 'cycle'],
            title = T_('BM bicycle update'))

        Analyser_Merge.__init__(self, config, logger,
            u"http://data.bordeaux-metropole.fr/data.php?themes=10",
            u"Station VCUB",
            SHP(Source(attribution = u"Bordeaux Métropole", millesime = "08/2016",
                fileUrl = u"http://data.bordeaux-metropole.fr/files.php?gid=43&format=2", zip = "TB_STVEL_P.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "bicycle_rental"}),
                osmRef = "ref",
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "bicycle_rental",
                        "network": "VCUB"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": "NOM",
                        "ref": "NUMSTAT",
                        "capacity": "NBSUPPOR",
                        "vending": lambda res: "subscription" if res["TERMBANC"] == "OUI" else None,
                        "description": lambda res: "VCUB+" if res["TARIF"] == "VLS PLUS" else None} )))
