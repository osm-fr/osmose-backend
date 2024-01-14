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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from modules.py3 import ilen
from modules.Stablehash import stablehash64

class Highway_Lanes(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[31601] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Bad lanes value'),
            detail = T_(
'''Non-numeric value, `lanes=*` must have an integer value.'''))
        self.errors[31603] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Conflict between usage of *:lanes or *:lanes:(forward|backward|both_ways)'),
            detail = T_(
'''You can not simultaneously set a tag and the variants with
`forward`, `backward` or `both_ways` suffixes.'''))
        self.errors[31604] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Conflict between lanes number'))
        self.errors[31605] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Invalid usage of *:lanes:(backward|both_ways) on oneway highway'),
            detail = T_(
'''You can not set opposite lanes data on a one way.'''))
        self.errors[31606] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Unknown turn lanes value'),
            detail = T_(
'''[Valid values](https://wiki.openstreetmap.org/wiki/Key:turn#Values)'''))
        self.errors[31607] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Bad turn lanes order'),
            detail = T_(
'''Right must be on the right and left on the left.'''))
        self.errors[31608] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Conflict between lanes number of same suffix ("", forward, backward or both_ways)'),
            detail = T_(
'''The number of lanes defined by many lane tags are not the same for a
given direction.'''))
        self.errors[31609] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Bad access lanes value, should not be an integer but a restriction'),
            detail = T_(
'''`psv:lanes=*` is an access restriction tag, while `lanes:psv=*` is
the number of lanes.'''))
        self.errors[31600] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Turn lanes merge_to_* need an aside lane on good side'),
            detail = T_(
'''The `merge_to_right` or `merge_to_left` lane must be on the same way
as the destination lane and the `merge_to_right` must be on the *left
side* and `the merge_to_left` on the *right side*.'''))
        self.errors[316011] = self.def_class(item = 3160, level = 3, tags = ['highway', 'fix:chair'],
            title = T_('Merge lane and other turn lane in a single lane'),
            detail = T_(
'''It is unlikely that merge_to_* and another turn lane value are indicated on a single lane.'''))
        self.errors[316012] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Indicated turn lane together with `none`'),
            detail = T_(
'''A `none` (or empty value) turn lane cannot be combined with other types of turn lanes within the same lane.'''))
        self.errors[316013] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Unknown change lanes value'),
            detail = T_(
'''[Valid values](https://wiki.openstreetmap.org/wiki/Key:change#How_to_map)'''))
        self.errors[316014] = self.def_class(item = 3160, level = 2, tags = ['highway', 'fix:chair'],
            title = T_('Lane changing value only_* need an aside lane on the good side'),
            detail = T_(
'''The `only_right` or `only_left` lane must be on the same way as the
lane to which the traffic can change and must be on the left (for `only_right`)
or right (for `only_left`) side of the lane to which changing is possible.'''),
            resource = "https://wiki.openstreetmap.org/wiki/Key:change")

        self.knownTurnLaneValues = ["left", "slight_left", "sharp_left", "through", "right", "slight_right", "sharp_right", "reverse", "merge_to_left", "merge_to_right", "none", ""]
        self.knownChangeLaneValues = ["yes", "no", "not_right", "not_left", "only_right", "only_left", ""]

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

        # Check turn lanes values
        tl = "turn:lanes" in tags_lanes
        tlf = "turn:lanes:forward" in tags_lanes
        tlb = "turn:lanes:backward" in tags_lanes
        tl2 = "turn:lanes:both_ways" in tags_lanes
        if tl or tlf or tlb or tl2:
            for tl in ["turn:lanes", "turn:lanes:forward", "turn:lanes:backward", "turn:lanes:both_ways"]:
                if tl in tags_lanes:
                    ttt = tags_lanes[tl].split("|")
                    unknown_turn_lanes_value = False
                    bad_turn_lanes_value = False
                    i = 0
                    for tt in ttt:
                        settt = set(tt.split(";"))
                        for t in settt:
                            if t not in self.knownTurnLaneValues:
                                unknown_turn_lanes_value = True
                                err.append({"class": 31606, "subclass": 0 + stablehash64(tl + '|' + t + '|' + str(i)), "text": T_("Unknown turn lanes value \"{0}\"", t)})

                        if ("merge_to_left" in settt and i == 0) or ("merge_to_right" in settt and i == len(ttt) - 1):
                            # A lane must exist in the merging direction
                            err.append({"class": 31600, "subclass": 1 + stablehash64(tl + '|' + tt + '|' + str(i))})
                            bad_turn_lanes_value = True

                        elif (not unknown_turn_lanes_value and len(settt) > 1 and ("none" in settt or "" in settt)):
                            # A single turn lane containing both `none` and `something`
                            if (not ("none" in settt and "" in settt and len(settt) == 2)):
                                err.append({"class": 316012, "subclass": 3 + stablehash64(tl + '|' + tt + '|' + str(i)), "text": T_("Combined none and indicated turn lane: \"{0}\"", tt)})
                                bad_turn_lanes_value = True

                        elif (not unknown_turn_lanes_value and len(settt) > 1 and
                              ((len(settt) > 2 and ("merge_to_right" in settt or "merge_to_left" in settt)) or
                               ("merge_to_right" in settt and not "merge_to_left" in settt) or
                               ("merge_to_left" in settt and not "merge_to_right" in settt))):
                            # A combination of merge_to_* with a turn (other than another merge_to_*)
                            err.append({"class": 316011, "subclass": 2 + stablehash64(tl + '|' + tt + '|' + str(i)), "text": T_("Merge together with another turn lane: \"{0}\"", tt)})

                        i += 1
                    if not unknown_turn_lanes_value and not bad_turn_lanes_value:
                        # Sequence (left-to-right) should be sharp_left (1)|left (2)|slight_left (3)|through (4)|slight_right (5)|right (6)|sharp_right (7)
                        # Reverse (depends on driving direction) and merge_to_* (can be anywhere except
                        #  outer lane in merging direction; already handled by error 31600) are ignored
                        # None is a special case: considered as 'through' except when outer lane
                        throughvalue = "4"
                        t = tags_lanes[tl] \
                            .replace("reverse", "-") \
                            .replace("merge_to_right", "-").replace("merge_to_left", "-") \
                            .replace("none", "N") \
                            .replace("sharp_left", "1").replace("slight_left", "3").replace("left", "2") \
                            .replace("through", throughvalue) \
                            .replace("slight_right", "5").replace("sharp_right", "7").replace("right", "6") \
                            .replace(";", "").split("|")

                        # Empty equals a 'none', otherwise sort values within a single lane (as left;right equals right;left)
                        t = list(map(lambda e: "N" if len(e) == 0 else e[0] if len(e) == 1 else ''.join(sorted(e)), t))

                        # Find transitions between normal lanes and "special" lanes. Each can have its own turn lanes.
                        # Use the hash sign (#) as a temporary indicator of these positions, for splitting later.
                        for k in ["access", "vehicle", "motor_vehicle", "bus", "bicycle", "psv"]:
                            tag = tl.replace("turn", k, 1)
                            if tag in tags:
                                tagsplit = tags[tag].split("|")
                                changeindices = [i for i in range(1, len(tagsplit)) if tagsplit[i] != tagsplit[i-1] and (tagsplit[i] == "no" or tagsplit[i-1] == "no")]
                                for i in changeindices:
                                    if i < len(t) and not "#" in t[i]:
                                        t[i] = "#" + t[i]

                        # Replace ignored values; split by access condition sections of the way
                        t = ''.join(t).replace('-', '').split("#")

                        if len(t) == 1 and len(t[0]) > 1:
                            # No lane access restrictions were present.
                            # Ignore single none on the outside lanes: it could be a bus lane.
                            # (It is much less likely that there are traffic-crossing bus lanes in the middle of the road)
                            if t[0][0] == "N":
                                t[0] = t[0][1:]
                            if t[0][-1:] == "N":
                                t[0] = t[0][0:-1]

                        for k in range(len(t)):
                            tk = t[k].replace('N', throughvalue) # Treat remaining none as through

                            if tk != ''.join(sorted(tk)):
                                err.append({"class": 31607, "subclass": 1 + stablehash64(tl), "text": T_("Bad turn lanes order in \"{0}\"", tl)})
                                break

        # Check change:lanes values
        for tag_cl in ["change:lanes", "change:lanes:forward", "change:lanes:backward", "change:lanes:both_ways"]:
            if tag_cl in tags_lanes:
                changeLanesValues = tags_lanes[tag_cl].split("|")
                unknown_change_lanes_value = False
                for clv in changeLanesValues:
                    if clv not in self.knownChangeLaneValues:
                        err.append({"class": 316013, "subclass": 0 + stablehash64(tag_cl + '|' + clv), "text": T_("Unknown {0} value \"{1}\"", tag_cl, clv)})
                        unknown_change_lanes_value = True
                        break
                if not unknown_change_lanes_value:
                    if changeLanesValues[0] == "only_left" or changeLanesValues[-1] == "only_right":
                        err.append({"class": 316014, "subclass": 0 + stablehash64(tag_cl), "text": T_("Impossible lane change in tag \"{0}\"", tag_cl)})

        # Check access lanes values

        # Count for non fullwidth lanes
        non_fullwidth_lanes_number = {}
        for direction in ['', ':forward', ':backward', ':both_ways']:
            o = tags_lanes.get('bicycle:lanes'+direction)
            if o:
                non_fullwidth_lanes_number[direction] = ilen(filter(lambda i: i == 'designated', o.split('|')))

        # Verify *:lanes tags are not numerical
        for access in ['hgv', 'bus', 'access', 'bicycle', 'psv', 'taxi', 'vehicle', 'motor_vehicle', 'hov', 'motorcycle', 'goods']:
            base = access+':lanes'
            for tag in tags_lanes:
                if tag.startswith(base):
                    try:
                        int(tags_lanes[tag])
                        err.append({"class": 31609, "subclass": 1 + stablehash64(tag), "text": {'en': '{0}={1}'.format(tag, tags_lanes[tag]) }})
                    except ValueError:
                        # Ok, should not be an integer
                        pass

        # Get all * in *:lanes suffixed keys
        stars = set(map(lambda tag: tag.split(":lanes")[0], filter(lambda tag: ":lanes" in tag and tag.split(":")[0] not in ('source', 'proposed', 'construction', 'note'), tags_lanes)))

        # Verify *:lanes doesn't co-exist with *:lanes:[direction]
        for star in stars:
            if star + ':lanes' in tags_lanes:
                for direction in [':forward', ':backward', ':both_ways']:
                    if star + ':lanes' + direction in tags_lanes:
                        err.append({"class": 31603, "subclass": stablehash64(star + "|" + direction), "text": {"en": "`{0}` + `{1}`".format(star + ":lanes", star + ":lanes" + direction)}})

        if err != []:
            return err

        # 1. Collects the values of lanes and lanes:[direction] only
        # 2. Validates all lanes:* to be numerical
        number = {'lanes': {}}
        for tag in tags_lanes:
            if tag == 'lanes' or tag.startswith('lanes:'):
                try:
                    if tag.endswith(':conditional'):
                        n = int(tags_lanes[tag].split('@', 1)[0].rstrip())
                    else:
                        n = int(tags_lanes[tag])
                    if n < 0:
                        err.append({"class": 31601, "subclass": 1 + stablehash64(tag), "text": T_("{0}={1} is not a positive integer", tag, tags_lanes[tag])})
                    parts = tag.split(':')
                    if len(parts) == 1:
                        number['lanes'][''] = n
                    elif len(parts) == 2 and parts[1] in ['forward', 'backward', 'both_ways']:
                        number['lanes'][':'+parts[1]] = n
                except ValueError:
                    err.append({"class": 31601, "subclass": 0 + stablehash64(tag), "text": T_("{0}={1} is not a positive integer", tag, tags_lanes[tag])})

        # Count the number of lanes in *:lanes tags
        for star in stars:
            number[star] = {}
            for direction in ['', ':forward', ':backward', ':both_ways']:
                o = tags_lanes.get(star+':lanes'+direction)
                if o:
                    number[star][direction] = len(o.split('|'))

        # Check if the number of lanes matches within tags of the same direction
        n_lanes = {}
        for direction in ['', ':forward', ':backward', ':both_ways']:
            tag = None
            for star in sorted(number.keys()):
                non_fullwidth_lanes_number_star = ((non_fullwidth_lanes_number.get(direction) or 0) if star != 'lanes' else 0)
                non_fullwidth_lanes_number_tag = ((non_fullwidth_lanes_number.get(direction) or 0) if tag != 'lanes' + direction else 0)
                if n_lanes.get(direction) is not None and number[star].get(direction) is not None and \
                        (number[star][direction] - non_fullwidth_lanes_number_star > n_lanes[direction] or
                        n_lanes[direction] - non_fullwidth_lanes_number_tag > number[star][direction]):
                    err.append({"class": 31608, "subclass": 0 + stablehash64(direction + '|' + star), "text": {
                        "en": "(lanes({0})={1}) - (non fullwidth={2}) != (lanes({3})={4}) - (non fullwidth={5})".format(
                            star + ":lanes" + direction if star != "lanes" else star + direction,
                            number[star][direction],
                            non_fullwidth_lanes_number_star,
                            tag,
                            n_lanes[direction],
                            non_fullwidth_lanes_number_tag) }})
                elif n_lanes.get(direction) is None and number[star].get(direction) is not None:
                    # First loop, pick the star as tag and the number of lanes to compare to the others
                    n_lanes[direction] = number[star][direction]
                    tag = star + ":lanes" + direction if star != "lanes" else star + direction

        if err != []:
            return err

        if tags["highway"] == 'motorway':
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

        nfw_nl = non_fullwidth_lanes_number.get('') or 0
        nfw_nlf = non_fullwidth_lanes_number.get(':forward') or 0
        nfw_nlb = non_fullwidth_lanes_number.get(':backward') or 0
        nfw_nl2 = non_fullwidth_lanes_number.get(':both_ways') or 0

        if oneway:
            if nl is not None and nlf is not None and nl != nlf - nfw_nlf:
                err.append({"class": 31604, "subclass": 0, "text": T_("on oneway, (lanes={0}) != (lanes:forward={1}) - (non fullwidth forward={2})", nl, nlf, nfw_nlf)})
            elif nlb is not None or nl2 is not None:
                err.append({"class": 31605, "subclass": 0})
        else:
            if nl is not None and nlf is not None and nlb is not None and (nl < nlf + nlb + (nl2 or 0) - nfw_nl - nfw_nlf - nfw_nlb - nfw_nl2 or nl > nlf + nlb + (nl2 or 0)):
                err.append({"class": 31604, "subclass": 0, "text": T_("on two way, (lanes={0}) != (lanes:forward={1}) + (lanes:backward={2}) + (lanes:both_ways={3}) - (non fullwidth={4}) - (non fullwidth forward={5}) - (non fullwidth backward={6}) - (non fullwidth both_ways={7})", nl, nlf, nlb, nl2, nfw_nl, nfw_nlf, nfw_nlb, nfw_nl2)})
            elif nl is not None and nlf is not None and nl <= nlf - nfw_nlf:
                err.append({"class": 31604, "subclass": 0, "text": T_("on two way, (lanes={0}) <= (lanes:forward={1}) - (non fullwidth forward={2})", nl, nlf, nfw_nlf)})
            elif nl is not None and nlb is not None and nl <= nlb - nfw_nlb:
                err.append({"class": 31604, "subclass": 0, "text": T_("on two way, (lanes={0}) <= (lanes:backward={1}) - (non fullwidth backward={2})", nl, nlb, nfw_nlb)})
            elif nl is not None and nl2 is not None and nl < nl2 - nfw_nl2:
                err.append({"class": 31604, "subclass": 0, "text": T_("on two way, (lanes={0}) < (lanes:both_ways={1}) - (non fullwidth both_ways={2})", nl, nl2, nfw_nl2)})

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

        for t in [{"highway": "residential", "destination:lanes": "x|y", "destination:lanes:backward": "y"},
                  {"highway": "residential", "lanes": "2", "destination:lanes": "*"},
                  {"highway": "residential", "hgv:lanes": "2"},
                  {"highway": "residential", "lanes": "r"},
                  {"highway": "residential", "lanes:forward": "-1"},
                  {"highway": "residential", "lanes:hgv": "r"},
                  {"highway": "another", "lanes": "1", "destination:lanes": "a|b"},
                  {"highway": "another", "lanes": "1", "destination:lanes:backward": "a", "oneway": "yes"},
                  {"highway": "another", "lanes": "1", "lanes:backward": "2", "destination:lanes:backward": "a"},
                  {"highway": "another", "lanes": "2", "lanes:forward": "2", "destination:lanes:forward": "a", "destination:lanes:backward": "b"},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left", "lanes": "1"},
                  {"highway": "motorway", "turn:lanes": "none|none|merge_to_left", "destination:lanes": "A|B"},
                  {"highway": "residential", "lanes": "2", "lanes:backward": "2"},
                  {"highway": "residential", "lanes": "3", "lanes:backward": "2", "lanes:forward": "2"},
                  {"highway": "another", "oneway": "yes", "vehicle:lanes": "yes|yes|yes|no|no|no|no", "bicycle:lanes": "designated|designated", "turn:lanes": "||||"},
                  {"highway": "another", "oneway": "yes", "destination:lanes": "A|B", "destination:color:lanes": "A|B|C"},
                 ]:
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
                  {"highway": "secondary", "lanes": "3", "lanes:bus:conditional": "1 @ (Mo-Fr 07:00-19:00)", "bus:lanes:conditional": "||designated @ (Mo-Fr 07:00-19:00)"},
                  {"highway": "secondary", "lanes": "2", "change:lanes": "no|no|no|no", "bicycle:lanes": "|designated||designated", "cycleway": "lane"},
                  {"highway": "secondary", "lanes": "1", "width:lanes": "3|1.5|1.5", "access:lanes": "yes|no|no", "bicycle:lanes": "yes|designated|designated"},
                  {"highway": "tertiary", "lanes": "6", "lanes:forward": "4", "lanes:backward": "2", "bus:lanes:backward": "yes|designated", "bicycle:lanes:backward": "yes|designated", "cycleway": "opposite_share_busway"},
                  {"highway": "tertiary", "lanes": "3", "bus:lanes": "||designated", "bicycle:lanes": "no|designated|designated", "turn:lanes": "through|through|right"},
                  {"highway": "residential", "destination:lanes:both_ways": "x|y", "destination:lanes:backward": "y"},
                 ]:
            assert not a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left||right"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|left;right|right"},
                  {"highway": "residential", "oneway": "yes", "lanes": "4", "turn:lanes": "left|left;right|right|none"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|left;right|merge_to_left"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|left;left|merge_to_left"},
                  {"highway": "residential", "oneway": "yes", "lanes": "2", "turn:lanes": "left|"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|merge_to_left;merge_to_right|right"},
                  {"highway": "residential", "oneway": "yes", "lanes": "2", "turn:lanes": "|right"},
                  {"highway": "another", "turn:lanes": "left;reverse|left|left;through|through|right;sharp_right"},
                  {"highway": "another", "turn:lanes": "reverse|sharp_left|left|slight_left||through|none|slight_right|right|sharp_right|merge_to_left"},
                  {"highway": "another", "turn:lanes": "merge_to_right|none"},
                  {"highway": "another", "turn:lanes": "through|merge_to_right|through"},
                  {"highway": "another", "turn:lanes": "reverse|left|left;through||"},
                  {"highway": "another", "lanes:forward": "2", "lanes:backward": "1", "turn:lanes:forward": "reverse|reverse", "turn:lanes:backward": "reverse"},
                  {"highway": "another", "lanes": "2", "turn:lanes": "reverse|none", "bus:lanes": "|designated", "vehicle:lanes": "designated|no"},
                  {"highway": "another", "lanes": "3", "source:lanes": "usgs_imagery_2007;survey;image", "source_ref:lanes": "AM909_DSCS7435"},
                  {"highway": "another", "lanes": "1", "lanes:both_ways": "1"},
                  {"highway": "another", "oneway": "yes", "lanes": "3", "vehicle:lanes": "no|yes|yes|no", "bicycle:lanes": "no|no|no|designated", "bus:lanes": "designated|yes|yes|no", "turn:lanes": "|left;through|right|through;right"},
                  {"highway": "another", "vehicle:lanes:forward": "no|yes|yes|no", "bicycle:lanes:forward": "no|no|no|designated", "bus:lanes:forward": "designated|yes|yes|no", "turn:lanes:forward": "|left;through|right|through;right"},
                  {"highway": "another", "oneway": "yes", "lanes": "3", "vehicle:lanes": "yes|yes|yes|no|no", "bicycle:lanes": "no|no|no|designated|designated", "turn:lanes": "left|through|right|left|through;right"},
                  {"highway": "another", "oneway": "yes", "lanes": "3", "vehicle:lanes": "||no|", "bicycle:lanes": "no|no|designated|", "turn:lanes": "left|through|through;left|right"},
                 ]:
            assert not a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "residential", "oneway": "yes", "lanes": "4", "turn:lanes": "left|right||"},
                  {"highway": "residential", "oneway": "yes", "lanes": "3", "turn:lanes": "left|right|through"},
                  {"highway": "residential", "oneway": "yes", "lanes": "2", "turn:lanes": "right|left"},
                  {"highway": "another", "turn:lanes": "merge_to_left"},
                  {"highway": "another", "turn:lanes": "merge_to_left|none"},
                  {"highway": "another", "turn:lanes": "none|merge_to_right"},
                  {"highway": "another", "turn:lanes": "none;right"},
                  {"highway": "another", "turn:lanes": "merge_to_right;through|through"},
                  {"highway": "another", "turn:lanes": "slight_right|through|right"},
                  {"highway": "another", "turn:lanes": "right;through|through|right"},
                  {"highway": "another", "turn:lanes": "through|right;left|through"},
                  {"highway": "another", "turn:lanes": "left;right|left;right"},
                  {"highway": "another", "turn:lanes": "left|sharp_left|through"},
                  {"highway": "another", "oneway": "yes", "lanes": "3", "vehicle:lanes": "yes|yes|yes|no|no", "bicycle:lanes": "no|no|no|designated|designated", "turn:lanes": "left|through|left|left|through;right"},
                  {"highway": "another", "oneway": "yes", "lanes": "3", "vehicle:lanes": "yes|yes|yes|no|no", "bicycle:lanes": "no|no|no|designated|designated", "turn:lanes": "left|through|right|left;right|through"},
                 ]:
            assert a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "primary", "oneway": "yes", "lanes": "4", "change:lanes": "no|not_right|not_left|yes"},
                  {"highway": "primary", "oneway": "yes", "lanes": "3", "change:lanes": "only_right|yes|only_left"},
                  {"highway": "primary", "lanes": "4", "lanes:forward": "2", "change:lanes:forward": "not_left|yes", "lanes:backward": "2", "change:lanes:backward": "not_left|not_right"},
                  {"highway": "primary", "oneway": "yes", "lanes": "1", "change:lanes": "no"},
                 ]:
            assert not a.way(None, t, None), a.way(None, t, None)

        for t in [{"highway": "primary", "oneway": "yes", "lanes": "2", "change:lanes": "not|yes"},
                  {"highway": "primary", "oneway": "yes", "lanes": "2", "change:lanes": "not_left;not_right|no"},
                  {"highway": "primary", "oneway": "yes", "lanes": "2", "change:lanes": "only_left|yes"},
                  {"highway": "primary", "oneway": "yes", "lanes": "2", "change:lanes": "yes|only_right"},
                  {"highway": "primary", "oneway": "yes", "lanes": "1", "change:lanes": "only_right"},
                 ]:
            assert a.way(None, t, None), a.way(None, t, None)
