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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin

from .modules.Cuisine_Guess_lib import Cuisine, guess_prune


class Cuisine_Guess(Plugin):

    only_for = ["FR", "ES"]
    not_for = [
        "FR-GP", "FR-GF", "FR-YT", "FR-RE", "FR-BL", "FR-MF", "FR-PM", "FR-WF", "FR-PF",
    ]

    def init(self, logger):
        Plugin.init(self, logger)
        detail = '''Using statistics based on amenity name, amenity tag value and takeaway tag, guess a possible value for `cuisine` tag.'''
        self.errors[1] = self.def_class(item = 3270, level = 3, tags = ['fix:survey'],
            title = T_('Possible mistake or lack of precision of `cuisine` value'),
            detail = T_(detail))
        self.errors[2] = self.def_class(item = 3270, level = 3, tags = ['fix:survey'],
            title = T_('Suggestion of `cuisine` value'),
            detail = T_(detail))

        country = self.father.config.options.get("country")
        if country is None:
            return None

        country_csv = {
            'ES': 'dictionaries/es/cuisine.csv',
            'FR': 'dictionaries/fr/cuisine.csv',
        }.get(country.split('-', 1)[0])
        if country_csv is None:
            return None

        self.local_cuisines = self.father.config.options.get("local_cuisines")
        if self.father.config.options.get("test"):
            # Make learning very fast
            self.taster = Cuisine(country_csv, self.local_cuisines, train_size=0.1, ngram=2)
        else:
            self.taster = Cuisine(country_csv, self.local_cuisines)

    def full(self, cuisines, actions):
        for action in actions:
            if action[0][0]:
                cuisines = self.remove(cuisines, action[0][0])
            if action[0][1]:
                cuisines = list(cuisines)
                cuisines.append(action[0][1])
        return cuisines

    def replace(self, cuisines, a, b):
        return map(lambda c: b if c == a else c, cuisines)

    def remove(self, cuisines, a):
        return filter(lambda c: c != a, cuisines)

    def node(self, data, tags):
        if 'name' not in tags or tags.get('amenity') not in ('restaurant', 'fast_food'):
            return

        cuisines = list(map(lambda s: s.strip(), tags['cuisine'].split(';'))) if 'cuisine' in tags else set()
        cuisine_guess = guess_prune(self.taster, self.local_cuisines, set(cuisines), tags['name'], tags['amenity'], tags.get('takeaway'), tags.get('brand'))
        guess_number = len(cuisine_guess.get('probable_subclass', [])) + len(cuisine_guess.get('probable_others', [])) + len(cuisine_guess.get('improbable', []))
        if guess_number > 0:
            full_cusine = list(self.full(cuisines, cuisine_guess.get('probable_subclass', []) + cuisine_guess.get('probable_others', []) + cuisine_guess.get('improbable', []))) if guess_number <= 3 else []
            return {'class': 1 if 'cuisine' in tags else 2,
                'text': T_('Guess with probability: {0}', ', '.join(
                    list(map(
                        lambda cs: 'sub kind "{0}" -> "{1}" ({2}%)'.format(cs[0][0], cs[0][1], round(cs[1] * 100, 1)),
                        cuisine_guess.get('probable_subclass', [])
                    )) +
                    list(map(
                        lambda cs: '"{0}" ({1}%)'.format(cs[0][1], round(cs[1] * 100, 1)),
                        cuisine_guess.get('probable_others', [])
                    )) +
                    list(map(
                        lambda cs: 'impropable {0} ({1}%)'.format(cs[0][0], round(cs[1] * 100, 1)),
                        cuisine_guess.get('improbable', [])
                    ))
                )),
                'fix':
                    ([{'~': {'cuisine': ';'.join(full_cusine) }}] if len(full_cusine) > 0 else []) +
                    ([{'~': {'cuisine': ';'.join(self.replace(cuisines, guess[0][0], guess[0][1]))}} for guess in cuisine_guess.get('probable_subclass', [])] if guess_number >= 2 else []) +
                    ([{'~': {'cuisine': ';'.join(list(cuisines) + [guess[0][1]])}} for guess in cuisine_guess.get('probable_others', [])] if guess_number >= 2 else []) +
                    ([{'~': {'cuisine': ';'.join(self.remove(cuisines, guess[0][0]))}} for guess in cuisine_guess.get('improbable', [])] if guess_number >= 2 else [])
            }

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon
from plugins.Plugin import with_options # noqa

class Test(TestPluginCommon):
    def test(self):
        a = Cuisine_Guess(None)
        class _config:
            options = {'test': True, 'country': 'FR', 'language': None, 'local_cuisines': ['french']}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert a.node(None, {"amenity": "restaurant", "name": "Fujiyama"})
        assert not a.node(None, {"amenity": "restaurant", "name": "wwwwwwwwwwwww"})
