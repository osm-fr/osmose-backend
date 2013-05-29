#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013                                      ##
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
from Analyser_Merge import Analyser_Merge


class _Analyser_Merge_ServicePublic_FR(Analyser_Merge):

    create_table = """
        id VARCHAR(254),
        pivot VARCHAR(254),
        nom VARCHAR(254),
        lat VARCHAR(254),
        lon VARCHAR(254),
        acc VARCHAR(254)
    """

    def __init__(self, config, logger, clas, select, osmTags, defaultTag):
        self.missing_official = {"item":"8110", "class": clas, "level": 3, "tag": ["merge"], "desc":{"fr":u"Service public non intégrée"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://lecomarquage.service-public.fr/index.php"
        # http://lecomarquage.service-public.fr/donnees_locales_v2/
        self.officialName = "Service-Public.fr"
        self.csv_file = "merge_data/co-marquage-service-public.csv"
        self.csv_select = {
            "pivot": select
        }
        self.osmTags = osmTags
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "serive_public"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Service-Public.fr - 05/2013",
        }
        self.defaultTag.update(defaultTag)
        self.defaultTagMapping = {
            "name": "nom",
        }
        self.conflationDistance = 300
        self.text = lambda tags, fields: {"fr": tags["name"]}


class Analyser_Merge_ServicePublic_FR_Mairie(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 1, "mairie", {"amenity": "townhall"}, {"amenity": "townhall"})

class Analyser_Merge_ServicePublic_FR_Gendarmerie(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 2, "gendarmerie", {"amenity": "police"}, {"amenity": "police", "police:FR": "gendarmerie"})

class Analyser_Merge_ServicePublic_FR_Police(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 3, "commissariat_police", {"amenity": "police"}, {"amenity": "police", "police:FR": "police"})

class Analyser_Merge_ServicePublic_FR_EPIC(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 4, "epic", {"office": "administrative"}, {"office": "administrative"})

class Analyser_Merge_ServicePublic_FR_Pole_Emploi(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 5, "pole_emploi", {"office": "employment_agency"}, {"office": "employment_agency"})

class Analyser_Merge_ServicePublic_FR_Tribunal(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 6, ["ta", "ti", "tribunal_commerce", "tgi", "te", "cour_appel"], {"amenity": "courthouse"}, {"amenity": "courthouse"})

class Analyser_Merge_ServicePublic_FR_Prison(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 7, ["maison_centrale", "maison_arret", "centre_penitentiaire", "centre_detention", "csl"], {"amenity": "prison"}, {"amenity": "prison"})

class Analyser_Merge_ServicePublic_FR_Prefecture(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 8, ["prefecture", "sous_pref"], {"office": "government"}, {"office": "government"})

class Analyser_Merge_ServicePublic_FR_CG_CR(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 9, ["cg", "cr"], {"office": "administrative"}, {"office": "administrative"})
