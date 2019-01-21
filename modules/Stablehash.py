#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2018                                      ##
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

import hashlib


def stablehash(s):
    """
    Compute a stable positive integer hash on 32bits
    @param s: a string
    """
    return int(abs(int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)) % 2147483647)


def hexastablehash(s):
    """
    Compute a stable hexa hash
    @param s: a string
    """
    return hashlib.md5(s.encode('utf-8')).hexdigest()


###########################################################################
import unittest

class Test(unittest.TestCase):
    def test_stablehash(self):
        h1 = stablehash( "toto")
        h2 = stablehash(u"toto")
        h3 = stablehash(u"é")
        self.assertEquals(h1, h2)
        self.assertNotEquals(h1, h3)
