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

import requests, time, os, shutil, hashlib, codecs, tempfile
import json, csv
from modules import config
from modules.PointInPolygon import PointInPolygon
from modules import SourceVersion


class Analyser_Merge_Traffic_Signs(Analyser_Merge_Dynamic):

    def check_not_only_for(self, not_for, only_for):
        country = "country" in self.config.options and self.config.options["country"]
        if only_for:
            return country and any(map(lambda co: co.startswith(country), only_for))
        if not_for:
            return not country or not any(map(lambda co: co.startswith(country), not_for))
        return True


    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)
        if "country" not in self.config.options:
            return

        mapingfile = json.loads(open("merge_data/mapillary-traffic-signs.mapping.json", "rb").read())
        for r in mapingfile:
            if self.check_not_only_for(r.get('not_for'), r.get('only_for')):
                self.classFactory(SubAnalyser_Merge_Traffic_Signs, r['class'], r['class'], r['level'], r['otype'], r['conflation'], r['title'], r['sign'], r['select_tags'], r['generate_tags'])


class SubAnalyser_Merge_Traffic_Signs(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, classs, level, otype, conflation, title, sign, selectTags, generateTags):
        self.missing_official = {"item":"8300", "class": classs, "level": level, "tag": ["merge", "leisure"], "desc": T_(u"%s Traffic signs for %s observed around but not associated tags", ', '.join(map(lambda kv: '%s=%s' % (kv[0], kv[1] if kv[1] else '*'), generateTags.items())), title) }
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            "www.mapillary.com",
            u"Traffic Signs from Street-level imagery",
            CSV(Source(attribution = u"Mapillary Traffic Signs", millesime = "10/2018", fetcher = self.fetch_cached)),
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


    def fetch_cached(self):
      country = self.config.options['country']
      polygon_id = self.config.polygon_id
      delay = 120
      url = 'mapillary-feature-{0}-{1}.csv'.format(country, SourceVersion.version("merge_data/mapillary-traffic-signs.mapping.json"))

      file_name = hashlib.sha1(url.encode('utf-8')).hexdigest()
      cache = os.path.join(config.dir_cache, file_name)

      cur_time = time.time()

      if os.path.exists(cache):
        statbuf = os.stat(cache)
        if (cur_time - delay*24*60*60) < statbuf.st_mtime:
          # force cache by local delay
          return cache

      tmp_file = self.fetch(polygon_id)

      outfile = codecs.open(cache+".url", "w", "utf-8")
      outfile.write(url)
      outfile.close()
      shutil.move(tmp_file, cache)

      # set timestamp
      os.utime(cache, (cur_time, cur_time))

      return cache


    def fetch(self, polygon_id):
      fd, tmp_file = tempfile.mkstemp()

      pip = PointInPolygon(polygon_id, 60)

      traffic_signs = []
      reader = json.loads(open('merge_data/mapillary-traffic-signs.mapping.json', 'r').read())
      try:
        for row in reader:
          traffic_signs += row['sign']
      except:
        self.logger.log(row)
        raise

      with open(tmp_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['accuracy', 'direction', 'image_key', 'first_seen_at', 'last_seen_at', 'value', 'X', 'Y'])

      slice = lambda A, n: [A[i:i+n] for i in range(0, len(A), n)]

      bbox = pip.bbox()

      sleep = 1
      b = 0
      for traffic_signs_ in slice(traffic_signs, 10):
        b = b +1
        self.logger.log('Batch {0}/{1}: {2}'.format(b, round(len(traffic_signs) / 10 + 0.5), ','.join(traffic_signs_)))
        url = 'https://a.mapillary.com/v3/map_features?bbox={bbox}&client_id={client_id}&layers=trafficsigns&per_page=1000&start_time={start_time}&values={values}'.format(bbox=','.join(map(str, bbox)), client_id='MEpmMTFQclBTUWlacjV6RTUxWWMtZzo5OTc2NjY2MmRiMDUwYmMw', start_time='2016-06-01', values=','.join(traffic_signs_))
        with open(tmp_file, 'a') as csvfile:
          writer = csv.writer(csvfile)

          try:
            page = 0
            while(url):
              page = page + 1
              self.logger.log("Page {0}".format(page))
              while True:
                r = requests.get(url=url)
                if r.status_code != 502 and r.status_code != 504:
                  sleep = int(sleep / 2 + 0.5)
                  break
                else:
                  self.logger.log("Too fast: sleep {0}".format(sleep))
                  time.sleep(sleep)
                  sleep = sleep * 2
              url = r.links['next']['url'] if 'next' in r.links else None

              features = json.loads(r.text)['features']
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
          except:
            self.logger.log(url)
            self.logger.log(str(r.status_code))
            self.logger.log(r.text[0:200])
            raise

      return tmp_file
