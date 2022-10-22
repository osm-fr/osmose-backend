#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights François Lacombe 2022                                      ##
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
## This tool uses French administrative API to find center coordinates   ##
## of cities                                                             ##
## See https://geo.api.gouv.fr/decoupage-administratif                   ##
##                                                                       ##
###########################################################################

from .Analyser_Merge import Source
from modules import downloader
import csv
import json


class Geocode_FR_City_CSV(Source):

    def __init__(self, source, logger, citycode, delimiter = ',', encoding = 'utf-8'):
        self.source = source
        self.citycode = citycode
        self.delimiter = delimiter
        self.encoding = encoding
        self.logger = logger

    def __getattr__(self, name):
        return getattr(self.source, name)

    def open(self):
        return open(downloader.update_cache('citycoded://' + self.source.fileUrl, 60, fetch=self.fetch))

    def fetch(self, url, tmp_file, date_string=None):
        data = downloader.urlread('https://geo.api.gouv.fr/communes?zone=metro&fields=nom,code,codesPostaux,siren,codeEpci,codeDepartement,codeRegion,population&format=geojson&geometry=centre', delay=60)
        jdata = json.loads(data)
        mapCode = dict(map(lambda feature: [feature['properties']['code'], feature['geometry']['coordinates']], jdata['features']))

        with open(tmp_file, 'w', encoding='utf-8') as output:
            csv_writer = csv.writer(output, delimiter=self.delimiter)
            csv_reader = csv.reader(self.source.open(), delimiter=self.delimiter)

            headers = next(csv_reader)
            citycode_index = headers.index(self.citycode)
            csv_writer.writerow(headers + ['longitude', 'latitude'])
            for row in csv_reader:
                coords = mapCode.get(row[citycode_index], [None, None])
                csv_writer.writerow(row + coords)

        return True
