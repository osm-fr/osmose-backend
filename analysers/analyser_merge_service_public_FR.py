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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class _Analyser_Merge_ServicePublic_FR(Analyser_Merge):

    def __init__(self, config, logger, item, clas, level, select, osmTags, defaultTag, defaultTagMapping = {}):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = item, id = clas, level = level, tags = ['merge'],
            title = T_('Public service not integrated'),
            trap = T_(
'''The location can be quite rough.'''))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/",
            "Service-Public.fr",
            CSV(Source(attribution = u"Service-Public.fr", millesime = "08/2018",
                    file = "service_public_FR.csv.bz2"),
                csv = False, separator = None),
            Load("lon", "lat",
                select = {"pivot": select},
                create = """
                    id VARCHAR(254),
                    pivot VARCHAR(254),
                    adresse VARCHAR(1024),
                    acc VARCHAR(254),
                    nom VARCHAR(254),
                    lat VARCHAR(254),
                    lon VARCHAR(254),
                    precision VARCHAR(254)"""),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = osmTags),
                conflationDistance = 300,
                generate = Generate(
                    static1 = defaultTag,
                    static2 = {"source": self.source},
                    mapping1 = dict({"wheelchair": lambda res: self.accTable[res["acc"]] if res["acc"] else None}, **defaultTagMapping),
                    text = lambda tags, fields: {"en": u"%s, %s (geocoded %s)" % (fields["nom"], fields["adresse"], self.prescitionTableEn[fields["precision"]]), "fr": u"%s, %s (géocodé %s)" % (fields["nom"], fields["adresse"], self.prescitionTableFr[fields["precision"]])} )))

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
            "8": u"à l'address",
            "9": u"au bâtiment",
            "10": "10",
        }

class _Analyser_Merge_ServicePublic_Name_FR(_Analyser_Merge_ServicePublic_FR):
    def __init__(self, config, logger, item, clas, level, select, osmTags, defaultTag):
        defaultTagMapping = {
            "name": "nom",
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
        _Analyser_Merge_ServicePublic_FR.__init__(self, config, logger, 8110, 8, 3, ["prefecture", "sous_pref"], {"office": "government"}, {"office": "government"})

class Analyser_Merge_ServicePublic_FR_CG_CR(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 9, 3, ["cg", "cr"], {"office": "government", "government": "parliament"}, {"office": "government", "government": "parliament"})

class Analyser_Merge_ServicePublic_FR_Tresorerie(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 10, 3, "tresorerie", [{"office": "tax"}, {"office": "government", "government": "tax"}], {"office": "government", "government": "tax"})

class Analyser_Merge_ServicePublic_FR_CAF(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 11, 3, "caf", {"social_facility": "outreach", "network": "Caisse d'Allocations Familiales"}, {"social_facility": "outreach", "network": "Caisse d'Allocations Familiales"})

class Analyser_Merge_ServicePublic_FR_CPAM(_Analyser_Merge_ServicePublic_Name_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_ServicePublic_Name_FR.__init__(self, config, logger, 8110, 12, 3, "cpam", {"social_facility": "outreach", "network": "Caisse Primaire d'Assurance Maladie"}, {"social_facility": "outreach", "network": "Caisse Primaire d'Assurance Maladie"})
