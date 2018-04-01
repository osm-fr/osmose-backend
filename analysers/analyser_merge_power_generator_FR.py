#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate


class Analyser_Merge_Power_Generator_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8270", "class": 1, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power generator not integrated") }
        self.missing_osm      = {"item":"7180", "class": 2, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power generator without ref:FR:RTE") }
        self.possible_merge   = {"item":"8271", "class": 3, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power generator, integration suggestion") }
        self.update_official  = {"item":"8272", "class": 4, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power generator update") }

        Analyser_Merge.__init__(self, config, logger,
            "https://opendata.rte-france.com/explore/dataset/registre_parc_prod_rpt",
            u"Registre 2015 des installations de production raccordées au Réseau de Transport d'Electricité",
            CSV(Source(attribution = u"data.gouv.fr:RTE", millesime = "2015",
                    fileUrl = "https://opendata.rte-france.com/explore/dataset/registre_parc_prod_rpt/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true"),
                separator = ";"),
            Load("Geo-point IRIS", "Geo-point IRIS",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Mapping(
                select = Select(
                    types = ["ways"],
                    tags = {"power": "generator"}),
                conflationDistance = 5000,
                generate = Generate(
                    static1 = {
                        "power": "generator"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:RTE": "Identifiant",
                        "voltage": lambda fields: (int(float(fields["Tension (kV)"]) * 1000)) if fields.get("Tension (kV)") and fields["Tension (kV)"] != "<45" else None,
                        "generator:source": lambda fields: self.filiere[fields["Filière"]][fields["Combustible"]],
                        "generator:output:electricity": lambda fields: (int(float(fields["Puissance maximale (MW)"]) * 1000000)) if fields.get("Puissance maximale (MW)") else None},
                    mapping2 = {
                        "start": lambda fields: fields[u"Date de mise en service"][0:4] if fields[u"Date de mise en service"].endswith('-01-01') or fields[u"Date de mise en service"].endswith('-12-31') else fields[u"Date de mise en service"],
                        "operator": "Exploitant"},
                   tag_keep_multiple_values = ["voltage"],
                   text = lambda tags, fields: T_(u"Power substation of %s", fields["Site de production"]))))

    filiere = {
        u"Eolien": {"n.a.": "wind"},
        u"Bioénergie": {
            u"Déchets papèterie, liqueur noire…": "biomass",
            u"Biomasse (Bois et dérivés, marc de raisin…)": "biomass",
            #"": "biofuel",
            u"Biogaz, gaz de décharge, gaz de station d'épuration…": "biogas",
            u"Déchets ménagers": "waste"}, # For RTE waste is bio-power!
        u"Nucléaire": {"n.a.": "nuclear"},
        u"Solaire": {"n.a.": "solar"},
        u"Thermique fossile": {
            u"Gaz ou excédent de vapeur": None,
            u"Gaz de haut fourneau": None,
            u"Fioul (divers)": "oil",
            u"Fioul lourd": "oil",
            #"": "diesel",
            u"Fioul distillé": "gasoline",
            u"Fioul domestique": "gasoline",
            u"Gaz naturel": "gaz",
            u"Gaz de raffinerie": "gaz",
            u"Charbon (divers)": "coal",
            u"Charbon marchand": "coal"},
        u"Hydraulique": {"n.a.": "hydro"}
    }
