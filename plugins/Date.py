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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
import datetime
import dateutil.parser
import re

class Date(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3090] = self.def_class(item = 3090, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Bad date format'),
            detail = T_(
'''The date entered is not in the expected format described at
[Key:start_date](https://wiki.openstreetmap.org/wiki/Key:start_date)'''))

        self.tag_date = [
            "date", "start_date", "end_date", "paved:date", "date_closed", "built_date",
            "opening_date", "check_date", "open_date", "construction:date", "temporary:date_on",  # Construction
            "mhs:inscription_date", # Heritage
        ]
        self.default_date = datetime.datetime(9999, 12, 1)
        self.Aprox = re.compile(u"^(?:early|mid|late|before|after|spring|summer|autumn|winter) [^ ]+")

    def convert2date(self, string):
        try:
            date = dateutil.parser.parse(string, default=self.default_date)
            if date.year < 3000:
                return date
        except (ValueError, TypeError, OverflowError):
            pass

    # http://wiki.openstreetmap.org/wiki/Key:start_date
    def check(self, string):
        if len(string) == 0:
            return True
        if string[0] == '~':
            return len(string) > 1 and self.check(string[1:])
        if string[-1] == 's':
            return len(string) > 1 and self.check(string[:-1])
        if string[-3:] == ' BC' or string[-3:] == ' AD':
            return len(string) > 3 and self.check(string[:-3])
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
        if tags.get("amenity") == "clock":
            return

        for i in self.tag_date:
            if i in tags:
                if ".." in tags[i]:
                    for d in tags[i].split('..'):
                        if not self.check(d):
                            return {"class": 3090, "subclass": 2, "text": T_("Concerns tag: `{0}`", '='.join([i, tags[i]])) }
                elif not self.check(tags[i]):
                    return {"class": 3090, "subclass": 1, "text": T_("Concerns tag: `{0}`", '='.join([i, tags[i]])) }

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Date(None)
        a.init(None)
        for d in ["~1855", "~1940s", "~C13", "C18", "1970s", "1914", "1914..1918", "2008-08-08..2008-08-24", "late 1920s", "after 1500", "summer 1998", "480 BC", "2012-10", "2002-11", "2014", "2010..", "2022-04-08"]:
            assert not a.node(None, {"date":d}), ("date={0}".format(d))

        assert not a.node(None, {"date":"yes", "amenity":"clock"}), ("date=yes")

        for d in ["yes", "XVI", "p", "0000", "9999", "Ca9", "1914..9999", "2014..Ca09", "7000", "~", "2022-88", "2022-12-99", "2022-99-12"]:
            self.check_err(a.node(None, {"date":d}), ("date={0}".format(d)))
            self.check_err(a.way(None, {"date":d}, None), ("date={0}".format(d)))
            self.check_err(a.relation(None, {"date":d}, None), ("date={0}".format(d)))
