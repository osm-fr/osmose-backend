#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
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

class TagACorriger_BadKey(Plugin):

    err_3050    = 3050
    err_3050_fr = u"Mauvais tag"
    err_3050_en = u"Bad tag"

    def init(self, logger):
        import re
        self.KeyPart1 = re.compile("^[a-zA-Z_0-9]+$")
        self.KeyPart2 = re.compile("^[-_:a-zA-Z_0-9<>°\(\)\[\].]+$")
        self.exceptions = set( ("ISO3166-1",
                                "iso3166-1",
                                "ISO3166-2",
                                "iso3166-2",
                                "drive-through",
                                "aims-id",
                                "au.gov.abs",
                                "catmp-RoadID",
                                "dc-gis",
                                "nhd-shp",
                                "USGS-LULC",
                             ) )

    def node(self, data, tags):
        err = []
        keys = tags.keys()
        for k in keys:
            if k.startswith("def:") or k in self.exceptions:
                # key def: can contains sign =
                continue

            part = k.split(':', 1)
            if not self.KeyPart1.match(part[0]):
                err.append((3050, 0, {"fr": "Mauvais tag %s=%s" % (k, tags[k]), "en": "Bad tag %s=%s" % (k, tags[k])}))
            elif len(part) == 2 and not self.KeyPart2.match(part[1]):
                err.append((3050, 1, {"fr": "Mauvais tag %s=%s" % (k, tags[k]), "en": "Bad tag %s=%s" % (k, tags[k])}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
