#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .Analyser_Merge_Dynamic import Analyser_Merge_Dynamic, SubAnalyser_Merge_Dynamic
from .Analyser_Merge import Source, CSV, Load, Mapping, Select, Generate
import json

class Analyser_Merge_Radio_Support_FR(Analyser_Merge_Dynamic):

    def __init__(self, config, logger = None):
        Analyser_Merge_Dynamic.__init__(self, config, logger)

        mapingfile = json.loads(open("merge_data/radio_support_FR.mapping.json").read())
        for r in mapingfile:
            self.classFactory(SubAnalyser_Merge_Radio_Support_FR, r['NAT_ID'], r['NAT_ID'], r['title'], r['tags_select'], r['tags_generate1'], r['tags_generate2'])


class SubAnalyser_Merge_Radio_Support_FR(SubAnalyser_Merge_Dynamic):
    def __init__(self, config, error_file, logger, NAT_ID, title, tags_select, tags_generate1, tags_generate2):

        self.missing_official = {"item":"10000", "class": 1+10*NAT_ID, "level": 3, "tag": ["merge"], "desc": T_f(u"Radio support ({0}) not integrated", title) }
        self.possible_merge   = {"item":"10001", "class": 3+10*NAT_ID, "level": 3, "tag": ["merge"], "desc": T_f(u"Radio support ({0}), integration suggestion", title) }
        self.update_official  = {"item":"10002", "class": 4+10*NAT_ID, "level": 3, "tag": ["merge"], "desc": T_f(u"Radio support ({0}) update", title) }

        self.communeNameIndexedByInsee = {}
        with open("dictionaries/FR/BddCommunes", "r") as f :
            for x in f :
                x = x.split("\t")
                code_insee = x[0]
                name_insee = x[1].strip().decode('utf-8')
                self.communeNameIndexedByInsee[code_insee] = name_insee
                
        SubAnalyser_Merge_Dynamic.__init__(self, config, error_file, logger,
            u"https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/",
            u"Données sur les installations radioélectriques de plus de 5 watts",
            CSV(Source(attribution = u"data.gouv.fr:ANFR", millesime = "08/2019",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/b947376a-68a9-49a0-adf2-0899b35fffd9", zip = "SUP_SUPPORT.txt", encoding = "ISO-8859-15"),
                separator = u";", quote = u'$'),
            Load(
("CASE \"COR_CD_EW_LON\" WHEN 'W' THEN -1*(to_number(\"COR_NB_DG_LON\", '99') + to_number(\"COR_NB_MN_LON\", '99') / 60 + to_number(\"COR_NB_SC_LON\", '99') / 3600) WHEN 'E' THEN to_number(\"COR_NB_DG_LON\", '99') + to_number(\"COR_NB_MN_LON\", '99') / 60 + to_number(\"COR_NB_SC_LON\", '99') / 3600 END",), 
("CASE \"COR_CD_NS_LAT\" WHEN 'S' THEN -1*(to_number(\"COR_NB_DG_LAT\", '99') + to_number(\"COR_NB_MN_LAT\", '99') / 60 + to_number(\"COR_NB_SC_LAT\", '99') / 3600) WHEN 'N' THEN to_number(\"COR_NB_DG_LAT\", '99') + to_number(\"COR_NB_MN_LAT\", '99') / 60 + to_number(\"COR_NB_SC_LAT\", '99') / 3600 END",),
                  select = {"NAT_ID": str(NAT_ID)},
                  uniq = ("SUP_ID",)
                 ),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = tags_select),
                conflationDistance = 50,
                osmRef = "ref:FR:ANFR",
                generate = Generate(
                    static1 = tags_generate1,
                    static2 = dict({"source": self.source}, **tags_generate2),
                    mapping1 = {
                        "ref:FR:ANFR": "SUP_ID",
                        "owner": lambda fields: self.proprietaire[int(fields["TPO_ID"])] if fields["TPO_ID"] and int(fields["TPO_ID"]) in self.proprietaire else None,
                        "height": lambda fields: fields["SUP_NM_HAUT"].replace(",", ".") if fields["SUP_NM_HAUT"] else None
                    },
                    mapping2 = {
                        },
                text = lambda tags, fields: {"en": u"%s, address : %s, %s" % (title,
                                                                              ", ".join(filter(lambda x: x != "None", [fields["ADR_LB_LIEU"], fields["ADR_LB_ADD1"], fields["ADR_LB_ADD2"], fields["ADR_LB_ADD3"],fields["ADR_NM_CP"]])),
                                                                              (lambda x: self.communeNameIndexedByInsee[x] if x in self.communeNameIndexedByInsee else x)(fields["COM_CD_INSEE"]))
                                             })))

    # nombre : colonne TPO_ID dans SUP_SUPPORT.txt et valeur : SUP_PROPRIETAIRE.txt
    proprietaire = {1 : u"ANFR",
        #2 : Association,
        #3 : Aviation Civile,
        4 : u"Bouygues",
        #5 : CCI,Ch Metiers,Port Aut,Aérop,
        #6 : Conseil Départemental,
        #7 : Conseil Régional,
        #8 : Coopérative Agricole, Vinicole,
        #9 : Copropriété, Syndic, SCI,
        10 : u"CROSS",
        #11 : DDE,
        #12 : Autres
        #13 : EDF ou GDF,
        #14 : Etablissement de soins,
        #15 : Etat, Ministère,
        16 : u"Orange Services Fixes",
        #17 : Syndicat des eaux, Adduction,
        #18 : Intérieur,
        19 : u"La Poste",
        #20 : Météo,
        21 : u"Orange",
        #22 : Particulier,
        #23 : Phares et balises,
        24 : u"SNCF Réseau",
        25 : u"RTE",
        #26 : SDIS, secours, incendie,
        27 : u"SFR",
        #28 : Société HLM,
        #29 : Société Privée SA,
        #30 : Sociétés d'Autoroutes,
        31 : "Société réunionnaise du radiotéléphone",
        32 : u"TDF",
        33 : u"Towercast",
        #34 : Commune, communauté de commune,
        35 : u"Voies navigables de France",
        36 : u"Altitude Telecom",
        37 : u"Antalis",
        38 : u"One Cast",
        39 : u"Gendarmerie nationale",
        40 : u"Tikiphone",
        41 : u"France Caraibes Mobiles",
        42 : u"IFW-Free",
        43 : u"Lagardère Active Média",
        44 : u"Outremer Telecom",
        45 : u"RATP",
        #46 : Titulaire programme Radio/TV,
        47 : u"Office des Postes et Telecom",
        49 : u"Bolloré",
        48 : u"Neuf Cegetel",
        50 : u"Completel",
        51 : u"Digicel",
        52 : u"Eutelsat",
        53 : u"Expertmedia",
        54 : u"Mediaserv",
        55 : u"Belgacom",
        56 : u"Airbus",
        57 : u"Guyane Numérique",
        58 : u"Dauphin Telecom",
        59 : u"Itas Tim",
        60 : u"Réunion Numérique",
        62 : u"SNCF",
        64 : u"Pacific Mobile Telecom",
        63 : u"Viti",
        61 : u"Globecast",
        69 : u"Zeop",
        68 : u"Cellnex",
        67 : u"Service des Postes et Telecom",
        65 : u"ATC France",
        66 : u"Telco OI"
    }
