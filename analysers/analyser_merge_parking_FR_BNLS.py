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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Parking_FR_BNLS(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)

        doc_main = dict(
            detail = T_(
'''It is not because it is from and OpenData source that it is good data. Review it before integrating. Your are an OSM contributors, not a machin to do blind import.'''),
            fix = T_(
'''If after review you are sure that it is a new data and right for OpenStreetMap, then you can add it.'''),
            trap = T_(
'''Be sure there is not existing it in an other place.'''))

        doc_missing_official = self.merge_docs(doc_main,
            detail = T_(
'''This is issue if from an OpenData source, without any prior individual verification on this same issue.'''))
        doc_possible_merge = self.merge_docs(doc_main,
            detail = T_(
'''This is a integration suggestion, mixing OpenData source and OpenStreetMap.'''))
        doc_update_official = self.merge_docs(doc_main,
            detail = T_(
'''This is an update suggestion because there is the same ref in opendatabase and OSM.'''))

        doc_detail = T_(
'''This parking is referenced in the database of car parks managed by local authorities in France, off-street.

See [the mapping](https://wiki.openstreetmap.org/wiki/France/data.gouv.fr/Base_nationale_des_lieux_de_stationnement)
on the wiki. Add a node or add tags if already existing.''')

        self.missing_official = self.def_class(item = 8130, id = 1, level = 3, tags = ['merge', 'parking'], **self.merge_docs(doc_missing_official,
            title = T_f('{0} parking not integrated', 'BNLS'),
            detail = doc_detail)),
        self.possible_merge = self.def_class(item = 8131, id = 3, level = 3, tags = ['merge', 'parking'], **self.merge_docs(doc_possible_merge,
            title = T_f('{0} parking integration suggestion', 'BNLS'),
            detail = doc_detail,
            trap = T_(
'''It is not street parking, it is only closed (with or without fee, for all or not...)'''))),
        self.update_official = self.def_class(item = 8132, id = 4, level = 3, tags = ['merge', 'parking'], **self.merge_docs(doc_update_official,
            title = T_f('{0} parking  update', 'BNLS'),
            detail = doc_detail))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/base-nationale-des-lieux-de-stationnement/",
            "Base Nationale des Lieux de Stationnement",
            CSV(Source(attribution = "Équipe du Point d'Accès National", millesime = "2020/04/30",
                    fileUrl = "https://www.data.gouv.fr/fr/datasets/r/9723bb08-b38d-4ce6-88a9-81f3e366d316"),
                separator = ";"),
            Load("Xlong", "Ylat",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "parking"}),
                conflationDistance = 200,
                osmRef = "ref:FR:BNLS",
                generate = Generate(
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
                    text = lambda tags, fields: {"en": u"Parking %s" % tags["name"]} )))
