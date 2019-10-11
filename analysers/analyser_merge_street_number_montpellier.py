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

from .Analyser_Merge import Source, CSV, Load, Mapping, Generate
from .analyser_merge_street_number import _Analyser_Merge_Street_Number


class Analyser_Merge_Street_Number_Montpellier(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 5, "Montpellier", logger,
            u"http://opendata.montpelliernumerique.fr/Point-adresse",
            u"Ville de Montpellier - Point adresse",
            # Convert shp with QGis, save as CSV with layer "GEOMETRY=AS_XY".
            CSV(Source(attribution = u"Ville de Montpellier", millesime = "05/2016",
                    file = "address_france_montpellier.csv.bz2")),
            Load("X", "Y", srid = 2154,
                where = lambda res: res["NUM_VOI"] != "0"),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "NUM_SUF"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["NUM_SUF"], fields["LIB_OFF"])} )))
