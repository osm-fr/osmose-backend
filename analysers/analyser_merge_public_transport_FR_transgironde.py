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


class Analyser_Merge_Public_Transport_FR_TransGironde(Analyser_Merge):

    create_table = """
        x VARCHAR(254),
        y VARCHAR(254),
        allign_hor VARCHAR(254),
        allign_ver VARCHAR(254),
        amenagemEn VARCHAR(254),
        controlz VARCHAR(254),
        decallag_e VARCHAR(254),
        decallage_ VARCHAR(254),
        nom VARCHAR(254),
        nom_commun VARCHAR(254),
        numero_peg VARCHAR(254),
        sous_type VARCHAR(254),
        type_arret VARCHAR(254),
        zone_tarif VARCHAR(254),
        rotation VARCHAR(254),
        point_x VARCHAR(254),
        point_y VARCHAR(254),
        x_l93 VARCHAR(254),
        y_l93 VARCHAR(254),
        lon NUMERIC(13,11),
        lat NUMERIC(13,11)
    """

    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8040", "class": 41, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TransGironde stop not integrated") }
        self.possible_merge   = {"item":"8041", "class": 43, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TransGironde stop, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.datalocale.fr/drupal7/dataset/ig_transgironde_pa"
        self.officialName = "Localisation des points d'arrêts des lignes régulières du réseau TransGironde"
        self.csv_file = "merge_data/public_transport_FR_transgironde.csv"
        self.csv_format = "WITH DELIMITER AS ',' NULL AS '' CSV HEADER"
        self.osmTags = {"highway": "bus_stop"}
        self.osmRef = "ref:FR:TransGironde"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "transgironde"
        self.sourceX = "lon"
        self.sourceY = "lat"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": "Conseil général de la Gironde - 03/2013",
            "highway": "bus_stop",
            "public_transport": "stop_position",
            "bus": "yes",
            "network": "TransGironde"
        }
        self.defaultTagMapping = {
            "ref:FR:TransGironde": "numero_peg",
            "name": lambda res: self.replace(res['nom'].split(' - ')[1]),
        }
        self.conflationDistance = 100
        self.text = lambda tags, fields: {"en": u"TransGironde stop of %s" % fields["nom"], "fr": u"Arrêt TransGironde de %s" % fields["nom"]}

    def replace(self, string):
        for s in self.replacement.keys():
            string = string.replace(s, replacement[s])
        return string

    replacement = {
        'Coll.': 'Collège',
        'Pl.': 'Place',
        'Eglise': 'Église',
        'Rte ': 'Route ',
        'Bld ': 'Boulevard',
        'St ': 'Staint ',
        'Av. ': 'Avenue',
        'Hôp.': 'Hôpital',
    }
