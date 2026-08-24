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
import random
from collections import defaultdict
from unidecode import unidecode

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder


# Non-cuisine tags to drop entirely
_CUISINE_DROP = ['buffet', 'dessert', 'cake', 'world', 'bio']

# i10n / synonyms: token -> list of replacement tokens
_CUISINE_SYNONYMS = {
  'japonais': ['japanese'],
  'vietnam': ['vietnamese'],
  'indien': ['indian'],
  'italian_pizza': ['italian', 'pizza'],
}

# Common mistake / implicit association: trigger -> list of cuisines to add
_CUISINE_IMPLIES = {
  'sushi': ['japanese'],
  'japanese': ['sushi'],
  'pizza': ['italian'],
  'tacos': ['mexican'],
}


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

      # remove non-cuisine tags
      for tag in _CUISINE_DROP:
        if tag in cuisines:
          cuisines.remove(tag)

      # i10n / synonyms
      for old, new in _CUISINE_SYNONYMS.items():
        if old in cuisines:
          cuisines.remove(old)
          cuisines.extend(new)

      # Common mistake / implied cuisines
      for trigger, implied in _CUISINE_IMPLIES.items():
        if trigger in cuisines:
          cuisines.extend(implied)

      return cuisines

  multiple_space = re.compile(' +')

  @staticmethod
  def expland_name(text):
    text = text.lower()
    text = unidecode(text)
    text = text.strip()
    text = text.replace("'", '')
    text = text.translate(str.maketrans(' ', ' ', string.punctuation)) # Remove punctuation
    text = text.translate(str.maketrans(' ', ' ', '0123456789')) # Remove digits
    text = Cuisine.multiple_space.sub(' ', text)
    text = ' '.join(filter(lambda t: len(t) > 1 and t not in ('le',), text.split(' ')))
    text = '  ' + text + '  '
    return text

  @staticmethod
  def enumerate_word(text):
    return list(filter(lambda w: len(w) >= 3, text.strip().split(' ')))

  @staticmethod
  def enumerate_amenity(amenity):
    return list(sorted(set(map(lambda s: s.strip(), amenity.split(';'))).intersection(set(['fast_food', 'restaurant']))))

  @staticmethod
  def enumerate_takeaway(takeaway):
    return [takeaway and takeaway != 'no']

  @staticmethod
  def enumerate_brand(brand):
    if brand:
      return brand.strip()

  def __init__(self, cuisine_csv, evaluation=0):
    self.N = 3

    self.data = self.load_csv(cuisine_csv)

    if evaluation:
      random.shuffle(self.data)
      self.data_slice = round(len(self.data) * evaluation)
    else:
      self.data_slice = -1

    # Count "cuisine" occurrences and remove unfrequented ones
    coef = defaultdict(int)

    for row in self.data[0:self.data_slice]:
      if row['cuisine']:
        for cuisine in self.expland_cuisine(row['cuisine']):
          coef[cuisine] += 1

    self.keep_cuisines = {k for k, v in coef.items() if v >= 8} # Remove unfrequented "cuisine"
    # Build the training rows: (name, amenity, takeaway, brand) -> set of cuisines
    rows = []
    labels = []
    for row in self.data[0:self.data_slice]:
      name = row['name']
      if row['cuisine'] and len(name) >= self.N + 1:
        cuisines = self.expland_cuisine(row['cuisine']) & self.keep_cuisines
        if cuisines:
          rows.append({
              'name': self.expland_name(name),
              'amenity': ';'.join(self.enumerate_amenity(row['amenity'])) or 'unknown',
              'takeaway': str(self.enumerate_takeaway(row['takeaway'])[0]),
              'brand': self.enumerate_brand(row['brand']) or 'unknown',
          })
          labels.append(cuisines)

    preprocessor = ColumnTransformer([
        # Use min_df>=2 to ignore ngrams or words that appear only once in the training set
        # Which are likely to be typos or very specific names. Lower the classifer size.
        ('name_ngram', TfidfVectorizer(analyzer='char', ngram_range=(self.N, self.N), min_df=5), 'name'),
        ('name_word', TfidfVectorizer(analyzer='word', token_pattern=r'(?u)\b\w{3,}\b', min_df=5), 'name'),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['amenity', 'takeaway', 'brand']),
    ])
    self.pipeline = Pipeline([
        ('prep', preprocessor),
        ('clf', OneVsRestClassifier(LogisticRegression(C=1.0, class_weight='balanced', max_iter=1000))),
    ])

    self.mlb = MultiLabelBinarizer(classes=sorted(self.keep_cuisines))
    X = pd.DataFrame(rows)
    y = self.mlb.fit_transform(labels)

    # Train the model
    self.pipeline.fit(X, y)
    self.print_feature_importance()

    # - OR -

    # # Optimize model hyperparameters using grid search and cross-validation
    # # Note: This is commented out to avoid long training times during normal execution.
    # from sklearn.model_selection import GridSearchCV
    # param_grid = {
    #   'prep__name_ngram__min_df': [2],  # [1, 2],
    #   'prep__name_ngram__ngram_range': [(3, 4)],  # [(3, 3), (3, 4), (4, 4)],
    #   'prep__name_word__min_df': [2],  # [1, 2, 3, 4, 5],
    #   'clf__estimator__C': [1.0],  # [1.0, 2.0, 5.0, 10.0],
    # }
    # grid_search = GridSearchCV(self.pipeline, param_grid, scoring='f1_micro', cv=3, n_jobs=-1)
    # grid_search.fit(X, y)
    # self.grid_search = grid_search
    # self.pipeline = grid_search.best_estimator_

    # print('Best hyperparameters selected by grid search:')
    # print(grid_search.best_params_)
    # print('Best cross-validation f1_micro score:', grid_search.best_score_)

  def print_feature_importance(self):
    """Print, per feature group (name n-grams/words, amenity, takeaway,
    brand), the mean and max absolute coefficient
    magnitude across all cuisine classifiers. This is a proxy for how much
    each input actually contributes to the predictions."""
    import numpy as np

    feature_names = self.pipeline.named_steps['prep'].get_feature_names_out()
    clf = self.pipeline.named_steps['clf']

    groups = defaultdict(list)
    for i, fname in enumerate(feature_names):
      for group in ('amenity', 'takeaway', 'brand'):
        if fname.startswith('cat__' + group):
          groups[group].append(i)
          break
      else:
        if fname.startswith('name_ngram'):
          groups['name_ngram'].append(i)
        elif fname.startswith('name_word'):
          groups['name_word'].append(i)

    all_coefs = np.vstack([est.coef_[0] for est in clf.estimators_])
    mean_abs_coef = np.abs(all_coefs).mean(axis=0)

    print('Feature importance (mean/max |coefficient| across all cuisine classifiers):')
    print(f"{'group':<18} {'#features':<10} {'mean |coef|':<14} {'max |coef|'}")
    for group, idxs in sorted(groups.items(), key=lambda kv: -mean_abs_coef[kv[1]].mean()):
      idxs = np.array(idxs)
      print(f"{group:<18} {len(idxs):<10} {mean_abs_coef[idxs].mean():<14.4f} {mean_abs_coef[idxs].max():.4f}")

  def guess_score(self, name, amenity, takeaway, brand):
    X = pd.DataFrame([{
      'name': self.expland_name(name),
      'amenity': ';'.join(self.enumerate_amenity(amenity)) or 'unknown',
      'takeaway': str(self.enumerate_takeaway(takeaway)[0]),
      'brand': self.enumerate_brand(brand),
    }])
    probas = self.pipeline.predict_proba(X)[0]
    return dict(zip(self.mlb.classes_, probas))

  def guess(self, name, amenity, takeaway, brand, s=0.5):
    g = self.guess_score(name, amenity, takeaway, brand)
    return dict(filter(lambda c: c[1] > s, g.items()))

  def evaluate(self, s):
    n = 0
    c = 0
    sco = 0
    for row in self.data[self.data_slice:-1]:
      name = row['name']
      cuisines = self.expland_cuisine(row['cuisine'])
      if cuisines and len(name) >= self.N + 1:
        r = self.guess(name, row['amenity'], row['takeaway'], row['brand'], s)

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


# CSV data from extract query
"""
wget https://download.geofabrik.de/europe/france-latest.osm.pbf
curl "https://polygons.openstreetmap.fr/get_poly.py?id=1403916&params=0" > france-metropolitan.poly
osmium tags-filter france-latest.osm.pbf nwr/cuisine --omit-referenced -f pbf > france-cuisine.osm.pbf
osmium tags-filter france-cuisine.osm.pbf nwr/name --omit-referenced -f pbf > france-cuisine-name.osm.pbf
osmium tags-filter france-cuisine-name.osm.pbf nwr/amenity=restaurant,fast_food --omit-referenced -f pbf > france-cuisine-name-amenity.osm.pbf
osmium extract france-cuisine-name-amenity.osm.pbf --strategy=simple --polygon=france-metropolitan.poly -f pbf > france-cuisine-name-amenity-metropolitan.osm.pbf
osmium export france-cuisine-name-amenity-metropolitan.osm.pbf -f geojson \
  | jq -r '.features[] | [.properties.amenity, .properties.cuisine, .properties.takeaway, .properties.name, .properties.brand] | @tsv' \
  | sort \
  > cuisine-france-metropolitan.csv
rm *.osm.pbf france-metropolitan.poly
"""


def optimize():
  cuisine = Cuisine(sys.argv[1], evaluation=0.9)

  for s in [0.6, 0.7, 0.8, 0.9, 1]:
    r = cuisine.evaluate(s)
    print(s)
    print(r)


if __name__ == "__main__":
  optimize()
