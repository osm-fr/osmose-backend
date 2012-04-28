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


class Name_TypeVoieMalEcrit(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[702] = { "item": 5020, "level": 2, "tag": ["name"], "desc": {"en": u"Badly written way type", "fr": u"Type de voie mal écrit"} }

        import re
        self.ReTests = {}
        # Captial at start already checked by Toponymie plugin
        self.ReTests[( 0, u"Allée")]     = re.compile(u"^([A][Ll][Ll]?[EÉée][Ee]?|[Aa][Ll][Ll]\.) .*$")
        self.ReTests[( 0, u"Allées")]    = re.compile(u"^([A][Ll][Ll]?[EÉée][Ee][sS]) .*$")
        self.ReTests[( 1, u"Boulevard")] = re.compile(u"^([B]([Oo][Uu][Ll][Ll]?[Ee]?)?[Vv]?([Aa][Rr])?[Dd]\.?) .*$")
        self.ReTests[( 2, u"Avenue")]    = re.compile(u"^([A][Vv][Ee][Nn][Uu][Ee]) .*$")
        self.ReTests[( 4, u"Chemin")]    = re.compile(u"^([C][Hh][Ee][Mm][Ii][Nn]) .*$")
        self.ReTests[( 5, u"Route")]     = re.compile(u"^([R][Oo][Uu][Tt][Ee]) .*$")
        self.ReTests[( 6, u"Esplanade")] = re.compile(u"^([EÉ][Ss][Pp][Ll][Aa][Nn][Aa][Dd][Ee]) .*$")
        self.ReTests[( 7, u"Rue")]       = re.compile(u"^([R][Uu][Ee]) .*$")
        self.ReTests = self.ReTests.items()

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


if __name__ == "__main__":
    a = Name_TypeVoieMalEcrit(None)
    a.init(None)
    for d in [u"Allée ", u"ALLÉE ", u"Allées fleuries", u"AllÉes grandioses", u"Boulevard ", u"BOUleVARD "]:
        print d, a.node(None, {"name": d})
