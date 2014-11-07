#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

class TagFix_BadKey(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3050] = { "item": 3050, "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Bad tag") }

        import re
        self.KeyPart1 = re.compile("^[a-zA-Z_0-9]+$")
        self.KeyPart2 = re.compile("^[-_:a-zA-Z_0-9<>°]+$")
        self.exceptions = set( ("ISO3166-1", "iso3166-1", "ISO3166-2", "iso3166-2",
                                "ISO3166-1:alpha2",
                                "ISO3166-1:alpha3",
                                "ISO3166-1:numeric",
                                "USGS-LULC",
                                "aims-id",
                                "au.gov.abs",
                                "catmp-RoadID",
                                "dc-gis",
                                "drive-through",
                                "e-road",
                                "nhd-shp",
                                "voltage-high", "voltage-low",
                             ) )

    def node(self, data, tags):
        err = []
        keys = tags.keys()
        for k in keys:
            if ":(" in k or k.startswith("def:") or k in self.exceptions:
                # acess:([date])
                # key def: can contains sign =
                continue

            part = k.split(':', 1)
            if not self.KeyPart1.match(part[0]):
                err.append((3050, 0, T_("Bad tag %(k)s=%(v)s", {"k":k, "v":tags[k]})))
            elif len(part) == 2 and not self.KeyPart2.match(part[1]):
                err.append((3050, 1, T_("Bad tag %(k)s=%(v)s", {"k":k, "v":tags[k]})))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_BadKey(None)
        a.init(None)
        for k in ["toto", "def9", "disused:amenity", "access:([date])", "def:a=b",
                  "ISO3166-1", "ISO3166-1:alpha2"]:
            assert not a.node(None, {k: 1}), ("key='%s'" % k)
            assert not a.way(None, {k: 1}, None), ("key='%s'" % k)
            assert not a.relation(None, {k: 1}, None), ("key='%s'" % k)

        for k in ["a-b", "a''b", u"é", u"û", "a=b", u"a:é", "a:a:'"]:
            self.check_err(a.node(None, {k: 1}), ("key='%s'" % k))

