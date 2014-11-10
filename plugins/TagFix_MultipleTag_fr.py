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


class TagFix_MultipleTag_fr(Plugin):

    only_for = ["fr"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3032] = { "item": 3032, "level": 1, "tag": ["tag", "fix:chair"], "desc": T_(u"Watch multiple tags") }

        import re
        self.Eglise = re.compile(u"(.glise|chapelle|basilique|cath.drale) de .*", re.IGNORECASE)
        self.EgliseNot1 = re.compile(u"(.glise|chapelle|basilique|cath.drale) de la .*", re.IGNORECASE)
        self.EgliseNot2 = re.compile(u"(.glise|chapelle|basilique|cath.drale) de l'.*", re.IGNORECASE)
        self.MonumentAuxMorts = re.compile(u"monument aux morts.*", re.IGNORECASE)
        self.SalleDesFetes = re.compile(u".*salle des f.tes.*", re.IGNORECASE)
        self.MaisonDeQuartier = re.compile(u".*maison de quartier.*", re.IGNORECASE)
        self.Al = re.compile(u"^(all?\.?) .*", re.IGNORECASE)
        self.Marche = re.compile(u"marché( .+)?", re.IGNORECASE)

    def node(self, data, tags):
        err = []

        if not "name" in tags:
            return err

        if "amenity" in tags:
            if tags["amenity"] == "place_of_worship":
                if self.Eglise.match(tags["name"]) and not self.EgliseNot1.match(tags["name"]) and not self.EgliseNot2.match(tags["name"]):
                    err.append((3032, 1, {"en": u"\"name=%s\" is the localisation but not the name" % (tags["name"]), "fr": u"\"name=%s\" est la localisation mais pas le nom" % (tags["name"])}))
        else:
            if "shop" not in tags and self.Marche.match(tags["name"]):
                err.append({"class": 3032, "subclass": 5, 
                            "fix": {"amenity": "marketplace"}})

        if "historic" in tags:
            if tags["historic"] == "monument":
                if self.MonumentAuxMorts.match(tags["name"]):
                    err.append({"class": 3032, "subclass": 2,
                                "text": {"en": u"A war memorial is not a historic=monument", "fr": u"Un monument aux morts n'est pas un historic=monument"},
                                "fix": {"historic": "memorial"} })

        if (not "highway" in tags) and (self.SalleDesFetes.match(tags["name"]) or self.MaisonDeQuartier.match(tags["name"])) and not ("amenity" in tags and tags["amenity"] == "community_centre"):
            err.append({"class": 3032, "subclass": 3,
                        "text": {"en": u"Put a tag for a village hall or a community center", "fr": u"Mettre un tag pour une salle des fêtes ou une maison de quartier"},
                        "fix": {"+": {"amenity": "community_centre"}} })

        r = self.Al.match(tags["name"])
        if "highway" in tags and r:
            al = r.group(1)
            err.append({"class": 3032, "subclass": 4,
                        "text": {"en": u"No abbreviation for french \"Allée\"", "fr": u"Pas d'abréviation pour Allée"},
                        "fix": {"name": tags["name"].replace(al, u"Allée")} })

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_MultipleTag_fr(None)
        class _config:
            options = {"language": "fr"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)
        for t in [{"amenity": "place_of_worship", "name": u"Église de Paris"},
                  {"amenity": "place_of_worship", "name": u"Cathédrale de Notre-Dame"},
                  {"name": u"Marché des Capucines"},
                  {"historic": "monument", "name": u"Monument aux morts du quartier"},
                  {"name": u"Salle des fêtes"},
                  {"name": u"Maison de quartier"},
                  {"highway": "primary", "name": u"All. des Roses"},
                 ]:
            self.check_err(a.node(None, t), t)
            self.check_err(a.way(None, t, None), t)
            self.check_err(a.relation(None, t, None), t)

        for t in [{"amenity": "place_of_worship", "name": u"Église de l'endroit"},
                  {"shop": "yes", "name": u"Marché des Capucines"},
                  {"amenity":"place_of_worship"},
                  {"historic": "yes", "name": u"Monument aux morts du quartier"},
                  {"historic": "monument", "name": u"Monument typique du quartier"},
                  {"highway": "primary", "name": u"Salle des fêtes"},
                  {"highway": "residential", "name": u"Maison de quartier"},
                  {"amenity": "community_centre", "name": u"Salle des fêtes"},
                  {"amenity": "community_centre", "name": u"Maison de quartier"},
                  {"highway": "primary", "name": u"Allée des Roses"},
                 ]:
            assert not a.way(None, t, None), t
