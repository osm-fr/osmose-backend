#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014                                      ##
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

from Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Police_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8190", "class": 1, "level": 3, "tag": ["merge"], "desc": T_(u"Police not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "http://www.data.gouv.fr/fr/dataset/liste-des-points-d-accueil-de-la-gendarmerie-nationale-avec-geolocalisation",
                name = u"Liste des points d'accueil de la gendarmerie nationale avec géolocalisation",
                file = "police_FR.csv.bz2",
                encoding = "ISO-8859-15",
                csv = CSV(separator = "|")),
            Load("lambert93_x", "lambert93_y", srid = 2154, table = "police_fr"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "police"}),
                conflationDistance = 1000,
                generate = Generate(
                    static = {
                        "amenity": "police",
                        "operator": "Gendarmerie Nationale",
                        "source": "data.gouv.fr:Ministère de l'Intérieur - 11/2013"},
                    mapping = {
                        "phone": "num_tph_fixe_unite"},
                text = lambda tags, fields: {"en": u"%s, %s" % (fields["nom_contextuel_unite"], fields["adresse_geographique_unite"])} )))
