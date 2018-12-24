#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Colour(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[30911] = {'item': 3091, 'level': 2, 'tag': mapcss.list_(u'tag'), 'desc': mapcss.tr(u'Colour code should start with \'#\' followed by 3 or 6 digits')}

        self.re_1b3f6ace = re.compile(ur'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')
        self.re_30dca0d4 = re.compile(ur'^#')
        self.re_7d65c79d = re.compile(ur'^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building:colour][building:colour=~/^#/][building:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^#/][roof:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^#/][ref:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if (u'building:colour' in keys) or (u'ref:colour' in keys) or (u'roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'building:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'roof:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'ref:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:0/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                err.append({'class': 30911, 'subclass': 0, 'text': mapcss.tr(u'{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building:colour][building:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if (u'building:colour' in keys) or (u'ref:colour' in keys) or (u'roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:1/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                # fixAdd:"{0.key}=#{0.value}"
                err.append({'class': 30911, 'subclass': 1, 'text': mapcss.tr(u'{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=#{0.value}')).split('=', 1)])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building:colour][building:colour=~/^#/][building:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^#/][roof:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^#/][ref:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if (u'building:colour' in keys) or (u'ref:colour' in keys) or (u'roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'building:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'roof:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'ref:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:0/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                # assertNoMatch:"way building:colour=#123"
                # assertMatch:"way building:colour=#1234"
                # assertNoMatch:"way building:colour=#abcdef"
                # assertMatch:"way building:colour=#foobar9"
                # assertMatch:"way building:colour=#zzz"
                # assertNoMatch:"way roof:colour=#484443 building:colour=#8c6b57"
                err.append({'class': 30911, 'subclass': 0, 'text': mapcss.tr(u'{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building:colour][building:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if (u'building:colour' in keys) or (u'ref:colour' in keys) or (u'roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:1/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                # fixAdd:"{0.key}=#{0.value}"
                # assertNoMatch:"way building:colour=#123"
                # assertMatch:"way building:colour=123"
                # assertMatch:"way building:colour=abcdef"
                # assertNoMatch:"way building:colour=red"
                # assertNoMatch:"way roof:colour=#484443 building:colour=#8c6b57"
                err.append({'class': 30911, 'subclass': 1, 'text': mapcss.tr(u'{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=#{0.value}')).split('=', 1)])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building:colour][building:colour=~/^#/][building:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^#/][roof:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^#/][ref:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if (u'building:colour' in keys) or (u'ref:colour' in keys) or (u'roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'building:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'roof:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, u'ref:colour')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1b3f6ace), mapcss._tag_capture(capture_tags, 2, tags, u'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:0/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                err.append({'class': 30911, 'subclass': 0, 'text': mapcss.tr(u'{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building:colour][building:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if (u'building:colour' in keys) or (u'ref:colour' in keys) or (u'roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:colour') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, u'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:1/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                # fixAdd:"{0.key}=#{0.value}"
                err.append({'class': 30911, 'subclass': 1, 'text': mapcss.tr(u'{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=#{0.value}')).split('=', 1)])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Colour(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.way(data, {u'building:colour': u'#123'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_err(n.way(data, {u'building:colour': u'#1234'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_not_err(n.way(data, {u'building:colour': u'#abcdef'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_err(n.way(data, {u'building:colour': u'#foobar9'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_err(n.way(data, {u'building:colour': u'#zzz'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_not_err(n.way(data, {u'building:colour': u'#8c6b57', u'roof:colour': u'#484443'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_not_err(n.way(data, {u'building:colour': u'#123'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_err(n.way(data, {u'building:colour': u'123'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_err(n.way(data, {u'building:colour': u'abcdef'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_not_err(n.way(data, {u'building:colour': u'red'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_not_err(n.way(data, {u'building:colour': u'#8c6b57', u'roof:colour': u'#484443'}, [0]), expected={'class': 30911, 'subclass': 1})
