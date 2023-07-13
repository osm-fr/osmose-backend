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
from modules import downloader
from .Analyser_Merge import Analyser_Merge_Point, Source, CSV, Load_XY, Conflate, Select, Mapping
from io import BytesIO
import json
import csv
import datetime
import tarfile

class _Generic_Analyser_Merge_Public_Services_FR_(Analyser_Merge_Point):
    def __init__(self, config, logger, osmose_class, public_service_category, osm_select_tags, osm_default_tags):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8110, id = osmose_class, level = 3, tags = ['merge', 'fix:imagery', 'fix:survey', 'fix:picture'],
            title = T_('Public service not integrated'))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/",
            "Service-Public.fr",
            CSV(Public_Services_Source(Source(attribution = "Service-Public.fr",
                    fileUrl="https://www.data.gouv.fr/fr/datasets/r/73302880-e4df-4d4c-8676-1a61bb997f3d"))),
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

class Public_Services_Source(Source):
    def __init__(self, source):
        self.source = source

    def __getattr__(self, name):
        return getattr(self.source, name)

    def open(self):
        return open(downloader.update_cache('join://' + self.source.fileUrl, 15, fetch=self.fetch))

    def fetch(self, url, tmp_file, date_string=None):
        dataset_dl = downloader.request_get(self.source.fileUrl)
        with tarfile.open(fileobj=BytesIO(dataset_dl.raw.read())) as archive:
            for content in archive.getmembers():
                if content.name.endswith("data.gouv_local.json"):
                    date_and_blabla = content.name.split("/")[1]
                    millesime = datetime.datetime.strptime(date_and_blabla[0:10], '%Y-%m-%d').strftime('%m/%Y')
                    json_file = archive.extractfile(content.name)
                    data = json.load(json_file)

        export = []

        wheelchair_mapping = {
            "ACC": "yes",
            "DEM": "limited",
            "NAC": "no",
            "": None
        }

        for feature in data["service"]:
            elem = {}
            if not feature.get("pivot"):
                continue
            elem["categorie"] = feature["pivot"][0]["type_service_local"]
            elem["official_name"] = feature["nom"]
            elem['branch'] = None
            if elem["categorie"] in ["mairie", "mairie_com"]:
                elem["name"] = retreat_townhall_name(feature["nom"])
            elif elem["categorie"] in ["esm"]:
                elem["name"] = retreat_prison_name(feature["nom"])
            elif elem["categorie"] in ["sous_pref"]:
                elem["name"] = retreat_sous_prefecture_name(feature["nom"])
            elif elem["categorie"] in ["cpam"]:
                elem["name"] = retreat_CPAM_name(feature["nom"])
            elif elem["categorie"] in ["caf"]:
                elem["name"] = retreat_Caf_name(feature["nom"])
            elif elem["categorie"] in ["cio"]:
                elem["name"] = retreat_CIO_name(feature["nom"])
            elif elem["categorie"] in ["pmi"]:
                elem["name"] = retreat_PMI_name(feature["nom"])
            elif elem["categorie"] in ["mission_locale"]:
                elem["name"] = retreat_Mission_Locale_name(feature["nom"])
            elif elem["categorie"] in ["pole_emploi"]:
                elem["name"], elem["branch"] = retreat_Pole_Emploi_name(feature["nom"])
            elif elem["categorie"] in ["msap"]:
                elem["name"], elem["branch"] = retreat_France_Services_name(feature["nom"])
            elif elem["categorie"] in ["ti", "tribunal_commerce", "tgi",
                                    "te", "cour_appel", "maison_centrale", "maison_arret",
                                    "centre_penitentiaire", "centre_detention", "csl"]:
                elem["name"] = feature["nom"]
            elif elem["categorie"] in ["urssaf"]:
                elem["name"] = retreat_Urssaf_name(feature["nom"])
            else:
                elem["name"] = None
            elem["contact:phone"] = None
            if feature.get("telephone"):
                phone_number = feature["telephone"][0]["valeur"]
                if len(phone_number) > 9 and phone_number.startswith("0") and '(' not in phone_number:
                    elem["contact:phone"] = "+33 " + phone_number[1:]
            elem["contact:website"] = None
            if feature.get("site_internet"):
                elem["contact:website"] = feature.get("site_internet")[0]["valeur"]
            elem["contact:email"] = None
            if feature.get("adresse_courriel"):
                elem["contact:email"] = feature.get("adresse_courriel")[0]
            elem["ref:FR:SIRET"] = feature["siret"]

            if not feature.get("adresse"):
                continue
            feature_address = feature["adresse"][0]
            elem["longitude"] = feature_address["longitude"]
            elem["latitude"] = feature_address["latitude"]
            elem["address_txt"] = "{} {} {} {} {}".format(
                feature_address["complement1"],
                feature_address["complement2"],
                feature_address["numero_voie"],
                feature_address["code_postal"],
                feature_address["nom_commune"],
            )
            elem["wheelchair"] = wheelchair_mapping[feature_address["accessibilite"]]
            elem["wheelchair:description"] = feature_address["note_accessibilite"]

            elem["opening_hours"] = parse_opening_hours(feature["plage_ouverture"])

            elem["millesime"] = millesime

            export.append(elem)

        with open(tmp_file, 'w') as out_file:
            csv_writer = csv.DictWriter(out_file, delimiter=',', fieldnames=export[0].keys())
            csv_writer.writeheader()
            for row in export:
                csv_writer.writerow(row)

        return out_file

def parse_opening_hours(txt):
    if txt is None:
        return None
    osm_days = {"Lundi": "Mo", "Mardi": "Tu", "Mercredi":"We", "Jeudi": "Th", "Vendredi":"Fr", "Samedi":"Sa", "Dimanche":"Su", "jours_feries": "PH"}

    opening_hours = ""
    for plage in txt:
        opening_hours += osm_days[plage["nom_jour_debut"]]
        if plage["nom_jour_debut"] != plage["nom_jour_fin"]:
            opening_hours += "-{}".format(osm_days[plage["nom_jour_fin"]])
        opening_hours += " "

        opening_hours += "{}-{}".format(plage['valeur_heure_debut_1'][0:5], plage['valeur_heure_fin_1'][0:5])
        if plage['valeur_heure_debut_2']:
            opening_hours += ",{}-{}".format(plage['valeur_heure_debut_2'][0:5], plage['valeur_heure_fin_2'][0:5])
        opening_hours += "; "
    return opening_hours[:-2]

def _retreat_name(official_name):
    zz = official_name.split(" - ")
    if len(zz) == 1:
        return
    city_name = zz[1]

    if city_name.startswith("A"):
        return
    if city_name.startswith("E"):
        return
    if city_name.startswith("I"):
        return
    if city_name.startswith("O"):
        return
    if city_name.startswith("U"):
        return
    if city_name.startswith("É"):
        return
    if city_name.startswith("È"):
        return
    if city_name.startswith("Ê"):
        return
    if city_name.startswith("Î"):
        return
    if city_name.startswith("Le "):
        return
    if city_name.startswith("Les "):
        return
    return official_name.replace(" - ", " de ")

def retreat_sous_prefecture_name(official_name):
    name = _retreat_name(official_name)
    if name:
        return name.replace("préfecture","Préfecture")
    return

def retreat_townhall_name(official_name):
    return _retreat_name(official_name)

def retreat_prison_name(official_name):
    if not official_name.startswith("Etablissement"):
        return
    return "É" + official_name[1:]

def retreat_CPAM_name(official_name):
    return official_name.replace("Caisse primaire d'assurance maladie (CPAM)", "CPAM").split(" - ")[0]

def retreat_Caf_name(official_name):
    return official_name.replace("Caisse d'allocations familiales (Caf)", "Caf").split(" - ")[0]

def retreat_PMI_name(official_name):
    return official_name.replace("Centre de protection maternelle et infantile (PMI)", "PMI").split(" - ")[0]

def retreat_CIO_name(official_name):
    return official_name.replace("Centre d’information et d’orientation (CIO)", "CIO").replace("Centre d'information et d'orientation (CIO)","CIO").split(" - ")[0]

def retreat_Mission_Locale_name(official_name):
    return official_name.replace("Mission locale pour l'insertion professionnelle et sociale des jeunes (16-25 ans)", "Mission locale").split(" - ")[0]

def retreat_Pole_Emploi_name(official_name):
    return "Pôle Emploi", official_name.replace("Pôle emploi - ", "")

def retreat_France_Services_name(official_name):
    return "France Services", official_name.replace("France Services - ", "")

def retreat_Urssaf_name(official_name):
    if not official_name.startswith("Urssaf"):
        return
    return official_name.split(" - ")[0]
