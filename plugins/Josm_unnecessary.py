#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_unnecessary(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9010001] = {'item': 9010, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'unnecessary tag')}
        self.errors[9010002] = {'item': 9010, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} makes no sense', u'{0.tag')}

        self.re_3ad9e1f5 = re.compile(ur'^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][vehicle!=no][access!=no][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if (u'bridge' in keys) or (u'building' in keys) or (u'elevation' in keys) or (u'access' in keys and u'highway' in keys) or (u'highway' in keys and u'motor_vehicle' in keys) or (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') != mapcss._value_capture(capture_tags, 1, u'no') and mapcss._tag_capture(capture_tags, 2, tags, u'access') != mapcss._value_capture(capture_tags, 2, u'no') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != mapcss._value_capture(capture_tags, 3, u'yes') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 1949087363, 'text': mapcss.tr(u'{0} is unnecessary', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[emergency=permissive]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag")
                # fixAdd:"emergency=yes"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', u'{0.tag'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys and u'payment:coins' in keys and u'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'payment:cash'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][vehicle!=no][access!=no][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if (u'bridge' in keys) or (u'building' in keys) or (u'elevation' in keys) or (u'access' in keys and u'highway' in keys) or (u'highway' in keys and u'motor_vehicle' in keys) or (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') != mapcss._value_capture(capture_tags, 1, u'no') and mapcss._tag_capture(capture_tags, 2, tags, u'access') != mapcss._value_capture(capture_tags, 2, u'no') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != mapcss._value_capture(capture_tags, 3, u'yes') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                # assertMatch:"way bridge=no"
                # assertMatch:"way highway=proposed access=no"
                # assertMatch:"way layer=0"
                err.append({'class': 9010001, 'subclass': 1949087363, 'text': mapcss.tr(u'{0} is unnecessary', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[emergency=permissive]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag")
                # fixAdd:"emergency=yes"
                # assertNoMatch:"way emergency=designated"
                # assertMatch:"way emergency=permissive"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', u'{0.tag'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys and u'payment:coins' in keys and u'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'payment:cash'])
                }})

        # way[waterway][oneway?]
        if (u'oneway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{1.key}","{0.key}")
                # fixRemove:"{1.key}"
                err.append({'class': 9010001, 'subclass': 877465780, 'text': mapcss.tr(u'{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # way[waterway][oneway=-1]
        if (u'oneway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, -1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}. The flow direction is defined by the way direction.","{1.key}","{0.key}")
                err.append({'class': 9010001, 'subclass': 1802985931, 'text': mapcss.tr(u'{0} is unnecessary for {1}. The flow direction is defined by the way direction.', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][vehicle!=no][access!=no][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if (u'bridge' in keys) or (u'building' in keys) or (u'elevation' in keys) or (u'access' in keys and u'highway' in keys) or (u'highway' in keys and u'motor_vehicle' in keys) or (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') != mapcss._value_capture(capture_tags, 1, u'no') and mapcss._tag_capture(capture_tags, 2, tags, u'access') != mapcss._value_capture(capture_tags, 2, u'no') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != mapcss._value_capture(capture_tags, 3, u'yes') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 1949087363, 'text': mapcss.tr(u'{0} is unnecessary', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[emergency=permissive]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag")
                # fixAdd:"emergency=yes"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', u'{0.tag'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys and u'payment:coins' in keys and u'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'payment:cash'])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_unnecessary(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {u'bridge': u'no'}, [0]), expected={'class': 9010001, 'subclass': 1949087363})
        self.check_err(n.way(data, {u'access': u'no', u'highway': u'proposed'}, [0]), expected={'class': 9010001, 'subclass': 1949087363})
        self.check_err(n.way(data, {u'layer': u'0'}, [0]), expected={'class': 9010001, 'subclass': 1949087363})
        self.check_not_err(n.way(data, {u'emergency': u'designated'}, [0]), expected={'class': 9010002, 'subclass': 325672362})
        self.check_err(n.way(data, {u'emergency': u'permissive'}, [0]), expected={'class': 9010002, 'subclass': 325672362})
