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

from io import open # In python3 only, this import is not required
from .Analyser_Merge import Source
from .modules import downloader


class Geocode_Addok_CSV(Source):

    def __init__(self, source, columns, logger, citycode = None, delimiter = ',', encoding = 'utf-8'):
        self.source = source
        self.columns = columns
        self.citycode = citycode
        self.delimiter = delimiter
        self.encoding = encoding
        self.logger = logger

    def __getattr__(self, name):
        return getattr(self.source, name)

    def open(self):
        return open(downloader.update_cache('geocoded://' + self.source.fileUrl, 60, self.fetch))

    def fetch(self, url, tmp_file, date_string=None):
        service = u'https://api-adresse.data.gouv.fr/search/csv/'
        outfile = open(tmp_file, 'w', encoding='utf-8')

        content = self.source.open().readlines()
        header = content[0:1]
        step = 2000
        slices = int((len(content)-1) / step) + 1
        for i in range(0, slices):
            self.logger.log("Geocode slice {0}/{1}".format(i, slices))
            slice = ''.join(header + content[1 + step*i : 1 + step*(i+1)])
            r = downloader.requests_retry_session().post(url=service, data={
                'delimiter': self.delimiter,
                'encoding': self.encoding,
                'columns': self.columns,
                'citycode': self.citycode,
            }, files={
                'data': slice,
            })
            r.raise_for_status()
            if i == 0:
                text = '\n'.join(r.text.split('\n')[0:])
            else:
                text = '\n'.join(r.text.split('\n')[1:])
            writer = outfile.write(text)

        return True
