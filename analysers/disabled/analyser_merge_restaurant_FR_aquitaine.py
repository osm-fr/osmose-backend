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

from .Analyser_Merge import Analyser_Merge, Source, JSON, Load, Mapping, Select, Generate


class Analyser_Merge_Restaurant_FR_aquitaine(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8240, id = 1, level = 3, tags = ['merge', 'amenity'],
            title = T_('Restaurant not integrated'))

        self.init(
            u"http://catalogue.datalocale.fr/dataset/liste-restaurants-aquitaine",
            u"Liste des restaurants en Aquitaine",
            JSON(Source(attribution = u"Réseau SIRTAQUI - Comité Régional de Tourisme d'Aquitaine - www.sirtaqui-aquitaine.com", millesime = "06/2016",
                    fileUrl = u"http://wcf.tourinsoft.com/Syndication/aquitaine/e150e425-fbb6-4e32-916b-5bfc47171c3c/Objects?$format=json"),
                extractor = lambda json: json['d']),
            Load("LON", "LAT",
                select = {
                    'TYPRES': [u"Restaurant", u"Hôtel restaurant", u"Ferme auberge"],
                    'CATRES': list(self.amenity_type.keys())},
                xFunction = self.degree,
                yFunction = self.degree),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": ["restaurant", "fast_food", "bar", "pub", "cafe"]}),
                conflationDistance = 200,
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {
                        "amenity": lambda fields: self.amenity_type[fields["CATRES"]],
                        "name": "NOMOFFRE",
                        "ref:FR:CRTA": "SyndicObjectID",
                        "tourism": lambda fields: "hotel" if fields["TYPRES"] == u"Hôtel restaurant" else None,
                        "cuisine": lambda fields: self.cuisine(fields),
                        "diet:kosher": lambda fields: "yes" if fields["SPECIALITES"] and u"Cuisine casher" in fields["SPECIALITES"] else None,
                        "diet:vegetarian ": lambda fields: "yes" if fields["SPECIALITES"] and u"Cuisine végétarienne" in fields["SPECIALITES"] else None,
                        "organic": lambda fields: "only" if fields["SPECIALITES"] and u"Cuisine bio" in fields["SPECIALITES"] else None,
                        "website": lambda fields: None if not fields["URL"] else fields["URL"] if fields["URL"].startswith('http') else 'http://' + fields["URL"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["TYPRES"], fields["CATRES"], fields["SPECIALITES"], fields["NOMOFFRE"], fields["AD1"], fields["AD1SUITE"], fields["AD2"], fields["AD3"], fields["CP"], fields["COMMUNE"]]))} )))


    amenity_type = {
        u"Bistrot / bar à vin": "bar",
        u"Brasserie": "restaurant",
        u"Cafétéria": "restaurant",
        u"Cidrerie": "pub",
        u"Crêperie": "restaurant",
        u"Grill": "restaurant",
        u"Pizzeria": "restaurant",
        u"Restaurant à thème": "restaurant",
        u"Restaurant gastronomique": "restaurant",
        u"Restaurant traditionnel": "restaurant",
        u"Restauration rapide": "fast_food",
        u"Rôtisserie": "restaurant",
        u"Salon de thé": "cafe",
    }

    cuisine_categorie = {
        u"Crêperie": "crepe",
        u"Grill": "steak_house",
        u"Pizzeria": "pizza",
        u"Restaurant gastronomique": "fine_dining",
    }

    cuisine_specialite = {
        u"Cuisine africaine": "african",
        u"Cuisine asiatique": "asian",
#        u"Cuisine des Iles": "",
#        u"Cuisine diététique": "",
        u"Cuisine européenne": "european",
        u"Cuisine gastronomique": "fine_dining",
        u"Cuisine indienne": "indian",
        u"Cuisine méditerranéenne": "mediterranean",
        u"Cuisine nord-américaine": "american",
        u"Cuisine sud-américaine": "latin_american",
#        u"Cuisine traditionnelle": "regional",
        u"Glaces": "ice_cream",
#        u"Nouvelle cuisine française": "",
        u"Poisson / fruits de mer": "seafood",
        u"Régionale française": "regional",
        u"Salades": "salad",
        u"Sandwichs": "sandwich",
        u"Tapas": "tapas",
        u"Tartes": "pie",
#        u"Viandes": "",
    }

    def cuisine(self, fields):
        categorie = fields["CATRES"]
        if self.amenity_type.get(categorie) == "restaurant":
            if fields["CATRES"] in self.cuisine_categorie:
                return self.cuisine_categorie[categorie]
            if fields["SPECIALITES"] in self.cuisine_specialite:
                return self.cuisine_specialite[fields["SPECIALITES"]]
            if fields["SPECIALITES"] and (u"Régionale française" in fields["SPECIALITES"] or u"Cuisine traditionnelle" in fields["SPECIALITES"]):
                return "regional"
            if fields["SPECIALITES"] and u"Sandwichs" in fields["SPECIALITES"]:
                return "sandwich"
        return None
