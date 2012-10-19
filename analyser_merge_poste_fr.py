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

import re
from Analyser_Merge import Analyser_Merge


# http://wiki.openstreetmap.org/wiki/WikiProject_France/data.gouv.fr/Import_des_points_de_contact_postaux

class Analyser_Merge_Poste_Fr(Analyser_Merge):

    create_table = """
        identifiant VARCHAR(254) PRIMARY KEY,
        libelle_site VARCHAR(254),
        caracteristique_site VARCHAR(254),
        complement_adresse VARCHAR(254),
        adresse VARCHAR(254),
        lieu_dit VARCHAR(254),
        code_postal VARCHAR(254),
        localite VARCHAR(254),
        pays VARCHAR(254),
        latitude NUMERIC(10,7),
        longitude NUMERIC(10,7),
        telephone VARCHAR(254),
        changeur_monnaie VARCHAR(254),
        photocopieur VARCHAR(254),
        dab VARCHAR(254),
        affranchissement_libre_service VARCHAR(254),
        recharge_moneo VARCHAR(254),
        monnaie_paris VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8020", "class": 1, "level": 3, "tag": ["merge", "post"], "desc":{"fr":u"Poste non intégrée"} }
        self.missing_osm      = {"item":"7050", "class": 2, "level": 3, "tag": ["merge", "post"], "desc":{"fr":u"Poste sans ref:FR:LaPoste ou invalide"} }
        self.possible_merge   = {"item":"8021", "class": 3, "level": 3, "tag": ["merge", "post"], "desc":{"fr":u"Poste, proposition d'intégration"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.data.gouv.fr/donnees/view/Liste-des-points-de-contact-du-r%C3%A9seau-postal-fran%C3%A7ais-551640"
        self.officialName = "points de contact du réseau postal français"
        self.csv_file = "merge_data/270949f7a9ff7dce81b45d8150279259.csv"
        self.csv_format = "WITH DELIMITER AS ';' NULL AS 'null' CSV"
        self.csv_encoding = "ISO-8859-15"
        self.osmTags = {
            "amenity": "post_office",
        }
        self.osmRef = "ref:FR:LaPoste"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "poste_fr"
        self.sourceRef = "identifiant"
        self.sourceX = "longitude"
        self.sourceY = "latitude"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "amenity": "post_office",
            "operator": "La Poste",
            "source": "data.gouv.fr:LaPoste - 04/2012"
        }
        self.Annexe = re.compile(' A$')
        self.Principal = re.compile(' PAL$')
        self.defaultTagMapping = {
            "ref:FR:LaPoste": "identifiant",
            "name": lambda res: re.sub(self.Principal, " Principal", re.sub(self.Annexe, " Annexe", res["libelle_site"])),
            "post_office:type": lambda res: {
                None: None,
                "AGENCE POSTALE COMMUNALE": "post_annex",
                "RELAIS POSTE COMMERCANT": "post_partner"
            }[res["caracteristique_site"]],
            "addr:postcode": "code_postal",
            # localite
            # pays
            "phone": "telephone",
            "change_machine": lambda res: self.bool[res["changeur_monnaie"]],
            "copy_facility": lambda res: self.bool[res["photocopieur"]],
            "atm": lambda res: self.bool[res["dab"]],
            "stamping_machine": lambda res: self.bool[res["affranchissement_libre_service"]],
            "moneo:loading": lambda res: self.bool[res["recharge_moneo"]],
            # monnaie_paris
        }
        self.conflationDistance = 1000
        self.text = lambda tags, fields: {"fr":"Bureau de poste de %s" % ", ".join(filter(lambda x: x!=None, [fields["adresse"], fields["complement_adresse"], fields["lieu_dit"], fields["localite"]]))}

    bool = {"N": None, "O": "yes"}
