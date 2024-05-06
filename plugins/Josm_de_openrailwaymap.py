#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_de_openrailwaymap(PluginMapCSS):

    MAPCSS_URL = 'https://www.openrailwaymap.org/validator/de-openrailwaymap.validator.mapcss'

    only_for = ['DE']


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9016002] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'hp signals only exist as semaphore or light signals'})
        self.errors[9016003] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'KVB hp signals only exist as light signals'})
        self.errors[9016004] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Vr repeated signals only exist as light signals'})
        self.errors[9016005] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Signal Gsp 2 was renamed to Wn 7 in 2008'})
        self.errors[9016006] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Ne 14 sign requires additional tag railway:signal:train_protection:type=block_marker'})
        self.errors[9016007] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'main and repeated distant signal usually are not at the same place'})
        self.errors[9016008] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'German distant signals can\'t be repeated and shortened at the same time'})
        self.errors[9016009] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'German Ks signals can\'t have main and distant signal at the same place, try a combined signal instead'})
        self.errors[9016010] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Sh semaphore signals cannot display Hp 0, but only Sh 0'})
        self.errors[9016011] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Sh light signals cannot display Sh 0, but only Hp 0'})
        self.errors[9016012] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Zs3v sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'})
        self.errors[9016013] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Zs3 sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'})
        self.errors[9016014] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Zs3v light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'})
        self.errors[9016015] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Zs3 light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'})
        self.errors[9016016] = self.def_class(item = 9016, level = 3, tags = ["tag", "railway"], title = {'en': 'It is unclear if Zs10 light signals have ever been placed, please double check.'})
        self.errors[9016017] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Tracks should not be named by their timetable number (KBS xy). Use a route relation with route=railway, instead.'})
        self.errors[9016018] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'ref=* should be a VzG number (without "VzG"). Use a route relation with route=railway for KBS numbers, instead.'})
        self.errors[9016019] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'ref=* should be a VzG number without "VzG"'})
        self.errors[9016020] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'VzG numbers should be tagged as ref=* without "VzG"'})
        self.errors[9016021] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'ref=* should only be a VzG number, it should not contain the track number'})
        self.errors[9016022] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Track names should be real names. VzG numbers should be tagged ref=*. KBS numbers should be mapped as a relation with route=railway.'})
        self.errors[9016023] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Track names should be real names. KBS numbers should be mapped as a relation with route=railway.'})
        self.errors[9016024] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Track names should be real names. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'})
        self.errors[9016025] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway.'})
        self.errors[9016026] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'})
        self.errors[9016028] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'workrules=BOA is deprecated, replace by an adequate value'})
        self.errors[9016029] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'workrules: separate country and ruleset by : , not by -'})
        self.errors[9016030] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': mapcss._tag_uncapture(capture_tags, '{1.value} signals only exist as light signals')})
        self.errors[9016031] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': mapcss._tag_uncapture(capture_tags, 'workrules={1.value} is deprecated, change to workrules=DE:{1.value}')})
        self.errors[9016032] = self.def_class(item = 9016, level = 2, tags = ["tag", "railway"], title = {'en': 'It is not possible that a main or combined signal both has a substitute signal and has no substitute signal.'})

        self.re_057dc3df = re.compile(r'^Kursbuchstrecke [0-9]*.*')
        self.re_103aec5a = re.compile(r'^DE-ESO:')
        self.re_12ca7ec2 = re.compile(r'^[0-9]{3}\.[0-9]+$')
        self.re_27c794aa = re.compile(r'^[0-9]{3}\.[0-9]{1,2}[-.][0-9]{1,2}$')
        self.re_36ee52ff = re.compile(r'^[0-9]{4}-[0-9]+')
        self.re_38b81466 = re.compile(r'^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$')
        self.re_3b196b7c = re.compile(r';no|no;')
        self.re_480b052a = re.compile(r'^VzG [0-9]*.*')
        self.re_48fcc4a9 = re.compile(r'^[0-9]{3}$')
        self.re_4fd6fb40 = re.compile(r'^KBS [0-9]*.*')
        self.re_555f3b4c = re.compile(r'^[0-9]{4}$')
        self.re_707f42a1 = re.compile(r'^[1-9][0-9]?[05]$')
        self.re_77700681 = re.compile(r'^(.*;)?DE-ESO:kennlicht(;.*)?$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[railway=signal][railway:signal:main="DE-ESO:ks"][railway:signal:main:form!=light]
        # node[railway=signal][railway:signal:distant="DE-ESO:ks"][railway:signal:distant:form!=light]
        # node[railway=signal][railway:signal:combined="DE-ESO:ks"][railway:signal:combined:form!=light]
        # node[railway=signal][railway:signal:main="DE-ESO:hl"][railway:signal:main:form!=light]
        # node[railway=signal][railway:signal:distant="DE-ESO:hl"][railway:signal:distant:form!=light]
        # node[railway=signal][railway:signal:combined="DE-ESO:hl"][railway:signal:combined:form!=light]
        if ('railway' in keys and 'railway:signal:combined' in keys) or ('railway' in keys and 'railway:signal:distant' in keys) or ('railway' in keys and 'railway:signal:main' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:ks')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:ks')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:combined') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:ks')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:combined:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:hl')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:hl')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:combined') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:hl')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:combined:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"{1.value} signals only exist as light signals"
                # fixAdd:"{2.key}=light"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hl railway:signal:main:form=light"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hl railway:signal:main:form=semaphore"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hl"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:ks railway:signal:main:form=light"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:ks railway:signal:main:form=semaphore"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:ks"
                err.append({'class': 9016030, 'subclass': 64936959, 'text': {'en': mapcss._tag_uncapture(capture_tags, '{1.value} signals only exist as light signals')}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, '{2.key}=light')).split('=', 1)])
                }})

        # node[railway=signal][railway:signal:main="DE-ESO:hp"][railway:signal:main:form!=light][railway:signal:main:form!=semaphore]
        # node[railway=signal][railway:signal:distant="DE-ESO:vr"][railway:signal:distant:form!=light][railway:signal:distant:form!=semaphore]
        if ('railway' in keys and 'railway:signal:distant' in keys) or ('railway' in keys and 'railway:signal:main' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:hp')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:main:form') != mapcss._value_const_capture(capture_tags, 3, 'semaphore', 'semaphore')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:vr')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:distant:form') != mapcss._value_const_capture(capture_tags, 3, 'semaphore', 'semaphore')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"hp signals only exist as semaphore or light signals"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:main:form=light"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:main:form=semaphore"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:main:form=typo"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp"
                err.append({'class': 9016002, 'subclass': 1455678760, 'text': {'en': 'hp signals only exist as semaphore or light signals'}})

        # node[railway=signal][railway:signal:combined="DE-KVB:hp"][railway:signal:combined:form!=light]
        if ('railway' in keys and 'railway:signal:combined' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:combined') == mapcss._value_capture(capture_tags, 1, 'DE-KVB:hp')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:combined:form') != mapcss._value_const_capture(capture_tags, 2, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"KVB hp signals only exist as light signals"
                # assertNoMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=light"
                # assertNoMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=light"
                # assertMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=semaphore"
                # assertMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=typo"
                # assertMatch:"node railway=signal railway:signal:combined=DE-KVB:hp"
                err.append({'class': 9016003, 'subclass': 1610282655, 'text': {'en': 'KVB hp signals only exist as light signals'}})

        # node[railway=signal]["railway:signal:distant"="DE-ESO:vr"]["railway:signal:distant:repeated"="yes"]["railway:signal:distant:form"!="light"]
        if ('railway' in keys and 'railway:signal:distant' in keys and 'railway:signal:distant:repeated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:vr')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 2, 'yes')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:distant:form') != mapcss._value_const_capture(capture_tags, 3, 'light', 'light')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Vr repeated signals only exist as light signals"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes railway:signal:distant:form=light"
                # assertMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes railway:signal:distant:form=semaphore"
                # assertMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes"
                err.append({'class': 9016004, 'subclass': 377147416, 'text': {'en': 'Vr repeated signals only exist as light signals'}})

        # node["railway:signal:minor:states"="DE-ESO:sh0;DE-ESO:gsp2"]
        # node["railway:signal:minor:states"="sh0;gsp2"]
        if ('railway:signal:minor:states' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:minor:states') == mapcss._value_capture(capture_tags, 0, 'DE-ESO:sh0;DE-ESO:gsp2')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:minor:states') == mapcss._value_capture(capture_tags, 0, 'sh0;gsp2')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Signal Gsp 2 was renamed to Wn 7 in 2008"
                # suggestAlternative:"railway:signal:minor:states=DE-ESO:sh0;DE-ESO:wn7"
                # fixAdd:"railway:signal:minor:states=DE-ESO:sh0;DE-ESO:wn7"
                # assertMatch:"node railway=derail railway:signal:minor:states=DE-ESO:sh0;DE-ESO:gsp2"
                # assertNoMatch:"node railway=derail railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
                # assertNoMatch:"node railway=derail railway:signal:minor:states=DE-ESO:sh0;DE-ESO:wn7"
                # assertMatch:"node railway=signal railway:signal:minor:states=sh0;gsp2"
                err.append({'class': 9016005, 'subclass': 931682141, 'text': {'en': 'Signal Gsp 2 was renamed to Wn 7 in 2008'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:signal:minor:states','DE-ESO:sh0;DE-ESO:wn7']])
                }})

        # node["railway:signal:train_protection"="DE-ESO:ne14"]["railway:signal:train_protection:type"!=block_marker]
        if ('railway:signal:train_protection' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:train_protection') == mapcss._value_capture(capture_tags, 0, 'DE-ESO:ne14')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:train_protection:type') != mapcss._value_const_capture(capture_tags, 1, 'block_marker', 'block_marker')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Ne 14 sign requires additional tag railway:signal:train_protection:type=block_marker"
                # suggestAlternative:"railway:signal:train_protection:type=block_marker"
                # fixAdd:"railway:signal:train_protection:type=block_marker"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp"
                # assertNoMatch:"node railway=signal railway:signal:train_protection=DE-ESO:ne14 railway:signal:train_protection:type=block_marker"
                # assertMatch:"node railway=signal railway:signal:train_protection=DE-ESO:ne14"
                err.append({'class': 9016006, 'subclass': 1157239794, 'text': {'en': 'Ne 14 sign requires additional tag railway:signal:train_protection:type=block_marker'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:signal:train_protection:type','block_marker']])
                }})

        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"!~/^(.*;)?DE-ESO:kennlicht(;.*)?$/]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"~="DE-ESO:kennlicht"]["railway:signal:distant:shortened"="no"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"~="DE-ESO:kennlicht"][!"railway:signal:distant:shortened"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"=~/^DE-ESO:/]["railway:signal:main"!="DE-ESO:hp"]
        if ('railway:signal:distant:repeated' in keys and 'railway:signal:distant:shortened' in keys and 'railway:signal:main' in keys and 'railway:signal:main:states' in keys) or ('railway:signal:distant:repeated' in keys and 'railway:signal:main' in keys) or ('railway:signal:distant:repeated' in keys and 'railway:signal:main' in keys and 'railway:signal:main:states' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:hp')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_77700681, '^(.*;)?DE-ESO:kennlicht(;.*)?$'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main:states'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:hp')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main:states'), mapcss._value_capture(capture_tags, 2, 'DE-ESO:kennlicht'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:distant:shortened') == mapcss._value_capture(capture_tags, 3, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:hp')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main:states'), mapcss._value_capture(capture_tags, 2, 'DE-ESO:kennlicht'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:distant:shortened')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_103aec5a), mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main') != mapcss._value_const_capture(capture_tags, 2, 'DE-ESO:hp', 'DE-ESO:hp')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"main and repeated distant signal usually are not at the same place"
                # suggestAlternative:"railway:signal:distant:shortened=yes"
                # fixRemove:"railway:signal:distant:repeated"
                # fixAdd:"railway:signal:distant:shortened=yes"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=no"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes railway:signal:main:states=DE-ESO:hp0;DE-ESO:hp1"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes railway:signal:main:states=DE-ESO:hp0;DE-ESO:kennlicht railway:signal:distant:shortened=yes"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:distant=DE-ESO:vr"
                err.append({'class': 9016007, 'subclass': 1775285105, 'text': {'en': 'main and repeated distant signal usually are not at the same place'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:signal:distant:shortened','yes']]),
                    '-': ([
                    'railway:signal:distant:repeated'])
                }})

        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:distant"=~/^DE-ESO:/]["railway:signal:distant"!="DE-ESO:vr"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:distant"="DE-ESO:vr"][!"railway:signal:main"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:main"]["railway:signal:main"!="DE-ESO:hp"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:distant"="DE-ESO:vr"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"!~/^(.*;)?DE-ESO:kennlicht(;.*)?$/]
        if ('railway:signal:distant' in keys and 'railway:signal:distant:repeated' in keys and 'railway:signal:distant:shortened' in keys) or ('railway:signal:distant' in keys and 'railway:signal:distant:repeated' in keys and 'railway:signal:distant:shortened' in keys and 'railway:signal:main' in keys) or ('railway:signal:distant:repeated' in keys and 'railway:signal:distant:shortened' in keys and 'railway:signal:main' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant:shortened') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_103aec5a), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:distant') != mapcss._value_const_capture(capture_tags, 3, 'DE-ESO:vr', 'DE-ESO:vr')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant:shortened') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant') == mapcss._value_capture(capture_tags, 2, 'DE-ESO:vr')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:main')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant:shortened') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:main') != mapcss._value_const_capture(capture_tags, 3, 'DE-ESO:hp', 'DE-ESO:hp')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:distant:repeated') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant:shortened') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant') == mapcss._value_capture(capture_tags, 2, 'DE-ESO:vr')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 3, 'DE-ESO:hp')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_77700681, '^(.*;)?DE-ESO:kennlicht(;.*)?$'), mapcss._tag_capture(capture_tags, 4, tags, 'railway:signal:main:states'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"German distant signals can't be repeated and shortened at the same time"
                # assertMatch:"node railway=signal railway:signal:distant:repeated=yes railway:signal:distant:shortened=yes railway:signal:distant=DE-ESO:ks"
                # assertMatch:"node railway=signal railway:signal:distant:repeated=yes railway:signal:distant:shortened=yes railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp railway:signal:main:states=DE-ESO:hp0;DE-ESO:hp1"
                # assertMatch:"node railway=signal railway:signal:distant:repeated=yes railway:signal:distant:shortened=yes railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp"
                # assertMatch:"node railway=signal railway:signal:distant:repeated=yes railway:signal:distant:shortened=yes railway:signal:distant=DE-ESO:vr"
                # assertMatch:"node railway=signal railway:signal:distant:repeated=yes railway:signal:distant:shortened=yes railway:signal:main=DE-ESO:hl"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:ks railway:signal:distant:repeated=yes"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:ks railway:signal:distant:shortened=yes"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes railway:signal:distant:shortened=yes railway:signal:main=DE-ESO:hp railway:signal:main:states=DE-ESO:kennlicht;DE-ESO:hp1"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:shortened=yes"
                err.append({'class': 9016008, 'subclass': 331861787, 'text': {'en': 'German distant signals can\'t be repeated and shortened at the same time'}})

        # node["railway:signal:main"="DE-ESO:ks"]["railway:signal:distant"]
        # node["railway:signal:main"]["railway:signal:distant"="DE-ESO:ks"]
        if ('railway:signal:distant' in keys and 'railway:signal:main' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:main') == mapcss._value_capture(capture_tags, 0, 'DE-ESO:ks')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:main')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:ks')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"German Ks signals can't have main and distant signal at the same place, try a combined signal instead"
                # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:minor=DE-ESO:sh1"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:distant=DE-ESO:ks"
                # assertMatch:"node railway=signal railway:signal:main=DE-ESO:ks railway:signal:distant=DE-ESO:vr"
                err.append({'class': 9016009, 'subclass': 832014689, 'text': {'en': 'German Ks signals can\'t have main and distant signal at the same place, try a combined signal instead'}})

        # node[railway=signal]["railway:signal:minor"="DE-ESO:sh"]["railway:signal:minor:form"=semaphore]["railway:signal:minor:states"~="DE-ESO:hp0"]
        if ('railway' in keys and 'railway:signal:minor' in keys and 'railway:signal:minor:form' in keys and 'railway:signal:minor:states' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:minor') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:sh')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:minor:form') == mapcss._value_capture(capture_tags, 2, 'semaphore')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:minor:states'), mapcss._value_capture(capture_tags, 3, 'DE-ESO:hp0'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Sh semaphore signals cannot display Hp 0, but only Sh 0"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0;DE-ESO:sh1"
                # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:hp0"
                # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:hp0;DE-ESO:sh1"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
                err.append({'class': 9016010, 'subclass': 1342331763, 'text': {'en': 'Sh semaphore signals cannot display Hp 0, but only Sh 0'}})

        # node[railway=signal]["railway:signal:minor"="DE-ESO:sh"]["railway:signal:minor:form"=light]["railway:signal:minor:states"~="DE-ESO:sh0"]
        if ('railway' in keys and 'railway:signal:minor' in keys and 'railway:signal:minor:form' in keys and 'railway:signal:minor:states' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:minor') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:sh')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:minor:form') == mapcss._value_capture(capture_tags, 2, 'light')) and (mapcss.list_contains(mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:minor:states'), mapcss._value_capture(capture_tags, 3, 'DE-ESO:sh0'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Sh light signals cannot display Sh 0, but only Hp 0"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0;DE-ESO:sh1"
                # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:sh0"
                # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0"
                # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
                err.append({'class': 9016011, 'subclass': 1627617188, 'text': {'en': 'Sh light signals cannot display Sh 0, but only Hp 0'}})

        # node[railway=signal]["railway:signal:speed_limit_distant"="DE-ESO:zs3v"]["railway:signal:speed_limit_distant:form"=sign]["railway:signal:speed_limit_distant:speed"]["railway:signal:speed_limit_distant:speed"!~/^[1-9][0-9]?[05]$/]["railway:signal:speed_limit_distant:speed"!=5]["railway:signal:speed_limit_distant:speed"!="?"]
        # node[railway=signal]["railway:signal:speed_limit_distant"="DE-ESO:zs3v"]["railway:signal:speed_limit_distant:form"=sign]["railway:signal:speed_limit_distant:speed">160]
        if ('railway' in keys and 'railway:signal:speed_limit_distant' in keys and 'railway:signal:speed_limit_distant:form' in keys and 'railway:signal:speed_limit_distant:speed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit_distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:zs3v')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit_distant:form') == mapcss._value_capture(capture_tags, 2, 'sign')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:speed_limit_distant:speed')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_707f42a1, '^[1-9][0-9]?[05]$'), mapcss._tag_capture(capture_tags, 4, tags, 'railway:signal:speed_limit_distant:speed'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'railway:signal:speed_limit_distant:speed') != mapcss._value_capture(capture_tags, 5, 5)) and (mapcss._tag_capture(capture_tags, 6, tags, 'railway:signal:speed_limit_distant:speed') != mapcss._value_const_capture(capture_tags, 6, '?', '?')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit_distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:zs3v')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit_distant:form') == mapcss._value_capture(capture_tags, 2, 'sign')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:speed_limit_distant:speed') > mapcss._value_capture(capture_tags, 3, 160)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Zs3v sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=light railway:signal:speed_limit_distant:speed=\"80;90\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=light railway:signal:speed_limit_distant:speed=\"87\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=light railway:signal:speed_limit_distant:speed=foo"
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=\"80;90\""
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=05"
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=200"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=5"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=80"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=85"
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=87"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=?"
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=foo"
                err.append({'class': 9016012, 'subclass': 1868832018, 'text': {'en': 'Zs3v sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'}})

        # node[railway=signal]["railway:signal:speed_limit"="DE-ESO:zs3"]["railway:signal:speed_limit:form"=sign]["railway:signal:speed_limit:speed"]["railway:signal:speed_limit:speed"!~/^[1-9][0-9]?[05]$/]["railway:signal:speed_limit:speed"!=5]["railway:signal:speed_limit:speed"!="?"]
        # node[railway=signal]["railway:signal:speed_limit"="DE-ESO:zs3"]["railway:signal:speed_limit:form"=sign]["railway:signal:speed_limit:speed">160]
        if ('railway' in keys and 'railway:signal:speed_limit' in keys and 'railway:signal:speed_limit:form' in keys and 'railway:signal:speed_limit:speed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:zs3')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit:form') == mapcss._value_capture(capture_tags, 2, 'sign')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:speed_limit:speed')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_707f42a1, '^[1-9][0-9]?[05]$'), mapcss._tag_capture(capture_tags, 4, tags, 'railway:signal:speed_limit:speed'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'railway:signal:speed_limit:speed') != mapcss._value_capture(capture_tags, 5, 5)) and (mapcss._tag_capture(capture_tags, 6, tags, 'railway:signal:speed_limit:speed') != mapcss._value_const_capture(capture_tags, 6, '?', '?')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:zs3')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit:form') == mapcss._value_capture(capture_tags, 2, 'sign')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:speed_limit:speed') > mapcss._value_capture(capture_tags, 3, 160)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Zs3 sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"80;90\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=87"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=foo"
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=\"80;90\""
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=05"
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=200"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=5"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=80"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=85"
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=87"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=?"
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=foo"
                err.append({'class': 9016013, 'subclass': 1804825947, 'text': {'en': 'Zs3 sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'}})

        # node[railway=signal]["railway:signal:speed_limit_distant"="DE-ESO:zs3v"]["railway:signal:speed_limit:form"=light]["railway:signal:speed_limit_distant:speed"]["railway:signal:speed_limit_distant:speed"!~/^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$/]
        if ('railway' in keys and 'railway:signal:speed_limit:form' in keys and 'railway:signal:speed_limit_distant' in keys and 'railway:signal:speed_limit_distant:speed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit_distant') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:zs3v')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit:form') == mapcss._value_capture(capture_tags, 2, 'light')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:speed_limit_distant:speed')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_38b81466, '^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$'), mapcss._tag_capture(capture_tags, 4, tags, 'railway:signal:speed_limit_distant:speed'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Zs3v light signal states should have the form 'speed[;speed …][;off][;?], speeds can only be multiples of 10"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"80\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"80;120\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"80;120;off;?\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"80;?\""
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"80;foo\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"80;off\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"?;80;off;120\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=\"off;?\""
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=200"
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=85"
                # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit:form=light railway:signal:speed_limit_distant:speed=foo"
                err.append({'class': 9016014, 'subclass': 720472651, 'text': {'en': 'Zs3v light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'}})

        # node[railway=signal]["railway:signal:speed_limit"="DE-ESO:zs3"]["railway:signal:speed_limit:form"=light]["railway:signal:speed_limit:speed"]["railway:signal:speed_limit:speed"!~/^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$/]
        if ('railway' in keys and 'railway:signal:speed_limit' in keys and 'railway:signal:speed_limit:form' in keys and 'railway:signal:speed_limit:speed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:zs3')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit:form') == mapcss._value_capture(capture_tags, 2, 'light')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:signal:speed_limit:speed')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_38b81466, '^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$'), mapcss._tag_capture(capture_tags, 4, tags, 'railway:signal:speed_limit:speed'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Zs3 light signal states should have the form 'speed[;speed …][;off][;?], speeds can only be multiples of 10"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"80\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"80;120\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"80;120;off;?\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"80;?\""
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"80;foo\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"80;off\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"?;80;off;120\""
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=\"off;?\""
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=200"
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=85"
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=light railway:signal:speed_limit:speed=foo"
                err.append({'class': 9016015, 'subclass': 1065351347, 'text': {'en': 'Zs3 light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'}})

        # node|z16-[railway=signal]["railway:signal:speed_limit"="DE-ESO:db:zs10"]["railway:signal:speed_limit:form"=light]
        if ('railway' in keys and 'railway:signal:speed_limit' in keys and 'railway:signal:speed_limit:form' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit') == mapcss._value_capture(capture_tags, 1, 'DE-ESO:db:zs10')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit:form') == mapcss._value_capture(capture_tags, 2, 'light')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"It is unclear if Zs10 light signals have ever been placed, please double check."
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:db:zs1\" railway:signal:speed_limit:form=light"
                # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:db:zs10\" railway:signal:speed_limit:form=light"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:db:zs10\" railway:signal:speed_limit:form=sign"
                err.append({'class': 9016016, 'subclass': 1437297810, 'text': {'en': 'It is unclear if Zs10 light signals have ever been placed, please double check.'}})

        # node[railway=signal]["railway:signal:main:substitute_signal"=~/;no|no;/]
        # node[railway=signal]["railway:signal:combined:substitute_signal"=~/;no|no;/]
        if ('railway' in keys and 'railway:signal:combined:substitute_signal' in keys) or ('railway' in keys and 'railway:signal:main:substitute_signal' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3b196b7c), mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main:substitute_signal'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3b196b7c), mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:combined:substitute_signal'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"It is not possible that a main or combined signal both has a substitute signal and has no substitute signal."
                # assertMatch:"node railway=signal railway:signal:main:substitute_signal=\";no\""
                # assertMatch:"node railway=signal railway:signal:main:substitute_signal=\"?;no\""
                # assertMatch:"node railway=signal railway:signal:main:substitute_signal=\"DE-ESO:zs1;no\""
                # assertMatch:"node railway=signal railway:signal:main:substitute_signal=\"no;?\""
                # assertNoMatch:"node railway=signal railway:signal:main:substitute_signal=no"
                err.append({'class': 9016032, 'subclass': 1068560505, 'text': {'en': 'It is not possible that a main or combined signal both has a substitute signal and has no substitute signal.'}})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[railway][name=~/^KBS [0-9]*.*/]
        # way[railway][name=~/^Kursbuchstrecke [0-9]*.*/]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4fd6fb40), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_057dc3df), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Tracks should not be named by their timetable number (KBS xy). Use a route relation with route=railway, instead."
                # assertMatch:"way railway=light_rail name=\"Kursbuchstrecke 710.1\""
                # assertNoMatch:"way railway=light_rail ref=\"Kursbuchstrecke 710.1\""
                # assertMatch:"way railway=rail name=\"KBS 258\""
                # assertNoMatch:"way railway=rail name=Frankenbahn"
                err.append({'class': 9016017, 'subclass': 460679615, 'text': {'en': 'Tracks should not be named by their timetable number (KBS xy). Use a route relation with route=railway, instead.'}})

        # way[railway][ref=~/^KBS [0-9]*.*/]
        # way[railway][ref=~/^Kursbuchstrecke [0-9]*.*/]
        if ('railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4fd6fb40), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_057dc3df), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"ref=* should be a VzG number (without \"VzG\"). Use a route relation with route=railway for KBS numbers, instead."
                # assertMatch:"way railway=light_rail ref=\"Kursbuchstrecke 710.1\""
                # assertMatch:"way railway=rail ref=\"KBS 258\""
                # assertNoMatch:"way railway=rail ref=7400"
                err.append({'class': 9016018, 'subclass': 1307191883, 'text': {'en': 'ref=* should be a VzG number (without "VzG"). Use a route relation with route=railway for KBS numbers, instead.'}})

        # way[railway][ref=~/^VzG [0-9]*.*/]
        if ('railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480b052a), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"ref=* should be a VzG number without \"VzG\""
                # assertMatch:"way railway=rail ref=\"VzG 7400\""
                # assertNoMatch:"way railway=rail ref=7400"
                err.append({'class': 9016019, 'subclass': 1513071347, 'text': {'en': 'ref=* should be a VzG number without "VzG"'}})

        # way[railway][name=~/^VzG [0-9]*.*/]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480b052a), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"VzG numbers should be tagged as ref=* without \"VzG\""
                # assertMatch:"way railway=rail name=\"VzG 7400\""
                # assertNoMatch:"way railway=rail name=7400"
                err.append({'class': 9016020, 'subclass': 498921024, 'text': {'en': 'VzG numbers should be tagged as ref=* without "VzG"'}})

        # way[railway][ref=~/^[0-9]{4}-[0-9]+/]
        if ('railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_36ee52ff), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"ref=* should only be a VzG number, it should not contain the track number"
                # assertNoMatch:"way railway=rail ref=7400"
                # assertMatch:"way railway=rail ref=7400-1"
                err.append({'class': 9016021, 'subclass': 1211908367, 'text': {'en': 'ref=* should only be a VzG number, it should not contain the track number'}})

        # way[railway][name=~/^[0-9]{4}$/]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_555f3b4c), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Track names should be real names. VzG numbers should be tagged ref=*. KBS numbers should be mapped as a relation with route=railway."
                # suggestAlternative:"ref"
                # fixChangeKey:"name=>ref"
                # assertMatch:"way railway=rail name=\"7400\""
                # assertNoMatch:"way railway=rail name=\"750\""
                # assertNoMatch:"way railway=rail name=Hohenlohebahn"
                # assertNoMatch:"way railway=rail ref=7400"
                err.append({'class': 9016022, 'subclass': 1094567914, 'text': {'en': 'Track names should be real names. VzG numbers should be tagged ref=*. KBS numbers should be mapped as a relation with route=railway.'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref', mapcss.tag(tags, 'name')]]),
                    '-': ([
                    'name'])
                }})

        # way[railway][name=~/^[0-9]{3}\.[0-9]+$/]
        # way[railway][name=~/^[0-9]{3}\.[0-9]{1,2}[-.][0-9]{1,2}$/]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_12ca7ec2), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_27c794aa), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Track names should be real names. KBS numbers should be mapped as a relation with route=railway."
                # assertMatch:"way railway=rail name=\"740.4\""
                # assertNoMatch:"way railway=rail name=\"780\""
                # assertNoMatch:"way railway=rail name=\"790.4--5\""
                # assertMatch:"way railway=rail name=\"790.4-5\""
                # assertNoMatch:"way railway=rail name=\"790.4..5\""
                # assertMatch:"way railway=rail name=\"790.4.5\""
                # assertNoMatch:"way railway=rail name=\"790.4a5\""
                # assertNoMatch:"way railway=rail name=7400"
                # assertNoMatch:"way railway=rail name=7400a"
                # assertNoMatch:"way railway=rail name=Hohenlohebahn"
                err.append({'class': 9016023, 'subclass': 1319009137, 'text': {'en': 'Track names should be real names. KBS numbers should be mapped as a relation with route=railway.'}})

        # way[railway][name=~/^[0-9]{3}$/]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_48fcc4a9), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Track names should be real names. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*."
                # assertNoMatch:"way railway=rail name=\"740.4\""
                # assertMatch:"way railway=rail name=\"780\""
                # assertNoMatch:"way railway=rail name=\"790.4--5\""
                # assertNoMatch:"way railway=rail name=\"790.4-5\""
                # assertNoMatch:"way railway=rail name=\"790.4..5\""
                # assertNoMatch:"way railway=rail name=\"790.4.5\""
                # assertNoMatch:"way railway=rail name=\"790.4a5\""
                # assertNoMatch:"way railway=rail name=7400"
                # assertNoMatch:"way railway=rail name=7400a"
                # assertNoMatch:"way railway=rail name=Hohenlohebahn"
                err.append({'class': 9016024, 'subclass': 1536179499, 'text': {'en': 'Track names should be real names. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'}})

        # way[railway][ref=~/^[0-9]{3}\.[0-9]+$/]
        # way[railway][ref=~/^[0-9]{3}\.[0-9]{1,2}[-.][0-9]{1,2}$/]
        if ('railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_12ca7ec2), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_27c794aa), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway."
                # assertMatch:"way railway=rail ref=\"740.4\""
                # assertNoMatch:"way railway=rail ref=\"780\""
                # assertNoMatch:"way railway=rail ref=\"790.4--5\""
                # assertMatch:"way railway=rail ref=\"790.4-5\""
                # assertNoMatch:"way railway=rail ref=\"790.4..5\""
                # assertMatch:"way railway=rail ref=\"790.4.5\""
                # assertNoMatch:"way railway=rail ref=\"790.4a5\""
                # assertNoMatch:"way railway=rail ref=7400"
                # assertNoMatch:"way railway=rail ref=7400a"
                err.append({'class': 9016025, 'subclass': 1194218564, 'text': {'en': 'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway.'}})

        # way[railway][ref=~/^[0-9]{3}$/]
        if ('railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_48fcc4a9), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*."
                # assertNoMatch:"way railway=rail ref=\"740.4\""
                # assertMatch:"way railway=rail ref=\"780\""
                # assertNoMatch:"way railway=rail ref=\"790.4--5\""
                # assertNoMatch:"way railway=rail ref=\"790.4-5\""
                # assertNoMatch:"way railway=rail ref=\"790.4..5\""
                # assertNoMatch:"way railway=rail ref=\"790.4.5\""
                # assertNoMatch:"way railway=rail ref=\"790.4a5\""
                # assertNoMatch:"way railway=rail ref=7400"
                # assertNoMatch:"way railway=rail ref=7400a"
                err.append({'class': 9016026, 'subclass': 2032079245, 'text': {'en': 'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'}})

        # way[railway][workrules=EBO]
        # way[railway][workrules=ESBO]
        # way[railway][workrules=BOStrab]
        if ('railway' in keys and 'workrules' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'workrules') == mapcss._value_capture(capture_tags, 1, 'EBO')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'workrules') == mapcss._value_capture(capture_tags, 1, 'ESBO')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'workrules') == mapcss._value_capture(capture_tags, 1, 'BOStrab')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"workrules={1.value} is deprecated, change to workrules=DE:{1.value}"
                # fixAdd:"workrules=DE:{1.value}"
                # assertMatch:"way railway=rail workrules=BOStrab"
                # assertNoMatch:"way railway=rail workrules=DE:BOStrab"
                # assertNoMatch:"way railway=rail workrules=DE:EBO"
                # assertNoMatch:"way railway=rail workrules=DE:ESBO"
                # assertMatch:"way railway=rail workrules=EBO"
                # assertMatch:"way railway=rail workrules=ESBO"
                # assertNoMatch:"way railway=rail"
                err.append({'class': 9016031, 'subclass': 1085911640, 'text': {'en': mapcss._tag_uncapture(capture_tags, 'workrules={1.value} is deprecated, change to workrules=DE:{1.value}')}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, 'workrules=DE:{1.value}')).split('=', 1)])
                }})

        # way[railway][workrules=BOA]
        if ('railway' in keys and 'workrules' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'workrules') == mapcss._value_capture(capture_tags, 1, 'BOA')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"workrules=BOA is deprecated, replace by an adequate value"
                # assertMatch:"way railway=rail workrules=BOA"
                # assertNoMatch:"way railway=rail workrules=DE:BOStrab"
                # assertNoMatch:"way railway=rail"
                err.append({'class': 9016028, 'subclass': 219100574, 'text': {'en': 'workrules=BOA is deprecated, replace by an adequate value'}})

        # way[railway][workrules="DE-BOStrab"]
        if ('railway' in keys and 'workrules' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'workrules') == mapcss._value_capture(capture_tags, 1, 'DE-BOStrab')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"workrules: separate country and ruleset by : , not by -"
                # suggestAlternative:"workrules=DE:BOStrab"
                # fixAdd:"workrules=DE:BOStrab"
                # assertMatch:"way railway=rail workrules=DE-BOStrab"
                # assertNoMatch:"way railway=rail workrules=DE:BOStrab"
                err.append({'class': 9016029, 'subclass': 2059785415, 'text': {'en': 'workrules: separate country and ruleset by : , not by -'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['workrules','DE:BOStrab']])
                }})

        # way[railway][workrules="DE-EBO"]
        if ('railway' in keys and 'workrules' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'workrules') == mapcss._value_capture(capture_tags, 1, 'DE-EBO')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"workrules: separate country and ruleset by : , not by -"
                # suggestAlternative:"workrules=DE:EBO"
                # fixAdd:"workrules=DE:EBO"
                # assertMatch:"way railway=rail workrules=DE-EBO"
                # assertNoMatch:"way railway=rail workrules=DE:EBO"
                err.append({'class': 9016029, 'subclass': 2020708529, 'text': {'en': 'workrules: separate country and ruleset by : , not by -'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['workrules','DE:EBO']])
                }})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_de_openrailwaymap(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hl', 'railway:signal:main:form': 'light'}), expected={'class': 9016030, 'subclass': 64936959})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hl', 'railway:signal:main:form': 'semaphore'}), expected={'class': 9016030, 'subclass': 64936959})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hl'}), expected={'class': 9016030, 'subclass': 64936959})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:ks', 'railway:signal:main:form': 'light'}), expected={'class': 9016030, 'subclass': 64936959})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:ks', 'railway:signal:main:form': 'semaphore'}), expected={'class': 9016030, 'subclass': 64936959})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:ks'}), expected={'class': 9016030, 'subclass': 64936959})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hp', 'railway:signal:main:form': 'light'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hp', 'railway:signal:main:form': 'semaphore'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hp', 'railway:signal:main:form': 'typo'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-KVB:hp', 'railway:signal:combined:form': 'light'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-KVB:hp', 'railway:signal:combined:form': 'light'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-KVB:hp', 'railway:signal:combined:form': 'semaphore'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-KVB:hp', 'railway:signal:combined:form': 'typo'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-KVB:hp'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:form': 'light', 'railway:signal:distant:repeated': 'yes'}), expected={'class': 9016004, 'subclass': 377147416})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:form': 'semaphore', 'railway:signal:distant:repeated': 'yes'}), expected={'class': 9016004, 'subclass': 377147416})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes'}), expected={'class': 9016004, 'subclass': 377147416})
        self.check_err(n.node(data, {'railway': 'derail', 'railway:signal:minor:states': 'DE-ESO:sh0;DE-ESO:gsp2'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_not_err(n.node(data, {'railway': 'derail', 'railway:signal:minor:states': 'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_not_err(n.node(data, {'railway': 'derail', 'railway:signal:minor:states': 'DE-ESO:sh0;DE-ESO:wn7'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:minor:states': 'sh0;gsp2'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016006, 'subclass': 1157239794})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:train_protection': 'DE-ESO:ne14', 'railway:signal:train_protection:type': 'block_marker'}), expected={'class': 9016006, 'subclass': 1157239794})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:train_protection': 'DE-ESO:ne14'}), expected={'class': 9016006, 'subclass': 1157239794})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'no', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes', 'railway:signal:main': 'DE-ESO:hp', 'railway:signal:main:states': 'DE-ESO:hp0;DE-ESO:hp1'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes', 'railway:signal:distant:shortened': 'yes', 'railway:signal:main': 'DE-ESO:hp', 'railway:signal:main:states': 'DE-ESO:hp0;DE-ESO:kennlicht'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:ks', 'railway:signal:distant:repeated': 'yes', 'railway:signal:distant:shortened': 'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes', 'railway:signal:distant:shortened': 'yes', 'railway:signal:main': 'DE-ESO:hp', 'railway:signal:main:states': 'DE-ESO:hp0;DE-ESO:hp1'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes', 'railway:signal:distant:shortened': 'yes', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes', 'railway:signal:distant:shortened': 'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant:repeated': 'yes', 'railway:signal:distant:shortened': 'yes', 'railway:signal:main': 'DE-ESO:hl'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:ks', 'railway:signal:distant:repeated': 'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:ks', 'railway:signal:distant:shortened': 'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes', 'railway:signal:distant:shortened': 'yes', 'railway:signal:main': 'DE-ESO:hp', 'railway:signal:main:states': 'DE-ESO:kennlicht;DE-ESO:hp1'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:repeated': 'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:distant:shortened': 'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-ESO:ks', 'railway:signal:minor': 'DE-ESO:sh1'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:ks', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:main': 'DE-ESO:ks'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'light', 'railway:signal:minor:states': 'DE-ESO:hp0'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'light', 'railway:signal:minor:states': 'DE-ESO:hp0;DE-ESO:sh1'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'semaphore', 'railway:signal:minor:states': 'DE-ESO:hp0'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'semaphore', 'railway:signal:minor:states': 'DE-ESO:hp0;DE-ESO:sh1'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'semaphore', 'railway:signal:minor:states': 'DE-ESO:sh0'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'semaphore', 'railway:signal:minor:states': 'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'light', 'railway:signal:minor:states': 'DE-ESO:hp0'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'light', 'railway:signal:minor:states': 'DE-ESO:hp0;DE-ESO:sh1'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'light', 'railway:signal:minor:states': 'DE-ESO:sh0'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'light', 'railway:signal:minor:states': 'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'semaphore', 'railway:signal:minor:states': 'DE-ESO:sh0'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:minor': 'DE-ESO:sh', 'railway:signal:minor:form': 'semaphore', 'railway:signal:minor:states': 'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'light', 'railway:signal:speed_limit_distant:speed': '80;90'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'light', 'railway:signal:speed_limit_distant:speed': '87'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'light', 'railway:signal:speed_limit_distant:speed': 'foo'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '80;90'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '05'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '200'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '5'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '80'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '85'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '87'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': '?'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:form': 'sign', 'railway:signal:speed_limit_distant:speed': 'foo'}), expected={'class': 9016012, 'subclass': 1868832018})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '80;90'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '87'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': 'foo'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '80;90'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '05'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '200'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '5'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '80'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '85'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '87'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '?'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': 'foo'}), expected={'class': 9016013, 'subclass': 1804825947})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '80'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '80;120'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '80;120;off;?'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '80;?'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '80;foo'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '80;off'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '?;80;off;120'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': 'off;?'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '200'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': '85'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit_distant': 'DE-ESO:zs3v', 'railway:signal:speed_limit_distant:speed': 'foo'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '80'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '80;120'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '80;120;off;?'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '80;?'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '80;foo'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '80;off'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '?;80;off;120'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': 'off;?'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '200'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': '85'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:zs3', 'railway:signal:speed_limit:form': 'light', 'railway:signal:speed_limit:speed': 'foo'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:db:zs1', 'railway:signal:speed_limit:form': 'light'}), expected={'class': 9016016, 'subclass': 1437297810})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:db:zs10', 'railway:signal:speed_limit:form': 'light'}), expected={'class': 9016016, 'subclass': 1437297810})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit': 'DE-ESO:db:zs10', 'railway:signal:speed_limit:form': 'sign'}), expected={'class': 9016016, 'subclass': 1437297810})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main:substitute_signal': ';no'}), expected={'class': 9016032, 'subclass': 1068560505})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main:substitute_signal': '?;no'}), expected={'class': 9016032, 'subclass': 1068560505})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main:substitute_signal': 'DE-ESO:zs1;no'}), expected={'class': 9016032, 'subclass': 1068560505})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main:substitute_signal': 'no;?'}), expected={'class': 9016032, 'subclass': 1068560505})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main:substitute_signal': 'no'}), expected={'class': 9016032, 'subclass': 1068560505})
        self.check_err(n.way(data, {'name': 'Kursbuchstrecke 710.1', 'railway': 'light_rail'}, [0]), expected={'class': 9016017, 'subclass': 460679615})
        self.check_not_err(n.way(data, {'railway': 'light_rail', 'ref': 'Kursbuchstrecke 710.1'}, [0]), expected={'class': 9016017, 'subclass': 460679615})
        self.check_err(n.way(data, {'name': 'KBS 258', 'railway': 'rail'}, [0]), expected={'class': 9016017, 'subclass': 460679615})
        self.check_not_err(n.way(data, {'name': 'Frankenbahn', 'railway': 'rail'}, [0]), expected={'class': 9016017, 'subclass': 460679615})
        self.check_err(n.way(data, {'railway': 'light_rail', 'ref': 'Kursbuchstrecke 710.1'}, [0]), expected={'class': 9016018, 'subclass': 1307191883})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': 'KBS 258'}, [0]), expected={'class': 9016018, 'subclass': 1307191883})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400'}, [0]), expected={'class': 9016018, 'subclass': 1307191883})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': 'VzG 7400'}, [0]), expected={'class': 9016019, 'subclass': 1513071347})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400'}, [0]), expected={'class': 9016019, 'subclass': 1513071347})
        self.check_err(n.way(data, {'name': 'VzG 7400', 'railway': 'rail'}, [0]), expected={'class': 9016020, 'subclass': 498921024})
        self.check_not_err(n.way(data, {'name': '7400', 'railway': 'rail'}, [0]), expected={'class': 9016020, 'subclass': 498921024})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400'}, [0]), expected={'class': 9016021, 'subclass': 1211908367})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': '7400-1'}, [0]), expected={'class': 9016021, 'subclass': 1211908367})
        self.check_err(n.way(data, {'name': '7400', 'railway': 'rail'}, [0]), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_not_err(n.way(data, {'name': '750', 'railway': 'rail'}, [0]), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_not_err(n.way(data, {'name': 'Hohenlohebahn', 'railway': 'rail'}, [0]), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400'}, [0]), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_err(n.way(data, {'name': '740.4', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': '780', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': '790.4--5', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_err(n.way(data, {'name': '790.4-5', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': '790.4..5', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_err(n.way(data, {'name': '790.4.5', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': '790.4a5', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': '7400', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': '7400a', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': 'Hohenlohebahn', 'railway': 'rail'}, [0]), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {'name': '740.4', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_err(n.way(data, {'name': '780', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': '790.4--5', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': '790.4-5', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': '790.4..5', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': '790.4.5', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': '790.4a5', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': '7400', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': '7400a', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {'name': 'Hohenlohebahn', 'railway': 'rail'}, [0]), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': '740.4'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '780'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4--5'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': '790.4-5'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4..5'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': '790.4.5'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4a5'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400a'}, [0]), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '740.4'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': '780'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4--5'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4-5'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4..5'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4.5'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '790.4a5'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '7400a'}, [0]), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_err(n.way(data, {'railway': 'rail', 'workrules': 'BOStrab'}, [0]), expected={'class': 9016031, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {'railway': 'rail', 'workrules': 'DE:BOStrab'}, [0]), expected={'class': 9016031, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {'railway': 'rail', 'workrules': 'DE:EBO'}, [0]), expected={'class': 9016031, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {'railway': 'rail', 'workrules': 'DE:ESBO'}, [0]), expected={'class': 9016031, 'subclass': 1085911640})
        self.check_err(n.way(data, {'railway': 'rail', 'workrules': 'EBO'}, [0]), expected={'class': 9016031, 'subclass': 1085911640})
        self.check_err(n.way(data, {'railway': 'rail', 'workrules': 'ESBO'}, [0]), expected={'class': 9016031, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {'railway': 'rail'}, [0]), expected={'class': 9016031, 'subclass': 1085911640})
        self.check_err(n.way(data, {'railway': 'rail', 'workrules': 'BOA'}, [0]), expected={'class': 9016028, 'subclass': 219100574})
        self.check_not_err(n.way(data, {'railway': 'rail', 'workrules': 'DE:BOStrab'}, [0]), expected={'class': 9016028, 'subclass': 219100574})
        self.check_not_err(n.way(data, {'railway': 'rail'}, [0]), expected={'class': 9016028, 'subclass': 219100574})
        self.check_err(n.way(data, {'railway': 'rail', 'workrules': 'DE-BOStrab'}, [0]), expected={'class': 9016029, 'subclass': 2059785415})
        self.check_not_err(n.way(data, {'railway': 'rail', 'workrules': 'DE:BOStrab'}, [0]), expected={'class': 9016029, 'subclass': 2059785415})
        self.check_err(n.way(data, {'railway': 'rail', 'workrules': 'DE-EBO'}, [0]), expected={'class': 9016029, 'subclass': 2020708529})
        self.check_not_err(n.way(data, {'railway': 'rail', 'workrules': 'DE:EBO'}, [0]), expected={'class': 9016029, 'subclass': 2020708529})
