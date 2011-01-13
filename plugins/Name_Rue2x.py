#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Yoann Arnaud <yarnaud@crans.org> 2009                       ##
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

class plugin:
    
    err_705    = 5030
    err_705_fr = u"Le tag name contient 2 noms"
    err_705_en = u"The name tag contains two names"

    def init(self, logger):
        import re
        self.Re1 = re.compile(u"^.*;.*$")
        self.Re2 = re.compile(u"^.*/.*$")
        self.Re3 = re.compile(u"^.*\+.*$")

    def way(self, data, tags, nds):
        if u"name" not in tags:
            return
        if u"aeroway" in tags:
            return
        
        if self.Re1.match(tags["name"]):
            return [(705,0,{})]
        if self.Re2.match(tags["name"]):
            return [(705,1,{})]
        if self.Re3.match(tags["name"]):
            return [(705,2,{})]
