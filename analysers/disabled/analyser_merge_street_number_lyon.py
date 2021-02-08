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

from .Analyser_Merge import Source, SHP, LoadGeomCentroid, Conflate, Mapping
from .analyser_merge_street_number import _Analyser_Merge_Street_Number


class Analyser_Merge_Street_Number_Lyon(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 4, "Lyon", logger,
            "https://data.grandlyon.com/localisation/points-dadressage-sur-bftiments-de-la-mftropole-de-lyon/",
            "Grand Lyon - Points d'adressage sur bâtiments de la Métropole de Lyon",
            SHP(Source(attribution = "Grand Lyon", millesime = "092020",
                    fileUrl = "https://download.data.grandlyon.com/ws/grandlyon/adr_voie_lieu.adradresse.shp?srsname=EPSG:4326&maxfeatures=999999&start=1",
                zip = "adr_voie_lieu.adradresse.shp", encoding = "ISO-8859-15")),
            LoadGeomCentroid(),
            Conflate(
                mapping = Mapping(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "numero"},
                    text = lambda tags, fields: {"en": u"{0} {1}".format(fields["numero"], fields["voie"])} )))
