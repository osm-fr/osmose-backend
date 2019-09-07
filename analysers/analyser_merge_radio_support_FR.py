#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate
import json
from io import open


class _Analyser_Merge_Radio_Support_FR(Analyser_Merge):
    def __init__(self, config, logger, clas, NAT_IDs, tags_select):

        self.missing_official = {"item":"8370", "class": 1+10*clas, "level": 3, "tag": ["merge"], "desc": T_(u"Radio support not integrated") }
        self.possible_merge   = {"item":"8371", "class": 3+10*clas, "level": 3, "tag": ["merge"], "desc": T_(u"Radio support, integration suggestion") }
        self.update_official  = {"item":"8372", "class": 4+10*clas, "level": 3, "tag": ["merge"], "desc": T_(u"Radio support update") }

        mapingfile = json.loads(open("merge_data/radio_support_FR.mapping.json").read())
        self.supportTags = {}
        for x in mapingfile :
            self.supportTags[x['NAT_ID']] = x
        self.communeNameIndexedByInsee = {}
        with open("dictionaries/FR/BddCommunes", "r", encoding="utf-8") as f :
            for x in f :
                x = x.split("\t")
                code_insee = x[0]
                name_insee = x[1].strip()
                self.communeNameIndexedByInsee[code_insee] = name_insee
                
        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/",
            u"Données sur les installations radioélectriques de plus de 5 watts",
            CSV(Source(attribution = u"data.gouv.fr:ANFR", millesime = "08/2019",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/b947376a-68a9-49a0-adf2-0899b35fffd9", zip = "SUP_SUPPORT.txt", encoding = "ISO-8859-15"),
                separator = u";", quote = u'$'),
            Load(
("CASE \"COR_CD_EW_LON\" WHEN 'W' THEN -1*(to_number(\"COR_NB_DG_LON\", '99') + to_number(\"COR_NB_MN_LON\", '99') / 60 + to_number(\"COR_NB_SC_LON\", '99') / 3600) WHEN 'E' THEN to_number(\"COR_NB_DG_LON\", '99') + to_number(\"COR_NB_MN_LON\", '99') / 60 + to_number(\"COR_NB_SC_LON\", '99') / 3600 END",), 
("CASE \"COR_CD_NS_LAT\" WHEN 'S' THEN -1*(to_number(\"COR_NB_DG_LAT\", '99') + to_number(\"COR_NB_MN_LAT\", '99') / 60 + to_number(\"COR_NB_SC_LAT\", '99') / 3600) WHEN 'N' THEN to_number(\"COR_NB_DG_LAT\", '99') + to_number(\"COR_NB_MN_LAT\", '99') / 60 + to_number(\"COR_NB_SC_LAT\", '99') / 3600 END",),
                  select = {"NAT_ID": NAT_IDs},
                  uniq = ("SUP_ID",)
                 ),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = tags_select),
                conflationDistance = 50,
                osmRef = "ref:FR:ANFR",
                generate = Generate(
                    static2 = {"source": self.source},
                    mapping1 = {
                        "ref:FR:ANFR": "SUP_ID",
                        "owner": lambda fields: self.proprietaire[int(fields["TPO_ID"])] if fields["TPO_ID"] and int(fields["TPO_ID"]) in self.proprietaire else None,
                        "height": lambda fields: fields["SUP_NM_HAUT"].replace(",", ".") if fields["SUP_NM_HAUT"] else None,
                        "man_made": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["man_made"] if "man_made" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        "location": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["location"] if "location" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        "tower:type": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["tower:type"] if "tower:type" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        "antenna": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["antenna"] if "antenna" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        "service": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["service"] if "service" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        "power": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["power"] if "power" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        "generator:source": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["generator:source"] if "generator:source" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        },
                    mapping2 = {
                        "material": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["material"] if "material" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        "tower:construction": lambda fields: self.supportTags[int(fields["NAT_ID"])]["tags_generate1"]["tower:construction"] if "tower:construction" in self.supportTags[int(fields["NAT_ID"])]["tags_generate1"] else None,
                        },

                text = lambda tags, fields: {"en": u"radio support : %s, address : %s, %s" % (self.supportTags[int(fields["NAT_ID"])]["title"],
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

class Analyser_Merge_Tour_Mat_Pylone(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 0, [u'11', u'12', u'21', u'22', u'23', u'24', u'25', u'26', u'33', u'42', u'44', u'47', u'48'], [{"man_made" : "tower","tower:type" : "communication"},{"man_made" : "mast","tower:type" : "communication"},{"man_made" : "communications_tower"},{"man_made": "tower", "service": "aircraft_control"}])

class Analyser_Merge_Antenne(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 1, [u'0', u'8', u'9', u'10', u'17', u'19', u'20', u'32', u'34', u'38', u'39', u'40', u'43', u'45', u'45', u'46', u'49', u'50', u'51', u'999999999'], {"man_made" : "antenna"})

class Analyser_Merge_Chateau_Eau(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 2, u'4', {"man_made" : "water_tower"})

class Analyser_Merge_Silo(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 2, u'31', {"man_made" : "silo"})

class Analyser_Merge_Phare(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 2, u'41', {"man_made" : "lighthouse"})

class Analyser_Merge_Eolienne(_Analyser_Merge_Radio_Support_FR):
    def __init__(self, config, logger = None):
        _Analyser_Merge_Radio_Support_FR.__init__(self, config, logger, 2, u'52', {"power" : "generator","generator:source" : "wind"})
      
