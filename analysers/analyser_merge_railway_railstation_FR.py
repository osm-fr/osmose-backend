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

from Analyser_Merge import Analyser_Merge, Source, Load, Mapping, Select, Generate


class Analyser_Merge_Railway_Railstation_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8050", "class": 1, "level": 3, "tag": ["merge", "railway"], "desc": T_(u"Railway station not integrated") }
        self.missing_osm      = {"item":"7100", "class": 2, "level": 3, "tag": ["merge", "railway"], "desc": T_(u"Railway station without uic_ref or invalid") }
        self.possible_merge   = {"item":"8051", "class": 3, "level": 3, "tag": ["merge", "railway"], "desc": T_(u"Railway station, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "https://ressources.data.sncf.com/explore/dataset/sncf-ter-gtfs/",
                name = u"Horaires prévus des trains TER",
                file = "railway_railstation_FR.csv.bz2"),
            Load("stop_lon", "stop_lat", table = "railstation_fr",
                select = {"stop_id": "StopArea:%"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"railway": ["station", "halt"]}),
                osmRef = "uic_ref",
                conflationDistance = 500,
                generate = Generate(
                    static = {
                        "railway": "station",
                        "operator": "SNCF",
                        "source": "SNCF - 08/2015"},
                    mapping = {
                        "uic_ref": lambda res: res["stop_id"].split(":")[1][3:].split("-")[-1][:-1],
                        "name": lambda res: res["stop_name"].replace("gare de ", "")},
                    text = lambda tags, fields: {"en": fields["stop_name"][0].upper() + fields["stop_name"][1:]} )))
