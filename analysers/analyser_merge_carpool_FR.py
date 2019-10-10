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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Carpool_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 41, "level": 3, "tag": ["merge", "parking", "carpool"], "desc": T_(u"Carpool parking not integrated") }
        self.possible_merge   = {"item":"8131", "class": 43, "level": 3, "tag": ["merge", "parking", "carpool"], "desc": T_(u"Carpool parking integration suggestion") }
        self.update_official  = {"item":"8132", "class": 44, "level": 3, "tag": ["merge", "parking", "carpool"], "desc": T_(u"Carpool parking update") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/base-nationale-consolidee-des-lieux-de-covoiturage",
            u"Base nationale consolidée des lieux de covoiturage",
            CSV(Source(attribution = u"Transport.data.gouv.fr", millesime = "09/2019", encoding = "utf-8-sig",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/e0962ca4-2fb9-4257-a569-56704df3243d"), separator = u";", universalNewLine = True),
            Load("Xlong", "Ylat",
                select = {
                    "ouvert": u"true"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [{"amenity": "parking", "carpool": "yes"}, {"amenity":"car_pooling"}, {"amenity":"parking", "carpool":"designated"}]),
                osmRef = "ref:FR:BNCLC",
                conflationDistance = 300,
                generate = Generate(
                    static1 = {"amenity": "parking", "carpool": "designated"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:BNCLC": "id_lieu",
                        "name": "nom_lieu",
                        "capacity": "nbre_pl",
                        "capacity:disabled": "nbre_pmr",
                        "lit": lambda res: "yes" if res["lumiere"] == "true" else ("no" if res["lumiere"] == "false" else None)},
                    text = lambda tags, fields: T_f(u"Carpool parking {0}", fields[u"nom_lieu"]) )))
