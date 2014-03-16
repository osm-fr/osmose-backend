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


class Analyser_Merge_Tourism_FR_Gironde_Caravan(Analyser_Merge):

    create_table = """
        nom VARCHAR(254),
        adresse VARCHAR(254),
        adresse_suite VARCHAR(254),
        code_postal VARCHAR(254),
        commune VARCHAR(254),
        mode_de_gestion VARCHAR(254),
        tel__informations VARCHAR(254),
        site_web VARCHAR(254),
        longitude VARCHAR(254),
        latitude VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8140", "class": 1, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde caravan site not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.datalocale.fr/drupal7/file/liste-aire-publique-camping-cdt33-1"
        self.officialName = "Liste des aires publiques pour camping-cars de Gironde"
        self.csv_file = "merge_data/tourism_FR_gironde_caravan.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.osmTags = {
            "tourism": "caravan_site"
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "gironde_caravan"
        self.sourceX = "longitude"
        self.sourceY = "latitude"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Observatoire du comité départemental du Tourisme de la Gironde - 09/2013",
            "tourism": "caravan_site",
        }
        self.defaultTagMapping = {
            "name": "nom",
        }
        self.conflationDistance = 500
        self.text = lambda tags, fields: {"en": u"Caravan site of %s" % fields["nom"], "fr": u"Site camping-cars de %s" % fields["nom"]}


class Analyser_Merge_Tourism_FR_Gironde_Camp(Analyser_Merge):

    create_table = """
        type VARCHAR(254),
        categorie VARCHAR(254),
        raison_sociale VARCHAR(254),
        adresse_1 VARCHAR(254),
        adresse_2 VARCHAR(254),
        code_postal VARCHAR(254),
        commune VARCHAR(254),
        tel__information_reservation VARCHAR(254),
        site_web VARCHAR(254),
        labels_et_marques VARCHAR(254),
        tourisme_et_handicap VARCHAR(254),
        longitude VARCHAR(254),
        latitude VARCHAR(254),
        column13 VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8140", "class": 11, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde camp site not integrated") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.datalocale.fr/drupal7/file/liste-campings-classes-cdt33-1"
        self.officialName = "Liste des campings classes et anciennement classes de Gironde"
        self.csv_file = "merge_data/tourism_FR_gironde_camp.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.osmTags = {
            "tourism": "camp_site"
        }
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "gironde_camp"
        self.sourceX = "longitude"
        self.sourceY = "latitude"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Observatoire du comité départemental du Tourisme de la Gironde - 09/2013",
            "tourism": "camp_site",
        }
        self.defaultTagMapping = {
            "name": "raison_sociale",
            "stars": lambda res: res["categorie"][0] if res["categorie"] != u"Non classé" else None,
            "website": "site_web",
        }
        self.conflationDistance = 300
        self.text = lambda tags, fields: {"en": u"Camp site of %s" % fields["raison_sociale"], "fr": u"Camping de %s" % fields["raison_sociale"]}

