#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Francesco Ansanelli 2020                                   ##
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
from modules import italian_strings


class Analyser_Merge_Parapharmacy_IT(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item = 7150, id = 21, level = 3, tags = ['merge', 'highway'],
            title = T_('Pharmacy not integrated'))
        self.missing_osm      = self.def_class(item = 7250, id = 22, level = 3, tags = ['merge', 'highway'],
            title = T_('Pharmacy without tag `ref:msal` or invalid'))
        self.possible_merge   = self.def_class(item = 7151, id = 23, level = 3, tags = ['merge', 'highway'],
            title = T_('Pharmacy integration suggestion'))
        self.update_official  = self.def_class(item = 7152, id = 24, level = 3, tags = ['merge', 'highway'],
            title = T_('Pharmacy update'))

        self.init(
            'http://www.dati.salute.gov.it/dataset/parafarmacie.jsp',
            'Ministero della Salute',
            CSV(Source(attribution = 'Ministero della Salute', fileUrl = 'http://www.dati.salute.gov.it/imgs/C_17_dataset_7_download_itemDownload0_upFile.CSV'),
                separator = ';'),
            Load('LONGITUDINE', 'LATITUDINE',
                xFunction = lambda x: self.float_comma(x.replace('\'', '')),# '9,258444
                yFunction = self.float_comma,
                where = lambda row: row['DATAFINEVALIDITA'] == '-' and row['LONGITUDINE'] != '-' and row['LATITUDINE'] != '-'),
            Mapping(
                select = Select(
                    types = ['nodes', 'ways'],
                    tags = {'amenity': 'pharmacy'}),
                osmRef = 'ref:msal',
                conflationDistance = 80,
                generate = Generate(
                    static1 = {
                        'amenity': 'pharmacy',
                        'dispensing': 'no'},
                    static2 = {'source': self.source},
                    mapping1 = {
                        'ref:msal': 'CODICEIDENTIFICATIVOSITO',
                        'ref:vatin': lambda res: italian_strings.osmRefVatin(res['PARTITAIVA']),
                        'start_date': lambda res: self.date_format(res['DATAINIZIOVALIDITA'])},
                    mapping2 = {'operator': lambda res: italian_strings.normalize_pharmacy(res['DENOMINAZIONESITOLOGISTICO'])},
                text = lambda tags, fields: {'en': '%s, %s' % (fields['INDIRIZZO'], fields['DESCRIZIONECOMUNE'])} )))

