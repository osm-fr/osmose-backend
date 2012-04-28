#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
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
import datetime
import dateutil.parser

class Construction(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[4070] = { "item": 4070, "level": 2, "tag": ["tag"], "desc": {"en": u"Finished construction", "fr": u"Construction terminée"} }

        self.tag_construction = ["highway", "landuse", "building"]
        self.tag_date = ["opening_date", "check_date", "open_date", "construction:date", "temporary:date_on", "date_on"]
        self.default_date = datetime.datetime(9999, 12, 1)
        self.today = datetime.datetime.today()
        self.date_limit = datetime.datetime.today() - datetime.timedelta(days=2 * 365)

    def getTagDate(self, tags):
        for i in self.tag_date:
            if i in tags:
                return tags[i]

    def convert2date(self, string):
        try:
            date = dateutil.parser.parse(string, default=self.default_date)
            if date.year != 9999:
                return date
        except ValueError:
            pass

    def node(self, data, tags):
        construction_found = False
        if "construction" in tags:
            construction_found = True

        for t in (set(self.tag_construction) & set(tags)):
            if t in tags and tags[t] == "construction":
                construction_found = True

        if not construction_found:
            return

        date = None
        tagDate = self.getTagDate(tags)
        if tagDate:
            date = self.convert2date(tagDate)

        if date:
            if date < self.today:
                return [(4070, 0, {})]
        else:
            if datetime.datetime.strptime(data["timestamp"][0:10], "%Y-%m-%d") < self.date_limit:
                return [(4070, 1, {})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)
