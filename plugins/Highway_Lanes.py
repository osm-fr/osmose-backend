#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012-2015                                 ##
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

class Highway_Lanes(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[31601] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad lanes value") }
        self.errors[31603] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Conflict between usage of *:lanes or *:lanes:(forward|backward|both_ways)") }
        self.errors[31604] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Conflict between lanes number") }
        self.errors[31605] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Invalid usage of *:lanes:(backward|both_ways) on oneway highway") }
        self.errors[31606] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Unknown turn lanes value") }
        self.errors[31607] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad turn lanes order") }
        self.errors[31608] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Conflict between lanes number of same sufix ('', forward, backward or both_ways)") }
        self.errors[31609] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad access lanes value, should not be an integer but a restriction") }
        self.errors[31600] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Turn lanes merge_to_* need an aside lane on good side") }

    def way(self, data, tags, nds):
        if not "highway" in tags:
            return

        lanes = False
        for tag in tags:
            if "lanes" in tag:
                lanes = True
                break

        if not lanes:
          return

        tags_lanes = {}
        for tag in tags:
            if "lanes" in tag and not "source" in tag and not "FIXME" in tag:
                tags_lanes[tag] = tags[tag]

        err = []

        # Check trun lanes values
        tl = "turn:lanes" in tags_lanes
        tlf = "turn:lanes:forward" in tags_lanes
        tlb = "turn:lanes:backward" in tags_lanes
        tl2 = "turn:lanes:both_ways" in tags_lanes
        if tl or tlf or tlb or tl2:
            for tl in ["turn:lanes", "turn:lanes:forward", "turn:lanes:backward", "turn:lanes:both_ways"]:
                if tl in tags_lanes:
                    ttt = tags_lanes[tl].split("|")
                    unknown = False
                    i = 0
                    for tt in ttt:
                        for t in tt.split(";"):
                            if t not in ["left", "slight_left", "sharp_left", "through", "right", "slight_right", "sharp_right", "reverse", "merge_to_left", "merge_to_right", "none", ""]:
                                unknown = True
                                err.append((31606, 1, T_("Unknown turn lanes value \"%s\"", t)))
                            if (t == "merge_to_left" and i == 0) or (t == "merge_to_right" and i == len(ttt) - 1):
                                err.append((31600, 1, {}))
                        i += 1
                    if not unknown:
                        # merge_to_left is a on the right and vice versa
                        t = tags_lanes[tl] \
                            .replace("left", "l").replace("slight_left", "l").replace("sharp_left", "l") \
                            .replace("through", " ") \
                            .replace("right", "r").replace("slight_right", "r").replace("sharp_right", "r") \
                            .replace("reverse", "U") \
                            .replace("merge_to_left", "r").replace("merge_to_right", "l") \
                            .replace("none", " ").replace(";", "").split("|")
                        t = ''.join(map(lambda e: " " if len(e) == 0 or e[0] != e[-1] else e[0], map(sorted, t)))
                        t = t.replace('U', '') # Ignore reverse
                        last_left = self.rindex_(t, "l")
                        first_space = self.index_(t, " ")
                        last_space = self.rindex_(t, " ")
                        first_right = self.index_(t, "r")
                        # Check right is on the right and left is on the left...
                        if not(
                            (last_left == None or first_space == None or last_left < first_space) and
                            (first_space == None or last_space == None or first_space <= last_space) and
                            (last_space == None or first_right == None or last_space < first_right) and
                            (last_left == None or first_right == None or last_left < first_right)):
                            err.append((31607, 1, {}))

        # Check acces lanes values
        for access in ['hgv', 'bus', 'access', 'bicycle', 'psv', 'taxi', 'vehicle', 'motor_vehicle', 'hov', 'motorcycle', 'goods']:
            base = access+':lanes'
            for tag in tags_lanes:
                if tag.startswith(base):
                    try:
                        int(tags_lanes[tag])
                        err.append((31609, 1, {'en': '%s=%s' % (tag, tags_lanes[tag]) }))
                    except ValueError:
                        # Ok, should not be an integer
                        pass

        stars = []
        for tag in tags_lanes:
            if ":lanes" in tag:
                star = tag.split(':')[0]
                if star not in ('source', 'proposed', 'construction', 'note'):
                    stars.append(star)
        stars = list(set(stars))

        for star in stars:
            l = star + '' in tags_lanes
            lf = star + ':forward' in tags_lanes
            lb = star + ':backward' in tags_lanes
            l2 = star + ':both_ways' in tags_lanes
            if l and (lf or lb or l2):
                err.append((31603, 0, {"en": star + ":*"}))

        if err != []:
            return err

        number = {'lanes': {}}
        for tag in tags_lanes:
            if tag == 'lanes' or tag.startswith('lanes:'):
                try:
                    n = int(tags_lanes[tag])
                    parts = tag.split(':')
                    direction = ''
                    if len(parts) > 1:
                        if parts[-1] in ['forward', 'backward', 'both_ways']:
                            direction = ':'+parts[-1]
                    if number['lanes'].get(direction) == None:
                        number['lanes'][direction] = 0
                    number['lanes'][direction] += n
                except ValueError:
                    err.append((31601, 0, {"en": "lanes=%s is not an integer" % (tags_lanes[tag],) }))

        for star in stars:
            number[star] = {}
            for direction in ['', ':forward', ':backward', ':both_ways']:
                o = tags_lanes.get(star+':lanes'+direction)
                if o:
                    number[star][direction] = len(o.split('|'))

        n_lanes = {}
        for direction in ['', ':forward', ':backward', ':both_ways']:
            tag = None
            for star in number.keys():
                if n_lanes.get(direction) != None and number[star].get(direction) != None and number[star][direction] != n_lanes[direction]:
                    err.append((31608, 0, {"en": "(lanes(%s)=%s) != (lanes(%s)=%s)" % (star+":*"+direction, number[star][direction], tag, n_lanes[direction]) }))
                elif n_lanes.get(direction) == None and number[star].get(direction) != None:
                    n_lanes[direction] = number[star][direction]
                    tag = star+":lanes"+direction

        if err != []:
            return err

        if tags["highway"] in ['motorway', 'trunk']:
            oneway = "oneway" not in tags or tags["oneway"] not in ["no", "false"]
        else:
            oneway = "oneway" in tags and tags["oneway"] not in ["no", "false"]

        if oneway:
            for tag in tags:
                if tag.startswith('oneway:') and tags[tag] in ["no", "false"]:
                    # Oneway for mainstream traffic, but not for an other one, so we are not really on a oneway
                    oneway = False

        if tags.get('junction') == 'roundabout':
            oneway = True

        nl = n_lanes.get('')
        nlf = n_lanes.get(':forward')
        nlb = n_lanes.get(':backward')
        nl2 = n_lanes.get(':both_ways')

        if oneway:
            if nl != None and nlf != None and nl != nlf:
                err.append((31604, 0, {"en": "on oneway, (lanes=%s) != (lanes:forward=%s)" % (nl, nlf) }))
            if nlb != None or nl2 != None:
                err.append((31605, 0, {}))
        else:
            if nl != None and nlf != None and nlb != None and nl != nlf + nlb + (nl2 or 0):
                err.append((31604, 0, {"en": "on two way, (lanes=%s) != (lanes:forward=%s) + (lanes:backward=%s) + (lanes:both_ways=%s)" % (nl, nlf, nlb, nl2) }))
            if nl != None and nlf != None and nl <= nlf:
                err.append((31604, 0, {"en": "on two way, (lanes=%s) <= (lanes:forward=%s)" % (nl, nlf) }))
            if nl != None and nlb != None and nl <= nlb:
                err.append((31604, 0, {"en": "on two way, (lanes=%s) <= (lanes:backward=%s)" % (nl, nlb) }))
            if nl != None and nl2 != None and nl < nl2:
                err.append((31604, 0, {"en": "on two way, (lanes=%s) < (lanes:both_ways=%s)" % (nl, nl2) }))

        if err != []:
            return err

    def index_(self, l, e):
        try:
            return l.index(e)
        except ValueError:
            return None

    def rindex_(self, l, e):
        try:
            return l.rindex(e)
        except ValueError:
            return None

###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Highway_Lanes(None)
        a.init(None)

        for t in [{"highway": "residential", "lanes": "2", "destination:lanes": "*", "destination:lanes:backward": "*"},
                  {"highway": "residential", "hgv:lanes": "2"},
                  {"highway": "residential", "lanes": "r"},
                  {"highway": "residential", "lanes:hgv": "r"},
                  {"highway": "another", "lanes": "1", "destination:lanes": "a|b"},
                  {"highway": "another", "lanes": "1", "destination:lanes:backward": "a", "oneway": "yes"},
                  {"highway": "another", "lanes": "1", "lanes:backward": "2", "destination:lanes:backward": "a"},
                  {"highway": "another", "lanes": "2", "lanes:forward": "2", "destination:lanes:forward": "a", "destination:lanes:backward": "b"},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left", "lanes": "1"},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left", "destination:lanes": "A|B"},
                  {"highway": "residential", "lanes": "2", "lanes:backward": "2"},
                  {"highway": "residential", "lanes": "3", "lanes:backward": "2", "lanes:forward": "2"},
                 ]:
            print(t)
            print(a.way(None, t, None))
            self.check_err(a.way(None, t, None), t)

        for t in [{"waterway": "river"},
                  {"highway": "residential"},
                  {"highway": "residential", "lanes": "1", "oneway": "yes"},
                  {"highway": "residential", "destination:lanes": "a;b"},
                  {"highway": "residential", "lanes": "2", "destination:lanes:forward": "*", "destination:lanes:backward": "*"},
                  {"highway": "residential", "lanes": "3", "lanes:backward": "2", "destination:lanes:forward": "*", "destination:lanes:backward": "*|*"},
                  {"highway": "motorway", "lanes": "2", "oneway": "yes"},
                  {"highway": "secondary", "lanes": "2", "proposed:lanes": "4"},
                  {"highway": "primary", "lanes": "4", "lanes:forward": "2", "lanes:backward": "2", "turn:lanes:forward": "left|none", "turn:lanes:backward": "none|none"},
                  {"highway": "secondary", "lanes": "2", "lanes:both_ways": "1", "turn:lanes:forward": "left"},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left"},
                  {"highway": "residential", "lanes": "4", "turn:lanes:forward": "none|none|merge_to_left", "turn:lanes:backward": ""},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left"},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left", "lanes": "3"},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left", "destination:lanes": "A|B|B"},
                  {"highway": "residential", "lanes": "3", "lanes:forward": "2", "lanes:psv:backward": "1", "oneway": "yes", "oneway:psv": "no"},
                  {"highway": "motorway", "lanes": "3", "lanes:backward": "2", "lanes:forward": "1", "oneway": "no"},
                  {"highway": "secondary", "lanes": "3", "lanes:both_ways": "1"},
                 ]:
            print(t)
            assert not a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left||right"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|left;right|right"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|left;right|merge_to_left"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|left;left|merge_to_left"},
                  {"highway": "residential", "oneway": "yes", "lanes": "2", "turn:lanes": "left|"},
                  {"highway": "residential", "oneway": "yes", "lanes": "2", "turn:lanes": "|right"},
                  {"highway": "another", "turn:lanes": "merge_to_right|none"},
                  {"highway": "another", "turn:lanes": "reverse|left|left;through||"},
                  {"highway": "another", "lanes": "3", "source:lanes": "usgs_imagery_2007;survey;image", "source_ref:lanes": "AM909_DSCS7435"},
                  {"highway": "another", "lanes": "1", "lanes:both_ways": "1"},
                 ]:
            print(t)
            assert not a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "residential", "oneway": "yes", "lanes": "2", "turn:lanes": "left|right|"},
                  {"highway": "residential", "oneway": "yes", "lanes": "2", "turn:lanes": "right|left"},
                  {"highway": "another", "turn:lanes": "merge_to_left"},
                  {"highway": "another", "turn:lanes": "merge_to_left|none"},
                  {"highway": "another", "turn:lanes": "none|merge_to_right"},
                 ]:
            print(t)
            assert a.way(None, t, None), a.way(None, t, None)
