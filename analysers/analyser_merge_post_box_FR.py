#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015                                      ##
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


class Analyser_Merge_Post_box_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8022", "class": 1, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post box not integrated") }
        self.missing_osm      = {"item":"7051", "class": 2, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post box without ref:FR:LaPoste") }
        self.possible_merge   = {"item":"8023", "class": 3, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Post box, integration suggestion") }

        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "https://www.data.gouv.fr/fr/datasets/liste-des-boites-aux-lettres-de-rue-france-metropolitaine-et-dom-1/",
                name = u"Liste des boîtes aux lettres de rue France métropolitaine et DOM",
                file = "post_box_FR.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ";")),
            Load("Longitude", "Latitude", table = "post_box_fr"),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "post_box"}),
                osmRef = "ref:FR:LaPoste",
                conflationDistance = 150,
                generate = Generate(
                    static = {
                        "amenity": "post_box",
                        "operator": "La Poste",
                        "source": "data.gouv.fr:LaPoste - 06/2015"},
                    mapping = {
                        "ref:FR:LaPoste": "CO_MUP",
                        "addr:postcode": "CO_POSTAL"},
                text = lambda tags, fields: {"en": ", ".join(filter(lambda x: x and x != 'None' and x != '', [fields[u"VA_NO_VOIE"], fields[u"LB_EXTENSION"].strip(), fields[u"LB_VOIE_EXT"], fields["CO_POSTAL"], fields[u"LB_COM"]]))} )))
