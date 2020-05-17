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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Railway_Level_Crossing_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8060, id = 1, level = 3, tags = ['merge', 'railway'],
            title = T_('Crossing level not integrated'))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/passages-a-niveau-30383135/",
            u"Passages à niveau",
            CSV(Source(attribution = u"data.gouv.fr:RFF", millesime = "01/2014",
                    fileUrl = u"http://static.data.gouv.fr/c5/caae14a4ab1f6530f4c24b3e3c25b4a4f753556a8eda7cbf989501626ff400.csv", encoding = "ISO-8859-15"),
                separator = u";"),
            Load("LONGITUDE (WGS84)", "LATITUDE (WGS84)",
                xFunction = self.float_comma,
                yFunction = self.float_comma,
                where = lambda res: res["TYPE"] != 'PN de classe 00'),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"railway": ["level_crossing", "crossing"]}),
                conflationDistance = 150,
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"railway": lambda res: self.type[res["TYPE"]]} )))

    type = {
        u"PN de classe 00": None,
        u"PN privé isolé pour piétons avec portillons": "crossing",
        u"PN privé isolé pour piétons sans portillons": "crossing",
        u"PN privé pour voitures avec barrières avec passage piétons accolé privé": "level_crossing",
        u"PN privé pour voitures avec barrières avec passage piétons accolé public": "level_crossing",
        u"PN privé pour voitures avec barrières sans passage piétons accolé": "level_crossing",
        u"PN privé pour voitures sans barrières": "level_crossing",
        u"PN public isolé pour piétons avec portillons": "crossing",
        u"PN public isolé pour piétons sans portillons": "crossing",
        u"PN public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à distance": "level_crossing",
        u"PN public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à pied d'oeuvre": "level_crossing",
        u"PN public pour voitures avec barrières gardé sans passage piétons accolé à pied d'oeuvre et distance": "level_crossing",
        u"PN public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à distance": "level_crossing",
        u"PN public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à pied d'oeuvre": "level_crossing",
        u"PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 et SAL 2B": "level_crossing",
        u"PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 + ilôt séparateur": "level_crossing",
        u"PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 4": "level_crossing",
        u"PN public pour voitures sans barrières avec SAL 0": "level_crossing",
        u"PN public pour voitures sans barrières protection assurée par un agent": "level_crossing",
        u"PN public pour voitures sans barrières sans SAL": "level_crossing",
    }
