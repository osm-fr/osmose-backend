#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2018                                      ##
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

import json
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Healthcare_FR_Finess(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        if config.db_schema == 'france_guadeloupe':
            srid = 2970
            is_in = lambda dep: dep == "9A"
        elif config.db_schema == 'france_guyane':
            srid = 2972
            is_in = lambda dep: dep == "9C"
        elif config.db_schema == 'france_reunion':
            srid = 2975
            is_in = lambda dep: dep == "9D"
        elif config.db_schema == 'france_martinique':
            srid = 2973
            is_in = lambda dep: dep == "9B"
        elif config.db_schema == 'france_saintpierreetmiquelon':
            srid = 32621
            is_in = lambda dep: dep == "9E"
        elif config.db_schema == 'france_mayotte':
            srid = 32738
            is_in = lambda dep: dep == "9F"
        else:
            srid = 2154
            is_in = lambda dep: dep not in ("9A", "9B", "9C", "9D")

        mapingfile = json.loads(open("merge_data/healthcare_FR_finess.mapping.csv", "rb").read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Healthcare_FR_Finess, r['classes'], srid, is_in, r['categories'], r['items'], r['missing_osm'], r['classes'], r['level'], r['title'], r['tags_select'], r['tags_generate1'], r['tags_generate2'])


class SubAnalyser_Merge_Healthcare_FR_Finess(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, srid, is_in, categories, items, missing_osm, classs, level, title, tags_select, tags_generate1, tags_generate2):
        self.missing_official = {"item":str(items[0]), "class": classs+1, "level": level, "tag": ["merge"], "desc": T_(u"{0} not integrated".format(title)) }
        if missing_osm != False:
            self.missing_osm = {"item":str(items[1]), "class": classs+2, "level": level, "tag": ["merge"], "desc": T_(u"{0} without (valid) ref:FR:FINESS".format(title)) }
        self.possible_merge = {"item":str(items[0]+1), "class": classs+3, "level": level, "tag": ["merge"], "desc": T_(u"{0}, integration suggestion".format(title)) }
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            "https://www.data.gouv.fr/fr/datasets/finess-extraction-du-fichier-des-etablissements/",
            u"FINESS Extraction du Fichier des établissements",
            CSV(Source(attribution = u"Le ministère des solidarités et de la santé", millesime = "08/2018",
                    file = "healthcare_FR_finess.csv.bz2")),
            Load("coordxet", "coordyet", srid = srid,
                select = {"categagretab": categories},
                where = lambda res: is_in(res["departement"])),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = tags_select),
                osmRef = "ref:FR:FINESS",
                conflationDistance = 200,
                generate = Generate(
                    static1 = tags_generate1,
                    static2 = dict({"source": self.source}, **tags_generate2),
                    mapping1 = {"ref:FR:FINESS": "nofinesset"},
                text = lambda tags, fields: {"en": ", ".join(filter(lambda i: i and i != "None", [fields["rslongue"], fields["complrs"], fields["compldistrib"], fields["numvoie"], fields["typvoie"], fields["voie"], fields["compvoie"], fields["lieuditbp"], fields["ligneacheminement"], fields["libcategetab"], fields["numuai"]]))} )))
