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
from .modules import italian_strings


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
        self.missing_official = self.def_class(item = 8200, id = 11, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station not integrated'))
        self.missing_osm      = self.def_class(item = 7250, id = 12, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station without tag `ref:mise` or invalid'))
        self.possible_merge   = self.def_class(item = 8201, id = 13, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station integration suggestion'))
        self.update_official  = self.def_class(item = 8202, id = 14, level = 3, tags = ['merge', 'highway'],
            title = T_('Gas station update'))

        self.init(
            'https://www.mise.gov.it/index.php/it/open-data/elenco-dataset/2032336-carburanti-prezzi-praticati-e-anagrafica-degli-impianti',
            'MISE - Ministero Sviluppo Economico',
            CSV(
                Source_Fuel(
                    (attribution = 'MISE - Ministero Sviluppo Economico', fileUrl = 'https://www.mise.gov.it/images/exportCSV/prezzo_alle_8.csv'),
                    (attribution = 'MISE - Ministero Sviluppo Economico', fileUrl = 'https://www.mise.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv'))
                ), separator = ';', quote = '~'),
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
                        'fuel:octane_95': lambda res: 'yes' if (res['Carburanti'] & OCTANE_95) != 0 else None,
                        'fuel:octane_98': lambda res: 'yes' if (res['Carburanti'] & OCTANE_98) != 0 else None,
                        'fuel:octane_100': lambda res: 'yes' if (res['Carburanti'] & OCTANE_100) != 0 else None,
                        'fuel:diesel': lambda res: 'yes' if (res['Carburanti'] & DIESEL) != 0 else None,
                        'fuel:diesel:class2': lambda res: 'yes' if (res['Carburanti'] & DIESEL_CL2) != 0 else None,
                        'fuel:GTL_diesel': lambda res: 'yes' if (res['Carburanti'] & GTL_DIESEL) != 0 else None,
                        'fuel:HGV_diesel': lambda res: 'yes' if (res['Carburanti'] & HGV_DIESEL) != 0 else None,
                        'fuel:lng': lambda res: 'yes' if (res['Carburanti'] & LNG) != 0 else None,
                        'fuel:lpg': lambda res: 'yes' if (res['Carburanti'] & LPG) != 0 else None,
                        'fuel:cng': lambda res: 'yes' if (res['Carburanti'] & CNG) != 0 else None,
                    },
                text = lambda tags, fields: {'en': '%s, %s' % (fields['Indirizzo'], fields['Comune'])} )))


class Source_Fuel(Source, Source2):
    def open(self):
        # Cheat the parent open
        self.encoding = 'UTF-8'
        f = Source.open(self)

        #         0              1      2      3      4
        #idImpianto;descCarburante;prezzo;isSelf;dtComu
        csvreader = csv.reader(f, delimiter=';')

        impianti = {}
        for row in csvreader:
            impianto = impianti.get(row[0], 0)
            carburante = self.evaluate_fuel(row[1])
            if (impianto & carburante) != 0:
                continue
            if self.diff_days(self.date_format(row[4], '%d/%m/%Y %H:%M:%S')) > 30:
                continue
            impianto |= carburante
            impianti[row[0]] = impianto

        csvfile = io.StringIO()
        writer = csv.writer(csvfile)

        f = Source2.open(self)
        csvreader = csv.reader(f, delimiter=';')
        for row in csvreader:
            if row[0] == 'idImpianto':
                writer.writerow(row + ';Carburanti')
            else:
                impianto = impianti.get(row[0])
                if impianto:
                    writer.writerow(row + ';' + impianto)
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
    'V-POWER DIESEL' :          GTL_DIESEL,
}


def evaluate_fuel(self, s):
    return FUEL_TYPE_MAP.get(s.upper())


def diff_days(self, date_string):
    d1 = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    d2 = datetime.date.today()
    return abs((d2 - d1).days)