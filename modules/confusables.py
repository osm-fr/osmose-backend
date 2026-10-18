###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2016                                      ##
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

from . import confusables_data

def unconfuse(char, script):
    group = confusables_data.confusables.get(char)
    if group:
        return confusables_data.confusables_fix.get(group).get(script)


###########################################################################
import unittest

class Test(unittest.TestCase):

    def test_Latin(self):
        for (c, exp) in [ ('!', 'ǃ'),
                          ('॰', None),
                          ('ﺓ', 'ö'),
                          ('_', None),
                          ('ƅ', 'ƅ'),
                          ('𝐷', None),
                          ('2', None),
                          ('𝟱', 'Ƽ'),
                        ]:
            self.assertEqual(unconfuse(c, "Latin"), exp)

    def test_Cyrillic(self):
        for (c, exp) in [ ('!', None),
                          ('॰', None),
                          ('ﺓ', None),
                          ('_', None),
                          ('ƅ', 'ь'),
                          ('2', 'Ꙅ'),
                          ('𝟱', None),
                        ]:
            self.assertEqual(unconfuse(c, "Cyrillic"), exp)

    def test_diff_char(self):
        # check that confusables_data doesn't propose the same character
        import regex
        wrong = 0
        for group in confusables_data.confusables.values():
            proposals = confusables_data.confusables_fix.get(group)
            for (script, prop) in proposals.items():
                re = regex.compile(r"[\p{%s}]" % script, flags=regex.V1 | regex.U)
                if re.match(prop):
                    pass
                elif group == prop:
                    wrong += 1
                    print("group=%s, script=%s, prop=%s" % (group, script, prop))
        assert wrong == 0
