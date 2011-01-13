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

class plugin:
    #err_503_fr = (u"!Trop de ways dans la relation", u"trop de ways")
    #err_503_en = (u"!Too many ways in relation", u"too many ways")
    
    err_504    = 6020
    err_504_fr = u"Way dupliqué dans la relation"
    err_504_en = u"Duplicated way in relation"
    
    def relation(self, data, tags):
        
        if tags.get(u"boundary", u"") <> u"administrative":
            return
        w = [m[u"ref"] for m in data[u"member"] if m[u"type"]==u"way"]
        if len(w) <> len(set(w)):
             return [(504, 0, {})]
        
        #if tags.get(u"admin_level", u"") <> u"8":
        #    return
        #n_limit = 15
        #n = len(data[u"member"])
        #if n >= n_limit:
        #    e_fr = u"La relation commune contient plus de %s membres (%s)"%(str(n_limit),str(n))
        #    e_en = u"More than %s ways in admin_level=8 relation (%s)"%(str(n_limit),str(n))
        #    return [(503, 0, {"fr": e_fr, "en": e_en})]
