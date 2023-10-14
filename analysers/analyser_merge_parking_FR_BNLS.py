#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Vincent Bergeot (thanks Frédéric Rodrigo) 2020             ##
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


class Analyser_Merge_Parking_FR_BNLS(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)

        doc_detail = T_(
'''This parking is referenced in the database of car parks managed by local authorities in France, off-street.

See [the mapping](https://wiki.openstreetmap.org/wiki/France/data.gouv.fr/Base_nationale_des_lieux_de_stationnement)
on the wiki. Add a node or add tags if already existing.''')

        self.missing_official = self.def_class(item = 8130, id = 51, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:survey'],
            title = T_('{0} parking not integrated', 'BNLS'),
            detail = doc_detail)
        self.possible_merge = self.def_class(item = 8131, id = 53, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:chair'],
            title = T_('{0} parking integration suggestion', 'BNLS'),
            detail = doc_detail,
            trap = T_(
'''It is not street parking, it is off-road parking (with or without fee, for all or not...)'''))
        self.update_official = self.def_class(item = 8132, id = 54, level = 3, tags = ['merge', 'parking', 'fix:chair', 'fix:survey'],
            title = T_('{0} parking  update', 'BNLS'),
            detail = doc_detail)

        self.init(
            "https://www.data.gouv.fr/fr/datasets/base-nationale-des-lieux-de-stationnement/",
            "Base Nationale des Lieux de Stationnement",
            CSV(
                SourceDataGouv(
                    attribution="Équipe du Point d'Accès National",
                    encoding="utf-8-sig",
                    dataset="5ea1add4a5a7dac3af82310a",
                    resource="e32f7675-913b-4e01-b8c8-0a29733e4407"),
                separator = ','),
            Load_XY("Xlong", "Ylat",
                xFunction = Load_XY.float_comma,
                yFunction = Load_XY.float_comma),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "parking"}),
                conflationDistance = 200,
                osmRef = "ref:FR:BNLS",
                mapping = Mapping(
                    static1 = {
                        "amenity": "parking"},
                    static2 = {
                        "source": self.source},
                    mapping1 = {
                        "ref:FR:BNLS": "id",
                        "name": "nom",
                        "website": "url",
                        "access": lambda res: "yes" if res["type_usagers"] == "tous" else "customers" if res["type_usagers"] == "abonnés" else None,
                        "fee": lambda res: "yes" if res["gratuit"] == "0" else None,
                        "capacity": lambda res: res["nb_places"] if res["nb_places"] != "0" else None,
                        "capacity:disabled": lambda res: res["nb_pmr"] if res["nb_pmr"] != "0" else None,
                        "capacity:charging": lambda res: res["nb_voitures_electriques"] if res["nb_voitures_electriques"] != "0" else None,
                        "maxheight": lambda res: int(res["hauteur_max"]) / 100 if res["hauteur_max"] != "N/A" else None,
                        "parking": lambda res: "surface" if res["type_ouvrage"] == "enclos_en_surface" else None},
                    text = lambda tags, fields: {"en": "Parking {0}".format(tags["name"])} )))
