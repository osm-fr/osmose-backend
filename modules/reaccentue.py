#!/usr/bin/env python

# Original work from https://github.com/cquest/reaccentue

import sys
import os
import re
import select
import csv
import pickle
import gzip

from unidecode import unidecode


def add_dico(mot, dico):
    if mot < 'A':
        return
    maj = unidecode(mot).upper()
    if maj in dico:
        if mot not in dico[maj]:
            dico[maj].append(mot)
    else:
        dico[maj] = [mot]


def load_word(mot, dico, affixes):
    m = re.sub(r'/.*', '', mot)
    add_dico(m, dico)
    rules = re.sub(r'.*/', '', mot)
    while rules != '':
        rule = rules[0:2]
        rules = rules[2:]
        if rule in affixes:
            if affixes[rule]['type'] == 'SFX':
                for r in affixes[rule]['rules']:
                    if re.search(r[4]+'$', m):
                        suffixe = re.sub(r'/.*', '', re.sub(r[2]+'$', r[3], m))
                        if suffixe != m:
                            add_dico(suffixe, dico)
                        if '/' in r[3]:
                            load_word(re.sub(r[2]+'$', r[3], m), dico, affixes)
            if affixes[rule]['type'] == 'PFX':
                for r in affixes[rule]['rules']:
                    if re.search('^'+r[4], m):
                        if '/' in r[3]:
                            add_dico(re.sub(r'/.*', '', re.sub('^'+r[2],
                                            r[3], m)), dico)
                            load_word(re.sub('^'+r[2], r[3], m), dico, affixes)
                        elif re.sub('^'+r[2], r[3], m) != m:
                            add_dico(re.sub('^'+r[2], r[3], m), dico)
                            print('-> ', re.sub('^'+r[2], r[3], m), r)


def load_dico(fichier, dico):
    "Charge le dictionnaire MAJUSCULE > minuscules accentuées"

    # charge les définitions des suffixes (SFX)
    affixes = dict()
    try:
        with open(fichier+'.aff', mode='r') as affix:
            for aff in affix:
                af = aff.split()
                if len(af) == 4 and af[0] in ['SFX']:  # header
                    affixes[af[1]] = {'type': af[0], 'cross_product': af[2],
                                      'rules': []}
                if len(af) > 4 and af[0] in ['SFX']:  # rules
                    if af[2] == '0':
                        af[2] = ''
                    if af[3][0] == '0':
                        af[3] = af[3][1:]
                    affixes[af[1]]['rules'].append(af)
    except:
        pass

    # charge le contenu du dictionaire en appliquant préfixes/suffixes
    with open(fichier+'.dic', mode='r') as dicco:
        for mot in dicco:
            mot = mot.replace('\n', '')
            load_word(mot, dico, affixes)

    return dico


def reduce_dico():
    # on élimine les entrées uniques sans accent
    global dico
    dico = {key:val for key, val in dico.items()
            if len(val) > 1 or val[0] != unidecode(val[0])}

    # on complète avec les fréquences de doublets avec mot précédent
    with gzip.open('dico/freq5.pz', 'rb') as cache:
        freq = pickle.load(cache)
    for f in freq:
        mots = unidecode(f).upper().split()
        if len(mots) > 1 and mots[1] in dico:
            dico[f] = freq[f]


def reaccentue(maj):
    prev = None
    maj = maj.strip().upper()
    majWords = maj.split()
    majRes = list()
    for mot in majWords:
        if mot.lower() in articles:
            majRes.append(mot.capitalize() if prev is None else mot.lower())
        elif mot.upper() in dico and len(dico[mot.upper()]) == 1:
            majRes.append(dico[mot.upper()][0].capitalize())
        else:
            mm = None
            if prev is not None and mot.upper() in dico:
                f = 0
                for m in dico[mot.upper()]:
                    ml = m.lower()
                    if prev+' '+ml in dico:
                        if dico[prev+' '+ml] > f:
                            f = dico[prev+' '+ml]
                            mm = m
            if mm is None:
                mm = mot
            majRes.append(mm.lower().capitalize())
        prev = mot.lower()
    return " ".join(majRes)


dico = None
freq = None

base_dir = os.path.dirname(os.path.realpath(__file__))
with gzip.open(os.path.join(base_dir, "../dictionaries/fr/reaccentue.pz"), 'rb') as dico_cache:
    dico = pickle.load(dico_cache)

articles = ['le', 'la', 'les',
            'un',  'une', 'des',
            'à', 'au', 'aux',
            'du', 'de',
            'et', 'ou']


if __name__ == "__main__":
    if len(sys.argv) == 1:
        if select.select([sys.stdin, ], [], [], 0.0)[0]:
            lines = sys.stdin.readlines()
            for l in lines:
                print(reaccentue(l.replace('\n', '')))
        else:
            print("""Usage:  reaccentue.py texte ou fichier
        reaccentue.py 'BOULEVARD DU MARECHAL JEAN MARIE DE LATTRE DE TASSIGNY'
        reaccentue.py fichier.csv nom_colonne""")
    else:
        if bool(re.search('.csv$', sys.argv[1])):
            with open(sys.argv[1], 'r') as in_file:
                csv_in = csv.DictReader(in_file)
                assert csv_in.fieldnames is not None
                csv_out = csv.DictWriter(sys.stdout,
                                         fieldnames=csv_in.fieldnames)
                csv_out.writerow(dict((fn, fn) for fn in csv_in.fieldnames))
                for row in csv_in:
                    row[sys.argv[2]] = reaccentue(row[sys.argv[2]])
                    csv_out.writerow(row)

        else:
            print(reaccentue(sys.argv[1]))
