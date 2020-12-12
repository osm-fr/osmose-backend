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
from .Analyser_Merge import Source, GPKG, LoadGeomCentroid, Mapping, Select, Generate


class Analyser_Merge_Man_Made_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        maping = [dict(
            # Antenne
            #   other data source

            # Autre construction élevée
            # Mât d'éclairage
            item = 8490,
            id = 100,
            level = 3,
            title = T_('Lighting mast not integrated'),
            select = {'nature_detaillee': 'Mât d\'éclairage'},
            tags = {'man_made': 'mast', 'tower:type': 'lighting'},
        ), dict(
            # Calvaire
            item = 8100,
            id = 2,
            level = 3,
            title = T_('Wayside cross not integrated'),
            select = {'nature': 'Calvaire'},
            tags = {'historic': 'wayside_cross'},
            generate_tags = {'historic': 'wayside_cross'},
       ), dict(
            # Cheminée
            item = 8490,
            id = 3,
            level = 2,
            title = T_('Chimney not integrated'),
            select = {'nature': 'Cheminée'},
            tags = {'man_made': 'chimney'},
        ), dict(
            # Clocher
            item = 8100,
            id = 4,
            title = T_('Bell tower not integrated'),
            level = 1,
            select = {'nature': 'Clocher'},
            tags = {'man_made': 'tower', 'tower:type': 'bell_tower'},
        ), dict(
            # Croix
            item = 8100,
            id = 5,
            level = 3,
            title = T_('Cross not integrated'),
            select = {'nature': 'Croix'},
            tags = [{'man_made': 'cross'}, {'historic': 'wayside_cross'}],
            generate_tags = {'historic': 'wayside_cross'},
        ), dict(
            # Eolienne
            item = 8270,
            id = 6,
            level = 2,
            title = T_('Wind turbine not integrated'),
            select = {'nature': 'Eolienne'},
            tags = {'power': 'generator', 'generator:source': 'wind'},
            height = False, # IGN: max height, OSM: center of rotor
        ), dict(
            # Minaret
            item = 8100,
            id = 7,
            level = 1,
            title = T_('Minaret not integrated'),
            select = {'nature': 'Minaret'},
            tags = {'man_made': 'tower', 'tower:type': 'minaret'},
            # Phare (300)
            #  not interested

        ), dict(
            # Puits d'hydrocarbures
            item = 8490,
            id = 9,
            level = 1,
            title = T_('Petroleum well not integrated'),
            select = {'nature': 'Puits d\'hydrocarbures'},
            tags = {'man_made': 'petroleum_well'},
        ), dict(
            # Torchère (200)
            item = 8490,
            id = 10,
            level = 1,
            title = T_('Flare not integrated'),
            select = {'nature': 'Torchère'},
            tags = {'man_made': 'flare'},

            # Transformateur
            #   other data source
        )]

        for r in maping:
            self.classFactory(SubAnalyser_Merge_Man_Made_FR, r['id'], r['item'], r['id'], r['level'], r['title'], r['select'], r['tags'], r.get('generate_tags', r['tags']), r.get('height', True))


class SubAnalyser_Merge_Man_Made_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, item, id, level, title, select, tags, generate_tags, height = True):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = item, id = id, level = level, tags = ['merge'], title = title)

        select.update({'etat_de_l_objet': 'En service'})
        self.init(
            "https://ign.fr",
            "IGN-Construction ponctuelle",
            GPKG(Source(attribution = "IGN", millesime = "01/2021",
                    file = "construction_ponctuelle.gpkg")),
            LoadGeomCentroid(
                select = select),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = tags),
                conflationDistance = 100,
                generate = Generate(
                    static1 = generate_tags,
                    static2 = {"source": self.source},
                    mapping2 = {
                        "height": lambda fields: fields["hauteur"] if height else None,
                        "name": lambda fields: fields["toponyme"] if fields["statut_du_toponyme"] == "Validé" else None},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda f: f not in (None, 'None'), [fields["nature"], fields["nature_detaillee"], fields["toponyme"]]))} )))
