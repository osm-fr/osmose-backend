#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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

class Structurel_Euskal_Baserri(Plugin):

    only_for = ["FR_aquitaine"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[1130] = { "item": 1130, "desc": {"eu": u"Euskal baserri"} }

    def way(self, data, tags, nds):
        if "name" not in tags or "landuse" not in tags or tags["landuse"] != "farm":
            return

        if nds[0] != nds[-1] or len(nds) != 4:
            return

        return [(1130, 0, {})]
