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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
import re


class Source_FR(Plugin):

    only_for = ["FR"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.IGN = re.compile(r'.*(\wign)|(ign\w).*')

    def check(self, tags):
        if "AAAA" in tags["source"]:
            return {"class": 706, "subclass": 0, "text": T_("Source tag contains AAAA")}
        if "Cartographes Associés" in tags["source"]:
            return {"class": 706, "subclass": 1, "text": {"en":"Cartographes Associés"}}
        source = tags["source"].lower()
        if "geoportail" in source or "géoportail" in source:
            return {"class": 706, "subclass": 3, "text": {"en":"Géoportail"}}
        if "camptocamp" in source:
            return {"class": 706, "subclass": 5, "text": {"en":"CampToCamp"}}

    def node(self, data, tags):
        if "source" not in tags:
            return
        return self.check(tags)

    def way(self, data, tags, nds):
        if "source" not in tags:
            if tags.get("boundary", None) == "administrative":
                return {"class": 707, "subclass": 0}
            return
        return self.check(tags)

    def relation(self, data, tags, members):
        if "source" not in tags:
            return
        return self.check(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Source_FR(None)
        a.init(None)
        for d in [{"highway":"residential"},
                  {"source":"ignoville"},
                  {"source":"BDOrtho IGN"},
                  {"source":"road sign"},
                 ]:
            assert not a.node(None, d), d
            assert not a.way(None, d, None), d
            assert not a.relation(None, d, None), d

        for d in [{"boundary":"administrative"},
                 ]:
            assert not a.node(None, d), d
            assert not a.relation(None, d, None), d


        for d in [{"source": "  AAAA   "},
                  {"source": "Cartographes Associés"},
                  {"source": "geoportail"},
                  {"source": "camptocamp"},
                 ]:
            self.check_err(a.node(None, d), d)
            self.check_err(a.way(None, d, None), d)
            self.check_err(a.relation(None, d, None), d)

        for d in [{"boundary":"administrative"},
                 ]:
            self.check_err(a.way(None, d, None), d)
