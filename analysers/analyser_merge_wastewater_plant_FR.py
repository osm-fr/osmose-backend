#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jérôme Amagat 2019                                         ##
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

class Analyser_Merge_Wastewater_Plant_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8380, id = 1, level = 3, tags = ['merge'],
            title = T_('Wastewater plant not integrated'))
        self.def_class_possible_merge(item = 8381, id = 3, level = 3, tags = ['merge'],
            title = T_('Wastewater plant, integration suggestion'))
        self.def_class_update_official(item = 8382, id = 4, level = 3, tags = ['merge'],
            title = T_('Wastewater plant update'))

        self.init(
            u"http://www.sandre.eaufrance.fr/atlas/srv/fre/catalog.search#/metadata/ebef2115-bee5-40bb-b5cc-4593d82ba334",
            u"Stations de traitement des eaux usées - France entière",
            CSV(Source(attribution = u"Sandre", millesime = "09/2019",
                    fileUrl = u"http://services.sandre.eaufrance.fr/geo/odp_FRA?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&typename=SysTraitementEauxUsees&SRSNAME=EPSG:4326&OUTPUTFORMAT=CSV")),
            Load("LongWGS84OuvrageDepollution", "LatWGS84OuvrageDepollution",
                select = {"DateMiseHorServiceOuvrageDepollution": None}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"man_made": "wastewater_plant"}),
                conflationDistance = 200,
                osmRef = "ref:sandre",
                generate = Generate(
                    static1 = {"man_made": "wastewater_plant"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:sandre": "CdOuvrageDepollution",
                        "start_date": lambda fields: None if not fields.get(u"DateMiseServiceOuvrageDepollution") else fields[u"DateMiseServiceOuvrageDepollution"][0:4] if fields[u"DateMiseServiceOuvrageDepollution"].endswith('-01-01') or fields[u"DateMiseServiceOuvrageDepollution"].endswith('-12-31') else fields[u"DateMiseServiceOuvrageDepollution"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["NomOuvrageDepollution"], fields["LbSystemeCollecte"], fields["NomAgglomerationAssainissement"]]))} )))
