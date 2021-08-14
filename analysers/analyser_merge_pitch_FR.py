#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2021                                 ##
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

import csv
from modules.OsmoseTranslation import T_
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Pitch_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        with open("merge_data/pitch_FR.mapping.csv") as mappingfile:
            spamreader = csv.reader(mappingfile)
            for row in spamreader:
                classs, topic = row[0:2]
                tags = list(map(lambda t: t.split('=') if t else None, row[2:5]))
                osmTags = dict(filter(lambda t: t, tags[0:2]))
                if len(osmTags) > 0:
                    defaultTags = dict(filter(lambda t: t, tags[2:3]))
                    self.classFactory(SubAnalyser_Merge_Pitch_FR, classs, classs, topic, osmTags, defaultTags)


class SubAnalyser_Merge_Pitch_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, classs, topic, osmTags, defaultTags):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = 8170, id = classs, level = 3, tags = ['merge', 'leisure', 'fix:imagery', 'fix:survey'],
            title = T_('Pitch not integrated {0}', topic))

        self.init(
            "https://equipements-sgsocialgouv.opendatasoft.com/explore/dataset/data-es/table/",
            "Data ES",
            # Source fileUrl is HTTP 404, but keeping it as per
            # https://github.com/osm-fr/osmose-backend/pull/1092#pullrequestreview-577717867
            CSV(SourceOpenDataSoft(
                    attribution = "Le ministère de la ville, de la jeunesse et des sports",
                    url = "https://equipements-sgsocialgouv.opendatasoft.com/explore/dataset/data-es/")),
            Load("Longitude (WGS84)", "Latitude (WGS84)",
                select = {"Type d'équipement sportif": topic},
                where = lambda row: self.validLatLon(row)),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = osmTags),
                conflationDistance = 200,
                mapping = Mapping(
                    static1 = dict(dict(**osmTags), **defaultTags),
                    static2 = {"source": self.source},
                    mapping1 = {"surface": self.surface},
                text = lambda tags, fields: {"en": ", ".join(filter(lambda i: i != "None", [fields["Numéro de l'installation sportive"], fields["Type d'équipement sportif"], fields["Nom de l'installation sportive"], fields["Nom du bâtiment"]]))} )))

    def validLatLon(self, row):
        if abs(float(row["Longitude (WGS84)"])) <= 180 and abs(float(row["Latitude (WGS84)"])) <= 90:
            return row
        else:
            return []

    surfaceMap = {
        "Sable": "sand",
        "Gazon naturel": "grass",
        "Bitume": "asphalt",
        "Béton": "concrete",
        "Gazon synthétique": "artificial_turf",
        "Bois": "wood",
        "Terre battue": "clay",
        "Métal": "metal",
        # 2967 Carrelage
        # 4637 Parquet
    }


    def surface(self, res):
        return self.surfaceMap.get(res["Nature du sol"])
