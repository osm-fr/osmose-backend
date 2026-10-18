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

class OsmGis:

    def __init__(self, dbstring, prefix = "planet_osm", user_patch = True):

        self._PgConn     = psycopg2.connect(dbstring)
        self._PgCurs     = self._PgConn.cursor()
        self._prefix     = prefix
        self._user_patch = user_patch

    def __del__(self):
        self._PgConn.commit()

    # ---------------------------------------------------------------------
    # Node

    def NodeGet(self, NodeId):

        self._PgCurs.execute("SELECT lat, lon, tags FROM %s_nodes WHERE id = %d;" % (self._prefix, NodeId))
        r1 = self._PgCurs.fetchone()
        if not r1: return None

        data = {}
        data["id"]      = NodeId
        data["lat"]     = r1[0]
        data["lon"]     = r1[1]
        data["tag"]     = {}
        for i in range(len(r1[2])//2):
            data["tag"][r1[2][2*i].decode("utf8")] = r1[2][2*i+1].decode("utf8")

        if self._user_patch and "user" in data["tag"]:
            data["user"] = data["tag"].pop("user")

        return data

    # ---------------------------------------------------------------------
    # Way

    def WayGet(self, WayId, dump_sub_elements=False):

        self._PgCurs.execute("SELECT nodes, tags FROM %s_ways WHERE id = %d;" % (self._prefix, WayId))
        r1 = self._PgCurs.fetchone()
        if not r1: return None

        data = {}
        data["id"]      = WayId
        data["nd"]      = r1[0]
        data["tag"]     = {}
        for i in range(len(r1[1])//2):
            data["tag"][r1[1][2*i].decode("utf8")] = r1[1][2*i+1].decode("utf8")

        if self._user_patch and "user" in data["tag"]:
            data["user"] = data["tag"].pop("user")

        return data

    # ---------------------------------------------------------------------
    # Relation

    def RelationGet(self, RelationId, dump_sub_elements=False):

        self._PgCurs.execute("SELECT members, tags FROM %s_rels WHERE id = %d;" % (self._prefix, RelationId))
        r1 = self._PgCurs.fetchone()
        if not r1: return None

        data = {}
        data["id"]      = RelationId
        data["member"]  = []
        for i in range(len(r1[0])//2):
            data["member"].append({"type":{"n":"node","w":"way","r":"relation"}[r1[0][2*i][0]],"ref":int(r1[0][2*i][1:]),"role":r1[0][2*i+1].decode("utf8")})
        data["tag"]     = {}
        for i in range(len(r1[1])//2):
            data["tag"][r1[1][2*i].decode("utf8")] = r1[1][2*i+1].decode("utf8")

        if self._user_patch and "user" in data["tag"]:
            data["user"] = data["tag"].pop("user")

        return data
