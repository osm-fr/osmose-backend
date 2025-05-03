#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2010                       ##
## Copyrights Frédéric Rodrigo 2011-2014                                 ##
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


class Source(Plugin):

    not_for = ["HT"] # Google made drone imagery for after-earthquake in Haiti

    def init(self, logger):
        Plugin.init(self, logger)
        if self.father.config.options.get("project") != 'openstreetmap':
            return False
        self.errors[706] = self.def_class(item = 3020, level = 1, tags = ['source', 'fix:chair'],
            title = T_('Illegal or incomplete source tag'),
            detail = T_(
'''The `source` tag is incorrect. For example, an illegal source like
Google.'''),
            fix = T_(
'''Correct the source and the location of the object if necessary. If the
source is illegal, promptly notify the contributor to remove
contributions.'''))
        self.errors[707] = self.def_class(item = 2040, level = 3, tags = ['source', 'fix:chair'],
            title = T_('Missing source tag'),
            detail = T_(
'''An administrative boundary does not contain tag `source=*` sourcing
the origin.'''),
            fix = T_(
'''If the limit comes from the French Cadastre, add the appropriate
`source=*`.'''))

    def check(self, tags):
        if "source" not in tags and "ref" not in tags:
            return

        for tag in ("source", "ref"):
            if tag in tags:
                value = tags[tag].lower()
                if any("google" in v and not v.rstrip().endswith("buildings") for v in value.split(';')):
                    return {"class": 706, "subclass": 2, "text": {"en": "Google {0}: {1}".format(tag, value)}}

    def node(self, data, tags):
        return self.check(tags)

    def way(self, data, tags, nds):
        return self.check(tags)

    def relation(self, data, tags, members):
        return self.check(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Source(None)
        class _config:
            options = {"country": "MD", "project": "openstreetmap"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        for d in [{"name": "Free"},
                  {"source": "Free"},
                  {"source": "esri/google_africa_buildings"}, # ODbL licensed, #2323
                  {"source": "Google Open Buildings; something else"}, # ODbL licensed, #2323
                 ]:
            assert not a.node(None, d), d

        for d in [{"source": "google maps"}]:
            self.check_err(a.node(None, d), d)
            self.check_err(a.way(None, d, None), d)
            self.check_err(a.relation(None, d, None), d)
