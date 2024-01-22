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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from modules.Stablehash import stablehash64

try:
    from PyKOpeningHours.PyKOpeningHours import OpeningHours, Error
    module_PyKOpeningHours = True
except ImportError as e:
    print(e)
    module_PyKOpeningHours = False

class TagFix_Opening_Hours(Plugin):

    def init(self, logger):
        if not module_PyKOpeningHours:
            return False
        Plugin.init(self, logger)
        self.errors[32501] = self.def_class(item = 3250, level = 3, tags = ['value', 'fix:chair'],
            title = T_('Invalid Opening Hours'))

        self.OHkeys = ['opening_hours', 'opening_hours:kitchen', 'opening_hours:drive_through']

    # Function is also called from ConditionalRestrictions
    def sanitize_openinghours(self, openinghours_value):
        if not module_PyKOpeningHours:
            return
        parser = OpeningHours()
        parser.setExpression(openinghours_value)
        if parser.error() == Error.SyntaxError or parser.error() == Error.IncompatibleMode:
            return {"isValid": False}
        sanitized_field = parser.normalizedExpression()
        # Ignore trivial changes that can be fixed by bots rather than humans like spaces, case errors, etc
        simplify = lambda s: s.replace(' ', '').replace('24:00', '00:00').replace('0', '')
        if simplify(sanitized_field) != simplify(openinghours_value):
            return {"isValid": False, 'fix': sanitized_field}
        return {"isValid": True}

    def node(self, data, tags):
        err = []
        for tag in self.OHkeys:
            if not tag in tags:
                continue
            sanitized = self.sanitize_openinghours(tags[tag])
            if not sanitized['isValid']:
                if "fix" in sanitized:
                    err.append({"class": 32501, "subclass": 0+stablehash64(tag), 'fix': {tag: sanitized['fix']}})
                else:
                    err.append({"class": 32501, "subclass": 1+stablehash64(tag), 'text': T_("The `{0}` value is invalid and could not be parsed", tag)})
        if err != []:
            return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_Opening_Hours(None)
        a.init(None)

        for k in ['opening_hours', 'opening_hours:kitchen']:
            # These should return a modification suggestion
            self.check_err(a.node(None, {k: 'mo-fr 10h - 19h00'}), expected={"class": 32501, 'fix': {k: 'Mo-Fr 10:00-19:00'}})
            self.check_err(a.node(None, {k: 'Monday to Friday 8:00AM to 4:30PM'}), expected={"class": 32501, 'fix': {k: 'Mo-Fr 08:00-16:30'}})

            # These return a parse error
            self.check_err(a.node(None, {k: 'mo-fr 10h - 19h00"'}), expected={"class": 32501})
            self.check_err(a.node(None, {k: '09:00-21:00 TEL/072(360)3200'}), expected={"class": 32501})

            # These are OK, no suggestion
            assert not a.node(None, {k: 'Mo-Fr 10:00-19:00'})
            assert not a.node(None, {k: 'Mo-Tu,Th-Fr 09:30-12:00; We 15:00-17:00; Dec 24,31 off; Sa,Su off; PH off'})
            assert not a.node(None, {k: 'Mo off, Tu-Th 09:00-18:00; Fr 09:00-19:00; Sa 08:00-18:00; Su off'})

            # Check 00:00 and 24:00 are both OK
            assert not a.node(None, {k: 'Mo-Su 09:00-00:00'})
            assert not a.node(None, {k: 'Mo-Su 09:00-24:00'})

        # Should be OK https://github.com/osm-fr/osmose-backend/issues/1568
        assert not a.node(None, {'opening_hours': 'Tu-Fr 11:00-19:00; Sa 10:00-22:15; 14:00-15:00 closed'})
