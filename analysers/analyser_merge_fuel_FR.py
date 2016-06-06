#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Fuel_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8200", "class": 1, "level": 3, "tag": ["merge", "highway"], "desc": T_(u"Gas station not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            "http://www.prix-carburants.economie.gouv.fr/rubrique/opendata/",
            u"Prix des carburants en France",
            CSV(Source(file = "fuel_FR.csv.bz2")),
            Load("lon", "lat", table = "fuel_FR"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "fuel"}),
                conflationDistance = 300,
                generate = Generate(
                    static = {
                        "amenity": "fuel",
                        "source": "Ministère de l'Economie, de l'Industrie et du Numérique - 15/09/2014"},
                    mapping = {
                        "fuel:e85": lambda res: "yes" if res["E85"] == "x" else None,
                        "fuel:lpg": lambda res: "yes" if res["GPLc"] == "x" else None,
                        "fuel:lpg": lambda res: "yes" if res["GPL"] == "x" else None,
                        "fuel:e10": lambda res: "yes" if res["E10"] == "x" else None,
                        "fuel:octane_95": lambda res: "yes" if res["SP95"] == "x" else None,
                        "fuel:octane_98": lambda res: "yes" if res["SP98"] == "x" else None,
                        "fuel:diesel": lambda res: "yes" if res["Gazole"] == "x" else None,
                        "vending_machine": lambda res: "fuel" if res["Automate CB"] == "x" else None,
                        "opening_hours": lambda res: "24/7" if res["debut"] != "" and res["debut"] == res["fin"] and res["saufjour"] == "" else None,
                        "toilets": lambda res: "yes" if res["Toilettes publiques"] == "x" else None,
                        "compressed_air": lambda res: "yes" if res["Station de gonflage"] == "x" else None,
                        "shop": lambda res: ";".join(filter(lambda x: x, (
                            "convenience" if res["Boutique alimentaire"] == "x" else None,
                            "gaz" if res["Vente de gaz domestique"] == "x" else None,
                            ))),
                        "hgv:lanes": lambda res: "yes" if res["Piste poids lourds"] == "x" else None,
                        "vending": lambda res: "fuel" if res["Automate CB"] == "x" else None},
                text = lambda tags, fields: {"en": u"%s, %s" % (fields["adresse"], fields["ville"])} )))
