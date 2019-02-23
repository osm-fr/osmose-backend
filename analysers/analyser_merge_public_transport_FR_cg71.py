#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Transport_FR_cg71(Analyser_Merge):
    def __init__(self, config, logger = None):
        place = "CG71"
        self.missing_official = {"item":"8040", "class": 61, "level": 3, "tag": ["merge", "public transport"], "desc": T_f(u"{0} stop not integrated", place) }
        self.possible_merge   = {"item":"8041", "class": 63, "level": 3, "tag": ["merge", "public transport"], "desc": T_f(u"{0} stop, integration suggestion", place) }
        Analyser_Merge.__init__(self, config, logger,
            u"http://www.opendata71.fr/thematiques/transport/localisation-des-points-d-arret-de-bus",
            u"Localisation des arrêts de bus et car - CG71",
            CSV(Source(attribution = u"Conseil général de la Saône-et-Loire - Direction des Transports et de l'intermodalité", millesime = "02/2015",
                    fileUrl = u"http://opendata71interactive.cloudapp.net/DataBrowser/DownloadCsv?container=dataviz&entitySet=CG71DTIPointsArret&filter=NOFILTER")),
            Load("latitude", "longitude",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                osmRef = "ref:FR:CG71",
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "stop_position",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:CG71": "cod_arret"},
                    mapping2 = {"name": lambda res: res['nom'].split(' - ')[1].strip() if ' - ' in res['nom'] else res['nom'].strip()},
                    text = lambda tags, fields: T_f(u"{0} stop of {1}", place, fields["nom"].strip()) )))
