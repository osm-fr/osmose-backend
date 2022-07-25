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
import json


class Geocode_City_CSV(Source):

    def __init__(self, source, logger, citycode = None, delimiter = ',', encoding = 'utf-8'):
        self.source = source
        self.delimiter = delimiter
        self.citycode = citycode
        self.encoding = encoding
        self.logger = logger

    def __getattr__(self, name):
        return getattr(self.source, name)

    def open(self):
        return open(downloader.update_cache('citycoded://' + self.source.fileUrl, 60, fetch=self.fetch))

    def fetch(self, url, tmp_file, date_string=None):
        service = u'https://geo.api.gouv.fr/communes/'
        outfile = open(tmp_file, 'w', encoding='utf-8')

        infile = self.source.open()
        header = None
        i = 0
        
        for linestr in infile:
            outline = linestr.split(self.delimiter)

            if i == 0:
                outline.extend(["longitude", "latitude"])
                header = outline
            else:
                self.logger.log("Geocode line {0}".format(i))
                r = downloader.requests_retry_session().get(url=service+outline[header[self.citycode]], params={
                    'fields': 'centre',
                    'format': 'json',
                    'geometry': 'centre',
                })

                r.raise_for_status()
                rData = json.loads(r.text)

                outline.extend(rData["centre"]["coordinates"])
            
            outfile.write(self.delimiter.join(outline))
            i += 1

        return True
