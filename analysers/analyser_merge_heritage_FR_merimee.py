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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate
from functools import reduce


class Analyser_Merge_Heritage_FR_Merimee(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        Analyser_Merge.__init__(self, config, logger)
        doc = dict(
            detail = T_(
'''A historical monument is here but is not mapped. The list of monuments
comes from the database "Merimee Inventory of monuments" in France by the
Ministry of Culture.'''),
            fix = T_(
'''See [heritage](https://wiki.openstreetmap.org/wiki/Key:heritage) on
wiki. Add a node or to integrate tags if something already existing.'''),
            trap = T_(
'''The position of the markers is made by address geocoding, it may be
located elsewhere. The marker can be a very rough position, located as
low accuracy to the town. Carefully check the contents of the proposed
tags, can be curious or unsuitable values. Do not overide tags of UNESCO
World Heritage.'''))
        self.def_class_missing_official(item = 8010, id = 1, level = 3, tags = ['merge', 'building'],
            title = T_('Historical monument not integrated'), **doc)
        self.def_class_missing_osm(item = 7080, id = 2, level = 3, tags = ['merge'],
            title = T_('Historical monument without tag "ref:mhs" or invalid'), **doc)
        self.def_class_possible_merge(item = 8011, id = 3, level = 3, tags = ['merge'],
            title = T_('Historical monument, integration suggestion'), **doc)
        self.def_class_update_official(item = 8012, id = 4, level = 3, tags = ['merge'],
            title = T_('Historical monument update'), **doc)

        def parseDPRO(dpro):
            ret = None
            # Match YYYY ou YYYY/MM ou YYYY/MM/DD
            match = re.match(r"^(\d{4}(?:/\d{2}(?:/\d{2})?)?) :", dpro)
            if match:
                ret = match.group(1).replace("/", "-")
            return ret

        BLACK_WORDS = [
            u"Eglise protestante", u"Ossuaire (ancien)", u"Polissoir", u"Citadelle",
            u"Sol de maison à maison", u"Boulangerie", u"Domaine du château",
            u"Monument aux morts", u"Château (ruines)", u"Croix du 16e siècle", u"Hôpital",
            u"Tour de l'Horloge", u"Chapelle du cimetière", u"Tumulus", u"Maison Renaissance",
            u"Abbaye (ancienne)", u"Moulin à vent", u"Théâtre municipal",
            u"Croix de carrefour", u"Tour", u"Mairie", u"Prieuré (ancien)", u"Eglise (ancienne)",
            u"Eglise de l'Assomption", u"Hôtel particulier", u"Beffroi", u"Ancienne église",
            u"Restes du château", u"Palais de Justice", u"Remparts", u"Halles",
            u"Croix en pierre", u"Croix du cimetière", u"Ferme", u"Calvaire", u"Motte féodale",
            u"Temple protestant", u"Synagogue", u"Ancien prieuré", u"Eglise paroissiale",
            u"Presbytère", u"Ruines du château", u"Maison du 15e siècle",
            u"Manoir", u"Maison du 16e siècle", u"Halle", u"Château (ancien)", u"Maisons",
            u"Menhir", u"Ancienne abbaye", u"Croix de chemin", u"Maison à pans de bois",
            u"Dolmen", u"Hôtel", u"Ancien château", u"Immeuble", u"Eglise", u"Maison"
        ]

        SKIP = [
            u"Ile-de-France;Paris;Paris 9e Arrondissement;Immeubles aux abords de l'Opéra (voir aussi : 25, 27, 29, 31 bd Haussmann, Immeuble de la Société Générale);19e siècle;Rohaut de Fleury Charles (architecte);Façades et toitures sur rue des immeubles situés 3, 5, 7 rue Auber, 1 rue Boudreau, 4, 6, 8 boulevard des Capucines, 3, 3bis, 5, 7, 9, 11, 13 rue de la Chaussée-d'Antin, 2, 4, 6, 8, 10, 12, 14, 16 rue Halévy, 1 rue des Mathurins, 1, 2, 3, 4, 5, 7 rue Meyerbeer, 9, 11, 11bis, 15, 17 rue Scribe, 2 rue Auber, 7, place Charles-Garnier : inscription par arrêté du 30 décembre 1977, modifiée par arrêtés des 16 mai 2013 et 14 juin 2013;\"1977/12/30 : inscrit MH ; 2013/05/16 : inscrit MH ; 2013/06/14 : inscrit MH\";propriété privée;\"Auber (rue) 2, 3, 5, 7 ; Boudreau (rue) 1 ; Capucines (boulevard des) 4, 6, 8 ; Charles-Garnier (place) 7 ; Chaussée-d'Antin (rue de la) 3 à 13 ; Halévy (rue) 2 à 16 ; Mathurins (rue des) 1 ; Meyerbeer (rue) 1, 2, 3, 4, 5, 7 ; Scribe (rue) 9, 11, 11bis, 15, 17\";75109;;recensement immeubles MH;PA00088922;48.8768961624, 2.33746024139;75;Ile-de-France;ile de france",
            u"Normandie;Calvados;Falaise;Vestiges de l'enceinte fortifiée;\"13e siècle;17e siècle\";;\"Restes de la porte Lecomte : inscription par arrêté du 31 mai 1927 ; Porte des Cordeliers : classement par arrêté du 13 mars 1930 ; Vestiges de l'enceinte fortifiée : de la porte du Château à la porte de Guibray : rue Porte-du-Château 10, 8 (cad. B 67, 68) , rue Blâcher 32, 28, 22, 10, 6 (cad. D 87, 92, 96, 105, 108 à 110). De la porte Guibray à la porte Marescot : rue Amiral-Courbet (cad. D 521, 519, 513, 514, 515, 512, 509). De la porte Marescot à la porte Lecomte : rue Georges-Clémenceau (cad. B 801) , rue Victor-Hugo 15, 17, 19, 21, 23, 25 (cad. B 604, 608, 612, 615) , rue du Sergent-Goubin (cad. B 625). De la porte Lecomte à la route de Caen : rue du Sergent Goubin 24, 22, 20, 2 (cad. B 566, 569, 562, 563, 559, 556, 557, 1058 à 1060) , rue Gambetta 18, 14, 12 (cad. B 1045, 1048, 994, 997). De la route de Caen à la porte Philippe-Jean : rue Frédéric-Gaberon (cad. E 235) , rue des Cordeliers (cad. E 247) , rue du Camp-Ferme (cad. E 354, 364, 365, 370, 383). De la porte Philippe-Jean auchâteau : place Guillaume-le-Conquérant et rue de la Porte-Philippe-Jean (cad. E 585, 572, 578) , place Guillaume-le-Conquérant (cad. E 594, 610, 612, 613) : inscription par arrêté du 19 juin 1951\";\"1927/05/31 : inscrit MH ; 1930/03/13 : classé MH ; 1951/06/19 : inscrit MH\";\"propriété de la commune ; propriété d'une personne privée\";\"Porte-du-Château (rue) ; Blâcher (rue) ; Amiral-Courbet (rue) ; Georges-Clémenceau (rue) ; Victor-Hugo (rue) ; Sergent-Goubin (rue du) ; Gambetta (rue) ; Frédéric-Gaberon (rue) ; Cordeliers (rue des) ; Camp-Ferme (rue du) ; Guillaume-le-Conquérant (place)\";14258;;Recensement immeubles MH;PA00111315;48.8957800281, -0.193401711782;14;Basse-Normandie;basse normandie",
        ]

        self.init(
            u"https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/",
            u"Immeubles protégés au titre des Monuments Historiques",
            CSV(Source(attribution = u"Ministère de la Culture", millesime = "06/2019",
                    fileUrl = u"https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true",
                    filter = lambda s: reduce(lambda a, v: a.replace(v, ''), SKIP, (u'' + s).encode('utf-8').replace(b'l\u92', b"l'").replace(b'\x85)', b"...)").decode('utf-8', 'ignore'))),
                separator = u';'),
            Load("coordonnees_ban", "coordonnees_ban",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0],
                select = {u"Date de Protection": True}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {
#                        "heritage": ["1", "2", "3"],
                        "heritage:operator": None,
                        "ref:mhs": lambda t: "{0} NOT LIKE 'PM%' AND {0} NOT LIKE 'IA%'".format(t)}), # Not a Palissy ref nor "Inventaire général du patrimoine culturel" ref
                osmRef = "ref:mhs",
                conflationDistance = 1000,
                generate = Generate(
                    static1 = {"heritage:operator": "mhs"},
                    static2 = {"source:heritage": self.source},
                    mapping1 = {
                        "ref:mhs": u"Référence",
                        "mhs:inscription_date": lambda res: parseDPRO(res[u"Date de Protection"]),
                        "heritage": lambda res: 2 if res[u"Précision sur la Protection"] and u"classement par arrêté" in res[u"Précision sur la Protection"] else 3 if res[u"Précision sur la Protection"] and u"inscription par arrêté" in res[u"Précision sur la Protection"] else None},
                    mapping2 = {"name": lambda res: res[u"Appellation courante"] if res[u"Appellation courante"] not in BLACK_WORDS else None},
                    tag_keep_multiple_values = ["heritage:operator"],
                    text = lambda tags, fields: T_f(u"Historical monument: {0} (positioned at {1} with confidence {2})", ", ".join(filter(lambda x: x, [fields[u"Date de Protection"], fields[u"Adresse"], fields[u"Commune"]])), fields[u"result_type"], fields[u"result_score"]) )))
