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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
  pitch.id,
  ST_AsText(way_locate(pitch.linestring))
FROM
  ways AS pitch
  LEFT JOIN ways AS site ON
    site.linestring && pitch.linestring AND
    site.tags != ''::hstore AND
    site.tags?'tourism' AND
    site.tags->'tourism' IN ('camp_site', 'caravan_site')
WHERE
  pitch.tags != ''::hstore AND
  pitch.tags ?| ARRAY['tourism', 'camp_site'] AND
  (pitch.tags->'tourism' = 'camp_pitch' OR pitch.tags->'camp_site' IN ('camp_pitch', 'pitch')) AND
  site.id IS NULL
"""

sql11 = """
SELECT
  pitch.id,
  ST_AsText(pitch.geom)
FROM
  nodes AS pitch
  LEFT JOIN ways AS site ON
    site.linestring && pitch.geom AND
    site.tags != ''::hstore AND
    site.tags?'tourism' AND
    site.tags->'tourism' IN ('camp_site', 'caravan_site')
WHERE
  pitch.tags != ''::hstore AND
  pitch.tags ?| ARRAY['tourism', 'camp_site'] AND
  (pitch.tags->'tourism' = 'camp_pitch' OR pitch.tags->'camp_site' IN ('camp_pitch', 'pitch')) AND
  site.id IS NULL
"""

class Analyser_Osmosis_Camp_Pitch_Out_Of_Camp_Site(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1290", "level": 2, "tag": ["geom", "fix:chair"], "desc": T_(u"Camp pitchs outside a camp site") }

    def analyser_osmosis_common(self):
        self.run(sql10, lambda res: {"class":1, "subclass":1, "data":[self.way_full, self.positionAsText]})
        self.run(sql11, lambda res: {"class":1, "subclass":2, "data":[self.node_full, self.positionAsText]})
