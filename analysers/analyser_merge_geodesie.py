#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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


class Analyser_Merge_Geodesie(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8070", "class": 1, "level": 3, "tag": ["merge"], "desc": T_(u"Missing survey point") }
        self.moved_official = {"item":"8070", "class": 3, "level": 3, "tag": ["merge"], "desc": T_(u"Moved survey point")}
        Analyser_Merge.__init__(self, config, logger,
            "http://geodesie.ign.fr",
            u"Fiches géodésiques",
            CSV(Source(file = "geodesie.csv.bz2"),
                header = False),
            Load("lon", "lat",
                create = """
                    id VARCHAR(254) PRIMARY KEY,
                    lat VARCHAR(254),
                    lon VARCHAR(254),
                    description VARCHAR(4096),
                    ele VARCHAR(254),
                    ref VARCHAR(254)"""),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"man_made": "survey_point"}),
                osmRef = "ref",
                extraJoin = "description",
                generate = Generate(
                    static = {
                        "man_made": "survey_point",
                        "note": u"Ne pas déplacer ce point, cf. - Do not move this node, see - http://wiki.openstreetmap.org/wiki/WikiProject_France/Repères_Géodésiques#Permanence_des_rep.C3.A8res",
                        "source": u"©IGN 2010 dans le cadre de la cartographie réglementaire"},
                    mapping = {
                        "ref": "ref",
                        "ele": "ele",
                        "description": "description"},
                    text = lambda tags, fields: {"en": u"Survey point %s" % tags["ref"], "fr": u"Repères géodésiques %s" % tags["ref"], "es": u"Señales geodésicas %s" % tags["ref"]} )))


class Analyser_Merge_Geodesie_Site(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8070", "class": 2, "level": 3, "tag": ["merge"], "desc": T_(u"Missing survey site") }
        Analyser_Merge.__init__(self, config, logger,
            "http://geodesie.ign.fr",
            u"Fiches géodésiques-site",
            CSV(Source(file = "geodesie_site.csv.bz2"),
                header = False),
            Load("lon", "lat",
                create = """
                    id VARCHAR(254) PRIMARY KEY,
                    ref VARCHAR(254),
                    name VARCHAR(254),
                    note VARCHAR(254),
                    network VARCHAR(254),
                    source VARCHAR(254),
                    lat VARCHAR(254),
                    lon VARCHAR(254)"""),
            Mapping(
                select = Select(
                    types = ["relations"],
                    tags = {
                        "type": "site",
                        "site": "geodesic"}),
                osmRef = "ref",
                generate = Generate(
                    static = {
                        "type": "site",
                        "site": "geodesic",
                        "source": u"©IGN 2010 dans le cadre de la cartographie réglementaire"},
                    mapping = {
                        "ref": "ref",
                        "name": "name",
                        "note": "note",
                        "network": "network"},
                    text = lambda tags, fields: {"en": u"Survey site %s - %s" % (fields["ref"], fields["name"]), "fr": u"Site géodésique %s - %s" % (fields["ref"], fields["name"]), "es": u"Sitio geodésico %s - %s" % (fields["ref"], fields["name"])} )))
