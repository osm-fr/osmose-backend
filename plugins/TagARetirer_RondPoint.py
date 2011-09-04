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


class TagARetirer_RondPoint(Plugin):
    
    err_101    = 4020
    err_101_fr = u"Tag à retirer sur junction=roundabout"
    err_101_en = u"Tag to remove on junction=roundabout"
    
    def way(self, data, tags, nds):
        
        if u"junction" not in tags:
            return
        
        if u"oneway" in tags:
            return [(101, 0, {"fr": u"Tag oneway inutile"})]
        
        if u"ref" in tags:
            return [(101, 1, {"fr": u"Ne doit pas contenir de tag ref"})]
