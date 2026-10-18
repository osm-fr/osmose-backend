###########################################################################
##                                                                       ##
## Copyright Osmose Contributors 2026                                    ##
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
from modules.Stablehash import stablehash
from plugins.Plugin import Plugin


class Highway_Traffic_Calming(Plugin):

    traffic_flow_highways = (
        "motorway",
        "trunk",
        "primary",
        "secondary",
        "tertiary",
        "unclassified",
        "residential",
        "living_street",
        "service",
        "pedestrian",
        "track",
        "busway",
        "road",
        "cycleway",
        "path",
        "bridleway",
        "motorway_link",
        "trunk_link",
        "primary_link",
        "secondary_link",
        "tertiary_link",
    )

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30411] = self.def_class(item = 3040, level = 3, tags = ['tag', 'highway', 'fix:survey'],
            title = T_('Misplaced traffic calming tag'),
            detail = T_(
'''A way that does not carry through traffic (such as a crossing, footway,
or area) has the `traffic_calming=*` tag. This tag should only appear on
highways that carry the traffic being calmed, such as roads and
cycleways.'''),
            fix = T_(
'''Move `traffic_calming=*` to the road, cycleway, path, or other highway where
traffic is slowed, or to a node on that highway.

If the tag was added here by mistake and there is no traffic
calming feature to map elsewhere, remove `traffic_calming=*` from this way.'''),
            trap = T_(
'''Do not remove the tag without checking whether a traffic calming feature still
needs to be moved to the highway whose traffic is calmed.'''))

    def way(self, data, tags, nds):
        if 'traffic_calming' not in tags:
            return []

        highway = tags.get('highway')
        if highway in ("construction", "proposed"):
            highway = tags.get(highway)

        if highway in self.traffic_flow_highways and tags.get('area') != 'yes' and tags.get(highway) != 'crossing':
            return []

        return [{
            'class': 30411,
            'subclass': stablehash(tags['traffic_calming']),
            'text': T_("misplaced traffic_calming={0}", tags['traffic_calming'])
        }]


###########################################################################
from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        a = Highway_Traffic_Calming(None)
        self.set_default_config(a)
        a.init(None)

        for crossing_key in ("footway", "cycleway", "path"):
            tags = {crossing_key: "crossing", "traffic_calming": "table"}
            self.check_err(a.way(None, tags, None), tags, expected={"class": 30411})

        self.check_err(a.way(None, {"highway": "footway", "footway": "traffic_island", "traffic_calming": "island"}, None), expected={"class": 30411})
        self.check_err(a.way(None, {"area:highway": "traffic_island", "traffic_calming": "island"}, None), expected={"class": 30411})
        self.check_err(a.way(None, {"area": "yes", "traffic_calming": "island"}, None), expected={"class": 30411})
        self.check_err(a.way(None, {"highway": "footway", "footway": "sidewalk", "traffic_calming": "table"}, None), expected={"class": 30411})
        self.check_err(a.way(None, {"highway": "footway", "traffic_calming": "table"}, None), expected={"class": 30411})
        self.check_err(a.way(None, {"traffic_calming": "table"}, None), expected={"class": 30411})

        self.check_not_err(a.way(None, {"highway": "residential", "traffic_calming": "hump"}, None))
        self.check_not_err(a.way(None, {"highway": "service", "traffic_calming": "chicane"}, None))
        self.check_not_err(a.way(None, {"highway": "pedestrian", "traffic_calming": "table"}, None))
        self.check_not_err(a.way(None, {"highway": "cycleway", "traffic_calming": "table"}, None))
        self.check_not_err(a.way(None, {"highway": "path", "traffic_calming": "bump"}, None))
        self.check_not_err(a.way(None, {"highway": "construction", "construction": "residential", "traffic_calming": "table"}, None))
        self.check_not_err(a.way(None, {"highway": "proposed", "proposed": "cycleway", "traffic_calming": "hump"}, None))
        self.check_not_err(a.way(None, {"highway": "footway", "footway": "crossing", "crossing": "uncontrolled"}, None))
        self.check_not_err(a.way(None, {"highway": "cycleway", "cycleway": "crossing", "crossing": "uncontrolled"}, None))
