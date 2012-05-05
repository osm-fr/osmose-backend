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
import urllib


class TagACorriger_Wikipedia(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30310] = { "item": 3031, "desc": {"en": u"Not a Wikipedia URL"} }
        self.errors[30311] = { "item": 3031, "desc": {"en": u"Use Wikipedia title"} }
        self.errors[30312] = { "item": 3031, "desc": {"en": u"Missing Wikipedia language before article title"} }
        self.errors[30313] = { "item": 3031, "desc": {"en": u"Use human Wikipedia page title"} }

        import re
        self.Wiki = re.compile(u"http://([^\.]+)\.wikipedia.+/(.+)")
        self.lang = re.compile(u"[-a-z]+:.*")

    def human_readable(self, string):
        try:
            string = urllib.unquote(string.encode('ascii')).decode('utf8')
        except:
            pass
        return string.replace("_"," ")

    def node(self, data, tags):
        if "wikipedia" in tags:
            if tags["wikipedia"].startswith("http://"):
                m = self.Wiki.match(tags["wikipedia"])
                if m:
                    return [(1, 1, {"en": u"Use wikipedia=%s:*" % m.group(1), "fix": {"wikipedia": "%s:%s" % (m.group(1), self.human_readable(m.group(2)))} })]
                else:
                    return [(0, 0, {})]

            err=[]
            if not self.lang.match(tags["wikipedia"]):
                err.append((2, 2, {}))
            if "%" in tags["wikipedia"] or "_" in tags["wikipedia"]:
                err.append((3, 3, {"fix": {"wikipedia": self.human_readable(tags["wikipedia"])}} ))

            return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


if __name__ == "__main__":
    a = TagACorriger_Wikipedia(None)
    a.init(None)
    for d in [u"http://fr.wikipedia.org/wiki/Wikipedia", "Wikipedia", "fr:Bip_le%20robot", u"http://en.wikipedia.org/wiki/Col_du_Pr%C3%A9", u"fr=Château_Saulnier"]:
        if not a.node(None, {"wikipedia":d}):
            print "fail: %s" % d
