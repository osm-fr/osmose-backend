#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

from .Analyser_Merge import Source, SHP, Load, Mapping, Select, Generate
from .analyser_merge_street_number import _Analyser_Merge_Street_Number


class Analyser_Merge_Street_Number_Bordeaux(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 3, "Bordeaux", logger,
            u"http://data.bordeaux-metropole.fr/data.php?themes=8",
            u"Numéro de voirie de Bordeaux Métropole",
            SHP(Source(attribution = u"Bordeaux Métropole", millesime = "08/2016",
                    fileUrl = u"http://data.bordeaux-metropole.fr/files.php?gid=20&format=2", zip = "FV_NUMVO_P.shp", encoding = "ISO-8859-15"),
                edit = lambda sql: sql.replace(u'"numero" float8', '"numero" integer').replace(u'"NUMERO" float8', '"NUMERO" integer')),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "NUMERO"},
                    text = lambda tags, fields: {"en": fields["NUMERO"]} )))
