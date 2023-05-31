#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2023                                      ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, SHP, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Bridge_ES(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8540, id = 1, level = 3, tags = ['merge', 'highway', 'fix:survey', 'fix:imagery'],
            title = T_('Bridge not integrated'))

        self.init(
            'http://centrodedescargas.cnig.es/CentroDescargas/buscar.do',
            'Hidrografía',
            SHP(Source(
                attribution='Instituto Geográfico Nacional', millesime='2023-05-22',
                fileUrl='http://centrodedescargas.cnig.es/CentroDescargas/descargaDir', post={'secuencialDescDir': self.secuencialDescDir(), 'aceptCodsLicsDD_0': '15'},
                encoding='LATIN1'),
                zip='hi_cruce_l_ES*.shp'),
            Load_XY(('ST_X(ST_LineInterpolatePoint(ST_GeometryN(geom, 1), 0.5))',), ('ST_Y(ST_LineInterpolatePoint(ST_GeometryN(geom, 1), 0.5))',),
                select = {'tipo_cruce': '26002'} ),  # Puente
            Conflate(
                select = Select(
                    types = ['ways'],
                    tags = [
                        {'highway': True, 'bridge': True},
                        {'railway': True, 'bridge': True},
                        {'waterway': True, 'tunnel': True}] ),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {'bridge': 'yes'},
                    static2 = {'source': self.source},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda x: x and x != 'None', [fields['nombre']]))} )))

    def secuencialDescDir(self):
        return self.config.options['hydro_map'][self.config.options['hydro'][0]]
