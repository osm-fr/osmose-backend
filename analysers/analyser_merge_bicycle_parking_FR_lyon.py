#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights XioNoX 2024                                                ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, GeoJSON, Load_XY, Conflate, Select, Mapping

class Analyser_Merge_Bicycle_Parking_FR_Lyon(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8150, id = 1, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking not integrated'))
        self.def_class_possible_merge(item = 8151, id = 3, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking integration suggestion'))
        self.def_class_update_official(item = 8152, id = 4, level = 3, tags = ['merge', 'public equipment', 'bicycle', 'fix:survey', 'fix:picture'],
            title = T_('Bicycle parking update'))
        self.init(
            "https://www.data.gouv.fr/fr/datasets/parcs-de-stationnement-velos-de-la-metropole-de-lyon/",
            "Localisation des stationnements vélos connus sur le territoire de la Métropole de Lyon",
            GeoJSON(
                Source(attribution = "Métropole de Lyon",
                    fileUrl = "https://data.grandlyon.com/geoserver/metropole-de-lyon/ows?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=metropole-de-lyon:pvo_patrimoine_voirie.pvostationnementvelo&outputFormat=application/json&SRSNAME=EPSG:4326"),
            ),
            Load_XY("geom_x", "geom_y", select = {"validite": "Validé"}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "bicycle_parking"}),
                conflationDistance = 10,
                mapping = Mapping(
                    static1 = {"amenity": "bicycle_parking"},
                    static2 = {"source": self.source,
                    },
                    mapping1 = {
                        "capacity": "capacite",
                        "bicycle_parking": lambda res: self.bicycle_parking.get(res.get("mobiliervelo")),
                        "covered": lambda res: "yes" if res.get("abrite") == "true" else "no",
                    },
                    mapping2 = {
                        "start_date": "anneerealisation",
                        "ref:FR:GrandLyon": "nom",
                        "operator": lambda res: None if res.get("gestionnaire") == "Autre" else res.get("gestionnaire"),
                    })))

    bicycle_parking = {
        None: None,
        'Wilmotte': 'stands',
        'En U inversé': 'stands',
        'Consigne collective': 'shed',
        'Consigne individuelle': 'lockers',
    }
