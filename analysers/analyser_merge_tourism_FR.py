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

import json
from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_tourism_FR(Analyser_Merge_Dynamic):
    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        mapingfile = json.loads(open("merge_data/tourism_FR.mapping.json").read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Datatourisme_FR, r['classes'], r['items'], r['classes'], r['title'], r['type'], r['tags_select'], r.get('osm_types', ['nodes', 'ways']), r['conflationDistance'], r['tags_generate'])


class SubAnalyser_Datatourisme_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, items, classs, title, type_, tags_select, osm_types, conflationDistance, tags_generate):
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger)
        self.def_class_missing_official(item = items, id = classs, level = 3, tags = ['merge'],
            title = T_f('{0} not integrated', title))

        self.init(
            "https://data.datatourisme.gouv.fr",
            "DATAtourisme, la base nationale des données du tourisme en Open Data",
            CSV(Source(attribution = "data.gouv.fr:DATAtourisme", millesime = "05/2020",
                    fileUrl = "https://diffuseur.datatourisme.gouv.fr/webservice/9e8b7142a9fe83b82225032611cdb57e/cb33fad9-e86e-4f8a-a105-f4472f720526")),
            Load("Longitude", "Latitude",
                select = {'type': type_},
                uniq = ["elem"]),
            Mapping(
                select = Select(
                    types = osm_types,
                    tags = tags_select),
                conflationDistance = conflationDistance,
                generate = Generate(
                    static1 = tags_generate,
                    static2 = {"source": self.source},
                    mapping1 = {
                        "contact:phone": "contact_phone",
                        "contact:email": "contact_email",
                        "contact:website": "contact_website",
                        "wheelchair": lambda fields: {"true": "yes", "false": "no"}.get(fields["wheelchair"]),
                        "takeaway": lambda fields: {"true": "yes", "false": "no"}.get(fields["takeaway"]),
                        "official_name": "label"},
                text = lambda tags, fields: {"en": "{} - {} {} - {}".format(fields["street_address"], fields["postalcode_address"], fields["city_address"], fields["elem"])} )))


# the csv data is generated with the following request:
sparql = """
SELECT
  ?elem ?type ?label
  ?Latitude ?Longitude ?street_address ?postalcode_address ?city_address
  ?wheelchair ?takeaway ?contact_phone ?contact_email ?contact_website
WHERE {
  ?elem <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type;
      <http://www.w3.org/2000/01/rdf-schema#label> ?label;
      <https://www.datatourisme.gouv.fr/ontology/core#isLocatedAt> ?location.

  FILTER (?type IN (
    <https://www.datatourisme.gouv.fr/ontology/core#Camping>,
    <https://www.datatourisme.gouv.fr/ontology/core#Church>,
    <https://www.datatourisme.gouv.fr/ontology/core#Restaurant>,
    <https://www.datatourisme.gouv.fr/ontology/core#LocalTouristOffice>
  )).

  ?location <http://schema.org/geo> ?geo.
  ?geo <http://schema.org/latitude> ?Latitude;
      <http://schema.org/longitude> ?Longitude.

  ?location <http://schema.org/address> ?address.
  ?address <http://schema.org/streetAddress> ?street_address;
      <http://schema.org/postalCode> ?postalcode_address;
      <http://schema.org/addressLocality> ?city_address.

  OPTIONAL {
    ?elem <https://www.datatourisme.gouv.fr/ontology/core#hasBookingContact> ?agent_contact.
    ?agent_contact <http://schema.org/telephone> ?contact_phone.
  }
  OPTIONAL {
    ?elem <https://www.datatourisme.gouv.fr/ontology/core#hasBookingContact> ?agent_contact.
    ?agent_contact <http://schema.org/email> ?contact_email.
  }
  OPTIONAL {
    ?elem <https://www.datatourisme.gouv.fr/ontology/core#hasBookingContact> ?agent_contact.
    ?agent_contact <http://xmlns.com/foaf/0.1/homepage> ?contact_website.
  }
  OPTIONAL {
    ?elem <https://www.datatourisme.gouv.fr/ontology/core#reducedMobilityAccess> ?wheelchair.
  }
  OPTIONAL {
    ?elem <https://www.datatourisme.gouv.fr/ontology/core#takeAway> ?takeaway.
  }
}
"""
