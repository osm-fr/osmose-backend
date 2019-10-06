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

from .Analyser_Merge import Source, SHP, Load, Mapping, Generate
from .analyser_merge_street_number import _Analyser_Merge_Street_Number


class Analyser_Merge_Street_Number_Lyon(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 4, "Lyon", logger,
            u"https://data.grandlyon.com/localisation/points-dadressage-sur-bftiments-de-la-mftropole-de-lyon/",
            u"Grand Lyon - Points d'adressage sur bâtiments de la Métropole de Lyon",
            SHP(Source(attribution = u"Grand Lyon", millesime = "06/2016",
                    fileUrl = u"https://download.data.grandlyon.com/ws/grandlyon/adr_voie_lieu.adradresse.shp?srsname=epsg:4171",
                zip = "adr_voie_lieu.adradresse.shp", encoding = "ISO-8859-15")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",)),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "numero"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["numero"], fields["voie"])} )))
