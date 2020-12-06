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

from .modules import Cuisine_Guess_lib


class Cuisine_Guess(Plugin):

    only_for = ["FR"]

    def init(self, logger):
        Plugin.init(self, logger)
        detail = '''Using statistics based on amenity name, amenity tag value and takeaway tag, guess a possible value for `cuisine` tag.'''
        self.errors[1] = self.def_class(item = 3270, level = 3, tags = ['fix:survey'],
            title = T_('Possible mistake or lack of precision of `cuisine` value'),
            detail = T_(detail))
        self.errors[2] = self.def_class(item = 3270, level = 3, tags = ['fix:survey'],
            title = T_('Suggestion of `cuisine` value'),
            detail = T_(detail))

        self.taster = Cuisine_Guess_lib.Cuisine('dictionaries/FR/cuisine.csv')

    def node(self, data, tags):
        if 'name' not in tags or tags.get('amenity') not in ('restaurant', 'fast_food'):
            return

        cuisine_guess = self.taster.guess(tags['name'], tags['amenity'], tags.get('takeaway'))
        if cuisine_guess:
            tasty_cuisines = None
            if 'cuisine' in tags:
                max_score = max(map(lambda c: c[1], cuisine_guess.items()))
                if max_score < 0.9:
                    tasty_cuisines = True
                else:
                    cuisines = set(map(lambda s: s.strip(), tags['cuisine'].split(';')))
                    tasty_cuisines = cuisines.intersection(set(map(lambda c: c[0], cuisine_guess.items())))

            if not tasty_cuisines:
                return {'class': 1 if 'cuisine' in tags else 2,
                    'text': T_('Guess with probability: {0}', ', '.join(map(lambda cs: '{0} ({1}%)'.format(cs[0], round(cs[1] * 100)), cuisine_guess.items()))),
                    'fix': [{'~': {'cuisine': cuisine[0]}} for cuisine in cuisine_guess.items()]
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
