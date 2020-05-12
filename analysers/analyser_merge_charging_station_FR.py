#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


class Analyser_Merge_Charging_station_FR(Analyser_Merge):
    def __init__(self, config, logger=None):
        Analyser_Merge.__init__(self, config, logger)
        doc = dict(
            detail = T_(
'''A car charging station may be here but is not mapped. The list of the
charging stations comes from a database published by Etalab. This database
brings together information published by the various local authorities and
networks in France.'''),
            fix = T_(
'''See [the
mapping](https://wiki.openstreetmap.org/wiki/France/data.gouv.fr/Bornes_de_Recharge_pour_V%C3%A9hicules_%C3%89lectriques)
on the  wiki. Add a node or add tags if already existing.'''),
            trap = T_(
'''The initial information corresponds to recharging pools and devices and not to
stations, so some values are worth checking in the field. For instance, an open data point
with `capacity=6` can sometimes match to 3 charging station with `capacity=2`'''))
        self.def_class_missing_official(item = 8410, id = 1, level = 3, tags = ['merge'],
            title = T_('Car charging station not integrated'), **doc)
        self.def_class_possible_merge(item = 8411, id = 3, level = 3, tags = ['merge'],
            title = T_('Car charging station, integration suggestion'), **doc)
        self.def_class_update_official(item = 8412, id = 4, level = 3, tags = ['merge'],
            title = T_('Car charging station  update'), **doc)

        self.init(
            "https://transport.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/",
            "Stations de recharge pour véhicules électriques",
            CSV(Source(attribution="data.gouv.fr:Etalab", millesime="01/2020",
                       fileUrl="https://raw.githubusercontent.com/Jungle-Bus/ref-EU-EVSE/gh-pages/opendata_stations.csv")),
            Load("Xlongitude", "Ylatitude"),
            Mapping(
                select=Select(
                    types=["nodes", "ways"],
                    tags={"amenity": "charging_station"}),
                conflationDistance=100,
                osmRef="ref:EU:EVSE",
                generate=Generate(
                    static1={
                        "amenity": "charging_station",
                        "motorcar": "yes"},
                    mapping1={
                        "operator": "n_operateur",
                        "network": "n_enseigne",
                        "owner": "n_amenageur",
                        "ref:EU:EVSE": "id_station"
                    },
                    mapping2={
                        # "source": "source_grouped",
                        "capacity": "nbre_pdc",
                        #"name": "n_station",
                        "socket:type2_combo": lambda fields: fields["nb_combo_grouped"] if fields["nb_combo_grouped"] != "0" else None,
                        "socket:type2": lambda fields: fields["nb_T2_grouped"] if fields["nb_T2_grouped"] != "0" else None,
                        "socket:chademo": lambda fields: fields["nb_chademo_grouped"] if fields["nb_chademo_grouped"] != "0" else None,
                        "socket:typee": lambda fields: fields["nb_EF_grouped"] if fields["nb_EF_grouped"] != "0" else None,
                        "socket:type3c": lambda fields: fields["nb_T3c_grouped"] if fields["nb_T3c_grouped"] != "0" else None,
                        "fee": lambda fields: guess_fee(fields["acces_recharge_grouped"]),
                        "opening_hours": lambda fields: guess_opening_hours(fields["accessibilité_grouped"]),
                    },
                    text=lambda tags, fields: {"en": "%s, %s" % (fields["n_station"], fields["ad_station"])})))

        def guess_fee(text_fee):
            if text_fee is None:
                return None
            if "payant" in text_fee.lower():
                return "yes"
            if "gratuit" in text_fee.lower():
                return "no"
            if "€" in text_fee:
                return "yes"
            return None

        def guess_opening_hours(text_opening_hours):

            if text_opening_hours is None:
                return None
            if "24/24" in text_opening_hours:
                return "24/7"
            if "24h/24" in text_opening_hours:
                return "24/7"
            return None
