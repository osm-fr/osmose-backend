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

class plugin:
    
    err_902    = 5010
    err_902_fr = u"Initiale collée au nom"
    err_902_en = u"Initial stuck to the name"
    
    def init(self, logger):
        import re
        self.ReInitColleNom  = re.compile(u"^.*[A-Z]\.[A-Z][a-z].*$")

    def way(self, data, tags, nds):
        
        err = []

        if "name" in tags:
            
            name = tags[u"name"]

            if self.ReInitColleNom.match(name): # and not u"E.Leclerc" in self._DataTags[u"name"]:
                err.append((902, 0, {}))

        return err
