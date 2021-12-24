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
    self.currentYear = date.today().year

    self.errors[33501] = self.def_class(item = 3350, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Bad conditional restriction'),
            detail = T_('''Conditional restrictions should follow `value @ condition; value2 @ condition2` syntax.
Combined restrictions should follow `value @ (condition1 AND condition2)
Parentheses `()` should be used if the condition itself contains semicolons `;` too'''))
    self.errors[33502] = self.def_class(item = 3350, level = 3, tags = ['highway', 'fix:chair'],
            title = T_('Use uppercase `and` to combine conditions'),
            detail = T_('''For readability, `AND` (uppercase) is to be preferred over lowercase variants when combining restrictions'''))
    self.errors[33503] = self.def_class(item = 3350, level = 3, tags = ['highway', 'fix:chair'],
            title = T_('Expired conditional'),
            detail = T_('''This conditional was only valid up to a date in the past. It can likely be removed'''),
            trap = T_('''Other tags might need to be updated too to reflect the new situation'''))




  def way(self, data, tags, nds):
    # Currently only checking highways with conditionals
    if not "highway" in tags:
      return

    # Get the relevant tags with *:conditional
    tags_conditional = {}
    for tag in tags:
      if tags[tag][-12:] == ":conditional":
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
        err.append({"class": 33501, "subclass": 0 + stablehash64(tag + '|' + tag_value), "text": T_("Missing `@`")})
        continue

      # Conditionals are split by semicolons, i.e. value @ condition; value @ condition
      # Herein, condition can also contain semicolons, e.g. no @ (Mo 06:00-24:00; Tu-Fr 00:00-24:00)
      # In this case, the condition is wrapped in parentheses ( )
      # Additionally, there's the magic keyword 'AND' to combine conditions

      # Get the parts after the @ excluding parentheses and put them in the list conditions
      # Also validate the syntax of value @ (condition); value @ condition is obeyed
      tmp_str = ""
      for c in tag_value:
        if c == "@":
          if len(tmp_str.strip()) == 0:
            err.append({"class": 33501, "subclass": 1 + stablehash64(tag + '|' + tag_value), "text": T_("Missing value for the condition")})
            bad_tag = True
            break
          tmp_str = ""
        elif c == "(":
          parentheses += 1
          continue
        elif c == ")":
          parentheses -= 1
          if parentheses == -1:
            err.append({"class": 33501, "subclass": 2 + stablehash64(tag + '|' + tag_value), "text": T_("Mismatch in the number of parentheses")})
            bad_tag = True
            break
        elif c == ";" and parentheses == 0:
          tmp_str = tmp_str.strip()
          if len(tmp_str) == 0:
            err.append({"class": 33501, "subclass": 3 + stablehash64(tag + '|' + tag_value), "text": T_("Missing condition")})
            bad_tag = True
            break
          conditions.append(tmp_str)
          tmp_str = ""
        else:
          tmp_str += c

      if not bad_tag:
        if parentheses == 0:
          # Last condition wouldn't be added in the loop
          tmp_str = tmp_str.strip()
          if len(tmp_str) == 0:
            err.append({"class": 33501, "subclass": 3 + stablehash64(tag + '|' + tag_value), "text": T_("Missing condition")})
            continue
          conditions.append(tmp_str)
        else:
          err.append({"class": 33501, "subclass": 2 + stablehash64(tag + '|' + tag_value), "text": T_("Mismatch in the number of parentheses")})
          continue

      # Check the position of AND is ok
      if not bad_tag:
        for condition in conditions:
          tmp_cond = " " + condition + " "
          tmp_ANDsplitted = tmp_cond.upper().split(" AND ")
          for splittedANDpart in tmp_ANDsplitted:
            if len(splittedANDpart.strip()) == 0:
              err.append({"class": 33501, "subclass": 4 + stablehash64(tag + '|' + tag_value), "text": T_("Missing condition before or after AND combinator")})
              bad_tag = True
              break

          if not bad_tag and tmp_cond.count(" AND ") != tmp_cond.upper().count(" AND "):
            err.append({"class": 33502, "subclass": 0 + stablehash64(tag + '|' + tag_value)}) # Recommendation to use uppercase "AND". Not a true error

      if bad_tag:
        continue


      # Find outdated conditional restrictions, i.e. temporary road closures
      for condition in conditions:
        years_str = re.findall(self.ReYear, condition)
        if len(years_str) == 0:
          continue

        maxYear = int(max(years_str))
        if maxYear < self.currentYear:
          err.append({"class": 33503, "subclass": 0 + stablehash64(tag + '|' + tag_value + '|' + condition), "text": T_("Condition \"{0}\" was only valid until {1}", condition, maxYear)})

    if err != []:
      return err



###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = ConditionalRestrictions(None)
        a.init(None)

        # Valid conditionals
        for t in [{"highway": "residential"},
                  {"highway": "residential", "access": "no"},
                  {"highway": "residential", "access:conditional": "no @ wet"},
                  {"highway": "residential", "maxspeed:conditional": "20 @ (06:00-19:00)"},
                  {"highway": "residential", "maxspeed:conditional": "20 @ (06:00-20:00); 100 @ (22:00-06:00)"},
                  {"highway": "residential", "access:forward:conditional": "delivery @ (Mo-Fr 06:00-11:00,17:00-19:00;Sa 03:30-19:00)"},
                  {"highway": "residential", "access:forward:conditional": "no @ (10:00-18:00 AND length>5)"},
                  {"highway": "residential", "access:conditional": "no @ 2099"},
                  {"highway": "residential", "access:conditional": "no @ (2099 May 22-2099 Oct 7)"},
                  {"highway": "residential", "access:conditional": "no @ (2010 May 22-2099 Oct 7)"},
                 ]:
          assert not a.way(None, t, None), a.way(None, t, None)

        # Expired conditionals
        for t in [{"highway": "residential", "access:forward:conditional": "no @ 2020"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7)"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7); delivery @ 2099"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7); destination @ length < 4"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22-2020 Oct 7 AND weight > 5)"},
                 ]:
          assert not a.way(None, t, None), a.way(None, t, None)

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
                  {"highway": "residential", "access:conditional": "yes@()"},
                  {"highway": "residential", "access:conditional": "yes@"},
                  {"highway": "residential", "access:conditional": "@wet"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22 AND AND 2020 Oct 7)"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22 AND 2020 Oct 7 AND); delivery @ wet"},
                  {"highway": "residential", "access:conditional": "no @ (2018 May 22 and 2020 Oct 7); delivery @ wet"},
                 ]:
          assert not a.way(None, t, None), a.way(None, t, None)
