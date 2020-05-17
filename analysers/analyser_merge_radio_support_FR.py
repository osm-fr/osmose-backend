#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jérôme Amagat 2019                                         ##
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
from io import open

class _Analyser_Merge_Radio_Support_FR(Analyser_Merge):
    def __init__(self, config, logger, clas, NAT_IDs, title, tags_select, tags_generate):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8390, id = 1+10*clas, level = 3, tags = ['merge'],
            title = T_f('Radio support ({0}) not integrated', title))
        self.def_class_possible_merge(item = 8391, id = 3+10*clas, level = 3, tags = ['merge'],
            title = T_f('Radio support ({0}), integration suggestion', title))
        self.def_class_update_official(item = 8392, id = 4+10*clas, level = 3, tags = ['merge'],
            title = T_f('Radio support ({0}) update', title))

        self.communeNameIndexedByInsee = {}
        with open("dictionaries/FR/BddCommunes", "r", encoding="utf-8") as f:
            for x in f:
                x = x.split("\t")
                code_insee = x[0]
                name_insee = x[1].strip()
                self.communeNameIndexedByInsee[code_insee] = name_insee

        self.init(
            u"https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/",
            u"Données sur les installations radioélectriques de plus de 5 watts",
            CSV(Source(attribution = u"data.gouv.fr:ANFR", millesime = "08/2019",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/5da74526-7781-4726-b98b-232756643090", zip = "SUP_SUPPORT.txt", encoding = "ISO-8859-15"),
                separator = u";", quote = u'$'),
            Load(
("CASE \"COR_CD_EW_LON\" WHEN 'W' THEN -1*(to_number(\"COR_NB_DG_LON\", '99') + to_number(\"COR_NB_MN_LON\", '99') / 60 + to_number(\"COR_NB_SC_LON\", '99') / 3600) WHEN 'E' THEN to_number(\"COR_NB_DG_LON\", '99') + to_number(\"COR_NB_MN_LON\", '99') / 60 + to_number(\"COR_NB_SC_LON\", '99') / 3600 END",),
("CASE \"COR_CD_NS_LAT\" WHEN 'S' THEN -1*(to_number(\"COR_NB_DG_LAT\", '99') + to_number(\"COR_NB_MN_LAT\", '99') / 60 + to_number(\"COR_NB_SC_LAT\", '99') / 3600) WHEN 'N' THEN to_number(\"COR_NB_DG_LAT\", '99') + to_number(\"COR_NB_MN_LAT\", '99') / 60 + to_number(\"COR_NB_SC_LAT\", '99') / 3600 END",),
                  select = {"NAT_ID": NAT_IDs},
                  uniq = ("SUP_ID",)),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = tags_select),
                conflationDistance = 50,
                osmRef = "ref:FR:ANFR",
                generate = Generate(
                    static1 = tags_generate,
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:ANFR": "SUP_ID",
                        "operator": lambda fields: self.owner[int(fields["TPO_ID"])] if fields["TPO_ID"] and int(fields["TPO_ID"]) in self.owner else None,
                        "height": lambda fields: fields["SUP_NM_HAUT"].replace(",", ".") if fields["SUP_NM_HAUT"] else None,
                        },
                    text = lambda tags, fields: {"en": u"%s, address: %s, %s%s" % (
                        (lambda x: self.Tour_Mat_Pylone[fields["NAT_ID"]] if x == u"Tour, mât et pylône" else x)(title),
                        ", ".join(filter(lambda x: x != "None", [fields["ADR_LB_LIEU"], fields["ADR_LB_ADD1"], fields["ADR_LB_ADD2"], fields["ADR_LB_ADD3"],fields["ADR_NM_CP"]])),
                        (lambda x: self.communeNameIndexedByInsee[x] if x in self.communeNameIndexedByInsee else x)(fields["COM_CD_INSEE"]),
                        (lambda x: (u", operator: " + self.other_owner[int(x)]) if x and x != "None" and int(x) in self.other_owner else "")(fields["TPO_ID"])
                    )} )))

    # number: column TPO_ID in SUP_SUPPORT.txt and value: SUP_PROPRIETAIRE.txt
    owner = {
        1: u"ANFR",
        4: u"Bouygues",
        10: u"CROSS",
        16: u"Orange Services Fixes",
        19: u"La Poste",
        21: u"Orange",
        24: u"SNCF Réseau",
        25: u"RTE",
        27: u"SFR",
        31: u"Société réunionnaise du radiotéléphone",
        32: u"TDF",
        33: u"Towercast",
        35: u"Voies navigables de France",
        36: u"Altitude Telecom",
        37: u"Antalis",
        38: u"One Cast",
        39: u"Gendarmerie nationale",
        40: u"Tikiphone",
        41: u"France Caraibes Mobiles",
        42: u"IFW-Free",
        43: u"Lagardère Active Média",
        44: u"Outremer Telecom",
        45: u"RATP",
        47: u"Office des Postes et Telecom",
        49: u"Bolloré",
        48: u"Neuf Cegetel",
        50: u"Completel",
        51: u"Digicel",
        52: u"Eutelsat",
        53: u"Expertmedia",
        54: u"Mediaserv",
        55: u"Belgacom",
        56: u"Airbus",
        57: u"Guyane Numérique",
        58: u"Dauphin Telecom",
        59: u"Itas Tim",
        60: u"Réunion Numérique",
        62: u"SNCF",
        64: u"Pacific Mobile Telecom",
        63: u"Viti",
        61: u"Globecast",
        69: u"Zeop",
        68: u"Cellnex",
        67: u"Service des Postes et Telecom",
        65: u"ATC France",
        66: u"Telco OI"
    }
    other_owner = {
        2: u"Association",
        3: u"Aviation Civile",
        5: u"CCI,Ch Metiers,Port Aut,Aérop",
        6: u"Conseil Départemental",
        7: u"Conseil Régional",
        8: u"Coopérative Agricole, Vinicole",
        9: u"Copropriété, Syndic, SCI",
        11: u"DDE",
        12: u"Autres",
        13: u"EDF ou GDF",
        14: u"Etablissement de soins",
        15: u"Etat, Ministère",
        17: u"Syndicat des eaux, Adduction",
        18: u"Intérieur",
        20: u"Météo",
        22: u"Particulier",
        23: u"Phares et balises",
        26: u"SDIS, secours, incendie",
        28: u"Société HLM",
        29: u"Société Privée SA",
        30: u"Sociétés d'Autoroutes",
        34: u"Commune, communauté de commune",
        46: u"Titulaire programme Radio/TV",
    }

    Tour_Mat_Pylone = {
        u"11": u"Mât béton",
        u"12": u"Mât métallique",
        u"21": u"Pylône",
        u"22": u"Pylône autoportant",
        u"23": u"Pylône autostable",
        u"24": u"Pylône haubané",
        u"25": u"Pylône treillis",
        u"26": u"Pylône tubulaire",
        u"42": u"Mât",
        u"48": u"pylône arbre"
    }

class Analyser_Merge_Tour_Mat_Pylone(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 0, [u'11', u'12', u'21', u'22', u'23', u'24', u'25', u'26', u'42', u'48'], u"Tour, mât et pylône",
                                                  [{"man_made": "tower","tower:type": "communication"},{"man_made": "mast","tower:type": "communication"},{"man_made": "communications_tower"}],
                                                  {"man_made": "mast","tower:type": "communication"})

class Analyser_Merge_Tour_Hertzienne(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 1, u'33', u"Tour hertzienne",
                                                  [{"man_made": "tower","tower:type": "communication"},{"man_made": "mast","tower:type": "communication"},{"man_made": "communications_tower"}],
                                                  {"man_made": "communications_tower"})

class Analyser_Merge_Tour_Controle(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 2, u'44', u"Tour de contrôle",
                                                  {"man_made": "tower", "service": "aircraft_control"}, {"man_made": "tower", "service": "aircraft_control"})

class Analyser_Merge_Chateau_Eau(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 3, u'4', u"Château d'eau ou réservoir", {"man_made": "water_tower"}, {"man_made": "water_tower"})

class Analyser_Merge_Silo(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 4, u'31', u"Silo", {"man_made": "silo"}, {"man_made": "silo"})

class Analyser_Merge_Phare(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 5, u'41', u"Phare", {"man_made": "lighthouse"}, {"man_made": "lighthouse"})

class Analyser_Merge_Eolienne(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 6, u'52', u"Éolienne", {"power": "generator","generator:source": "wind"}, {"power": "generator","generator:source": "wind"})
