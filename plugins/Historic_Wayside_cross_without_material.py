#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights: Morray 2020                                               ##
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


class Historic_Wayside_cross_without_material(Plugin):

    only_for = ["DE", "AT", "CH"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[303242] = self.def_class(item = 3032, level = 1, tags = ['historic', 'fix:survey'],
            title = T_('Wayside cross node without `material` tag'),
            detail = T_(
'''The tag `historic=wayside_cross` can always be used in combination with
the tag `material=*`.'''),
            fix = T_(
'''Fill the tag `material=*` as specific as possible.'''),
            trap = T_(
'''The tag `historic=wayside_cross` is sometimes misused. Please x-check
if `historic=wayside_shrine` or `summit:cross=yes` is more appropiate.'''))
        doc = dict(
            detail = T_(
'''Check if tag `material=*` is filled for `historic=wayside_cross` objects.'''),
            fix = T_(
'''Add tag `material=*` or change object type as appropriate. Also take the 
oportunity to add other meta-data as `religion`, `denomination`, `start_date`, 
`inscritption`, ...'''),
            trap = T_(
'''The tag `historic=wayside_cross` is sometimes misused. Please x-check
if `historic=wayside_shrine` or `summit:cross=yes` is more appropiate'''))


    def node(self, data, tags):
        if tags["historic"]=="wayside_cross" and "material" not in tags:
           return {"class": 800, "subclass": 0}
