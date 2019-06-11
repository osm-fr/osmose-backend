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

from io import open # In python3 only, this import is not required
from backports import csv # In python3 only just "import csv"
import json
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Mapping, Select, Generate
from time import gmtime, strftime


class Analyser_Merge_Shop_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        mapping = 'merge_data/shop_FR.mapping.json'
        mapingfile = json.loads(open(mapping).read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Shop_FR, r['class'].replace('.', ''), r['missing_official'], r['missing_osm'], r['class'], r['level'], r['title'], r['match'], r['generate'])


class SubAnalyser_Merge_Shop_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, missing_official, missing_osm, classs, level, title, selectTags, generateTags):
        classss = int(classs.replace('.', '0')[:-1]) * 100 + ord(classs[-1]) - 65
        self.missing_official = {"item": missing_official, "class": classss+1, "level": level, "tag": ["merge"], "desc": T_(u"%s not integrated", title) }
        #self.missing_osm      = {"item": missing_osm, "class": classss+2, "level": level, "tag": ["merge"], "desc": T_f(u"{0} without tag \"{1}\" or invalid", title, 'ref:FR:SIRET') }
        #self.possible_merge   = {"item": missing_official[0:-1]+"1", "class": classss+3, "level": level, "tag": ["merge"], "desc": T_(u"%s, integration suggestion", title) }
        #self.update_official  = {"item": missing_official[0:-1]+"2", "class": classss+4, "level": level, "tag": ["merge"], "desc": T_(u"%s update", title) }

        dep_code = config.options.get('country').split('-')[1]

        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            u"http://www.sirene.fr/sirene/public/static/open-data",
            u"Sirene",
            CSV(Source(attribution = u"INSEE", millesime = "06/2019", gzip = True,
                fileUrl = u"http://data.cquest.org/geo_sirene/v2019/last/dep/geo_siret_{0}.csv.gz".format(dep_code))),
            Load("longitude", "latitude",
                select = {"activitePrincipaleEtablissement": classs, "geo_type": "housenumber", "etatAdministratifEtablissement": "A"},
                where = lambda res: float(res["geo_score"]) > 0.9,
                uniq = ["siren", "nic"]),
            Mapping(
                select = Select(
                    types = ['nodes', 'ways'],
                    tags = selectTags),
                conflationDistance = 200,
                generate = Generate(
                    static1 = generateTags,
                    static2 = {"source": self.source},
                    mapping1 = {
                        # "ref:FR:SIRET": lambda fields: fields["siren"] + fields["nic"],
                        # "ref:FR:RNA": "RNA",
                        "name": lambda fields: fields["enseigne1Etablissement"] or fields["denominationUsuelleEtablissement"] or None},
                        #"short_name": "SIGLE"},
                        #"start_date": lambda fields:
                        #    "-".join([fields["DDEBACT"][0:4], fields["DDEBACT"][4:6], fields["DDEBACT"][6:8]]) if fields["DDEBACT"] != "19000101" else
                        #    "-".join([fields["DCRET"][0:4], fields["DCRET"][4:6], fields["DCRET"][6:8]]) if fields["DCRET"] != "19000101" else
                        #    None},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda f: f and f != 'None', [fields["enseigne1Etablissement"] or fields["denominationUsuelleEtablissement"]] + list(map(lambda k: fields[k], ["numeroVoieEtablissement", "indiceRepetitionEtablissement" ,"typeVoieEtablissement", "libelleVoieEtablissement", "complementAdresseEtablissement", "codePostalEtablissement", "libelleCommuneEtablissement"]))))} )))
