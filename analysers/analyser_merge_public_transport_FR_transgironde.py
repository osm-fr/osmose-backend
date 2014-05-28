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
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8040", "class": 41, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TransGironde stop not integrated") }
        self.possible_merge   = {"item":"8041", "class": 43, "level": 3, "tag": ["merge", "public transport"], "desc": T_(u"TransGironde stop, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger)
        self.officialURL = "http://www.datalocale.fr/drupal7/dataset/ig_transgironde_pa"
        self.officialName = u"Localisation des points d'arrêts des lignes régulières du réseau TransGironde"
        self.csv_file = "public_transport_FR_transgironde.csv.bz2"
        self.osmTags = {"highway": "bus_stop"}
        self.osmRef = "ref:FR:TransGironde"
        self.osmTypes = ["nodes", "ways"]
        self.sourceTable = "transgironde"
        self.sourceX = "LON"
        self.sourceY = "LAT"
        self.sourceSRID = "4326"
        self.defaultTag = {
            "source": u"Conseil général de la Gironde - 03/2013",
            "highway": "bus_stop",
            "public_transport": "stop_position",
            "bus": "yes",
            "network": "TransGironde"
        }
        self.defaultTagMapping = {
            "ref:FR:TransGironde": "NUMERO_PEG",
            "name": lambda res: res['NOM'].split(' - ')[1] if len(res['NOM'].split(' - ')) > 1 else None,
        }
        self.conflationDistance = 100
        self.text = lambda tags, fields: {"en": u"TransGironde stop of %s" % fields["NOM"], "fr": u"Arrêt TransGironde de %s" % fields["NOM"]}

    def replace(self, string):
        for s in self.replacement.keys():
            string = string.replace(s, self.replacement[s])
        return string

    replacement = {
        u'Coll.': u'Collège',
        u'Pl.': u'Place',
        u'Eglise': u'Église',
        u'Rte ': u'Route ',
        u'Bld ': u'Boulevard',
        u'St ': u'Staint ',
        u'Av. ': u'Avenue',
        u'Hôp.': u'Hôpital',
    }
