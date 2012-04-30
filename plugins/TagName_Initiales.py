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


class TagName_Initiales(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[902] = { "item": 5010, "desc": {"en": u"Initial stuck to the name", "fr": u"Initiale collée au nom"} }

        import re
        self.ReInitColleNom  = re.compile(u"^(.*[A-Z]\.)([A-Z][a-z].*)$")

    def way(self, data, tags, nds):
        if "name" in tags:
            name = tags[u"name"]
            r = self.ReInitColleNom.match(name)
            if r: # and not u"E.Leclerc" in self._DataTags[u"name"]:
                return [(902, 0, {"fix":{"name": "%s %s" % (r.group(1), r.group(2))}})]
