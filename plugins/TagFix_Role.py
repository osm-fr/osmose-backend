#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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
import re


class TagFix_Role(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[31700] = { "item": 3170, "level": 2, "tag": ["relation", "fix:chair"], "desc": T_(u"Inadequate role") }
        self.Role = re.compile("^[a-z_:]*$")

    def relation(self, data, tags, members):
        roles = []
        for member in members:
            if not self.Role.match(member["role"]):
                roles.append(member["role"])

        if len(roles) > 0:
            return {"class": 31700, "subclass": 1, "text": {"en": "role=%s" % ', '.join(roles)}}


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Role(None)
        a.init(None)
        self.check_err(a.relation(None, None, [{"role":"<std>"}, {"role":"$$"}]))
