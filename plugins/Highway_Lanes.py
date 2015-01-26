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
        self.errors[31602] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Missing lanes tag or useless *:lanes") }
        self.errors[31603] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Conflict between *:lanes and *:lanes:*") }
        self.errors[31604] = { "item": 3160, "level": 2, "tag": ["highway", "fix:chair"], "desc": T_(u"Bad lanes usage") }

    lanes_default = {
        "unclassified": 2,
        "residential": 2,
        "tertiary": 2,
        "secondary": 2,
        "primary": 2,
        "service": 1,
        "track": 1,
        "path": 1,
        "motorway": 2,
        "motorway_link": 1,
        "trunk": 2,
        "trunk_link": 1,
    }

    lanes_default_oneway = {
        "unclassified": 1,
        "residential": 1,
        "tertiary": 1,
        "secondary": 1,
        "primary": 1,
        "service": 1,
        "track": 1,
        "path": 1,
        "motorway": 2,
        "motorway_link": 1,
        "trunk": 2,
    }

    def get_default(self, tags, tag, default, err):
        if tag in tags:
            try:
                return int(tags[tag])
            except ValueError:
                err.append((31601, 0, {"en": "%s=%s is not an integer" % (tag, tags[tag])}))
                return default
        else:
            return default

    def count_n_lanes(self, tags, tag, default):
        if tag in tags:
            return len(tags[tag].split("|"))
        else:
            return default

    def check_star_lanes(self, tags, star, highway, oneway, lanes, err):
        _lanes = "%s:lanes" % star
        _lanes_forward = "%s:lanes:forward" % star
        _lanes_backward = "%s:lanes:backward" %star

        if _lanes in tags and (_lanes_forward in tags or _lanes_backward in tags):
            err.append((31603, 0, {}))

        if _lanes in tags:
            n_lanes = self.count_n_lanes(tags, _lanes, lanes)

            if n_lanes != lanes:
                err.append((31604, 1, {"en": "(%s=%s) != lanes number (%s)" % (_lanes, n_lanes, lanes)}))

        elif _lanes_forward in tags or _lanes_backward in tags:
            if highway in self.lanes_default_oneway:
                nd = self.lanes_default_oneway[highway]
            else:
                nd = 1

            lanes_forward = self.get_default(tags, "lanes:forward", nd, err)
            n_lanes_forward = self.count_n_lanes(tags, _lanes_forward, lanes_forward)

            if oneway or (highway in ["motorway", "trunk"]):
                lanes_backward = self.get_default(tags, "lanes:backward", 0, err)
                n_lanes_backward = self.count_n_lanes(tags, _lanes_backward, 0)
            else:
                lanes_backward = self.get_default(tags, "lanes:backward", nd, err)
                n_lanes_backward = self.count_n_lanes(tags, _lanes_backward, lanes_backward)

            if n_lanes_forward + n_lanes_backward != lanes:
                err.append((31604, 2, {"en": "(%s+%s=%s) != (number=%s)" % (_lanes_forward, _lanes_backward, n_lanes_forward+n_lanes_backward, lanes)}))

            if lanes_forward + lanes_backward != lanes:
                err.append((31604, 3, {"en": "(lanes_forward+lanes_backward=%s) != (lanes=%s)" % (lanes_forward+lanes_backward, lanes)}))

            if n_lanes_forward != lanes_forward:
                err.append((31604, 4, {"en": "(%s=%s) != (lanes:forward=%s)" % (_lanes_forward, n_lanes_forward, lanes_forward)}))
            if n_lanes_backward != lanes_backward:
                err.append((31604, 5, {"en": "(%s=%s) != (lanes:backward=%s)" % (_lanes_backward, n_lanes_backward, lanes_backward)}))

    def way(self, data, tags, nds):
        if not "highway" in tags:
            return
        if not "lanes" in tags and not "destination:lanes" in tags and not "destination:lanes:forward" in tags and not "destination:lanes:backward" in tags:
            return

        err = []

        highway = tags["highway"]
        oneway = "oneway" in tags and tags["oneway"] not in ["no", "false"]

        if not "lanes" in tags:
            err.append((31602, 0, {}))


        if oneway:
            if highway in self.lanes_default_oneway:
                nd = self.lanes_default_oneway[highway]
            else:
                nd = 1
        else:
            if highway in self.lanes_default:
                nd = self.lanes_default[highway]
            else:
                nd = 1
        lanes = self.get_default(tags, "lanes", nd, err)

        stars = []
        for tag in tags:
            if ":lanes" in tag:
                stars.append(tag.split(':')[0])

        for star in stars:
            if star not in ('source', 'proposed', 'construction'):
                self.check_star_lanes(tags, star, highway, oneway, lanes, err)

        return err


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        a = Highway_Lanes(None)
        a.init(None)

        for t in [{"highway": "residential", "lanes":"2", "destination:lanes":"*", "destination:lanes:backward":"*"},
                  {"highway": "residential", "lanes":"r"},
                  {"highway": "residential", "destination:lanes":"a;b"},
                  {"highway": "another", "lanes": "1", "destination:lanes":"a|b"},
                  {"highway": "another", "lanes": "1", "destination:lanes:backward":"a", "oneway": "yes"},
                  {"highway": "another", "lanes": "1", "lanes:backward":"2", "destination:lanes:backward":"a"},
                  {"highway": "another", "lanes": "2", "lanes:forward":"2", "destination:lanes:forward":"a", "destination:lanes:backward": "b"},
                 ]:
            print t
            print a.way(None, t, None)
            self.check_err(a.way(None, t, None), t)

        t = {"highway": "residential", "lanes":"r"}
        r = a.way(None, t, None)
        self.check_err(r)
        self.assertEquals(r[0][0], 31601)
        for t in [{"waterway": "river"},
                  {"highway": "residential"},
                  {"highway": "residential", "lanes":"1", "oneway":"yes"},
                  {"highway": "residential", "lanes":"2", "destination:lanes:forward":"*", "destination:lanes:backward":"*"},
                  {"highway": "residential", "lanes":"3", "lanes:backward":"2", "destination:lanes:forward":"*", "destination:lanes:backward":"*|*"},
                  {"highway": "motorway", "lanes":"2", "oneway":"yes"},
                  {"highway": "secondary", "lanes":"2", "proposed:lanes":"4"},
                 ]:
            assert not a.way(None, t, None), t
