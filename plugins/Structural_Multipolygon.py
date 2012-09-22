#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
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


class Structural_Multipolygon(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[11701] = { "item": 1170, "level": 2, "tag": ["relation", "multipolygon"], "desc": {"en": u"Inadequate role for multipolygon", "fr": u"Rôle inadéquat pour un multipolygon"} }
        self.errors[11702] = { "item": 1170, "level": 2, "tag": ["relation", "multipolygon"], "desc": {"en": u"Inadequate member for multipolygon", "fr": u"Membre inadéquat pour un multipolygon"} }
        self.errors[11703] = { "item": 1170, "level": 3, "tag": ["relation", "multipolygon"], "desc": {"en": u"Missing outer role for multipolygon", "fr": u"Pas de role outer le multipolygon"} }

    def relation(self, data, tags, members):
        if not ('type' in tags and tags['type'] == 'multipolygon'):
            return

        outer = False
        err = []
        for member in members:
            if member['type'] == 'way':
                if member['role'] not in ('', 'outer', 'inner'):
                    err.append((11701, 1, {"en": member['role']}))
                if member['role'] in ('', 'outer'):
                    outer = True
            else:
                err.append((11702, 1, {"en": "%s - %s" %(member['type'], member['role'])}))

        if not outer:
            err.append((11703, 1, {}))

        return err
