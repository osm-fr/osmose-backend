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
from .Analyser_Merge import Analyser_Merge_Point, SourceOpenDataSoft, CSV, Load_XY, Conflate, Select, Mapping
from .Analyser_Merge_Geocode_FR_City_CSV import Geocode_FR_City_CSV
from modules import Stablehash


class Analyser_Merge_Power_Plant_FR(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8270, id = 1, level = 3, tags = ['merge', 'power', 'fix:survey', 'fix:imagery'],
            title = T_('Power plant not integrated, geocoded at municipality level'))

        self.init(
            "https://opendata.reseaux-energies.fr/explore/dataset/registre-national-installation-production-stockage-electricite-agrege",
            "Registre national des installations de production d'électricité et de stockage",
            CSV(Geocode_FR_City_CSV(
                SourceOpenDataSoft(
                    attribution="data.gouv.fr:RTE",
                    url="https://opendata.reseaux-energies.fr/explore/dataset/registre-national-installation-production-stockage-electricite-agrege"),
                citycode='codeINSEECommune', logger = logger)),
            Load_XY("longitude", "latitude",
                where = lambda res: res["puisMaxRac"] and float(res["puisMaxRac"]) >= 250 and res["nomInstallation"] != "Agrégation des installations de moins de 36KW",
                map = lambda res: dict(res, **{"_geom": [
                    res["_geom"][0] is not None and (float(res["_geom"][0]) + (Stablehash.stablehash(str(res)) % 200 - 100) * 0.00001),
                    res["_geom"][1] is not None and (float(res["_geom"][1]) + (Stablehash.stablehash(str(res)) % 212 - 106) * 0.00001)] }),
                unique = ("codeEICResourceObject",)),
            Conflate(
                select = Select(
                    types = ["ways", "relations"],
                    tags = {"power": "plant"}),
                conflationDistance = 5000,
                osmRef = "ref:EU:ENTSOE_EIC",
                tag_keep_multiple_values = ["voltage"],
                mapping = Mapping(
                    static1 = {
                        "power": "plant"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:EU:ENTSOE_EIC": lambda fields: fields["codeEICResourceObject"],
                        # No voltage, frequency, phases tags on power=plant
                        #"voltage": lambda fields: (int(fields["Tension raccordement"].split(' ')[0]) * 1000) if fields["Tension raccordement"] and fields["Tension raccordement"] not in ["< 45 kV", "BT", "HTA"] else None,
                        "plant:source": lambda fields: self.filiere[fields["filiere"]][fields["combustible"]],
                        "plant:output:electricity": lambda fields: None if not fields["puisMaxRac"] else str(float(fields["puisMaxRac"]) / 1000).rstrip(".0") + " MW"},
                    mapping2 = {
                        "start_date": lambda fields: None if not fields["dateMiseEnService"] else fields["dateMiseEnService"][6:10] if fields["dateMiseEnService"].startswith('01/01/') or fields["dateMiseEnService"].startswith('31/12/') else '-'.join(fields["dateMiseEnService"].split('/')[::-1]) },
                    text = lambda tags, fields: T_("Power plant {0}", ', '.join(filter(lambda res: res and res != 'None', [fields["nomInstallation"] if fields["nomInstallation"] != 'Confidentiel' else None, fields["commune"]]))) )))

    filiere = {
        "Autre": {
            None: "",
            "Gaz": "",
            "Fioul": "oil",
        },
        "Bioénergies": {
            None: "",
            "Biogaz de station d'épuration": "biogas",
            "Bois": "biomass",
            "Déchets industriels": "waste",
            "Déchets ménagers": "waste", # For RTE waste is bio-power!
            "Déchets papeterie": "biomass",
            "Gaz": "biogas",
        },
        "Energies Marines": {None: ""},
        "Eolien": {None: "wind"},
        "Géothermie": {None: "geothermal"},
        "Hydraulique": {None: "hydro"},
        "Nucléaire": {"Uranium": "nuclear"},
        "Solaire": {None: "solar"},
        "Stockage non hydraulique": { None: ""},
        "Thermique non renouvelable": {
            None: "",
            "Charbon": "coal",
            "Déchets ménagers": "waste",
            "Fioul": "oil",
            "Gaz": "gas"},
    }
