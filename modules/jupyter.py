#!/usr/bin/env python3
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2020                                      ##
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

import json
import pandas as pd
from io import StringIO
from ipyleaflet import Map, basemaps, basemap_to_tiles, Marker, LayerGroup
from ipywidgets import HTML

import modules.OsmOsisManager
from osmose_run import analyser_config, issues_file_from_fromat
from modules import OsmoseLog


LOG = None

def run(conf, analyser, plugin = None, format = 'osmose'):
    from optparse import Values
    options = Values({
        'verbose': False,
        'plugin': plugin and [plugin] or [],
        'change': False,
    })

    LOG = StringIO()
    logger = OsmoseLog.logger(LOG, True)

    osmosis_manager = modules.OsmOsisManager.OsmOsisManager(conf, conf.db_host, conf.db_user, conf.db_password, conf.db_base, conf.db_schema or conf.country, conf.db_persistent, logger)
    analyser_conf = analyser_config(conf, options, osmosis_manager)

    output = StringIO()
    analyser_conf.error_file = issues_file_from_fromat(output, format)

    with analyser(analyser_conf, logger.sub()) as analyser_obj:
        analyser_obj.analyser()

    return output.getvalue()


def print_csv(csv):
    return pd.read_csv(StringIO(csv))


def print_geojson(geojson, limit = 100):
    center = None
    j = json.load(StringIO(geojson))
    layer_group = LayerGroup()

    features = j['features']
    if limit is not None:
        features = features[0:limit]

    for f in features:
        location = (f['geometry']['coordinates'][1], f['geometry']['coordinates'][0])
        marker = Marker(location = location)
        marker.popup = HTML(str(f['properties']))
        layer_group.add_layer(marker)
        if not center:
            center = location

    if not center:
        center = (0, 0)

    m = Map(
        layers = (basemap_to_tiles(basemaps.OpenStreetMap.Mapnik), ),
        center = center,
        zoom = 8
    )

    m.add_layer(layer_group)
    return m
