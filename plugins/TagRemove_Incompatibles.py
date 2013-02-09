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

class TagRemove_Incompatibles(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[900] = { "item": 4030, "level": 1, "tag": ["tag"], "desc": {"en": u"Tag conflict", "fr": u"Tag en conflit"} }
        self.CONFLICT = {}
        self.CONFLICT[0] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'leisure', 'railway', 'waterway', 'landuse'])
        self.CONFLICT[1] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'leisure', 'railway', 'natural'])
        self.CONFLICT[2] = set(['aerialway', 'aeroway', 'amenity', 'highway', 'leisure', 'railway', 'waterway', 'place'])

    def node(self, data, tags):
        if 'railway' in tags and tags['railway'] in ('abandoned', 'tram'):
            del tags['railway']
        if ('railway' in tags and tags['railway'] == 'tram_stop' and
            'highway' in tags and tags['highway'] == 'bus_stop'):
            del tags['railway']
            del tags['highway']
        for i in range(0, len(self.CONFLICT)):
            conflict = set(tags).intersection(self.CONFLICT[i])
            if len(conflict) > 1:
                return [(900, 1, {"fr": "Conflit entre les tags %s" % (", ".join(conflict)), "en": "Conflict between tags %s" % (", ".join(conflict))})]

        if 'bridge' in tags and 'tunnel' in tags and tags['bridge'] == 'yes' and tags['tunnel'] == 'yes':
            return [(900, 2, {"fr": "Conflit entre les tags bridge et tunnel", "en": "Conflict between tags bridge and tunnel"})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
