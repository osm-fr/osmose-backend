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

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate
import unidecode
import re
from modules import reaccentue

class Analyser_merge_defibrillators_FR(Analyser_Merge):
    def normalizeEtage(self, etg):
        if etg is None:
            return None
        else:
            etg = unidecode.unidecode(etg.lower().replace("-", "").replace(".", "").replace(" ", ""))
            if etg in ["rezdechaussee", "rezdejardin", "rezdechausse", "rez", "red-de-chaussee", "rdc", "rdj"]:
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
        self.def_class_missing_official(item = 8370, id = 120, level = 3, tags = ["merge"],
            title = T_("Defibrillator not integrated"))

        self.init(
            u"https://geo.data.gouv.fr/fr/datasets/a701db3964e8fd81823c92afc029f138ffa207b3",
            u"Défibrillateurs de la base nationale GeoDAE",
            CSV(Source(attribution = u"Direction Générale de la Santé",
                    fileUrl = u"https://transcode.geo.data.gouv.fr/services/5e2a1fbefa4268bc25629472/feature-types/ms:geodae_publique?format=CSV&projection=WGS84")),
            Load("c_long_coor1", "c_lat_coor1",
                 select = {"c_etat_fonct": u"En fonctionnement", "c_doublon": u"f"}),
            Mapping(
                select = Select(
                    types = ["nodes"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                osmRef = "ref:FR:GeoDAE",
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:GeoDAE": "c_gid",
                        "name": lambda res: reaccentue.reaccentue(res["c_nom"]) if res["c_nom"] else None,
                        "indoor": lambda res: "yes" if res["c_acc"] == u"Intérieur" else "no" if res["c_acc"] == u"Extérieur" else None,
                        "access": lambda res: "yes" if res["c_acc_lib"] == "t" else "permissive" if res["c_acc_lib"] == "f" else None,
                        "security_desk": lambda res: "yes" if res["c_acc_pcsec"] == "t" else "no" if res["c_acc_pcsec"] == "f" else None,
                        "reception_desk": lambda res: "yes" if res["c_acc_acc"] == "t" else "no" if res["c_acc_acc"] == "f" else None,
                        "level": lambda res: self.normalizeEtage(res["c_acc_etg"]),
                        "defibrillator:location": "c_acc_complt",
                        "opening_hours": lambda res: self.normalizeHours(res["c_disp_j"], res["c_disp_h"]),
                        "surveillance": lambda res: "yes" if res["c_dispsurv"] == "t" else "no" if res["c_dispsurv"] == "f" else None,
                        "start_date": "c_date_instal|timePosition",
                        "ref:FR:SIREN": "c_expt_siren",
                        "operator": lambda res: reaccentue.reaccentue(res["c_expt_rais"]) if res["c_expt_rais"] else None
                    },
                    text = lambda tags, fields: {"en": " - ".join(filter(lambda x: x, [
                        u"POSITION APPROXIMATIVE À VÉRIFIER" if fields["c_etat_valid"] == u"en attente de validation" else None,
                        fields["c_nom"],
                        "Horaires : "+fields["c_disp_j"][1:-1]+" "+fields["c_disp_h"][1:-1] if fields["c_disp_j"] and fields["c_disp_h"] else None
                    ]))} )))
