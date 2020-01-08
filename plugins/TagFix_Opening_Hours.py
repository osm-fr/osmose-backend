#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights rezemika 2018                                              ##
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

try:
    from modules.oh_sanitizer import sanitize_field, SanitizeError, InconsistentField
    module_oh_sanitizer = True
except ImportError as e:
    print(e)
    module_oh_sanitizer = False

class TagFix_Opening_Hours(Plugin):

    def init(self, logger):
        if not module_oh_sanitizer:
            return False
        Plugin.init(self, logger)
        self.errors[32501] = self.def_class(item = 3250, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Invalid Opening Hours'))

    def sanitize_tags(self, tags):
        if 'opening_hours' not in tags:
            return

        try:
            sanitized_field = sanitize_field(tags['opening_hours'])
            if sanitized_field.replace(' ', '').replace('0', '').lower() != tags['opening_hours'].replace(' ', '').replace('0', '').lower(): # Ignore sapce and 0 changes
                return {"class": 32501, "subclass": 0, 'fix': {'opening_hours': sanitized_field}}
        except InconsistentField as e:
            return {"class": 32501, "subclass": 1, 'text': {'en': str(e)}}
        except SanitizeError:
            return {"class": 32501, "subclass": 2}

    def node(self, data, tags):
        return self.sanitize_tags(tags)

    def way(self, data, tags, nds):
        return self.sanitize_tags(tags)

    def relation(self, data, tags, members):
        return self.sanitize_tags(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Opening_Hours(None)
        a.init(None)

        self.check_err(a.node(None, {'opening_hours': 'mo-fr 10h - 19h00'}))
        self.check_err(a.node(None, {'opening_hours': 'mo-fr 10h - 19h00"'}))
        self.check_err(a.node(None, {'opening_hours': '2010 - 2020/2 dec-feb 10:00 am - 12:00 am/1:00 pm-7:00pm'}))

        assert not a.node(None, {'opening_hours': 'Mo-Fr 10:00-19:00'})
        assert not a.node(None, {'opening_hours': 'Mo-Fr   10:00 -19:00'})
