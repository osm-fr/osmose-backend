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


class Analyser_Merge_Street_Number_Bordeaux(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 3, 'Bordeaux', logger,
            'https://opendata.bordeaux-metropole.fr/explore/dataset/fv_adresse_p',
            'Numéro de voirie de Bordeaux Métropole',
            CSV(Source(attribution = 'Bordeaux Métropole', millesime = '02/2020',
                    fileUrl = 'https://opendata.bordeaux-metropole.fr/explore/dataset/fv_adresse_p/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=,')),
            Load('Geo Point', 'Geo Point',
                xFunction = lambda x: x.split(",")[1],
                yFunction = lambda y: y.split(",")[0]),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": "NUMERO"},
                    text = lambda tags, fields: {"en": fields["NUMERO"]} )))
