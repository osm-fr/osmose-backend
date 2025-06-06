#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2012                                      ##
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
from modules.downloader import urlread
import re
import unicodedata


class TagFix_Tree_Lang_fr(Plugin):

    only_for = ["fr"]

    def strip_accents(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    def normalize(self, string):
        return self.strip_accents(string.strip().lower()).replace(' commun', '')

    def liste_des_arbres_fruitiers(self):
        reline = re.compile(r"\[\[([^:]*)$")
        data = urlread(u"https://fr.wikipedia.org/wiki/Liste_des_arbres_fruitiers?action=raw", 1)
        #data = open(u"Liste_des_arbres_fruitiers?action=raw").read()
        data = data.split("]]")
        for line in data:
            for res in reline.findall(line):
                for n in res.split('|'):
                    self.Tree[self.normalize(n)] = {'species:fr':res}

    def liste_des_essences_europennes(self):
        reline = re.compile(r"^\* \[\[([^]]*)\]\][^[]*\[\[([^]]*)\]\][^[]*(?:\[\[([^]]*)\]\][^[]*)?(?:\[\[([^]]*)\]\][^[]*)?")
        data = urlread(u"https://fr.wikipedia.org/wiki/Liste_des_essences_forestières_européennes?action=raw", 1)
        #data = open(u"Liste_des_essences_forestières_européennes?action=raw").read()
        data = data.split("\n")
        for line in data:
            for res in reline.findall(line):
                for n in res[0].split('|'):
                    self.Tree[self.normalize(n)] = {'genus':res[1], 'species':'|'.join(res[2:3]), 'species:fr':res[0]}

    def check(self, tag, value, subclass):
        name = self.normalize(u''.join(value))
        if name in self.Tree:
            return {"class": 3120, "subclass": subclass, "text": T_("Bad tag {0}=\"{1}\"", tag, value),
                    "fix": {"-": [tag], "+": self.Tree[name]}}

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3120] = self.def_class(item = 3120, level = 3, tags = ['natural', 'fix:imagery'],
            title = T_('Tree tagging'),
            detail = T_(
'''To characterize the trees `natural=tree`, there are two main tags:
`genus` and `species`.'''),
            fix = T_(
'''Put the right data in the correct tag, in this case species.'''),
            trap = T_(
'''Specify the language for the tag `species`: `species:en=oak`'''))

        self.Tree = {}
        self.liste_des_arbres_fruitiers()
        self.liste_des_essences_europennes()

    def node(self, data, tags):
        if tags.get('natural') != 'tree':
            return

        err = []

        if 'name' in tags:
            if tags['name'].lower() in ('arbre', 'tree') or 'chablis' in tags['name'].lower() or 'branche' in tags['name'].lower():
                err.append({"class": 3120, "subclass": 0, "text": T_("Bad tag name=\"{0}\"", tags["name"])})
            c = self.check('name', tags['name'], 1)
            if c:
                err.append(c)

        if 'type' in tags:
            # type is a deprecated tag, but the new tag isn't used with French tree names
            c = self.check('type', tags['type'], 2)
            if c:
                err.append(c)

        if 'denotation' in tags:
            if tags['denotation'] not in ('avenue', 'urban', 'natural_monument', 'landmark', 'agricultural','park','garden'):
                err.append({"class": 3120, "subclass": 4, "text": T_("Bad tag denotation=\"{0}\"", tags["denotation"])})

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Tree_Lang_fr(None)
        a.init(None)
        for d in [u"Arbre de miel", u"Le Gros Chêne", u"Les Cinq Jumeaux"]:
            assert not a.node(None, {"natural":"tree", "name":d}), ("name='{0}'".format(d))

        for d in [u"Arbre", u"chablis ouvert 25cmd", u"Pin Sylvestre", u"Frêne commun", u"Chêne vert", u"abricotier"]:
            self.check_err(a.node(None, {"natural":"tree", "name":d}), ("name='{0}'".format(d)))
            self.check_err(a.way(None, {"natural":"tree", "name":d}, None), ("name='{0}'".format(d)))
            self.check_err(a.relation(None, {"natural":"tree", "name":d}, None), ("name='{0}'".format(d)))
            assert not a.node(None, {"natural":"other", "name":d}), ("name='{0}'".format(d))

        for d in [u"anything", u"Pin Sylvestre", u"Frêne commun", u"Chêne vert"]:
            self.check_err(a.node(None, {"natural":"tree", "denotation":d}), ("denotation='{0}'".format(d)))

        for d in [u"landmark", u"agricultural"]:
            assert not a.node(None, {"natural":"tree", "denotation":d}), ("denotation='{0}'".format(d))

        for d in [u"broad_leafed", u"conifer"]:
            assert not a.node(None, {"natural":"tree", "type":d}), ("type='{0}'".format(d))
