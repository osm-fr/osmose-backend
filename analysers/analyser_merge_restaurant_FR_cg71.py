#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015                                      ##
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
import re


class Analyser_Merge_Restaurant_FR_cg71(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8240", "class": 11, "level": 3, "tag": ["merge", "amenity"], "desc": T_(u"Restaurant not integrated") }
        self.possible_merge   = {"item":"8241", "class": 13, "level": 3, "tag": ["merge", "amenity"], "desc": T_(u"Restaurant, integration suggestion") }

        latlon = re.compile(",(4[0-9])([0-9]+),([0-9])([0-9]+),")
        start_restaurant = re.compile("^(hôtel-)?restaurant ", flags=re.IGNORECASE)
        final_name = re.compile("/.*$")

        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://opendata71interactive.cloudapp.net/DataBrowser/data/CG71Restaurants",
                name = u"Les restaurants en Saône-et-Loire - CG71",
                file = "restaurant_FR_cg71.csv.bz2",
                csv = CSV(quote = "$")),
            Load("longitude", "latitude", table = "restaurant_cg71",
                filter = lambda text: latlon.sub(",\\1.\\2,\\3.\\4,", text)),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "restaurant"}),
                osmRef = "ref:FR:CG71",
                conflationDistance = 100,
                generate = Generate(
                    static = {
                        "source": u"Conseil général de la Saône-et-Loire - Agence de Développement Touristique - 03/2013",
                        "amenity": "restaurant"},
                    mapping = {
                        "amenity": lambda fields: self.amenity_type.get(fields["categorie"]) or "restaurant",
                        "name": lambda fields: final_name.sub('', start_restaurant.sub('', fields["nom"])),
                        "tourism": lambda fields: "hotel" if fields["type_restauration"] == u"Hotel-restaurant" else None,
                        "cuisine": lambda fields: self.cuisine(fields),
                        "website": "site_web",
                        "stars": lambda fields: len(fields["note_guide_rouge_michelin"]) if fields["note_guide_rouge_michelin"] else None,
                        },
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x != "None", [fields["nom"], fields["type_restauration"], fields["categorie"], fields["adresse1"], fields["adresse2"], fields["adresse3"], fields["ville"]]))} )))

    amenity_type = {
        u"Cafétéria": "restaurant",
        u"Crêperie": "restaurant",
        u"Bistrot": "bar",
        u"Grill": "restaurant",
        u"Restauration rapide": "fast_food",
        u"Restauration à thème": "restaurant",
        u"Brasserie": "restaurant",
        u"Cuisine traditionnelle": "restaurant",
    }

    cuisine_categorie = {
        u"Crêperie": "crepe",
        u"Grill": "steak_house",
        u"Pizzeria": "pizza",
    }

    def cuisine(self, fields):
        categorie = fields["categorie"]
        if self.amenity_type.get(categorie) == "restaurant":
            if fields["categorie"] in self.cuisine_categorie:
                return self.cuisine_categorie[categorie]
        return None
