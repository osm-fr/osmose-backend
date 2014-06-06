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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Railway_Level_Crossing_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8060", "class": 1, "level": 3, "tag": ["merge", "railway"], "desc": T_(u"Crossing level not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.data.gouv.fr/donnees/view/Passages-%C3%A0-niveau-30383135",
                name = u"Passages à niveau",
                file = "railway_level_crossing_FR.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ";")),
            Load("LONGITUDE (WGS84)", "LATITUDE (WGS84)", table = "level_crossing_fr",
                xFunction = self.float_comma,
                yFunction = self.float_comma,
                where = lambda res: res["TYPE"] != 'PN de classe 00'),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"railway": ["level_crossing", "crossing"]}),
                conflationDistance = 150,
                generate = Generate(
                    static = {"source": u"data.gouv.fr:RFF - 11/2011"},
                    mapping = {"railway": lambda res: self.type[res["TYPE"]]} )))

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
