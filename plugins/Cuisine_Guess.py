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

        self.taster = Cuisine('dictionaries/Lang_fr/cuisine.csv', use_cache=False, ngram=3)

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
        cuisine_guess = guess_prune(self.taster, cuisines, tags['name'], tags['amenity'], tags.get('takeaway'), tags.get('brand'))
        guess_number = len(cuisine_guess.get('probable_subclass', [])) + len(cuisine_guess.get('probable_others', [])) + len(cuisine_guess.get('improbable', []))
        if guess_number > 0:
            return {'class': 1 if 'cuisine' in tags else 2,
                'text': T_('Guess with probability: {0}', ', '.join(
                    list(map(
                        lambda cs: 'sub kind "{0}" -> "{1}" ({2}%)'.format(cs[0][0], cs[0][1], round(cs[1] * 100)),
                        cuisine_guess.get('probable_subclass', [])
                    )) +
                    list(map(
                        lambda cs: '"{0}" ({1}%)'.format(cs[0][1], round(cs[1] * 100)),
                        cuisine_guess.get('probable_others', [])
                    )) +
                    list(map(
                        lambda cs: 'impropable {0} ({1}%)'.format(cs[0][0], round(cs[1] * 100)),
                        cuisine_guess.get('improbable', [])
                    ))
                )),
                'fix': [
                    (list({'~': {'cuisine': ';'.join(self.full(cuisines, cuisine_guess.get('probable_subclass', []) + cuisine_guess.get('probable_others', []) + cuisine_guess.get('improbable', []))) }}) if guess_number <= 3 else []) +
                    (list({'~': {'cuisine': ';'.join(self.replace(cuisines, guess[0][0], guess[0][1]))}} for guess in cuisine_guess.get('probable_subclass', [])) if guess_number >= 2 else []) +
                    (list({'~': {'cuisine': ';'.join(list(cuisines) + [guess[0][1]])}} for guess in cuisine_guess.get('probable_others', [])) if guess_number >= 2 else []) +
                    (list({'~': {'cuisine': ';'.join(self.remove(cuisines, guess[0][0]))}} for guess in cuisine_guess.get('improbable', [])) if guess_number >= 2 else [])
                ]
            }

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Cuisine_Guess(None)
        a.init(None)
        assert a.node(None, {"amenity": "restaurant", "name": "Fujiyama"})
        assert not a.node(None, {"amenity": "restaurant", "name": "lkgverjverkj"})
