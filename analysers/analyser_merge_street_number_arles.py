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


class Analyser_Merge_Street_Number_Arles(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 6, "Arles", logger,
            u"https://trouver.datasud.fr/dataset/base-locale-dadresses-accm",
            u"Base locale d'adresses - ACCM",
            SHP(Source(attribution = u"Arles Crau Camargue Montagnette", millesime = "04/2016",
                    fileUrl = u"https://trouver.datasud.fr/dataset/4c3c3e85-2e53-4c22-938f-0d5ed5efde84/resource/471d295a-3b33-49c3-b051-93d49241afc8/download/accm_adresses.zip", zip = "ACCM_ADRESSES.shp")),
            Load(("ST_X(geom)",), ("ST_Y(geom)",), srid = 2154),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": lambda res: str(res["num_voi"]) + (res["suf_voi"] if res["suf_voi"] else "")},
                    text = lambda tags, fields: {"en": fields["adresse"]} )))
