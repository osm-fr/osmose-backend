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


class Structural_Useless_Relation(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[12001] = { "item": 1200, "level": 2, "tag": ["relation", "fix:chair"], "desc": {"en": u"1-member relation", "fr": u"Relation à un seul membre"} }

    def relation(self, data, tags, members):
        if len(members) == 1 and not ("site" in tags and tags["site"] == "geodesic") and not ("type" in tags and tags["type"] == "defaults"):
            return [(12001, 1, {})]
