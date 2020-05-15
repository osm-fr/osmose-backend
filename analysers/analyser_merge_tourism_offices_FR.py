#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Noémie Lehuby 2020                                         ##
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


class Analyser_Merge_Datatourisme_tourism_office_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item = 8010, id = 310, level = 3, tags = ['merge'],
            title = T_('Tourism office not integrated'))

        self.init(
            "https://data.datatourisme.gouv.fr",
            "DATAtourisme, la base nationale des données du tourisme en Open Data",
            CSV(Source(attribution = "data.gouv.fr:DATAtourisme", millesime = "05/2020",
                    fileUrl = "https://diffuseur.datatourisme.gouv.fr/webservice/9e8b7142a9fe83b82225032611cdb57e/cb33fad9-e86e-4f8a-a105-f4472f720526")),
            Load("Longitude", "Latitude",
                uniq = ["elem"]),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"information": "office"}),
                conflationDistance = 300,
                generate = Generate(
                    static1 = {
                        "information": "office",
                        "tourism": "information"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "contact:phone": "contact_phone",
                        "contact:email": "contact_email",
                        "contact:website": "contact_website",
                        "official_name": "label",
                    },
                text = lambda tags, fields: {"en": "%s - %s \n %s" % ( fields["street_address"], fields["city_address"], fields["elem"])} )))
