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
from modules.OsmoseTranslation import T_
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import CSV, Load, Conflate, Select, Mapping
from .Analyser_Merge_Mapillary import Source_Mapillary


class Analyser_Merge_Traffic_Signs(Analyser_Merge_Dynamic):

    def check_not_only_for(self, not_for, only_for):
        country = "country" in self.config.options and self.config.options["country"]
        if only_for:
            return country and any(map(lambda co: country.startswith(co), only_for))
        if not_for:
            return not country or not any(map(lambda co: country.startswith(co), not_for))
        return True

    def value_replace(self, v, key, replacement):
        if isinstance(v, dict):
            return dict(map(lambda kv: [kv[0], self.value_replace(kv[1], key, replacement)], v.items()))
        elif isinstance(v, list):
            return list(map(lambda vv: self.value_replace(vv, key, replacement), v))
        else:
            return v.replace(key, replacement)

    def dict_replace(self, d, f, r):
        return dict(map(lambda kv: [kv[0], kv[1] and self.value_replace(kv[1], f, r)], d.items()))

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)
        if "country" not in self.config.options:
            return

        speed_limit_unit = self.config.options.get("speed_limit_unit")

        mapping = 'merge_data/mapillary-traffic-signs.mapping.json'
        mapingfile = json.loads(open(mapping).read())
        for r in mapingfile:
            if self.check_not_only_for(r.get('not_for'), r.get('only_for')):
                if speed_limit_unit:
                    unit = ' ' + speed_limit_unit
                else:
                    unit = ''
                r['select_tags'] = list(map(lambda select: self.dict_replace(select, '{speed_limit_unit}', unit), r['select_tags']))
                r['generate_tags'] = self.dict_replace(r['generate_tags'], '{speed_limit_unit}', unit)

                self.classFactory(SubAnalyser_Merge_Traffic_Signs, r['class'], r['item'], r['class'], r['level'], r.get('tags', []), r['otype'], r['conflation'], r['title'], r['object'], r['select_tags'], r['generate_tags'], mapping, 'map_features', 'trafficsigns')


class SubAnalyser_Merge_Traffic_Signs(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, item, classs, level, tags, otype, conflation, title, object, selectTags, generateTags, mapping, source, layer):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)

        missing_tags = []
        for selection in selectTags:
            missing_tags.append(' + '.join(
                ['`{}={}`'.format(kv[0], kv[1] if kv[1] else '*') for kv in selection.items()]
            ))

        self.def_class_missing_official(item = item, id = classs, level = level, tags = ['merge', 'highway', 'fix:picture', 'fix:survey'] + tags,
            title = T_('Unmapped {0}', T_(title)),
            detail = T_('Traffic sign ({1}) detected by Mapillary, but no nearby tagging of any:{0}', '\n\n- ' + '\n- '.join(missing_tags), T_(title)),
            fix = T_('Add the appropriate highway tagging if the imagery is up-to-date and sign detection is correct.'))

        self.init(
            "https://www.mapillary.com",
            u"Traffic Signs from Street-level imagery",
            CSV(Source_Mapillary(attribution = u"Mapillary Traffic Signs", country = config.options['country'], polygon_id = config.polygon_id, logger = logger, mapping = mapping, source = source, layer = layer)),
            Load("X", "Y",
                select = {"value": object}),
            Conflate(
                select = Select(
                    types = otype,
                    tags = selectTags),
                conflationDistance = conflation,
                subclass_hash = lambda fields: {'image_key': fields['image_key'], 'value': fields['value']},
                mapping = Mapping(
                    static1 = dict(filter(lambda kv: kv[1], generateTags.items())),
                    static2 = {"source": self.source},
                    mapping1 = {
                        "mapillary": "image_key",
                        "survey:date": lambda res: res["last_seen_at"][0:10]},
                    text = lambda tags, fields:
                        T_('Observed between {0} and {1}', fields["first_seen_at"][0:10], fields["last_seen_at"][0:10]) if fields["first_seen_at"][0:10] != fields["last_seen_at"][0:10] else
                        T_('Observed on {0}', fields["first_seen_at"][0:10]) )))
