#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2020                                      ##
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

import csv
from .IssuesFile import IssuesFile


class IssuesFileCsv(IssuesFile):

    def begin(self):
        self.csv = csv.writer(super().begin())
        self.csv.writerow(['classs', 'subclass', 'ids', 'types', 'text', 'lon', 'lat', 'fix'])

    def end(self):
        del self.csv

    def error(self, classs, subclass, text, ids, types, fix, geom, allow_override=False):
        if self.filter and not self.filter.apply(classs, subclass, geom):
            return

        try:
            lat = geom['position'][0]['lat']
            lon = geom['position'][0]['lon']
        except:
            lat = lon = None
        self.csv.writerow([classs, subclass, ids, types, text and text.get('en'), lon, lat, fix])
