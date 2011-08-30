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

class plugin:

    err_3040    = 3040
    err_3040_fr = u"Mauvaise valeur pour un tag"
    err_3040_en = u"Bad value in a tag"

    def init(self, logger):
        import re
        self.Values = re.compile("^[a-z0-9_]+( *; *[a-z0-9_]+)*$")
        self.check_list = set( (
            'abutters', 'access', 'admin_level', 'aerialway', 'aeroway', 'amenity', 'area',
            'barrier', 'bicycle', 'boat', 'border_type', 'boundary', 'bridge', 'building', 'construction',
            'covered', 'craft', 'crossing', 'cutting',
            'disused', 'drive_in', 'drive_through',
            'electrified', 'embankment', 'emergency',
            'fenced', 'foot', 'ford',
            'geological', 'goods',
            'hgv', 'highway', 'historic',
            'internet_access',
            'landuse', 'lanes', 'leisure',
            'man_made', 'military', 'mooring', 'motorboat', 'mountain_pass', 'narrow', 'natural', 'noexit',
            'office', 'oneway',
            'power', 'public_transport',
            'railway', 'route',
            'sac_scale', 'service', 'shop', 'smoothness', 'sport', 'surface',
            'tactile_paving', 'toll', 'tourism', 'tracktype', 'traffic_calming', 'traffic_sign', 'trail_visibility',
            'tunnel', 'type',
            'usage',
            'vehicle',
            'wall', 'waterway', 'wheelchair', 'wood'
            ) )
        self.exceptions = { "type": ( "associatedStreet", ),
                          }

    def node(self, data, tags):
        err = []
        keys = tags.keys()
        keys = set(keys) & self.check_list
        for k in keys:
            if not self.Values.match(tags[k]):
                if k in self.exceptions:
                    if tags[k] in self.exceptions[k]:
                        # no error if in exception list
                        return err

                err.append((3040, 0, {"fr": "Mauvaise valeur pour %s=%s" % (k, tags[k]), "en": "Bad value for %s=%s" % (k, tags[k])}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags):
        return self.node(data, tags)
