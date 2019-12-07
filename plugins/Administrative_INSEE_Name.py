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


class Administrative_INSEE_Name(Plugin):

    only_for = ["FR", "NC"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[800] = self.def_class(item = 6030, level = 1, tags = ['place', 'fix:survey'],
            title = T_('Place node without name tag'),
            detail = T_(
'''The tag `place=*` must always be used in combination with the tag
`name=*`.'''),
            fix = T_(
'''For cities/towns, it is sometimes possible to find the name of the
village based on the boundary relationship and/or if the ref code if is
entered.'''),
            trap = T_(
'''The tag `place=*` is often misused, see
[`place`](https://wiki.openstreetmap.org/wiki/Key:place). It should not
be associated with tags such as `amenity`, `highway`. When the case, the
tag `place=*` should be removed.'''))
        doc = dict(
            detail = T_(
'''Check of tags `ref:INSEE` and `name` are consistent with the [COG
database](https://www.insee.fr/fr/information/2560452).'''),
            fix = T_(
'''Correct INSEE the value or the name as appropriate.'''),
            trap = T_(
'''The names on `place=*` may differ from the COG of INSEE, especially
for merged city. It also happens in several occasions that local
authorities are at odds with INSEE. In this case, that's always been a
priority for the field on OSM.'''))

        self.errors[801] = self.def_class(item = 6040, level = 1, tags = ['place', 'fix:chair'],
            title = T_('INSEE code cannot be found in INSEE database'),
            **doc)
        self.errors[802] = self.def_class(item = 6040, level = 1, tags = ['place', 'fix:chair'],
            title = T_('Municipality name does not match INSEE code'),
            **doc)

        lst = self.father.ToolsReadList("dictionaries/FR/BddCommunes")
        self.communeNameIndexedByInsee = {}

        for x in lst:
            x = x.split("\t")
            code_insee = x[0]
            name_insee = x[1]
            self.communeNameIndexedByInsee[code_insee] = name_insee

    def _check_insee_name(self, code_insee, name_osm, name_alt_osm):

        if code_insee not in self.communeNameIndexedByInsee:
            # The INSEE code is not known
            return {"class": 801, "subclass": 0, "text": {"en": code_insee}}

        name_insee = self.communeNameIndexedByInsee[code_insee]
        if name_osm != name_insee and (not name_alt_osm or name_alt_osm != name_insee):
            simpleName = self.ToolsStripAccents(name_osm.lower().replace(u"-", u" ").replace(u" ", u"")).strip()
            simpleInseeName = self.ToolsStripAccents(name_insee.lower().replace(u"-", u" ").replace(u" ", u"")).strip()
            msg = u"OSM=" + name_osm + u" => COG=" + name_insee
            fix = {"name": name_insee}
            if simpleName == simpleInseeName:
                if ((u"œ" in name_insee) or (u"æ" in name_insee) or
                     (u"Œ" in name_insee) or (u"Æ" in name_insee)):
                    return # No correction on ligation (ML talk-fr 03/2009)
                else:
                    return {"class": 802, "subclass": 1, "text": {"en": msg}, "fix": {"~":fix}}
            else:
                return {"class": 802, "subclass": 2, "text": {"en": msg}, "fix": fix}

    def node(self, data, tags):
        if u"place" in tags:
            if u"name" not in tags:
                # Le nom est obligatoire en complément du tag place.
                return {"class": 800, "subclass": 0, "text": T_(u"Node with place=%s without name", tags[u"place"])}

    def relation(self, relation, tags, members):
        if tags.get(u"boundary") == u"administrative" and tags.get(u"admin_level") == u"8":
            # Seul le niveau 8 contient des INSEE qui nous interresse
            # Le niveau 7 contient d'autre code INSEE (sur 3 chiffres)

            if u"name" not in tags:
                # Le nom est obligatoire en complément du tag place.
                return {"class": 800, "subclass": 0}

            if u"ref:INSEE" in tags:
                # Si en plus on a un ref:Insee, on verifie la coohérance des noms
                return self._check_insee_name(tags[u"ref:INSEE"], tags[u"name"], tags[u"alt_name"] if u"alt_name" in tags else None)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        import os
        import analysers.analyser_sax
        class config:
            dir_scripts = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        a = Administrative_INSEE_Name(analysers.analyser_sax.Analyser_Sax(config()))
        a.init(None)

        for t in [{"highway": "primary"},
                  {"place": "yes", "name": "Ici"},
                  {"place": "yes", "name": u"Béréziat", "ref:INSEE": "01040"},
                  {"place": "yes", "name": "Ici", "alt_name": u"Béréziat", "ref:INSEE": "01040"},
                  {"place": "yes", "name": u"Bonnœil", "ref:INSEE": "14087"},
                  {"place": "yes", "name": u"Bonnoeil", "ref:INSEE": "14087"},
                  {"name": u"Bat", "ref:INSEE": "01040"},
                 ]:
            assert not a.node(None, t), t

        bt = {"boundary": "administrative", "admin_level": "8"}
        for t in [bt,
                  dict(bt, **{"name": "Ici", "ref:INSEE": "90"}),
                  dict(bt, **{"name": u"Bat", "ref:INSEE": "01040"}),
                  dict(bt, **{"name": u"Beréziat", "ref:INSEE": "01040"}),
                  dict(bt, **{"name": u"Béréziàt", "ref:INSEE": "01040"}),
                 ]:
            self.check_err(a.relation(None, t, None), t)

        for t in [{"highway": "primary"},
                  dict(bt, **{"name": "Ici"}),
                  dict(bt, **{"name": u"Béréziat", "ref:INSEE": "01040"}),
                  dict(bt, **{"name": "Ici", "alt_name": u"Béréziat", "ref:INSEE": "01040"}),
                  dict(bt, **{"name": u"Bonnœil", "ref:INSEE": "14087"}),
                  dict(bt, **{"name": u"Bonnoeil", "ref:INSEE": "14087"}),
                 ]:
            assert not a.relation(None, t, None), t
