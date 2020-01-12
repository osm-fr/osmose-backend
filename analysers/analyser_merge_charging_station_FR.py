#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
##                                                                                                                                    ##
## Copyrights Noémie Lehuby 2020                                                                      ##
##                                                                                                                                    ##
## This program is free software: you can redistribute it and/or modify     ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or          ##
## (at your option) any later version.                                                                    ##
##                                                                                                                                    ##
## This program is distributed in the hope that it will be useful,                  ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See     ##
## the GNU General Public License for more details.                                        ##
##                                                                                                                                    ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                                                                                    ##
###########################################################################

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Charging_station_FR(Analyser_Merge):
    def __init__(self, config, logger=None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item=9990, id=1, level=3, tags=['merge'],
                                               title=T_('Car charging station not integrated'))
        self.possible_merge = self.def_class(item=9991, id=3, level=3, tags=['merge'],
                                             title=T_('Car charging station integration suggestion'))
        self.update_official = self.def_class(item=9992, id=4, level=3, tags=['merge'],
                                              title=T_('Car charging station update'))

        self.init(
            u"https://transport.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/",
            u"Stations de recharge pour véhicules électriques",
            CSV(Source(attribution=u"data.gouv.fr:Etalab", millesime="01/2020",
                       fileUrl=u"https://raw.githubusercontent.com/Jungle-Bus/ref-fr-IRVE/gh-pages/opendata_stations.csv")),
            Load("Xlongitude", "Ylatitude"),
            Mapping(
                select=Select(
                    types=["nodes", "ways"],
                    tags={"amenity": "charging_station"}),
                conflationDistance=100,
                osmRef="ref:FR:IRVE",
                generate=Generate(
                    static1={
                        "amenity": "charging_station",
                        "car": "yes"},
                    mapping1={
                        "operator": "n_operateur",
                        "network": "n_enseigne",
                        "owner": "n_amenageur",
                    },
                    mapping2={
                        # "source": "source_grouped",
                        "capacity": "nbre_pdc",
                        "name": "n_station",
                        "socket:type2_combo": lambda fields: fields["nb_combo_grouped"] if fields["nb_combo_grouped"] != "0" else None,
                        "socket:type2": lambda fields: fields["nb_T2_grouped"] if fields["nb_T2_grouped"] != "0" else None,
                        "socket:chademo": lambda fields: fields["nb_chademo_grouped"] if fields["nb_chademo_grouped"] != "0" else None,
                        "socket:typee": lambda fields: fields["nb_EF_grouped"] if fields["nb_EF_grouped"] != "0" else None,
                        "socket:type3": lambda fields: fields["nb_T3_grouped"] if fields["nb_T3_grouped"] != "0" else None,
                        "fee": lambda fields: guess_fee(fields["acces_recharge_grouped"]),
                        "opening_hours": lambda fields: guess_opening_hours(fields["accessibilité_grouped"]),
                    },
                    text=lambda tags, fields: {"en": u"%s, %s" % (fields["n_station"], fields["ad_station"])})))

        def guess_fee(text_fee):
            if "payant" in text_fee.lower():
                return "yes"
            if "gratuit" in text_fee.lower():
                return "no"
            if "€" in text_fee:
                return "yes"
            return None

        def guess_opening_hours(text_opening_hours):
            if "24/24" in text_opening_hours:
                return "24/7"
            if "24h/24" in text_opening_hours:
                return "24/7"
            return None
