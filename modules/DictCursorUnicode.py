#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2017                                      ##
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

import psycopg2.extras
import sys


class DictRowUnicode50(psycopg2.extras.DictRow):
    def __getitem__(self, x):
        if sys.version_info < (3, ):
            # Hack to make DictRow support of unicode key in Pyhton 2
            if isinstance(x, unicode):
                return super(DictRowUnicode50, self).__getitem__(x[:50].encode('utf-8'))
            elif isinstance(x, str):
                return super(DictRowUnicode50, self).__getitem__(x.decode('utf-8')[:50].encode('utf-8'))
            else:
                return super(DictRowUnicode50, self).__getitem__(x)
        else:
            if isinstance(x, str):
                return super(DictRowUnicode50, self).__getitem__(x[:50])
            else:
                return super(DictRowUnicode50, self).__getitem__(x)

class DictCursorUnicode50(psycopg2.extras.DictCursor):
    def __init__(self, *args, **kwargs):
         # Overwrite row_factory from parent psycopg2.extras.DictCursor
        kwargs['row_factory'] = DictRowUnicode50
        psycopg2.extras.DictCursorBase.__init__(self, *args, **kwargs)
        self._prefetch = 1
