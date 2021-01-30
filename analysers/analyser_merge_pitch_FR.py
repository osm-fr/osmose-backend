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

import csv
from modules.OsmoseTranslation import T_
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Conflate, Select, Mapping


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
        self.def_class_missing_official(item = 8170, id = classs, level = 3, tags = ['merge', 'leisure'],
            title = T_('Pitch not integrated {0}', topic))

        self.init(
            "http://www.data.gouv.fr/fr/dataset/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques",
            "Recensement des équipements sportifs, espaces et sites de pratiques",
            # Source fileUrl is HTTP 404, but keeping it as per
            # https://github.com/osm-fr/osmose-backend/pull/1092#pullrequestreview-577717867
            CSV(Source(attribution = "Le ministère de la ville, de la jeunesse et des sports", millesime = "01/2018",
                    fileUrl = "https://www.data.gouv.fr/s/resources/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques/20180112-114703/20180110_RES_FichesEquipements.zip", zip = "20180110_RES_FichesEquipements.csv", encoding = "ISO-8859-15"),
                separator = u';'),
            Load("EquGpsX", "EquGpsY",
                select = {"EquipementTypeLib": topic},
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
                text = lambda tags, fields: {"en": ", ".join(filter(lambda i: i is not None, [fields["EquipementTypeLib"], fields["InsNo"], fields["EquNom"], fields["EquNomBatiment"]]))} )))

    def validLatLon(self, row):
        if abs(float(row["EquGpsX"])) <= 180 and abs(float(row["EquGpsY"])) <= 90:
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
    }

    def surface(self, res):
        if res["NatureSolLib"] in self.surfaceMap:
            return self.surfaceMap[res["NatureSolLib"]]
        else:
            return None
