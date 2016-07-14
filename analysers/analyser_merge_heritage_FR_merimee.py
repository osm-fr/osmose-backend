#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2016                                 ##
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


class Analyser_Merge_Heritage_FR_Merimee(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8010", "class": 1, "level": 3, "tag": ["merge", "building"], "desc": T_(u"Historical monument not integrated") }
        self.missing_osm      = {"item":"7080", "class": 2, "level": 3, "tag": ["merge"], "desc": T_(u"Historical monument without ref:mhs or invalid") }
        self.possible_merge   = {"item":"8011", "class": 3, "level": 3, "tag": ["merge"], "desc": T_(u"Historical monument, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            "https://www.data.gouv.fr/fr/datasets/monuments-historiques-liste-des-immeubles-proteges-au-titre-des-monuments-historiques/",
            u"Monuments Historiques : liste des Immeubles protégés au titre des Monuments Historiques",
#            CSV(Source(fileUrl = "http://data.culture.fr/entrepot/MERIMEE/merimee-MH.csv.zip", zip = "merimee-MH-valid.csv.utf"),
#            Original without location, geocoded with http://adresse.data.gouv.fr/csv/
            CSV(Source(file = "heritage_FR_merimee.csv.bz2"),
                separator = '|'),
            Load("longitude", "latitude",
                select = {"DPRO": True}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {
#                        "heritage": ["1", "2", "3"],
                        "heritage:operator": None}),
                osmRef = "ref:mhs",
                conflationDistance = 1000,
                generate = Generate(
                    static1 = {"heritage:operator": "mhs"},
                    static2 = {"source:heritage": u"data.gouv.fr:Ministère de la Culture - 04/2015"},
                    mapping1 = {
                        "ref:mhs": "REF",
                        "mhs:inscription_date": lambda res: u"%s" % res["PPRO"][-4:],
                        "heritage": lambda res: 2 if u"classement par arrêté" in res["PPRO"] else 3 if u"inscription par arrêté" in res["PPRO"] else None},
                    mapping2 = {"name": "TICO"},
                    text = lambda tags, fields: {"en": u"Historical monument: %s (positioned at %s with confidence %s)" % (", ".join(filter(lambda x: x!= None and x != "", [fields["DPRO"], fields["ADRS"], fields["COM"]])), fields["result_type"], fields["result_score"])} )))
