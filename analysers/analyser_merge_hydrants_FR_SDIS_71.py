#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Antonin Delpeuch 2020                                      ##
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


class Analyser_Merge_Hydrants_FR_SDIS_71(_Analyser_Merge_Afigeo_Hydrants):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Afigeo_Hydrants.__init__(self, config,
            source_url='https://trouver.ternum-bfc.fr/dataset/points-deau-incendie-repertories-en-saone-et-loire',
            dataset_name='Points d\'eau incendie répertoriés en Saône-et-Loire',
            source=Source(attribution='Service départemental d\'incendie et de secours 71',
                millesime='2022-02',
                fileUrl='https://trouver.ternum-bfc.fr/dataset/59d07ea2-ca9a-444a-b977-0e32b280af1c/resource/5b76d323-d0b6-404b-9156-133b688aa9ca/service_proxy?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAME=pei_a3260f9&OUTPUTFORMAT=geojson&CRSNAME=EPSG:4326'),
            osmRef='ref:FR:SDIS71',
            logger=logger)
