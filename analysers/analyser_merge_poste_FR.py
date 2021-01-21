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
from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping


# http://wiki.openstreetmap.org/wiki/WikiProject_France/data.gouv.fr/Import_des_points_de_contact_postaux

class Analyser_Merge_Poste_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8020, id = 1, level = 3, tags = ['merge', 'post'],
            title = T_('Post office not integrated'))
        self.def_class_missing_osm(item = 7050, id = 2, level = 3, tags = ['merge', 'post'],
            title = T_('Post office without tag "ref:FR:LaPoste" or invalid'))
        self.def_class_possible_merge(item = 8021, id = 3, level = 3, tags = ['merge', 'post'],
            title = T_('Post office, integration suggestion'))
        self.def_class_update_official(item = 8022, id = 4, level = 3, tags = ['merge', 'post'],
            title = T_('Post office update'))

        self.APBP = re.compile(' (AP|BP|RP)$')

        self.init(
            "https://datanova.legroupe.laposte.fr/explore/dataset/laposte_poincont",
            "Liste des services disponibles en bureaux de poste, agences postales et relais poste",
            CSV(
                SourceOpenDataSoft(
                    attribution="LaPoste",
                    base_url="https://datanova.legroupe.laposte.fr",
                    dataset="laposte_poincont")),
            Load("Longitude", "Latitude"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "post_office"}),
                osmRef = "ref:FR:LaPoste",
                conflationDistance = 1000,
                mapping = Mapping(
                    static1 = {"amenity": "post_office"},
                    static2 = {
                        "source": self.source,
                        "brand": "La Poste"},
                    mapping1 = {
                        "ref:FR:LaPoste": "#Identifiant_du_site",
                        "post_office:type": lambda res:
                            "post_annex" if res["Libellé_du_site"].endswith(" AP") else # Bureau de poste annexe
                            "post_partner" if res["Libellé_du_site"].endswith(" RP") else # Relais poste commerçant
                            None, # BP: Bureau de poste; other
                        "addr:postcode": "Code_postal",
                        # localite
                        # pays
                        "atm": lambda res: self.bool[res["Distributeur_de_billets"]],
                        "stamping_machine": lambda res: self.bool[res["Affranchissement_Libre_Service"]],
                        "wheelchair": lambda res:
                            "yes" if self.bool[res["Accessibilité_Absence_de_ressaut_de_plus_de_2_cm_de_haut"]] and self.bool[res["Accessibilité_Entrée_autonome_en_fauteuil_roulant_possible"]] else
                            "limited" if self.bool[res["Accessibilité_Absence_de_ressaut_de_plus_de_2_cm_de_haut"]] or self.bool[res["Accessibilité_Entrée_autonome_en_fauteuil_roulant_possible"]] else
                            "no"},
                    mapping2 = {
                        "operator": lambda res:
                            None if res["Libellé_du_site"].endswith(" AP") else # Bureau de poste annexe
                            None if res["Libellé_du_site"].endswith(" RP") else # Relais poste commerçant
                            "La Poste", # BP: Bureau de poste; other
                        "name": lambda res: re.sub(self.APBP, "", res["Libellé_du_site"]),
                        "change_machine": lambda res: self.bool[res["Changeur_de_monnaie"]],
                        "phone": lambda res: ("+33" + res["Numéro_de_téléphone"][1:]) if res["Numéro_de_téléphone"] != "3631" else None},
                text = lambda tags, fields: {"en": "Post office {0}".format(", ".join(filter(lambda x: x, [fields["Précision_du_géocodage"].lower(), fields["Adresse"], fields["Complément_d_adresse"], fields["Lieu_dit"], fields["Code postal"], fields["Localité"]])))} )))

    bool = {"Non": None, "Oui": "yes"}
