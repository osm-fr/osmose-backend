#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Covid19(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[202004] = self.def_class(item = 4010, level = 2, tags = mapcss.list_('tag', 'fix:survey', 'deprecated'), title = mapcss.tr('This store was on an adapted schedule during the lockdown. Are these opening hours still in effect?'))

        self.re_3f390088 = re.compile(r'off|restricted')
        self.re_64916a2b = re.compile(r'same|off|open|restricted')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[takeaway:covid19=yes][takeaway!=yes][inside("FR")]
        if ('takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'takeaway:covid19') == mapcss._value_capture(capture_tags, 0, 'yes') and mapcss._tag_capture(capture_tags, 1, tags, 'takeaway') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a take-away service during the lockdown. Does it still offer take-away in usual times")
                # fixChangeKey:"takeaway:covid19=>takeaway"
                # -osmoseAssertMatchWithContext:list("node takeaway:covid19=yes takeaway=no","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store offered a take-away service during the lockdown. Does it still offer take-away in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['takeaway', mapcss.tag(tags, 'takeaway:covid19')]]),
                    '-': ([
                    'takeaway:covid19'])
                }})

        # *[delivery:covid19=yes][delivery!=yes][inside("FR")]
        if ('delivery:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'delivery:covid19') == mapcss._value_capture(capture_tags, 0, 'yes') and mapcss._tag_capture(capture_tags, 1, tags, 'delivery') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a delivery service during the lockdown. Does it still offer delivery in usual times")
                # fixChangeKey:"delivery:covid19=>delivery"
                # -osmoseAssertMatchWithContext:list("node delivery:covid19=yes delivery=no","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store offered a delivery service during the lockdown. Does it still offer delivery in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['delivery', mapcss.tag(tags, 'delivery:covid19')]]),
                    '-': ([
                    'delivery:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19=~/off|restricted/][inside("FR")]
        if ('opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3f390088), mapcss._tag_capture(capture_tags, 1, tags, 'opening_hours:covid19')) and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("The lockdown is over. Has this place reopened?")
                # fixRemove:"opening_hours:covid19"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('The lockdown is over. Has this place reopened?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'opening_hours:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19!~/same|off|open|restricted/][!opening_hours][inside("FR")]
        if ('opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_64916a2b, 'same|off|open|restricted'), mapcss._tag_capture(capture_tags, 1, tags, 'opening_hours:covid19')) and not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store was on an adapted schedule during the lockdown. Are these opening hours still in effect?")
                # fixChangeKey:"opening_hours:covid19=>opening_hours"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store was on an adapted schedule during the lockdown. Are these opening hours still in effect?'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours', mapcss.tag(tags, 'opening_hours:covid19')]]),
                    '-': ([
                    'opening_hours:covid19'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[takeaway:covid19=yes][takeaway!=yes][inside("FR")]
        if ('takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'takeaway:covid19') == mapcss._value_capture(capture_tags, 0, 'yes') and mapcss._tag_capture(capture_tags, 1, tags, 'takeaway') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a take-away service during the lockdown. Does it still offer take-away in usual times")
                # fixChangeKey:"takeaway:covid19=>takeaway"
                # -osmoseAssertNoMatchWithContext:list("way takeaway:covid19=no","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way takeaway:covid19=only","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way takeaway:covid19=yes takeaway=yes","inside=FR")
                # -osmoseAssertMatchWithContext:list("way takeaway:covid19=yes","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store offered a take-away service during the lockdown. Does it still offer take-away in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['takeaway', mapcss.tag(tags, 'takeaway:covid19')]]),
                    '-': ([
                    'takeaway:covid19'])
                }})

        # *[delivery:covid19=yes][delivery!=yes][inside("FR")]
        if ('delivery:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'delivery:covid19') == mapcss._value_capture(capture_tags, 0, 'yes') and mapcss._tag_capture(capture_tags, 1, tags, 'delivery') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a delivery service during the lockdown. Does it still offer delivery in usual times")
                # fixChangeKey:"delivery:covid19=>delivery"
                # -osmoseAssertNoMatchWithContext:list("way delivery:covid19=no","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way delivery:covid19=only","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way delivery:covid19=yes delivery=yes","inside=FR")
                # -osmoseAssertMatchWithContext:list("way delivery:covid19=yes","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store offered a delivery service during the lockdown. Does it still offer delivery in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['delivery', mapcss.tag(tags, 'delivery:covid19')]]),
                    '-': ([
                    'delivery:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19=~/off|restricted/][inside("FR")]
        if ('opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3f390088), mapcss._tag_capture(capture_tags, 1, tags, 'opening_hours:covid19')) and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("The lockdown is over. Has this place reopened?")
                # fixRemove:"opening_hours:covid19"
                # -osmoseAssertNoMatchWithContext:list("way opening_hours:covid19='Mo-Su 09:00-20:00' opening_hours='Mo-Su 09:00-20:00'","inside=FR")
                # -osmoseAssertMatchWithContext:list("way opening_hours:covid19=restricted","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way opening_hours:covid19=same","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('The lockdown is over. Has this place reopened?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'opening_hours:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19!~/same|off|open|restricted/][!opening_hours][inside("FR")]
        if ('opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_64916a2b, 'same|off|open|restricted'), mapcss._tag_capture(capture_tags, 1, tags, 'opening_hours:covid19')) and not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store was on an adapted schedule during the lockdown. Are these opening hours still in effect?")
                # fixChangeKey:"opening_hours:covid19=>opening_hours"
                # -osmoseAssertNoMatchWithContext:list("way opening_hours:covid19='Mo-Su 09:00-20:00' opening_hours='Mo-Su 09:00-20:00'","inside=FR")
                # -osmoseAssertMatchWithContext:list("way opening_hours:covid19='Mo-Su 09:00-20:00'","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store was on an adapted schedule during the lockdown. Are these opening hours still in effect?'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours', mapcss.tag(tags, 'opening_hours:covid19')]]),
                    '-': ([
                    'opening_hours:covid19'])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[takeaway:covid19=yes][takeaway!=yes][inside("FR")]
        if ('takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'takeaway:covid19') == mapcss._value_capture(capture_tags, 0, 'yes') and mapcss._tag_capture(capture_tags, 1, tags, 'takeaway') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a take-away service during the lockdown. Does it still offer take-away in usual times")
                # fixChangeKey:"takeaway:covid19=>takeaway"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store offered a take-away service during the lockdown. Does it still offer take-away in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['takeaway', mapcss.tag(tags, 'takeaway:covid19')]]),
                    '-': ([
                    'takeaway:covid19'])
                }})

        # *[delivery:covid19=yes][delivery!=yes][inside("FR")]
        if ('delivery:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'delivery:covid19') == mapcss._value_capture(capture_tags, 0, 'yes') and mapcss._tag_capture(capture_tags, 1, tags, 'delivery') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a delivery service during the lockdown. Does it still offer delivery in usual times")
                # fixChangeKey:"delivery:covid19=>delivery"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store offered a delivery service during the lockdown. Does it still offer delivery in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['delivery', mapcss.tag(tags, 'delivery:covid19')]]),
                    '-': ([
                    'delivery:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19=~/off|restricted/][inside("FR")]
        if ('opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3f390088), mapcss._tag_capture(capture_tags, 1, tags, 'opening_hours:covid19')) and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("The lockdown is over. Has this place reopened?")
                # fixRemove:"opening_hours:covid19"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('The lockdown is over. Has this place reopened?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'opening_hours:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19!~/same|off|open|restricted/][!opening_hours][inside("FR")]
        if ('opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'opening_hours:covid19') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_64916a2b, 'same|off|open|restricted'), mapcss._tag_capture(capture_tags, 1, tags, 'opening_hours:covid19')) and not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours') and mapcss.inside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store was on an adapted schedule during the lockdown. Are these opening hours still in effect?")
                # fixChangeKey:"opening_hours:covid19=>opening_hours"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr('This store was on an adapted schedule during the lockdown. Are these opening hours still in effect?'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours', mapcss.tag(tags, 'opening_hours:covid19')]]),
                    '-': ([
                    'opening_hours:covid19'])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Covid19(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'takeaway': 'no', 'takeaway:covid19': 'yes'}), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'delivery': 'no', 'delivery:covid19': 'yes'}), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'takeaway:covid19': 'no'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'takeaway:covid19': 'only'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'takeaway': 'yes', 'takeaway:covid19': 'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'takeaway:covid19': 'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'delivery:covid19': 'no'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'delivery:covid19': 'only'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'delivery': 'yes', 'delivery:covid19': 'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'delivery:covid19': 'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'opening_hours': 'Mo-Su 09:00-20:00', 'opening_hours:covid19': 'Mo-Su 09:00-20:00'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'opening_hours:covid19': 'restricted'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'opening_hours:covid19': 'same'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'opening_hours': 'Mo-Su 09:00-20:00', 'opening_hours:covid19': 'Mo-Su 09:00-20:00'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'opening_hours:covid19': 'Mo-Su 09:00-20:00'}, [0]), expected={'class': 202004, 'subclass': 0})
