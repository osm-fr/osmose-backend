#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe - 2023                                    ##
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

from .analyser_merge_eclext_FR import Analyser_merge_Eclext_FR
from .Analyser_Merge import Source


class Analyser_Merge_Eclext_FR_Syane(Analyser_merge_Eclext_FR):
    def __init__(self, config, logger = None):
        Analyser_merge_Eclext_FR.__init__(self, config,
            source_url='https://www.data.gouv.fr/fr/datasets/points-lumineux-declairage-public-exterieur-dont-le-syane-est-exploitant-haute-savoie/',
            dataset_name='Points lumineux d\'éclairage public extérieur dont le Syane est exploitant (Haute-Savoie)',
            source=Source(attribution='Syane',
                millesime='2023-04',
                fileUrl='https://www.data.gouv.fr/fr/datasets/r/011aa541-8510-4caf-8a00-43d7efbe7543'),
            srid = 2154,
            osmRef='ref',
            logger=logger)
