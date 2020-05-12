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
        self.def_class_missing_official(item = 8420, id = 310, level = 3, tags = ['merge'],
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
                conflationDistance = 1000,
                generate = Generate(
                    static1 = {
                        "information": "office",
                        "tourism": "information"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "contact:phone": "contact_phone",
                        "contact:email": "contact_email",
                        "contact:website": "contact_website",
                        "wheelchair": lambda fields: parse_wheelchair(fields),
                        "official_name": "label"},
                text = lambda tags, fields: {"en": "%s - %s \n %s" % ( fields["street_address"], fields["city_address"], fields["elem"])} )))

def parse_wheelchair(fields):
    if not "wheelchair" in fields:
        return None
    if fields["wheelchair"] == "true":
        return "yes"
    if fields["wheelchair"] == "false":
        return "no"

# the csv data is generated with the following request:
# SELECT
#   ?elem ?type ?label
#   ?Latitude ?Longitude ?street_address ?city_address
#   ?wheelchair ?contact_phone ?contact_email ?contact_website
# WHERE {
#   ?elem <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type;
#               <http://www.w3.org/2000/01/rdf-schema#label> ?label;
#        <https://www.datatourisme.gouv.fr/ontology/core#isLocatedAt> ?location.
#
#   FILTER (?type IN (
#    ## <https://www.datatourisme.gouv.fr/ontology/core#TouristInformationCenter>,
#    <https://www.datatourisme.gouv.fr/ontology/core#LocalTouristOffice>
#   )).
#
#   ?location <http://schema.org/geo> ?geo.
#   ?geo <http://schema.org/latitude> ?Latitude;
#        <http://schema.org/longitude> ?Longitude.
#
#     ?location <http://schema.org/address> ?address.
#   ?address <http://schema.org/streetAddress> ?street_address;
#        <http://schema.org/addressLocality> ?city_address.
#
#   OPTIONAL {
#   ?elem <https://www.datatourisme.gouv.fr/ontology/core#hasBookingContact> ?agent_contact.
#   ?agent_contact <http://schema.org/telephone> ?contact_phone.
# 	}
#     OPTIONAL {
#   ?elem <https://www.datatourisme.gouv.fr/ontology/core#hasBookingContact> ?agent_contact.
#   ?agent_contact <http://schema.org/email> ?contact_email.
# 	}
#     OPTIONAL {
#   	 ?elem <https://www.datatourisme.gouv.fr/ontology/core#hasBookingContact> ?agent_contact.
#  	 ?agent_contact <http://xmlns.com/foaf/0.1/homepage> ?contact_website.
# 	}
#
#   OPTIONAL {
#     ?elem <https://www.datatourisme.gouv.fr/ontology/core#reducedMobilityAccess> ?wheelchair.
#   }
#
# }
