#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2020, Noémie Lehuby 2025-2026        ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping

class _Generic_Analyser_Merge_School_FR(Analyser_Merge_Point):
    def __init__(self, config, logger, osmose_base_class, title_missing_official, title_missing_osm, title_possible_merge, title_update_official, school_category, osm_select_tags, osm_default_tags):
        Analyser_Merge_Point.__init__(self, config, logger)

        if config.db_schema == 'france_guadeloupe':
            classs = 10
            region_name = "Guadeloupe"
            self.is_in = lambda departement: departement == "Guadeloupe"
        elif config.db_schema == 'france_guyane':
            classs = 20
            region_name = "Guyane"
            self.is_in = lambda departement: departement == "Guyane"
        elif config.db_schema == 'france_reunion':
            classs = 30
            region_name = "Réunion"
            self.is_in = lambda departement: departement == "Réunion"
        elif config.db_schema == 'france_martinique':
            classs = 40
            region_name = "Martinique"
            self.is_in = lambda departement: departement == "Martinique"
        else:
            classs = 0
            region_name = "France hexagonale"
            self.is_in = lambda departement: departement not in ["Guadeloupe", "Guyane", "Martinique", "Réunion", "Mayotte", "St-Pierre-et-Miquelon", "Saint-Martin", "Saint-Barthélemy", "Nouvelle-Calédonie", "Polynésie Française"]

        trap = T_(
'''Check the location. Warning data from the Ministry may have several
administrative schools for a single physical school.''')
        self.def_class_missing_official(item = 8030, id = classs+1+osmose_base_class, level = 3, tags = ['merge', 'fix:survey', 'fix:picture'],
            title = T_(title_missing_official),
            trap = trap)
        if title_missing_osm:
            self.def_class_missing_osm(item = 7070, id = classs+2+osmose_base_class, level = 3, tags = ['merge', 'fix:chair'],
                title = T_(title_missing_osm),
                detail = T_('This element in OSM has a \"ref:UAI\" tag. However, this reference does not appear to exist, or no longer exists, in the dataset of the Ministry. This may be due to a copying error in OSM, a school that no longer exists, or an establishment not recognized by the Osmose analysis (administrative building, etc.). '),
                trap = trap)
        self.def_class_possible_merge(item = 8031, id = classs+3+osmose_base_class, level = 3, tags = ['merge', 'fix:chair'],
            title = T_(title_possible_merge),
            trap = trap)
        self.def_class_update_official(item = 8032, id = classs+4+osmose_base_class, level = 3, tags = ['merge', 'fix:chair'],
            title = T_(title_update_official),
            trap = trap)



        self.init(
            "https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education",
            "Annuaire de l'éducation - " + region_name,
            CSV(SourceOpenDataSoft(
                attribution="Ministère de l'Éducation nationale, de l'Enseignement supérieur et de la Recherche",
                url="https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/")),
            Load_XY("longitude", "latitude",
                select = {"etat": ["OUVERT"], "Type_etablissement": school_category},
                where = lambda res: res["Libelle_departement"] and self.is_in(res["Libelle_departement"])),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = osm_select_tags),
                osmRef = "ref:UAI",
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = osm_default_tags,
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:UAI": "Identifiant_de_l_etablissement",
                        "school:FR": lambda res: self.School_FR(res),
                        "contact:phone": lambda res: self.retreat_phone_number(res["Code_commune"], res["Telephone"]),
                        "contact:website": "Web",
                        "contact:email": "Mail",
                        "ref:FR:SIRET": "SIREN_SIRET",
                        "start_date": lambda res: res["date_ouverture"] if res["date_ouverture"] != "1965-05-01" else None,
                        "operator:type": lambda res: "private" if res["Statut_public_prive"] == "Privé" else "public" if res["Statut_public_prive"] == "Public" else None},
                    mapping2 = dict({
                        "name": lambda res: res["Nom_etablissement"].replace("Ecole", "École").replace("Saint ", "Saint-").replace("Sainte ", "Sainte-").replace("élementaire", "élémentaire").replace("elementaire", "élémentaire").replace("Elémentaire", "Élémentaire").replace("elémentaire", "élémentaire").replace("College", "Collège") if res["Nom_etablissement"] else None,
                    }),
                    text = self.text)))

    def text(self, tags, fields):
        lib = ', '.join(filter(lambda x: x and x != "None", [fields["Nom_etablissement"], fields["Adresse_1"], fields["Adresse_3"], fields["Code_postal"], fields["Adresse : code postal"], fields["Nom_commune"]]))
        return {
            "en": lib + " (positioned: {0})".format(self.School_FR_loc[fields["precision_localisation"]]["en"]),
            "fr": lib + " (position : {0})".format(self.School_FR_loc[fields["precision_localisation"]]["fr"]),
        }

    def School_FR(self, fields):
        if fields["Type_etablissement"] == "Ecole":
            if fields["Ecole_maternelle"] == '1' and fields["Ecole_elementaire"] == '0':
                return "maternelle"
            elif fields["Ecole_maternelle"] == '1' and fields["Ecole_elementaire"] == '1':
                return "primaire"
            elif fields["Ecole_maternelle"] == '0' and fields["Ecole_elementaire"] == '1':
                return "élémentaire"
            else:
                return None
        elif fields["Type_etablissement"] == "Collège":
            return "collège"
        elif fields["Type_etablissement"] == "Lycée":
            return "lycée"
        elif fields["Type_etablissement"] == "EREA":
            return "EREA"
        else:
            return None

    def retreat_phone_number(self, insee, phone_number):
        if not phone_number:
            return
        if len(phone_number) < 9:
            return
        if '(' in phone_number:
            return
        if not phone_number.startswith("0"):
            return
        if insee.startswith("971"):
            return "+590 " + phone_number[1:]
        if insee.startswith("972"):
            return "+596 " + phone_number[1:]
        if insee.startswith("973"):
            return "+594 " + phone_number[1:]
        if insee.startswith("974"):
            return "+262 " + phone_number[1:]
        if insee.startswith("975"):
            return "+508 " + phone_number[1:]
        if insee.startswith("976"):
            return "+262 " + phone_number[1:]
        if insee.startswith("977"):
            return "+590 " + phone_number[1:]
        if insee.startswith("978"):
            return "+590 " + phone_number[1:]
        if insee.startswith("986"):
            return "+681 " + phone_number[1:]
        if insee.startswith("987"):
            return "+689 " + phone_number[1:]
        if insee.startswith("988"):
            return "+687 " + phone_number[1:]
        return "+33 " + phone_number[1:]

    School_FR_loc = {
        "None": {"en": "none", "fr": "aucun"},
        "NE SAIT PAS": {"en": "none", "fr": "aucun"},
        "BATIMENT": {"en": "building", "fr": "bâtiment"},
        "CENTRE_PARCELLE": {"en": "parcel centre", "fr": "centre de la parcelle"},
        "CENTRE_PARCELLE_PROJETE": {"en": "parcel", "fr": "parcelle"},
        "COMMUNE": {"en": "municipality", "fr": "commune"},
        "DEFAUT_DE_NUMERO": {"en": "missing number", "fr": "défaut de numéro"},
        "DEFAUT_DE_TRONCON": {"en": "missing street", "fr": "défaut de troncon"},
        "ENTREE PRINCIPALE": {"en": "main entrance", "fr": "entrée principale"},
        "INTERPOLATION": {"en": "interpolated", "fr": "interpolation"},
        "MANUEL": {"en": "manual", "fr": "manuel"},
        "Lieu-dit": {"en": "locality", "fr": "lieu-dit"},
        "NUMERO (ADRESSE)": {"en": "addresse number", "fr": "numéro d'adresse"},
        "Numéro de rue": {"en": "street number", "fr": "numéro de rue"},
        "PLAQUE_ADRESSE": {"en": "house number", "fr": "plaque adresse"},
        "Rue": {"en": "street", "fr": "rue"},
        "Ville": {"en": "city", "fr": "ville"},
        "ZONE_ADRESSAGE": {"en": "addresse area", "fr": "zone d'adressage"},
        "Correcte": {"en": "good", "fr": "correcte"},
        "Parfaite": {"en": "parfect", "fr": "parfaite"},
        "Mauvaise": {"en": "bad", "fr": "imparfaite"},
        "Moyenne": {"en": "medium", "fr": "moyenne"},
        "CENTROIDE (D'EMPRISE)": {"en": "Centroid", "fr": "centroïde d'emprise"},
    }

class Analyser_Merge_School_FR(_Generic_Analyser_Merge_School_FR):
    def __init__(self, config, logger=None):
        _Generic_Analyser_Merge_School_FR.__init__(
            self,
            config,
            logger,
            0,
            "School not integrated",
            "School without tag \"ref:UAI\" or invalid",
            "School, integration suggestion",
            "School update",
            ["Ecole", "Collège", "Lycée", "EREA", "Autre"],
            {"amenity": "school"},
            {"amenity": "school"}
        )

class Analyser_Merge_School_Guidance_FR(_Generic_Analyser_Merge_School_FR):
    def __init__(self, config, logger=None):
        _Generic_Analyser_Merge_School_FR.__init__(
            self,
            config,
            logger,
            5,
            "Guidance couselling not integrated",
            "Guidance couselling without tag \"ref:UAI\" or invalid",
            "Guidance couselling, integration suggestion",
            "Guidance couselling update",
            ["Information et orientation"],
            {"education": "guidance_counselling"},
            {"education": "guidance_counselling", "office": "educational_institution"}
        )

class Analyser_Merge_School_Medical_FR(_Generic_Analyser_Merge_School_FR):
    def __init__(self, config, logger=None):
        _Generic_Analyser_Merge_School_FR.__init__(
            self,
            config,
            logger,
            10,
            "School with medical facility not integrated",
            None,  # Not all social facilities are educational
            "School with medical facility, integration suggestion",
            "School with medical facility update",
            ["Médico-social"],
            {"amenity": "social_facility"},
            {"amenity": "social_facility", "social_facility": "group_home"}
        )

class Analyser_Merge_School_Administrative_FR(_Generic_Analyser_Merge_School_FR):
    def __init__(self, config, logger=None):
        _Generic_Analyser_Merge_School_FR.__init__(
            self,
            config,
            logger,
            15,
            "Education governement office not integrated",
            "Education governement office without tag \"ref:UAI\" or invalid",
            "Education governement office, integration suggestion",
            "Education governement office facility update",
            ["Service Administratif"],
            {"office": "government", "government": "education"},
            {"office": "government", "government": "education"}
        )
