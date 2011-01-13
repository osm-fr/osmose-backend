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
    
    err_900    = 4030
    err_900_fr = u"Tags incompatibles"
    err_900_en = u"Incompatible tags"
    
    def init(self, logger):
        import re
        self.ReInitColleNom  = re.compile(u"^.*[A-Z]\.[A-Z][a-z].*$")
        self.ReInitSansPoint = re.compile(u"^(|.* )[A-Z]+\\.[A-Z\\.]*[A-Z](| .*)$")
        self.ReNEnMajuscule  = re.compile(u"^(|.* )N°[0-9](| .*)$")
        self.ReRefRoute      = re.compile(u"^[NDCEA] ?[0-9]+(| ?[a-z]| ?bis)$")
        self.ReChiffre       = re.compile(u"[0-9]")

    def way(self, data, tags, nds):
        
        err = []
        
        if u"highway" in tags and u"landuse" in tags:
            err.append((900, 0, {"en": u"highway=* + landuse=*"}))

        return err
