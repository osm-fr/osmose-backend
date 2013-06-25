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
import datetime
import dateutil.parser
import re

class Date(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3090] = { "item": 3090, "level": 3, "tag": ["value", "fix:chair"], "desc": {"en": u"Bad date format", "fr": u"Format de date inconsistant"} }
        self.tag_date = [
            "date", "start_date", "end_date", "paved:date", "date_closed", "built_date",
            "opening_date", "check_date", "open_date", "construction:date", "temporary:date_on",  # Construction
        ]
        self.default_date = datetime.datetime(9999, 12, 1)
        self.Year = re.compile(u"^[12][0-9][0-9][0-9]^")
        self.Day1 = re.compile(u"^[12][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]^")
        self.Day2 = re.compile(u"^[0-9][0-9]/[0-9][0-9]/[12][0-9][0-9][0-9]^")
        self.Aprox = re.compile(u"^(?:early|mid|late|before|after|spring|summer|autumn|winter) [^ ]+")

    def convert2date(self, string):
        try:
            date = dateutil.parser.parse(string, default=self.default_date)
            if date.year != 9999:
                return date
        except ValueError:
            pass

    # http://wiki.openstreetmap.org/wiki/Key:start_date
    def check(self, string):
        if string[0] == '~':
            return self.check(string[1:])
        if string[-1] == 's':
            return self.check(string[:-1])
        if string[-3:] == ' BC' or string[-3:] == ' AD':
            return self.check(string[:-3])
        if len(string) == 4 and self.Year.match(string):
            return True
        if len(string) == 10 and (self.Day1.match(string) or self.Day2.match(string)):
            return True
        if string[0] == 'C':
            try:
                int(string[1:])
                return True
            except ValueError:
                pass
        if self.Aprox.match(string):
            return self.check(string.split(' ',1)[1])
        if self.convert2date(string):
            return True

    def node(self, data, tags):
        for i in self.tag_date:
            if i in tags:
                if ".." in tags[i]:
                    for d in tags[i].split('..'):
                        if not self.check(d):
                            return [(3090, 2, {"fr": u"Date \"%s\" incorrecte" % d, "en": u"Bad date \"%s\"" % d})]
                elif not self.check(tags[i]):
                    return [(3090, 1, {"fr": u"Date \"%s\" incorrecte" % tags[i], "en": u"Bad date \"%s\"" % tags[i]})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


if __name__ == "__main__":
    a = Date(None)
    a.init(None)
    for d in ["~1855", "~1940s", "~C13", "C18", "1970s", "1914", "1914..1918", "2008-08-08..2008-08-24", "late 1920s", "after 1500", "summer 1998", "480 BC", "2012-10", "2002-11"]:
        if a.node(None, {"date":d}):
            print "fail: %s" % d

    for d in ["yes", "XVI"]:
        if not a.node(None, {"date":d}):
            print "fail: %s" % d
