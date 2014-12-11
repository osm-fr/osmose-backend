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


class P_Name_MisspelledWordByRegex(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[701] = { "item": 5010, "level": 1, "tag": ["name", "fix:chair"], "desc": T_(u"Badly written word") }

    def node(self, data, tags):
        if u"name" not in tags:
            return
        name = tags["name"]
        for test in self.ReTests:
            if not name.startswith(test[0][1]):
                r = test[1].match(name)
                if r:
                    add_str = r.group(2) if r.group(2) else u""
                    return [(701, test[0][0], {"fix": {"name": test[0][1] + add_str} })]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
