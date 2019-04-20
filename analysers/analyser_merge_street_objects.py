#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
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
from .Analyser_Merge import CSV, Load, Mapping, Select, Generate
from .Analyser_Merge_Mapillary import Source_Mapillary

from io import open # In python3 only, this import is not required
from modules import config


class Analyser_Merge_Street_Objects(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)
        if "country" not in self.config.options:
            return

        mapping = 'merge_data/mapillary-street-objects.mapping.json'
        mapingfile = json.loads(open(mapping).read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Street_Objects, r['class'], r['class'], r['level'], r['otype'], r['conflation'], r['title'], r['object'], r['select_tags'], r['generate_tags'], mapping, 'points')


class SubAnalyser_Merge_Street_Objects(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, classs, level, otype, conflation, title, object, selectTags, generateTags, mapping, layer):
        self.missing_official = {"item":"8360", "class": classs, "level": level, "tag": ["merge", "leisure"], "desc": T_f(u"{0} Street object {1} observed around but not associated tags", ', '.join(map(lambda kv: '%s=%s' % (kv[0], kv[1] if kv[1] else '*'), generateTags.items())), title) }
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            "www.mapillary.com",
            u"Street Objects from Street-level imagery",
            CSV(Source_Mapillary(attribution = u"Mapillary Street Objects", millesime = "04/2019", country = config.options['country'], polygon_id = config.polygon_id, logger = logger, mapping = mapping, layer = layer)),
            Load("X", "Y",
                select = {"value": object}),
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
