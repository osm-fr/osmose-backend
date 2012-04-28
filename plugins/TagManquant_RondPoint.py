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

from plugins.Plugin import Plugin


class TagManquant_RondPoint(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[102] = { "item": 3010, "level": 1, "tag": ["highway", "roundabout"], "desc": {"en": u"Tag highway missing on junction=roundabout", "fr": u"Tag highway manquant sur junction=roundabout"} }

    def way(self, data, tags, nds):
        if u"junction" not in tags:
            return

        if u"highway" not in tags:
            return [(102, 0, {})]
