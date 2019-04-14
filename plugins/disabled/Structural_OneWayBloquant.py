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


class Structural_OneWayBloquant(Plugin):

    #err_107_fr = (u"Way à sens unique sans entrée-sortie", u"oneway bloquant")
    #err_107_en = (u"One-way Way without entrance-exit", u"blocking one-way")

    def way(self, data, tags, nds):
        return

        if u"oneway" not in tags:
            return

        if tags[u"oneway"] not in [u"yes", u"1", u"true", u"-1"]:
            return

        err = []
        if len(self.father._reader.NodeWaysId(nds[0])) == 1 or len(self.father._reader.NodeWaysId(nds[-1])) == 1:
            err.append((107, 0, {}))
        return err
