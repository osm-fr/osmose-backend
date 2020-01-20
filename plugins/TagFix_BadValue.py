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
from modules.Stablehash import stablehash64

class TagFix_BadValue(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3040] = self.def_class(item = 3040, level = 1, tags = ['value', 'fix:chair'],
            title = T_('Bad tag value'))

        import re
        self.Values_open = re.compile("^[a-z0-9_]+( *; *[a-z0-9_]+)*$")
        self.check_list_open = set( (
            'abutters', 'access', 'admin_level', 'aerialway', 'aeroway', 'amenity',
            'barrier', 'bicycle', 'boat', 'border_type', 'boundary', 'bridge', 'building', 'construction',
            'covered', 'craft', 'crossing', 'cutting',
            'disused', 'drive_in', 'drive_through',
            'electrified', 'embankment', 'emergency',
            'fenced', 'foot', 'ford',
            'geological', 'goods',
            'hgv', 'highway', 'historic',
            'internet_access',
            'landuse', 'lanes', 'leisure',
            'man_made', 'military', 'mooring', 'motorboat', 'mountain_pass', 'natural', 'noexit',
            'office',
            'power', 'public_transport',
            'railway', 'route',
            'sac_scale', 'service', 'shop', 'smoothness', 'sport', 'surface',
            'tactile_paving', 'toll', 'tourism', 'tracktype', 'traffic_calming', 'trail_visibility',
            'tunnel',
            'usage',
            'vehicle',
            'wall', 'waterway', 'wheelchair', 'wood'
            ) )
        self.check_list_open_node = self.check_list_open
        self.check_list_open_way = self.check_list_open
        self.check_list_open_relation = self.check_list_open.copy()
        self.check_list_open_relation.add('type')
        self.exceptions_open = { "type": ( "associatedStreet",
                                           "turnlanes:lengths",
                                           "turnlanes:turns",
                                           "restriction:hgv", "restriction:caravan", "restriction:motorcar", "restriction:bus", "restriction:agricultural", "restriction:bicycle", "restriction:hazmat",
                                           "TMC" ),
                                 "service": ( "drive-through", ),
                                 "aerialway": ( "j-bar", "t-bar", ),
                                 "surface": ( "concrete:plates", "concrete:lanes",
                                            "paving_stones:20", "paving_stones:30", "paving_stones:50",
                                            "cobblestone:10", "cobblestone:20", "cobblestone:flattened"),
                                 "shop": ( "e-cigarette" ),
                                 "barrier": ( "full-height_turnstile" ),
                                 "man_made": ( "MDF" ),
                                }
        self.check_list_closed = set( (
            'area',
            'narrow',
            'oneway',
            ) )
        self.allow_closed = { "area": ( "yes", "no", ),
                            "narrow": ( "yes", "no", ),
                            "oneway": ( "yes", "no", "1", "-1", "reversible", "alternating"),
                          }

    def check(self, data, tags, check_list_open):
        err = []
        keyss = tags.keys()

        keys = set(keyss) & check_list_open
        for k in keys:
            if not self.Values_open.match(tags[k]):
                if k in self.exceptions_open:
                    if tags[k] in self.exceptions_open[k]:
                        # no error if in exception list
                        continue
                err.append({"class": 3040, "subclass": stablehash64(k), "text": T_("Bad tag value: \"%(key)s=%(val)s\"", {"key": k, "val": tags[k]})})

        keys = set(keyss) & self.check_list_closed
        for k in keys:
            if tags[k] not in self.allow_closed[k]:
                err.append({"class": 3040, "subclass": stablehash64(k), "text": T_("Bad tag value: \"%(key)s=%(val)s\"", {"key": k, "val": tags[k]})})

        return err

    def node(self, data, tags):
        return self.check(data, tags, self.check_list_open_node)

    def way(self, data, tags, nds):
        return self.check(data, tags, self.check_list_open_way)

    def relation(self, data, tags, members):
        return self.check(data, tags, self.check_list_open_relation)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_BadValue(None)
        a.init(None)
        for t in [{"access": "vor/dme"},
                  {"barrier": "AEGTO"},
                  {"barrier": "yes; AEGTO"},
                  {"aerialway": "ta-bar"},
                  {"tunnel": "-1st"},
                  {"area": "a"},
                  {"oneway": "yes;yes"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)
            self.check_err(a.relation(None, {"type": "vor/dme"}, None))
        for t in [{"type": "vor/dme"},
                 ]:
            self.check_err(a.relation(None, t, None), t)

        for t in [{"type": "vor"},
                  {"barrier": "yes"},
                  {"area": "yes"},
                  {"aerialway": "t-bar"},
                  {"oneway": "yes"},
                 ]:
            assert not a.node(None, t), t
            assert not a.way(None, t, None), t
            assert not a.relation(None, t, None), t

        for t in [{"type": "vor/dme"},
                  {"type": "associatedStreet"},
                 ]:
            assert not a.node(None, t), t
            assert not a.way(None, t, None), t
        for t in [{"type": "associatedStreet"},
                 ]:
            assert not a.relation(None, t, None), t
