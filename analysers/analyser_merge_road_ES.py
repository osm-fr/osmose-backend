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
from .Analyser_Merge import Source, SHP, Load, Select, Mapping
from .Analyser_Merge_Network import Analyser_Merge_Network, ConflateNetwork


class Analyser_Merge_Road_ES(Analyser_Merge_Network):
    def __init__(self, config, logger = None):
        Analyser_Merge_Network.__init__(self, config, logger)
        self.def_class_missing_official(item = 7170, id = 200, level = 3, tags = ['merge', 'highway', 'fix:survey', 'fix:imagery'],
            title = T_('Road not integrated'))

        self.init(
            'http://centrodedescargas.cnig.es/CentroDescargas/buscar.do?filtro.codFamilia=REDTR#',
            'Redes de transporte',
            SHP(Source(
                attribution='Instituto Geográfico Nacional', millesime='2022-04-26',
                fileUrl='http://centrodedescargas.cnig.es/CentroDescargas/descargaDir', post={'secuencialDescDir': self.secuencialDescDir(config.options['country']), 'aceptCodsLicsDD_0': '15'},
                encoding='LATIN1'),
                zip="*/*/rt_tramo_vial.shp",
                fields=['claseD', 'estadofis']),
            Load('geom',
                table_name = 'road_es_' + self.secuencialDescDir(config.options['country']),
                select = {
                    'claseD': ['Carretera convencional', 'Urbano', 'Autovía', 'Carretera multicarril'],  # Exclude 'Senda' and 'Camino'
                    'estadofis': '1'} ),
            ConflateNetwork(
                select = Select(
                    types = ['ways'],
                    tags = {'highway': None}),
                conflationDistance = 15,
                mapping = Mapping(
                    static1 = {'highway': 'road'},
                    static2 = {'source': self.source},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda x: x, [fields['claseD']]))} )))

    def secuencialDescDir(self, code):
        return {
            'ES-AL': '9150706',
            'ES-CA': '9150715',
            'ES-CO': '9150722',
            'ES-GR': '9150727',
            'ES-H': '9150729',
            'ES-J': '9150732',
            'ES-MA': '9150739',
            'ES-SE': '9150749',
            'ES-HU': '9150730',
            'ES-TE': '9150752',
            'ES-Z': '9150757',
            'ES-O': '9150708',
            'ES-S': '9150716',
            'ES-CE': '9150719',
            'ES-AV': '9150709',
            'ES-BU': '9150713',
            'ES-LE': '9150735',
            'ES-P': '9150744',
            'ES-SA': '9150746',
            'ES-SG': '9150748',
            'ES-SO': '9150750',
            'ES-VA': '9150755',
            'ES-ZA': '9150756',
            'ES-AB': '9150704',
            'ES-CR': '9150720',
            'ES-CU': '9150723',
            'ES-GU': '9150728',
            'ES-TO': '9150753',
            'ES-GC': '9150734',
            'ES-TF': '9150747',
            'ES-B': '9150711',
            'ES-GI': '9150726',
            'ES-L': '9150736',
            'ES-T': '9150751',
            'ES-BA': '9150710',
            'ES-CC': '9150714',
            'ES-C': '9150703',
            'ES-LU': '9150737',
            'ES-OR': '9150743',
            'ES-PO': '9150745',
            'ES-PM': '9150731',
            'ES-MU': '9150741',
            'ES-M': '9150738',
            'ES-ML': '9150740',
            'ES-NA': '9150742',
            'ES-VI': '9150707',
            'ES-BI': '9150712',
            'ES-SS': '9150725',
            'ES-LO': '9150733',
            'ES-A': '9150705',
            'ES-CS': '9150717',
            'ES-V': '9150754',
        }[code]
