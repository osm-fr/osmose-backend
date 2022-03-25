#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2022                                      ##
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

import csv
from modules.PointInPolygon import PointInPolygon
from modules import SourceVersion
from modules import downloader
from datetime import datetime, timedelta
from vt2geojson.tools import vt_bytes_to_geojson # type: ignore
from tiletanic import tilecover, tileschemes # type: ignore
import pyproj
from shapely.ops import transform


class Source_Mapillary(Source):
    def __init__(self, country, polygon_id, mapping, source, layer, logger, **args):
        self.polygon_id = polygon_id
        self.mapping = mapping
        self.source = source
        self.layer = layer
        self.logger = logger
        Source.__init__(self, **args)
        self.fileUrl = u'mapillary-{0}-{1}-{2}-{3}.csv'.format(source, country, polygon_id, SourceVersion.version(self.mapping))
        self.fileUrlCache = 120

    def time(self):
        self.open()
        return Source.time(self)

    def open(self):
        return open(downloader.update_cache(self.fileUrl, 60, self.fetch))

    def tile_generator(self, polygon, zoom=14):
        wgs84 = pyproj.CRS('EPSG:4326')
        webMarcator = pyproj.CRS('EPSG:3857')
        project = pyproj.Transformer.from_crs(wgs84, webMarcator, always_xy=True).transform
        polygon = transform(project, polygon)

        tiler = tileschemes.WebMercator()
        for t in tilecover.cover_geometry(tiler, polygon, zoom):
            yield [t.z, t.x, t.y]

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

        start_time = (datetime.today() - timedelta(days=365*2)).timestamp()
        MLY_ACCESS_TOKEN = 'MLY|3804396159685239|c5712d0fb9ef5d4dfef585154b00ffa7'

        with open(tmp_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'first_seen_at', 'last_seen_at', 'value', 'X', 'Y'])

            tiles = list(self.tile_generator(pip.polygon.polygon))
            n_tiles = len(tiles)
            for (n, [z, x, y]) in enumerate(tiles):
                if n % 500 == 0:
                    self.logger.log(f"{n} / {n_tiles}")

                if self.layer == 'trafficsigns':
                    url = f"https://tiles.mapillary.com/maps/vtp/mly_map_feature_traffic_sign/2/{z}/{x}/{y}/?access_token={MLY_ACCESS_TOKEN}"
                elif self.layer == 'points':
                    url = f"https://tiles.mapillary.com/maps/vtp/mly_map_feature_point/2/{z}/{x}/{y}/?access_token={MLY_ACCESS_TOKEN}"

                r = downloader.get(url).content
                # Tile on cache alternative
                # r = downloader.urlopen(url, delay=60, mode='rb').read()

                if not r:
                    continue
                geojson = vt_bytes_to_geojson(r, x, y, z)
                # {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-109.24706518650055, 45.18212758443923]}, 'properties': {'first_seen_at': 1506796436000, 'id': 224422696115054, 'last_seen_at': 1506796436000, 'value': 'complementary--keep-left--g1'}}]}

                features = filter(lambda feature:
                    feature['geometry']['type'] == 'Point' and
                    feature['properties']['last_seen_at'] / 1000 > start_time and
                    pip.point_inside_polygon(*feature['geometry']['coordinates']),
                    geojson['features']
                )
                for feature in features:
                    p = feature['properties']
                    row = [p['id'], int(p['first_seen_at'] / 1000), int(p['last_seen_at'] / 1000), p['value']]
                    writer.writerow(row + feature['geometry']['coordinates'])

        return True
