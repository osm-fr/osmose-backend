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

"""
DROP VIEW tags CASCADE;
CREATE TEMP VIEW tags AS
SELECT
    id,
    (each(tags)).key,
    (each(tags)).value
FROM
    nodes
;

SELECT
    DISTINCT(key, value)
FROM
    tags
WHERE
    NOT key LIKE '%source%' AND
    NOT key LIKE 'note%' AND
    NOT key LIKE '%ref%' AND
    NOT key LIKE '4C:%' AND
    NOT key LIKE 'CLC:%' AND
    NOT key LIKE 'seamark:%' AND
    key NOT IN (
    -- Accept multiple vaues
    'opening_hours', 'description', 'bus_routes', 'phone', 'created_by', 'comment', 'day_off', 'day_on', 'destination', 'fixme', 'FIXME', 'access', 'is_in', 'alt_name', 'boundary', 'fee', 'id', 'marked_trail', 'sport', 'shop', 'school:FR', 'hour_off', 'hour_on', 'old_name', 'operator', 'park_ride', 'antenna', 'brewery', 'collection_times', 'cuisine', 'exit_to', 'towards', 'traffic_sign', 'url',
    -- No multiple value
    'cycleway', 'highway', 'foot', 'layer', 'landuse', 'foot', 'building', 'left:city', 'left:country', 'left:departement', 'left:village', 'right:city', 'right:country', 'right:departement', 'right:village', 'name','maxspeed', 'lanes', 'oneway', 'service', 'admin_level', 'natural', 'smoothness', 'surface', 'tracktype', 'type', 'voltage', 'waterway', 'width', 'wikipedia', 'wires', 'wood', 'trail_visibility', 'bicycle', 'est_width', 'motorcar', 'motor_vehicle', 'mtb:scale', 'ele', 'level', 'material', 'power', 'railway', 'brand', 'addr:housenumber', 'addr:street', 'attraction', 'amenity', 'leisure' ) AND
    value LIKE '%;%'
;

"""
class plugin:

    err_3070    = 3070
    err_3070_fr = u"Valeurs multiples"
    err_3070_en = u"Multiple values"

    def init(self, logger):
        self.SimpleValuedTag = set(('cycleway', 'highway', 'foot', 'layer', 'landuse', 'foot', 'building', 'left:city', 'left:country', 'left:departement', 'left:village', 'right:city', 'right:country', 'right:departement', 'right:village', 'name','maxspeed', 'lanes', 'oneway', 'service', 'admin_level', 'natural', 'smoothness', 'surface', 'tracktype', 'type', 'voltage', 'waterway', 'width', 'wikipedia', 'wires', 'wood', 'trail_visibility', 'bicycle', 'est_width', 'motorcar', 'motor_vehicle', 'mtb:scale', 'ele', 'level', 'material', 'power', 'railway', 'brand', 'addr:housenumber', 'addr:street', 'attraction', 'amenity', 'leisure'))

    def node(self, data, tags):
        err = []
        keys = tags.keys()
        keys = set(keys) & self.SimpleValuedTag
        for k in keys:
            if ';' in tags[k]:
                err.append((3070, 0, {"fr": "Valeurs multiples %s=%s" % (k, tags[k]), "en": "Multiple values %s=%s" % (k, tags[k])}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags):
        return self.node(data, tags)
