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

import re
from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Postal_Code_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_osm      = {"item":"7160", "class": 2, "level": 3, "tag": ["merge", "post"], "desc": T_(u"admin_level 8 without addr:postcode") }
        self.possible_merge   = {"item":"8221", "class": 3, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Postal code, integration suggestion") }

        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "https://www.data.gouv.fr/fr/datasets/base-officielle-des-codes-postaux/",
                name = u"Base officielle des codes postaux",
                file = "postal_code_FR.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ";")),
            Load(srid= None, table = "postal_code_fr"),
            Mapping(
                select = Select(
                    types = ["relations"],
                    tags = {
                        "type": "boundary",
                        "admin_level": "8",
                        "ref:INSEE": None}),
                osmRef = "addr:postcode",
                extraJoin = "ref:INSEE",
                generate = Generate(
                    static = {
                        "source:postal_code": "La Poste - 11/2014"},
                    mapping = {
                        "ref:INSEE": "code commune INSEE",
                        "addr:postcode": "code postal"},
                text = lambda tags, fields: {"en": u"Postal code %s for %s (INSEE:%s)" % (fields["code postal"], (fields["nom de la commune"] or "").strip(), fields["code commune INSEE"])} )))
