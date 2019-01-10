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

import psycopg2
import psycopg2.extensions
import psycopg2.extras
import time

###########################################################################
## Reader / Writer

class OsmOsis:

    def __init__(self, dbstring, schema_path=None):
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        retry = 10 * 60
        self._PgConn = None
        while not self._PgConn and retry > 0:
            try:
                self._PgConn = psycopg2.connect(dbstring)
            except psycopg2.OperationalError:
                retry = retry - 1
                if retry == 0:
                    raise
                else:
                    time.sleep(1)
        psycopg2.extras.register_hstore(self._PgConn, unicode=True)
        self._PgCurs = self._PgConn.cursor()
        if schema_path:
            self._PgCurs.execute("SET search_path TO %s,public;" % schema_path)

    def __del__(self):
        try:
            self.close()
        except (AttributeError, psycopg2.InterfaceError):
            # psycopg2.InterfaceError can happen if connection was already closed
            pass


    def conn(self):
        return self._PgConn


    def close(self):
        self._PgCurs.close()
        self._PgConn.close()


    def timestamp(self):
        self._PgCurs.execute('SELECT tstamp FROM metainfo')
        (timestamp,) = self._PgCurs.fetchone()
        return timestamp


    def NodeGet(self, NodeId):
        self._PgCurs.execute("SELECT nodes.id, st_y(nodes.geom), st_x(nodes.geom), nodes.version, users.name, nodes.tags FROM nodes LEFT JOIN users ON nodes.user_id = users.id WHERE nodes.id = %d;" % NodeId)
        r1 = self._PgCurs.fetchone()
        if not r1: return None
        return {
            u"id": r1[0],
            u"lat": float(r1[1]),
            u"lon": float(r1[2]),
            u"version": r1[3],
            u"user": r1[4] or "",
            u"tag": r1[5],
        }


    def WayGet(self, WayId, dump_sub_elements=False):
        self._PgCurs.execute("SELECT ways.id, ways.version, users.name, ways.tags, ways.nodes FROM ways LEFT JOIN users ON ways.user_id = users.id WHERE ways.id = %d;" % WayId)
        r1 = self._PgCurs.fetchone()
        if not r1: return None
        return {
            u"id": r1[0],
            u"version": r1[1],
            u"user": r1[2] or "",
            u"tag": r1[3],
            u"nd": r1[4] if dump_sub_elements else [],
        }


    def RelationGet(self, RelationId, dump_sub_elements=False):
        self._PgCurs.execute("SELECT relations.id, relations.version, users.name, relations.tags FROM relations LEFT JOIN users ON relations.user_id = users.id WHERE relations.id = %d;" % RelationId)
        r1 = self._PgCurs.fetchone()
        if not r1: return None
        data = {
            u"id": r1[0],
            u"version": r1[1],
            u"user": r1[2] or "",
            u"tag": r1[3],
            u"member": [],
        }

        if dump_sub_elements:
            self._PgCurs.execute("SELECT member_id, member_type, member_role FROM relation_members WHERE relation_id = %d ORDER BY sequence_id;" % RelationId)
            for r1 in self._PgCurs.fetchall():
                data[u"member"].append({u"ref":r1[0], u"type":{"N":"node","W":"way","R":"relation"}[r1[1]], u"role":r1[2]})

        return data


    def UserGet(self, UserId):
        self._PgCurs.execute("SELECT name FROM users WHERE id = %d;" % UserId)
        r1 = self._PgCurs.fetchone()
        if not r1: return None
        return r1[0]
