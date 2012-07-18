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
        self.errors[3032] = { "item": 3032, "level": 1, "tag": ["tag"], "desc": {"en": u"Watch multiple tags"} }
        self.errors[1050] = { "item": 1050, "level": 1, "tag": ["highway", "roundabout"], "desc": {"fr":"Rond-point à l'envers", "en":"Reverse roundabout"} }


        import re
        self.Eglise = re.compile(u"(.glise|chapelle|basilique|cath.drale) de .*", re.IGNORECASE)
        self.EgliseNot1 = re.compile(u"(.glise|chapelle|basilique|cath.drale) de la .*", re.IGNORECASE)
        self.EgliseNot2 = re.compile(u"(.glise|chapelle|basilique|cath.drale) de l'.*", re.IGNORECASE)
        self.MonumentAuxMorts = re.compile(u"monument aux morts.*", re.IGNORECASE)
        self.SalleDesFetes = re.compile(u".*salle des f.tes.*", re.IGNORECASE)
        self.MaisonDeQuartier = re.compile(u".*maison de quartier.*", re.IGNORECASE)
        self.Al = re.compile(u"^(all?\.?) .*", re.IGNORECASE)

    def node(self, data, tags):
        err = []

        if "school:FR" in tags and "amenity" not in tags:
            err.append((3032, 5, {"fr": u"Il faut un tag amenity=nursery|kindergarten|school en plus de school:FR"}))

        if "highway" in tags and tags["highway"] == "mini_roundabout" and "direction" in tags:
            if tags["direction"] == "clockwise":
                err.append((1050, 1000, {"fr": u"Le sens des minis giratoires sur le pays est normalement \"anticlockwise\"", "fix": {"-": ["direction"]}}))
            if tags["direction"] in ["anticlockwise", "anti_clockwise"]:
                err.append((1050, 1001, {"fr": u"Le sens des minis giratoires est par défaut \"anticlockwise\", tag direction inutile", "fix": {"-": ["direction"]}}))

        if not "name" in tags:
            return err

        if "amenity" in tags:
            if tags["amenity"] == "place_of_worship":
                if self.Eglise.match(tags["name"]) and not self.EgliseNot1.match(tags["name"]) and not self.EgliseNot2.match(tags["name"]):
                    err.append((3032, 1, {"fr": u"\"name=%s\" est la localisation mais pas le nom" % (tags["name"])}))
        if "historic" in tags:
            if tags["historic"] == "monument":
                if self.MonumentAuxMorts.match(tags["name"]):
                    err.append((3032, 2, {"fr": u"Un monument aux Morts n'est pas un historic=monument", "fix": {"historic": "memorial"} }))

        if (not "highway" in tags) and (self.SalleDesFetes.match(tags["name"]) or self.MaisonDeQuartier.match(tags["name"])) and not ("amenity" in tags and tags["amenity"] == "community_centre"):
            err.append((3032, 3, {"fr": u"Mettre un tag pour une salle des fêtes ou une maison de quartier", "fix": {"+": {"amenity": "community_centre"}} }))

        r = self.Al.match(tags["name"])
        if "highway" in tags and r:
            al = r.group(1)
            err.append((3032, 4, {"fr": u"Pas d'abréviation pour Allée", "fix": {"name": tags["name"].replace(al, u"Allée")} }))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

if __name__ == "__main__":
    a = TagACorriger_MultipleTag_fr(None)
    a.init(None)
    for d in ["clockwise", "anticlockwise"]:
        if not a.node(None, {"highway":"mini_roundabout", "direction":d}):
            print "nofail: %s" % d
