#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
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

from .Name_Dictionary import P_Name_Dictionary
import re


class Name_Dictionary_Lang_xx(P_Name_Dictionary):

    not_for = ["fr"]

    def init(self, logger):
        P_Name_Dictionary.init(self, logger)

    def init_dictionaries(self):
        self.laod_numbering()


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        import modules.config as config
        from analysers.analyser_sax import Analyser_Sax
        class _config:
            options = {"language": "xx"}
            dir_scripts = config.dir_osmose
        class father(Analyser_Sax):
            config = _config()
            def __init__(self):
                pass
        a = Name_Dictionary_Lang_xx(father())
        a.init(None)
