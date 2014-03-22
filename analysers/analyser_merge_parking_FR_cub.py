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

from Analyser_Merge import Analyser_Merge


class Analyser_Merge_Parking_FR_cub(Analyser_Merge):

    create_table = """
        x VARCHAR(254),
        y VARCHAR(254),
        gid VARCHAR(254),
        ident VARCHAR(254),
        nom VARCHAR(254),
        theme VARCHAR(254),
        sstheme VARCHAR(254),
        codec VARCHAR(254),
        commune VARCHAR(254),
        toponyme VARCHAR(254),
        toponyme_x VARCHAR(254),
        toponyme_y VARCHAR(254),
        toponyme_o VARCHAR(254),
        geom_o VARCHAR(254),
        cdate VARCHAR(254),
        mdate VARCHAR(254),
        "parkings_donnees_date mise à jour des données" VARCHAR(254),
        "parkings_donnees_identification cub du parking" VARCHAR(254),
        "parkings_donnees_nom du parking" VARCHAR(254),
        "parkings_donnees_propriétaire" VARCHAR(254),
        "parkings_donnees_titulaire du contrat" VARCHAR(254),
        "parkings_donnees_exploitant" VARCHAR(254),
        "parkings_donnees_type de gestion" VARCHAR(254),
        "parkings_donnees_secteur" VARCHAR(254),
        "parkings_donnees_insee commune" VARCHAR(254),
        "parkings_donnees_commune" VARCHAR(254),
        "parkings_donnees_année de mise en service" VARCHAR(254),
        "parkings_donnees_type de construction" VARCHAR(254),
        "parkings_donnees_nombre de niveaux" VARCHAR(254),
        "parkings_donnees_places hors gabarit < 3,5t" VARCHAR(254),
        "parkings_donnees_places hors gabarit > 3,5t" VARCHAR(254),
        "parkings_donnees_nombre de places utilisées en fourrière" VARCHAR(254),
        "parkings_donnees_nombre de places utilisées en parc-relais (p+r)" VARCHAR(254),
        "parkings_donnees_nombre de places  en parking simple tous usagers" VARCHAR(254),
        "parkings_donnees_total places vl" VARCHAR(254),
        "parkings_donnees_dont places pmr" VARCHAR(254),
        "parkings_donnees_dont places vl électrique" VARCHAR(254),
        "parkings_donnees_dont places autopartage ou autocool ou citiz" VARCHAR(254),
        "parkings_donnees_dont covoiturage" VARCHAR(254),
        "parkings_donnees_et dont places pour station de lavage" VARCHAR(254),
        "parkings_donnees_places 2 roues à moteur" VARCHAR(254),
        "parkings_donnees_dont 2 roues à moteur électrique" VARCHAR(254),
        "parkings_donnees_total places vélo" VARCHAR(254),
        "parkings_donnees_dont places vélo électrique" VARCHAR(254),
        "parkings_donnees_remarques" VARCHAR(254),
        "parkings_donnees_lien vers site" VARCHAR(254),
        "parkings_donnees_coordonnées gps" VARCHAR(254),
        "parkings_donnees_adresse du parking" VARCHAR(254),
        "parkings_donnees_horaires d'ouverture" VARCHAR(254),
        "parkings_donnees_horaires de présence personnel" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_gid" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_nom" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_theme" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_sstheme" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_codec" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_commune" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_toponyme" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_toponyme_x" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_toponyme_y" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_toponyme_o" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_geom_o" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_cdate" VARCHAR(254),
        "parkings_donnees_to_eqpub_p_mdate" VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 31, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking not integrated") }
        self.possible_merge   = {"item":"8131", "class": 33, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=10" # joins on http://data.lacub.fr/data.php?themes=1
        self.officialName = "Parking public données techniques" # joins on "Équipement public"
        self.csv_file = "merge_data/parking_FR_cub.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_select = {
            "parkings_donnees_propriétaire": ["CUB", "CHU"]
        }
        self.osmTags = {
            "amenity": "parking",
        }
        self.osmRef = "ref:FR:CUB"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "cub_parking"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": "Communauté Urbaine de Bordeaux - 03/2014",
            "amenity": "parking",
        }
        self.defaultTagMapping = {
            "ref:FR:CUB": "ident",
            "start_date": "parkings_donnees_année de mise en service",
            "parking": lambda res: "surface" if "surface" in res["parkings_donnees_type de construction"].lower() else "underground" if "enterré" in res["parkings_donnees_type de construction"].lower() else None,
            "levels": "parkings_donnees_nombre de niveaux",
            "capacity": "parkings_donnees_total places vl",
            "capacity:disabled": "parkings_donnees_dont places pmr",
            "name": "parkings_donnees_nom du parking",
            "operator": "parkings_donnees_exploitant",
        }
        self.conflationDistance = 300
        self.text = lambda tags, fields: {"en": u"Parking %s" % fields["parkings_donnees_nom du parking"]}


class Analyser_Merge_Parking_FR_cub_disabled(Analyser_Merge):

    create_table = """
        x VARCHAR(254),
        y VARCHAR(254),
        gid VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8130", "class": 21, "level": 3, "tag": ["merge", "parking"], "desc": T_(u"CUB parking disabled not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://data.lacub.fr/data.php?themes=8"
        self.officialName = "Place de stationnement PMR"
        self.csv_file = "merge_data/parking_FR_cub_disabled.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        self.osmTags = {
            "amenity": "parking",
            "capacity:disabled": None,
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "cub_parking_disabled"
        self.sourceX = "x"
        self.sourceY = "y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "source": "Communauté Urbaine de Bordeaux - 03/2014",
            "amenity": "parking",
            "capacity:disabled": "yes",
        }
        self.conflationDistance = 100
