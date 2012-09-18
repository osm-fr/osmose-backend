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


class TagFix_MultipleTag(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30320] = { "item": 3032, "level": 1, "tag": ["tag", "highway"], "desc": {"en": u"Watch multiple tags"} }
        self.errors[20800] = { "item": 2080, "level": 1, "tag": ["tag", "highway", "roundabout"], "desc": {"en": u"Tag highway missing on junction=roundabout", "fr": u"Tag highway manquant sur junction=roundabout"} }
        self.errors[20801] = { "item": 2080, "level": 1, "tag": ["tag", "highway"], "desc": {"en": u"Tag highway missing on oneway", "fr": u"Tag highway manquant sur sens unique"} }

    def way(self, data, tags, nds):
        err = []
        if "highway" in tags and "fee" in tags:
            err.append((30320, 1000, {"fr": u"Use tags \"toll\" in place of \"fee\"", "fix": {"-": ["fee"], "+": {"toll": tags["fee"]}} }))

        if u"junction" in tags and u"highway" not in tags:
            err.append((20800, 0, {}))

        if u"oneway" in tags and not (u"highway" in tags or u"railway" in tags or u"aerialway" in tags or u"waterway" in tags):
            err.append((20801, 0, {}))

        return err
