#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
from .Analyser_Merge import Analyser_Merge_Point, Source, GeoJSON, Load_XY, Conflate, Select, Mapping


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
            u"http://www.prix-carburants.economie.gouv.fr/rubrique/opendata/",
            u"Prix des carburants en France",
            GeoJSON(Source(attribution = u"Ministère de l'Economie, de l'Industrie et du Numérique", millesime = "03/2020",
                    fileUrl = u"https://data.openfuelmap.net/carburants_gouv.geojson"),
                extractor = lambda geojson: geojson),
            Load_XY("geom_x", "geom_y"),
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
                        "fuel:e85": lambda res: "yes" if res["prices.E85"] else Mapping.delete_tag,
                        "fuel:lpg": lambda res: "yes" if res["prices.GPLc"] else Mapping.delete_tag,
                        "fuel:e10": lambda res: "yes" if res["prices.E10"] else Mapping.delete_tag,
                        "fuel:octane_95": lambda res: "yes" if res["prices.SP95"] else Mapping.delete_tag,
                        "fuel:octane_98": lambda res: "yes" if res["prices.SP98"] else Mapping.delete_tag,
                        "fuel:diesel": lambda res: "yes" if res["prices.Gazole"] else Mapping.delete_tag,
                        "vending_machine": lambda res: "fuel" if res["services"] and "Automate CB 24/24" in res["services"] else None,
                        "toilets": lambda res: "yes" if res["services"] and "Toilettes publiques" in res["services"] else None,
                        "compressed_air": lambda res: "yes" if res["services"] and "Station de gonflage" in res["services"] else None,
                        "shop": lambda res: ";".join(filter(lambda x: x, (
                            "convenience" if res["services"] and "Boutique alimentaire" in res["services"] else None,
                            "gas" if res["services"] and "Vente de gaz domestique (Butane, Propane)" in res["services"] else None,
                        ))),
                        "hgv:lanes": lambda res: "yes" if res["services"] and "Piste poids lourds" in res["services"] else None,
                        "vending": lambda res: "fuel" if res["services"] and "Automate CB 24/24" in res["services"] else None},
                text = lambda tags, fields: {"en": "{0}, {1}".format(fields["addr"], fields["city"])} )))
