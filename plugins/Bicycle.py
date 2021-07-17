#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Bicycle(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[20301] = self.def_class(item = 2030, level = 1, tags = mapcss.list_('tag', 'highway') + mapcss.list_('cycleway', 'fix:survey'), title = mapcss.tr('Opposite cycleway without oneway'))
        self.errors[20302] = self.def_class(item = 2030, level = 1, tags = mapcss.list_('tag', 'highway') + mapcss.list_('cycleway', 'fix:survey'), title = mapcss.tr('Opposite or opposite lane in the same way of the oneway'))
        self.errors[20805] = self.def_class(item = 2080, level = 3, tags = mapcss.list_('tag', 'highway') + mapcss.list_('footway', 'fix:chair'), title = mapcss.tr('{0} without {1}', 'footway=sidewalk', 'highway=footway|construction'))
        self.errors[30328] = self.def_class(item = 3032, level = 2, tags = mapcss.list_('tag', 'highway') + mapcss.list_('cycleway', 'fix:chair'), title = mapcss.tr('{0} with {1}', 'highway=cycleway', 'cycleway=track'))
        self.errors[30329] = self.def_class(item = 3032, level = 2, tags = mapcss.list_('tag', 'highway') + mapcss.list_('fix:chair'), title = mapcss.tr('{0} with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[40101] = self.def_class(item = 4010, level = 2, tags = mapcss.list_('tag', 'highway') + mapcss.list_('fix:chair'), title = mapcss.tr('{0} is preferred to {1}', 'psv', 'service=psv'))
        self.errors[40301] = self.def_class(item = 4030, level = 2, tags = mapcss.list_('tag', 'highway') + mapcss.list_('cycleway', 'fix:chair'), title = mapcss.tr('{0} with {1} and {2}', 'cycleway', 'cycleway:right', '{cycleway:left}'))

        self.re_1825c777 = re.compile(r'footway|construction')
        self.re_5b286a0d = re.compile(r'no|use_sidepath')
        self.re_6781a1fd = re.compile(r'no|none|separate')
        self.re_67b51e41 = re.compile(r'opposite|opposite_lane')


    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[cycleway][cycleway:right][cycleway:left]
        if ('cycleway' in keys and 'cycleway:left' in keys and 'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:right')) and (mapcss._tag_capture(capture_tags, 2, tags, 'cycleway:left')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:chair")
                # -osmoseItemClassLevel:"4030/40301/2"
                # throwWarning:tr("{0} with {1} and {2}","cycleway","cycleway:right","{cycleway:left}")
                # assertMatch:"way cycleway=a cycleway:right=b cycleway:left=c"
                err.append({'class': 40301, 'subclass': 0, 'text': mapcss.tr('{0} with {1} and {2}', 'cycleway', 'cycleway:right', '{cycleway:left}')})

        # way[footway=sidewalk][highway!~/footway|construction/]
        if ('footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'sidewalk')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1825c777, 'footway|construction'), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("footway","fix:chair")
                # -osmoseItemClassLevel:"2080/20805/3"
                # throwWarning:tr("{0} without {1}","footway=sidewalk","highway=footway|construction")
                # assertNoMatch:"way footway=sidewalk highway=construction construction=footway"
                # assertNoMatch:"way footway=sidewalk highway=footway"
                # assertMatch:"way footway=sidewalk highway=path"
                err.append({'class': 20805, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', 'footway=sidewalk', 'highway=footway|construction')})

        # way[highway=service][service=psv][psv!=yes]
        if ('highway' in keys and 'service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'service')) and (mapcss._tag_capture(capture_tags, 1, tags, 'service') == mapcss._value_capture(capture_tags, 1, 'psv')) and (mapcss._tag_capture(capture_tags, 2, tags, 'psv') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"4010/40101/2"
                # throwWarning:tr("{0} is preferred to {1}","psv","service=psv")
                # fixAdd:"psv=yes"
                # fixRemove:"service"
                # assertMatch:"way highway=service service=psv psv=no"
                # assertNoMatch:"way highway=service service=psv psv=yes"
                err.append({'class': 40101, 'subclass': 0, 'text': mapcss.tr('{0} is preferred to {1}', 'psv', 'service=psv'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['psv','yes']]),
                    '-': ([
                    'service'])
                }})

        # way[highway=cycleway][cycleway=track]
        if ('cycleway' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway') == mapcss._value_capture(capture_tags, 1, 'track')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:chair")
                # -osmoseItemClassLevel:"3032/30328/2"
                # throwWarning:tr("{0} with {1}","highway=cycleway","cycleway=track")
                # fixRemove:"cycleway"
                err.append({'class': 30328, 'subclass': 0, 'text': mapcss.tr('{0} with {1}', 'highway=cycleway', 'cycleway=track'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'cycleway'])
                }})

        # way[bicycle=~/no|use_sidepath/][cycleway][cycleway!~/no|none|separate/]
        # way[bicycle=~/no|use_sidepath/][cycleway:left][cycleway:left!~/no|none|separate/]
        # way[bicycle=~/no|use_sidepath/][cycleway:right][cycleway:right!~/no|none|separate/]
        if ('bicycle' in keys and 'cycleway' in keys) or ('bicycle' in keys and 'cycleway:left' in keys) or ('bicycle' in keys and 'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b286a0d), mapcss._tag_capture(capture_tags, 0, tags, 'bicycle'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6781a1fd, 'no|none|separate'), mapcss._tag_capture(capture_tags, 2, tags, 'cycleway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b286a0d), mapcss._tag_capture(capture_tags, 0, tags, 'bicycle'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:left')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6781a1fd, 'no|none|separate'), mapcss._tag_capture(capture_tags, 2, tags, 'cycleway:left'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b286a0d), mapcss._tag_capture(capture_tags, 0, tags, 'bicycle'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:right')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6781a1fd, 'no|none|separate'), mapcss._tag_capture(capture_tags, 2, tags, 'cycleway:right'))))
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
                err.append({'class': 30329, 'subclass': 0, 'text': mapcss.tr('{0} with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[cycleway=~/opposite|opposite_lane/][!oneway]
        # way[cycleway=~/opposite|opposite_lane/][oneway=no]
        if ('cycleway' in keys) or ('cycleway' in keys and 'oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, 'cycleway'))) and (not mapcss._tag_capture(capture_tags, 1, tags, 'oneway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, 'cycleway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'oneway') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:survey")
                # -osmoseItemClassLevel:"2030/20301/1"
                # throwError:tr("Opposite cycleway without oneway")
                # assertNoMatch:"way cycleway=lane oneway=yes"
                # assertNoMatch:"way cycleway=opposite oneway=yes"
                # assertMatch:"way cycleway=opposite"
                err.append({'class': 20301, 'subclass': 0, 'text': mapcss.tr('Opposite cycleway without oneway')})

        # way:righthandtraffic["cycleway:right"=~/opposite|opposite_lane/][oneway=yes]
        # way:righthandtraffic["cycleway:left"=~/opposite|opposite_lane/][oneway="-1"]
        # way!:righthandtraffic["cycleway:left"=~/opposite|opposite_lane/][oneway=yes]
        # way!:righthandtraffic["cycleway:right"=~/opposite|opposite_lane/][oneway="-1"]
        if ('cycleway:left' in keys and 'oneway' in keys) or ('cycleway:right' in keys and 'oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:right'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'oneway') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss.setting(self.father.config.options, 'driving_side') != 'left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'oneway') == mapcss._value_capture(capture_tags, 1, '-1')) and (mapcss.setting(self.father.config.options, 'driving_side') != 'left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'oneway') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss.setting(self.father.config.options, 'driving_side') == 'left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:right'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'oneway') == mapcss._value_capture(capture_tags, 1, '-1')) and (mapcss.setting(self.father.config.options, 'driving_side') == 'left'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("cycleway","fix:survey")
                # -osmoseItemClassLevel:"2030/20302/1"
                # throwError:tr("Opposite or opposite lane in the same way of the oneway")
                # assertMatch:"way cycleway:right=opposite oneway=yes"
                # assertNoMatch:"way cycleway=opposite oneway=yes"
                err.append({'class': 20302, 'subclass': 0, 'text': mapcss.tr('Opposite or opposite lane in the same way of the oneway')})

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

        self.check_err(n.way(data, {'cycleway': 'a', 'cycleway:left': 'c', 'cycleway:right': 'b'}, [0]), expected={'class': 40301, 'subclass': 0})
        self.check_not_err(n.way(data, {'construction': 'footway', 'footway': 'sidewalk', 'highway': 'construction'}, [0]), expected={'class': 20805, 'subclass': 0})
        self.check_not_err(n.way(data, {'footway': 'sidewalk', 'highway': 'footway'}, [0]), expected={'class': 20805, 'subclass': 0})
        self.check_err(n.way(data, {'footway': 'sidewalk', 'highway': 'path'}, [0]), expected={'class': 20805, 'subclass': 0})
        self.check_err(n.way(data, {'highway': 'service', 'psv': 'no', 'service': 'psv'}, [0]), expected={'class': 40101, 'subclass': 0})
        self.check_not_err(n.way(data, {'highway': 'service', 'psv': 'yes', 'service': 'psv'}, [0]), expected={'class': 40101, 'subclass': 0})
        self.check_not_err(n.way(data, {'bicycle': 'no', 'cycleway:right': 'no'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_err(n.way(data, {'bicycle': 'no', 'cycleway': 'track'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_err(n.way(data, {'bicycle': 'use_sidepath', 'cycleway:left': 'lane'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {'bicycle': 'use_sidepath', 'cycleway:left': 'none'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {'cycleway': 'separate', 'highway': 'cycleway'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {'bicycle': 'use_sidepath', 'highway': 'residential'}, [0]), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {'cycleway': 'lane', 'oneway': 'yes'}, [0]), expected={'class': 20301, 'subclass': 0})
        self.check_not_err(n.way(data, {'cycleway': 'opposite', 'oneway': 'yes'}, [0]), expected={'class': 20301, 'subclass': 0})
        self.check_err(n.way(data, {'cycleway': 'opposite'}, [0]), expected={'class': 20301, 'subclass': 0})
        self.check_err(n.way(data, {'cycleway:right': 'opposite', 'oneway': 'yes'}, [0]), expected={'class': 20302, 'subclass': 0})
        self.check_not_err(n.way(data, {'cycleway': 'opposite', 'oneway': 'yes'}, [0]), expected={'class': 20302, 'subclass': 0})
