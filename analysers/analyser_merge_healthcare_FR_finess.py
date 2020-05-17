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
import csv
import io
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

        mapingfile = json.loads(open("merge_data/healthcare_FR_finess.mapping.json").read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Healthcare_FR_Finess, r['classes'], srid, is_in, r['categories'], r['items'], r.get('missing_osm', True), r['classes'], r['level'], r['title'], r['tags_select'], r['tags_generate1'], r['tags_generate2'])


class SubAnalyser_Merge_Healthcare_FR_Finess(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, srid, is_in, categories, items, missing_osm, classs, level, title, tags_select, tags_generate1, tags_generate2):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item =str(items[0]), id = classs+1, level = level, tags = ['merge'],
            title = T_f('{0} not integrated', title))
        if missing_osm is not False:
            self.def_class_missing_osm(item =str(items[1]), id = classs+2, level = level, tags = ['merge'],
                title = T_f('{0} without tag "{1}" or invalid', title, 'ref:FR:FINESS'))
        self.def_class_possible_merge(item =str(items[0]+1), id = classs+3, level = level, tags = ['merge'],
            title = T_f(u'{0}, integration suggestion', title))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/finess-extraction-du-fichier-des-etablissements/",
            u"FINESS Extraction du Fichier des établissements",
            CSV(Source_Finess(attribution = 'Le ministère des solidarités et de la santé', millesime = '03/2019', encoding = 'ISO-8859-1',
                    fileUrl = 'https://static.data.gouv.fr/resources/finess-extraction-du-fichier-des-etablissements/20190307-093304/etalab-cs1100507-stock-20190307-0422.csv')),
            Load("coordxet", "coordyet", srid = srid,
                select = {"categetab": categories},
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
                    mapping2 = {
                        "type:FR:FINESS": "categetab",
                        "ref:FR:SIRET": "siret",
                        "phone": lambda fields: self.phone(fields["telephone"]),
                        "fax": lambda fields: self.phone(fields["telecopie"]),
                    },
                text = lambda tags, fields: {"en": ", ".join(filter(lambda i: i not in (None, 'None'), [fields["rs"], fields["rslongue"], fields["complrs"], fields["compldistrib"], fields["numvoie"], fields["typvoie"], fields["voie"], fields["compvoie"], fields["lieuditbp"], fields["ligneacheminement"], fields["libcategetab"], fields["numuai"]]))} )))

    def phone(self, number):
        if number and len(number) == 10 and number[0] == "0":
            return "+33" + number[1:]


class Source_Finess(Source):
    def open(self):
        # Cheat the parent open
        self.encoding = 'UTF-8'
        f = Source.open(self)

        csvreader = csv.reader(f, delimiter=u';')
        structureet = [u'nofinesset,nofinessej,rs,rslongue,complrs,compldistrib,numvoie,typvoie,voie,compvoie,lieuditbp,commune,departement,libdepartement,ligneacheminement,telephone,telecopie,categetab,libcategetab,categagretab,libcategagretab,siret,codeape,codemft,libmft,codesph,libsph,dateouv,dateautor,datemaj,numuai,coordxet,coordyet,sourcecoordet,datemajcoord'.split(',')]
        geolocalisation = {}
        for row in csvreader:
            if row[0] == 'structureet':
                structureet.append(row[1:])
            elif row[0] == 'geolocalisation':
                geolocalisation[row[1]] = row[2:]
        for row in structureet:
            row += geolocalisation.get(row[0], [])

        csvfile = io.StringIO()
        writer = csv.writer(csvfile)
        for row in structureet:
            writer.writerow(row)
        csvfile.seek(0)

        return csvfile
