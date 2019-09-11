#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyright Adrien Pavie 2019                                           ##
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
    from transporthours.main import Main
    module_transporthours = True
except ImportError as e:
    print(e)
    module_transporthours = False

class TagFix_IntervalConditional(Plugin):

    def init(self, logger):
        if not module_transporthours:
            return False
        Plugin.init(self, logger)
        self.errors[32502] = {"item": 3250, "level": 3, "tag": ["value", "fix:chair"], "desc": T_(u"Invalid Conditional Intervals")}

    def check_tags(self, tags):
        if 'interval:conditional' not in tags:
            return

        th = Main()

        # Check interval:conditional by itself
        try:
            interval_cond_obj = th.intervalConditionalStringToObject(tags['interval:conditional'])
        except Exception as e:
            return {"class": 32502, "subclass": 1, 'text': {'en': str(e)}}

        # Check combination of interval:conditional + opening_hours
        if 'opening_hours' in tags:
            parsedData = th.tagsToHoursObject(tags)
            if parsedData['allComputedIntervals'] == 'invalid':
                return {"class": 32502, "subclass": 2, 'text': {'en': "Conditional interval definition doesn't fit in opening hours"}}


    def relation(self, data, tags, members):
        return self.check_tags(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_IntervalConditional(None)
        a.init(None)

        self.check_err(a.relation(None, {'interval:conditional': 'Mo-Sa 15:00-17:00'}, None))
        self.check_err(a.relation(None, {'interval:conditional': 'BLA @ (Mo-Sa 15:00-17:00)'}, None))
        self.check_err(a.relation(None, {'interval:conditional': '00:15 @ (Mo-Sa 15:00-17:00); OUPS'}, None))
        self.check_err(a.relation(None, {'interval:conditional': '15 @ (Mo-Sa 15:00-17:00)', 'opening_hours': 'Mo-Sa 16:30-18:30'}, None))

        assert not a.relation(None, {'interval:conditional': '15 @ (Mo-Sa 15:00-17:00)'}, None)
        assert not a.relation(None, {'interval:conditional': '00:15 @ Mo-Sa 15:00-17:00'}, None)
        assert not a.relation(None, {'interval:conditional': '15 @ (Mo-Sa 15:00-17:00); 20 @ (Su 20:00-03:00)'}, None)
        assert not a.relation(None, {'interval:conditional': '15 @ (Mo-Sa 15:00-17:00)', 'opening_hours': 'Mo-Sa 05:00-22:00'}, None)
