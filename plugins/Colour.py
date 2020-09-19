#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Colour(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[30911] = self.def_class(item = 3091, level = 2, tags = mapcss.list_('tag'), title = mapcss.tr('Colour code should start with \'#\' followed by 3 or 6 digits'))

        self.re_1b3f6ace = re.compile(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')
        self.re_30dca0d4 = re.compile(r'^#')
        self.re_7d65c79d = re.compile(r'^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building:colour][building:colour=~/^#/][building:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^#/][roof:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[colour][colour=~/^#/][colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^#/][ref:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if ('building:colour' in keys) or ('colour' in keys) or ('ref:colour' in keys) or ('roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'building:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'roof:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'roof:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'ref:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'ref:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:0/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                err.append({'class': 30911, 'subclass': 0, 'text': mapcss.tr('{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building:colour][building:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[colour][colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if ('building:colour' in keys) or ('colour' in keys) or ('ref:colour' in keys) or ('roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'roof:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'ref:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:1/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                # fixAdd:"{0.key}=#{0.value}"
                err.append({'class': 30911, 'subclass': 1, 'text': mapcss.tr('{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=#{0.value}')).split('=', 1)])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building:colour][building:colour=~/^#/][building:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^#/][roof:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[colour][colour=~/^#/][colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^#/][ref:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if ('building:colour' in keys) or ('colour' in keys) or ('ref:colour' in keys) or ('roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'building:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'roof:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'roof:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'ref:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'ref:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'ref:colour')))
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
                err.append({'class': 30911, 'subclass': 0, 'text': mapcss.tr('{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building:colour][building:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[colour][colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if ('building:colour' in keys) or ('colour' in keys) or ('ref:colour' in keys) or ('roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'roof:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'ref:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'ref:colour')))
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
                err.append({'class': 30911, 'subclass': 1, 'text': mapcss.tr('{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=#{0.value}')).split('=', 1)])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building:colour][building:colour=~/^#/][building:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^#/][roof:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[colour][colour=~/^#/][colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^#/][ref:colour!~/^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if ('building:colour' in keys) or ('colour' in keys) or ('ref:colour' in keys) or ('roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'building:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'roof:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'roof:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'ref:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_30dca0d4), mapcss._tag_capture(capture_tags, 1, tags, 'ref:colour')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1b3f6ace, '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'), mapcss._tag_capture(capture_tags, 2, tags, 'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:0/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                err.append({'class': 30911, 'subclass': 0, 'text': mapcss.tr('{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building:colour][building:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[roof:colour][roof:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[colour][colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        # *[ref:colour][ref:colour=~/^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/]
        if ('building:colour' in keys) or ('colour' in keys) or ('ref:colour' in keys) or ('roof:colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'building:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'roof:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'roof:colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'colour')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'ref:colour') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7d65c79d), mapcss._tag_capture(capture_tags, 1, tags, 'ref:colour')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Colour code should start with '#' followed by 3 or 6 digits")
                # -osmoseItemClassLevel:"3091/30911:1/2"
                # throwWarning:tr("{0} colour code should start with '#' followed by 3 or 6 digits","{0.tag}")
                # fixAdd:"{0.key}=#{0.value}"
                err.append({'class': 30911, 'subclass': 1, 'text': mapcss.tr('{0} colour code should start with \'#\' followed by 3 or 6 digits', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{0.key}=#{0.value}')).split('=', 1)])
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

        self.check_not_err(n.way(data, {'building:colour': '#123'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_err(n.way(data, {'building:colour': '#1234'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_not_err(n.way(data, {'building:colour': '#abcdef'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_err(n.way(data, {'building:colour': '#foobar9'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_err(n.way(data, {'building:colour': '#zzz'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_not_err(n.way(data, {'building:colour': '#8c6b57', 'roof:colour': '#484443'}, [0]), expected={'class': 30911, 'subclass': 0})
        self.check_not_err(n.way(data, {'building:colour': '#123'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_err(n.way(data, {'building:colour': '123'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_err(n.way(data, {'building:colour': 'abcdef'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_not_err(n.way(data, {'building:colour': 'red'}, [0]), expected={'class': 30911, 'subclass': 1})
        self.check_not_err(n.way(data, {'building:colour': '#8c6b57', 'roof:colour': '#484443'}, [0]), expected={'class': 30911, 'subclass': 1})
