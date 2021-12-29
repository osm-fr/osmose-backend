#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights osmose project 2021                                        ##
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
import re
from datetime import date
from modules.Stablehash import stablehash64

class ConditionalRestrictions(Plugin):
  def init(self, logger):
    Plugin.init(self, logger)

    self.ReYear = re.compile(r'20\d\d') # Update in 2099
    self.ReSimpleCondition = re.compile(r'^\w+$', re.ASCII)
    self.currentYear = date.today().year

    self.errors[33501] = self.def_class(item = 3350, level = 2, tags = ['highway', 'fix:chair'],
        title = T_('Bad conditional restriction'),
        detail = T_('''Conditional restrictions should follow `value @ condition; value2 @ condition2` syntax.
Combined restrictions should follow `value @ (condition1 AND condition2)`.
Parentheses `()` must be used around the condition if the condition itself contains semicolons `;`, i.e. `value @ (date;date)`.'''),
        resource="https://wiki.openstreetmap.org/wiki/Conditional_restrictions")
    self.errors[33502] = self.def_class(item = 3350, level = 3, tags = ['highway', 'fix:chair'],
        title = T_('Suboptimal conditional restriction'),
        detail = T_('''Although valid, it is recommended to format conditional restrictions with:
- spaces around the `@`;
- uppercase `AND` (in combined restrictions);
- parentheses around all-but-the-simplest conditions. 
This helps to prevent errors and improves readability.
For example, use `no @ (weight > 5 AND wet)` rather than `no@weight>5 and wet`.'''),
        resource="https://wiki.openstreetmap.org/wiki/Conditional_restrictions")
    self.errors[33503] = self.def_class(item = 3350, level = 3, tags = ['highway', 'fix:chair'],
        title = T_('Expired conditional'),
        detail = T_('''This conditional was only valid up to a date in the past. It can likely be removed.'''),
        trap = T_('''Other tags might need to be updated too to reflect the new situation.'''))

  def way(self, data, tags, nds):
    # Get the relevant tags with *:conditional
    tags_conditional = {}
    for tag in tags:
      if tag[-12:] == ":conditional":
        if "source:" in tag or "note:" in tag or "fixme:" in tag:
          continue
        tags_conditional[tag] = tags[tag]
    if len(tags_conditional) == 0:
      return

    err = []
    for tag in tags_conditional:
      tag_value = tags_conditional[tag]
      conditions = []
      parentheses = 0
      bad_tag = False

      if not "@" in tag_value:
        err.append({"class": 33501, "subclass": 0 + stablehash64(tag + '|' + tag_value), "text": T_("Missing `@` in \"{0}\"", tag)})
        continue

      # Conditionals are split by semicolons, i.e. value @ condition; value @ condition
      # Herein, condition can also contain semicolons, e.g. no @ (Mo 06:00-24:00; Tu-Fr 00:00-24:00)
      # In this case, the condition is wrapped in parentheses ( )
      # Additionally, there's the magic keyword 'AND' to combine conditions

      # Get the parts after the @ excluding parentheses and put them in the list conditions
      # Also validate the syntax of value @ (condition); value @ condition is obeyed
      tmp_str = ""
      condition_started = False
      for c in tag_value:
        if c == "@":
          if len(tmp_str.strip()) == 0:
            err.append({"class": 33501, "subclass": 1 + stablehash64(tag + '|' + tag_value), "text": T_("Missing value for the condition in \"{0}\"", tag)})
            bad_tag = True
            break
          tmp_str = ""
          condition_started = True
        elif c == "(":
          parentheses += 1
          if not condition_started:
            err.append({"class": 33501, "subclass": 0 + stablehash64(tag + '|' + tag_value), "text": T_("Missing `@` in \"{0}\"", tag)})
            bad_tag = True
            break
        elif c == ")":
          parentheses -= 1
          if parentheses == -1:
            err.append({"class": 33501, "subclass": 2 + stablehash64(tag + '|' + tag_value), "text": T_("Mismatch in the number of parentheses in \"{0}\"", tag)})
            bad_tag = True
            break
        elif c == ";" and parentheses == 0 and condition_started:
          tmp_str = tmp_str.strip()
          if len(tmp_str) == 0:
            err.append({"class": 33501, "subclass": 3 + stablehash64(tag + '|' + tag_value), "text": T_("Missing condition, `@` or parentheses in \"{0}\"", tag)})
            bad_tag = True
            break
          conditions.append(tmp_str)
          condition_started = False
          tmp_str = ""
        else:
          tmp_str += c

      if not bad_tag:
        if parentheses == 0:
          # Last condition wouldn't be added in the loop
          tmp_str = tmp_str.strip()
          if not condition_started or len(tmp_str) == 0:
            err.append({"class": 33501, "subclass": 3 + stablehash64(tag + '|' + tag_value), "text": T_("Missing condition, `@` or parentheses in \"{0}\"", tag)})
            continue
          conditions.append(tmp_str)
        else:
          err.append({"class": 33501, "subclass": 2 + stablehash64(tag + '|' + tag_value), "text": T_("Mismatch in the number of parentheses in \"{0}\"", tag)})
          continue

      # Check the position of AND is ok
      if not bad_tag:
        for condition in conditions:
          tmp_cond = " " + condition.replace(" ", "  ") + " "
          tmp_ANDsplitted = tmp_cond.upper().split(" AND ")
          for splittedANDpart in tmp_ANDsplitted:
            if len(splittedANDpart.strip()) == 0:
              err.append({"class": 33501, "subclass": 4 + stablehash64(tag + '|' + tag_value), "text": T_("Missing condition before or after AND combinator in \"{0}\"", tag)})
              bad_tag = True
              break

      if bad_tag:
        continue

      # Find outdated conditional restrictions, i.e. temporary road closures
      for condition in conditions:
        years_str = re.findall(self.ReYear, condition)
        if len(years_str) == 0:
          continue

        maxYear = int(max(years_str))
        if maxYear < self.currentYear:
          err.append({"class": 33503, "subclass": 0 + stablehash64(tag + '|' + tag_value + '|' + condition), "text": T_("Condition \"{0}\" in \"{1}\" was only valid until {2}", condition, tag, maxYear)})

      # No parentheses around conditions
      if tag_value.count("(") < len(conditions):
        if not (tag_value.count("(") == len(conditions) - 1 and not tag_value[-1] == ")" and re.search(self.ReSimpleCondition, conditions[-1])):
          # Accept no parentheses around the last one if the last condition was a simple one
          err.append({"class": 33502, "subclass": 0 + stablehash64(tag + '|' + tag_value), "text": T_("Add parentheses around the condition in \"{0}\"", tag)})

    if err != []:
      return err

  def node(self, data, tags):
    return self.way(data, tags, None)

  def relation(self, data, tags, members):
    return self.way(data, tags, None)

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = ConditionalRestrictions(None)
        a.init(None)

        # Valid conditionals
        for t in [{"highway": "residential"},
                  {"highway": "residential", "access:conditional": "no@wet"}, # note: remove if we start warning about missing spaces around @
                  {"highway": "residential", "access:conditional": "no @ wet", "source:access:conditional": "survey"},
                  {"highway": "residential", "maxspeed:conditional": "20 @ (06:00-19:00)"},
                  {"highway": "residential", "maxspeed:conditional": "20 @ (06:00-20:00); 100 @ (22:00-06:00)"},
                  {"highway": "residential", "access:forward:conditional": "delivery @ (Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00)"},
                  {"highway": "residential", "access:forward:conditional": "no @ (10:00-18:00 AND length>5)"},
                  {"highway": "residential", "access:conditional": "no @ 2099"},
                  {"highway": "residential", "access:conditional": "no @ (2099 May 22-2099 Oct 7)"},
                  {"highway": "residential", "access:conditional": "no @ (2010 May 22-2099 Oct 7)"},
                  {"highway": "residential", "turn:lanes:forward:conditional": "left|through|through;right @ (Mo-Fr 06:00-09:00)"},
                 ]:
          assert not a.way(None, t, None), a.way(None, t, None)

        # Expired conditionals
        for t in [{"highway": "residential", "access:forward:conditional": "no @ 2020"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7)"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7); delivery @ 2099"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7); destination @ (length < 4)"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7 AND weight > 5)"},
                 ]:
          assert a.way(None, t, None), a.way(None, t, None)

        # Invalid conditionals
        for t in [{"highway": "residential", "access:conditional": "no"},
                  {"highway": "residential", "access:forward:conditional": "no @ 2098;2099"},
                  {"highway": "residential", "access:conditional": "delivery @ Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00"},
                  {"highway": "residential", "access:conditional": "delivery @ Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00)"},
                  {"highway": "residential", "access:conditional": "delivery @ (Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00"},
                  {"highway": "residential", "access:conditional": "delivery @ (Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00))"},
                  {"highway": "residential", "access:conditional": "delivery @ Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00);yes@wet"},
                  {"highway": "residential", "access:conditional": "delivery @ (Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00;yes@wet"},
                  {"highway": "residential", "access:conditional": "delivery @ (Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00));yes@wet"},
                  {"highway": "residential", "access:conditional": "yes @ ()"},
                  {"highway": "residential", "access:conditional": "yes @"},
                  {"highway": "residential", "access:conditional": "@ wet"},
                  {"highway": "residential", "access:conditional": "no @ (2099 May 22 AND AND 2099 Oct 7)"},
                  {"highway": "residential", "access:conditional": "no @ (2099 May 22 AND 2099 Oct 7 AND); delivery @ wet"},
                  {"highway": "residential", "maxweight:conditional": "27000 lbs (axles=2); 41400 lbs @ (axles=3); 48600 lbs @ (axles>=4)"},
                 ]:
          assert a.way(None, t, None), a.way(None, t, None)

          # Optimizable, yet valid conditions
          for t in [{"highway": "residential", "access:conditional": "no @ 2099 May 22-2099 Oct 7"},
                    {"highway": "residential", "access:conditional": "no @ wet; no @ snow"},
                    {"highway": "residential", "access:conditional": "no @ wet; no @ (20:00-22:00)"},
                 ]:
          assert a.way(None, t, None), a.way(None, t, None)

          # Nodes
          assert not a.node(None, {"barrier": "lift_gate", "access:conditional": "no @ wet"})
          assert a.node(None, {"barrier": "lift_gate", "access:conditional": "no @ Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00"})

          # Relations
          assert not a.relation(None, {"type": "restriction", "restriction:conditional": "no_u_turn @ (06:00-22:00)"}, None)
          assert a.relation(None, {"type": "restriction", "restriction:conditional": "no_u_turn @ 06:00-22:00)"}, None)
