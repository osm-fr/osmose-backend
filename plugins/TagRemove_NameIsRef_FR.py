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
import re


class TagRemove_NameIsRef_FR(Plugin):

    only_for = ["FR"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[904] = self.def_class(item = 4040, level = 1, tags = ['name', 'highway', 'ref', 'fix:chair'],
            title = T_('Highway reference in name tag'),
            detail = T_(
'''Reference road (eg. D 73) is in the tag `name=*` and not in the tag
`ref=*`.'''),
            fix = T_(
'''Transfer the value from the tag `name=*` to the tag `ref=*`.'''))

        #self.ReRefRoute = re.compile(u"^[NDCEAM] ?[0-9]+(| ?[a-z]| ?bis)$")
        self.ReRefRoute1 = re.compile(u"(?:^|.*[^RV] +)([RV]?([NDCEAM] ?[0-9]+[^ ]*)).*")
        self.ReRefRoute2 = re.compile(u".*[nN][o°] ?[0-9]+[^ ]*")
        self.MultipleSpace = re.compile(u" +")

    def way(self, data, tags, nds):
        if "name" not in tags or "highway" not in tags or "ref" in tags:
            return

        ref = self.ReRefRoute1.match(tags["name"])
        if ref:
            ref_src = ref.group(1)
            ref_dest = ref.group(2)
            if " la %s" % ref_src in tags["name"] or " de %s" % ref_src in tags["name"] or " du %s" % ref_src in tags["name"]:
                return
            if "ancienne" in tags["name"]:
                return {"class": 904}
            name = re.sub(self.MultipleSpace, " ", tags["name"].replace(ref_src, "").strip())
            if name == "":
                fix = {"-":["name"], "+":{"ref": ref_dest}}
            else:
                fix = {"~":{"name": name}, "+":{"ref": ref_dest}}
            return {"class": 904, "fix": fix}

        if self.ReRefRoute2.match(tags["name"]):
            return {"class": 904, "subclass": 1, "text": {"en": "name=%s" % tags["name"]}}


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagRemove_NameIsRef_FR(None)
        a.init(None)
        name = [(u"Route des Poules N10 vers le poulailler", True, u"Route des Poules vers le poulailler", u"N10"),
                (u"Chemin de la C6 au moulin", False, None, None),
                (u"Ancienne RN 7", True, u"Ancienne", u"N 7"),
                (u"la D21E1", True, "la", u"D21E1"),
                (u"ancienne N10", True, None, None),
                (u"RN 7", True, None, u"N 7"),
                (u"N° 7", True, None, None),
               ]
        for (n, gen_err, f, r) in name:
            rdp = a.way(None, {"name": n, "highway": "H"}, None)
            if gen_err:
                self.check_err(rdp, ("name='%s'" % n))
            else:
                assert not rdp, ("name='%s'" % n)

            if f:
                fix1 = rdp["fix"]["~"]["name"]
                self.assertEqual(fix1, f, "name='%s' - fix = wanted='%s' / got='%s'" % (n, f, fix1))
            elif gen_err and r:
                fix1 = rdp["fix"]["-"]
                self.assertEqual(fix1, ["name"], "name='%s' - fix = wanted='%s' / got='%s'" % (n, f, fix1))

            if r:
                fix2 = rdp["fix"]["+"]["ref"]
                self.assertEqual(fix2, r, "ref='%s' - fix = wanted='%s' / got='%s'" % (n, r, fix2))

            assert not a.way(None, {"name": n, "highway": "H", "ref": "N10"}, None)
            assert not a.way(None, {"name": n}, None)
