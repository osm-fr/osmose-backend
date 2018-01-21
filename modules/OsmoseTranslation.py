#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jocelyn Jaubert 2013                                       ##
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

import os
import polib

class OsmoseTranslation:

    def __init__(self):
        self.languages = []
        self.trans = {}
        for fn in os.listdir("po/josm/"):
            if fn.endswith(".po"):
                self.add_po(fn, "po/josm/")
        for fn in os.listdir("po/"):
            if fn.endswith(".po"):
                self.add_po(fn, "po/")

    def add_po(self, fn, base):
        l = fn[:-3]
        po = polib.pofile(base + l + ".po")
        if not l in self.trans:
            self.languages.append(l)
            self.trans[l] = {}
        for entry in po:
            if entry.msgstr != "":
                self.trans[l][entry.msgid] = entry.msgstr

    def translate(self, str, *args):
        out = {}

        # english version
        if len(args) == 0:
            out["en"] = str
        elif isinstance(args[0], dict):
            out["en"] = str % args[0]
        else:
            out["en"] = str % args

        for l in self.languages:
            if str in self.trans[l] and self.trans[l][str] != "":
                if len(args) == 0:
                    out[l] = self.trans[l][str]
                elif isinstance(args[0], dict):
                    out[l] = self.trans[l][str] % args[0]
                else:
                    out[l] = self.trans[l][str] % args

        return out

    def translate_format(self, str, *args):
        out = {}

        # english version
        if len(args) == 0:
            out["en"] = str
        else:
            out["en"] = str.format(*args)

        for l in self.languages:
            if str in self.trans[l] and self.trans[l][str] != "":
                if len(args) == 0:
                    out[l] = self.trans[l][str]
                else:
                    out[l] = self.trans[l][str].format(*args)

        return out

if __name__ == "__main__":
    translate = OsmoseTranslation()
    print("languages: ")
    for l in translate.languages:
        print(l, len(translate.trans[l]))

