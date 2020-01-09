#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Bicycle(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[20301] = {'item': 2030, 'level': 1, 'tag': mapcss.list_(u'tag', u'highway') + mapcss.list_(u'cycleway', u'fix:survey'), 'desc': mapcss.tr(u'Opposite cycleway without oneway')}
        self.errors[20302] = {'item': 2030, 'level': 1, 'tag': mapcss.list_(u'tag', u'highway') + mapcss.list_(u'cycleway', u'fix:survey'), 'desc': mapcss.tr(u'Opposite or opposite lane in the same way of the oneway')}
        self.errors[20805] = {'item': 2080, 'level': 3, 'tag': mapcss.list_(u'tag', u'highway') + mapcss.list_(u'footway', u'fix:chair'), 'desc': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'highway=footway|construction')}
        self.errors[30328] = {'item': 3032, 'level': 2, 'tag': mapcss.list_(u'tag', u'highway') + mapcss.list_(u'cycleway', u'fix:chair'), 'desc': mapcss.tr(u'{0} with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))}
        self.errors[30329] = {'item': 3032, 'level': 2, 'tag': mapcss.list_(u'tag', u'highway') + mapcss.list_(u'fix:chair'), 'desc': mapcss.tr(u'{0} with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))}
        self.errors[40101] = {'item': 4010, 'level': 2, 'tag': mapcss.list_(u'tag', u'highway') + mapcss.list_(u'fix:chair'), 'desc': mapcss.tr(u'{0} is preferred to {1}', mapcss._tag_uncapture(capture_tags, u'{2.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))}
        self.errors[40301] = {'item': 4030, 'level': 2, 'tag': mapcss.list_(u'tag', u'highway') + mapcss.list_(u'cycleway', u'fix:chair'), 'desc': mapcss.tr(u'{0} with {1} and {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))}

        self.re_1825c777 = re.compile(r'footway|construction')
        self.re_5b286a0d = re.compile(r'no|use_sidepath')
        self.re_6781a1fd = re.compile(r'no|none|separate')
        self.re_67b51e41 = re.compile(r'opposite|opposite_lane')


    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[cycleway][cycleway:right][cycleway:left]
        if (u'cycleway' in keys and u'cycleway:left' in keys and u'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:right') and mapcss._tag_capture(capture_tags, 2, tags, u'cycleway:left'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:chair")
                # -osmoseItemClassLevel:"4030/40301/2"
                # throwWarning:tr("{0} with {1} and {2}","{0.key}","{1.key}","{2.key}")
                # assertMatch:"way cycleway=a cycleway:right=b cycleway:left=c"
                err.append({'class': 40301, 'subclass': 0, 'text': mapcss.tr(u'{0} with {1} and {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # way[footway=sidewalk][highway!~/footway|construction/]
        if (u'footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'sidewalk') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1825c777, u'footway|construction'), mapcss._tag_capture(capture_tags, 1, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("footway","fix:chair")
                # -osmoseItemClassLevel:"2080/20805/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","highway=footway|construction")
                # assertNoMatch:"way footway=sidewalk highway=construction construction=footway"
                # assertNoMatch:"way footway=sidewalk highway=footway"
                # assertMatch:"way footway=sidewalk highway=path"
                err.append({'class': 20805, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'highway=footway|construction')})

        # way[highway=service][service=psv][psv!=yes]
        if (u'highway' in keys and u'service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'service') and mapcss._tag_capture(capture_tags, 1, tags, u'service') == mapcss._value_capture(capture_tags, 1, u'psv') and mapcss._tag_capture(capture_tags, 2, tags, u'psv') != mapcss._value_const_capture(capture_tags, 2, u'yes', u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"4010/40101/2"
                # throwWarning:tr("{0} is preferred to {1}","{2.tag}","{1.tag}")
                # fixAdd:"psv=yes"
                # fixRemove:"service"
                # assertMatch:"way highway=service service=psv psv=no"
                # assertNoMatch:"way highway=service service=psv psv=yes"
                err.append({'class': 40101, 'subclass': 0, 'text': mapcss.tr(u'{0} is preferred to {1}', mapcss._tag_uncapture(capture_tags, u'{2.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'psv',u'yes']]),
                    '-': ([
                    u'service'])
                }})

        # way[highway=cycleway][cycleway=track]
        if (u'cycleway' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway') == mapcss._value_capture(capture_tags, 1, u'track'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:chair")
                # -osmoseItemClassLevel:"3032/30328/2"
                # throwWarning:tr("{0} with {1}","{0.tag}","{1.tag}")
                # fixRemove:"cycleway"
                err.append({'class': 30328, 'subclass': 0, 'text': mapcss.tr(u'{0} with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'cycleway'])
                }})

        # way[bicycle=~/no|use_sidepath/][cycleway][cycleway!~/no|none|separate/]
        # way[bicycle=~/no|use_sidepath/][cycleway:left][cycleway:left!~/no|none|separate/]
        # way[bicycle=~/no|use_sidepath/][cycleway:right][cycleway:right!~/no|none|separate/]
        if (u'bicycle' in keys and u'cycleway' in keys) or (u'bicycle' in keys and u'cycleway:left' in keys) or (u'bicycle' in keys and u'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b286a0d), mapcss._tag_capture(capture_tags, 0, tags, u'bicycle')) and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6781a1fd, u'no|none|separate'), mapcss._tag_capture(capture_tags, 2, tags, u'cycleway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b286a0d), mapcss._tag_capture(capture_tags, 0, tags, u'bicycle')) and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:left') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6781a1fd, u'no|none|separate'), mapcss._tag_capture(capture_tags, 2, tags, u'cycleway:left')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b286a0d), mapcss._tag_capture(capture_tags, 0, tags, u'bicycle')) and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:right') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6781a1fd, u'no|none|separate'), mapcss._tag_capture(capture_tags, 2, tags, u'cycleway:right')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3032/30329/2"
                # throwWarning:tr("{0} with {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way bicycle=no cycleway:right=no"
                # assertMatch:"way bicycle=no cycleway=track"
                # assertMatch:"way bicycle=use_sidepath cycleway:left=lane"
                # assertNoMatch:"way bicycle=use_sidepath cycleway:left=none"
                # assertNoMatch:"way highway=cycleway cycleway=separate"
                # assertNoMatch:"way highway=residential bicycle=use_sidepath"
                err.append({'class': 30329, 'subclass': 0, 'text': mapcss.tr(u'{0} with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[cycleway=~/opposite|opposite_lane/][!oneway]
        # way[cycleway=~/opposite|opposite_lane/][oneway=no]
        if (u'cycleway' in keys) or (u'cycleway' in keys and u'oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway')) and not mapcss._tag_capture(capture_tags, 1, tags, u'oneway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:survey")
                # -osmoseItemClassLevel:"2030/20301/1"
                # throwError:tr("Opposite cycleway without oneway")
                # assertNoMatch:"way cycleway=lane oneway=yes"
                # assertNoMatch:"way cycleway=opposite oneway=yes"
                # assertMatch:"way cycleway=opposite"
                err.append({'class': 20301, 'subclass': 0, 'text': mapcss.tr(u'Opposite cycleway without oneway')})

        # way:righthandtraffic["cycleway:right"=~/opposite|opposite_lane/][oneway=yes]
        # way:righthandtraffic["cycleway:left"=~/opposite|opposite_lane/][oneway="-1"]
        # way!:righthandtraffic["cycleway:left"=~/opposite|opposite_lane/][oneway=yes]
        # way!:righthandtraffic["cycleway:right"=~/opposite|opposite_lane/][oneway="-1"]
        if (u'cycleway:left' in keys and u'oneway' in keys) or (u'cycleway:right' in keys and u'oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway:right')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss.setting(self.father.config.options, u'driving_side') != u'left')
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway:left')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'-1') and mapcss.setting(self.father.config.options, u'driving_side') != u'left')
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway:left')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss.setting(self.father.config.options, u'driving_side') == u'left')
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway:right')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'-1') and mapcss.setting(self.father.config.options, u'driving_side') == u'left')
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:survey")
                # -osmoseItemClassLevel:"2030/20302/1"
                # throwError:tr("Opposite or opposite lane in the same way of the oneway")
                # assertMatch:"way cycleway:right=opposite oneway=yes"
                # assertNoMatch:"way cycleway=opposite oneway=yes"
                err.append({'class': 20302, 'subclass': 0, 'text': mapcss.tr(u'Opposite or opposite lane in the same way of the oneway')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Bicycle(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {u'cycleway': u'a', u'cycleway:left': u'c', u'cycleway:right': u'b'}, [0]), expected={'class': 40301, 'subclass': 0})
        self.check_not_err(n.way(data, {u'construction': u'footway', u'footway': u'sidewalk', u'highway': u'construction'}, [0]), expected={'class': 20805, 'subclass': 0})
        self.check_not_err(n.way(data, {u'footway': u'sidewalk', u'highway': u'footway'}, [0]), expected={'class': 20805, 'subclass': 0})
        self.check_err(n.way(data, {u'footway': u'sidewalk', u'highway': u'path'}, [0]), expected={'class': 20805, 'subclass': 0})
        self.check_err(n.way(data, {u'highway': u'service', u'psv': u'no', u'service': u'psv'}, [0]), expected={'class': 40101, 'subclass': 0})
        self.check_not_err(n.way(data, {u'highway': u'service', u'psv': u'yes', u'service': u'psv'}, [0]), expected={'class': 40101, 'subclass': 0})
        self.check_not_err(n.way(data, {u'bicycle': u'no', u'cycleway:right': u'no'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_err(n.way(data, {u'bicycle': u'no', u'cycleway': u'track'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_err(n.way(data, {u'bicycle': u'use_sidepath', u'cycleway:left': u'lane'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {u'bicycle': u'use_sidepath', u'cycleway:left': u'none'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {u'cycleway': u'separate', u'highway': u'cycleway'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {u'bicycle': u'use_sidepath', u'highway': u'residential'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {u'cycleway': u'lane', u'oneway': u'yes'}, [0]), expected={'class': 20301, 'subclass': 0})
        self.check_not_err(n.way(data, {u'cycleway': u'opposite', u'oneway': u'yes'}, [0]), expected={'class': 20301, 'subclass': 0})
        self.check_err(n.way(data, {u'cycleway': u'opposite'}, [0]), expected={'class': 20301, 'subclass': 0})
        self.check_err(n.way(data, {u'cycleway:right': u'opposite', u'oneway': u'yes'}, [0]), expected={'class': 20302, 'subclass': 0})
        self.check_not_err(n.way(data, {u'cycleway': u'opposite', u'oneway': u'yes'}, [0]), expected={'class': 20302, 'subclass': 0})
