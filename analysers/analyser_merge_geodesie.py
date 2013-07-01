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

from Analyser_Merge import Analyser_Merge


class _Analyser_Merge_Geodesie(Analyser_Merge):

    create_table = """
        id VARCHAR(254) PRIMARY KEY,
        lat VARCHAR(254),
        lon VARCHAR(254),
        description VARCHAR(4096),
        ele VARCHAR(254),
        ref VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8070", "class": 1, "level": 3, "tag": ["merge"], "desc":{"en": u"Missing survey point", "fr": u"Repère géodésique manquant", "es": u"Falta la señal geodésico"} }
        self.moved_official = {"item":"8070", "class": 3, "level": 3, "tag": ["merge"], "desc":{"en": u"Moved survey point", "fr": u"Repère géodésique déplacé", "es": u"La señal geodésica está desplazada"}}
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://geodesie.ign.fr"
        self.officialName = "Fiches géodésiques"
        self.csv_file = "merge_data/geodesie.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV"
        self.osmTags = {
            "man_made": "survey_point",
        }
        self.extraJoin = "description"
        self.osmRef = "ref"
        self.osmTypes = ["nodes"]
        self.sourceTable = "geodesie"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "man_made": "survey_point",
            "note": "Ne pas déplacer ce point, cf. - Do not move this node, see - http://wiki.openstreetmap.org/wiki/WikiProject_France/Repères_Géodésiques#Permanence_des_rep.C3.A8res",
            "source": "©IGN 2010 dans le cadre de la cartographie réglementaire",
        }
        self.defaultTagMapping = {
            "ref": "ref",
            "ele": "ele",
            "description": "description",
        }
        self.text = lambda tags, fields: {"en": u"Survey point %s" % tags["ref"], "fr": u"Repères géodésiques %s" % tags["ref"], "es": u"Señales geodésicas" % tags["ref"]}


class Analyser_Merge_Geodesie_Site(Analyser_Merge):

    create_table = """
        id VARCHAR(254) PRIMARY KEY,
        ref VARCHAR(254),
        name VARCHAR(254),
        note VARCHAR(254),
        network VARCHAR(254),
        source VARCHAR(254),
        lat VARCHAR(254),
        lon VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8070", "class": 2, "level": 3, "tag": ["merge"], "desc":{"en": u"Missing survey site", "fr": u"Site géodésique manquant", "es": u"Sitio geodésico desaparecido"} }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://geodesie.ign.fr"
        self.officialName = "Fiches géodésiques-site"
        self.csv_file = "merge_data/geodesie_site.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV"
        self.osmTags = {
            "type": "site",
            "site": "geodesic",
        }
        self.osmRef = "ref"
        self.osmTypes = ["relations"]
        self.sourceTable = "geodesie_site"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "type": "site",
            "site": "geodesic",
            "source": "©IGN 2010 dans le cadre de la cartographie réglementaire",
        }
        self.defaultTagMapping = {
            "ref": "ref",
            "name": "name",
            "note": "note",
            "network": "network",
        }
        self.text = lambda tags, fields: {"en": u"Survey site %s - %s" % (fields["ref"], fields["name"]), "fr": u"Site géodésiques %s - %s" % (fields["ref"], fields["name"]), "es": u"Sitio geodésico %s - %s" % (fields["ref"], fields["name"])}
