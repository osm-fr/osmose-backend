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


class Name_MotMalEcritParRegex(Plugin):
    
    err_701    = 5010
    err_701_fr = u"Mot mal écrit"
    err_701_en = u"Badly written word"
    
    def init(self, logger):
        import re
        self.ReTests = {}
        self.ReTests[( 0, u"École ")]     = re.compile(u"^[EÉée][Cc][Oo][Ll][Ee] .*$")
        self.ReTests[( 1, u"Église ")]    = re.compile(u"^[EÉée][Gg][Gl][Ii][Ss][Ee] .*$")
        self.ReTests[( 2, u"La ")]        = re.compile(u"^[Ll][Aa] .*$")
        self.ReTests[( 3, u"Étang ")]     = re.compile(u"^[EÉée][Tt][Tt]?[AaEe][Nn][GgTt]? .*$")
        self.ReTests[( 4, u"Saint ")]     = re.compile(u"^[Ss]([Aa][Ii][Nn])?[Tt]\\.? .*$")
        self.ReTests[( 5, u"Hôtel ")]     = re.compile(u"^[Hh][OoÔô][Tt][Ee][Ll] .*$")
        self.ReTests[( 6, u"Château ")]   = re.compile(u"^[Cc][Hh][ÂâAa][Tt][Ee][Aa][Uu] .*$")
        self.ReTests[( 7, u"McDonald's")] = re.compile(u"^[Mm][Aa]?[Cc] ?[Dd][Oo]([Nn][Aa][Ll][Dd]'?[Ss]?)?( .+)?$")
        self.ReTests[( 8, u"Sainte ")]    = re.compile(u"^[Ss]([Aa][Ii][Nn])?[Tt][Ee]\\.? .*$")
        self.ReTests[( 9, u"Le ")]        = re.compile(u"^[Ll][Ee] .*$")
        self.ReTests[(10, u"Les ")]       = re.compile(u"^[Ll][Ee][Ss] .*$")
        self.ReTests[(11, u"L'")]         = re.compile(u"^[Ll]['].*$")
        self.ReTests = self.ReTests.items()

    def node(self, data, tags):        
        if u"name" not in tags:
            return
        name = tags["name"]
        for test in self.ReTests:
            if test[1].match(name) and not name.startswith(test[0][1]):
                return [(701, test[0][0], {"en": test[0][1]})]
            
    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
