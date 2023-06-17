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


class Analyser_Merge_Hydrants_FR_SDIS_21(_Analyser_Merge_Afigeo_Hydrants):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Afigeo_Hydrants.__init__(self, config,
            source_url='https://trouver.ternum-bfc.fr/dataset/points-deau-incendie-pei-du-sdis-cote-dor',
            dataset_name='Points d\'eau incendie (PEI) du SDIS Côte d\'Or',
            source=Source(attribution='Service Départemental d\'Incendie et de Secours de la Côte d\'Or (SDIS21) Service Prévision',
                millesime='2023-07',
                fileUrl='https://trouver.ternum-bfc.fr/dataset/230e8d9c-8a4d-446c-b910-7d1f85aff047/resource/b991c949-8068-4f9d-ba6a-7765eb2e0504/service_proxy?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAME=poteaux_incendie_a11c796&OUTPUTFORMAT=geojson&CRSNAME=EPSG:4326'),
            osmRef='ref:FR:SDIS21',
            logger=logger)
