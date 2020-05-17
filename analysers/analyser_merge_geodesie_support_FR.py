#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015                                      ##
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
import re
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Mapping, Select, Generate


class Analyser_Geodesie_Support_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        with open("merge_data/geodesie_support_FR.mapping.csv") as mappingfile:
            spamreader = csv.reader(mappingfile,  delimiter=u';')
            for row in spamreader:
                item, classs, level, topic = row[0:4]
                tags = list(map(lambda t: t.split('=') if t else None, row[4:7]))
                osmTags = dict(filter(lambda t: t, tags[0:2]))
                if len(osmTags) > 0:
                    defaultTags = dict(filter(lambda t: t, tags[2:3]))
                    slug = u''.join(filter(lambda x: x.isalpha(), topic.split('|')[0])).capitalize().encode('ascii', 'ignore').decode('utf8')
                    self.classFactory(SubAnalyser_Geodesie_Support_FR, slug, item, classs, level, topic, osmTags, defaultTags)


class SubAnalyser_Geodesie_Support_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, item, classs, level, topic, osmTags, defaultTags):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = item, id = classs, level = level, tags = ['merge'],
            title = T_f('Geodesic support not integrated {0}', topic.replace('^', '').replace('|', ', ')))

        self.init(
            u"http://geodesie.ign.fr",
            u"Fiches géodésiques",
            CSV(Source(attribution = u"©IGN 2010 dans le cadre de la cartographie réglementaire",
                    file = "geodesie.csv.bz2"),
                header = False),
            Load("lon", "lat",
                create = """
                    id VARCHAR(254) PRIMARY KEY,
                    lat VARCHAR(254),
                    lon VARCHAR(254),
                    description VARCHAR(4096),
                    ele VARCHAR(254),
                    ref VARCHAR(254)""",
                where = lambda res: not 'ruine' in res['description'].lower() and not 'ancien' in res['description'].lower() and not u'détruit' in res['description'].lower() and re.search(topic, res['description'], re.IGNORECASE)),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = osmTags),
                conflationDistance = 200,
                generate = Generate(
                    static1 = dict(dict(**osmTags), **defaultTags),
                    static2 = {"source": lambda a: a.parser.source.attribution},
                text = lambda tags, fields: {"en": fields["description"]} )))
