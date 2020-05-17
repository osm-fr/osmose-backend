#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_College_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8030, id = 100, level = 3, tags = ['merge'],
            title = T_('College not integrated'))
        self.def_class_missing_osm(item = 7070, id = 101, level = 3, tags = ['merge'],
            title = T_('College without tag "ref:UAI" or invalid'))
        self.def_class_possible_merge(item = 8031, id = 102, level = 3, tags = ['merge'],
            title = T_('College, integration suggestion'))
        self.def_class_update_official(item = 8032, id = 103, level = 3, tags = ['merge'],
            title = T_('College update'))

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/etablissements-denseignement-superieur-2",
            u"Etablissements d'enseignement supérieur",
            CSV(Source(attribution = u"Etablissements d'enseignement supérieur", millesime = "09/2017",
                    fileUrl = u"https://api.opendata.onisep.fr/downloads/57da952417293/57da952417293.csv", encoding = "utf-8-sig"),
                separator = u';'),
            Load("longitude (X)", "latitude (Y)",
                xFunction = self.float_comma,
                yFunction = self.float_comma),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"amenity": ["college", "university"]}),
                osmRef = "ref:UAI",
                conflationDistance = 500,
                generate = Generate(
                    static1 = {"amenity": "college"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:UAI": "code UAI",
                        "operator:type": lambda res: "private" if res["statut"] in [u"Privé hors contrat", u"Privé reconnu", u"Privé sous contrat"] else None,
                        "short_name": "sigle"},
                    mapping2 = {"name": lambda res: res["nom"].replace(u"Ecole", u"École")},
                    text = lambda tags, fields: {"en": " - ".join(filter(lambda i: i is not None, [fields["sigle"], fields["nom"].replace(u"Ecole", u"École")]))} )))
