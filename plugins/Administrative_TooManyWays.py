#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Yoann Arnaud <yarnaud@crans.org> 2009                      ##
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


class Administrative_TooManyWays(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[504] = self.def_class(item = 6020, level = 3, tags = ['boundary', 'fix:chair'],
            title = T_('Duplicated way in relation'),
            detail = T_(
'''In a relation, a way should be present only once.'''),
            fix = T_(
'''Most often, this is an user issue that add several times the same way.
The editor JOSM can easily visualize the relationships and see duplicates
(in color).'''),
            trap = T_(
'''Double check the ways roles in the relation before deleting.

Caution: in a route, a path can be taken several times. The multiple
presence of this path in the relation `type=route` is not then an issue.
Then ensure the roles `forward` and `backward`.'''))

    def relation(self, data, tags, members):

        if tags.get(u"boundary", u"") != u"administrative":
            return
        w = [m[u"ref"] for m in members if m[u"type"] == u"way"]
        if len(w) != len(set(w)):
            return {"class": 504}

        #if tags.get(u"admin_level", u"") != u"8":
        #    return
        #n_limit = 15
        #n = len(data[u"member"])
        #if n >= n_limit:
        #    return {"class": 503, "subclass": 0, "text": T_(u"More than %s ways in admin_level=8 relation (%s)", str(n_limit),str(n))}

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def setUp(self):
        TestPluginCommon.setUp(self)
        self.p = Administrative_TooManyWays(None)
        self.p.init(None)

    def test(self):
        w1_0 = { "ref": 1, "role": "xx", "type": "way"}
        w1_1 = { "ref": 1, "role": "yy", "type": "way"}
        w2   = { "ref": 2, "role": "xx", "type": "way"}
        w3   = { "ref": 2, "role": "xx", "type": "way"}
        n1   = { "ref": 1, "role": "xx", "type": "node"}
        self.check_err(self.p.relation(None, {"boundary": "administrative"}, [w1_0, w1_1]))
        self.check_err(self.p.relation(None, {"boundary": "administrative"}, [w1_0, w1_1, w2, w3, n1]))
        assert not self.p.relation(None, {"boundary": "administrative"}, [w1_0, w2])
        assert not self.p.relation(None, {"boundary": "administrative"}, [w1_0, n1])
        assert not self.p.relation(None, {}, [w1_0, w1_1])
        assert not self.p.relation(None, {}, [w1_0, w1_1])
