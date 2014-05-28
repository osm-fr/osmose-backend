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

from Analyser_Merge import Analyser_Merge


class _Analyser_Merge_ServicePublic_FR(Analyser_Merge):


    def __init__(self, config, logger, clas, select, osmTags, defaultTag, defaultTagMapping = {}):
        self.missing_official = {"item":"8110", "class": clas, "level": 3, "tag": ["merge"], "desc": T_(u"Public service not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://lecomarquage.service-public.fr/index.php"
        # http://lecomarquage.service-public.fr/donnees_locales_v2/
        self.officialName = "Service-Public.fr"
        self.csv_file = "merge_data/co-marquage-service-public.csv"
        self.csv = False
        self.csv_separator = None
        self.csv_select = {
            "pivot": select
        }
        self.osmTags = osmTags
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "serive_public"
        self.createTable = """
            id VARCHAR(254),
            pivot VARCHAR(254),
            adresse VARCHAR(1024),
            acc VARCHAR(254),
            nom VARCHAR(254),
            lat VARCHAR(254),
            lon VARCHAR(254),
            precision VARCHAR(254)"""
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Service-Public.fr - 06/2013",
        }
        self.defaultTag.update(defaultTag)
        self.accTable = {
            "ACC": "yes",
            "DEM": "limited",
            "NAC": "no",
        }
        self.defaultTagMapping = {
            "wheelchair": lambda res: self.accTable[res["acc"]] if res["acc"] else None,
        }
        self.defaultTagMapping.update(defaultTagMapping)
        self.conflationDistance = 300
        self.prescitionTableEn = {
            "0": "unknown",
            "1": "country",
            "2": "region",
            "3": "sub-region",
            "4": "town",
            "5": "post code",
            "6": "street",
            "7": "intersection",
            "8": "address",
            "9": "building",
        }
        self.prescitionTableFr = {
            "0": u"indeterminé",
            "1": u"au pays",
            "2": u"à la région",
            "3": u"à la sous-région",
            "4": u"au village",
            "5": u"au code postal",
            "6": u"à la rue",
            "7": u"à l'intersection",
            "8": u"à l'address",
            "9": u"au bâtiment",
        }
        self.text = lambda tags, fields: {"en": u"%s, %s (geocoded %s)" % (fields["nom"], fields["adresse"], self.prescitionTableEn[fields["precision"]]), "fr": u"%s, %s (géocodé %s)" % (fields["nom"], fields["adresse"], self.prescitionTableFr[fields["precision"]])}

class _Analyser_Merge_ServicePublic_Name_FR(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger, clas, select, osmTags, defaultTag):
        defaultTagMapping = {
            "name": "nom",
        }
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, clas, select, osmTags, defaultTag, defaultTagMapping)

class Analyser_Merge_ServicePublic_FR_Mairie(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 1, "mairie", {"amenity": "townhall"}, {"amenity": "townhall"})

class Analyser_Merge_ServicePublic_FR_Gendarmerie(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 2, "gendarmerie", {"amenity": "police"}, {"amenity": "police", "operator": "Gendarmerie nationale"})

class Analyser_Merge_ServicePublic_FR_Police(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 3, "commissariat_police", {"amenity": "police"}, {"amenity": "police", "operator": "Police nationale"})

class Analyser_Merge_ServicePublic_FR_EPIC(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 4, "epic", {"office": "administrative"}, {"office": "administrative"})

class Analyser_Merge_ServicePublic_FR_Pole_Emploi(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 5, "pole_emploi", {"office": "employment_agency"}, {"office": "employment_agency"})

class Analyser_Merge_ServicePublic_FR_Tribunal(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 6, ["ta", "ti", "tribunal_commerce", "tgi", "te", "cour_appel"], {"amenity": "courthouse"}, {"amenity": "courthouse"})

class Analyser_Merge_ServicePublic_FR_Prison(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 7, ["maison_centrale", "maison_arret", "centre_penitentiaire", "centre_detention", "csl"], {"amenity": "prison"}, {"amenity": "prison"})

class Analyser_Merge_ServicePublic_FR_Prefecture(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 8, ["prefecture", "sous_pref"], {"office": "government"}, {"office": "government"})

class Analyser_Merge_ServicePublic_FR_CG_CR(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 9, ["cg", "cr"], {"office": "administrative"}, {"office": "administrative"})
