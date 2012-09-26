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


class ODbL_migration(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[1] = { "item": 7060, "level": 2, "tag": ["source"], "desc": {"en": u"ODbL migration damage", "fr": u"Dommage de la migration ODbL"} }

    def node(self, data, tags):
        if ("user" in data and data['user'] == 'OSMF Redaction Account' or
            "uid" in data and data['uid'] == 722137):
            if not ("name" in tags and "place" in tags and "ref:INSEE" in tags): # skip place node
                return [(1, 1, {})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
