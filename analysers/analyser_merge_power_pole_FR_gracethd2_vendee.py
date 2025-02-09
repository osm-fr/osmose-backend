#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe - 2024                                    ##
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

from .Analyser_Merge_power_pole_FR_gracethd2 import Analyser_Merge_power_pole_FR_gracethd2
from .Analyser_Merge import SourceDataGouv

class Analyser_Merge_power_pole_FR_gracethd2_vendee(Analyser_Merge_power_pole_FR_gracethd2):
    def __init__(self, config, logger = None):
        Analyser_Merge_power_pole_FR_gracethd2.__init__(self, config,
            source_url='https://www.data.gouv.fr/fr/datasets/appuis-aeriens-enedis-utilises-dans-le-cadre-du-deploiement-de-la-fibre-sur-le-rip-de-la-vendee/',
            dataset_name='Appuis aériens ENEDIS utilisés dans le cadre du déploiement de la Fibre sur le RIP de la Vendée',
            source=SourceDataGouv(
                attribution="Vendée Numérique",
                dataset="673d09a837eab9c52f42268b",
                resource="cc66ae17-26a2-43f5-aea3-37496775776c"),
            conflationDistance=5,
            classs=1010,
            extract_operator = {
                'ENEDIS': 'Enedis'
            },
            logger=logger)
