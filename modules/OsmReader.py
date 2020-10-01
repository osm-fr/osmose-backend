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

import sys
from .OsmState import OsmState
from abc import abstractmethod
from typing import Optional


class OsmReader:
    def log(self, txt):
        self._logger.log(txt)

    def __init__(self, pbf_file: str, logger, state_file: Optional[OsmState] = None):
        pass

    def is_change(self) -> bool:
        return False

    def set_filter_since_timestamp(self, since_timestamp) -> None:
        pass

    def timestamp(self):
        pass

    @abstractmethod
    def CopyTo(self, output) -> None:
        pass


class dummylog:
    def log(self, text):
        return


def open(osm: str, logger = dummylog(), state_file: Optional[OsmState] = None) -> OsmReader:
    if osm.endswith(".pbf"):
        from .OsmPbf import OsmPbfReader
        return OsmPbfReader(osm, logger, state_file)
    elif (osm.endswith(".osc") or
          osm.endswith(".osc.gz") or
          osm.endswith(".osc.bz2")):
        from .OsmSax import OscSaxReader
        return OscSaxReader(osm, logger, state_file)
    elif (osm.endswith(".osm") or
          osm.endswith(".osm.gz") or
          osm.endswith(".osm.bz2")):
        from .OsmSax import OsmSaxReader
        return OsmSaxReader(osm, logger, state_file)
    elif osm == '-':
        from .OsmSax import OsmSaxReader
        return OsmSaxReader(sys.stdin, logger, state_file)
    else:
        raise Exception('File extension "{0}" is not recognized'.format(osm))
