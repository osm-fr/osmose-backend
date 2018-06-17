#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Mapping, Select, Generate
from time import gmtime, strftime


class Analyser_Merge_Traffic_Signs(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        with open("merge_data/mapillary-traffic-signs.mapping.csv", "rb") as mappingfile:
            spamreader = csv.reader(mappingfile)
            self.analysers = []
            for row in spamreader:
                if len(row) == 0 or row[0][0] == '#':
                    continue
                classs, level, otype, dist, title, topic = row[0:6]
                otype = otype.split('|')
                dist = int(dist)
                topic = topic.split('|')
                osmTags = map(lambda t: (t.split('=') + [None])[0:2] if t else None, row[6:])
                if len(osmTags) > 0:
                    self.classFactory(SubAnalyser_Merge_Traffic_Signs, classs, classs, level, otype, dist, title, topic, dict(osmTags), dict(filter(lambda a: a[1], osmTags)))


class SubAnalyser_Merge_Traffic_Signs(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, classs, level, otype, dist, title, topic, selectTags, generateTags):
        self.missing_official = {"item":"8300", "class": classs, "level": level, "tag": ["merge", "leisure"], "desc": T_(u"%s Traffic signs for %s observed around but not associated tags", ', '.join(map(lambda kv: '%s=%s' % (kv[0], kv[1] if kv[1] else '*'), selectTags.items())), title) }
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            "www.mapillary.com",
            u"Traffic Signs from Street-level imagery",
            CSV(Source(attribution = u"Mapillary Traffic Signs - Osmose-QA Experiment", millesime = "07/2018",
                    file = "mapillary-traffic-signs_%s.csv.bz2" % config.options["country"])),
            Load("X", "Y",
                select = {"value": topic}),
            Mapping(
                select = Select(
                    types = otype,
                    tags = selectTags),
                conflationDistance = dist,
                generate = Generate(
                    static1 = generateTags,
                    static2 = {"source": self.source},
                    mapping1 = {"mapillary": "image_key"},
                text = lambda tags, fields: {"en": (
                    "Observed between %s and %s" % (fields["first_seen_at"][0:10], fields["last_seen_at"][0:10]) if fields["first_seen_at"][0:10] != fields["last_seen_at"][0:10] else
                    "Observed on %s" % (fields["first_seen_at"][0:10],))} )))
