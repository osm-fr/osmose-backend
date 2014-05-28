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

class Analyser_Merge_Poste_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8020", "class": 1, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post office not integrated") }
        self.missing_osm      = {"item":"7050", "class": 2, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post office without ref:FR:LaPoste") }
        self.possible_merge   = {"item":"8021", "class": 3, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post office, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.data.gouv.fr/donnees/view/Liste-des-points-de-contact-du-r%C3%A9seau-postal-fran%C3%A7ais-551640"
        self.officialName = u"points de contact du réseau postal français"
        self.csv_file = "poste_FR.csv.bz2"
        self.csv_separator = ";"
        self.csv_encoding = "ISO-8859-15"
        self.osmTags = {
            "amenity": "post_office",
        }
        self.osmRef = "ref:FR:LaPoste"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "poste_fr"
        self.sourceX = "Longitude"
        self.sourceY = "Latitude"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "amenity": "post_office",
            "operator": "La Poste",
            "source": "data.gouv.fr:LaPoste - 01/2013"
        }
        self.Annexe = re.compile(' A$')
        self.Principal = re.compile(' PAL$')
        self.APBP = re.compile(' (AP|BP)$')
        self.defaultTagMapping = {
            "ref:FR:LaPoste": "Identifiant",
            "name": lambda res: re.sub(self.Principal, " Principal", re.sub(self.Annexe, " Annexe", re.sub(self.APBP, "", res["Libellé du site"]))),
            "post_office:type": lambda res: {
                None: None,
                u"Bureau de poste": None,
                u"Agence postale communale": "post_annex",
                u"Relais poste commercant": "post_partner"
            }[res["Caractéristique du site"]],
            "addr:postcode": "Code postal",
            # localite
            # pays
            "phone": "Numéro de téléphone",
            "change_machine": lambda res: self.bool[res["Changeur de monnaie"]],
            "copy_facility": lambda res: self.bool[res["Photocopie"]],
            "atm": lambda res: self.bool[res["Distributeur de billets"]],
            "stamping_machine": lambda res: self.bool[res["Affranchissement Libre Service"]],
            "moneo:loading": lambda res: self.bool[res["Bornes de rechargement MONEO"]],
            "wheelchair": lambda res:
                "yes" if self.bool[res["Accessibilité - Absence de ressaut de plus de 2 cm de haut"]] and self.bool[res["Accessibilité - Entrée autonome en fauteuil roulant possible"]] else
                "limited" if self.bool[res["Accessibilité - Absence de ressaut de plus de 2 cm de haut"]] or self.bool[res["Accessibilité - Entrée autonome en fauteuil roulant possible"]] else
                "no"
        }
        self.conflationDistance = 1000
        self.text = lambda tags, fields: {"en": u"Post office %s" % ", ".join(filter(lambda x: x and x!='None', [fields[u"Précision du géocodage"].lower(), fields[u"Adresse"], fields[u"Complément adresse"], fields[u"Lieu-dit"], fields["Code postal"], fields[u"Localité"]]))}

    bool = {"Non": None, "Oui": "yes"}
