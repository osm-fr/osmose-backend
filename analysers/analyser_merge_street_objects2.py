#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2020                                      ##
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


class Analyser_Merge_Street_Objects2(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)
        if "country" not in self.config.options:
            return

        mapping = 'merge_data/mapillary-street-tags.mapping.json'
        mapingfile = json.loads(open(mapping).read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Street_Objects2, r['class'], r['class'], r['level'], r['otype'], r['conflation'], r['title'], r['object'], r['select_tags'], r['generate_tags'], mapping, 'image_detections', 'tags')


class SubAnalyser_Merge_Street_Objects2(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, classs, level, otype, conflation, title, object, selectTags, generateTags, mapping, source, layer):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = 8360, id = classs, level = level, tags = ['merge', 'leisure'],
            title = T_f('Unmapped {0}', title),
            detail = T_f('Street object ({1}) detected by Mapillary, but no nearby "{0}" tagging.',
                ', '.join(map(lambda kv: '%s=%s' % (kv[0], kv[1] if kv[1] else '*'), generateTags.items())), title),
            fix = T_('Map the corresponding object if the imagery is up-to-date and object detection is correct.'))

        self.init(
            "https://www.mapillary.com",
            u"Street Objects from Street-level imagery",
            CSV(Source_Mapillary(attribution = u"Mapillary Street Objects", country = config.options['country'], polygon_id = config.polygon_id, logger = logger, mapping = mapping, source = source, layer = layer)),
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
                    mapping1 = {
                      "mapillary": "image_key",
                      "survey:date": lambda res: res["last_seen_at"][0:10]},
                text = lambda tags, fields:
                    T_f('Observed between {0} and {1}', fields["first_seen_at"][0:10], fields["last_seen_at"][0:10]) if fields["first_seen_at"][0:10] != fields["last_seen_at"][0:10] else
                    T_f('Observed on {0}', fields["first_seen_at"][0:10]) )))
