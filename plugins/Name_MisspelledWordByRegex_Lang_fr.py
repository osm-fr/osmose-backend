###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
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

from plugins.Name_MisspelledWordByRegex import P_Name_MisspelledWordByRegex


class Name_MisspelledWordByRegex_Lang_fr(P_Name_MisspelledWordByRegex):

    only_for = ["fr"]

    def init(self, logger):
        P_Name_MisspelledWordByRegex.init(self, logger)

        import re
        self.ReTests = {}
        self.ReTests[( 0, "École\\2")]      = [re.compile(r"^École(| .*)$"),
                                               re.compile(r"^([EÉée][Cc][Oo][Ll][Ee])(| .*)$")]
        self.ReTests[( 1, "Église\\2")]     = [re.compile(r"^Église(| .*)$"),
                                               re.compile(r"^([EÉée][Gg][l][Ii][Ss][Ee])(| .*)$")]
        self.ReTests[( 2, "La\\2")]         = [re.compile(r"^La(| .*)$"),
                                               re.compile(r"^([Ll][Aa])( .*)$")]
        self.ReTests[( 3, "Étang\\2")]      = [re.compile(r"^Étang(| .*)$"),
                                               re.compile(r"^([EÉée][Tt][Tt]?[AaEe][Nn][GgTt]?)(| .*)$")]
        self.ReTests[( 4, "Saint\\2")]      = [re.compile(r"^Saint(| .*)$"),
                                               re.compile(r"^([Ss](?:[Aa][Ii][Nn])?[Tt]\.?)( .*)$")]
        self.ReTests[( 5, "Hôtel\\2")]      = [re.compile(r"^Hôtel(| .*)$"),
                                               re.compile(r"^([Hh][OoÔô][Tt][Ee][Ll])(| .*)$")]
        self.ReTests[( 6, "Château\\2")]    = [re.compile(r"^Château(| .*)$"),
                                               re.compile(r"^([Cc][Hh][ÂâAa][Tt][Ee][Aa][Uu])(| .*)$")]
        self.ReTests[( 7, "McDonald's\\2")] = [re.compile(r"^McDonald's(| .*)$"),
                                               re.compile(r"^([Mm][Aa]?[Cc] ?[Dd][Oo](?:[Nn][Aa][Ll][Dd]'?[Ss]?)?)(| .+)$")]
        self.ReTests[( 8, "Sainte\\2")]     = [re.compile(r"^Sainte(| .*)$"),
                                               re.compile(r"^([Ss](?:[Aa][Ii][Nn])?[Tt][Ee]\.?)( .*)$")]
        self.ReTests[( 9, "Le\\2")]         = [re.compile(r"^Le(| .*)$"),
                                               re.compile(r"^([Ll][Ee])( .*)$")]
        self.ReTests[(10, "Les\\2")]        = [re.compile(r"^Les(| .*)$"),
                                               re.compile(r"^([Ll][Ee][Ss])( .*)$")]
        self.ReTests[(11, "\\1\\2'\\4")]    = [re.compile(r"[LlDd]'(|[^ ].*)$"),
                                               re.compile(r"(^|.* )([LlDd])( +' +| +'|' +)(|.*)$")]
        self.ReTests = self.ReTests.items()


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Name_MisspelledWordByRegex_Lang_fr(None)
        a.init(None)
        for (d, f) in [("eglise ", "Église "),
                       ("St. Michel", "Saint Michel"),
                       ("Ecole", "École"),
                       ("Mac Donald", "McDonald's"),
                       ("Ste Amal et Fils Sarl", "Sainte Amal et Fils Sarl"),
                       ("SAiNte anne", "Sainte anne"),
                       ("les lesles", "Les lesles"),
                       ("de l' été", "de l'été"),
                       ("de l' ", "de l'"),
                       ("de l 'été", "de l'été"),
                       ("de l '", "de l'"),
                       ("l ' été", "l'été"),
                      ]:
            self.check_err(a.node(None, {"name": d}), ("name='{0}'".format(d)))
            self.assertEqual(a.node(None, {"name": d})["fix"]["name"], f)
            assert not a.node(None, {"name": f}), ("name='{0}'".format(f))

            self.check_err(a.way(None, {"name": d}, None), ("name='{0}'".format(d)))
            self.check_err(a.relation(None, {"name": d}, None), ("name='{0}'".format(d)))
            assert not a.node(None, {"amenity": d}), ("amenity='{0}'".format(d))
