#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien PAVIE 2019                                          ##
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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceDataGouv, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Carpool_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 41, level = 3, tags = ['merge', 'parking', 'carpool'],
            title = T_('Carpool parking not integrated'))
        self.def_class_possible_merge(item = 8131, id = 43, level = 3, tags = ['merge', 'parking', 'carpool'],
            title = T_('Carpool parking integration suggestion'))
        self.def_class_update_official(item = 8132, id = 44, level = 3, tags = ['merge', 'parking', 'carpool'],
            title = T_('Carpool parking update'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/base-nationale-consolidee-des-lieux-de-covoiturage",
            "Base nationale consolidée des lieux de covoiturage",
            CSV(
                SourceDataGouv(
                    attribution="Transport.data.gouv.fr",
                    encoding="utf-8-sig",
                    dataset="5d6eaffc8b4c417cdc452ac3",
                    resource="e0962ca4-2fb9-4257-a569-56704df3243d",
                    filter=lambda text: text.replace('\r', '\n')),
                separator=";"),
            Load("Xlong", "Ylat",
                select = {
                    "ouvert": u"true"}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"amenity": "parking", "carpool": "yes"}, {"amenity":"car_pooling"}, {"amenity":"parking", "carpool":"designated"}]),
                osmRef = "ref:FR:BNCLC",
                conflationDistance = 300,
                mapping = Mapping(
                    static1 = {"amenity": "parking", "carpool": "designated"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:BNCLC": "id_lieu",
                        "name": "nom_lieu",
                        "capacity": "nbre_pl",
                        "capacity:disabled": "nbre_pmr",
                        "lit": lambda res: "yes" if res["lumiere"] == "true" else ("no" if res["lumiere"] == "false" else None)},
                    text = lambda tags, fields: T_("Carpool parking {0}", fields[u"nom_lieu"]) )))
