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

import csv
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

        with open("merge_data/healthcare_FR_finess.mapping.csv", "rb") as mappingfile:
            spamreader = csv.reader(mappingfile)
            self.analysers = []
            for row in spamreader:
                if row[0][0] == '#':
                    continue
                categories, items, classes, level, title = row[0:5]
                categories = categories.split('|')
                items = map(int, items.split('|'))
                classes = int(classes)
                level = int(level)
                tags = dict(map(lambda t: t.split('=') if t else None, row[5:]))
                if len(tags) > 0:
                    self.classFactory(SubAnalyser_Merge_Healthcare_FR_Finess, classes, srid, is_in, categories, items, classes, level, title.decode('utf-8'), tags)


class SubAnalyser_Merge_Healthcare_FR_Finess(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, srid, is_in, categories, items, classs, level, title, tags):
        self.missing_official = {"item":str(items[0]), "class": classs+1, "level": level, "tag": ["merge"], "desc": T_(u"{0} not integrated".format(title)) }
        self.missing_osm      = {"item":str(items[1]), "class": classs+2, "level": level, "tag": ["merge"], "desc": T_(u"{0} without ref:FR:FINESS".format(title)) }
        self.possible_merge   = {"item":str(items[0]+1), "class": classs+3, "level": level, "tag": ["merge"], "desc": T_(u"{0}, integration suggestion".format(title)) }
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
                    tags = tags),
                osmRef = "ref:FR:FINESS",
                conflationDistance = 200,
                generate = Generate(
                    static1 = tags,
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:FINESS": "nofinesset"},
                text = lambda tags, fields: {"en": ", ".join(filter(lambda i: i and i != "None", [fields["rslongue"], fields["complrs"], fields["compldistrib"], fields["numvoie"], fields["typvoie"], fields["voie"], fields["compvoie"], fields["lieuditbp"], fields["ligneacheminement"], fields["libcategetab"], fields["numuai"]]))} )))
