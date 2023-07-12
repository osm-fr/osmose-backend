#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2023                                         ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, CSV, Load_XY, Conflate, Select, Mapping

class _Generic_Analyser_Merge_Public_Services_FR_(Analyser_Merge_Point):
    def __init__(self, config, logger, osmose_class, public_service_category, osm_select_tags, osm_default_tags):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8110, id = osmose_class, level = 3, tags = ['merge', 'fix:imagery', 'fix:survey', 'fix:picture'],
            title = T_('Public service not integrated'))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/",
            "Service-Public.fr",
            CSV(Source(attribution = "Service-Public.fr",
                    fileUrl="https://raw.githubusercontent.com/nlehuby/sepuqu/gh-pages/services_publics.csv")),
            Load_XY("longitude", "latitude",
                select = {"categorie": public_service_category}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = osm_select_tags),
                conflationDistance = 500,
                mapping = Mapping(
                    static1 = osm_default_tags,
                    mapping1 = dict({
                        "name": "name",
                        "wheelchair": "wheelchair",
                        "wheelchair:description": lambda feature: feature["wheelchair:description"] if feature["wheelchair"] == "limited" else None,
                        "contact:email": "contact:email",
                        "contact:website": "contact:website",
                        "ref:FR:SIRET": "ref:FR:SIRET",
                        "branch": "branch",
                        "opening_hours": "opening_hours",
                        "contact:phone":  "contact:phone"
                    }),
                    mapping2 = dict({
                        "source": lambda feature: "Service-Public.fr - " + feature["millesime"]
                    }),
                    text = lambda tags, fields: {"en": "{0}, {1}".format(fields["official_name"], fields["address_txt"])} )))

class Analyser_Merge_Public_Services_Mairie(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger=None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 1, ["mairie", "mairie_com"], {"amenity": "townhall"}, {"amenity": "townhall"})

class Analyser_Merge_ServicePublic_FR_EPCI(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 2, "epci",
            {"office": "government", "government": "local_authority"},
            {"office": "government", "government": "local_authority"})

class Analyser_Merge_ServicePublic_FR_PMI(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 3, "pmi",
            {"amenity": "social_facility", "social_facility:for": "child"},
            {"amenity": "social_facility", "social_facility:for": "child", "social_facility": "ambulatory_care", "short_name": "PMI"})

class Analyser_Merge_ServicePublic_FR_CIJ(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 4, ["cij", "cio", "mission_locale"],
            {"amenity": "social_facility", "social_facility:for": "juvenile"},
            {"amenity": "social_facility", "social_facility:for": "juvenile", "social_facility": "outreach"})

class Analyser_Merge_ServicePublic_FR_Pole_Emploi(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 5, "pole_emploi",
            {"office": "employment_agency"},
            {"office": "employment_agency", "brand": "Pôle Emploi", "brand:wikidata": "Q8901192"})

class Analyser_Merge_ServicePublic_FR_Tribunal(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 6, ["ta", "ti", "tribunal_commerce", "tgi", "te", "cour_appel"], {"amenity": "courthouse"}, {"amenity": "courthouse"})

class Analyser_Merge_ServicePublic_FR_Prison(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 7, ["maison_centrale", "maison_arret", "centre_penitentiaire", "centre_detention", "csl", "esm"], {"amenity": "prison"}, {"amenity": "prison"})

class Analyser_Merge_ServicePublic_FR_Prefecture(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 8, ["prefecture", "sous_pref"],
            {"office": "government", "government": "prefecture"},
            {"office": "government", "government": "prefecture"})

class Analyser_Merge_ServicePublic_FR_CG(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 9, "cg",
            {"office": "government", "government": "parliament"},
            {"office": "government", "government": "parliament", "admin_level": "6"})

class Analyser_Merge_ServicePublic_FR_Impots(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 10, "sip",
            [{"office": "tax"}, {"office": "government", "government": "tax"}],
            {"office": "government", "government": "tax"})

class Analyser_Merge_ServicePublic_FR_CAF(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 11, "caf",
            {"office": "government", "government": "social_welfare", "operator": "Caisse d'Allocations Familiales"},
            {"office": "government", "government": "social_welfare", "operator": "Caisse d'Allocations Familiales", "operator:wikidata":"Q1395254"})

class Analyser_Merge_ServicePublic_FR_CPAM(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 12, "cpam",
            {"office": "government", "government": "social_security", "operator": "Caisse Primaire d'Assurance Maladie"},
            {"office": "government", "government": "social_security", "operator": "Caisse Primaire d'Assurance Maladie", "operator:wikidata":"Q2110238"})

class Analyser_Merge_ServicePublic_FR_URSSAF(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 13, "urssaf",
            [{"office": "tax"}, {"office": "government", "government": "tax"}],
            {"office": "government", "government": "tax", "operator": "URSSAF", "operator:wikidata":"Q3550086"})

class Analyser_Merge_ServicePublic_FR_CCI(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 14, ["chambre_agriculture", "chambre_metier", "cci"],
            {"office": "government", "government": "chamber_of_commerce"},
            {"office": "government", "government": "chamber_of_commerce"})

class Analyser_Merge_ServicePublic_FR_CR(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 15, "cr",
            {"office": "government", "government": "parliament"},
            {"office": "government", "government": "parliament", "admin_level": "4"})

class Analyser_Merge_ServicePublic_FR_MSAP(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 16, "msap",
            {"office": "government", "government": "public_service", "operator": "France Services"},
            {"office": "government", "government": "public_service", "operator": "France Services", "operator:wikidata":"Q24931343"})

class Analyser_Merge_ServicePublic_FR_CLIC(_Generic_Analyser_Merge_Public_Services_FR_):
    def __init__(self, config, logger = None):
        _Generic_Analyser_Merge_Public_Services_FR_.__init__(self, config, logger, 16, "clic",
            {"amenity": "social_facility", "social_facility:for": "senior"},
            {"amenity": "social_facility", "social_facility:for": "senior", "social_facility": "outreach"})
