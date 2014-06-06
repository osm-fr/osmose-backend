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

import sys
import csv
from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class _Analyser_Merge_Pitch_FR(Analyser_Merge):
    def __init__(self, config, classs, topic, osmTags, defaultTags, logger):
        self.missing_official = {"item":"8030", "class": classs, "level": 3, "tag": ["merge", "leisure"], "desc": T_(u"Pitch not integrated") }
## TODO autres
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.data.gouv.fr/fr/dataset/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques",
                name = u"Recensement des équipements sportifs, fiches équipements",
                file = "pitch_FR.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = ';')),
            Load("EquGpsX", "EquGpsY", table = "pitch_fr",
                where = lambda row: self.validLatLon(row) and row["EquipementTypeLib"] == topic),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = osmTags),
                conflationDistance = 200,
                mapping = Mapping(
                    static = dict(dict({"source": u"data.gouv.fr:Le ministère des droits des femmes, de la ville, de la jeunesse et des sports - 2014"},
                        **osmTags), *defaultTags),
                text = lambda tags, fields: {"en": ", ".join(filter(lambda i: i and i != "None", [fields["EquipementTypeLib"], fields["InsNo"], fields["EquNom"], fields["EquNomBatiment"]]))} )))

    def validLatLon(self, row):
        if abs(float(row["EquGpsX"])) <= 180 and abs(float(row["EquGpsY"])) <= 90:
            return row
        else:
            return []

def ClassFactory(classs, topic, osmTags, defaultTags):
    def __init__(self, config, logger = None):
        self.osmTags = osmTags
        self.defaultTags = defaultTags
        _Analyser_Merge_Pitch_FR.__init__(self, config, classs, topic, osmTags, defaultTags, logger)
    newclass = type("Analyser_Merge_Pitch_FR_%s" % classs, (_Analyser_Merge_Pitch_FR,), {"__init__": __init__})
    return newclass

with open("merge_data/pitch_FR.mapping.csv", "rb") as mappingfile:
    spamreader = csv.reader(mappingfile)
    for row in spamreader:
        classs, topic = row[0:2]
        tags = map(lambda t: t.split('=') if t else None, row[2:5])
        osmTags = dict(filter(lambda t: t, tags[0:2]))
        if len(osmTags) > 0:
            defaultTags = dict(filter(lambda t: t, tags[2:3]))
            generatedClass = ClassFactory(classs, topic.decode('utf-8'), osmTags, defaultTags)
            setattr(sys.modules[__name__], generatedClass.__name__, generatedClass)
