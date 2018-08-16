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

import json
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Mapping, Select, Generate
from time import gmtime, strftime


class Analyser_Merge_Traffic_Signs(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        self.analysers = []
        mapingfile = json.loads(open("merge_data/mapillary-traffic-signs.mapping.json", "rb").read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Traffic_Signs, r['class'], r['class'], r['level'], r['otype'], r['conflation'], r['title'], r['sign'], r['select_tags'], r['generate_tags'])


class SubAnalyser_Merge_Traffic_Signs(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, classs, level, otype, conflation, title, sign, selectTags, generateTags):
        self.missing_official = {"item":"8300", "class": classs, "level": level, "tag": ["merge", "leisure"], "desc": T_(u"%s Traffic signs for %s observed around but not associated tags", ', '.join(map(lambda kv: '%s=%s' % (kv[0], kv[1] if kv[1] else '*'), generateTags.items())), title) }
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            "www.mapillary.com",
            u"Traffic Signs from Street-level imagery",
            CSV(Source(attribution = u"Mapillary Traffic Signs", millesime = "07/2018",
                    file = "mapillary-traffic-signs_%s.csv.bz2" % config.options["country"][0:2])),
            Load("X", "Y",
                select = {"value": sign}),
            Mapping(
                select = Select(
                    types = otype,
                    tags = selectTags),
                conflationDistance = conflation,
                generate = Generate(
                    static1 = dict(filter(lambda kv: kv[1], generateTags.items())),
                    static2 = {"source": self.source},
                    mapping1 = {"mapillary": "image_key"},
                text = lambda tags, fields: {"en": (
                    "Observed between %s and %s" % (fields["first_seen_at"][0:10], fields["last_seen_at"][0:10]) if fields["first_seen_at"][0:10] != fields["last_seen_at"][0:10] else
                    "Observed on %s" % (fields["first_seen_at"][0:10],))} )))
