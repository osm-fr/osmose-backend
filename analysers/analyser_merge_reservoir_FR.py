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
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, GPKG, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_Reservoir_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        maping = [dict(
            # Château d'eau
            item = 8500,
            id = 0,
            level = 1,
            title = T_('Water tower not integrated'),
            select = {'nature': 'Château d\'eau'},
            tags = {'man_made': 'water_tower'},
        ), dict(
            # Réservoir d'eau ou château d'eau au sol
            item = 8500,
            id = 1,
            level = 2,
            title = T_('Covered reservoir not integrated'),
            select = {'nature': 'Réservoir d\'eau ou château d\'eau au sol'},
            tags = {'man_made': 'reservoir_covered'},
        ), dict(
            # Réservoir industriel
            item = 8500,
            id = 2,
            level = 3,
            title = T_('Storage tank not integrated'),
            select = {'nature': 'Réservoir industriel'},
            tags = {'man_made': 'storage_tank'},
            # Inconnue
            #   not done
        )]

        for r in maping:
            self.classFactory(SubAnalyser_Merge_Reservoir_FR, r['id'], r['item'], r['id'], r['level'], r['title'], r['select'], r['tags'], r.get('height', True))


class SubAnalyser_Merge_Reservoir_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, item, id, level, title, select, tags, height = True):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = item, id = id, level = level, tags = ['merge', 'water'], title = title)

        select.update({'etat_de_l_objet': 'En service'})
        self.init(
            "https://ign.fr",
            "IGN-Construction ponctuelle",
            GPKG(Source(attribution = "IGN", millesime = "09/2020", gzip = True,
                    fileUrl = "http://files.opendatarchives.fr/professionnels.ign.fr/bdtopo/latest/geopackage/reservoir.gpkg.gz")),
            LoadGeomCentroid(
                select = select),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = tags),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = tags,
                    static2 = {"source": self.source},
                    mapping2 = {
                        "height": lambda fields: fields["hauteur"] if height else None} )))
