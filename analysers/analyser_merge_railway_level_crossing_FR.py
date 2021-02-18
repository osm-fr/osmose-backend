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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceDataGouv, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Railway_Level_Crossing_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8060, id = 1, level = 3, tags = ['merge', 'railway', 'fix:survey', 'fix:imagery'],
            title = T_('Crossing level not integrated'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/passages-a-niveau-30383135/",
            "Passages à niveau",
            CSV(
                SourceDataGouv(
                    attribution="data.gouv.fr:RFF",
                    dataset="53699bd5a3a729239d205825",
                    resource="77cd3505-76ef-41ba-aace-82b4df3a376c",
                    encoding="ISO-8859-15"),
                separator = ";"),
            Load("LONGITUDE (WGS84)", "LATITUDE (WGS84)",
                xFunction = Load.float_comma,
                yFunction = Load.float_comma,
                where = lambda res: res["TYPE"] != 'PN de classe 00'),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"railway": ["level_crossing", "crossing"]}),
                conflationDistance = 150,
                mapping = Mapping(
                    static2 = {"source": self.source},
                    mapping1 = {"railway": lambda res: self.type[res["TYPE"]]} )))

    type = {
        "PN de classe 00": None,
        "PN privé isolé pour piétons avec portillons": "crossing",
        "PN privé isolé pour piétons sans portillons": "crossing",
        "PN privé pour voitures avec barrières avec passage piétons accolé privé": "level_crossing",
        "PN privé pour voitures avec barrières avec passage piétons accolé public": "level_crossing",
        "PN privé pour voitures avec barrières sans passage piétons accolé": "level_crossing",
        "PN privé pour voitures sans barrières": "level_crossing",
        "PN public isolé pour piétons avec portillons": "crossing",
        "PN public isolé pour piétons sans portillons": "crossing",
        "PN public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à distance": "level_crossing",
        "PN public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à pied d'oeuvre": "level_crossing",
        "PN public pour voitures avec barrières gardé sans passage piétons accolé à pied d'oeuvre et distance": "level_crossing",
        "PN public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à distance": "level_crossing",
        "PN public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à pied d'oeuvre": "level_crossing",
        "PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 et SAL 2B": "level_crossing",
        "PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 + ilôt séparateur": "level_crossing",
        "PN public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 4": "level_crossing",
        "PN public pour voitures sans barrières avec SAL 0": "level_crossing",
        "PN public pour voitures sans barrières protection assurée par un agent": "level_crossing",
        "PN public pour voitures sans barrières sans SAL": "level_crossing",
    }
