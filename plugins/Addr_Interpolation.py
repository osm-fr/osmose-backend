#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2019                                      ##
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
import datetime
import dateutil.parser

class Addr_Interpolation(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[20601] = self.def_class(item = 2060, level = 3, tags = ['tag', 'addr'],
            title = T_('Misusing addr:interpolation in combination with other tags'))

    ALLOWED = set(['addr:interpolation', 'source', 'addr:inclusion', 'addr:street', 'addr:postcode', 'addr:country', 'id_origin', 'addr:state', 'addr:county', 'attribution', 'addr:city', 'addr:province', 'created_by', 'fixme', 'addr:suburb', 'is_in:city', 'note'])

    def way(self, data, tags, nds):
        if 'addr:interpolation' not in tags:
            return

        remaning = set(tags.keys()) - self.ALLOWED
        if len(remaning) > 0:
            return {'class': 20601, 'text': {'en': ', '.join(remaning)}}


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def setUp(self):
        TestPluginCommon.setUp(self)
        self.p = Addr_Interpolation(None)
        self.set_default_config(self.p)
        self.p.init(None)

    def test(self):
        assert not self.p.way(None, {'addr:interpolation': 'odd', 'source': 'survey'}, None)
        self.check_err(self.p.way(None, {'addr:interpolation': 'odd', 'highway': 'residential'}, None), expected={'class': 20601})
