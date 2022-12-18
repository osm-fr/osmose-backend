#-*- coding: utf-8 -*-

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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin


class TagRemove_Fixme(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[40610] = self.def_class(item = 4061, level = 3, tags = ['fixme', 'fix:chair'],
            title = T_('Object needs review'))
        self.errors[40611] = self.def_class(item = 4061, level = 2, tags = ['fixme', 'fix:chair', 'highway'],
            title = T_('Highway classification needs review'),
            detail = T_(
'''`highway=road` has been used, choose a correct value, such as
`highway=unclassified`.'''))

    def node(self, data, tags):
        if "fixme" in tags or "FIXME" in tags:
            return [{"class": 40610, "subclass": 1, "text": {"en": tags['fixme'] if 'fixme' in tags else tags['FIXME']}}]
        else:
            return []

    def way(self, data, tags, nds):
        ret = self.node(data, tags)

        if tags.get("highway") == "road":
            ret.append({"class": 40611, "subclass": 1})

        return ret

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_Fixme(None)
        a.init(None)
        assert not a.way(None, {"highway": "trunk"}, None)
        self.check_err(a.way(None, {"highway": "road"}, None))
        self.check_err(a.way(None, {"fixme": "plop"}, None))
        self.check_err(a.way(None, {"FIXME": "plop"}, None))
        self.check_err(a.way(None, {"fixme": ""}, None))
