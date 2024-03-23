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

from .Analyser_Merge_power_pole_FR_gracethd import Analyser_Merge_power_pole_FR_gracethd
from .Analyser_Merge import SourceDataGouv

class Analyser_Merge_power_pole_FR_gracethd_dordogne(Analyser_Merge_power_pole_FR_gracethd):
    def __init__(self, config, logger = None):
        Analyser_Merge_power_pole_FR_gracethd.__init__(self, config,
            source_url='https://www.data.gouv.fr/fr/datasets/appuis-aeriens-enedis-utilises-dans-le-cadre-du-deploiement-de-la-fibre-sur-le-rip-de-la-dordogne/',
            dataset_name='Appuis aériens ENEDIS utilisés dans le cadre du déploiement de la Fibre sur le RIP de la Dordogne',
            source=SourceDataGouv(
                attribution="Syndicat Mixte Périgord Numérique",
                dataset="659d72fb641c7c0d6fe6cc59",
                resource="82e49c1f-976f-4be7-ab20-0a58e9badb56"),
            srid = 2154,
            conflationDistance=5,
            classs=1000,
            extract_operator = {
                'OR000000000003': 'Enedis'
            },
            logger=logger)
