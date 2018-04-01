#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Postal_Code_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_osm      = {"item":"7160", "class": 2, "level": 3, "tag": ["merge", "post"], "desc": T_(u"admin_level 8 without addr:postcode") }
        self.possible_merge   = {"item":"8221", "class": 3, "level": 3, "tag": ["merge", "post"], "desc": T_(u"Postal code, integration suggestion") }

        Analyser_Merge.__init__(self, config, logger,
            "https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal",
            u"Base officielle des codes postaux",
            CSV(Source(attribution = u"La Poste", millesime = "12/2014",
                    fileUrl = "https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/download/?format=csv&use_labels_for_header=true"),
                separator = ";"),
            Load(srid = None),
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
                    static2 = {"source:postal_code": self.source},
                    mapping1 = {
                        "ref:INSEE": "Code_commune_INSEE",
                        "addr:postcode": "Code_postal"},
                text = lambda tags, fields: {"en": u"Postal code %s for %s (INSEE:%s)" % (fields["Code_postal"], (fields["Nom_commune"] or "").strip(), fields["Code_commune_INSEE"])} )))
