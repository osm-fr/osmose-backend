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


class TagACorriger_Wikipedia(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3031] = { "item": 3031, "desc": {"en": u"Wikipedia"} }

        import re
        self.Wiki = re.compile(u"http://([^\.]+)\.wikipedia.+/(.+)")

    def node(self, data, tags):
        if "wikipedia" in tags:
            if tags["wikipedia"].startswith("http://"):
                m = self.Wiki.match(tags["wikipedia"])
                if m:
                    return [(3031, 1, {"en": u"wikipedia=%s => wikipedia=%s:%s" % (tags["wikipedia"], m.group(1), urllib.unquote(m.group(2)).replace("_"," "))})]
                else:
                    return [(3031, 0, {"en": u"Not a wikipedia URL"})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
