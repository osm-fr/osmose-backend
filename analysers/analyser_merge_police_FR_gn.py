#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
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

from modules.OsmoseTranslation import T_
from collections import OrderedDict
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Police_FR_gn(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8190, id = 1, level = 3, tags = ['merge', 'amenity', 'fix:survey', 'fix:picture'],
            title = T_('Police/"Gendarmerie" not integrated'))
        self.def_class_possible_merge(item = 8191, id = 3, level = 3, tags = ['merge', 'amenity', 'fix:chair'],
            title = T_('Police/"Gendarmerie", integration suggestion'))
        self.def_class_update_official(item = 8192, id = 4, level = 3, tags = ['merge', 'amenity', 'fix:picture', 'fix:survey'],
            title = T_('Police/"Gendarmerie" update'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/liste-des-unites-de-gendarmerie-accueillant-du-public-comprenant-leur-geolocalisation-et-leurs-horaires-douverture/",
            "Liste des points d'accueil de la gendarmerie nationale",
            CSV(
                SourceDataGouv(
                    attribution="data.gouv.fr:Ministère de l'Intérieur",
                    dataset="5369993fa3a729239d2051cd",
                    resource="d6a43ef2-d302-4456-90e9-ff2c47cac562"),
                separator = ";"),
            Load_XY("geocodage_x_GPS", "geocodage_y_GPS",
                where = lambda row: "Centre d'information et de recrutement" not in row["service"] and "motorisé" not in row["service"] ),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "police"}),
                conflationDistance = 500,
                osmRef = "ref:FR:GendarmerieNationale",
                mapping = Mapping(
                    static1 = {
                        "amenity": "police",
                        "name": "Gendarmerie nationale",
                        "police:FR": "gendarmerie",
                        "operator:wikidata": "Q1422336",
                        "operator": "Gendarmerie nationale"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:GendarmerieNationale": "identifiant_public_unite",
                        "opening_hours": lambda fields: parse_opening_hours(fields),
                        "seasonal": lambda fields: "yes" if "Poste provisoire" in fields["service"] else None},
                    mapping2 = {
                        "phone": "telephone",
                        "official_name": "service",
                    },
                text = lambda tags, fields: {"en": "{0}, {1}".format(fields["service"], fields["adresse_geographique"])} )))


        OSM_DAYS_FR = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'jours_feries']
        OSM_DAYS = OrderedDict(lundi='Mo', mardi='Tu', mercredi='We', jeudi='Th', vendredi='Fr', samedi='Sa', dimanche='Su', jours_feries='PH')

        def parse_opening_hours(line):
            hours_list = []
            for a_day in OSM_DAYS_FR:
                hours = ''
                if line[a_day + '_plage1_fin']:
                    hours += '{}-{}'.format(line[a_day + '_plage1_debut'], line[a_day + '_plage1_fin'])
                if line[a_day + '_plage2_fin']:
                    hours += ',{}-{}'.format(line[a_day + '_plage2_debut'], line[a_day + '_plage2_fin'])
                if line[a_day + '_plage3_fin']:
                    hours += ',{}-{}'.format(line[a_day + '_plage3_debut'], line[a_day + '_plage3_fin'])
                hours_list.append({'hours': hours.replace('h', ':'), 'day': OSM_DAYS[a_day]})

            hours_text = ''
            day_two = 0
            for i in range(7):
                if i < day_two:
                    continue
                current_hours_txt = ''
                for j in range(7):
                    if j < i:
                        continue
                    day_two = j
                    if hours_list[j]['hours'] == hours_list[i]['hours']:
                        if hours_list[j]['hours']:
                            if i == j:
                                current_hours_txt = '{} {}; '.format(hours_list[i]['day'], hours_list[i]['hours'])
                            else:
                                current_hours_txt = '{}-{} {}; '.format(hours_list[i]['day'], hours_list[j]['day'], hours_list[i]['hours'])
                    else:
                        break

                hours_text += current_hours_txt

            if hours_list[7]['hours']:
                hours_text += '{} {}'.format(hours_list[7]['day'], hours_list[7]['hours'])

            if hours_text.endswith('; '):
                hours_text = hours_text[0:-2]

            if not hours_text:
                hours_text = None
            return hours_text
