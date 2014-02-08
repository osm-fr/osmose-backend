#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2013                                      ##
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
from modules.downloader import urlread
import re


class TagFix_Postcode(Plugin):

    def list_postcode(self):
        reline = re.compile("^[-CAN ]+$")
        remline = re.compile("^[-CAN ]+ *\([-CAN ]+\)$")
        data = urlread("http://en.wikipedia.org/wiki/List_of_postal_codes?action=raw", 1)
        data = filter(lambda t: len(t)>2 and t[1] != "- no codes -", map(lambda x: map(lambda y: y.strip(), x.split("|"))[5:8], data.split("|-")[1:-1]))
        postcode = {}
        for line in data:
            iso = line[0][0:2]
            format = line[1]
            note = line[2]

            if format[-1] == ')':
                format = map(lambda x: x.strip(), format[:-1].split('('))
            else:
                format = [format]

            regexs = []
            for f in format:
                if reline.match(f):
                    regex = f.replace("N", "[0-9]").replace("A", "[A-Z]").replace("CC", self.Country)
                    regexs.append(regex)

            if len(regexs) > 1:
                postcode[iso] = "^\("+("\)|\(".join(regexs))+"\)$"
            elif len(regexs) == 1:
                postcode[iso] = "^"+regexs[0]+"$"

        return postcode

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[31901] = {"item": 3190, "level": 3, "tag": ["postcode", "fix:chair"], "desc": T_(u"Invalid postcode") }

        self.Country = self.father.config.options.get("country")
        postcode = self.list_postcode()
        if self.Country in postcode:
            self.CountryPostcode = re.compile(postcode[self.Country])
        else:
            self.CountryPostcode = None

    def node(self, data, tags):
        if not self.CountryPostcode or (not 'postal_code' in tags and not 'addr:postcode' in tags):
            return

        err = []
        for tag in ("postal_code", "addr:postcode"):
            if tag in tags and not self.CountryPostcode.match(tags[tag]):
                err.append((31901, 0, {"en": "Invalid postcode %s for country code %s" % (tags[tag], self.Country), "fr": "Code postal %s invalide pour le code pays %s" % (tags[tag], self.Country)}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Postcode(None)
        class _config:
            options = {"country": "FR"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        assert a.node(None, {"addr:postcode":"la bas"})
        assert not a.node(None, {"addr:postcode":"75000"})
