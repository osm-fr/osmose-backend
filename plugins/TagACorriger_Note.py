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

from plugins.Plugin import Plugin
import urllib, re
import unicodedata


class TagACorriger_Note(Plugin):

    only_for = ["fr"]

    def normalize(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')).lower()

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[3110] = {"item": 3110, "desc": {"en": u"Improve note or comment tags", "fr": u"Amélioration possible des tags note ou comment"} }
        self.FixmeFull = (
            "fix me", "grosso modo", "note de memoire", )
        self.FixmeWord = (
            "?",  "accurate",  "approximatif",  "approximation",
            "approximativement",  "attendre",  "bad",  "check",  "checkme",
            "completer",  "corriger",  "crappy",  "draft",  "effacer",
            "estimation",  "exact",  "gourre",  "incomplete",  "renderers",
            "rendering",  "semblant",  "semble",  "tag",  "tagged",  "tagguer",
            "todo",  "uncertain",  "verified",  "verifier",  "wip", )
        self.Opening_hours = (
            "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche",
            "janvier",  "fevrier",  "mars",  "avril",  "mai",  "juin",  "juillet",
            "aout",  "septembre",  "octobre",  "novembre",  "decembre", )
        self.Destruction = (
            "ferme",  "fermee",  "ancien",  "ancienne",  "brule",  "brulee",  "burn",  "closed",  "declasse",
            "declassee",  "demoli",  "demolished",  "demolition",  "destroyed",
            "detruit",  "no_longer",  "rase",  "rasee", )
        self.Construction = (
            "construction", "travaux", "ouvert", "ouverture")
        self.TagFull = (
            "arret de bus",  "http://",  "maison de retraite",  "reserve naturelle",
            "salle des fetes",  "voies de service",  "zone 30", )
        self.TagWord = (
            "football",  "basket",  "bassin",  "canal",  "cyclable",  "ecluse",
            "ehpad",  "entree",  "etang",  "garages",  "gare",  "gendarmerie",
            "gynmase",  "halles",  "handball",  "hangar",  "jardin",  "piste",
            "plot",  "prairie",  "prive",  "ruin",  "ruine",  "sortie",  "tel",  "toilettes",
            "transformateur",  "verger",  "volley", )
        self.Hours = re.compile("[0-9]{1,2}h")
        self.Date = re.compile("[0-9]{4,8}|(?:(?:[0-9]{1,2}/){2}/[0-9]{2,4})")
        self.Split = re.compile('[- _\(\),.:/''"+!;<>=\[\]]')

    def node(self, data, tags):
        if "note" not in tags and "comment" not in tags:
            return

        for t in ("note", "comment"):
            if t not in tags:
                continue
            if 'http://wiki.openstreetmap.org' in tags[t] or 'CLC import' in tags[t]: # Skip French man_made=survey_point note tag
                continue
            tt = self.normalize(tags[t])
            words = re.split(self.Split, tt)
            # Add FIXME on note tag
            if 'FIXME' not in tags and ('note' not in tags or 'fixme' not in tags['note']):
                for w in self.FixmeFull:
                    if w in tt:
                        return [(3110, 100, {"fr": u"Le tag note devrait avoir un \"FIXME\" : \"%s\"" % tags[t], "en": u"note tag need FIXME : \"%s\"" % tags[t]})]
                for w in self.FixmeWord:
                    if w in words:
                        return [(3110, 101, {"fr": u"Le tag note devrait avoir un \"FIXME\" : \"%s\"" % tags[t], "en": u"note tag need FIXME : \"%s\"" % tags[t]})]
            # Destruction
            if 'end_date' not in tags and 'historic' not in tags and 'disused' not in tags and 'abandoned' not in tags:
                for w in self.Destruction:
                    if w in tt:
                        return [(3110, 500, {"fr": u"Utiliser un tag pour signifier l'arret : \"%s\"" % tags[t], "en": u"Use a tag to specity end : \"%s\"" % tags[t]})]
            # start_date
            if 'start_date' not in tags:
                if self.Date.match(tt) or "siecle" in tt:
                    return [(3110, 300, {"fr": u"Utiliser le tag start_date pour \"%s\"" % tags[t], "en": u"Use start_date tag for \"%s\"" % tags[t]})]
            # opening_hours
            if 'opening_hours' not in tags:
                if self.Hours.match(tt):
                    return [(3110, 200, {"fr": u"Utiliser le tag opening_hours pour \"%s\"" % tags[t], "en": u"Use opening_hours tag for \"%s\"" % tags[t]})]
                for w in self.Opening_hours:
                    if w in words:
                        return [(3110, 201, {"fr": u"Utiliser le tag opening_hours pour \"%s\"" % tags[t], "en": u"Use opening_hours tag for \"%s\"" % tags[t]})]
            # construction
            if 'construction' not in tags:
                for w in self.Construction:
                    if w in words:
                        return [(3110, 400, {"fr": u"Utiliser le tag construction pour \"%s\"" % tags[t], "en": u"Use construction tag for \"%s\"" % tags[t]})]
            # an other tag
            for w in self.TagFull:
                if w in tt:
                    return [(3110, 900, {"fr": u"\"%s\" peut être mis dans un tag spécifique" % tags[t], "en": u"\"%s\" can be set in specific tag" % tags[t]})]
            for w in self.TagWord:
                if w in words:
                    return [(3110, 901, {"fr": u"\"%s\" peut être mis dans un tag spécifique" % tags[t], "en": u"\"%s\" can be set in specific tag" % tags[t]})]

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)

if __name__ == "__main__":
    a = TagACorriger_Note(None)
    a.init(None)
    for d in [u"fix me", u"a corriger", u"Du lundi au vendredi", u"9h-12h/14h-17h", u"20091211", u"travaux", u"Salle des Fêtes", u"gendarmerie", u"See http://gpvlyonduchere", u"demolished"]:
        if not a.node(None, {"note":d}):
            print "fail: %s" % d
