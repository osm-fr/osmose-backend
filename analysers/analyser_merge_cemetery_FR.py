#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2021                                      ##
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
from .Analyser_Merge import Analyser_Merge, Source, GPKG, LoadGeomCentroid, Mapping, Select, Generate


class Analyser_Merge_Public_Cemetery_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8480, id = 8, level = 1, tags = ['merge', 'public equipment', 'fix:imagery'],
            title = T_('Cemetery not integrated'))

        self.init(
            "https://ign.fr",
            "IGN-Cimetière",
            GPKG(Source(attribution = "IGN", millesime = "09/2020",
                    fileUrl = "http://files.opendatarchives.fr/professionnels.ign.fr/bdtopo/.gpkg/cimetiere.gpkg")),
            LoadGeomCentroid(
                select = {"etat_de_l_objet": "En service"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [
                        {"landuse": "cemetery"},
                        {"amenity": "grave_yard"} ]),
                conflationDistance = 200,
                generate = Generate(
                    static1 = {
                        "landuse": "cemetery"},
                    static2 = {"source": self.source},
                    mapping2 = {
                        "name": lambda fields: fields["toponyme"] if fields["statut_du_toponyme"] == "Validé" else None},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda f: f not in (None, 'None'), [fields["nature"], fields["nature_detaillee"], fields["toponyme"]]))} )))
