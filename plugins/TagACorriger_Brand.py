#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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

#from plugins.Plugin import Plugin
from Plugin import Plugin
import unicodedata


class TagACorriger_Brand(Plugin):

    def normalize(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')).lower()

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3130] = { "item": 3130, "desc": {"en": u"Tag name is a brand", "fr": u"Le tag name est une marque"} }
        self.Brand = self.BRAND.split("\n")

    def node(self, data, tags):
        if not "name" in tags:
            return

        if self.normalize(tags["name"]) in self.Brand:
            return [(3130, 0, {})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

    BRAND = """
8 a huit
ad
ada
agip
air bp
alfa romeo
alinea
alpha romeo
aral
as24
atac
atol
auchan
audi
autofit
auto securite
avia
axa
banette
banque populaire
bentley
bmw
bnp paribas
bosh
bp
bricomarche
british petroleum
buffalo grill
buro+
caisse d'epargne
campanile
carglass
carrefour
carrefour contact
carrefoure market
carrefour express
carrefourmarket
carrefour market
carrefour-market
case
cash converters
casino
castorama
champion
chaussures na !
chevrolet
cic
citroen
cittoen
conforama
coop
cora
courtepaille
credit agricole
crescendo
dacia
dacia renault
darty
decathlon
dekra
dekra veritas auto
desigual
deutz-fahr
devred
dia
d.m. combustibles
dynef
dyneff
ecomarcher
ed
elan
e.leclerc
e. leclerc
elephant bleu
elf
esso
esso express
etape-auto
europcar
eurorepar
ferrari
feuvert
feu vert
fiat
fina
florajet
fnac
ford
franprix
gare sncf
geant casino
gecco
gfi informatique
gilera
gmf
harley-davidson
honda
hsbc
hummer
hyper u
hypo wash
hyundai
ibis
igol
ih
ikea
ina
interflora
intermarche
intersport
itelcementi group
jaguar
jardiland
jecrismavie
jennyfer
john deere
kai
kia
kiabi
krys
lancia
land rover
land-rover
la poste
la station u
lcl
leader price
leclerc
l'elephant bleu
leonidas
leroy merlin
les briconautes
lexmark
libreco
lidl
logis de france
lotus
loxam
marche franprix
marionnaud
maserati
match
mazda
mcdonald's
mercedes
mercedes-benz
midas
midi music
migrol
mini
monoprix
motrio
mowag
nature & decouvertes
netto
new holland
nissan
norauto
okaidi obaibi
opel
optic 2000
oxbow
paris store
petit casino
peugeot
piaggio
picard
pizza hut
pole emploi
porsche
premiere classe
pro&cie
proxi
pulsat
q8
quick
renaud
renault
rent a car
roady
rolls royce
saab
seat
securitest
sergio bossi
sfr
shell
shopi
simply
simply market
sixt
skoda
societe generale
sopra group
spar
speedy
ssangyong
station bp
station carrefour
station elf
station esso
station intermarche
station match
station shell
station total
stihl
subway
superu
super u
suziki
suzuki
tati
texaco
total
total/rubis
toyota
trendel
triumph
troc.com
u
u express
utile
velo & oxigene
veolia
vespa
viking
vito
vival
volkswagen
volvo
vw
weldom
yacco
yamaha
"""

if __name__ == "__main__":
    a = TagACorriger_Brand(None)
    a.init(None)
    for d in [u"Citroën"]:
        if not a.node(None, {"name":d}):
            print "fail: %s" % d
