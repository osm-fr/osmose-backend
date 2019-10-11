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


class Analyser_Merge_Street_Number_Toulouse(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 1, "Toulouse", logger,
            u"http://data.grandtoulouse.fr/les-donnees/-/opendata/card/12673-n-de-rue",
            u"GrandToulouse-N° de rue",
            CSV(Source(attribution = "ToulouseMetropole", millesime = "2012-10-04",
                    file = "address_france_toulouse.csv.bz2"),
                separator = u";"),
            Load("X_WGS84", "Y_WGS84",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                generate = Generate(
                    static2 = {
                        "source": lambda a: a.parser.source.attribution,
                        "source:date": lambda a: a.parser.source.millesime},
                    mapping1 = {"addr:housenumber": "no"},
                    text = lambda tags, fields: {"en": u"%s %s" % (fields["no"], fields["lib_off"])} )))
