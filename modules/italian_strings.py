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

from functools import reduce


COMMON_WORDS_MAP = {
    'A': 'a',
    'Dei': 'dei',
    'Del': 'del',
    'Di': 'di',
    'Ed': 'ed',
    'E': 'e',
    'F.Lli': 'F.lli',
    'In': 'in',
    'Responsabilita\'': 'Responsabilità',
    'Sas': 'S.A.S.',
    'Sigla': 'sigla',
    'Snc': 'S.N.C.',
    'Societa\'': 'Società',
    'S.P.A.': 'S.p.A.',
    'Spa': 'S.p.A.',
    'Srl': 'S.R.L.',
}


TITLES_MAP = {
    'Dott.Ri': 'Dott.ri',
    'Dott.Ssa': 'Dott.ssa',
    'Dott.Sse': 'Dott.sse',
    'Dr.I': 'Dott.ri',
    'Dr.Ssa': 'Dott.ssa',
}


ROMAN_NUMBERS_MAP = {
    'Vii': 'VII',
    'Vi': 'VI',
    'Xiv': 'XIV',
    'Xxiii': 'XXIII',
    'Xx': 'XX',
}

PHARMACY_WORDS_MAP = reduce(lambda x, y: dict(x, **y), (COMMON_WORDS_MAP, TITLES_MAP, ROMAN_NUMBERS_MAP))

# First Char Uppercase
# quotes (") removal
# asterisk (*) removal
# extra spaces trim
# special case stopwords


def normalize(s, replace_map = {}):
    s = s.replace('"', ' ').replace('*', ' ').title()
    s = ' '.join(map(lambda x: replace_map.get(x, x), s.split()))
    return s[:1].upper() + s[1:]


def normalize_common(s):
    return normalize(s, COMMON_WORDS_MAP)


def normalize_pharmacy(s):
    return normalize(s, PHARMACY_WORDS_MAP)


def osmRefVatin(s):
    if len(s) != 11 or s.isdigit() is False:
        return None
    return 'IT' + s


###########################################################################
import unittest


class Test(unittest.TestCase):

    def test_normalization(self):
        for (s, t) in [
            ('GIUSEPPE LINGUA & C. S.A.S. SIGLABILE GIUSEPPE LINGUA SAS', 'Giuseppe Lingua & C. S.A.S. Siglabile Giuseppe Lingua S.A.S.'),
            ('TRAVERSA MARIO SNC DI TRAVERSA MASSIMO E MARCO SIGLABILE TRAVERSA SNC', 'Traversa Mario S.N.C. di Traversa Massimo e Marco Siglabile Traversa S.N.C.'),
            ('"IP SERVICES S.R.L."', 'Ip Services S.R.L.'),
            ('ARCOBALENO DI GARRO DARIO & C. S.A.S.', 'Arcobaleno di Garro Dario & C. S.A.S.'),
            ('DIS-CAR DI SARRA PAOLO & C. S.N.C.', 'Dis-Car di Sarra Paolo & C. S.N.C.'),
            ('SOCIETA\' AGRICOLA LUBRIFICANTI CARBURANTI ED AFFINI (SIGLA S.A.L.C.A.) A RESPONSABILITA\' LIMITATA', 'Società Agricola Lubrificanti Carburanti ed Affini (Sigla S.A.L.C.A.) a Responsabilità Limitata'),
            ('F.LLI BOVIO S.N.C. DI BOVIO ENRICO', 'F.lli Bovio S.N.C. di Bovio Enrico'),
            ('vignolo e garbarino s.n.c.', 'Vignolo e Garbarino S.N.C.'),
            ('DI SCIORIO DOMENICO', 'Di Sciorio Domenico'),
            ('"S.S.C. SOCIETA\' SVILUPPO COMMERCIALE S.R.L." IN SIGLA "S.S.C. S. R.L.', 'S.S.C. Società Sviluppo Commerciale S.R.L. in sigla S.S.C. S. R.L.'),
            ('CARBURANTI DI RAFFAELE NIEDDU E GIOVANNI MARCO NIEDDU SOCIETA\' IN NOME COLLETTIVO *', 'Carburanti di Raffaele Nieddu e Giovanni Marco Nieddu Società in Nome Collettivo'),
            ('DI ROSA ANGELO S.A.S. DEI FRATELLI PAOLO CORRADO E GIUSEPPE DI RO SA & C.', 'Di Rosa Angelo S.A.S. dei Fratelli Paolo Corrado e Giuseppe di Ro Sa & C.'),
            ('SERVIZI E GESTIONI ZENIT S.R.L. IN SIGLA - ZENIT S.R.L.', 'Servizi e Gestioni Zenit S.R.L. in sigla - Zenit S.R.L.'),
            ('ITALIANA CARBURANTI S.P.A.', 'Italiana Carburanti S.p.A.'),
            ('SERVIZI & GESTIONI ITALIA srl', 'Servizi & Gestioni Italia S.R.L.'),
        ]:
            self.assertEqual(normalize_common(s), t)

        for (s, t) in [
            ('Farmacia Dell\'Olmina Di A. Leardi E Dott.ssa B. Torretta E C. S.a.s.', 'Farmacia Dell\'Olmina di A. Leardi e Dott.ssa B. Torretta e C. S.A.S.'),
        ]:
            self.assertEqual(normalize_pharmacy(s), t)
