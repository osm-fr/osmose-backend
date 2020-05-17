#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015-2016                                 ##
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
import re


class Analyser_Merge_Restaurant_FR_cg71(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8240, id = 11, level = 3, tags = ['merge', 'amenity'],
            title = T_('Restaurant not integrated'))

        start_restaurant = re.compile("^(hôtel-)?restaurant ", flags=re.IGNORECASE)
        final_name = re.compile("/.*$")

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/restaurants-od71",
            u"Les restaurants en Saône-et-Loire - CG71",
            CSV(Source(attribution = u"Département de Saône-et-Loire", millesime = "03/2013",
                    fileUrl = u"https://www.data.gouv.fr/s/resources/restaurants-od71/20180207-141445/CG71Restaurants.csv", encoding = "ISO-8859-15"),
                separator = u";"),
            Load("LONGITUDE", "LATITUDE",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "restaurant"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {"amenity": "restaurant"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "amenity": lambda fields: self.amenity_type.get(fields["CATEGORIE"]) or "restaurant",
                        "name": lambda fields: final_name.sub('', start_restaurant.sub('', fields["NOM"])),
                        "tourism": lambda fields: "hotel" if fields["TYPE_RESTAURATION"] == u"Hotel-restaurant" else None,
                        "cuisine": lambda fields: self.cuisine(fields),
                        "website": "SITE_WEB",
                        "stars": lambda fields: len(fields["note_Guide_Rouge_Michelin"]) if fields["note_Guide_Rouge_Michelin"] else None},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["NOM"], fields["TYPE_RESTAURATION"], fields["CATEGORIE"], fields["ADRESSE1"], fields["ADRESSE2"], fields["ADRESSE3"], fields["VILLE"]]))} )))

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
        categorie = fields["CATEGORIE"]
        if self.amenity_type.get(categorie) == "restaurant":
            if fields["CATEGORIE"] in self.cuisine_categorie:
                return self.cuisine_categorie[categorie]
        return None
