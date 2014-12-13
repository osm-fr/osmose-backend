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
import re


class P_Name_PoorlyWrittenWayType(Plugin):

    def generator(self, p):
        (p1, p2) = p.split("|")
        r = u"^(("
        r += p1[0]  # keep first lever in uppercase
        for c in p1[1:]:
            r += u"[%s%s]" % (c.lower(), c.upper())
        r += u")(\.|"
        for c in p2:
            r += u"[%s%s]" % (c.lower(), c.upper())
        r += u")?) .*$"
        return re.compile(r)

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[702] = { "item": 5020, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Badly written way type") }

    def node(self, data, tags):
        if u"name" not in tags:
            return
        name = tags["name"]
        for test in self.ReTests:
            if not name.startswith("%s " % test[0][1]):
                r = test[1].match(name)
                if r:
                    return [(702, test[0][0], {"fix": {"name": name.replace(r.group(1), test[0][1])} })]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


available_plugin_classes = []
