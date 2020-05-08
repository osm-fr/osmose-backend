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
            u"https://www.data.gouv.fr/fr/datasets/datatourisme-la-base-nationale-des-donnees-du-tourisme-en-open-data/",
            u"DATAtourisme, la base nationale des données du tourisme en Open Data",
            CSV(Source(attribution = u"data.gouv.fr:DATAtourisme", millesime = "05/2020",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/b9aa0996-4bdf-46d0-a375-cf7adc02d19b"), #TODO: no stable url ?
                separator = u","),
            Load("Longitude", "Latitude",
                where =lambda row: "core#LocalTouristOffice" in row["Categories_de_POI"]
            ),
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
                        "contact:phone": lambda fields: parse_contact(fields)[1],
                        "contact:email": lambda fields: parse_contact(fields)[2],
                        "contact:website": lambda fields: parse_contact(fields)[3],
                        "official_name": "Nom_du_POI",
                    },
                text = lambda tags, fields: {"en": u"%s - %s \n %s" % ( fields["Adresse_postale"], fields["Code_postal_et_commune"], fields["URI_ID_du_POI"])} )))

        def parse_contact(line):
            contact_list = line["Contacts_du_POI"]
            contact = contact_list.split("|")[0] #TODO: is there a point of keep multiple contacts here ?
            contact_name, contact_phone, contact_email, contact_website = contact.split("#")
            return (contact_name, contact_phone, contact_email, contact_website)
