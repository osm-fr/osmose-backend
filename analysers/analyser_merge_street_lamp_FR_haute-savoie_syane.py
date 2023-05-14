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

from .Analyser_Merge_street_lamp_FR_eclext import Analyser_Merge_street_lamp_FR_eclext
from .Analyser_Merge import SourceDataGouv


class Analyser_Merge_Eclext_FR_Syane(Analyser_Merge_street_lamp_FR_eclext):
    def __init__(self, config, logger = None):
        Analyser_Merge_street_lamp_FR_eclext.__init__(self, config,
            source_url='https://www.data.gouv.fr/fr/datasets/points-lumineux-declairage-public-exterieur-dont-le-syane-est-exploitant-haute-savoie/',
            dataset_name='Points lumineux d\'éclairage public extérieur dont le Syane est exploitant (Haute-Savoie)',
            source=SourceDataGouv(
                attribution="Syane",
                dataset="6447bfe8709c0b4a2b88355a",
                resource="011aa541-8510-4caf-8a00-43d7efbe7543"),
            srid = 2154,
            osmRef='ref',
            logger=logger)
