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
        self.missing_official = {"item":"8140", "class": 41, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde caravan site not integrated") }
        self.possible_merge   = {"item":"8141", "class": 43, "level": 3, "tag": ["merge", "tourism"], "desc": T_(u"Gironde caravan site, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.datalocale.fr/drupal7/file/liste-aire-publique-camping-cdt33-1"
        self.officialName = "liste-aire-publique-camping-cdt33"
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
