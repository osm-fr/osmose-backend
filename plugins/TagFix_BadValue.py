#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
## Copyrights Nico Rikken <nico@nicorikken.eu> 2021                      ##
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
from modules.Stablehash import stablehash64

class TagFix_BadValue(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3040] = self.def_class(item = 3040, level = 1, tags = ['value', 'fix:chair'],
            title = T_('Bad tag value'),
            detail = T_(
'''This feature is tagged with a value which does not match the typical format used for tags with distinct values
 (lowercase alphanumeric characters with no spaces). It's most likely not an expected tagging.'''),
            fix = T_('Check the value of the tag in question and update the tagging to reflect what this feature is.'),
            trap = T_(
'''It's possible a mapper was trying to map a feature with no existing agreed upon tagging.
However, this should probably still conform to the typical format used for values of the given tag.''')
        )
        self.errors[40613] = self.def_class(item = 4061, level = 3, tags = ['highway', 'fix:chair'],
        title = T_('Unspecific value'),
        detail = T_('''The value of the tag is very unspecific. Replace it by a meaningful value.'''))

        import re
        self.Values_open = re.compile("^[a-z0-9_]+( *; *[a-z0-9_]+)*$")
        self.check_list_open = set((
            'abutters', 'admin_level', 'aerialway', 'aeroway', 'amenity',
            'barrier', 'bench', 'bicycle_parking', 'bin', 'border_type', 'boundary', 'bridge', 'building', 'bus_bay',
            'cemetery', 'club', 'construction', 'covered', 'craft', 'crossing_ref', 'cuisine', 'cutting', 'cycleway',
            'disused', 'drive_in', 'drive_through',
            'electrified', 'embankment', 'emergency', 'entrance',
            'fenced', 'footway', 'ford',
            'geological', 'golf',
            'handrail', 'hazard', 'healthcare', 'highway', 'historic',
            'information', 'intermittent', 'internet_access',
            'junction',
            'kerb',
            'landuse', 'leaf_type', 'leaf_cycle', 'leisure', 'location',
            'material', 'man_made', 'meadow', 'military', 'mooring', 'mountain_pass',
            'natural', 'noexit',
            'office',
            'parking', 'place', 'power', 'public_transport',
            'railway', 'ramp', 'religion', 'route', 'route_master',
            'sac_scale', 'seasonal', 'service', 'shelter', 'shop', 'shoulder', 'sidewalk', 'smoothness', 'sport', 'surface',
            'tactile_paving', 'toll', 'tourism', 'traffic_calming', 'trail_visibility', 'traffic_signals', 'tunnel',
            'usage', 'utility',
            'wall', 'water', 'waterway', 'wetland', 'wheelchair', 'wood'
        ))
        self.check_list_open_node = self.check_list_open
        self.check_list_open_way = self.check_list_open
        self.check_list_open_relation = self.check_list_open.copy()
        self.check_list_open_relation.add('type')
        self.exceptions_open = { "type": ( "associatedStreet",
                                           "turnlanes:lengths",
                                           "turnlanes:turns",
                                           "TMC" ),
                                 "service": ( "drive-through", ),
                                 "aerialway": ( "j-bar", "t-bar", ),
                                 "surface": ( "concrete:plates", "concrete:lanes",
                                            "paving_stones:20", "paving_stones:30", "paving_stones:50",
                                            "cobblestone:10", "cobblestone:20", "cobblestone:flattened"),
                                 "shop": ( "e-cigarette" ),
                                 "sport": ( "five-a-side", "jiu-jitsu", "pesäpallo", "shot-put" ),
                                 "barrier": ( "full-height_turnstile" ),
                                 "parking": ( "multi-storey" ),
                                 "bicycle_parking": ( "two-tier" ),
                                 "electrified": ( "ground-level_power_supply" ),
                                 "religion": ( "self-realization_fellowship" ),
                                 "man_made": ( "MDF", "piste:halfpipe" ),
                                 "cuisine": ( "tex-mex" ),
                                }

        self.allow_closed = { "area": ( "yes", "no", ),
                            "backrest": ( "yes", "no", ),
                            "conveying": ( "yes", "forward", "backward", "no", "reversible", ),
                            "crossing": ( "traffic_signals", "uncontrolled", "unmarked", "no", "marked", "zebra", ),
                            "lane_markings": ( "yes", "no", ),
                            "narrow": ( "yes", "no", ),
                            "oneway": ( "yes", "no", "1", "-1", "reversible", "alternating"),
                            "segregated": ( "yes", "no", ),
                            "trolley_wire": ( "yes", "no", ),
                            "tracktype":  ( "grade1", "grade2", "grade3", "grade4", "grade5", ),
                          }
        self.check_list_closed = set(self.allow_closed.keys())

    def check(self, data, tags, check_list_open):
        err = []
        keyss = tags.keys()

        keys = set(keyss) & check_list_open
        for k in keys:
            if (not self.Values_open.match(tags[k]) and ( # value has a non-standard character
                not k in self.exceptions_open or # no exceptions exist for the key
                any(map(lambda val: val not in self.exceptions_open[k] and not self.Values_open.match(val), tags[k].split(";"))) # Check each value in a multiple-value key for not being whitelisted (or normal)
            )):
                err.append({"class": 3040, "subclass": stablehash64(k), "text": T_("Concerns tag: `{0}`", '='.join([k, tags[k]])) })

        keys = set(keyss) & self.check_list_closed
        for k in keys:
            if tags[k] not in self.allow_closed[k]:
                err.append({"class": 3040, "subclass": stablehash64(k), "text": T_("Concerns tag: `{0}`", '='.join([k, tags[k]])) })

        for k in keyss:
            if tags[k] == "unknown":
                err.append({"class": 40613, "subclass": stablehash64(k), "text": T_("Concerns tag: `{0}`", '='.join([k, tags[k]])) })

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
        for t in [{"barrier": "AEGTO"},
                  {"barrier": "yes; AEGTO"},
                  {"aerialway": "ta-bar"},
                  {"tunnel": "-1st"},
                  {"area": "a"},
                  {"oneway": "yes;yes"},
                  {"sport": "rugby-union;long_jump"}, # bad;good
                  {"sport": "rugby-union;shot-put;long_jump"}, # bad;whitelisted;good
                  {"sport": "rugby_union;shot-put;long-jump"}, # good;whitelisted;bad
                  {"access": "unknown"},
                  {"tracktype": "gradde1"},
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
                  {"sport": "athletics;jiu-jitsu;rugby_union;hockey;shot-put;long_jump"},
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

        # Assure keys are not present in both sets
        assert not a.check_list_open & a.check_list_closed
