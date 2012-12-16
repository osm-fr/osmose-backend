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


class Name_PoorlyWrittenWayType(Plugin):

    only_for = ["fr"]

    def generator(self, p):
        (p1, p2) = p.split("|")
        r = u"^(("
        for c in p1:
            r += u"[%s%s]" % (c.lower(), c.upper())
        r += u")(\.|"
        for c in p2:
            r += u"[%s%s]" % (c.lower(), c.upper())
        r += u")?) .*$"
        print r
        return re.compile(r)

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[702] = { "item": 5020, "level": 2, "tag": ["name"], "desc": {"en": u"Badly written way type", "fr": u"Type de voie mal écrit"} }

        self.ReTests = {}
        # Captial at start already checked by Toponymie plugin
        self.ReTests[( 0, u"Allée")]     = re.compile(u"^([A][Ll][Ll]?[EÉée][Ee]?|[Aa][Ll][Ll]\.) .*$")
        self.ReTests[( 0, u"Allées")]    = re.compile(u"^([A][Ll][Ll]?[EÉée][Ee]?[sS]) .*$")
        self.ReTests[( 1, u"Boulevard")] = re.compile(u"^([B]([Oo][Uu][Ll][Ll]?[Ee]?)?[Vv]?([Aa][Rr])?[Dd]\.?) .*$")
        self.ReTests[( 2, u"Avenue")]    = self.generator(u"Av|enue")
        self.ReTests[( 4, u"Chemin")]    = self.generator(u"Che|min")
        self.ReTests[( 5, u"Route")]     = re.compile(u"^([R]([Oo][Uu])?[Tt][Ee]?\.?) .*$")
        self.ReTests[( 6, u"Esplanade")] = re.compile(u"^([EÉ][Ss][Pp][Ll][Aa][Nn][Aa][Dd][Ee]) .*$")
        self.ReTests[( 7, u"Rue")]       = self.generator(u"R|ue")
        self.ReTests[( 8, u"Giratoire")] = re.compile(u"^([G][Ii][Rr][Aa][Tt][Oo][Ii][Rr][Ee]) .*$")
        self.ReTests[( 9, u"Rond-Point")]= re.compile(u"^([R][Oo][Nn][Dd]-[p][Oo][Ii][Nn][Tt]) .*$")
        self.ReTests[( 9, u"Rondpoint")] = re.compile(u"^([R][Oo][Nn][Dd][Pp][Oo][Ii][Nn][Tt]) .*$")
        self.ReTests[(10, u"Carrefour")] = re.compile(u"^([C][Aa][Rr][Rr][Ee][Ff][Oo][Uu][Rr]) .*$")
        self.ReTests[(11, u"Place")]     = self.generator(u"Pl|ace")
        self.ReTests[(12, u"Impasse")]   = self.generator(u"Imp|asse")
        self.ReTests[(13, u"Quai")]      = self.generator(u"Qu|ai")
        self.ReTests[(14, u"Square")]    = self.generator(u"Sq|uare")
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
    a = Name_PoorlyWrittenWayType(None)
    a.init(None)
    for d in [u"Allée ", u"ALLÉE ", u"Allées fleuries", u"AllÉes grandioses", u"Boulevard ", u"BOUleVARD ", "Av. ", "Av ", "Bvd. ", "Rte", "Rt. "]:
        print d, a.node(None, {"name": d})
