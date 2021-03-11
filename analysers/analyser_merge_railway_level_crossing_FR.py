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
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, GeoJSON, Load, Conflate, Select, Mapping


class Analyser_Merge_Railway_Level_Crossing_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8060, id = 1, level = 3, tags = ['merge', 'railway', 'fix:survey', 'fix:imagery'],
            title = T_('Crossing level not integrated'))

        self.init(
            "https://data.sncf.com/explore/dataset/liste-des-passages-a-niveau",
            "Passages à niveau",
            GeoJSON(
                SourceOpenDataSoft(
                    attribution="SNCF Réseau",
                    url="https://data.sncf.com/explore/dataset/liste-des-passages-a-niveau",
                    format="geojson")),
            Load("geom_x", "geom_y",
                where = lambda res: res["mnemo"] != "CLASSE 00"),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"railway": ["level_crossing", "crossing"]}),
                conflationDistance = 150,
                mapping = Mapping(
                    static2 = {"source": self.source},
                    mapping1 = {"railway": lambda res: self.type[res["mnemo"]]},
                    mapping2 = {"ref": lambda res: self.ref(res["libelle"])} )))

    def ref(self, libelle):
        if libelle.startswith("PN"):
            libelle = libelle[2:]
        libelle = libelle.strip()
        return libelle

    type = {
        "CLASSE 00": None, # secondaire
        "CLASSE 46": "crossing", # privé isolé pour piétons avec portillons
        "CLASSE 45": "crossing", # privé isolé pour piétons sans portillons
        "CLASSE 44": "level_crossing", # privé pour voitures avec barrières avec passage piétons accolé privé
        "CLASSE 43": "level_crossing", # privé pour voitures avec barrières avec passage piétons accolé public
        "CLASSE 42": "level_crossing", # privé pour voitures avec barrières sans passage piétons accolé
        "CLASSE 41": "level_crossing", # privé pour voitures sans barrières
        "CLASSE 32": "crossing", # public isolé pour piétons avec portillons
        "CLASSE 31": "crossing", # public isolé pour piétons sans portillons
        "CLASSE 16": "level_crossing", # public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à pied d'oeuvre distance
        "CLASSE 15": "level_crossing", # public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à distance
        "CLASSE 14": "level_crossing", # public pour voitures avec barrières gardé avec passage piétons accolé manoeuvré à pied d'oeuvre
        "CLASSE 13": "level_crossing", # public pour voitures avec barrières gardé sans passage piétons accolé à pied d'oeuvre et distance
        "CLASSE 12": "level_crossing", # public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à distance
        "CLASSE 11": "level_crossing", # public pour voitures avec barrières gardé sans passage piétons accolé manoeuvré à pied d'oeuvre
        "CLASSE 17": "level_crossing", # public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 et SAL 2B
        "CLASSE 18": "level_crossing", # public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 2 + ilôt séparateur
        "CLASSE 19": "level_crossing", # public pour voitures avec barrières ou 1/2 barrières non gardé à SAL 4
        "CLASSE 21": "level_crossing", # public pour voitures sans barrières avec SAL 0
        "CLASSE 10": "level_crossing", # public pour voitures sans barrières protection assurée par un agent
        "CLASSE 20": "level_crossing", # public pour voitures sans barrières sans SAL
    }
