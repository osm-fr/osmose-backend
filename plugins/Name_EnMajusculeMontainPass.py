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


class Name_EnMajusculeMontainPass(Plugin):

    err_803    = 5010
    err_803_fr = u"Nom tout en majuscules"
    err_803_en = u"Name entirely uppercase"
    
    err_804    = 2020
    err_804_fr = u"Altitude manquante"
    err_804_en = u"Missing altitude"
    
    def node(self, data, tags):        
        if u"mountain_pass" not in tags:
            return
        if tags["mountain_pass"] not in ["yes", "1"]:
            return
        err = []
        if u"ele" not in tags:
            err.append((804, 0, {}))
        if u"name" in tags and tags[u"name"].upper() == tags[u"name"] and tags[u"name"].lower() != tags[u"name"]:
            err.append((803, 0, {}))
        return err
    
    def way(self, data, tags, nds):
        return self.node(data, tags)
