#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate

class Analyser_Merge_Wastewater_Plant_FR(Analyser_Merge):
    def __init__(self, config, logger = None):

        self.missing_official = {"item":"8380", "class": 1, "level": 3, "tag": ["merge"], "desc": T_(u"Wastewater plant not integrated") }
        self.possible_merge   = {"item":"8381", "class": 3, "level": 3, "tag": ["merge"], "desc": T_(u"Wastewater plant, integration suggestion") }
        self.update_official  = {"item":"8382", "class": 4, "level": 3, "tag": ["merge"], "desc": T_(u"Wastewater plant update") }

        Analyser_Merge.__init__(self, config, logger,
            u"http://www.sandre.eaufrance.fr/atlas/srv/fre/catalog.search#/metadata/ebef2115-bee5-40bb-b5cc-4593d82ba334",
            u"Stations de traitement des eaux usées - France entière",
            CSV(Source(attribution = u"Sandre", millesime = "09/2019",
                    fileUrl = u"http://services.sandre.eaufrance.fr/geo/odp_FRA?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&typename=SysTraitementEauxUsees&SRSNAME=EPSG:4326&OUTPUTFORMAT=CSV")),
            Load("LongWGS84OuvrageDepollution", "LatWGS84OuvrageDepollution",
                  select = {"DateMiseHorServiceOuvrageDepollution": None}
                 ),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"man_made": "wastewater_plant"}),
                conflationDistance = 200,
                osmRef = "ref:FR:Sandre",
                generate = Generate(
                    static1 = {"man_made": "wastewater_plant"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:Sandre": "CdOuvrageDepollution",
                                "start_date" : lambda fields: None if not fields.get(u"DateMiseServiceOuvrageDepollution") else fields[u"DateMiseServiceOuvrageDepollution"][0:4] if fields[u"DateMiseServiceOuvrageDepollution"].endswith('-01-01') or fields[u"DateMiseServiceOuvrageDepollution"].endswith('-12-31') else fields[u"DateMiseServiceOuvrageDepollution"]},
                    text = lambda tags, fields: {"en": ', '.join(filter(lambda x: x, [fields["NomOuvrageDepollution"], fields["LbSystemeCollecte"], fields["NomAgglomerationAssainissement"]]))})))

