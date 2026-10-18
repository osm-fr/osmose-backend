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


class Analyser_Merge_Hydrants_FR_SDIS_58(_Analyser_Merge_Afigeo_Hydrants):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Afigeo_Hydrants.__init__(self, config,
            source_url='https://ideo.data.arnia-bfc.fr/databfc/dataset/points-deau-incendies-du-service-departemental-incendie-et-secours-de-la-nievre-sdis-58/informations',
            dataset_name='oints d\'eau incendies (PEI) du Service Départemental Incendie et Secours de la Nièvre (SDIS 58)',
            source=Source(attribution='Service départemental d\'incendie et de secours de la Nièvre (SDIS 58)',
                millesime='2026-09',
                fileUrl='https://ckan2.data.arnia-bfc.fr/dataset/b35bbd27-a5db-46f1-97d0-725c4722df45/resource/5b1dcef2-0a54-4547-8a0f-3bdc26fb2c16/download/poteaux_bouches_sdis58.zip'),
            srid=2154,
            osmRef='ref:FR:SDIS39',
            logger=logger)
