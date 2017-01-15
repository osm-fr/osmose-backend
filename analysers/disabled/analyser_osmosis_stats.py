#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
##            Frédéric Rodrigo <****@free.fr> 2010                       ##
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

sql_users = """
SELECT count({0}.id) as count, user_id, users.name,
       min(tstamp) AS tstamp_min, max(tstamp) AS tstamp_max
FROM {0}
JOIN users ON users.id = user_id
GROUP BY user_id, users.name
ORDER BY count desc;
"""

class Analyser_Osmosis_Stats(Analyser_Osmosis):

    def __init__(self, config, logger = None):
        Analyser_Osmosis.__init__(self, config, logger)

    def analyser_osmosis_common(self):
        for t in ("nodes", "ways", "relations"):
            self.outxml.startElement("stat_users", {"type": t})
            self.run(sql_users.format(t), lambda res: {"self": self.stats} )
            self.outxml.endElement("stat_users")

    def stats(self, res):
        self.outxml.startElement("user", {"user_id":str(res[1]), "user_name":str(res[2])})
        self.outxml.Element("count", {"value":str(res[0])})
        self.outxml.Element("timestamp", {"min":str(res[3]), "max":str(res[4])})
        self.outxml.endElement("user")


if __name__=="__main__":
  country = "france_limousin"
  class config:
    db_string = "dbname=osmose"
    dst = country + ".xml"
    db_schema = country

  from modules import OsmoseLog
  a = OsmoseLog.logger()
  Analyser_Osmosis_Stats(config, a).analyser()
