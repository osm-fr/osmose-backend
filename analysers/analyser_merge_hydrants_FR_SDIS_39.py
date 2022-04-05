#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2022                                      ##
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

from .analyser_merge_hydrants_FR import _Analyser_Merge_Afigeo_Hydrants
from .Analyser_Merge import Source


class Analyser_Merge_Hydrants_FR_SDIS_39(_Analyser_Merge_Afigeo_Hydrants):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Afigeo_Hydrants.__init__(self, config,
            source_url='https://trouver.ternum-bfc.fr/dataset/points-deau-incendie-pei-de-cote-dor-du-sdis-21',
            dataset_name='Points d\'eau incendie du SDIS 39',
            source=Source(attribution='Service départemental d\'incendie et de secours 39',
                millesime='2022-03',
                fileUrl='https://trouver.ternum-bfc.fr/dataset/e2ea75c7-0c44-4894-bd70-6c59a2e665da/resource/806a9dc0-e31d-47a9-ab8d-9da7f6401085/service_proxy?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAME=pei_b80f3a5&OUTPUTFORMAT=geojson&CRSNAME=EPSG:4326'),
            osmRef='ref:FR:SDIS39',
            logger=logger)
