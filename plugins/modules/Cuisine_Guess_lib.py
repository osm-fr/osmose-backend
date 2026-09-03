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
from collections import defaultdict
from unidecode import unidecode
import joblib
from modules import downloader, SourceVersion
from typing import Dict, List, Optional, Any, Set, Iterable, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder


class Cuisine:
  # Non-cuisine tags to drop entirely
  _CUISINE_DROP: List[str] = [
      'buffet', 'dessert',
      'cake', 'ice_cream',
      'coffee_shop', 'wine', 'bubble_tea', 'juice', 'tea',
      'regional', 'local', 'traditional',
      'world', 'bio',
  ]

  # i10n / synonyms: token -> list of replacement tokens
  _CUISINE_SYNONYMS: Dict[str, List[str]] = {
      'japonais': ['japanese'],
      'vietnam': ['vietnamese'],
      'indien': ['indian'],
      'italian_pizza': ['italian', 'pizza'],
      'pancake': ['savory_pancakes'],
      'pancakes': ['savory_pancakes'],
  }

  _CUISINE_HIERARCHY: Dict[str, Dict[str, Optional[Dict[str, Any]]]]  = {
      "maghrebi": {
          "algerian": None,
          "moroccan": None,
          "tunisian": None,
          "couscous": None,
          "tajine": None,
      },
      "oriental": {
          "afghan": None,
          "arab": None,
          "lebanese": None,
          "persian": None,
          "syrian": None,
          "turkish": {
              "kebab": None,
          },
      },
      "african": {
          "senegalese": None,
      },
      "american": {
          "burger": None,
          "diner": None,
          "fried_chicken": None,
          "hotdog": None,
          "wings": None,
      },
      "mexican": {
          "tacos": None,
      },
      "spanish": {
          "basque": None,
          "basque_ciderhouse": None,
          "catalan": None,
          "churro": None,
          "galician": None,
          "paella": None,
          "tapas": None,
          "valencian": None,
          "vasca": None,
      },
      "asian": {
          "cambodian": None,
          "chinese": None,
          "indian": {
              "curry": None,
              "naan": None,
          },
          "tibetan": None,
          "pakistani": None,
          "indonesian": None,
          "japanese": {
              "ramen": None,
              "sushi": None,
          },
          "korean": None,
          "lao": None,
          "nepalese": None,
          "sri_lankan": None,
          "taiwanese": None,
          "thai": None,
          "vietnamese": None,
      },
      "caribbean": {
          "creole": None,
      },
      "latin_american": {
          "argentinian": None,
          "brazilian": None,
          "colombian": None,
          "peruvian": None,
          "venezuelan": None,
          "empanada": None,
          "arepa": None,
      },
      "italian": {
          "pasta": None,
          "pizza": None,
      },
      "hawaiian": {
          "poke": None,
      },
      "meat": {
          "steak_house": None,
          "barbecue": None,
      },
      "friture": {
          "fries": None
      },
      "seafood": {
          "fish": None,
      },
  }

  @staticmethod
  def _flatten_reversed_cuisine_hierarchy(hierarchy, parent=None) -> Dict[str, str]:
    def rec(hierarchy, parent):
      parents = {}
      for cuisine, children in hierarchy.items():
        if parent is not None:
          parents[cuisine] = parent
        if isinstance(children, dict):
          parents.update(rec(children, cuisine))
      return parents
    return rec(hierarchy, parent)

  _CUISINE_PARENTS: Dict[str, str] = _flatten_reversed_cuisine_hierarchy(_CUISINE_HIERARCHY)

  @staticmethod
  def _flatten_cuisine_hierarchy(hierarchy) -> Dict[str, Set[str]]:
    def rec(hierarchy):
      parents = {}
      for cuisine, children in hierarchy.items():
        if isinstance(children, dict):
          parents[cuisine] = children.keys()
          parents = dict(parents, **rec(children))
      return parents
    return rec(hierarchy)

  _CUISINE_CHILDREN: Dict[str, Set[str]] = _flatten_cuisine_hierarchy(_CUISINE_HIERARCHY)

  @staticmethod
  def _expand_ancestors(cuisines: Set[str]) -> Set[str]:
    result = set(cuisines)
    for cuisine in cuisines:
      parent = Cuisine._CUISINE_PARENTS.get(cuisine)
      while parent:
        result.add(parent)
        parent = Cuisine._CUISINE_PARENTS.get(parent)
    return result

  @staticmethod
  def load_csv(file_path: str) -> Iterable[Dict[str, str]]:
    with open(file_path) as csvfile:
      return list(csv.DictReader(csvfile, delimiter="\t"))

  @staticmethod
  def expland_cuisine(cuisine: str, local_cuisine: List[str]) -> Set[str]:
    cuisine = cuisine.lower()
    cuisines = set(map(lambda s: s.strip(), cuisine.split(';')))

    # remove non-cuisine tags
    for tag in Cuisine._CUISINE_DROP + local_cuisine:
      if tag in cuisines:
        cuisines.remove(tag)

    # i10n / synonyms
    for old, new in Cuisine._CUISINE_SYNONYMS.items():
      if old in cuisines:
        cuisines.remove(old)
        for n in new:
          cuisines.add(n)

    # Common mistake / implied cuisines
    cuisines = Cuisine._expand_ancestors(cuisines)

    return cuisines

  multiple_space = re.compile(' +')

  @staticmethod
  def expland_name(text: str) -> str:
    text = text.lower()
    text = unidecode(text)
    text = text.strip()
    text = text.replace("'", '')
    text = text.translate(str.maketrans(' ', ' ', string.punctuation)) # Remove punctuation
    text = text.translate(str.maketrans(' ', ' ', '0123456789')) # Remove digits
    text = Cuisine.multiple_space.sub(' ', text)
    text = ' '.join(filter(lambda t: len(t) > 1 and t not in ('le',), text.split(' ')))
    text = ' ' + text + ' '
    return text

  @staticmethod
  def make_row(name: str, amenity: str, takeaway: Optional[str], brand: Optional[str]) -> Dict[str, Optional[str]]:
    if amenity:
      amenity = ';'.join(sorted(set(map(lambda s: s.strip(), amenity.split(';'))).intersection(set(['fast_food', 'restaurant']))))
    else:
      amenity = 'unknown'

    return {
        'name': Cuisine.expland_name(name),
        'amenity': amenity,
        'takeaway': str(takeaway and takeaway != 'no'),
        'brand': brand.strip() if brand else 'unknown',
    }

  def __init__(self, cuisine_csv: str, local_cuisines: Optional[List[str]], s: float = 0.95, use_cache: bool = True, train_size: Optional[float] = None, ngram: int = 4):
    self.local_cuisines = local_cuisines or []
    self.N = ngram

    cache_path = downloader.get_cache_path(cuisine_csv, str(SourceVersion.version(cuisine_csv, Cuisine, self.N, train_size)))
    if use_cache:
      try:
        loaded = joblib.load(cache_path)
        self.__dict__.update(loaded)
        return
      except FileNotFoundError:
        pass

    csv_data = self.load_csv(cuisine_csv)
    if train_size is not None:
      self.train_data, self.test_data = train_test_split(csv_data, random_state=0, train_size=train_size if train_size > 0 else 0.9)
    else:
      self.train_data, self.test_data = csv_data, []

    # Count "cuisine" occurrences and remove unfrequented ones
    coef: Dict[str, int] = defaultdict(int)

    for row in self.train_data:
      if row['cuisine']:
        for cuisine in self.expland_cuisine(row['cuisine'], self.local_cuisines):
          coef[cuisine] += 1

    keep_cuisines = {k for k, v in coef.items() if v >= 20} # Remove unfrequented "cuisine"
    # Build the training rows: (name, amenity, takeaway, brand) -> set of cuisines
    rows = []
    labels = []
    for row in self.train_data:
      name = row['name']
      if row['cuisine'] and len(name) >= self.N + 1:
        cuisines = self.expland_cuisine(row['cuisine'], self.local_cuisines) & keep_cuisines
        if cuisines:
          rows.append(self.make_row(name, row['amenity'], row['takeaway'], row['brand']))
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

    self.mlb = MultiLabelBinarizer(classes=sorted(keep_cuisines))
    X = pd.DataFrame(rows)
    y = self.mlb.fit_transform(labels)

    # Train the model
    self.pipeline.fit(X, y)
    self.print_feature_importance()
    print(self.classification_report(s, keep_cuisines))
    if train_size is not None:
      print(self.classification_report(s, keep_cuisines))

    if use_cache:
      joblib.dump({
          "pipeline": self.pipeline,
          "mlb": self.mlb,
      }, cache_path)

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

  def guess_score(self, name: str, amenity: str, takeaway: Optional[str], brand: Optional[str]) -> Dict[str, float]:
    X = pd.DataFrame([self.make_row(name, amenity, takeaway, brand)])
    probas = self.pipeline.predict_proba(X)[0]
    return dict(zip(self.mlb.classes_, probas))

  def classification_report(self, s: float, keep_cuisines: Set[str]):
    """Precision/recall/F1 per cuisine on the full test set, using
    scikit-learn's classification_report instead of the single aggregate
    score computed by evaluate()."""
    rows = []
    labels = []
    for row in self.test_data:
      name = row['name']
      cuisines = self.expland_cuisine(row['cuisine'], self.local_cuisines) & keep_cuisines
      if cuisines and len(name) >= self.N + 1:
        rows.append(self.make_row(name, row['amenity'], row['takeaway'], row['brand']))
        labels.append(cuisines)

    X = pd.DataFrame(rows)
    y_true = self.mlb.transform(labels)
    y_pred = (self.pipeline.predict_proba(X) > s).astype(int)

    return classification_report(y_true, y_pred, target_names=self.mlb.classes_, zero_division=0)


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

def guess_prune(teaster: Cuisine, cuisines: Set[str], name: str, amenity: str, takeaway: Optional[str], brand: Optional[str], s: float = 0.95) -> Dict[str, List[Tuple[Tuple[Optional[str], Optional[str]], float]]]:
  g = teaster.guess_score(name, amenity, takeaway, brand)

  probable_g = dict(filter(lambda c: c[0] not in cuisines and c[1] > s, g.items()))

  if not cuisines:
    return {
        "probable_others": list(map(lambda cs: ((None, cs[0]), cs[1]), probable_g.items()))
    }
  else:
    improbable_g = dict(filter(lambda c: c[0] in cuisines and c[1] <= 1 - s, g.items()))

    ret: Dict[str, List[Tuple[Tuple[Optional[str], Optional[str]], float]]] = {
        "probable_subclass": [],
        "probable_others": [],
        "improbable": [],
    }
    for cuisine, coef in probable_g.items():
      children = Cuisine._CUISINE_CHILDREN.get(cuisine, [])
      if cuisines.intersection(children):
        continue

      # The cuisine has a parent, but the parent is the not the parent of an other initial cuisines (sibling cuisine)
      parent = Cuisine._CUISINE_PARENTS.get(cuisine)
      if parent in cuisines:
        if not cuisines.intersection(Cuisine._CUISINE_CHILDREN.get(parent)):
          ret['probable_subclass'].append(((parent, cuisine), coef))
      else:
        ret['probable_others'].append(((None, cuisine), coef))
    for cuisine, coef in improbable_g.items():
      ret['improbable'].append(((cuisine, None), coef))
    return dict(filter(lambda cs: len(cs[1]) > 0, ret.items()))

def evaluate(taster: Cuisine, local_cuisines: Optional[List[str]], s: float):
  n = 0
  c = 0
  for row in taster.test_data:
    name = row['name']
    cuisines = taster.expland_cuisine(row['cuisine'], local_cuisines or [])
    if cuisines and len(name) >= taster.N + 1:
      r = taster.guess_score(name, row['amenity'], row['takeaway'], row['brand'])
      r = dict(filter(lambda c: c[1] > s, r.items()))

      if r:
        n += 1
        m = False
        for cuisine, score in r.items():
          if cuisine in cuisines:
            c += 1
            # print(True, name, cuisines, r)
            m = True
            break
          # else:
          #   print(cuisines, cuisine)

        if not m:
          print(False, name, cuisines, r)

        p = guess_prune(taster, cuisines, name, row['amenity'], row['takeaway'], row['brand'], s)
        if p:
          print('     ', name, cuisines, p)

  return [n, c/n if n != 0 else 0]

def optimize():
  csv_path = sys.argv[1]
  local_cuisines = sys.argv[2].split(';')
  cuisine = Cuisine(csv_path, local_cuisines, s=0.95, use_cache=False, train_size=-1, ngram=3)

  for s in [0.95]:
    r = evaluate(cuisine, local_cuisines, s)
    print(s)
    print(r)

if __name__ == "__main__":
  optimize()
