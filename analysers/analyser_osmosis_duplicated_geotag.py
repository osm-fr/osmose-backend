#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Didier Marchand  <****@free.fr> 2013                       ##
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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMP TABLE cvqnotag AS
SELECT
    *
FROM
(
    SELECT
        ways.id,
        ways.linestring
    FROM
        ways
        LEFT JOIN relation_members ON
            relation_members.member_id = ways.id AND
            relation_members.member_type = 'W'
    WHERE
        relation_members.member_id IS NULL AND
        ways.tags = ''::hstore AND
        ST_NPoints(ways.linestring) > 1
) AS t
WHERE
    ST_IsValid(linestring)
"""

sql11 = """
CREATE INDEX cvqnotag_linestring_idx ON cvqnotag USING gist(linestring)
"""

sql12 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(b1.linestring))
FROM
    cvqnotag AS b1,
    cvqnotag AS b2
WHERE
    b1.id > b2.id AND
    b1.linestring && b2.linestring AND
    ST_Equals(b1.linestring, b2.linestring)
"""

sql20 = """
CREATE TEMP TABLE cvq AS
SELECT
    id,
    linestring,
    delete(delete(tags, 'source'), 'create_by') as lsttag
FROM
    ways
WHERE
    tags ?| ARRAY['natural', 'landuse', 'waterway', 'amenity', 'highway', 'leisure', 'barrier', 'railway', 'addr:interpolation', 'man_made', 'power'] AND
    ST_NPoints(ways.linestring) > 1 AND
    ST_IsValid(linestring)
"""

sql21 = """
CREATE INDEX cvq_linestring_idx ON cvq USING gist(linestring)
"""

sql22 = """
SELECT
    b1.id AS id1,
    b2.id AS id2,
    ST_AsText(ST_Centroid(b1.linestring)),
--    ((b1.lsttag @> b2.lsttag ) AND (b2.lsttag @> b1.lsttag ))
    b1.lsttag = b2.lsttag
FROM
    cvq AS b1,
    cvq AS b2
WHERE
    b1.id > b2.id AND
    b1.linestring && b2.linestring AND
    ST_Equals(b1.linestring, b2.linestring) AND
    (
        (b1.lsttag->'natural' = b2.lsttag->'natural') OR
        (b1.lsttag->'landuse' = b2.lsttag->'landuse') OR
        (b1.lsttag->'waterway' = b2.lsttag->'waterway') OR
        (b1.lsttag->'amenity' = b2.lsttag->'amenity') OR
        (b1.lsttag->'highway' = b2.lsttag->'highway') OR
        (b1.lsttag->'leisure' = b2.lsttag->'leisure') OR
        (b1.lsttag->'barrier' = b2.lsttag->'barrier') OR
        (b1.lsttag->'railway' = b2.lsttag->'railway') OR
        (b1.lsttag->'addr:interpolation' = b2.lsttag->'addr:interpolation') OR
        (b1.lsttag->'man_made' = b2.lsttag->'man_made') OR
        (b1.lsttag->'power' = b2.lsttag->'power')
    ) AND
    (NOT b1.lsttag?'layer' AND NOT b2.lsttag?'layer' OR b1.lsttag->'layer' = b2.lsttag->'layer') AND
    (NOT b1.lsttag?'level' AND NOT b2.lsttag?'level' OR b1.lsttag->'level' = b2.lsttag->'level')
"""

class Analyser_Osmosis_Duplicated_Geotag(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1230", "level": 1, "tag": ["geom", "fix:chair"], "desc": T_(u"Duplicated geometry and tags") }
        self.classs[2] = {"item":"1230", "level": 2, "tag": ["geom", "fix:chair"], "desc": T_(u"Duplicated geometry but different tags") }
        self.callback10 = lambda res: {"class":1, "data":[self.way, self.way, self.positionAsText]}
        self.callback20 = lambda res: {"class":1 if res[3] else 2, "data":[self.way_full, self.way_full, self.positionAsText]}

    def analyser_osmosis_all(self):
        self.run(sql10.format(""))
        self.run(sql11.format(""))
        self.run(sql12.format("", ""), self.callback10)

        self.run(sql20.format(""))
        self.run(sql21.format(""))
        self.run(sql22.format("",""), self.callback20)
