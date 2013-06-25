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
        self.errors[31700] = { "item": 3170, "level": 2, "tag": ["relation", "fix:chair"], "desc": {"en": u"Inadequate role", "fr": u"Rôle inadéquat"} }
        self.Role = re.compile("^[a-z_:]*$")

    def relation(self, data, tags, members):
        err = []
        for member in members:
            if not self.Role.match(member["role"]):
                err.append((31700, 1, {"en": member["role"]}))
        return err

if __name__ == "__main__":
    a = TagFix_Role(None)
    a.init(None)
    if not a.relation(None, None, [{"role":"<std>"}]):
        print "fail: %s" % d
