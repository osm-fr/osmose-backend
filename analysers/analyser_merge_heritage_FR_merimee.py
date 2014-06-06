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
from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Heritage_FR_Merimee(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8010", "class": 1, "level": 3, "tag": ["merge", "building"], "desc": T_(u"Historical monument not integrated") }
        self.missing_osm      = {"item":"7080", "class": 2, "level": 3, "tag": ["merge"], "desc": T_(u"Historical monument without ref:mhs or invalid") }
        self.possible_merge   = {"item":"8011", "class": 3, "level": 3, "tag": ["merge"], "desc": T_(u"Historical monument, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.data.gouv.fr/donnees/view/Liste-des-Immeubles-prot%C3%A9g%C3%A9s-au-titre-des-Monuments-Historiques-30382152",
                name = u"Liste des Immeubles protégés au titre des Monuments Historiques",
                file = "heritage_FR_merimee.csv.bz2",
                csv = CSV(separator = None, csv = False)),
            Load("lon", "lat", srid = 4326, table = "merimee",
                create = """
                    ref VARCHAR(254) PRIMARY KEY,
                    etud VARCHAR(254),
                    loca VARCHAR(254),
                    reg VARCHAR(254),
                    dpt VARCHAR(254),
                    com VARCHAR(254),
                    insee VARCHAR(254),
                    tico VARCHAR(4048),
                    adrs VARCHAR(4048),
                    stat VARCHAR(254),
                    affe VARCHAR(254),
                    ppro VARCHAR(8096),
                    autr VARCHAR(4048),
                    scle VARCHAR(254),
                    monument VARCHAR(300),
                    lat VARCHAR(254),
                    lon VARCHAR(254)"""),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {
                        "heritage": ["1", "2", "3"],
                        "heritage:operator": None}),
                osmRef = "ref:mhs",
                conflationDistance = 1000,
                generate = Generate(
                    static = {
                        "heritage:operator": "mhs",
                        "source": u"data.gouv.fr:Ministère de la Culture - 08/2011"},
                    mapping = {
                        "ref:mhs": "ref",
                        "name": "tico",
                        "mhs:inscription_date": lambda res: u"%s" % res["ppro"][-4:],
                        "heritage": lambda res: 2 if u"classement par arrêté" in res["ppro"] else 3 if u"inscription par arrêté" in res["ppro"] else None,
                        "wikipedia": self.wikipedia},
                    text = lambda tags, fields: {"en": u"Historical monument: %s" % ", ".join(filter(lambda x: x!= None and x != "", [fields["ppro"], fields["adrs"], fields["loca"]]))} )))

        self.WikipediaSearch = re.compile("\[\[.*\]\]")
        self.WikipediaSub = re.compile("[^[]*\[\[([^|]*).*\]\][^]]*")

    def wikipedia(self, res):
        name = res["monument"]
        if name and re.search(self.WikipediaSearch, name):
            nameWikipedia = re.sub(self.WikipediaSub, "\\1", name)
            return "fr:%s" % nameWikipedia
