#!/usr/bin/env python
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
            source_url='https://ideo.data.arnia-bfc.fr/databfc/dataset/points-deau-incendie-repertories-en-saone-et-loire/informations',
            dataset_name='Points d\'eau incendie (pei) répertoriés en Saône-et-Loire (71)',
            source=Source(attribution='Service départemental d\'incendie et de secours de Saône-et-Loire (SDIS 71)',
                millesime='2026-09',
                fileUrl='https://ckan2.data.arnia-bfc.fr/dataset/d34769e3-e696-41da-a841-bd7665b8574c/resource/5411d34f-af20-4a29-94f8-38a63e93fe65/download/pei.zip'),
            srid=4326,
            osmRef='ref:FR:SDIS71',
            logger=logger)
