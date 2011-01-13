#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
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
    
    only_for = ["FR"]
    
    err_706    = 3020
    err_706_fr = u"Tag source illegal ou incomplet"
    err_706_en = u"Illegal or uncomplete source tag"

    err_707    = 2040
    err_707_fr = u"Tag source manquant"
    err_707_en = u"Missing tag source"
    
    def node(self, data, tags):
        if u"source" not in tags:
            return
        if u"AAAA" in tags[u"source"]:
            return [(706,0,{"fr":u"Le tag source contient AAAA", "en":u"Source tag contains AAAA"})]        
        if u"Cartographes Associés" in tags[u"source"]:
            return [(706,1,{"fr":u"Cartographes Associés", "en":u"Cartographes Associés"})]        
    
    def way(self, data, tags, nds):
        if u"source" not in tags:
            if tags.get(u"boundary", None) == u"administrative":
                return [(707,0,{})]
            return
        if u"AAAA" in tags[u"source"]:
            return [(706,0,{"fr":u"Le tag source contient AAAA", "en":u"Source tag contains AAAA"})]        
        if u"Cartographes Associés" in tags[u"source"]:
            return [(706,1,{"fr":u"Cartographes Associés", "en":u"Cartographes Associés"})]        
    
    def relation(self, data, tags):
        if u"source" not in tags:
            return
        if u"AAAA" in tags[u"source"]:
            return [(706,0,{"fr":u"Le tag source contient AAAA", "en":u"Source tag contains AAAA"})]        
        if u"Cartographes Associés" in tags[u"source"]:
            return [(706,1,{"fr":u"Cartographes Associés", "en":u"Cartographes Associés"})]        
