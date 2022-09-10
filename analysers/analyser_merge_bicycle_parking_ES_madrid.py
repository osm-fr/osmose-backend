#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2022                                      ##
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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, Source, SHP, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_Bicycle_Parking_ES_Madrid(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 71, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking not integrated'))

        self.init(
            "https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=1239827b864f4410VgnVCM2000000c205a0aRCRD",
            "Bici. Aparcabicis",
            SHP(Source(
                attribution="Ayuntamiento de Madrid",
                fileUrl="https://datos.madrid.es/egob/catalogo/205099-14-aparca-bicis.zip",
                zip="20220329_APARCABICIS.shp")),
            LoadGeomCentroid(
                select = {"ESTADO": ["ACTIVO", "OPERATIVO"]}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {
                        "source": self.source,
                        "source:date": "01/04/2022"},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["DIRECCION"], fields["COMPLEMENTO_DIRECCION"], fields["DISTRITO"]]))} )))
