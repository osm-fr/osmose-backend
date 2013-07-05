#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2012                                      ##
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

from plugins.Plugin import Plugin
import os
import sqlite3
import sys

sql01 = """
CREATE TABLE temp.count AS
SELECT
    key,
    SUM(count_nodes) AS count_nodes,
    SUM(count_ways) AS count_ways,
    SUM(count_relations) AS count_relations
FROM
    tags
GROUP BY
    key
;
"""

sql02 = """
SELECT
    keypairs.key2 AS key,
    keypairs.key1 AS other_key,
    CAST(keypairs.count_%(type)s AS REAL) / count.count_%(type)s AS together_faction,
    CAST(keypairs.count_%(type)s AS REAL) / keys.count_%(type)s AS from_fraction
FROM
    keypairs
    JOIN keys ON
        keypairs.key1 = keys.key AND
        keys.count_%(type)s > 100
    JOIN temp.count ON
        keypairs.key2 = count.key AND
        together_faction > 0.1
WHERE
    keypairs.count_%(type)s > 100 AND
    from_fraction > .9 AND
    from_fraction < 1.0
UNION
SELECT
    keypairs.key1 AS key,
    keypairs.key2 AS other_key,
    CAST(keypairs.count_%(type)s AS REAL) / count.count_%(type)s AS together_faction,
    CAST(keypairs.count_%(type)s AS REAL) / keys.count_%(type)s AS from_fraction
FROM
    keypairs
    JOIN keys ON
        keypairs.key2 = keys.key AND
        keys.count_%(type)s > 100
    JOIN temp.count ON
        keypairs.key1 = count.key AND
        together_faction > 0.1
WHERE
    keypairs.count_%(type)s > 100 AND
    from_fraction > .9 AND
    from_fraction < 1.0
;
"""

class TagMissing_LookLike(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[2070] = {"item": 2070, "level": 2, "tag": ["tag", "fix:chair"], "desc": T_(u"Missing tag by cooccurrence") }

        if not os.path.exists('taginfo-db.db'):
            self.info = {}
            for type in ['nodes', 'ways', 'relations']:
                self.info[type] = {}
            return

        # Taginfo wiki extract database
        # http://taginfo.openstreetmap.org/download/taginfo-db.db.bz2
        con = sqlite3.connect('taginfo-db.db')

        with con:
            cur = con.cursor()
            cur.execute(sql01)
            self.info = {}
            for type in ['nodes', 'ways', 'relations']:
                cur.execute(sql02 % {'type':'nodes'})
                rows = cur.fetchall()
                info = {}
                for row in rows:
                    if info.has_key(row[1]):
                        info[row[1]].append(row)
                    else:
                         info[row[1]] = [row]
                self.info[type] = info

    def check(self, type, tags):
        ret = []
        for tag in tags:
            if tag in self.info[type]:
                for mwm in self.info[type][tag]:
                    print mwm
                    if mwm[0] not in tags:
                        arg = (mwm[0], round(mwm[3],2))
                        ret.append((2070, int((1-mwm[3])*100), {"fr": u"Le tag \"%s\" semble manquant (proba=%s)" % arg, "en": u"Tag \"%s\" may be missing (proba=%s)" % arg}))
        return ret

    def node(self, data, tags):
        return self.check('nodes', tags);

    def way(self, data, tags, nds):
        return self.check('ways', tags);

    def relation(self, data, tags, members):
        return self.check('relations', tags);


if __name__ == "__main__":
    a = TagMissing_LookLike(None)
    a.init(None)
    r = a.node(None, {u"ref:INSEE":"33", u"place":"La-Haut-sur-la-Montagne"})
    print r
