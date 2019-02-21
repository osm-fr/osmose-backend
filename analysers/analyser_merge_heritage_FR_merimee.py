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


class Analyser_Merge_Heritage_FR_Merimee(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8010", "class": 1, "level": 3, "tag": ["merge", "building"], "desc": T_(u"Historical monument not integrated") }
        self.missing_osm      = {"item":"7080", "class": 2, "level": 3, "tag": ["merge"], "desc": T_(u"Historical monument without ref:mhs or invalid") }
        self.possible_merge   = {"item":"8011", "class": 3, "level": 3, "tag": ["merge"], "desc": T_(u"Historical monument, integration suggestion") }
        self.update_official  = {"item":"8012", "class": 4, "level": 3, "tag": ["merge"], "desc": T_(u"Historical monument update") }

        def parseDPRO(dpro):
            ret = None;
            # Match YYYY ou YYYY/MM ou YYYY/MM/DD
            match = re.match("^(\d{4}(?:/\d{2}(?:/\d{2})?)?) :", dpro);
            if match:
                ret = match.group(1).replace("/", "-");
            return ret;

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

        Analyser_Merge.__init__(self, config, logger,
            u"https://data.culturecommunication.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/",
            u"Immeubles protégés au titre des Monuments Historiques",
            # Original without accurate location, geocoded with https://adresse.data.gouv.fr/csv
            CSV(Source(attribution = u"Ministère de la Culture", millesime = "07/2018",
                    file = "heritage_FR_merimee.csv.bz2"),
                separator = u';'),
            Load("longitude", "latitude",
                select = {u"Date de Protection": True}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {
#                        "heritage": ["1", "2", "3"],
                        "heritage:operator": None,
                        "ref:mhs": lambda t: "{0} NOT LIKE 'PM%'".format(t)}), # Not a Palissy ref
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
                    text = lambda tags, fields: T_(u"Historical monument: %s (positioned at %s with confidence %s)", ", ".join(filter(lambda x: x, [fields[u"Date de Protection"], fields[u"Adresse"], fields[u"Commune"]])), fields[u"result_type"], fields[u"result_score"]) )))
