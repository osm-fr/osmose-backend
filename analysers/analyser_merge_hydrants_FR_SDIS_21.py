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


class Analyser_Merge_Hydrants_FR_SDIS_21(_Analyser_Merge_Afigeo_Hydrants):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Afigeo_Hydrants.__init__(self, config,
            source_url='https://ideo.data.arnia-bfc.fr/databfc/dataset/points-deau-incendie-pei-du-sdis-cote-dor/informations',
            dataset_name='Points d\'eau incendie (PEI) du SDIS Côte d\'Or',
            source=Source(attribution='Service Départemental d\'Incendie et de Secours de la Côte d\'Or (SDIS21)',
                millesime='2026-09',
                fileUrl='https://ckan2.data.arnia-bfc.fr/dataset/9b0ff096-fdb9-46b2-8c66-d9dfeb12c01d/resource/929f4a04-6707-497d-aab0-0e8c6bd912ae/download/poteaux.zip'),
            srid=2154,
            osmRef='ref:FR:SDIS21',
            logger=logger)
