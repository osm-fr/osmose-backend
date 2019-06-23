#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_addresses(Plugin):


    not_for = ['CA']

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9000003] = {'item': 9000, 'level': 3, 'tag': ["tag", "addr"], 'desc': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9000004] = {'item': 9000, 'level': 3, 'tag': ["tag", "addr"], 'desc': mapcss.tr(u'{0} without number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}

        self.re_4983542e = re.compile(r'[0-9]')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_ok_housenumber = False

        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housename' in keys and u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                # assertMatch:"node addr:housename=1 addr:housenumber=1"
                # assertNoMatch:"node addr:housename=1 addr:housenumber=2"
                err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[addr:housenumber=bb][inside("BA")]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 0, u'bb') and mapcss.inside(self.father.config.options, u'BA'))
                except mapcss.RuleAbort: pass
            if match:
                # setok_housenumber
                set_ok_housenumber = True

        # *[addr:housenumber][addr:housenumber!~/[0-9]/]!.ok_housenumber
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_ok_housenumber and mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4983542e), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} without number","{0.key}")
                err.append({'class': 9000004, 'subclass': 1053226919, 'text': mapcss.tr(u'{0} without number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_ok_housenumber = False

        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housename' in keys and u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[addr:housenumber=bb][inside("BA")]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 0, u'bb') and mapcss.inside(self.father.config.options, u'BA'))
                except mapcss.RuleAbort: pass
            if match:
                # setok_housenumber
                set_ok_housenumber = True

        # *[addr:housenumber][addr:housenumber!~/[0-9]/]!.ok_housenumber
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_ok_housenumber and mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4983542e), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} without number","{0.key}")
                # assertNoMatch:"way addr:housenumber=0"
                # assertNoMatch:"way addr:housenumber=5/1"
                # assertNoMatch:"way addr:housenumber=5a"
                # assertMatch:"way addr:housenumber=?"
                # assertMatch:"way addr:housenumber=Palace of Westminster"
                # assertMatch:"way addr:housenumber=S/N"
                # assertMatch:"way addr:housenumber=unknown"
                err.append({'class': 9000004, 'subclass': 1053226919, 'text': mapcss.tr(u'{0} without number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_ok_housenumber = False

        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housename' in keys and u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[addr:housenumber=bb][inside("BA")]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 0, u'bb') and mapcss.inside(self.father.config.options, u'BA'))
                except mapcss.RuleAbort: pass
            if match:
                # setok_housenumber
                set_ok_housenumber = True

        # *[addr:housenumber][addr:housenumber!~/[0-9]/]!.ok_housenumber
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_ok_housenumber and mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4983542e), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} without number","{0.key}")
                err.append({'class': 9000004, 'subclass': 1053226919, 'text': mapcss.tr(u'{0} without number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_addresses(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'addr:housename': u'1', u'addr:housenumber': u'1'}), expected={'class': 9000003, 'subclass': 1820984183})
        self.check_not_err(n.node(data, {u'addr:housename': u'1', u'addr:housenumber': u'2'}), expected={'class': 9000003, 'subclass': 1820984183})
        self.check_not_err(n.way(data, {u'addr:housenumber': u'0'}, [0]), expected={'class': 9000004, 'subclass': 1053226919})
        self.check_not_err(n.way(data, {u'addr:housenumber': u'5/1'}, [0]), expected={'class': 9000004, 'subclass': 1053226919})
        self.check_not_err(n.way(data, {u'addr:housenumber': u'5a'}, [0]), expected={'class': 9000004, 'subclass': 1053226919})
        self.check_err(n.way(data, {u'addr:housenumber': u'?'}, [0]), expected={'class': 9000004, 'subclass': 1053226919})
        self.check_err(n.way(data, {u'addr:housenumber': u'Palace of Westminster'}, [0]), expected={'class': 9000004, 'subclass': 1053226919})
        self.check_err(n.way(data, {u'addr:housenumber': u'S/N'}, [0]), expected={'class': 9000004, 'subclass': 1053226919})
        self.check_err(n.way(data, {u'addr:housenumber': u'unknown'}, [0]), expected={'class': 9000004, 'subclass': 1053226919})
