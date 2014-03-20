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

from Analyser_Merge import Analyser_Merge


class Analyser_Merge_Public_Transport_FR_cg71(Analyser_Merge):

    create_table = """
        entityid VARCHAR(254),
        cod_arret VARCHAR(254),
        cod_comm VARCHAR(254),
        dat_dval VARCHAR(254),
        nom VARCHAR(254),
        latitude VARCHAR(254),
        longitude VARCHAR(254)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8040", "class": 61, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"CG71 stop not integrated") }
        self.possible_merge   = {"item":"8041", "class": 63, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"CG71 stop, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.opendata71.fr/thematiques/transport/localisation-des-points-d-arret-de-bus"
        self.officialName = "Localisation des arrêts de bus et car - CG71"
        self.csv_file = "merge_data/public_transport_FR_cg71.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER QUOTE '~'"
        self.osmTags = {
            "highway": "bus_stop"
        }
        self.osmRef = "ref:FR:CG71"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "bus_cg71"
        self.sourceX = "latitude"
        self.sourceY = "longitude"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Conseil général de la Saône-et-Loire - Direction des Transports et de l'intermodalité - 03/2013",
            "highway": "bus_stop",
            "public_transport": "stop_position",
            "bus": "yes",
        }
        self.defaultTagMapping = {
            "ref:FR:CG71": "cod_arret",
            "name": lambda res: res['nom'].split(' - ')[1].strip() if ' - ' in res['nom'] else res['nom'].strip(),
        }
        self.conflationDistance = 100
        self.text = lambda tags, fields: {"en": u"CG71 stop of %s" % fields["nom"].strip(), "fr": u"Arrêt CG71 de %s" % fields["nom"].strip()}
