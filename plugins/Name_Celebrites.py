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


class Name_Celebrites(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[700] = { "item": 5010, "level": 2, "tag": ["name", "fix:chair"], "desc": {"en": u"Badly spelled celebrity name", "fr": u"Nom de célébrité erroné"} }

        import re
        self.ReTests = {}
        self.ReTests[( 1, u"Christophe Colomb")] = re.compile(u"(^| )[Ch][Hh]?[Rr][Ii][Ss][Tt][Oo]([Pp][Hh]|[Ff]+)[Ee]? [Cc][Oo][Ll][Ll]?[Oo][MmNn][BbDdTt]?( |$)")
        self.ReTests[( 2, u"Benoit"           )] = re.compile(u"(^| )(Paul|Pierre|Hubert|Chris|Michel|André) Benoît( |$)")
        self.ReTests = self.ReTests.items()

    def node(self, data, tags):
        if u"name" not in tags:
            return
        name = tags["name"]
        for test in self.ReTests:
            if test[1].match(name) and test[0][1] not in name:
                return [(700, test[0][0], {"en": test[0][1]})]

    def way(self, data, tags, nodes):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
