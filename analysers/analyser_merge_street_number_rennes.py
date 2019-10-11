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

from .Analyser_Merge import Source, CSV, Load, Mapping, Generate
from .analyser_merge_street_number import _Analyser_Merge_Street_Number


class Analyser_Merge_Street_Number_Rennes(_Analyser_Merge_Street_Number):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Street_Number.__init__(self, config, 7, "Rennes", logger,
            u"https://data.rennesmetropole.fr/explore/dataset/rva-bal/information/",
            u"Référentiel voies et adresses de Rennes Métropole",
            CSV(Source(attribution = u"Rennes Métropole", millesime = "03/2018",
                    fileUrl = u"https://data.rennesmetropole.fr/explore/dataset/rva-bal/download/?format=csv"),
                separator = u";"),
            Load("long", "lat",
                where = lambda res: res["numero"] != "99999"),
            Mapping(
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {"addr:housenumber": lambda res: res["numero"] + (" "+res["suffixe"] if res["suffixe"] else "")},
                    text = lambda tags, fields: {"en": u"%s%s %s" % (fields["numero"], (" "+fields["suffixe"] if fields["suffixe"] else ""), fields["voie_nom"])} )))
