#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, GTFS, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Railway_Railstation_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8050, id = 1, level = 3, tags = ['merge', 'railway', 'fix:imagery', 'fix:survey'],
            title = T_('Railway station not integrated'))
        self.def_class_missing_osm(item = 7100, id = 2, level = 3, tags = ['merge', 'railway', 'fix:chair'],
            title = T_('Railway station without tag "uic_ref" or invalid'))
        self.def_class_possible_merge(item = 8051, id = 3, level = 3, tags = ['merge', 'railway', 'fix:chair'],
            title = T_('Railway station, integration suggestion'))

        self.init(
            "https://ressources.data.sncf.com/explore/dataset/sncf-ter-gtfs/",
            "Horaires prévus des trains TER",
            GTFS(Source(attribution = "SNCF", millesime = "08/2017",
                    fileUrl = "https://eu.ftp.opendatasoft.com/sncf/gtfs/export-ter-gtfs-last.zip")),
            Load_XY("stop_lon", "stop_lat",
                select = {"stop_id": {"like": "StopPoint:OCETrain%"}}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"railway": ["station", "halt"]}),
                osmRef = "uic_ref",
                conflationDistance = 500,
                mapping = Mapping(
                    static1 = {
                        "railway": "station",
                        "operator": "SNCF"},
                    static2 = {"source": self.source},
                    mapping1 = {"uic_ref": lambda res: res["stop_id"].split(":")[1][3:].split("-")[-1][:-1]},
                    mapping2 = {"name": lambda res: res["stop_name"].replace("gare de ", "")},
                    text = lambda tags, fields: {"en": fields["stop_name"][0].upper() + fields["stop_name"][1:]} )))
