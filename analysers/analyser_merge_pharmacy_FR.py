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


class Analyser_Merge_Pharmacy_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8210", "class": 1, "level": 3, "tag": ["merge"], "desc": T_(u"Pharmacy not integrated") }
        self.missing_osm      = {"item":"7150", "class": 2, "level": 3, "tag": ["merge"], "desc": T_(u"Pharmacy without ref:FR:FINESS") }
        self.possible_merge   = {"item":"8211", "class": 3, "level": 3, "tag": ["merge"], "desc": T_(u"Pharmacy, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            Source(
                url = "",
                name = u"Celtipharm",
                file = "pharmacy_FR.csv.bz2"),
            Load("CTPM_LAMBERT93_X", "CTPM_LAMBERT93_y", srid = 2154, table = "pharmacy_fr"),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "pharmacy"}),
                osmRef = "ref:FR:FINESS",
                conflationDistance = 300,
                generate = Generate(
                    static = {
                        "amenity": "pharmacy",
                        "dispensing": "yes",
                        "source": "Celtipharm - 10/2014"},
                    mapping = {
                        "name": lambda res: res['CTPM_NOMUSAGE'].replace('PHARMACIE', 'Pharmacie').replace(' D ', " d'").replace(' L ', " l'").replace(' DE ', ' de ').replace(' DU ', ' du ').replace(' DES ', ' des ').replace(' LA ', ' la ').replace(' LES ', ' les ').replace(' ET ', ' et ').replace(' SAINT ', ' Saint-').replace(' SAINTE ', ' Sainte-'),
                        "ref:FR:FINESS": "CTPM_FINESSGEOGRAPHIQUE"},
                text = lambda tags, fields: {"en": ', '.join(filter( lambda x: x and x != 'None', [fields["CTPM_ADR1"], fields["CTPM_ADR2"], fields["CTPM_ADR3"], fields["CTPM_CP"], fields["CTPM_VILLE"]]))} )))
