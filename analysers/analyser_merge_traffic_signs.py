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

import time, os, shutil, hashlib, codecs, tempfile
from io import open # In python3 only, this import is not required
from backports import csv # In python3 only just "import csv"
from modules import config
from modules.PointInPolygon import PointInPolygon
from modules import SourceVersion
from modules import downloader


class Analyser_Merge_Traffic_Signs(Analyser_Merge_Dynamic):

    def check_not_only_for(self, not_for, only_for):
        country = "country" in self.config.options and self.config.options["country"]
        if only_for:
            return country and any(map(lambda co: country.startswith(co), only_for))
        if not_for:
            return not country or not any(map(lambda co: country.startswith(co), not_for))
        return True

    def dict_replace(self, d, f, r):
        return dict(map(lambda kv: [kv[0], kv[1] and kv[1].replace(f, r)], d.items()))

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)
        if "country" not in self.config.options:
            return

        speed_limit_unit = self.config.options.get("speed_limit_unit")

        mapingfile = json.loads(open("merge_data/mapillary-traffic-signs.mapping.json").read())
        for r in mapingfile:
            if self.check_not_only_for(r.get('not_for'), r.get('only_for')):
                if speed_limit_unit:
                    unit = ' ' + speed_limit_unit
                else:
                    unit = ''
                r['select_tags'] = list(map(lambda select: self.dict_replace(select, '{speed_limit_unit}', unit), r['select_tags']))
                r['generate_tags'] = self.dict_replace(r['generate_tags'], '{speed_limit_unit}', unit)

                self.classFactory(SubAnalyser_Merge_Traffic_Signs, r['class'], r['class'], r['level'], r['otype'], r['conflation'], r['title'], r['sign'], r['select_tags'], r['generate_tags'])


class SubAnalyser_Merge_Traffic_Signs(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, classs, level, otype, conflation, title, sign, selectTags, generateTags):
        self.missing_official = {"item":"8300", "class": classs, "level": level, "tag": ["merge", "leisure"], "desc": T_f(u"{0} Traffic signs for {1} observed around but not associated tags", ', '.join(map(lambda kv: '%s=%s' % (kv[0], kv[1] if kv[1] else '*'), generateTags.items())), title) }
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            "www.mapillary.com",
            u"Traffic Signs from Street-level imagery",
            CSV(Source_Mapillary(attribution = u"Mapillary Traffic Signs", millesime = "10/2018", country = config.options['country'], polygon_id = config.polygon_id, logger = logger)),
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


class Source_Mapillary(Source):
    def __init__(self, country, polygon_id, logger, **args):
      self.polygon_id = polygon_id
      self.logger = logger
      Source.__init__(self, **args)
      self.fileUrl = 'mapillary-feature-{0}-{1}.csv'.format(country, SourceVersion.version("merge_data/mapillary-traffic-signs.mapping.json"))
      self.fileUrlCache = 120

    def time(self):
       self.fetch_cached()
       return Source.time(self)

    def open(self):
      return self.fetch_cached()

    def fetch_cached(self):
      file_name = hashlib.sha1(self.fileUrl.encode('utf-8')).hexdigest()
      cache = os.path.join(config.dir_cache, file_name)

      cur_time = time.time()

      if os.path.exists(cache):
        statbuf = os.stat(cache)
        if (cur_time - self.fileUrlCache*24*60*60) < statbuf.st_mtime:
          # force cache by local delay
          return open(cache)

      tmp_file = self.fetch()

      outfile = codecs.open(cache+".url", "w", "utf-8")
      outfile.write(self.fileUrl)
      outfile.close()
      shutil.move(tmp_file, cache)

      # set timestamp
      os.utime(cache, (cur_time, cur_time))

      return open(cache)

    def fetch(self):
      fd, tmp_file = tempfile.mkstemp()

      pip = PointInPolygon(self.polygon_id, 60)

      traffic_signs = []
      reader = json.loads(open('merge_data/mapillary-traffic-signs.mapping.json', 'r').read())
      try:
        for row in reader:
          traffic_signs += row['sign']
      except:
        self.logger.err(row)
        raise

      with open(tmp_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['accuracy', 'direction', 'image_key', 'first_seen_at', 'last_seen_at', 'value', 'X', 'Y'])

      slice = lambda A, n: [A[i:i+n] for i in range(0, len(A), n)]

      bboxes = pip.bboxes()

      b = 0
      for traffic_signs_ in slice(traffic_signs, 10):
        b = b + 1
        self.logger.log('Batch {0}/{1}: {2}'.format(b, round(len(traffic_signs) / 10 + 0.5), ','.join(traffic_signs_)))
        for bbox in bboxes:
          url = 'https://a.mapillary.com/v3/map_features?bbox={bbox}&client_id={client_id}&layers=trafficsigns&per_page=1000&start_time={start_time}&values={values}'.format(bbox=','.join(map(str, bbox)), client_id='MEpmMTFQclBTUWlacjV6RTUxWWMtZzo5OTc2NjY2MmRiMDUwYmMw', start_time='2016-06-01', values=','.join(traffic_signs_))
          with open(tmp_file, 'a') as csvfile:
            writer = csv.writer(csvfile)

            r = None
            page = 0
            while(url):
              page = page + 1
              self.logger.log("Page {0}".format(page))
              r = downloader.get(url)
              url = r.links['next']['url'] if 'next' in r.links else None

              features = r.json()['features']
              filtered = 0
              self.logger.log('{0} features fetched'.format(len(features)))
              for j in features:
                p = j['properties']
                image_key = p['detections'][0]['image_key']
                gc = j['geometry']['coordinates']
                row = [p['accuracy'], p['direction'] if 'direction' in p else None, image_key, p['first_seen_at'], p['last_seen_at'], p['value']] + gc
                if row[0] > 0.01 and pip.point_inside_polygon(gc[0], gc[1]):
                  writer.writerow(row)
                  filtered = filtered + 1
              self.logger.log('{0} keeped'.format(filtered))

      return tmp_file
