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
from .Analyser_Merge import SourceIGN, GPKG, LoadGeomCentroid, Conflate, Select, Mapping


class Analyser_Merge_Water_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        maping = [
            # Amer
            # Baie
            # Balise
            # Banc
        dict(
            # Cascade
            item = 8510,
            id = 4,
            level = 3,
            title = T_('Waterfall not integrated'),
            select = {'nature': 'Cascade'},
            tags = {'waterway': 'waterfall'},

            # Citerne
            # Embouchure
            # Espace maritime
            # Feu
        #), dict(
        # Too many false positives
        #    # Fontaine
        #    item = 8510,
        #    id = 9,
        #    level = 2,
        #    title = T_('Fountain not integrated'),
        #    select = {'nature': 'Fontaine'},
        #    tags = {'amenity': 'fountain'},
        ), dict(
            # Lavoir
            item = 8490,
            id = 101,
            level = 3,
            title = T_('Lavoir not integrated'),
            select = {'nature': 'Lavoir'},
            tags = {'amenity': 'lavoir'},

            # Marais
        ), dict(
            # Perte
            item = 8510,
            id = 12,
            level = 3,
            title = T_('Sinkhole not integrated'),
            select = {'nature': 'Perte'},
            tags = {'natural': 'sinkhole'},
        #), dict(
        #    # Point d'eau / Puits
        #    item = 8510,
        #    id = 131,
        #    level = 3,
        #    title = T_('Water well not integrated'),
        #    select = {'nature_detaillee': 'Puits'},
        #    tags = {'man_made': 'water_well'},
        ), dict(
            # Résurgence
            item = 8510,
            id = 14,
            level = 3,
            title = T_('Resurgence not integrated'),
            select = {'nature': 'Résurgence'},
            tags = {'natural': 'spring'},
        #), dict(
        # Too many false positives
        #    # Source
        #    item = 8510,
        #    id = 15,
        #    level = 3,
        #    title = T_('Spring not integrated'),
        #    select = {'nature': 'Source'},
        #    tags = [{'natural': 'spring'}, {'natural': 'hot_spring'}],
        #    generate_tags = {'natural': 'spring'}
        ), dict(
            # Source captée
            item = 8510,
            id = 16,
            level = 3,
            title = T_('Spring box not integrated'),
            select = {'nature': 'Source captée'},
            tags = {'natural': 'spring'},
            generate_tags = {'natural': 'spring', 'man_made': 'spring_box'},
        )]

        for r in maping:
            self.classFactory(SubAnalyser_Merge_Water_FR, r['id'], r['item'], r['id'], r['level'], r['title'], r['select'], r['tags'], r.get('generate_tags', r['tags']))


class SubAnalyser_Merge_Water_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, item, id, level, title, select, tags, generate_tags):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = item, id = id, level = level, tags = ['merge', 'water', 'fix:survey', 'fix:imagery'], title = title)

        select.update({'etat_de_l_objet': 'En service'})
        self.init(
            "https://ign.fr",
            "IGN-Détail Hydrographique",
            GPKG(SourceIGN(attribution = "IGN", gzip = True,
                    fileUrl = "http://files.opendatarchives.fr/professionnels.ign.fr/bdtopo/latest/geopackage/detail_hydrographique.gpkg.gz")),
            LoadGeomCentroid(
                select = select),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = tags),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = generate_tags,
                    static2 = {"source": self.source},
                    mapping2 = {
                        "name": lambda fields: fields["toponyme"] if fields["statut_du_toponyme"] == "Validé" else None},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda f: f not in (None, 'None'), [fields["nature"], fields["nature_detaillee"], fields["toponyme"]]))} )))
