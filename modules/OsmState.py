#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2017                                      ##
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

import dateutil.parser

###########################################################################

class dummylog:
    def log(self, text):
        return

###########################################################################

class OsmState:

  def __init__(self, state_file, logger = dummylog()):
    self._state_file = state_file
    self._logger = logger
    self._timestamp = None

    with open(state_file, 'r') as f:
      state_lines = f.readlines()
      for line in state_lines:
        logger.log("state: {0}".format(line))
        if line.startswith("timestamp="):
          s = line.replace('\\', '')
          self._timestamp = dateutil.parser.parse(s[len("timestamp="):]).replace(tzinfo=None)


  def timestamp(self):
    return self._timestamp

###########################################################################
import unittest

class Test(unittest.TestCase):
  def test_state(self):
    import datetime

    s = OsmState("tests/state1.txt")
    exp = datetime.datetime(2010, 10, 29, 23, 0, 0, 0, None)
    self.assertEqual(s.timestamp(), exp, "got=%s, exp=%s" % (s.timestamp(), exp))

    s = OsmState("tests/state2.txt")
    exp = datetime.datetime(2017, 9, 3, 16, 47, 2, 0, None)
    self.assertEqual(s.timestamp(), exp, "got=%s, exp=%s" % (s.timestamp(), exp))

    s = OsmState("tests/state3.txt")
    exp = datetime.datetime(2017, 9, 2, 20, 43, 2, 0, None)
    self.assertEqual(s.timestamp(), exp, "got=%s, exp=%s" % (s.timestamp(), exp))
