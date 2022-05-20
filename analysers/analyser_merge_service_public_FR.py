#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013-2016                                 ##
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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load_XY, Conflate, Select, Mapping

def transform_phone(phone_number):
    if len(phone_number) > 6 and phone_number.startswith("0"):
        return "+33 " + phone_number[1:]
    else:
        return phone_number

class _Analyser_Merge_ServicePublic_FR(Analyser_Merge):

    def __init__(self, config, logger, item, clas, level, select, osmTags, defaultTag, defaultTagMapping = {}):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = item, id = clas, level = level, tags = ['merge', 'fix:survey', 'fix:picture'],
            title = T_('Public service not integrated'),
            trap = T_(
'''The location can be quite rough.'''))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/",
            "Service-Public.fr",
            CSV(Source(attribution = "Service-Public.fr", millesime = "11/2020",
                    file = "service_public_FR.csv.bz2", bz2 = True)),
            Load_XY("longitude", "latitude",
                select = {"category": select}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = osmTags),
                conflationDistance = 500,
                mapping = Mapping(
                    static1 = defaultTag,
                    static2 = {"source": self.source},
                    mapping1 = dict({"wheelchair": lambda res: self.accTable[res["wheelchair_access"]] if res["wheelchair_access"] else None,
                        "contact:email": lambda res:res["email"] if "@" in res["email"] else None,
                        "contact:phone": lambda res: transform_phone(res["phone"]) if res["phone"] else None},
                        **defaultTagMapping),
                    text = lambda tags, fields: {"en": "{0}, {1} (geocoded {2})".format(fields["name"], fields["address"], self.prescitionTableEn[fields["geoloc_precision"]]), "fr": "{0}, {1} (géocodé {2})".format(fields["name"], fields["address"], self.prescitionTableFr[fields["geoloc_precision"]])} )))

        self.accTable = {
            "ACC": "yes",
            "DEM": "limited",
            "NAC": "no",
        }
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
            "10": "10",
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
            "8": u"à l'adresse",
            "9": u"au bâtiment",
            "10": "10",
        }

class _Analyser_Merge_ServicePublic_Name_FR(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger, item, clas, level, select, osmTags, defaultTag):
        defaultTagMapping = {
            "name": "name",
        }
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, item, clas, level, select, osmTags, defaultTag, defaultTagMapping)

class Analyser_Merge_ServicePublic_FR_Mairie(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 8110, 1, 3, ["mairie", "paris_mairie_arrondissement"], {"amenity": "townhall"}, {"amenity": "townhall"})

#class Analyser_Merge_ServicePublic_FR_Gendarmerie(_Analyser_Merge_ServicePublic_Name_FR):
#    def __init__(self, config, logger = None):
#        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 2, 3, "gendarmerie", {"amenity": "police"}, {"amenity": "police", "operator": "Gendarmerie nationale"})

#class Analyser_Merge_ServicePublic_FR_Police(_Analyser_Merge_ServicePublic_Name_FR):
#    def __init__(self, config, logger = None):
#        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 3, 3, "commissariat_police", {"amenity": "police"}, {"amenity": "police", "operator": "Police nationale"})

#class Analyser_Merge_ServicePublic_FR_EPIC(_Analyser_Merge_ServicePublic_Name_FR):
#    def __init__(self, config, logger = None):
#        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 4, 3, "epic", {"office": None}, {})

class Analyser_Merge_ServicePublic_FR_Pole_Emploi(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 5, 3, "pole_emploi", {"office": "employment_agency"}, {"office": "employment_agency"})

class Analyser_Merge_ServicePublic_FR_Tribunal(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 6, 3, ["ta", "ti", "tribunal_commerce", "tgi", "te", "cour_appel"], {"amenity": "courthouse"}, {"amenity": "courthouse"})

class Analyser_Merge_ServicePublic_FR_Prison(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 7, 3, ["maison_centrale", "maison_arret", "centre_penitentiaire", "centre_detention", "csl", "esm"], {"amenity": "prison"}, {"amenity": "prison"})

class Analyser_Merge_ServicePublic_FR_Prefecture(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 8110, 8, 3, ["prefecture", "sous_pref"],
            {"office": "government", "government": "prefecture"},
            {"office": "government", "government": "prefecture"})

class Analyser_Merge_ServicePublic_FR_CG(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 9, 3, "cg",
            {"office": "government", "government": "parliament"},
            {"office": "government", "government": "parliament", "admin_level": "6"})

class Analyser_Merge_ServicePublic_FR_Tresorerie(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 10, 3, "tresorerie",
            [{"office": "tax"}, {"office": "government", "government": "tax"}],
            {"office": "government", "government": "tax"})

class Analyser_Merge_ServicePublic_FR_CAF(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 11, 3, "caf",
            {"office": "government", "government": "social_welfare", "operator": "Caisse d'Allocations Familiales"},
            {"office": "government", "government": "social_welfare", "operator": "Caisse d'Allocations Familiales", "operator:wikidata":"Q1395254"})

class Analyser_Merge_ServicePublic_FR_CPAM(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 12, 3, "cpam",
            {"office": "government", "government": "social_security", "operator": "Caisse Primaire d'Assurance Maladie"},
            {"office": "government", "government": "social_security", "operator": "Caisse Primaire d'Assurance Maladie", "operator:wikidata":"Q2110238"})

class Analyser_Merge_ServicePublic_FR_URSSAF(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 13, 3, "urssaf",
            [{"office": "tax"}, {"office": "government", "government": "tax"}],
            {"office": "government", "government": "tax", "operator": "URSSAF", "operator:wikidata":"Q3550086"})

class Analyser_Merge_ServicePublic_FR_CCI(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 14, 3, ["chambre_agriculture", "chambre_metier", "cci"],
            {"office": "government", "government": "chamber_of_commerce"},
            {"office": "government", "government": "chamber_of_commerce"})

class Analyser_Merge_ServicePublic_FR_CR(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 15, 3, "cr",
            {"office": "government", "government": "parliament"},
            {"office": "government", "government": "parliament", "admin_level": "4"})
