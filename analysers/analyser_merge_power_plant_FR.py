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

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping
from .Analyser_Merge_Geocode_Addok_CSV import Geocode_Addok_CSV
from modules import Stablehash


class Analyser_Merge_Power_Plant_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8270, id = 1, level = 3, tags = ['merge', 'power'],
            title = T_('Power plant not integrated, geocoded at municipality level'))

        self.init(
            u"https://opendata.reseaux-energies.fr/explore/dataset/registre-national-installation-production-stockage-electricite-agrege-311217",
            u"Registre national des installations de production d'électricité et de stockage",
            CSV(Geocode_Addok_CSV(
                SourceOpenDataSoft(
                    attribution="data.gouv.fr:RTE",
                    base_url="https://opendata.reseaux-energies.fr",
                    dataset="registre-national-installation-production-stockage-electricite-agrege-311217"),
                columns='commune', citycode='codeINSEEcommune', logger=logger)),
            Load("longitude", "latitude",
                where = lambda res: res.get('puisMaxRac') and float(res["puisMaxRac"]) > 1000,
                map = lambda res: dict(res, **{"_x": float(res["_x"]) + (Stablehash.stablehash(str(res)) % 200 - 100) * 0.00001, "_y": float(res["_y"]) + (Stablehash.stablehash(str(res)) % 212 - 106) * 0.00001})),
            Conflate(
                select = Select(
                    types = ["ways", "relations"],
                    tags = {"power": "plant"}),
                conflationDistance = 5000,
                tag_keep_multiple_values = ["voltage"],
                mapping = Mapping(
                    static1 = {
                        "power": "plant"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        # No voltage tga on power=plant
                        #"voltage": lambda fields: (int(fields["Tension raccordement"].split(' ')[0]) * 1000) if fields.get("Tension raccordement") and fields["Tension raccordement"] not in ["< 45 kV", "BT", "HTA"] else None,
                        "plant:source": lambda fields: self.filiere[fields["filiere"]][fields["combustible"]],
                        "plant:output:electricity": lambda fields: int(float(fields["puisMaxRac"]) * 1000)},
                    mapping2 = {
                        "start_date": lambda fields: None if not fields.get(u"dateMiseEnService") else fields[u"dateMiseEnService"][0:4] if fields[u"dateMiseEnService"].endswith('-01-01') or fields[u"dateMiseEnService"].endswith('-12-31') else fields[u"dateMiseEnService"]},
                    text = lambda tags, fields: T_("Power plant {0}", ', '.join(filter(lambda res: res and res != 'None', [fields["nomInstallation"], fields["commune"]]))) )))

    filiere = {
        u"Autre": {
            None: "",
            u"Gaz": "",
        },
        u"Bioénergies": {
            None: "",
            u"Biogaz de station d'épuration": "biogas",
            u"Bois": "biomass",
            u"Déchets ménagers": "waste", # For RTE waste is bio-power!
            u"Déchets papeterie": "biomass",
            u"Gaz": "biogas",
        },
        u"Energies Marines": {None: ""},
        u"Eolien": {None: "wind"},
        u"Géothermie": {None: "geothermal"},
        u"Hydraulique": {None: "hydro"},
        u"Nucléaire": {"Uranium": "nuclear"},
        u"Solaire": {None: "solar"},
        u"Thermique non renouvelable": {
            None: "",
            u"Charbon": "coal",
            u"Fioul": "oil",
            u"Gaz": "gas"},
     }
