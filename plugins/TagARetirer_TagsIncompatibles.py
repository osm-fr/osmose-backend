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


class TagARetirer_TagsIncompatibles(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[900] = { "item": 4030, "desc": {"en": u"Incompatible tags", "fr": u"Tags incompatibles"} }

    def way(self, data, tags, nds):
        if u"highway" in tags and u"landuse" in tags:
            return [(900, 0, {"en": u"highway=* + landuse=*"})]
