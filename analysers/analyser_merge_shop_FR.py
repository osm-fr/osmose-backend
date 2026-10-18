#!/usr/bin/env python
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

import json
import re
from modules.OsmoseTranslation import T_
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import SourceDataGouv, Parquet, Load_XY, Conflate, Select, Mapping
from modules import reaccentue


class Analyser_Merge_Shop_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        mapping = 'merge_data/shop_FR.mapping.json'
        mapingfile = json.loads(open(mapping).read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Shop_FR, r['class'].replace('.', ''), r['missing_official'], r['missing_osm'], r['class'], r['level'], r['title:fr'], r.get('trancheEffectifs'), r['match'], r['generate'])


class SubAnalyser_Merge_Shop_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, missing_official, missing_osm, classs, level, title, trancheEffectifs, selectTags, generateTags):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        classss = int(re.sub("[^0-9]", "", classs)) * 100 + ord(classs[-1]) - 65
        self.def_class_missing_official(item = missing_official, id = classss+1, level = level, tags = ['merge', 'fix:survey', 'fix:picture'],
            title = T_('{0} not integrated', classs + ', ' + title))
        #self.def_class_missing_osm(item = missing_osm, id = classss+2, level = level, tags = ['merge'],
        #    title = T_('{0} without tag "{1}" or invalid', title, 'ref:FR:SIRET'))
        #self.def_class_possible_merge(item = missing_official[0:-1]+"1", id = classss+3, level = level, tags = ['merge'],
        #    title = T_('{0}, integration suggestion', title))
        #self.def_class_update_official(item = missing_official[0:-1]+"2", id = classss+4, level = level, tags = ['merge'],
        #    title = T_('{0} update', title))

        dep_code = config.options.get('dep_code') or config.options.get('country').split('-')[1]
        proj = {971: 5490, 972: 5490, 973: 2972, 974: 2975, 976: 4471}.get(dep_code, 2154)

        self.init(
            "https://www.data.gouv.fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret",
            "Sirene",
            Parquet(SourceDataGouv(
                attribution="INSEE",
                dataset="5b7ffc618b4c4169d30727e0",
                resource="a29c1297-1f92-4e2a-8f6b-8c902ce96c5f",
            ), srid=proj, filters=(
                (
                    ('codeCommuneEtablissement', '>=', str(dep_code)),
                    ('codeCommuneEtablissement', '<', dep_code[:-1] + chr(ord(dep_code[-1]) + 1)),
                    ('coordonneeLambertAbscisseEtablissement', '!=', '[ND]'),
                    ('coordonneeLambertOrdonneeEtablissement', '!=', '[ND]'),
                    ('activitePrincipaleEtablissement', '=', classs),
                    ('etatAdministratifEtablissement', '=', 'A'),
                ),
            )),
            Load_XY("coordonneeLambertAbscisseEtablissement", "coordonneeLambertOrdonneeEtablissement",
                select = {"codeCommuneEtablissement": {"like": f"{dep_code}%"}},
                where = lambda res: (
                    (not res["complementAdresseEtablissement"] or (" APP" not in res["complementAdresseEtablissement"] and " CHEZ " not in res["complementAdresseEtablissement"])) and
                    (not trancheEffectifs or (res["trancheEffectifsEtablissement"] and res["trancheEffectifsEtablissement"] != "NN" and int(res["trancheEffectifsEtablissement"]) > trancheEffectifs)) ),
                unique = ["siren", "nic"]),
            Conflate(
                select = Select(
                    types = ['nodes', 'ways'],
                    tags = selectTags),
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = generateTags,
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:SIRET": lambda fields: fields["siret"],
                        # "ref:FR:RNA": "RNA",
                        #"short_name": "SIGLE",
                        #"start_date": lambda fields:
                        #    "-".join([fields["DDEBACT"][0:4], fields["DDEBACT"][4:6], fields["DDEBACT"][6:8]]) if fields["DDEBACT"] != "19000101" else
                        #    "-".join([fields["DCRET"][0:4], fields["DCRET"][4:6], fields["DCRET"][6:8]]) if fields["DCRET"] != "19000101" else
                        #    None,
                        "name": lambda fields: reaccentue.reaccentue(fields["enseigne1Etablissement"]) if fields["enseigne1Etablissement"] else (reaccentue.reaccentue(fields["denominationUsuelleEtablissement"]) if fields["denominationUsuelleEtablissement"] else None)},
                text = lambda tags, fields: {"en": ', '.join(filter(lambda f: f and f != 'None', [
                    fields["enseigne1Etablissement"] or fields["denominationUsuelleEtablissement"],
                    ' '.join(filter(lambda f: f and f != 'None', map(lambda k: fields[k], ["numeroVoieEtablissement", "indiceRepetitionEtablissement", "typeVoieEtablissement", "libelleVoieEtablissement", "complementAdresseEtablissement", "codePostalEtablissement", "libelleCommuneEtablissement"])))
                ]))} )))
