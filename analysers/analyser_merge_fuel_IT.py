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
from .modules import downloader
from .modules import italian_strings
import csv
import datetime


OCTANE_95  = 1 << 0# fuel:octane_95=yes
OCTANE_98  = 1 << 1# fuel:octane_98=yes
OCTANE_100 = 1 << 2# fuel:octane_100=yes
DIESEL     = 1 << 3# fuel:diesel=yes
DIESEL_CL2 = 1 << 4# fuel:diesel:class2=yes
GTL_DIESEL = 1 << 5# fuel:GTL_diesel=yes
HGV_DIESEL = 1 << 6# fuel:HGV_diesel=yes
LNG        = 1 << 7# fuel:lng=yes
LPG        = 1 << 8# fuel:lpg=yes
CNG        = 1 << 9# fuel:cng=yes


class Analyser_Merge_Fuel_IT(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8200, id = 11, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station not integrated'))
        self.def_class_missing_osm(item = 7250, id = 12, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station without tag `ref:mise` or invalid'))
        self.def_class_possible_merge(item = 8201, id = 13, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station integration suggestion'))
        self.def_class_update_official(item = 8202, id = 14, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station update'))

        self.init(
            'https://www.mise.gov.it/index.php/it/open-data/elenco-dataset/2032336-carburanti-prezzi-praticati-e-anagrafica-degli-impianti',
            'MISE - Ministero Sviluppo Economico',
            CSV(Source_Fuel(Source(attribution = 'MISE - Ministero Sviluppo Economico', fileUrl = 'https://www.mise.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv'),
                    fileUrl = 'https://www.mise.gov.it/images/exportCSV/prezzo_alle_8.csv')),
            Load('Longitudine', 'Latitudine',
                where = lambda row: row['Bandiera'] != 'Pompe Bianche' and row['Longitudine'] != 'NULL' and row['Latitudine'] != 'NULL'),
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
                        'operator': lambda res: italian_strings.normalize_common(res['Gestore']),
                        'brand': 'Bandiera',
                        'fuel:octane_95': lambda res: 'yes' if (int(res['Carburanti']) & OCTANE_95) != 0 else Generate.delete_tag,
                        'fuel:octane_98': lambda res: 'yes' if (int(res['Carburanti']) & OCTANE_98) != 0 else Generate.delete_tag,
                        'fuel:octane_100': lambda res: 'yes' if (int(res['Carburanti']) & OCTANE_100) != 0 else Generate.delete_tag,
                        'fuel:diesel': lambda res: 'yes' if (int(res['Carburanti']) & DIESEL) != 0 else Generate.delete_tag,
                        'fuel:diesel:class2': lambda res: 'yes' if (int(res['Carburanti']) & DIESEL_CL2) != 0 else Generate.delete_tag,
                        'fuel:GTL_diesel': lambda res: 'yes' if (int(res['Carburanti']) & GTL_DIESEL) != 0 else Generate.delete_tag,
                        'fuel:HGV_diesel': lambda res: 'yes' if (int(res['Carburanti']) & HGV_DIESEL) != 0 else Generate.delete_tag,
                        'fuel:lng': lambda res: 'yes' if (int(res['Carburanti']) & LNG) != 0 else Generate.delete_tag,
                        'fuel:lpg': lambda res: 'yes' if (int(res['Carburanti']) & LPG) != 0 else Generate.delete_tag,
                        'fuel:cng': lambda res: 'yes' if (int(res['Carburanti']) & CNG) != 0 else Generate.delete_tag,
                    },
                text = lambda tags, fields: {'en': '%s, %s' % (fields['Indirizzo'], fields['Comune'])} )))


class Source_Fuel(Source):
    def __init__(self, source, fileUrl):
        self.source = source
        self.fileUrl = fileUrl

    def __getattr__(self, name):
        return getattr(self.source, name)

    def open(self):
        return open(downloader.update_cache('join://' + self.source.fileUrl, 60, self.fetch))

    def fetch(self, url, tmp_file, date_string=None):
        f = downloader.urlopen(self.fileUrl, 60)

        #         0              1      2      3      4
        #idImpianto;descCarburante;prezzo;isSelf;dtComu
        csvreader = csv.reader(f, delimiter=';')
        next(csvreader) # Skip date
        next(csvreader) # Skip header

        impianti = {}
        for row in csvreader:
            impianto = impianti.get(row[0], 0)
            carburante = self.FUEL_TYPE_MAP.get(row[1].upper())
            if (impianto & carburante) != 0:
                continue
            dt_price = self.date_format(row[4], '%d/%m/%Y %H:%M:%S')
            if not dt_price or self.diff_days(dt_price) > 30:
                continue
            impianto |= carburante
            impianti[row[0]] = impianto

        csvfile = open(tmp_file, 'w', encoding='utf-8')
        writer = csv.writer(csvfile)

        f = self.source.open()
        csvreader = csv.reader(f, delimiter=';', quotechar = '~')
        next(csvreader) # Skip date
        header = next(csvreader)
        writer.writerow(header + ['Carburanti'])
        for row in csvreader:
            impianto = impianti.get(row[0])
            if impianto:
                writer.writerow(row + [ impianto ])

        csvfile.seek(0)
        return csvfile


    FUEL_TYPE_MAP = {
        'BENZINA':                  OCTANE_95,
        'BENZINA 100 OTTANI':       OCTANE_100,
        'BENZINA ENERGY 98 OTTANI': OCTANE_98,
        'BENZINA PLUS 98':          OCTANE_98,
        'BENZINA SHELL V POWER':    OCTANE_100,
        'BENZINA SPECIALE':         OCTANE_100,
        'BENZINA WR 100':           OCTANE_100,
        'BLU DIESEL ALPINO':        DIESEL_CL2,
        'BLUE DIESEL':              GTL_DIESEL,
        'BLUE SUPER':               OCTANE_100,
        'DIESEL E+10':              GTL_DIESEL,# repsol
        'DIESELMAX':                GTL_DIESEL,
        'DIESEL SHELL V POWER':     GTL_DIESEL,
        'E-DIESEL':                 HGV_DIESEL,# esso
        'EXCELLIUM DIESEL':         GTL_DIESEL,
        'F101':                     OCTANE_100,
        'GASOLIO':                  DIESEL,
        'GASOLIO ALPINO':           DIESEL_CL2,
        'GASOLIO ARTICO':           DIESEL_CL2,
        'GASOLIO ECOPLUS':          DIESEL,
        'GASOLIO ENERGY D':         HGV_DIESEL,
        'GASOLIO GELO':             DIESEL_CL2,
        'GASOLIO ORO DIESEL':       GTL_DIESEL,
        'GASOLIO PREMIUM':          GTL_DIESEL,
        'GASOLIO SPECIALE':         GTL_DIESEL,
        'GNL':                      LNG,
        'GP DIESEL':                GTL_DIESEL,
        'GPL':                      LPG,
        'HI-Q DIESEL':              GTL_DIESEL,
        'HIQ PERFORM+':             OCTANE_100,
        'L-GNC':                    LNG,
        'MAGIC DIESEL':             HGV_DIESEL,
        'METANO':                   CNG,
        'R100':                     OCTANE_100,# repsol
        'S-DIESEL':                 GTL_DIESEL,# ?
        'SUPREME DIESEL':           GTL_DIESEL,# esso
        'V-POWER':                  OCTANE_100,
        'V-POWER DIESEL':           GTL_DIESEL,
    }


    def diff_days(self, date_string):
        d1 = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
        d2 = datetime.date.today()
        return abs((d2 - d1).days)


    def date_format(self, date_string, format='%d/%m/%Y'):
        try:
            dt = datetime.datetime.strptime(date_string, format)
            return str(dt.date())
        except ValueError:
            return None
