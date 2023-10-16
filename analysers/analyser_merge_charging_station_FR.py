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

from modules.OsmoseTranslation import T_
from .formatters.IRVEChecker import IRVE_checker
from .Analyser_Merge import Analyser_Merge_Point, Source, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Charging_station_FR(Analyser_Merge_Point):
    def __init__(self, config, logger=None):
        Analyser_Merge_Point.__init__(self, config, logger)
        doc = dict(
            detail=T_(
                '''A car charging station may be here but is not mapped. The list of the
                charging stations comes from a database published by Etalab. This database
                brings together information published by the various local authorities and
                networks in France.'''),
            fix=T_(
                '''See [the
                mapping](https://wiki.openstreetmap.org/wiki/France/data.gouv.fr/Bornes_de_Recharge_pour_V%C3%A9hicules_%C3%89lectriques)
                on the  wiki. Add a node or add tags if already existing.'''),
            trap=T_(
                '''The initial information corresponds to recharging pools and devices and not to
                stations, so some values are worth checking in the field. For instance, an open data point
                with `capacity=6` can sometimes match to 3 charging station with `capacity=2`'''))
        self.def_class_missing_official(item=8410, id=1, level=3,
                                        tags=['merge', 'fix:imagery', 'fix:survey', 'fix:picture'],
                                        title=T_('Car charging station not integrated'), **doc)
        self.def_class_possible_merge(item=8411, id=3, level=3,
                                      tags=['merge', 'fix:imagery', 'fix:survey', 'fix:picture'],
                                      title=T_('Car charging station, integration suggestion'), **doc)
        self.def_class_update_official(item=8412, id=4, level=3,
                                       tags=['merge', 'fix:imagery', 'fix:survey', 'fix:picture'],
                                       title=T_('Car charging station update'), **doc)




self.init(
    "https://transport.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/",
    "Stations de recharge pour véhicules électriques",
    CSV(Source(attribution="data.gouv.fr:Etalab", millesime="05/2022",
               fileUrl="https://raw.githubusercontent.com/Jungle-Bus/ref-EU-EVSE/gh-pages/opendata_stations.csv")),
    Load_XY("Xlongitude", "Ylatitude"),
    Conflate(
        select=Select(
            types=["nodes", "ways"],
            tags={"amenity": "charging_station"}),
        conflationDistance=100,
        osmRef="ref:EU:EVSE",
        mapping=Mapping(
            static1={
                "amenity": "charging_station",
                "motorcar": "yes"},
            static2={"source": self.source},
            mapping1={
                "operator": "nom_operateur",
                "network": "nom_enseigne",
                "owner": "nom_amenageur",
                "ref:EU:EVSE": "id_station_itinerance"
            },
            mapping2={
                "email": "contact_operateur",
                "operator:phone": "telephone_operateur",
                "operator:email": "contact_operateur",
                "start_date": "date_mise_en_service",
                "capacity": "nbre_pdc",
                "charging_station:output": lambda fields: IRVE_checker.socket_output_find_correspondances(fields['puissance_nominale']) if fields["puissance_nominale"] else None,
                "bicycle": lambda fields: "yes" if fields["station_deux_roues"] == "true" else None,
                "motorcycle": lambda fields: "yes" if fields["station_deux_roues"] == "true" else None,
                "moped": lambda fields: "yes" if fields["station_deux_roues"] == "true" else None,
                "motorcar": lambda fields: "no" if fields["station_deux_roues"] == "true" else "yes",
                "opening_hours": "horaires_grouped",
                "fee": lambda fields: "yes" if fields["gratuit_grouped"] == "false" else (
                    "no" if fields["gratuit_grouped"] == "true" else None),
                "authentication:none": lambda fields: "yes" if fields["paiement_acte_grouped"] == "true" else None,
                "payment:credit_cards": lambda fields: "yes" if fields["paiement_cb_grouped"] == "true" else (
                    "no" if fields["paiement_cb_grouped"] == "false" else None),
                "reservation": lambda fields: "yes" if fields["reservation_grouped"] == "true" else None,
                "wheelchair": lambda fields: "yes" if fields[
                                                          "accessibilite_pmr_grouped"] == "Accessible mais non réservé PMR" else (
                    "no" if fields["accessibilite_pmr_grouped"] == "Non accessible" else None),
                "socket:typee": lambda fields: fields["nb_EF_grouped"] if fields["nb_EF_grouped"] != "0" else None,
                "socket:type2": lambda fields: fields["nb_T2_grouped"] if fields["nb_T2_grouped"] != "0" else None,
                "socket:type2_cable": lambda fields: fields["cable_t2_attache"] if fields[
                                                                                       "cable_t2_attache"] == "1" else None,
                "socket:type2_combo": lambda fields: fields["nb_combo_ccs_grouped"] if fields[
                                                                                           "nb_combo_ccs_grouped"] != "0" else None,
                "socket:chademo": lambda fields: fields["nb_chademo_grouped"] if fields[
                                                                                     "nb_chademo_grouped"] != "0" else None
            },
            text=lambda tags, fields: {"en": "{0}, {1}, {2}".format(fields["nom_station"], fields["adresse_station"],
                                                                    fields["observations"] if fields[
                                                                                                  "observations"] != "null" else "-")})))
