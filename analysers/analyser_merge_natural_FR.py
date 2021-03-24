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


class Analyser_Merge_Natural_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        maping = [
        #   40806 Vallée
        dict(
            #   40802
            #       4 Ancien glacier
            item = 8530,
            id = 100,
            level = 3,
            title = T_('Valley not integrated'),
            select = {'nature': 'Vallée'},
            tags = {'natural': 'valley'},
        ),
        #   38194 Rochers
        dict(
            #    7034
            item = 8530,
            id = 110,
            level = 3,
            title = T_('Rock not integrated'),
            select = {'nature': 'Rochers', 'nature_detaillee': 'None'},
            tags = {'natural': 'rock'},
        ),
        dict(
            #   31138 Bloc rocheux isolé
            item = 8530,
            id = 111,
            level = 3,
            title = T_('Stone not integrated'),
            select = {'nature': 'Rochers', 'nature_detaillee': 'Bloc rocheux isolé'},
            tags = {'natural': 'stone'},
        ),
        dict(
            #      22 Cheminée de fée
            item = 8530,
            id = 112,
            level = 3,
            title = T_('Hoodoo not integrated'),
            select = {'nature': 'Rochers', 'nature_detaillee': 'Cheminée de fée'},
            tags = {'natural': 'rock'},
            generate_tags = {'natural': 'rock', 'rock': 'hoodoo'},
        ),
        # Sommet, Pic, Montagne
        dict(
            #   36228 Sommet
            #        36225
            #            3 Inselberg
            #    2501 Pic
            #     617 Montagne
            item = 8530,
            id = 120,
            level = 2,
            title = T_('Peak not integrated'),
            select = {'nature': ['Sommet', 'Pic', 'Montagne']},
            tags = {'natural': 'peak'},
        ),
        #   18204 Versant
        dict(
            item = 8530,
            id = 130,
            level = 3,
            title = T_('Moutainside not integrated'),
            select = {'nature': 'Versant'},
            tags = {'natural': 'mountainside'},
        ),
        #   10468 Crête
        dict(
            item = 8530,
            id = 140,
            level = 3,
            title = T_('Ridge not integrated'),
            select = {'nature': 'Crête'},
            tags = {'natural': 'ridge'},
        ),
        #   10063 Col
        dict(
            item = 8530,
            id = 150,
            level = 2,
            title = T_('Saddle not integrated'),
            select = {'nature': 'Col'},
            tags = {'natural': 'saddle'},
        ),
        #    8335 Grotte
        dict(
            #    7064
            #    1271 Cave
            item = 8530,
            id = 160,
            level = 2,
            title = T_('Cave entrance not integrated'),
            select = {'nature': 'Grotte'},
            tags = {'natural': 'cave_entrance'},
        ),
        #    4184 Plaine
        dict(
            item = 8530,
            id = 170,
            level = 3,
            title = T_('Plain not integrated'),
            select = {'nature': 'Plaine'},
            tags = {'natural': 'plain'},
        ),
        #    1998 Ile
        dict(
            #    1993
            item = 8530,
            id = 180,
            level = 1,
            title = T_('Island not integrated'),
            select = {'nature': 'Ile', 'nature_detaillee': 'None'},
            tags = {'place': 'island'},
        ),
        dict(
            #       5 Presqu'île
            item = 8530,
            id = 181,
            level = 1,
            title = T_('Peninsula not integrated'),
            select = {'nature': 'Ile', 'nature_detaillee': 'Presqu\'île'},
            tags = {'natural': 'peninsula'},
        ),
        #    1697 Gouffre
             #    1118
             #     579 Aven
        dict(
            item = 8530,
            id = 190,
            level = 2,
            title = T_('Pit not integrated'),
            select = {'nature': 'Gouffre'},
            tags = {'natural': 'sinkhole', 'sinkhole': 'pit'},
        ),
        #    2041 Plage
        dict(
            item = 8530,
            id = 200,
            level = 2,
            title = T_('Beach not integrated'),
            select = {'nature': 'Plage'},
            tags = {'natural': 'beach'},
        ),
        #    2132 Cap
        dict(
            item = 8530,
            id = 210,
            level = 2,
            title = T_('Cape not integrated'),
            select = {'nature': 'Cap'},
            tags = {'natural': 'cape'},
        ),
        #    1434 Récif
        dict(
            item = 8530,
            id = 220,
            level = 3,
            title = T_('Reef not integrated'),
            select = {'nature': 'Récif'},
            tags = {'natural': 'reef'},
        ),
        #    1262 Dépression
        dict(
            item = 8530,
            id = 230,
            level = 3,
            title = T_('Sinkhole not integrated'),
            select = {'nature': 'Dépression'},
            tags = {'natural': 'sinkhole'},
        ),
        #     600 Gorge
        dict(
            item = 8530,
            id = 240,
            level = 3,
            title = T_('Gorge not integrated'),
            select = {'nature': 'Gorge'},
            tags = {'natural': 'gorge'},
        ),
        #     286 Escarpement
        dict(
            item = 8530,
            id = 250,
            level = 3,
            title = T_('Cliff not integrated'),
            select = {'nature': 'Escarpement'},
            tags = {'natural': 'cliff'},
        ),
        #     250 Dune
        dict(
            item = 8530,
            id = 250,
            level = 3,
            title = T_('Dune not integrated'),
            select = {'nature': 'Dune'},
            tags = {'natural': 'dune'},
        ),
        #     159 Volcan
        dict(
            item = 8530,
            id = 260,
            level = 1,
            title = T_('Volcano not integrated'),
            select = {'nature': 'Volcan'},
            tags = {'natural': 'volcano'},
        ),
        #     142 Cirque
        dict(
            item = 8530,
            id = 270,
            level = 3,
            title = T_('Cirque not integrated'),
            select = {'nature': 'Cirque'},
            tags = {'natural': 'cirque'},
        ),
        #      36 Terril
        dict(
            item = 8530,
            id = 280,
            level = 3,
            title = T_('Spoil heap not integrated'),
            select = {'nature': 'Terril'},
            tags = {'man_made': 'spoil_heap'},
        ),
        #      10 Isthme
        dict(
            item = 8530,
            id = 290,
            level = 2,
            title = T_('Isthmus not integrated'),
            select = {'nature': 'Isthme'},
            tags = {'natural': 'isthmus'},
        )
        ]

        for r in maping:
            self.classFactory(SubAnalyser_Merge_Orography_FR, r['id'], r['item'], r['id'], r['level'], r['title'], r['select'], r['tags'], r.get('generate_tags', r['tags']), r.get('height', True))


class SubAnalyser_Merge_Orography_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, item, id, level, title, select, tags, generate_tags, height = True):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = item, id = id, level = level, tags = ['merge', 'fix:imagery', 'fix:survey'], title = title)

        self.init(
            "https://ign.fr",
            "IGN-Détail orographique",
            GPKG(Source(attribution = "IGN", millesime = "12/2020", gzip = True,
                    fileUrl = "http://files.opendatarchives.fr/professionnels.ign.fr/bdtopo/latest/geopackage/detail_orographique.gpkg.gz")),
            LoadGeomCentroid(
                select = select),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = tags),
                conflationDistance = 500,
                mapping = Mapping(
                    static1 = generate_tags,
                    static2 = {"source": self.source},
                    mapping2 = {
                        "name": lambda fields: fields["toponyme"] if fields["statut_du_toponyme"] == "Validé" else None},
                    text = lambda tags, fields: {'en': ', '.join(filter(lambda f: f not in (None, 'None'), [fields["nature"], fields["nature_detaillee"]]))} )))
