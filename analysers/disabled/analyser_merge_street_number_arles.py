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


class Analyser_Merge_Street_Number_Arles(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 6, "Arles", logger,
            "http://metadonnees.agglo-accm.fr/geosource/srv/fre/catalog.search#/metadata/1e251473-4dc0-4f03-bb89-aa54269c8e3f",
            "Adresses postales",
            SHP(Source(attribution = "Arles Crau Camargue Montagnette", millesime = "08/2020",
                    fileUrl = u"http://webcarto.agglo-accm.fr/ressources/donnees_ouvertes/adresse.adr_accm_adresse.zip", zip = "adr_accm_adresse.shp")),
            LoadGeomCentroid(),
            Conflate(
                mapping = Mapping(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": lambda res: str(res["NUM_VOI"]) + (res["SUF_VOI"] if res["SUF_VOI"] else "")},
                    text = lambda tags, fields: {"en": fields["ADRESSE"]} )))
