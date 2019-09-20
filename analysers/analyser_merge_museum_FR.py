#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate
import re

class Analyser_Merge_Museum_FR(Analyser_Merge):
    def __init__(self, config, logger = None):

        self.missing_official = {"item":"8010", "class": 31, "level": 3, "tag": ["merge"], "desc": T_(u"Museum not integrated") }
        self.possible_merge   = {"item":"8011", "class": 33, "level": 3, "tag": ["merge"], "desc": T_(u"Museum, integration suggestion") }
        self.update_official  = {"item":"8012", "class": 34, "level": 3, "tag": ["merge"], "desc": T_(u"Museum update") }

        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/musees-de-france-base-museofile/",
            u"Musées de France : base Muséofile",
            CSV(Source(attribution = u"Ministère de la Culture - Muséofile", millesime = "09/2019",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/5ccd6238-4fb0-4b2c-b14a-581909489320"),
                separator = u';'),
            Load("geolocalisation", "geolocalisation",
                 where = lambda row: row["geolocalisation"],
                 xFunction = lambda x: x and x.split(',')[1],
                 yFunction = lambda y: y and y.split(',')[0]
                 ),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"tourism": "museum"}),
                conflationDistance = 50,
                osmRef = u"ref:FR:muséofile",
                generate = Generate(
                    static1 = {"tourism": "museum"},
                    static2 = {"source": self.source},
                    mapping1 = {u"ref:FR:muséofile": "Identifiant"},
                    mapping2 = {"website": "URL",
                                "phone": u"Téléphone",
                                "phone": lambda res: "+33 " + res["Téléphone"][1:] if re.match(r"^0[0-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2}", res["Téléphone"]) else res["Téléphone"],
                                "name": lambda res: res["Nom usage"] if res["Nom usage"] else res["Nom officiel"][0].upper() + res["Nom officiel"][1:],
                                "official_name" : lambda res: res["Nom officiel"][0].upper() + res["Nom officiel"][1:] if res["Nom usage"] and res["Nom officiel"].lower() != res["Nom usage"].lower() else None,
                                },
                    text = lambda tags, fields: {"en": ' '.join(filter(lambda x: x, [fields["Adresse"], fields["Code Postal"], fields["Ville"]]))})))

