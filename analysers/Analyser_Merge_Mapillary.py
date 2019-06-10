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
from .Analyser_Merge import Source

import time, os, shutil, hashlib, codecs, tempfile
from io import open # In python3 only, this import is not required
from backports import csv # In python3 only just "import csv"
from modules import config
from modules.PointInPolygon import PointInPolygon
from modules import SourceVersion
from modules import downloader
from datetime import datetime, timedelta


class Source_Mapillary(Source):
    def __init__(self, country, polygon_id, mapping, layer, logger, **args):
      self.polygon_id = polygon_id
      self.mapping = mapping
      self.layer = layer
      self.logger = logger
      Source.__init__(self, **args)
      self.fileUrl = u'mapillary-feature-{0}-{1}.csv'.format(country, SourceVersion.version(self.mapping))
      self.fileUrlCache = 120

    def time(self):
      self.open()
      return Source.time(self)

    def open(self):
      return open(downloader.update_cache(self.fileUrl, 60, self.fetch))

    def fetch(self, url, tmp_file, date_string=None):
      pip = PointInPolygon(self.polygon_id, 60)

      traffic_signs = []
      reader = json.loads(open(self.mapping, 'r').read())
      try:
        for row in reader:
          traffic_signs += row['object']
      except:
        self.logger.err(row)
        raise

      with open(tmp_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['accuracy', 'direction', 'image_key', 'first_seen_at', 'last_seen_at', 'value', 'X', 'Y'])

      slice = lambda A, n: [A[i:i+n] for i in range(0, len(A), n)]

      bboxes = pip.bboxes()

      start_time = (datetime.today() - timedelta(days=365*2)).isoformat()[0:10]
      b = 0
      for traffic_signs_ in slice(traffic_signs, 10):
        b = b + 1
        self.logger.log('Batch {0}/{1}: {2}'.format(b, round(len(traffic_signs) / 10 + 0.5), ','.join(traffic_signs_)))
        for bbox in bboxes:
          url = 'https://a.mapillary.com/v3/map_features?bbox={bbox}&client_id={client_id}&layers={layer}&per_page=1000&start_time={start_time}&values={values}'.format(bbox=','.join(map(str, bbox)), layer=self.layer, client_id='MEpmMTFQclBTUWlacjV6RTUxWWMtZzo5OTc2NjY2MmRiMDUwYmMw', start_time=start_time, values=','.join(traffic_signs_))
          self.logger.log(url)
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

      return True
