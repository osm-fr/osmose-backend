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
from plugins.Plugin import 

class ConditionalRestrictions(Plugin):
  def init(self, logger):
    Plugin.init(self, logger)
    # TODO define errors
    
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
        err.append({}) # TODO - not a conditional
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
            err.append({}) # TODO - no value before @
            bad_tag = True
            break
          tmp_str = ""
        elif c == "(":
          parentheses += 1
          continue
        elif c == ")":
          parentheses -= 1
          if parentheses == -1:
            err.append({}) # TODO - mismatch in ( and ) count
            bad_tag = True
            break
        elif c == ";" and parentheses == 0:
          tmp_str = tmp_str.strip()
          if len(tmp_str) == 0:
            err.append({}) # TODO - no value after @
            bad_tag = True
            break
          conditions.append(tmp_str)
          tmp_str = ""
        else:
          tmp_str += c
      
      if parentheses == 0 and not bad_tag:
        # Last condition wouldn't be added in the loop
        tmp_str = tmp_str.strip()
        if len(tmp_str) == 0:
          err.append({}) # TODO - no value after @
          continue
        conditions.append(tmp_str)
      else:
        err.append({}) # TODO - mismatch in ( and ) count
        continue
      
      # Check the position of AND is ok
      if not bad_tag:
        for condition in conditions:
          tmp_cond = " " + condition + " "
          tmp_ANDsplitted = tmp_cond.upper().split(" AND ")
          for splittedANDpart in tmp_ANDsplitted:
            if len(splittedANDpart.strip()) == 0:
              err.append({}) # TODO - AND without condition before or after
              bad_tag = True
              break

          if not bad_tag and tmp_cond.count(" AND ") != tmp_cond.upper().count(" AND "):
            err.append({}) # TODO - recommendation: use uppercase "AND". Not an error though

      if bad_tag:
        continue
      
      ## TODO continue: find and validate years
      
      
      
  
###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = ConditionalRestrictions(None)
        a.init(None)
        
        # TODO write tests
