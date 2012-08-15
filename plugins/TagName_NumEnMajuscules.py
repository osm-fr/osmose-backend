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


class TagName_NumEnMajuscules(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[905] = { "item": 5010, "level": 1, "tag": ["name"], "desc": {"en": u"Uppercase number", "fr": u"Numéro en majuscules"} }

        import re
        self.ReNEnMajuscule  = re.compile(u"^(|.* )N(°[0-9]+)(| .*)$")

    def node(self, data, tags):
        if "name" in tags:
            name = tags[u"name"]
            r = self.ReNEnMajuscule.match(name)
            if r:
                return [(905, 0, {"fix":{"name":"%sn%s%s" % (r.group(1), r.group(2), r.group(3))}})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
