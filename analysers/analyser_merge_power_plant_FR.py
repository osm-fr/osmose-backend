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
from io import open # In python3 only, this import is not required
from .Analyser_Merge import Analyser_Merge, Source, CSV, Load, Mapping, Select, Generate
from .modules import downloader


class Analyser_Merge_Power_Plant_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8270", "class": 1, "level": 3, "tag": ["merge", "power"], "desc": T_(u"Power plant not integrated, geocoded at municipality level") }

        Analyser_Merge.__init__(self, config, logger,
            u"https://opendata.reseaux-energies.fr/explore/dataset/registre-national-installation-production-stockage-electricite-agrege-311217",
            u"Registre national des installations de production d'électricité et de stockage",
            CSV(Power_Plant_FR_Source(attribution = u"data.gouv.fr:RTE", millesime = "2017",
                    fileUrl = u"https://opendata.reseaux-energies.fr/explore/dataset/registre-national-installation-production-stockage-electricite-agrege-311217/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true", logger=logger),
                separator = u";"),
            Load("longitude", "latitude",
                where = lambda res: res.get('max_puissance') and float(res["max_puissance"]) > 1000),
            Mapping(
                select = Select(
                    types = ["ways", "relations"],
                    tags = {"power": "plant"}),
                conflationDistance = 5000,
                generate = Generate(
                    static1 = {
                        "power": "plant"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        # No voltage tga on power=plant
                        #"voltage": lambda fields: (int(fields["Tension raccordement"].split(' ')[0]) * 1000) if fields.get("Tension raccordement") and fields["Tension raccordement"] not in ["< 45 kV", "BT", "HTA"] else None,
                        "plant:source": lambda fields: self.filiere[fields["Filière"]][fields["Combustible"]],
                        "plant:output:electricity": lambda fields: int(float(fields["max_puissance"]) * 1000)},
                    mapping2 = {
                        "start_date": lambda fields: None if not fields.get(u"dateMiseEnService") else fields[u"dateMiseEnService"][0:4] if fields[u"dateMiseEnService"].endswith('-01-01') or fields[u"dateMiseEnService"].endswith('-12-31') else fields[u"dateMiseEnService"]},
                   tag_keep_multiple_values = ["voltage"],
                   text = lambda tags, fields: T_(u"Power plant %s", fields["nomInstallation"]) if fields["nomInstallation"] != 'None' else None)))

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
            u"Gaz": "gaz"},
     }


class Power_Plant_FR_Source(Source):

    def open(self):
      return open(downloader.update_cache('geocoded://' + self.fileUrl, 60, self.fetch))

    def fetch(self, url, tmp_file, date_string=None):
        service = u'https://api-adresse.data.gouv.fr/search/csv/'
        outfile = open(tmp_file, 'w', encoding='utf-8')

        content = Source.open(self).readlines()
        header = content[0:1]
        step = 2000
        slices = int((len(content)-1) / step) + 1
        for i in range(0, slices):
            self.logger.log("Geocode slice {0}/{1}".format(i, slices))
            slice = '\n'.join(header + content[1 + step*i : step*(i+1)])
            r = downloader.requests_retry_session().post(url=service, data={
                'delimiter': ';',
                'encoding': 'utf-8',
                'columns': 'Commune',
                'citycode': 'codeINSEECommune',
            }, files={
                'data': slice,
            })
            r.raise_for_status()
            if i == 0:
                text = '\n'.join(r.text.split('\n')[0:])
            else:
                text = '\n'.join(r.text.split('\n')[1:])
            writer = outfile.write(text)

        return True
