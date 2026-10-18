#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Fuel_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8200, id = 1, level = 3, tags = ['merge', 'highway', 'fix:imagery', 'fix:survey'],
            title = T_('Gas station not integrated'))
        self.def_class_possible_merge(item = 8201, id = 3, level = 3, tags = ['merge', 'highway', 'fix:imagery', 'fix:survey', 'fix:chair'],
            title = T_('Gas station integration suggestion'))
        self.def_class_update_official(item = 8202, id = 4, level = 3, tags = ['merge', 'highway', 'fix:chair', 'fix:survey'],
            title = T_('Gas station update'))

        self.init(
            "https://www.data.gouv.fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-amelioree/",
            "Prix des carburants en France",
            CSV(
                SourceDataGouv(
                    attribution="Ministère de l'Économie, des Finances et de l'Industrie",
                    dataset="6407d088d4e23dc662022e2c",
                    resource="edd67f5b-46d0-4663-9de9-e5db1c880160",
                    encoding = "utf-8-sig"),
                separator = ";"),
            Load_XY("geom", "geom",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                where = lambda row: row["Carburants disponibles"]),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "fuel"}),
                osmRef = "ref:FR:prix-carburants",
                conflationDistance = 300,
                mapping = Mapping(
                    static1 = {"amenity": "fuel"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:prix-carburants": "id",
                        "fuel:e85": lambda res: "yes" if res["Carburants disponibles"] and "E85" in res["Carburants disponibles"] else None if res["Carburants en rupture temporaire"] and "E85" in res["Carburants en rupture temporaire"] else Mapping.delete_tag,
                        "fuel:lpg": lambda res: "yes" if res["Carburants disponibles"] and "GPLc" in res["Carburants disponibles"] else None if res["Carburants en rupture temporaire"] and "GPLc" in res["Carburants en rupture temporaire"] else Mapping.delete_tag,
                        "fuel:e10": lambda res: "yes" if res["Carburants disponibles"] and "E10" in res["Carburants disponibles"] else None if res["Carburants en rupture temporaire"] and "E10" in res["Carburants en rupture temporaire"] else Mapping.delete_tag,
                        "fuel:octane_95": lambda res: "yes" if res["Carburants disponibles"] and "SP95" in res["Carburants disponibles"] else None if res["Carburants en rupture temporaire"] and "SP95" in res["Carburants en rupture temporaire"] else Mapping.delete_tag,
                        "fuel:octane_98": lambda res: "yes" if res["Carburants disponibles"] and "SP98" in res["Carburants disponibles"] else None if res["Carburants en rupture temporaire"] and "SP98" in res["Carburants en rupture temporaire"] else Mapping.delete_tag,
                        "fuel:diesel": lambda res: "yes" if res["Carburants disponibles"] and "Gazole" in res["Carburants disponibles"] else None if res["Carburants en rupture temporaire"] and "Gazole" in res["Carburants en rupture temporaire"] else Mapping.delete_tag,
                        "vending_machine": lambda res: "fuel" if res["Automate 24-24 (oui/non)"] == "Oui" else None,
                        "toilets": lambda res: "yes" if res["Services proposés"] and "Toilettes publiques" in res["Services proposés"] else None,
                        "compressed_air": lambda res: "yes" if res["Services proposés"] and "Station de gonflage" in res["Services proposés"] else None,
                        "shop": lambda res: ";".join(filter(lambda x: x, (
                            "convenience" if res["Services proposés"] and "Boutique alimentaire" in res["Services proposés"] else None,
                            "gas" if res["Services proposés"] and "Vente de gaz domestique (Butane" in res["Services proposés"] else None,
                        ))),
                        "hgv:lanes": lambda res: "yes" if res["Services proposés"] and "Piste poids lourds" in res["Services proposés"] else None,
                        "vending": lambda res: "fuel" if res["Automate 24-24 (oui/non)"] == "Oui" else None,},
                text = lambda tags, fields: {"en": "{0}, {1}".format(fields["Adresse"], fields["Ville"])} )))
