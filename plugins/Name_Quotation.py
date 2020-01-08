#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2018                                      ##
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


class Name_Quotation(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[50704] = self.def_class(item = 5070, level = 2, tags = ['name', 'fix:chair'],
            title = T_('Unbalanced quotation mark or bracket in name'),
            resource = 'https://en.wikipedia.org/wiki/Bracket#Encoding_in_digital_media')

        self.quotes = [
            # https://en.wikipedia.org/wiki/Quotation_mark#Unicode_code_point_table
            u"«»", u"‹›", u"“”‟„", u"〝〞〟",
            # https://en.wikipedia.org/wiki/Bracket#Encoding_in_digital_media
            u"()", u"[]", u"{}", u"«»", u"‹›", u"⌈⌉", u"⌊⌋", u"⌜⌝", u"⌞⌟", u"⁽⁾", u"₍₎", u"⸢⸣", u"⸤⸥", u"﴾﴿", u"⸜⸝", u"᚛᚜", u"༼༡༽", u"〔〕", u"〖〗", u"〘〙", u"〚〛", u"〝〞", u"〈〉", u"｢｣", u"〈〉", u"《》", u"「」", u"『』", u"【】", u"（）", u"［］", u"＜＞", u"｛｝", u"｟｠",
        ]

        self.quotes_j = u"".join(self.quotes)

    def node(self, data, tags):
        if 'name' not in tags:
            return

        stack = []
        for c in tags["name"]:
            if c in self.quotes_j:
                if len(stack) == 0 or stack[-1][0] == c or c not in stack[-1][1]:
                    group = next(q for q in self.quotes if c in q)
                    stack.append([c, group])
                else:
                    p, group = stack.pop()
                    if c not in group:
                        return [{"class": 50704, "subclass": 0, "text": T_f(u"Umbalanced {0} with {1}", p, c)}]

        if len(stack) > 0:
            return [{"class": 50704, "subclass": 1, "text": T_f(u"Umbalanced {0}", "".join(map(lambda q: q[0], stack)))}]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        TestPluginCommon.setUp(self)
        self.p = Name_Quotation(None)
        self.p.init(None)

        assert not self.p.node(None, {"foo": u"bar"})
        assert self.p.node(None, {"name": u"("})
        assert self.p.node(None, {"name": u"(]"})
        assert self.p.node(None, {"name": u"(("})
        assert not self.p.node(None, {"name": u"{[]}"})
        assert self.p.node(None, {"name": u"{[}]"})
