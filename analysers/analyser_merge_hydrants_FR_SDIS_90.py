#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2026                                      ##
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


class Analyser_Merge_Hydrants_FR_SDIS_90(_Analyser_Merge_Afigeo_Hydrants):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Afigeo_Hydrants.__init__(self, config,
            source_url='https://ideo.data.arnia-bfc.fr/databfc/dataset/points-deau-incendie-pei-pour-le-territoire-de-belfort/informations',
            dataset_name='Points d\'Eau Incendie (PEI) pour le Territoire de Belfort',
            source=Source(attribution='Service d\'incendie et de secours du Territoire de Belfort (SDIS 90)',
                millesime='2026-09',
                fileUrl='https://ckan2.data.arnia-bfc.fr/dataset/eb2716ca-89ac-47c1-b619-b1b57218790f/resource/f8b7dd5f-958b-4ad8-9f01-fa6e842cfcb3/download/d_pei_cd90_p.zip'),
            srid=2154,
            osmRef='ref:FR:SDIS39',
            logger=logger)
