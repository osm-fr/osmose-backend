#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

from Analyser_Osmosis import Analyser_Osmosis

sql10 = """
SELECT
    id,
    AsText(ST_Centroid(linestring))
FROM
    ways
WHERE
    tags ? 'junction' AND
    tags->'junction' = 'roundabout' AND
    is_polygon AND
    ST_IsSimple(linestring) AND
    ST_OrderingEquals(linestring, st_forceRHR(linestring))
;
"""

class Analyser_Osmosis_Roundabout_Reverse(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item":"1050", "desc":{"fr":"Rond-point à l'envers", "en":"Reverse roundabout"} } # FIXME "menu":"rond-point à l'envers", "menu":"reverse roundabout"

    def analyser_osmosis(self):
        self.run(sql10, lambda res: {"class":1, "data":[self.way_full, self.positionAsText]} )
