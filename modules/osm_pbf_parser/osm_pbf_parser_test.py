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

import sys
import osm_pbf_parser

class V(osm_pbf_parser.Visitor):
  def node(self, osmid, lon, lat, tags):
    print('node', osmid, tags)

  def way(self, osmid, tags, refs):
    print('way', osmid, tags, refs)

  def relation(self, osmid, tags, ref):
    print('relation', osmid, tags, ref)

v = V()

osm_pbf_parser.read_osm_pbf(sys.argv[1], v)
