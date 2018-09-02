#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

from plugins.Plugin import Plugin


# Largely inspired from
# https://github.com/keepright/keepright/blob/master/checks/0210_loopings.php

class Structural_DuplicateNodes(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[103] = { "item": 1010, "level": 2, "tag": ["geom", "fix:chair"], "desc": T_(u"Duplicated nodes") }

    def way(self, data, tags, nds):
        c = {}
        twice = 0
        max_ = 0
        for n in nds:
            c[n] = c.get(n, 0) + 1
            max_ = max(max_, c[n])
            if c[n] == 2:
               twice += 1

        # Any way with only 2 different nodes in it, having one node more than once, is an error.
        if len(c) == 1:
            return {"class": 103, "subclass": 0}

        # Any way with only 2 different nodes in it, having one node more than once, is an error.
        if len(c) == 2 and max_ > 1:
            return {"class": 103, "subclass": 1}

        # Way that contains any single node more than twice is considered as an issue
        if max_ > 2:
            return {"class": 103, "subclass": 2}

        # If more than one node is found twice it is considered as an issue
        if twice > 1:
            return {"class": 103, "subclass": 3}


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Structural_DuplicateNodes(None)
        a.init(None)
        for nds in [[1, 2],
                    [2, 4, 189, 100909, 3898932],
                    [2^32, 4, 189, 100909, 3898932, 0, 2^32-1],
                   ]:
            assert not a.way(None, {}, nds), nds

        for nds in [[1, 2, 1, 1, 2], # subclass 2
                    [2, 4, 189, 100909, 3898932, 100909, 189, 189], # subclass 3
                    [2**32, 4, 4, 4, 4, 4, 4, 189, 100909, 3898932, 0, 2**32-1], # subclass 2
                    [2**32, 2**32, 0, 0, 2**60, 2**60], # subclass 3
                    [1, 2, 1, 1], # subclass 2
                    [1, 1, 1], # subclass 1
                    [1, 1], # subclass 0
                   ]:
            self.check_err(a.way(None, {}, nds), nds)
