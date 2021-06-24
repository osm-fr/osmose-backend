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
import re

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, GTFS, Load, Conflate, Select, Mapping, Source


class Analyser_Merge_Public_Transport_FR_zou_06(Analyser_Merge):

    CITY_NAME_EXTRACT_REGEX = r"^(?P<stop>.*(?<!R|A)) (?:(?:- [R|A] )?)- (?P<city>[[A-Z]+(?:[ -\/.][A-Z]*)*)$"

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        place = "Zou 06"
        self.def_class_missing_official(item = 8040, id = 41, level = 3, tags = ['merge', 'public transport', 'fix:survey', 'fix:picture'],
            title = T_('{0} stop not integrated', place))
        self.def_class_possible_merge(item = 8041, id = 43, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop, integration suggestion', place))
        self.def_class_update_official(item = 8042, id = 44, level = 3, tags = ['merge', 'public transport', 'fix:chair'],
            title = T_('{0} stop update', place))

        self.init(
            "https://trouver.datasud.fr/dataset/lignes-autocars-interurbains-regionsud/resource/db4be056-c7e8-4efb-8299-4b8c6235defe",
            "Export quotidien au format GTFS sur du réseau des lignes d'autocars interurbains"
            " de la Région Sud Provence-Alpes-Côte d'Azur dans les Alpes-Maritimes (06)",
            GTFS(Source(attribution = "Région Sud - DataSud", millesime = "01/2022",
                        fileUrl = "https://trouver.datasud.fr/dataset/44187c20-e037-4733-950a-b4463d314b90/resource/db4be056-c7e8-4efb-8299-4b8c6235defe/download/gtfs_06.zip")),
            Load("stop_lon", "stop_lat",
                 #select = {"location_type": '0', "stop_code": True},
                 ),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"highway": "bus_stop"}),
                osmRef = "ref:FR:RLA",
                conflationDistance = 50,
                mapping = Mapping(
                    static1 = {
                        "highway": "bus_stop",
                        "public_transport": "platform",
                        "bus": "yes"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:ZOU_06": lambda res: res["stop_id"].split(':')[-1],
                        # If stop_code is defined, the platform belongs to the Lignes d'Azur network,
                        # else it belongs generally to the ZOU (Région Sud) network, which some old
                        # Lignes d'Azur / TAM lines have been transferred to (lines 100 and 200 for example)
                        # If stop_name contains an upper case name, it's the station city name
                        "name": lambda res: self.extract_name(res['stop_name'])[0],
                        "addr:city": lambda res: self.extract_name(res['stop_name'])[1],
                    },
                    text = lambda tags, fields: T_(f"{place} stop of {fields['stop_name']}")))
            )

    def extract_name(self, stop_name):
        match = re.match(self.CITY_NAME_EXTRACT_REGEX, stop_name)
        if match:
            return match.group("stop") if not match.group("stop").isupper() else match.group("stop").title(),\
                   self.replace(match.group("city"))
        return stop_name.title(), None


    def replace(self, string):
        if string in self.replacement:
            return self.replacement[string]
        return string.title()

    replacement = {
        'AURIBEAU/SIAGNE': 'Auribeau-sur-Siagne',
        'BEAULIEU / MER': 'Beaulieu-sur-Mer',
        'BEZAUDUN/ ALPES': 'Bezaudun-les-Alpes',
        'CAP D AIL': "Cap d'Ail",
        'CHATNEUF-GRASSE': 'Châteauneuf-Grasse',
        'COLLE SUR LOUP': 'La Colle-sur-Loup',
        'EZE': 'Èze',
        'GREOLIERES': 'Gréolières',
        'LE BAR SUR LOUP': 'Le Bar-sur-Loup',
        'L ESCARENE': "L'Escarène",
        'REVEST LES ROCH': 'Revest-les-Roches',
        'ROQUEBRUNE CAP': 'Roquebrune-Cap-Martin',
        'ROQUEFT-LS-PINS': 'Roquefort-les-Pins',
        'ROQUETTE/SIAGNE': "La Roquette-sur-Siagne",
        'ROQUETTE/VAR': 'La Roquette-sur-Var',
        'S.LAURENT-D-VAR': 'Saint-Laurent-du-Var',
        'ST BENOIT': 'Saint-Benoît',
        'ST-MARTIN-D.VAR': 'Saint-Martin-du-Var',
        'ST-MT-ENTRAUNES': "Saint-Martin-d'Entraunes",
        'ST PAUL DE VENC': 'Saint-Paul-de-Vence',
        'TOUET-ESCARENE': "Touët-de-l'Escarène",
        'TOUET SUR VAR': 'Touët-sur-Var',
        'TOURETTE DU CHT': 'Tourette-du-Château',
        'TOURRETTES/LOUP': 'Tourrettes-sur-Loup',
        'VILLARS SUR VAR': 'Villars-sur-Var',
        'VILLEFRANCH/MER': 'Villefranche-sur-Mer',
        'VILLENEUVE-LBT': 'Villeneuve-Loubet',
        'VLNVE-ENTRAUNES': "Villeneuve-d'Entraunes"
    }
