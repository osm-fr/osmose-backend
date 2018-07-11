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

import inspect
import time
import hashlib


def version(*sources):
    h = hashlib.md5()
    for source in sources:
        if isinstance(source, int):
            h.update(str(source))
        elif inspect.isclass(source):
            cc = inspect.getmro(source)
            cc = cc[:-3]
            for c in cc:
                h.update(open(inspect.getfile(c)).read())
        else:
            raise NotImplementedError(source.__class__)

    return int(h.hexdigest(), 16) % 2147483647
