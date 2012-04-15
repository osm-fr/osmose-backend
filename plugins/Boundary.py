#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

class Boundary(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[6070] = { "item": 6070, "desc": {"en": u"Relation de type boundary", "fr": u"Boundary relation"} }

    def relation(self, data, tags, members):
        if not "type" in tags or not tags["type"] == "boundary":
            return

        ret = []
        admin_centre = False
        for member in members:
            admin_centre |= (member["role"] == "admin_centre")
            if member["type"] == "node" and member["role"] not in ["admin_centre", "label"]:
                ret.append((6070, 1, {"fr": u"Nœud %d inadapté dans la relation" % member["ref"], "en": u"Bad node %d into relation" % member["ref"]}))

        if admin_centre:
            ret.append((6070, 2, {"fr": u"Relation boundary sans rôle admin_centre", "en": u"Boundary relation without admin_centre role"}))
