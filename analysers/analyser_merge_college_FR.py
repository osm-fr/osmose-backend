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

import re
from Analyser_Merge import Analyser_Merge


class Analyser_Merge_College_FR(Analyser_Merge):

    create_table = """
        nom VARCHAR(254),
        sigle VARCHAR(254),
        lat NUMERIC(10,7),
        lon NUMERIC(10,7),
        statut VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8030", "class": 100, "level": 3, "tag": ["merge", "railway"], "desc":{"en":u"College not integrated", "fr":u"Établissements d'enseignement supérieur non intégrée", "es": u"Las instituciones de educación superior no están integradas"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.data.gouv.fr/DataSet/30382046"
        self.officialName = "Etablissements d'enseignement supérieur"
        self.csv_file = "merge_data/Etablissements d'enseignement supérieur.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        decsep = re.compile("([0-9]),([0-9])")
        self.csv_filter = lambda t: decsep.sub("\\1.\\2", t)
        self.osmTags = {
            "amenity": ["college", "university"],
        }
        self.osmTypes = ["nodes", "ways", "relations"]
        self.sourceTable = "college_fr"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "amenity": "college",
            "source": u"data.gouv.fr:Office national d'information sur les enseignements et les professions - 11/2011"
        }
        self.defaultTagMapping = {
            "name": "nom",
            "short_name": "sigle",
            "operator:type": lambda res: "private" if res["statut"] in [u"CFA privé", u"Privé hors contrat", u"Privé reconnu", u"Privé sous contrat"] else None,
        }
        self.conflationDistance = 50
        self.text = lambda tags, fields: {"en": " - ".join(filter(lambda i: i != "None", [fields["sigle"], fields["nom"]]))}
