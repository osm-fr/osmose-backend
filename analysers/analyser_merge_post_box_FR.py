#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015-2016                                 ##
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
from .Analyser_Merge import Analyser_Merge_Point, SourceDataFair, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Post_box_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8025, id = 1, level = 3, tags = ['merge', 'post', 'fix:survey', 'fix:picture'],
            title = T_('Post box not integrated'))
        self.def_class_missing_osm(item = 7051, id = 2, level = 3, tags = ['merge', 'post', 'fix:chair'],
            title = T_('Post box without tag "ref" or invalid'))
        self.def_class_possible_merge(item = 8026, id = 3, level = 3, tags = ['merge', 'post', 'fix:chair'],
            title = T_('Post box, integration suggestion'))

        self.init(
            "https://datanova.laposte.fr/datasets/laposte-boiterue",
            "Liste des boîtes aux lettres de rue - France métropolitaine et DOM avec heure limite de dépôt",
            CSV(SourceDataFair(
                attribution = "data.gouv.fr:LaPoste",
                url="https://datanova.laposte.fr/datasets/laposte-boiterue", file_name="BAL_de_rue_0923.csv")),
            Load_XY("VA_COORD_ADR_X", "VA_COORD_ADR_Y"),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "post_box"}),
                osmRef = "ref",
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {
                        "amenity": "post_box",
                        "operator": "La Poste"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref": "CO_MUP"},
                text = lambda tags, fields: {"en": ", ".join(filter(lambda x: x, [fields["VA_NO_VOIE"], fields["LB_EXTENSION"], fields["LB_VOIE_EXT"], fields["CO_POSTAL"], fields["LB_COM"]]))} )))
