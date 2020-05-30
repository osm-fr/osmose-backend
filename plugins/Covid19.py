#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Covid19(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[202004] = self.def_class(item = 4010, level = 2, tags = mapcss.list_(u'tag', u'fix:survey', u'deprecated'), title = mapcss.tr(u'This store was on an adapted schedule during the lockdown. Are these opening hours still in effect ?'))

        self.re_3f390088 = re.compile(r'off|restricted')
        self.re_64916a2b = re.compile(r'same|off|open|restricted')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[takeaway:covid19=yes][takeaway!=yes][inside("FR")]
        if (u'takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'takeaway:covid19') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'takeaway') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a take-away service during the lockdown. Does it still offer take-away in usual times")
                # fixChangeKey:"takeaway:covid19=>takeaway"
                # -osmoseAssertMatchWithContext:list("node takeaway:covid19=yes takeaway=no","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store offered a take-away service during the lockdown. Does it still offer take-away in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'takeaway', mapcss.tag(tags, u'takeaway:covid19')]]),
                    '-': ([
                    u'takeaway:covid19'])
                }})

        # *[delivery:covid19=yes][delivery!=yes][inside("FR")]
        if (u'delivery:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'delivery:covid19') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'delivery') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a delivery service during the lockdown. Does it still offer delivery in usual times")
                # fixChangeKey:"delivery:covid19=>delivery"
                # -osmoseAssertMatchWithContext:list("node delivery:covid19=yes delivery=no","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store offered a delivery service during the lockdown. Does it still offer delivery in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'delivery', mapcss.tag(tags, u'delivery:covid19')]]),
                    '-': ([
                    u'delivery:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19=~/off|restricted/][inside("FR")]
        if (u'opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'opening_hours:covid19') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3f390088), mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours:covid19')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("The lockdown is over. Has this place reopened ?")
                # fixRemove:"opening_hours:covid19"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'The lockdown is over. Has this place reopened ?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'opening_hours:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19!~/same|off|open|restricted/][!opening_hours][inside("FR")]
        if (u'opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'opening_hours:covid19') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_64916a2b, u'same|off|open|restricted'), mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours:covid19')) and not mapcss._tag_capture(capture_tags, 2, tags, u'opening_hours') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store was on an adapted schedule during the lockdown. Are these opening hours still in effect ?")
                # fixChangeKey:"opening_hours:covid19=>opening_hours"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store was on an adapted schedule during the lockdown. Are these opening hours still in effect ?'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'opening_hours', mapcss.tag(tags, u'opening_hours:covid19')]]),
                    '-': ([
                    u'opening_hours:covid19'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[takeaway:covid19=yes][takeaway!=yes][inside("FR")]
        if (u'takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'takeaway:covid19') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'takeaway') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a take-away service during the lockdown. Does it still offer take-away in usual times")
                # fixChangeKey:"takeaway:covid19=>takeaway"
                # -osmoseAssertNoMatchWithContext:list("way takeaway:covid19=no","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way takeaway:covid19=only","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way takeaway:covid19=yes takeaway=yes","inside=FR")
                # -osmoseAssertMatchWithContext:list("way takeaway:covid19=yes","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store offered a take-away service during the lockdown. Does it still offer take-away in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'takeaway', mapcss.tag(tags, u'takeaway:covid19')]]),
                    '-': ([
                    u'takeaway:covid19'])
                }})

        # *[delivery:covid19=yes][delivery!=yes][inside("FR")]
        if (u'delivery:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'delivery:covid19') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'delivery') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a delivery service during the lockdown. Does it still offer delivery in usual times")
                # fixChangeKey:"delivery:covid19=>delivery"
                # -osmoseAssertNoMatchWithContext:list("way delivery:covid19=no","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way delivery:covid19=only","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way delivery:covid19=yes delivery=yes","inside=FR")
                # -osmoseAssertMatchWithContext:list("way delivery:covid19=yes","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store offered a delivery service during the lockdown. Does it still offer delivery in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'delivery', mapcss.tag(tags, u'delivery:covid19')]]),
                    '-': ([
                    u'delivery:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19=~/off|restricted/][inside("FR")]
        if (u'opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'opening_hours:covid19') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3f390088), mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours:covid19')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("The lockdown is over. Has this place reopened ?")
                # fixRemove:"opening_hours:covid19"
                # -osmoseAssertNoMatchWithContext:list("way opening_hours:covid19='Mo-Su 09:00-20:00' opening_hours='Mo-Su 09:00-20:00'","inside=FR")
                # -osmoseAssertMatchWithContext:list("way opening_hours:covid19=restricted","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way opening_hours:covid19=same","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'The lockdown is over. Has this place reopened ?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'opening_hours:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19!~/same|off|open|restricted/][!opening_hours][inside("FR")]
        if (u'opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'opening_hours:covid19') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_64916a2b, u'same|off|open|restricted'), mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours:covid19')) and not mapcss._tag_capture(capture_tags, 2, tags, u'opening_hours') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store was on an adapted schedule during the lockdown. Are these opening hours still in effect ?")
                # fixChangeKey:"opening_hours:covid19=>opening_hours"
                # -osmoseAssertNoMatchWithContext:list("way opening_hours:covid19='Mo-Su 09:00-20:00' opening_hours='Mo-Su 09:00-20:00'","inside=FR")
                # -osmoseAssertMatchWithContext:list("way opening_hours:covid19='Mo-Su 09:00-20:00'","inside=FR")
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store was on an adapted schedule during the lockdown. Are these opening hours still in effect ?'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'opening_hours', mapcss.tag(tags, u'opening_hours:covid19')]]),
                    '-': ([
                    u'opening_hours:covid19'])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[takeaway:covid19=yes][takeaway!=yes][inside("FR")]
        if (u'takeaway:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'takeaway:covid19') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'takeaway') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a take-away service during the lockdown. Does it still offer take-away in usual times")
                # fixChangeKey:"takeaway:covid19=>takeaway"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store offered a take-away service during the lockdown. Does it still offer take-away in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'takeaway', mapcss.tag(tags, u'takeaway:covid19')]]),
                    '-': ([
                    u'takeaway:covid19'])
                }})

        # *[delivery:covid19=yes][delivery!=yes][inside("FR")]
        if (u'delivery:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'delivery:covid19') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'delivery') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store offered a delivery service during the lockdown. Does it still offer delivery in usual times")
                # fixChangeKey:"delivery:covid19=>delivery"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store offered a delivery service during the lockdown. Does it still offer delivery in usual times'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'delivery', mapcss.tag(tags, u'delivery:covid19')]]),
                    '-': ([
                    u'delivery:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19=~/off|restricted/][inside("FR")]
        if (u'opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'opening_hours:covid19') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3f390088), mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours:covid19')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("The lockdown is over. Has this place reopened ?")
                # fixRemove:"opening_hours:covid19"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'The lockdown is over. Has this place reopened ?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'opening_hours:covid19'])
                }})

        # *[opening_hours:covid19][opening_hours:covid19!~/same|off|open|restricted/][!opening_hours][inside("FR")]
        if (u'opening_hours:covid19' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'opening_hours:covid19') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_64916a2b, u'same|off|open|restricted'), mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours:covid19')) and not mapcss._tag_capture(capture_tags, 2, tags, u'opening_hours') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4010/202004/2"
                # throwWarning:tr("This store was on an adapted schedule during the lockdown. Are these opening hours still in effect ?")
                # fixChangeKey:"opening_hours:covid19=>opening_hours"
                err.append({'class': 202004, 'subclass': 0, 'text': mapcss.tr(u'This store was on an adapted schedule during the lockdown. Are these opening hours still in effect ?'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'opening_hours', mapcss.tag(tags, u'opening_hours:covid19')]]),
                    '-': ([
                    u'opening_hours:covid19'])
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
            self.check_err(n.node(data, {u'takeaway': u'no', u'takeaway:covid19': u'yes'}), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {u'delivery': u'no', u'delivery:covid19': u'yes'}), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'takeaway:covid19': u'no'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'takeaway:covid19': u'only'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'takeaway': u'yes', u'takeaway:covid19': u'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {u'takeaway:covid19': u'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'delivery:covid19': u'no'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'delivery:covid19': u'only'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'delivery': u'yes', u'delivery:covid19': u'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {u'delivery:covid19': u'yes'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'opening_hours': u'Mo-Su 09:00-20:00', u'opening_hours:covid19': u'Mo-Su 09:00-20:00'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {u'opening_hours:covid19': u'restricted'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'opening_hours:covid19': u'same'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'opening_hours': u'Mo-Su 09:00-20:00', u'opening_hours:covid19': u'Mo-Su 09:00-20:00'}, [0]), expected={'class': 202004, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {u'opening_hours:covid19': u'Mo-Su 09:00-20:00'}, [0]), expected={'class': 202004, 'subclass': 0})
