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

        self.taster = Cuisine('dictionaries/Lang_fr/cuisine.csv')

    def node(self, data, tags):
        if 'name' not in tags or tags.get('amenity') not in ('restaurant', 'fast_food'):
            return

        cuisines = set(map(lambda s: s.strip(), tags.get('cuisine', []).split(';')))
        cuisine_guess = guess_prune(self.taster, cuisines, tags['name'], tags['amenity'], tags.get('takeaway'), tags.get('brand'))
        if cuisine_guess:
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
