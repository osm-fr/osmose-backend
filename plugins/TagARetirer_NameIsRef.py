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


class TagARetirer_NameIsRef(Plugin):
    
    err_904    = 4040
    err_904_fr = u"Référence d'une route dans le champ name"
    err_904_en = u"Route reference in name tag"
    
    def init(self, logger):
        import re
        #self.ReRefRoute = re.compile(u"^[NDCEA] ?[0-9]+(| ?[a-z]| ?bis)$")
        self.ReRefRoute1 = re.compile(u"[NDCEA] ?[0-9]+.*")
        self.ReRefRoute2 = re.compile(u".*[nN]° ?[0-9]+.*")

    def way(self, data, tags, nds):
        
        if "name" not in tags:
            return
        if "highway" not in tags:
            return
            
        if self.ReRefRoute1.match(tags["name"]):
            return [(904, 0, {"en": "name=%s" % tags["name"]})]
        
        if self.ReRefRoute2.match(tags["name"]):
            return [(904, 1, {"en": "name=%s" % tags["name"]})]
