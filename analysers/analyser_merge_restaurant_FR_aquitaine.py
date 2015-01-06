#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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


class Analyser_Merge_Restaurant_FR_aquitaine(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8240", "class": 1, "level": 3, "tag": ["merge", "amenity"], "desc": T_(u"Restaurant not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.sirtaqui-aquitaine.com",
                name = u"Liste des restaurants en Aquitaine",
                file = "restaurant_FR_aquitaine.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ";")),
            Load("LONGITUDE", "LATITUDE", table = "restaurant_FR_aquitaine",
                filter = lambda text: re.sub("(;\"[^\"]+)\r\n", '\\1', text),
                select = {
                    'TYPE': [u"Restaurant", u"Hôtel restaurant", u"Ferme auberge"],
                    'CATEGORIE': self.amenity_type.keys()}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": ["restaurant", "fast_food", "bar", "pub", "cafe"]}),
                conflationDistance = 200,
                generate = Generate(
                    static = {
                        "source": u"Réseau SIRTAQUI - Comité Régional de Tourisme d'Aquitaine - www.sirtaqui-aquitaine.com - 12/2014"},
                    mapping = {
                        "amenity": lambda fields: self.amenity_type[fields["CATEGORIE"]],
                        "ref:FR:CRTA": "Id",
                        "name": "NOM_OFFRE",
                        "tourism": lambda fields: "hotel" if fields["TYPE"] == u"Hôtel restaurant" else None,
                        "cuisine": lambda fields: self.cuisine(fields),
                        "diet:kosher": lambda fields: "yes" if u"Cuisine casher" in fields["SPECIALITES"] else None,
                        "diet:vegetarian ": lambda fields: "yes" if u"Cuisine végétarienne" in fields["SPECIALITES"] else None,
                        "organic": lambda fields: "only" if u"Cuisine bio" in fields["SPECIALITES"] else None,
                        "website": lambda fields: None if not fields["SITE_WEB"] else fields["SITE_WEB"] if fields["SITE_WEB"].startswith('http') else 'http://' + fields["SITE_WEB"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x != "", [fields["TYPE"], fields["CATEGORIE"], fields["SPECIALITES"], fields["NOM_OFFRE"], fields["PORTE_ESCALIER"], fields["BATIMENT_RESIDENCE"], fields["RUE"], fields["LIEUDIT_BP"], fields["CODE_POSTAL"], fields["COMMUNE"]]))} )))

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
        categorie = fields["CATEGORIE"]
        if self.amenity_type.get(categorie) == "restaurant":
            if fields["CATEGORIE"] in self.cuisine_categorie:
                return self.cuisine_categorie[categorie]
            if fields["SPECIALITES"] in self.cuisine_specialite:
                return self.cuisine_specialite[fields["SPECIALITES"]]
            if u"Régionale française" in fields["SPECIALITES"] or u"Cuisine traditionnelle" in fields["SPECIALITES"]:
                return "regional"
            if u"Sandwichs" in fields["SPECIALITES"]:
                return "sandwich"
        return None
