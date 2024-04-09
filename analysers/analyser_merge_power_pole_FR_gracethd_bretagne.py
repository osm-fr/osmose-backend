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

class Analyser_Merge_power_pole_FR_gracethd_bretagne(Analyser_Merge_power_pole_FR_gracethd):
    def __init__(self, config, logger = None):
        Analyser_Merge_power_pole_FR_gracethd.__init__(self, config,
            source_url='https://www.data.gouv.fr/fr/datasets/recensement-poteaux-enedis-reutilises-dans-le-cadre-du-deploiement-ftth-du-projet-bretagne-tres-haut-debit/',
            dataset_name='Recensement poteaux ENEDIS réutilisés dans le cadre du déploiement FTTH du projet Bretagne Très Haut Débit',
            source=SourceDataGouv(
                attribution="Mégalis Bretagne",
                dataset="6613a43e5b40aaa8022d3787",
                resource="b00051b6-69e5-42c3-8229-f6b556561d83"),
            srid = 2154,
            conflationDistance=5,
            classs=1000,
            extract_operator = {
                'ORMB0000000003': 'Enedis'
            },
            logger=logger)
