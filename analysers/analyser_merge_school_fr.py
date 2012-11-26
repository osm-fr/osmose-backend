#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

# https://gitorious.org/osm-hacks/osm-hacks/trees/master/etablissements-scolaires

class Analyser_Merge_School_Fr(Analyser_Merge):

    create_table = """
        numero_uai VARCHAR(254) PRIMARY KEY,
        appellation_officielle_uai VARCHAR(254),
        denomination_principale_uai VARCHAR(254),
        patronyme_uai VARCHAR(254),
        X NUMERIC(7),
        Y NUMERIC(7),
        etat_etablissement VARCHAR(254),
        nature_uai VARCHAR(254),
        lib_nature VARCHAR(254),
        sous_fic VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8030", "class": 1, "level": 3, "tag": ["merge"], "desc":{"fr":"École non intégrée"} }
        self.missing_osm      = {"item":"7070", "class": 2, "level": 3, "tag": ["merge"], "desc":{"fr":"École sans ref:UAI ou invalide"} }
        self.possible_merge   = {"item":"8031", "class": 3, "level": 3, "tag": ["merge"], "desc":{"fr":"École, proposition d'intégration"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.data.gouv.fr/donnees/view/G%C3%A9olocalisation-des-%C3%A9tablissements-d%27enseignement-du-premier-degr%C3%A9-et-du-second-degr%C3%A9-du-minist%C3%A8re-d-30378093"
        self.officialName = "établissements d'enseignement du premier degré et du second degré"
        self.csv_file = "merge_data/MENJVA_etab_geoloc.csv"
        self.csv_format = "WITH DELIMITER AS ';' NULL AS 'null' CSV HEADER"
        self.csv_encoding = "ISO-8859-15"
        self.csv_filter = lambda t: t.replace("; ", ";null").replace(";.", ";null").replace("Ecole", u"École").replace("Saint ", "Saint-").replace("Sainte ", "Sainte-").replace(u"élementaire", u"élémentaire")
        self.osmTags = {
            "amenity": ["school", "kindergarten"],
        }
        self.osmRef = "ref:UAI"
        self.osmTypes = ["nodes", "ways", "relations"]
        self.sourceTable = "school_fr"
        self.sourceRef = "numero_uai"
        self.sourceX = "X"
        self.sourceY = "Y"
        self.sourceSRID = "2154"
        self.defaultTag = {
            "amenity": "school",
            "source": "data.gouv.fr:Ministère de l'Éducation nationale, de la Jeunesse et de la Vie associative - 05/2012"
        }
        self.defaultTagMapping = {
            "ref:UAI": "numero_uai",
            "school:FR": self.school_FR,
            "name": "appellation_officielle_uai",
            "operator:type": lambda res: "private" if "PRIVE" in res["denomination_principale_uai"] else None,
        }
        self.conflationDistance = 50
        self.text = lambda tags, fields: {"fr":fields["appellation_officielle_uai"] if fields["appellation_officielle_uai"] else ""}

    School_FR_token = {
        "ECOLE ELEMENTAIRE": "élémentaire",
        "ECOLE DE NIVEAU ELEMENTAIRE": "élémentaire",
        "ECOLE MATERNELLE": "maternelle",
        "ECOLE PRIMAIRE": "primaire",
        "COLLEGE": "collège",
        "LYCEE": "lycée",
        "LP": "lycée",
        "LYC": "lycée",
        "ECOLE SECONDAIRE": "secondaire",
    }

    def school_FR(self, res):
        for k, v in self.School_FR_token.items():
            if res["lib_nature"].startswith(k):
                return v
        return res["lib_nature"]
