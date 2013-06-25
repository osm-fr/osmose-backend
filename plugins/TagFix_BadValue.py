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

class TagFix_BadValue(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3040] = { "item": 3040, "level": 1, "tag": ["value", "fix:chair"], "desc": {"en": u"Bad value in a tag", "fr": u"Mauvaise valeur pour un tag"} }

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
            'tunnel', 'type',
            'usage',
            'vehicle',
            'wall', 'waterway', 'wheelchair', 'wood'
            ) )
        self.exceptions_open = { "type": ( "associatedStreet",
                                           "turnlanes:lengths",
                                           "turnlanes:turns" ),
                                 "service": ( "drive-through", ),
                                 "aerialway": ( "j-bar", "t-bar", ),
                                 "surface": ( "concrete:plates", "concrete:lanes",
                                            "paving_stones:20", "paving_stones:30", "paving_stones:50",
                                            "cobblestone:10", "cobblestone:20", ),
                                }
        self.check_list_closed = set( (
            'area',
            'narrow',
            'oneway',
            ) )
        self.allow_closed = { "area": ( "yes", "no", ),
                            "narrow": ( "yes", "no", ),
                            "oneway": ( "yes", "no", "1", "-1", "reversible", ),
                          }

    def node(self, data, tags):
        err = []
        keyss = tags.keys()

        keys = set(keyss) & self.check_list_open
        for k in keys:
            if not self.Values_open.match(tags[k]):
                if k in self.exceptions_open:
                    if tags[k] in self.exceptions_open[k]:
                        # no error if in exception list
                        continue
                err.append((3040, 0, {"fr": "Mauvaise valeur pour %s=%s" % (k, tags[k]), "en": "Bad value for %s=%s" % (k, tags[k])}))

        keys = set(keyss) & self.check_list_closed
        for k in keys:
            if tags[k] not in self.allow_closed[k]:
                err.append((3040, 1, {"fr": "Mauvaise valeur pour %s=%s" % (k, tags[k]), "en": "Bad value for %s=%s" % (k, tags[k])}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
