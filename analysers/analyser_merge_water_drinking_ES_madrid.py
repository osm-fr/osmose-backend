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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Water_Drinking_ES_Madrid(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8510, id = 21, level = 3, tags = ['merge', 'public equipment', 'water', 'fix:survey', 'fix:picture'],
            title = T_('Drinking water not integrated'))

        self.init(
            "https://datos.madrid.es/sites/v/index.jsp?vgnextoid=b8b2e44003b95510VgnVCM1000001d4a900aRCRD",
            "Fuentes de agua para beber",
            CSV(Source(
                attribution="Ayuntamiento de Madrid",
                fileUrl="https://datos.madrid.es/egob/catalogo/300051-13-fuentes.csv"),
                separator = ';'),
            Load("Longitud", "Latitud",
                select = {"OBSERVACIONES": "EN SERVICIO"}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "drinking_water"}),
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "drinking_water"},
                    static2 = {
                        "source": self.source,
                        "source:date": "21/01/2022",
                        "operator": "Ayuntamiento de Madrid"},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["DESCRIPTIO"], fields["MINTNUMERO"], fields["NIMTTIPOVI"], fields["MINTNOMBRE"], fields["NOMBRE_BAR"], fields["NOMBRE_DIS"]]))} )))
