#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Black Myst <black.myst@free.fr> 2011                       ##
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

import os
from inspect import getframeinfo, stack


class PluginMapCSS(Plugin):
    mapcss_lineno = None

    def def_class(self, **kwargs):
        if 'source' not in kwargs:
            lineno = '#L{0}'.format(self.mapcss_lineno) if self.mapcss_lineno else ''
            if hasattr(self, 'MAPCSS_URL') and self.MAPCSS_URL:
                kwargs['source'] = '{0}{1}'.format(self.MAPCSS_URL, lineno)
            elif self.father and self.father.config:
                config = self.father.config
                caller = getframeinfo(stack()[1][0]).filename.replace('.py', '.validator.mapcss')
                kwargs['source'] = '{0}/plugins/{1}{2}'.format(config and hasattr(config, 'source_url') and config.source_url or None, os.path.basename(caller), lineno)

        return super().def_class(**kwargs)



from plugins.Plugin import TestPluginCommon

class TestPluginMapcss(TestPluginCommon):

    def check_err(self, error, **kwargs):
        if "text" in error and "en" in error["text"]:
            disallowed_str_in_text = ['{', '}']
            assert not any(c in disallowed_str_in_text for c in error["text"]["en"]), ("Encountered any of '" +
              ''.join(disallowed_str_in_text) + "' in text: " + error["text"]["en"])

        return super().check_err(error, **kwargs)
