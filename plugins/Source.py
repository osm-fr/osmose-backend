#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
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


class Source(Plugin):

    only_for = ["FR"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[706] = { "item": 3020, "desc": {"en": u"Illegal or uncomplete source tag", "fr": u"Tag source illegal ou incomplet"} }
        self.errors[707] = { "item": 2040, "desc": {"en": u"Missing tag source", "fr": u"Tag source manquant"} }

    def check(self, tags):
        if u"AAAA" in tags[u"source"]:
            return [(706,0,{"fr":u"Le tag source contient AAAA", "en":u"Source tag contains AAAA"})]
        if u"Cartographes Associés" in tags[u"source"]:
            return [(706,1,{"en":u"Cartographes Associés"})]
        if u"google" in tags[u"source"].lower():
            return [(706,2,{"en":u"Google"})]
        if u"geoportail" in tags[u"source"].lower() or u"géoportail" in tags[u"source"].lower():
            return [(706,3,{"en":u"Géoportail"})]
        if u"ign" in tags[u"source"].lower() and not u"geofla" in tags[u"source"].lower() and not u"cartographie réglementaire" in tags[u"source"].lower():
            return [(706,4,{"en":u"IGN"})]

    def node(self, data, tags):
        if u"source" not in tags:
            return
        return self.check(tags);

    def way(self, data, tags, nds):
        if u"source" not in tags:
            if tags.get(u"boundary", None) == u"administrative":
                return [(707,0,{})]
            return
        return self.check(tags);

    def relation(self, data, tags, members):
        if u"source" not in tags:
            return
        return self.check(tags);
