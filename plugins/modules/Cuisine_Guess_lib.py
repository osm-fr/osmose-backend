#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2020                                      ##
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

import string
import csv
import sys
import re
import itertools
import random
from collections import defaultdict
from unidecode import unidecode


class Index:
  def __init__(self):
    self.index = defaultdict(lambda: defaultdict(int))
    self.count = defaultdict(int)

  def insert(self, tokens, clazz, coef):
    n = len(tokens)
    for token in tokens:
      self.count[token] += 1
      self.index[token][clazz] += coef / n

  def normalize(self, prune):
    for token, n in list(self.count.items()):
      if n <= prune:
        del self.count[token]
        del self.index[token]

    for _, clazz_score in self.index.items():
      s = sum(clazz_score.values())
      for clazz in clazz_score.keys():
        clazz_score[clazz] /= s

  def search(self, tokens):
    total = defaultdict(int)
    n = 0
    for token in tokens:
      if token in self.index:
        n += 1
        for clazz, score in self.index[token].items():
          total[clazz] += score

    return {k: v/n for k, v in total.items()}


def sum_dict(*d):
  keys = map(lambda coef_dd: list(coef_dd[1].keys()), d)
  keys = set(itertools.chain.from_iterable(keys))

  s_coef = sum(map(lambda coef_dd: coef_dd[0], d))

  ret = {}
  for cuisine in keys:
    s = 0
    for coef, dd in d:
      s += coef * dd.get(cuisine, 0)
    ret[cuisine] = s / s_coef
  return ret


def ngram(text, n):
  return [text[i:i+n] for i in range(0, len(text) - n + 1)]


class Cuisine:
  @staticmethod
  def load_csv(file_path):
    data = []
    with open(file_path) as csvfile:
      spamreader = csv.DictReader(csvfile, delimiter="\t")
      for row in list(spamreader):
        data.append(row)
    return data


  @staticmethod
  def expland_cuisine(cuisines):
    if not cuisines:
      return
    else:
      cuisines = cuisines.lower()
      cuisines = list(set(map(lambda s: s.strip(), cuisines.split(';'))))

      # Non cuisine77
      if 'buffet' in cuisines:
        cuisines.remove('buffet')
      if 'dessert' in cuisines:
        cuisines.remove('dessert')
      if 'cake' in cuisines:
        cuisines.remove('cake')
      if 'world' in cuisines:
        cuisines.remove('world')
      if 'bio' in cuisines:
        cuisines.remove('bio')

      # i10n
      if 'japonais' in cuisines:
        cuisines.append('japanese')
        cuisines.remove('japonais')
      if 'vietnam' in cuisines:
        cuisines.append('vietnamese')
        cuisines.remove('vietnam')
      if 'indien' in cuisines:
        cuisines.append('indian')
        cuisines.remove('indien')

      # Common mistake
      if 'sushi' in cuisines:
        cuisines.append('japanese')
      elif 'japanese' in cuisines:
        cuisines.append('sushi')
      if 'pizza' in cuisines:
        cuisines.append('italian')
      if 'italian_pizza' in cuisines:
        cuisines.append('italian')
        cuisines.append('pizza')
        cuisines.remove('italian_pizza')
      if 'tacos' in cuisines:
        cuisines.append('mexican')

      # if 'regional' in cuisines:
      #   cuisines.append('french')
      # if 'pasta' in cuisines:
      #   cuisines.append('italian')
      # if 'chinese' in cuisines:
      #   cuisines.append('asian')
      return set(cuisines)

  multiple_space = re.compile(' +')

  def expland_name(self, text):
    text = text.lower()
    text = unidecode(text)
    text = text.strip()
    text = text.replace("'", '')
    text = text.translate(str.maketrans(' ', ' ', string.punctuation)) # Remove punctiation
    text = text.translate(str.maketrans(' ', ' ', '0123456789')) # Remove
    text = self.multiple_space.sub(' ', text)
    text = ' '.join(filter(lambda t: len(t) > 1 and t not in ('le',), text.split(' ')))
    text = '  ' + text + '  '
    return text

  @staticmethod
  def enumerate_word(text):
    return list(filter(lambda w: len(w) >= 3, text.strip().split(' ')))

  @staticmethod
  def enumerate_amenity(amenity):
    return list(set(map(lambda s: s.strip(), amenity.split(';'))).intersection(set(['fast_food', 'restaurant'])))

  @staticmethod
  def enumerate_takeaway(takeaway):
    return [takeaway and takeaway != 'no']

  def __init__(self, cuisine_csv, evaluation=0):
    self.N = 3

    self.data = self.load_csv(cuisine_csv)

    if evaluation:
      random.shuffle(self.data)
      self.data_slice = round(len(self.data) * evaluation)
    else:
      self.data_slice = -1

    # Normalize score for "cuisine" occurrences
    coef = defaultdict(int)

    for row in self.data[0:self.data_slice]:
      if row['cuisine']:
        for cuisine in self.expland_cuisine(row['cuisine']):
          coef[cuisine] += 1

    coef = {k: v for k, v in coef.items() if v >= 8} # Remove unfrequented "cuisine"
    for cuisine in coef.keys():
      coef[cuisine] = 1 / coef[cuisine]

    # Index "cuisine" by name and other attributes
    self.index_ngram = Index()
    self.index_words = Index()
    self.index_amenity = Index()
    self.index_takeaway = Index()

    for row in self.data[0:self.data_slice]:
      name = row['name']
      if row['cuisine'] and len(name) >= self.N + 1:
        for cuisine in self.expland_cuisine(row['cuisine']):
          if cuisine in coef:
            text = self.expland_name(name)
            self.index_ngram.insert(ngram(text, self.N), cuisine, coef[cuisine])
            self.index_words.insert(self.enumerate_word(text), cuisine, coef[cuisine])
            self.index_amenity.insert(self.enumerate_amenity(row['amenity']), cuisine, coef[cuisine])
            self.index_takeaway.insert(self.enumerate_takeaway(row['takeaway']), cuisine, coef[cuisine])

    # Normalize and remove unfrequented token
    self.index_ngram.normalize(1)
    self.index_words.normalize(5)
    self.index_amenity.normalize(0)
    self.index_takeaway.normalize(0)


  def guess_score(self, name, amenity, takeaway, c1, c2, c3, c4, s):
    text = self.expland_name(name)
    r_ngram = self.index_ngram.search(ngram(text, self.N))
    r_word = self.index_words.search(self.enumerate_word(text))
    r_amenity = self.index_amenity.search(self.enumerate_amenity(amenity))
    r_takeaway = self.index_takeaway.search(self.enumerate_takeaway(takeaway))

    r = sum_dict([c1, r_ngram], [c2, r_word], [c3, r_amenity], [c4, r_takeaway])
    r = {k: v for k, v in r.items() if v > s}
    return r

  def guess(self, name, amenity, takeaway, c1=1, c2=2.02414594, c3=0.1519341, c4=0.14086179, s=0.5):
    g = self.guess_score(name, amenity, takeaway, c1, c2, c3, c4, s)
    return {k: 0.9 if v > 0.6 else 0.75 for k, v in g.items()}

  def evaluate(self, c1, c2, c3, c4, s):
    n = 0
    c = 0
    sco = 0
    for row in self.data[self.data_slice:-1]:
      name = row['name']
      cuisines = self.expland_cuisine(row['cuisine'])
      if cuisines and len(name) >= self.N + 1:
        r = self.guess_score(name, row['amenity'], row['takeaway'], c1, c2, c3, c4, s)

        if r:
          n += 1
          # m = False
          for cuisine, score in r.items():
            if cuisine in cuisines:
              sco += score
              c += 1
              # print(True, name, cuisines, r)
              # m = True
              break
            # else:
            #   print(cuisines, cuisine)

          # if not m:
          #   print(False, name, cuisines, r)

    # print(self.N, c, n, c/n*100, sco/c)
    return [n, c/n if n != 0 else 0]


# CSV data from overpass query
"""
[out:csv(amenity,cuisine,takeaway,name)][timeout:2500];
{{geocodeArea:France}}->.searchArea;
nwr["amenity"~"restaurant|fast_food"]["name"]["cuisine"](area.searchArea);
out;
"""


def optimize():
  from scipy.optimize import minimize # type: ignore

  cuisine = Cuisine(sys.argv[1], evaluation=0.9)

  def f(c):
    c2, c3, c4 = c
    for s in [0.3, 0.4, 0.5, 0.6, 1]:
      n, r = cuisine.evaluate(1, c2, c3, c4, s)
      if r > 0.75:
        return -n
    return 0

  x0 = [2.02414594, 0.1519341, 0.14086179]
  res = minimize(f, x0, method='nelder-mead', options={'xatol': 1e-8, 'disp': True})
  print(res)

  r = cuisine.evaluate(1, *res.x, 0.5)
  print(0.5)
  print(r)

  r = cuisine.evaluate(1, *res.x, 0.6)
  print(0.6)
  print(r)

  r = cuisine.evaluate(1, *res.x, 0.7)
  print(0.7)
  print(r)

  print(res.x)


if __name__ == "__main__":
  optimize()
