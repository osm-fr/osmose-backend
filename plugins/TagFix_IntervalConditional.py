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
from transporthours.main import Main

class TagFix_IntervalConditional(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[32502] = { 'item': 3250, 'level': 3, 'tag': ['value', 'fix:chair', 'public_transport'], 'desc': T_(u'Invalid Conditional Intervals') }
        self._th = Main()

    def check_tags(self, tags):
        if 'interval' not in tags and 'interval:conditional' not in tags:
            return

        # Analyse all tags related to transport hours (interval, interval:conditional, opening_hours)
        parsedData = self._th.tagsToHoursObject(tags)

        # Check validity of interval tag
        if parsedData['defaultInterval'] == 'invalid':
            return { 'class': 32502, 'subclass': 1, 'text': T_(u'Invalid interval tag format') }

        # Check validity of interval:conditional tag
        if parsedData['otherIntervals'] == 'invalid':
            return { 'class': 32502, 'subclass': 2, 'text': T_(u'Conditional intervals tag is not valid') }

        # Check combination of opening_hours, interval and interval:conditional
        if 'opening_hours' in tags and type(parsedData['opens']) is dict and parsedData['allComputedIntervals'] == 'invalid':
            return { 'class': 32502, 'subclass': 3, 'text': T_(u'Conditional intervals does not fit into opening hours') }


    def relation(self, data, tags, members):
        return self.check_tags(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = TagFix_IntervalConditional(None)
        a.init(None)

        self.check_err(a.relation(None, {'interval': 'not minutes'}, None))
        self.check_err(a.relation(None, {'interval': '01:30', 'interval:conditional': 'Invalid conditional'}, None))
        self.check_err(a.relation(None, {'opening_hours': 'Mo-Fr 05:00-23:00', 'interval': '15', 'interval:conditional': '5 @ (Mo-Sa 12:00-15:00)'}, None))

        assert not a.relation(None, {'interval': '00:10'}, None)
        assert not a.relation(None, {'interval': '00:10', 'interval:conditional': '15 @ (Mo-Sa 15:00-17:00)'}, None)
        assert not a.relation(None, {'opening_hours': 'Mo-Su 05:00-23:00', 'interval': '00:10', 'interval:conditional': '15 @ (Mo-Sa 15:00-17:00)'}, None)
