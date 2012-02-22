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
import urllib


class Name_Saint(Plugin):

    only_for = ["FR"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3033] = { "item": 3033, "desc": {"fr": u"Saint"} }

        import re
        self.Saint = re.compile(u".*Sainte? +.+")

    def node(self, data, tags):
        if "name" in tags and tags["name"] != "Saint Algue" and self.Saint.match(tags["name"]):
                return [(3033, 1, {"fr": u"Trait d'union après \"Saint(e)\" : %s" % (tags["name"]), "en": u"Missing hyphen after \"Saint(e)\": %s" % (tags["name"])})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
