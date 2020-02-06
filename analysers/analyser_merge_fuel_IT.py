#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyright 2020                                                        ##
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


class Analyser_Merge_Fuel_IT(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item = 8200, id = 1, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station not integrated'))
        self.possible_merge   = self.def_class(item = 8201, id = 3, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station integration suggestion'))
        self.update_official  = self.def_class(item = 8202, id = 4, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station update'))

        self.init(
            'https://www.mise.gov.it/index.php/it/open-data/elenco-dataset/2032336-carburanti-prezzi-praticati-e-anagrafica-degli-impianti',
            'MISE - Ministero Sviluppo Economico',
            CSV(Source(attribution = u'MISE - Ministero Sviluppo Economico', fileUrl = u'https://www.mise.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv'),
                separator = ';', skip_first_lines = 1, quote = '~'),
            Load('Longitudine', 'Latitudine',
                where = lambda row: row['Bandiera'] != u'Pompe Bianche' and row['Longitudine'] != 'NULL' and row['Latitudine'] !='NULL'),
            Mapping(
                select = Select(
                    types = ['nodes', 'ways'],
                    tags = {'amenity': 'fuel'}),
                osmRef = 'ref:mise',
                conflationDistance = 50,
                generate = Generate(
                    static1 = {'amenity': 'fuel'},
                    static2 = {'source': self.source},
                    mapping1 = {
                        'ref:mise': 'idImpianto',
                        'operator': lambda res: res[u'Gestore'].strip().replace('"', ' ').replace(',', ' ').replace('  ', ' ').title(),
                        'brand': 'Bandiera'},
                text = lambda tags, fields: {'en': u'%s, %s' % (fields['Indirizzo'], fields['Comune'])} )))
