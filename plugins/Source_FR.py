#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
## Copyrights Frédéric Rodrigo 2011-2014                                 ##
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


class Source_FR(Plugin):

    only_for = ["FR"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.IGN = re.compile(".*(\wign)|(ign\w).*")

    def check(self, tags):
        if u"AAAA" in tags[u"source"]:
            return {"class": 706, "subclass": 0, "text": T_(u"Source tag contains AAAA")}
        if u"Cartographes Associés" in tags[u"source"]:
            return {"class": 706, "subclass": 1, "text": {"en":u"Cartographes Associés"}}
        source = tags[u"source"].lower()
        if u"geoportail" in source or u"géoportail" in source:
            return {"class": 706, "subclass": 3, "text": {"en":u"Géoportail"}}
        if u"ign" in source and not u"geofla" in source and not u"cartographie réglementaire" in source and not u"géodési" in source and not u"500" in source and not u"CRAIG/IGN" in source and not u"rtho" in source and not u'craig' in source:
            if not self.IGN.match(source):
                return {"class": 706, "subclass": 4, "text": {"en":u"IGN"}}
        if u"camptocamp" in source:
            return {"class": 706, "subclass": 5, "text": {"en":u"CampToCamp"}}

    def node(self, data, tags):
        if u"source" not in tags:
            return
        return self.check(tags)

    def way(self, data, tags, nds):
        if u"source" not in tags:
            if tags.get(u"boundary", None) == u"administrative":
                return {"class": 707, "subclass": 0}
            return
        return self.check(tags)

    def relation(self, data, tags, members):
        if u"source" not in tags:
            return
        return self.check(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Source_FR(None)
        a.init(None)
        for d in [{u"highway":u"residential"},
                  {u"source":u"nign"},
                  {u"source":u"ignoville"},
                  {u"source":u"IGN géodésique"},
                  {u"source":u"BDOrtho IGN"},
                  {u"source":u"road sign"},
                 ]:
            assert not a.node(None, d), d
            assert not a.way(None, d, None), d
            assert not a.relation(None, d, None), d

        for d in [{u"boundary":u"administrative"},
                 ]:
            assert not a.node(None, d), d
            assert not a.relation(None, d, None), d


        for d in [{u"source": u"IGN"},
                  {u"source": u"  AAAA   "},
                  {u"source": u"Cartographes Associés"},
                  {u"source": u"geoportail"},
                  {u"source": u"camptocamp"},
                 ]:
            self.check_err(a.node(None, d), d)
            self.check_err(a.way(None, d, None), d)
            self.check_err(a.relation(None, d, None), d)

        for d in [{u"boundary":u"administrative"},
                 ]:
            self.check_err(a.way(None, d, None), d)
