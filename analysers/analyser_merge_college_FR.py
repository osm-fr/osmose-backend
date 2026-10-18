#!/usr/bin/env python
###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2013-2018                                 ##
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
from .Analyser_Merge import Analyser_Merge_Point, Source, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_College_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8030, id = 100, level = 3, tags = ['merge', 'fix:survey', 'fix:imagery'],
            title = T_('College not integrated'))
        self.def_class_missing_osm(item = 7070, id = 101, level = 3, tags = ['merge', 'fix:chair'],
            title = T_('College without tag "ref:UAI" or invalid'))
        self.def_class_possible_merge(item = 8031, id = 102, level = 3, tags = ['merge', 'fix:survey', 'fix:imagery'],
            title = T_('College, integration suggestion'))
        self.def_class_update_official(item = 8032, id = 103, level = 3, tags = ['merge', 'fix:survey', 'fix:chair'],
            title = T_('College update'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/ideo-structures-denseignement-superieur/",
            "Idéo-Structures d'enseignement supérieur",
            CSV(
                Source(
                    attribution="Onisep - Idéo-Structures d'enseignement supérieur",
                    millesime = "07/2025",
                    fileUrl="https://api.opendata.onisep.fr/downloads/5fa586da5c4b6/5fa586da5c4b6.csv",
                    encoding = "utf-8-sig"),
                separator = ";"),
            Load_XY("longitude (X)", "latitude (Y)",
                xFunction = Load_XY.float_comma,
                yFunction = Load_XY.float_comma,
                select = {"type d'établissement": ["autre établissement d’enseignement",
                                                   #"campus connecté",
                                                   #"centre de formation d'apprentis",
                                                   #"centre de formation de fonctionnaires",
                                                   #"centre de formation professionnelle",
                                                   #"conservatoire départemental",
                                                   #"conservatoire national",
                                                   #"conservatoire régional",
                                                   #"CREPS",
                                                   "école d'architecture",
                                                   "école d'art",
                                                   "école d'ingénieurs",
                                                   "école de formation sportive",
                                                   "école de gestion et de commerce",
                                                   "école de santé",
                                                   "école des beaux-arts",
                                                   "école du secteur social",
                                                   "école vétérinaire",
                                                   #"enseignement public à distance",
                                                   #"établissement national de sport",
                                                   #"établissement régional d'enseignement adapté",
                                                   "grande école de commerce",
                                                   "institut d'études politiques",
                                                   "institut national polytechnique",
                                                   "institut national supérieur du professorat et de l'éducation",
                                                   "institut universitaire de technologie",
                                                   #"lycée agricole",
                                                   #"lycée général, technologique ou polyvalent",
                                                   #"lycée professionnel",
                                                   #"maison familiale rurale",
                                                   "unité de formation et de recherche",
                                                   "université",
                                                   ]}),
            Conflate(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"amenity": ["college", "university"]}),
                osmRef = "ref:UAI",
                conflationDistance = 500,
                mapping = Mapping(
                    static1 = {"source": self.source},
                    mapping1 = {
                        "amenity": lambda res: "university" if res["type d'établissement"] in ["institut national supérieur du professorat et de l'éducation", "institut universitaire de technologie", "unité de formation et de recherche", "université"] else "college",
                        "ref:UAI": "code UAI",
                        "operator:type": lambda res: "private" if res["statut"] in ["privé hors contrat", "privé reconnu par l’Etat", "privé sous contrat", "privé"] else None,
                        "short_name": "sigle"},
                    mapping2 = {"name": lambda res: res["nom"].replace("Ecole", "École")},
                    text = lambda tags, fields: {"en": " - ".join(filter(lambda i: i is not None, [fields["sigle"], fields["nom"].replace("Ecole", "École")]))} )))
