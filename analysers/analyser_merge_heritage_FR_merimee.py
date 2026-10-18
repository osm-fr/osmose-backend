#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2016                                 ##
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

import re
from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Heritage_FR_Merimee(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        doc = dict(
            detail = T_(
'''A historical monument is here but is not mapped. The list of monuments
comes from the database "Merimee Inventory of monuments" in France by the
Ministry of Culture.'''),
            fix = T_(
'''See [heritage](https://wiki.openstreetmap.org/wiki/Key:heritage) on
wiki. Add the proper tags if something already exists.'''),
            trap = T_(
'''The position of the markers comes from address geocoding. They may be
located elsewhere. The marker can have a very rough position, with
low accuracy to the town. Carefully check the contents of the proposed
tags, there can be curious or unsuitable values. Do not override tags of UNESCO
World Heritage.'''))
        self.def_class_missing_official(item = 8010, id = 1, level = 3, tags = ['merge', 'building', 'historic', 'fix:imagery', 'fix:survey'],
            title = T_('Historical monument not integrated'), **doc)
        self.def_class_missing_osm(item = 7080, id = 2, level = 3, tags = ['merge', 'historic', 'fix:chair'],
            title = T_('Historical monument without tag "ref:mhs" or invalid'), **doc)
        self.def_class_possible_merge(item = 8011, id = 3, level = 3, tags = ['merge', 'historic', 'fix:chair', 'fix:survey'],
            title = T_('Historical monument, integration suggestion'), **doc)
        self.def_class_update_official(item = 8012, id = 4, level = 3, tags = ['merge', 'historic', 'fix:chair', 'fix:survey'],
            title = T_('Historical monument update'), **doc)

        def parseDPRO(dpro):
            ret = None
            # Match YYYY ou YYYY/MM ou YYYY/MM/DD
            match = re.match(r"^(\d{4}(?:/\d{2}(?:/\d{2})?)?) :", dpro)
            if match:
                ret = match.group(1).replace("/", "-")
            return ret

        BLACK_WORDS = [
            "Eglise protestante", "Ossuaire (ancien)", "Polissoir", "Citadelle",
            "Sol de maison à maison", "Boulangerie", "Domaine du château",
            "Monument aux morts", "Château (ruines)", "Croix du 16e siècle", "Hôpital",
            "Tour de l'Horloge", "Chapelle du cimetière", "Tumulus", "Maison Renaissance",
            "Abbaye (ancienne)", "Moulin à vent", "Théâtre municipal",
            "Croix de carrefour", "Tour", "Mairie", "Prieuré (ancien)", "Eglise (ancienne)",
            "Eglise de l'Assomption", "Hôtel particulier", "Beffroi", "Ancienne église",
            "Restes du château", "Palais de Justice", "Remparts", "Halles",
            "Croix en pierre", "Croix du cimetière", "Ferme", "Calvaire", "Motte féodale",
            "Temple protestant", "Synagogue", "Ancien prieuré", "Eglise paroissiale",
            "Presbytère", "Ruines du château", "Maison du 15e siècle",
            "Manoir", "Maison du 16e siècle", "Halle", "Château (ancien)", "Maisons",
            "Menhir", "Ancienne abbaye", "Croix de chemin", "Maison à pans de bois",
            "Dolmen", "Hôtel", "Ancien château", "Immeuble", "Eglise", "Maison"
        ]

        self.init(
            "https://culture.data.gouv.fr/datasets/5af120e5b595087cfabcde81",
            "Immeubles protégés au titre des Monuments Historiques",
            CSV(SourceDataGouv(
                attribution="Ministère de la Culture",
                dataset="5af120e5b595087cfabcde81",
                resource="3a52af4a-f9da-4dcc-8110-b07774dfb3bc"),
                separator = "|"),
            Load_XY("coordonnees_au_format_WGS84", "coordonnees_au_format_WGS84",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                select = {"Date_et_typologie_de_la_protection": True}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {
#                        "heritage": ["1", "2", "3"],
                        "heritage:operator": None,
                        "ref:mhs": lambda t: "{0} NOT LIKE 'PM%' AND {0} NOT LIKE 'IA%'".format(t)}), # Not a Palissy ref nor "Inventaire général du patrimoine culturel" ref
                osmRef = "ref:mhs",
                conflationDistance = 1000,
                tag_keep_multiple_values = ["heritage:operator"],
                mapping = Mapping(
                    static1 = {"heritage:operator": "mhs"},
                    static2 = {"source:heritage": self.source},
                    mapping1 = {
                        "ref:mhs": "Reference",
                        "mhs:inscription_date": lambda res: parseDPRO(res["Date_et_typologie_de_la_protection"]),
                        "heritage": lambda res: 2 if res["Precision_de_la_protection"] and "classement par arrêté" in res["Precision_de_la_protection"] else 3 if res["Precision_de_la_protection"] and "inscription par arrêté" in res["Precision_de_la_protection"] else None},
                    mapping2 = {"name": lambda res: res["Titre_editorial_de_la_notice"] if res["Titre_editorial_de_la_notice"] not in BLACK_WORDS else None},
                    text = lambda tags, fields: T_("Historical monument: {0}", ", ".join(filter(lambda x: x and x != "None", [fields["Date_et_typologie_de_la_protection"], fields["Adresse_forme_index"], fields["Commune_forme_index"]]))) )))
