#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping
from functools import reduce


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

        SKIP = [
            "Ile-de-France;Paris;Paris 9e Arrondissement;Immeubles aux abords de l'Opéra (voir aussi : 25, 27, 29, 31 bd Haussmann, Immeuble de la Société Générale);19e siècle;Rohaut de Fleury Charles (architecte);Façades et toitures sur rue des immeubles situés 3, 5, 7 rue Auber, 1 rue Boudreau, 4, 6, 8 boulevard des Capucines, 3, 3bis, 5, 7, 9, 11, 13 rue de la Chaussée-d'Antin, 2, 4, 6, 8, 10, 12, 14, 16 rue Halévy, 1 rue des Mathurins, 1, 2, 3, 4, 5, 7 rue Meyerbeer, 9, 11, 11bis, 15, 17 rue Scribe, 2 rue Auber, 7, place Charles-Garnier : inscription par arrêté du 30 décembre 1977, modifiée par arrêtés des 16 mai 2013 et 14 juin 2013;\"1977/12/30 : inscrit MH ; 2013/05/16 : inscrit MH ; 2013/06/14 : inscrit MH\";propriété privée;\"Auber (rue) 2, 3, 5, 7 ; Boudreau (rue) 1 ; Capucines (boulevard des) 4, 6, 8 ; Charles-Garnier (place) 7 ; Chaussée-d'Antin (rue de la) 3 à 13 ; Halévy (rue) 2 à 16 ; Mathurins (rue des) 1 ; Meyerbeer (rue) 1, 2, 3, 4, 5, 7 ; Scribe (rue) 9, 11, 11bis, 15, 17\";75109;;recensement immeubles MH;PA00088922;48.8768961624, 2.33746024139;75;Ile-de-France;ile de france",
            "Normandie;Calvados;Falaise;Vestiges de l'enceinte fortifiée;\"13e siècle;17e siècle\";;\"Restes de la porte Lecomte : inscription par arrêté du 31 mai 1927 ; Porte des Cordeliers : classement par arrêté du 13 mars 1930 ; Vestiges de l'enceinte fortifiée : de la porte du Château à la porte de Guibray : rue Porte-du-Château 10, 8 (cad. B 67, 68) , rue Blâcher 32, 28, 22, 10, 6 (cad. D 87, 92, 96, 105, 108 à 110). De la porte Guibray à la porte Marescot : rue Amiral-Courbet (cad. D 521, 519, 513, 514, 515, 512, 509). De la porte Marescot à la porte Lecomte : rue Georges-Clémenceau (cad. B 801) , rue Victor-Hugo 15, 17, 19, 21, 23, 25 (cad. B 604, 608, 612, 615) , rue du Sergent-Goubin (cad. B 625). De la porte Lecomte à la route de Caen : rue du Sergent Goubin 24, 22, 20, 2 (cad. B 566, 569, 562, 563, 559, 556, 557, 1058 à 1060) , rue Gambetta 18, 14, 12 (cad. B 1045, 1048, 994, 997). De la route de Caen à la porte Philippe-Jean : rue Frédéric-Gaberon (cad. E 235) , rue des Cordeliers (cad. E 247) , rue du Camp-Ferme (cad. E 354, 364, 365, 370, 383). De la porte Philippe-Jean auchâteau : place Guillaume-le-Conquérant et rue de la Porte-Philippe-Jean (cad. E 585, 572, 578) , place Guillaume-le-Conquérant (cad. E 594, 610, 612, 613) : inscription par arrêté du 19 juin 1951\";\"1927/05/31 : inscrit MH ; 1930/03/13 : classé MH ; 1951/06/19 : inscrit MH\";\"propriété de la commune ; propriété d'une personne privée\";\"Porte-du-Château (rue) ; Blâcher (rue) ; Amiral-Courbet (rue) ; Georges-Clémenceau (rue) ; Victor-Hugo (rue) ; Sergent-Goubin (rue du) ; Gambetta (rue) ; Frédéric-Gaberon (rue) ; Cordeliers (rue des) ; Camp-Ferme (rue du) ; Guillaume-le-Conquérant (place)\";14258;;Recensement immeubles MH;PA00111315;48.8957800281, -0.193401711782;14;Basse-Normandie;basse normandie",
        ]

        self.init(
            "https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/",
            "Immeubles protégés au titre des Monuments Historiques",
            CSV(SourceOpenDataSoft(
                attribution="Ministère de la Culture",
                url="https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques",
                filter=lambda s: reduce(lambda a, v: a.replace(v, ''), SKIP, (u'' + s).encode('utf-8').replace(b'l\u92', b"l'").replace(b'\x85)', b"...)").decode('utf-8', 'ignore')))),
            Load_XY("coordonnees", "coordonnees",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                select = {"Date de protection": True}),
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
                        "ref:mhs": "Référence",
                        "mhs:inscription_date": lambda res: parseDPRO(res["Date de protection"]),
                        "heritage": lambda res: 2 if res["Précision protection"] and "classement par arrêté" in res["Précision protection"] else 3 if res["Précision protection"] and "inscription par arrêté" in res["Précision protection"] else None},
                    mapping2 = {"name": lambda res: res["Appellation courante"] if res["Appellation courante"] not in BLACK_WORDS else None},
                    text = lambda tags, fields: T_("Historical monument: {0}", ", ".join(filter(lambda x: x, [fields["Date de Protection"], fields["Adresse"], fields["Commune"]]))) )))
