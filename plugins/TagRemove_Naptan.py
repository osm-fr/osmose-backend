#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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


class TagRemove_Naptan(Plugin):

    only_for = ["GB"]

    def init(self, logger):
        Plugin.init(self, logger)
        if self.father.config.options.get("project") != 'openstreetmap':
            return False
        self.errors[40601] = self.def_class(item = 4060, level = 2, tag = ['public_transport', 'fix:survey'],
            title = T_('Naptan import, survey needed.'))

    def node(self, data, tags):
        if tags.get('naptan:verified') == 'no':
            return {"class": 40601}

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_Naptan(None)
        self.set_default_config(a)
        a.init(None)
        assert not a.node(None, {"seamark": "trunk"})
        assert not a.node(None, {"naptan:verified": "yes"})
        self.check_err(a.node(None, {"naptan:verified": "no"}))
