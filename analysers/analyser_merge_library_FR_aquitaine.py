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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Library_FR_aquitaine(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8230", "class": 1, "level": 3, "tag": ["merge", "amenity"], "desc": T_(u"Library not integrated") }
        self.possible_merge   = {"item":"8231", "class": 3, "level": 3, "tag": ["merge", "amenity"], "desc": T_(u"Library, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.sirtaqui-aquitaine.com",
                name = u"Liste des bibliothèques et médiathèques en Aquitaine",
                file = "library_FR_aquitaine.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ";")),
            Load("LONGITUDE", "LATITUDE", table = "library_FR_aquitaine",
                where = lambda row: u"Bibliothèque" in row["NOM_OFFRE"] or u"Médiathèque" in row["NOM_OFFRE"]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "library"}),
                conflationDistance = 200,
                generate = Generate(
                    static = {
                        "source": u"CRT Aquitaine - 12/2014",
                        "amenity": "library"},
                    mapping = {
                        "ref:FR:CRTA": "Id",
                        "website": lambda fields: None if not fields["SITE_WEB"] else fields["SITE_WEB"] if fields["SITE_WEB"].startswith('http') else 'http://' + fields["SITE_WEB"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x != "", [fields["NOM_OFFRE"], fields["PORTE_ESCALIER"], fields["BATIMENT_RESIDENCE"], fields["RUE"], fields["LIEUDIT_BP"], fields["CODE_POSTAL"], fields["COMMUNE"]]))} )))
