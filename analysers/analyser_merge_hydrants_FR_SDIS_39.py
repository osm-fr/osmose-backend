#!/usr/bin/env python
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
            source_url='https://ideo.data.arnia-bfc.fr/databfc/dataset/points-deau-incendie-pei-du-jura-du-sdis-39/informations',
            dataset_name='Points d\'eau Incendie (PEI) du Jura du SDIS 39',
            source=Source(attribution='Service d\'incendie et de secours du Jura (SDIS 39)',
                millesime='2026-09',
                fileUrl='https://ckan2.data.arnia-bfc.fr/dataset/8eb7aa3a-c021-463b-981a-cced646c43d6/resource/b52486dd-fd77-4a0d-9769-3281a5def3a7/download/pei_sdis39_4.zip'),
            srid=2154,
            osmRef='ref:FR:SDIS39',
            logger=logger)
