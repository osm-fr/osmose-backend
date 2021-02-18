#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien Pavie 2020                                          ##
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
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Conflate, Select, Mapping
import unidecode
import re
from modules import reaccentue

class Analyser_merge_defibrillators_FR(Analyser_Merge):
    def normalizeEtage(self, etg):
        if etg is None:
            return None
        else:
            etg = unidecode.unidecode(etg.lower().replace("-", "").replace(".", "").replace(" ", ""))
            if etg == "0":
                return None
            elif etg in ["rezdechaussee", "rezdechausse", "reddechaussee", "rdc"]:
                return "0"
            elif re.compile(r"^r\+\d$").match(etg):
                return etg[2:]
            elif re.compile(r"^niveau -?\d+$").match(etg):
                return etg[7:]
            elif re.compile(r"^-?\d+ e.*$").match(etg):
                return etg.split(" ")[0]
            elif re.compile(r"^-?\d+e.*$").match(etg):
                return etg.split("e")[0]
            elif re.compile(r"^-?\d+$").match(etg):
                return etg
            else:
                return None

    def normalizeHours(self, jours, heures):
        if jours == "{7j/7}" and heures == "{24h/24}":
            return "24/7"
        else:
            return None

    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8370, id = 120, level = 3, tags = ["merge", "emergency", "fix:picture", "fix:survey"],
            title = T_("Defibrillator not integrated"),
            trap = T_("Location of defibrillators from this dataset can be very approximative. Check carefully the position before adding to OSM."))

        self.init(
            "https://geo.data.gouv.fr/fr/datasets/a701db3964e8fd81823c92afc029f138ffa207b3",
            "Défibrillateurs de la base nationale GeoDAE",
            CSV(Source(
                attribution="Direction Générale de la Santé",
                fileUrl="https://transcode.geo.data.gouv.fr/services/5e2a1fbefa4268bc25629472/feature-types/ms:geodae_publique?format=CSV&projection=WGS84",
                millesime=None,
            )),
            Load("c_long_coor1", "c_lat_coor1",
                 select = {"c_etat_fonct": "En fonctionnement", "c_doublon": "f"}),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 100,
                mapping = Mapping(
                    static1 = {"emergency": "defibrillator"},
                    mapping1 = {
                        "name": lambda res: reaccentue.reaccentue(res["c_nom"]) if res["c_nom"] and res["c_acc_complt"] else None,
                        "indoor": lambda res: "yes" if res["c_acc"] == "Intérieur" else "no" if res["c_acc"] == "Extérieur" else None,
                        "access": lambda res: "yes" if res["c_acc_lib"] == "t" else "permissive" if res["c_acc_lib"] == "f" else None,
                        "security_desk": lambda res: "yes" if res["c_acc_pcsec"] == "t" else "no" if res["c_acc_pcsec"] == "f" else None,
                        "reception_desk": lambda res: "yes" if res["c_acc_acc"] == "t" else "no" if res["c_acc_acc"] == "f" else None,
                        "level": lambda res: self.normalizeEtage(res["c_acc_etg"]),
                        "defibrillator:location": lambda res: res["c_acc_complt"] if "c_acc_complt" in res else reaccentue.reaccentue(res["c_nom"]) if res["c_nom"] else None,
                        "opening_hours": lambda res: self.normalizeHours(res["c_disp_j"], res["c_disp_h"]),
                        "start_date": "c_date_instal|timePosition",
                        "operator:ref:FR:SIREN": lambda res: res["c_expt_siren"] if "c_expt_siren" in res else None,
                        "operator": lambda res: reaccentue.reaccentue(res["c_expt_rais"]) if "c_expt_rais" in res else None,
                        "source": lambda res: ("Direction Générale de la Santé - " + res["c__edit_datemaj|timePosition"].split("T")[0]),
                    },
                    text = lambda tags, fields: {"en": " - ".join(filter(lambda x: x, [
                        "POSITION APPROXIMATIVE À VÉRIFIER" if fields["c_etat_valid"] == "en attente de validation" else None,
                        fields["c_nom"],
                        "Horaires : "+fields["c_disp_j"][1:-1]+" "+fields["c_disp_h"][1:-1] if fields["c_disp_j"] and fields["c_disp_h"] else None,
                        " ".join(filter(lambda x: x, [
                            fields["c_adr_num"],
                            fields["c_adr_voie"],
                            fields["c_com_cp"],
                            fields["c_com_nom"]
                        ]))
                    ]))} )))
