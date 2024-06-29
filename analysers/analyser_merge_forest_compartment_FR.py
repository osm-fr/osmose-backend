#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyright StC 2024                                                   ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, SHP, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Forest_Compartment_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8550, id = 1, level = 3, tags = ['merge', 'boundary', 'fix:survey', 'fix:imagery'],
            title = T_('Forest compartment not integrated'),
	    fix = T_('Please use the geopf.fr WMTS FORETS.PUBLIQUES service or the ONF data at http://metadata.carmencarto.fr/geonetwork/105/api/records/fr-662043116-82880F0D-E1C4-4EF3-80AF-416977F118F1 to create the appropriate boundary with forest compartment tags in OSM'),
	    trap = T_('Do not import to OSM the POI created by Osmose, which is just there to help you locate the missing forest compartment'))

        self.init(
            'http://metadata.carmencarto.fr/geonetwork/105/api/records/fr-662043116-82880F0D-E1C4-4EF3-80AF-416977F118F1',
            'parcelles forestières',
            SHP(Source(
                attribution='Office National des Forêts',
                millesime='2023-03-12',
                fileUrl='http://ws.carmencarto.fr/WFS/105/ONF_Forets?request=GetFeature&service=WFS&version=1.1.0&typeName=PARC_PUBL_FR&outputFormat=SHAPE'),
                zip='PARC_PUBL_FR.shp'),
            Load_XY(('ST_X(ST_PointOnSurface(ST_GeometryN(geom, 1)))',), ('ST_Y(ST_PointOnSurface(ST_GeometryN(geom, 1)))',)),
            Conflate(
                select = Select(
                    types = ['nodes','ways','relations'],
                    tags = {'boundary': 'forest_compartment'}),
                conflationDistance = 5000,
                mapping = Mapping(
                    static1 = {'type': 'boundary'},
                    static2 = {'boundary': 'forest_compartment'},
		    mapping1 = {
                      'ref' : 'ccod_prf',
                      'name' : 'llib_frt'
                    },
                )
            )
        )
