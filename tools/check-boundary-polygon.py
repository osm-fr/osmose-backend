#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Rodrigo Frédéric 2014                                      ##
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

import sys
from shapely.geometry import MultiPolygon

sys.path.append("..")

from modules import OsmoseErrorFile_ErrorFilter
from modules import downloader

import osmose_config as config


# Function based on http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Python_Parsing
def parse_poly(lines):
    """ Parse an Osmosis polygon filter file.
        Accept a sequence of lines from a polygon file, return a shapely.geometry.MultiPolygon object.
        http://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Format
    """
    in_ring = False
    coords = []

    for (index, line) in enumerate(lines):
        if index == 0:
            # first line is junk.
            continue

        elif index == 1:
            # second line is the first polygon ring.
            coords.append([[], []])
            ring = coords[-1][0]
            in_ring = True

        elif in_ring and line.strip() == 'END':
            # we are at the end of a ring, perhaps with more to come.
            in_ring = False

        elif in_ring:
            # we are in a ring and picking up new coordinates.
            ring.append(map(float, line.split()))

        elif not in_ring and line.strip() == 'END':
            # we are at the end of the whole polygon.
            break

        elif not in_ring and line.startswith('!'):
            # we are at the start of a polygon part hole.
            coords[-1][1].append([])
            ring = coords[-1][1][-1]
            in_ring = True

        elif not in_ring:
            # we are at the start of a polygon part.
            coords.append([[], []])
            ring = coords[-1][0]
            in_ring = True

    return MultiPolygon(coords)


def load_poly(poly):
    try:
        print poly
        s = downloader.urlread(poly, 1)
        return parse_poly(s.split('\n'))
    except IOError as e:
        print e
        return


for country, country_conf in config.config.iteritems():
    if not country_conf.polygon_id:
        print "Warning(%s): no polygon_id" % country
    elif not 'poly' in country_conf.download:
        print "Warning(%s): no poly declared" % country
    else:
        #print "%s" % country
        poly = load_poly(country_conf.download['poly'])
        if not poly:
            print "Warning(%s): no poly fetched : %s" % (country, country_conf.download['poly'])
        else:
            polygonFilter = OsmoseErrorFile_ErrorFilter.PolygonErrorFilter(country_conf.polygon_id, cache_delay=1)
            if not polygonFilter.polygon.is_valid:
                print "Error(%s) boundary not valid (r_id=%s)" % (country, country_conf.polygon_id)
            if not poly.is_valid:
                print "Error(%s) poly not valid (%s)" % (country, country_conf.polygon_id)
            try:
                if not poly.contains(polygonFilter.polygon):
                    print "Error(%s) poly inside boundary (%s)" % (country, country_conf.download_repo)
            except:
                print "Error(%s) evaluating intersection" % country
