#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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
from time import gmtime, strftime


class Analyser_Merge_Shop_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        with open("merge_data/shop_FR.mapping.csv", "rb") as mappingfile:
            spamreader = csv.reader(mappingfile)
            for row in spamreader:
                if row[0][0] == '#':
                    continue
                items, classs, level, title = row[0:4]
                items = items.split('|')
                level = int(level)
                title = title.decode('utf8')
                osmTags = filter(lambda a: a, map(lambda t: (t.split('=') + [None])[0:2] if t else None, row[4:]))
                if len(osmTags) > 0:
                    self.classFactory(SubAnalyser_Merge_Shop_FR, classs, items, classs, level, title, dict(osmTags), dict(filter(lambda a: a[1], osmTags)))


class SubAnalyser_Merge_Shop_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, items, classs, level, title, selectTags, generateTags):
        classss = int(classs.replace('.', '0')[:-1]) * 100 + ord(classs[-1]) - 65
        self.missing_official = {"item": items[0], "class": classss+1, "level": level, "tag": ["merge"], "desc": T_(u"%s not integrated", title) }
        self.missing_osm      = {"item": items[1], "class": classss+2, "level": level, "tag": ["merge"], "desc": T_(u"%s without ref:FR:SIRET or invalid", title) }
        self.possible_merge   = {"item": items[0][0:-1]+"1", "class": classss+3, "level": level, "tag": ["merge"], "desc": T_(u"%s, integration suggestion", title) }
        self.update_official  = {"item": items[0][0:-1]+"2", "class": classss+4, "level": level, "tag": ["merge"], "desc": T_(u"%s update", title) }
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            "http://www.sirene.fr/sirene/public/static/open-data",
            u"Sirene",
            CSV(Source(attribution = u"INSEE", millesime = "07/2017", file = "shop_FR-light.csv.bz2")),
            Load("longitude", "latitude",
                select = {"APET700": classs, "NJ": True},
                uniq = ["SIREN", "NIC"]),
            Mapping(
                select = Select(
                    types = ['nodes', 'ways'],
                    tags = selectTags),
                conflationDistance = 80,
                generate = Generate(
                    static1 = generateTags,
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:SIRET": lambda fields: fields["SIREN"] + fields["NIC"],
                        "ref:FR:RNA": "RNA",
                        "name": lambda fields: fields["ENSEIGNE"] or (fields["NOMEN_LONG"] if fields["NJ"] else None),
                        "short_name": "SIGLE",
                        "start_date": lambda fields:
                            "-".join([fields["DDEBACT"][0:4], fields["DDEBACT"][4:6], fields["DDEBACT"][6:8]]) if fields["DDEBACT"] != "19000101" else
                            "-".join([fields["DCRET"][0:4], fields["DCRET"][4:6], fields["DCRET"][6:8]]) if fields["DCRET"] != "19000101" else
                            None},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda f: f and f != 'None', [fields["ENSEIGNE"] or (fields["NOMEN_LONG"] if fields["NJ"] else None)] + map(lambda k: fields[k], ["L1_DECLAREE", "L2_DECLAREE" ,"L3_DECLAREE", "L4_DECLAREE", "L5_DECLAREE", "L6_DECLAREE", "L7_DECLAREE"])))} )))
