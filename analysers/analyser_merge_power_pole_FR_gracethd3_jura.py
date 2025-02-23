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

from .Analyser_Merge_power_pole_FR_gracethd3 import Analyser_Merge_power_pole_FR_gracethd3
from .Analyser_Merge import SourceDataGouv

class Analyser_Merge_power_pole_FR_gracethd3_jura(Analyser_Merge_power_pole_FR_gracethd3):
    def __init__(self, config, logger = None):
        Analyser_Merge_power_pole_FR_gracethd3.__init__(self, config,
            source_url='https://www.data.gouv.fr/fr/datasets/appuis-aeriens-enedis-utilises-dans-le-cadre-du-deploiement-de-la-fibre-sur-le-rip-du-jura/',
            dataset_name='Appuis aériens ENEDIS utilisés dans le cadre du déploiement de la Fibre sur le RIP du Jura',
            source=SourceDataGouv(
                attribution="SIDEC Jura",
                dataset="66158cdd04686348037417af",
                resource="3f427bbd-f2bb-49dc-9457-c0aad16b1529"),
            conflationDistance=5,
            classs=1040,
            extract_operator = {
                'OR00000003': ['Enedis', 'Q3587594']
            },
            logger=logger)
