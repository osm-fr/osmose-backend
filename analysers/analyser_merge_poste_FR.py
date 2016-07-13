#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2015                                 ##
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
from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


# http://wiki.openstreetmap.org/wiki/WikiProject_France/data.gouv.fr/Import_des_points_de_contact_postaux

class Analyser_Merge_Poste_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8020", "class": 1, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post office not integrated") }
        self.missing_osm      = {"item":"7050", "class": 2, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post office without ref:FR:LaPoste") }
        self.possible_merge   = {"item":"8021", "class": 3, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post office, integration suggestion") }

        self.Annexe = re.compile(' A$')
        self.Principal = re.compile(' PAL$')
        self.APBP = re.compile(' (AP|BP)$')

        Analyser_Merge.__init__(self, config, logger,
            "https://www.data.gouv.fr/fr/datasets/liste-des-points-de-contact-du-reseau-postal-francais-et-horaires",
            u"Liste des points de contact du réseau postal français et horaires",
            CSV(Source(file = "poste_FR.csv.bz2", encoding = "ISO-8859-15"),
                separator = ";"),
            Load("Longitude", "Latitude"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "post_office"}),
                osmRef = "ref:FR:LaPoste",
                conflationDistance = 1000,
                generate = Generate(
                    static = {
                        "amenity": "post_office",
                        "operator": "La Poste",
                        "source": "data.gouv.fr:LaPoste - 06/2015"},
                    mapping = {
                        "ref:FR:LaPoste": "#Identifiant",
                        "name": lambda res: re.sub(self.Principal, " Principal", re.sub(self.Annexe, " Annexe", re.sub(self.APBP, "", res["Libellé_du_site"]))),
                        "post_office:type": lambda res: {
                            None: None,
                            u"Bureau de poste": None,
                            u"Agence postale commnunale": "post_annex",
                            u"Relais poste commerçant": "post_partner"
                        }[res["Caractéristique_du_site"]],
                        "addr:postcode": "Code_postal",
                        # localite
                        # pays
                        "phone": "Numéro_de_téléphone",
                        "change_machine": lambda res: self.bool[res["Changeur_de_monnaie"]],
                        "copy_facility": lambda res: self.bool[res["Photocopie"]],
                        "atm": lambda res: self.bool[res["Distributeur_de_billets"]],
                        "stamping_machine": lambda res: self.bool[res["Affranchissement_Libre_Service"]],
                        "wheelchair": lambda res:
                            "yes" if self.bool[res["Accessibilité_Absence_de_ressaut_de_plus_de_2_cm_de_haut"]] and self.bool[res["Accessibilité_Entrée_autonome_en_fauteuil_roulant_possible"]] else
                            "limited" if self.bool[res["Accessibilité_Absence_de_ressaut_de_plus_de_2_cm_de_haut"]] or self.bool[res["Accessibilité_Entrée_autonome_en_fauteuil_roulant_possible"]] else
                            "no"},
                text = lambda tags, fields: {"en": u"Post office %s" % ", ".join(filter(lambda x: x and x!='None', [fields[u"Précision_du_géocodage"].lower(), fields[u"Adresse"], fields[u"Complément_d_adresse"], fields[u"Lieu_dit"], fields["Code postal"], fields[u"Localité"]]))} )))

    bool = {"Non": None, "Oui": "yes"}
