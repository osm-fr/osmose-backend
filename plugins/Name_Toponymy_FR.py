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

from modules.Stablehash import stablehash64
from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin


class Name_Toponymy_FR(Plugin):

    only_for = ["FR", "NC"]
    not_for = ["FR-PF"]

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[906] = self.def_class(item = 5040, level = 2, tags = ['name', 'fix:chair'],
            title = T_('Toponymy'),
            detail = T_(
'''Apply of "[charte de
toponymie](https://web.archive.org/web/2019/http://education.ign.fr/sites/all/files/charte_toponymie_ign.pdf)" of
IGN (French geographic name conventions)'''),
            resource = 'https://web.archive.org/web/2019/http://education.ign.fr/sites/all/files/charte_toponymie_ign.pdf')

        # article 4.9 Majuscules et minuscules
        special  = [""]

        special += ["j", "d", "l", "n", "h"]

        special += ["della"] # way 43563373
        special += ["on"]    # Newark on Tren way/23791990
        special += ["dit"]   # way/32519405
        special += ["dite"]   # way/32519405
        special += ["qui"]   # way/22790488
        special += ["von"]   # way/8481714
        special += ["van"]   # way/4254712
        special += ["dal"]   # way/41271222

        special += ["mon","ma","mes","ton","ta","tes","son","sa","ses","votre","vos","leur","leurs"]

        special += ["bis", "ter"]

        special += ["le", "la", "les", "l", "un", "une"]

        special += ["a", "al", "als", "an", "ar", "d", "das", "de",
                    "dem", "den", "der", "die", "e", "ech", "el",
                    "éla", "els", "en", "er", "era", "ero", "et",
                    "eul", "eun", "eur", "gli", "het", "i", "las",
                    "lé", "lo", "los", "lou", "lous", "s", "t",
                    "u", "ul", "ur"]

        special += ["au", "aux", "du", "des", "ès"]

        special += ["â", "agli", "ai", "al", "als", "am", "as", "beim",
                    "dei", "del", "dels", "det", "dets", "em", "im",
                    "um", "vom", "zum", "zur"]

        special += ["à", "à-bas", "à-haut", "au-deçà", "au-delà", "au-dessous",
                    "au-dessus", "auprès", "bien", "chez", "ci-devant", "contre",
                    "d'", "dans", "de", "deçà", "de-ci", "delà", "de-là",
                    "derrière", "dessous", "dessus", "devant", "en", "entre",
                    "et", "face (à)", "lès", "lez", "loin", "(de)", "mal",
                    "malgré", "mi", "non", "ou", "où", "outre", "outre-mer",
                    "outre-tombe", "outre-Rhin", "par", "par-delà", "par-dessous",
                    "par-dessus", "peu", "près", "sans", "sauf", "sous", "sur",
                    "sus", "tard", "tout", "très", "vers", "vis-à-vis"]

        special += ["a", "auf", "bei", "cal", "can", "d'al laez", "dalaé",
                    "darios", "darré", "debas", "débas", "debat", "débat",
                    "delai", "detras", "di", "durch", "hinter", "in", "nieder",
                    "oben", "ober", "op", "over", "soubre", "soubré", "tras",
                    "tré", "ueber", "unter", "vor", "vorder", "zu", "zwischen",
                    "dell", "delle", "alla", "da", "to", "ins", "dera", "deth",
                    "deths", "y", "alten"]

        special += ["dou", "es", "und"]

        special += ["deu", "dous"] # parlé Gascon (F. Rodrigo)

        special += ["rural", "exploitation"] # Chemin rural / Chemin d'exploitation

        special += ["do"]

        self.special = set(special)

        self.minus = "abcdefghijklmnopqrstuvwxyzàäâéèëêïîöôüûÿ"

        # Les apostrophes sont replacées par des caractères à usage privé d'Unicode
        apost_subst = {"'": "\ue000", "’": "\ue001", "&apos;": "\ue002"}
        special_with_apost = ["c'h", "C'h", "prud'homme", "Prud'homme"]

        self.special_subst = dict()
        for x in special_with_apost:
            for k, v in apost_subst.items():
                before = x.replace("'", k)
                after  = x.replace("'", v)
                self.special_subst[before] = after

    def apply_special_subst(self, name):
        for k, v in self.special_subst.items():
            name = name.replace(k, v)
        return name

    def remove_special_subst(self, name):
        for k, v in self.special_subst.items():
            name = name.replace(v, k)
        return name

    def _split(self, name):
        for x in [" ", "’", "\xa0", "°", "'", "&amp;", "&apos;", "&quot;", "/", ")", "-", "\"", ";", ".", ":", "+", "?", "!", ",", "|", "*", "Â°", "_", "="]:
            name = name.replace(x, "\xffff{0}\xffff".format(x))
        return name.split("\xffff")

    def node(self, data, tags):
        if "name" not in tags:
            return
        if ("highway" not in tags) and ("waterway" not in tags) and ("place" not in tags):
            return
        words = []

        name = tags["name"]
        name_subst = self.apply_special_subst(name)
        split = self._split(name_subst)
        for i in range(0, len(split), 2):
            split[i] = self.remove_special_subst(split[i])
        splitfix = list(split)

        if split and split[0] and split[0][0] in self.minus:
            words.append(split[0])
            splitfix[0] = split[0].capitalize()
        for i in range(0, len(split), 2):
            word = split[i]
            if word in self.special:
                continue
            if word[0] in self.minus:
                words.append(word)
                splitfix[i] = split[i].capitalize()
        if words:
            return {"class": 906, "subclass": stablehash64(','.join(words)), "text": T_("Missing capital letter for: {0}", ", ".join(sorted(set(words)))),
                     "fix": {"name": "".join(splitfix)} }
        return

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_Toponymy_FR(None)
        a.init(None)
        assert not a.node(None, {"place": "yep"})
        assert not a.node(None, {"amenity": "baker", "name": "tio tio tiotio de  tio &apos;tio-tio &amp;tio! "})

        self.check_err(a.node(None, {"highway": "trunk", "name": "Rue des pommiers"}))
        self.check_err(a.way(None, {"highway": "trunk", "name": "Rue des pommiers"}, None))
        self.check_err(a.relation(None, {"highway": "trunk", "name": "Rue des pommiers"}, None))
        assert not a.node(None, {"highway": "trunk", "name": "Rue des Pommiers"})

        e = a.node(None, {"place": "yep", "name": "tio tio tiotio de  tio &apos;tio-tio &amp;tio! "})
        self.check_err(e)
        self.assertEqual(e["fix"]["name"], "Tio Tio Tiotio de  Tio &apos;Tio-Tio &amp;Tio! ")
