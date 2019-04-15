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
from modules.downloader import update_cache
import os
import sqlite3

sql01 = """
CREATE TEMP TABLE temp.count AS
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
    k.key2 AS key,
    k.key1 AS other_key,
    CAST(k.count_%(type)s AS REAL) / count.count_%(type)s AS together_faction,
    CAST(k.count_%(type)s AS REAL) / keys.count_%(type)s AS from_fraction
FROM
    key_combinations k
    JOIN keys ON
        k.key1 = keys.key AND
        keys.count_%(type)s > 100
    JOIN temp.count ON
        k.key2 = count.key AND
        together_faction > 0.1
WHERE
    k.count_%(type)s > 100 AND
    from_fraction > .9 AND
    from_fraction < 1.0
UNION
SELECT
    k.key1 AS key,
    k.key2 AS other_key,
    CAST(k.count_%(type)s AS REAL) / count.count_%(type)s AS together_faction,
    CAST(k.count_%(type)s AS REAL) / keys.count_%(type)s AS from_fraction
FROM
    key_combinations k
    JOIN keys ON
        k.key2 = keys.key AND
        keys.count_%(type)s > 100
    JOIN temp.count ON
        k.key1 = count.key AND
        together_faction > 0.1
WHERE
    k.count_%(type)s > 100 AND
    from_fraction > .9 AND
    from_fraction < 1.0
;
"""

class TagMissing_LookLike(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[2070] = {"item": 2070, "level": 2, "tag": ["tag", "fix:chair"], "desc": T_(u"Missing tag by cooccurrence") }

        bdd = update_cache(u"http://taginfo.openstreetmap.org/download/taginfo-db.db.bz2", 30, bz2_decompress=True)

        if not os.path.exists(bdd):
            self.info = {}
            for type in ['nodes', 'ways', 'relations']:
                self.info[type] = {}
            return

        # Taginfo wiki extract database
        con = sqlite3.connect(bdd)

        with con:
            cur = con.cursor()
            cur.execute(sql01)
            self.info = {}
            for type in ['nodes', 'ways', 'relations']:
                cur.execute(sql02 % {'type':'nodes'})
                rows = cur.fetchall()
                info = {}
                for row in rows:
                    if row[1] in info:
                        info[row[1]].append(row)
                    else:
                        info[row[1]] = [row]
                self.info[type] = info

    def check(self, type, tags):
        ret = []
        for tag in tags:
            if tag in self.info[type]:
                for mwm in self.info[type][tag]:
                    if mwm[0] not in tags:
                        arg = (mwm[0], round(mwm[3],2))
                        ret.append((2070, int((1-mwm[3])*100), {"fr": u"Le tag \"%s\" semble manquant (proba=%s)" % arg, "en": u"Tag \"%s\" may be missing (proba=%s)" % arg}))
        return ret

    def node(self, data, tags):
        return self.check('nodes', tags)

    def way(self, data, tags, nds):
        return self.check('ways', tags)

    def relation(self, data, tags, members):
        return self.check('relations', tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagMissing_LookLike(None)
        a.init(None)
        self.check_err(a.node(None, {u"ref:INSEE":"33"}))
        self.check_err(a.node(None, {u"ref:INSEE":"33", u"population":100}))
        self.check_err(a.node(None, {u"ref:INSEE":"33", u"population":100, u"place":"Ici"}))
        assert not a.node(None, {u"ref:INSEE":"33", u"population":100, u"place":"Ici", u"name": u"Toto"})
        self.check_err(a.node(None, {u"place":"La-Haut-sur-la-Montagne"}))
        assert not a.node(None, {u"place":"La-Haut-sur-la-Montagne", u"name":"Toto"})
