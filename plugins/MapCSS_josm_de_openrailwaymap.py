#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_de_openrailwaymap(Plugin):

    only_for = ['DE']

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9016001] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'{1.value} signals only exist as light signals'}}
        self.errors[9016002] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'hp signals only exist as semaphore or light signals'}}
        self.errors[9016003] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'KVB hp signals only exist as light signals'}}
        self.errors[9016004] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Vr repeated signals only exist as light signals'}}
        self.errors[9016005] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Signal Gsp 2 was renamed to Wn 7 in 2008'}}
        self.errors[9016006] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Ne 14 sign requires additional tag railway:signal:train_protection:type=block_marker'}}
        self.errors[9016007] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'main and repeated distant signal usually are not at the same place'}}
        self.errors[9016008] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'German distant signals can\'t be repeated and shortened at the same time'}}
        self.errors[9016009] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'German Ks signals can\'t have main and distant signal at the same place, try a combined signal instead'}}
        self.errors[9016010] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Sh semaphore signals cannot display Hp 0, but only Sh 0'}}
        self.errors[9016011] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Sh light signals cannot display Sh 0, but only Hp 0'}}
        self.errors[9016012] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Zs3v sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'}}
        self.errors[9016013] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Zs3 sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'}}
        self.errors[9016014] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Zs3v light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'}}
        self.errors[9016015] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Zs3 light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'}}
        self.errors[9016016] = {'item': 9016, 'level': 2, 'tag': [], 'desc': {'en': u'It is unclear if Zs10 light signals have ever been placed, please double check.'}}
        self.errors[9016017] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Tracks should not be named by their timetable number (KBS xy). Use a route relation with route=railway, instead.'}}
        self.errors[9016018] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'ref=* should be a VzG number (without "VzG"). Use a route relation with route=railway for KBS numbers, instead.'}}
        self.errors[9016019] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'ref=* should be a VzG number without "VzG"'}}
        self.errors[9016020] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'VzG numbers should be tagged as ref=* without "VzG"'}}
        self.errors[9016021] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'ref=* should only be a VzG number, it should not contain the track number'}}
        self.errors[9016022] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Track names should be real names. VzG numbers should be tagged ref=*. KBS numbers should be mapped as a relation with route=railway.'}}
        self.errors[9016023] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Track names should be real names. KBS numbers should be mapped as a relation with route=railway.'}}
        self.errors[9016024] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Track names should be real names. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'}}
        self.errors[9016025] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway.'}}
        self.errors[9016026] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'}}
        self.errors[9016027] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'workrules={1.value} is deprecated, change to workrules=DE:{1.value}'}}
        self.errors[9016028] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'workrules=BOA is deprecated, replace by an adequate value'}}
        self.errors[9016029] = {'item': 9016, 'level': 1, 'tag': [], 'desc': {'en': u'workrules: separate country and ruleset by : , not by -'}}

        self.re_057dc3df = re.compile(ur'^Kursbuchstrecke [0-9]*.*')
        self.re_103aec5a = re.compile(ur'^DE-ESO:')
        self.re_12ca7ec2 = re.compile(ur'^[0-9]{3}\.[0-9]+$')
        self.re_27c794aa = re.compile(ur'^[0-9]{3}\.[0-9]{1,2}[-.][0-9]{1,2}$')
        self.re_36ee52ff = re.compile(ur'^[0-9]{4}-[0-9]+')
        self.re_38b81466 = re.compile(ur'^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$')
        self.re_480b052a = re.compile(ur'^VzG [0-9]*.*')
        self.re_48fcc4a9 = re.compile(ur'^[0-9]{3}$')
        self.re_4fd6fb40 = re.compile(ur'^KBS [0-9]*.*')
        self.re_555f3b4c = re.compile(ur'^[0-9]{4}$')
        self.re_707f42a1 = re.compile(ur'^[1-9][0-9]?[05]$')
        self.re_77700681 = re.compile(ur'^(.*;)?DE-ESO:kennlicht(;.*)?$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[railway=signal][railway:signal:main="DE-ESO:ks"][railway:signal:main:form!=light]
        # node[railway=signal][railway:signal:distant="DE-ESO:ks"][railway:signal:distant:form!=light]
        # node[railway=signal][railway:signal:combined="DE-ESO:ks"][railway:signal:combined:form!=light]
        # node[railway=signal][railway:signal:main="DE-ESO:hl"][railway:signal:main:form!=light]
        # node[railway=signal][railway:signal:distant="DE-ESO:hl"][railway:signal:distant:form!=light]
        # node[railway=signal][railway:signal:combined="DE-ESO:hl"][railway:signal:combined:form!=light]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main') == u'DE-ESO:ks' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main:form') != u'light') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant') == u'DE-ESO:ks' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant:form') != u'light') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:combined') == u'DE-ESO:ks' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:combined:form') != u'light') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main') == u'DE-ESO:hl' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main:form') != u'light') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant') == u'DE-ESO:hl' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant:form') != u'light') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:combined') == u'DE-ESO:hl' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:combined:form') != u'light')):
            # throwError:"{1.value} signals only exist as light signals"
            # fixAdd:"{2.key}=light"
            # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hl railway:signal:main:form=light"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hl railway:signal:main:form=semaphore"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hl"
            # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:ks railway:signal:main:form=light"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:ks railway:signal:main:form=semaphore"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:ks"
            err.append({'class': 9016001, 'subclass': 64936959, 'text': {'en': u'{1.value} signals only exist as light signals'}, 'fix': {
                '+': dict([
                    [u'{2.key}',u'light']])
            }})

        # node[railway=signal][railway:signal:main="DE-ESO:hp"][railway:signal:main:form!=light][railway:signal:main:form!=semaphore]
        # node[railway=signal][railway:signal:distant="DE-ESO:vr"][railway:signal:distant:form!=light][railway:signal:distant:form!=semaphore]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main') == u'DE-ESO:hp' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main:form') != u'light' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:main:form') != u'semaphore') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant') == u'DE-ESO:vr' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant:form') != u'light' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:distant:form') != u'semaphore')):
            # throwError:"hp signals only exist as semaphore or light signals"
            # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:main:form=light"
            # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:main:form=semaphore"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:main:form=typo"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp"
            err.append({'class': 9016002, 'subclass': 1455678760, 'text': {'en': u'hp signals only exist as semaphore or light signals'}})

        # node[railway=signal][railway:signal:combined="DE-KVB:hp"][railway:signal:combined:form!=light]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:combined') == u'DE-KVB:hp' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:combined:form') != u'light')):
            # throwError:"KVB hp signals only exist as light signals"
            # assertNoMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=light"
            # assertNoMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=light"
            # assertMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=semaphore"
            # assertMatch:"node railway=signal railway:signal:combined=DE-KVB:hp railway:signal:combined:form=typo"
            # assertMatch:"node railway=signal railway:signal:combined=DE-KVB:hp"
            err.append({'class': 9016003, 'subclass': 1610282655, 'text': {'en': u'KVB hp signals only exist as light signals'}})

        # node[railway=signal]["railway:signal:distant"="DE-ESO:vr"]["railway:signal:distant:repeated"="yes"]["railway:signal:distant:form"!="light"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant') == u'DE-ESO:vr' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:distant:form') != u'light')):
            # throwError:"Vr repeated signals only exist as light signals"
            # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes railway:signal:distant:form=light"
            # assertMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes railway:signal:distant:form=semaphore"
            # assertMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:distant:repeated=yes"
            err.append({'class': 9016004, 'subclass': 377147416, 'text': {'en': u'Vr repeated signals only exist as light signals'}})

        # node["railway:signal:minor:states"="DE-ESO:sh0;DE-ESO:gsp2"]
        # node["railway:signal:minor:states"="sh0;gsp2"]
        if (u'railway:signal:minor:states' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:minor:states') == u'DE-ESO:sh0;DE-ESO:gsp2') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:minor:states') == u'sh0;gsp2')):
            # throwError:"Signal Gsp 2 was renamed to Wn 7 in 2008"
            # suggestAlternative:"railway:signal:minor:states=DE-ESO:sh0;DE-ESO:wn7"
            # fixAdd:"railway:signal:minor:states=DE-ESO:sh0;DE-ESO:wn7"
            # assertMatch:"node railway=derail railway:signal:minor:states=DE-ESO:sh0;DE-ESO:gsp2"
            # assertNoMatch:"node railway=derail railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
            # assertNoMatch:"node railway=derail railway:signal:minor:states=DE-ESO:sh0;DE-ESO:wn7"
            # assertMatch:"node railway=signal railway:signal:minor:states=sh0;gsp2"
            err.append({'class': 9016005, 'subclass': 931682141, 'text': {'en': u'Signal Gsp 2 was renamed to Wn 7 in 2008'}, 'fix': {
                '+': dict([
                    [u'railway:signal:minor:states',u'DE-ESO:sh0;DE-ESO:wn7']])
            }})

        # node["railway:signal:train_protection"="DE-ESO:ne14"]["railway:signal:train_protection:type"!=block_marker]
        if (u'railway:signal:train_protection' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:train_protection') == u'DE-ESO:ne14' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:train_protection:type') != u'block_marker')):
            # throwError:"Ne 14 sign requires additional tag railway:signal:train_protection:type=block_marker"
            # suggestAlternative:"railway:signal:train_protection:type=block_marker"
            # fixAdd:"railway:signal:train_protection:type=block_marker"
            # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:hp"
            # assertNoMatch:"node railway=signal railway:signal:train_protection=DE-ESO:ne14 railway:signal:train_protection:type=block_marker"
            # assertMatch:"node railway=signal railway:signal:train_protection=DE-ESO:ne14"
            err.append({'class': 9016006, 'subclass': 1157239794, 'text': {'en': u'Ne 14 sign requires additional tag railway:signal:train_protection:type=block_marker'}, 'fix': {
                '+': dict([
                    [u'railway:signal:train_protection:type',u'block_marker']])
            }})

        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"!~/^(.*;)?DE-ESO:kennlicht(;.*)?$/]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"~="DE-ESO:kennlicht"]["railway:signal:distant:shortened"="no"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"~="DE-ESO:kennlicht"][!"railway:signal:distant:shortened"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:main"=~/^DE-ESO:/]["railway:signal:main"!="DE-ESO:hp"]
        if (u'railway:signal:distant:repeated' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main') == u'DE-ESO:hp' and not mapcss.regexp_test_(self.re_77700681, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main:states'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main') == u'DE-ESO:hp' and mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main:states'), u'DE-ESO:kennlicht') and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:distant:shortened') == u'no') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main') == u'DE-ESO:hp' and mapcss.list_contains(mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main:states'), u'DE-ESO:kennlicht') and not mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:distant:shortened')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss.regexp_test_(self.re_103aec5a, mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main')) and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main') != u'DE-ESO:hp')):
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
            err.append({'class': 9016007, 'subclass': 1775285105, 'text': {'en': u'main and repeated distant signal usually are not at the same place'}, 'fix': {
                '+': dict([
                    [u'railway:signal:distant:shortened',u'yes']]),
                '-': ([
                    u'railway:signal:distant:repeated'])
            }})

        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:distant"=~/^DE-ESO:/]["railway:signal:distant"!="DE-ESO:vr"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:distant"="DE-ESO:vr"][!"railway:signal:main"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:main"]["railway:signal:main"!="DE-ESO:hp"]
        # node["railway:signal:distant:repeated"="yes"]["railway:signal:distant:shortened"="yes"]["railway:signal:distant"="DE-ESO:vr"]["railway:signal:main"="DE-ESO:hp"]["railway:signal:main:states"!~/^(.*;)?DE-ESO:kennlicht(;.*)?$/]
        if (u'railway:signal:distant:repeated' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant:shortened') == u'yes' and mapcss.regexp_test_(self.re_103aec5a, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant')) and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:distant') != u'DE-ESO:vr') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant:shortened') == u'yes' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant') == u'DE-ESO:vr' and not mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:main')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant:shortened') == u'yes' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main') and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:main') != u'DE-ESO:hp') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:distant:repeated') == u'yes' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant:shortened') == u'yes' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant') == u'DE-ESO:vr' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:main') == u'DE-ESO:hp' and not mapcss.regexp_test_(self.re_77700681, mapcss._tag_capture(capture_tags, 4, tags, u'railway:signal:main:states')))):
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
            err.append({'class': 9016008, 'subclass': 331861787, 'text': {'en': u'German distant signals can\'t be repeated and shortened at the same time'}})

        # node["railway:signal:main"="DE-ESO:ks"]["railway:signal:distant"]
        # node["railway:signal:main"]["railway:signal:distant"="DE-ESO:ks"]
        if (u'railway:signal:main' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:main') == u'DE-ESO:ks' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:main') and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant') == u'DE-ESO:ks')):
            # throwError:"German Ks signals can't have main and distant signal at the same place, try a combined signal instead"
            # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:minor=DE-ESO:sh1"
            # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:hp railway:signal:distant=DE-ESO:ks"
            # assertMatch:"node railway=signal railway:signal:main=DE-ESO:ks railway:signal:distant=DE-ESO:vr"
            err.append({'class': 9016009, 'subclass': 832014689, 'text': {'en': u'German Ks signals can\'t have main and distant signal at the same place, try a combined signal instead'}})

        # node[railway=signal]["railway:signal:minor"="DE-ESO:sh"]["railway:signal:minor:form"=semaphore]["railway:signal:minor:states"~="DE-ESO:hp0"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:minor') == u'DE-ESO:sh' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:minor:form') == u'semaphore' and mapcss.list_contains(mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:minor:states'), u'DE-ESO:hp0'))):
            # throwError:"Sh semaphore signals cannot display Hp 0, but only Sh 0"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0;DE-ESO:sh1"
            # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:hp0"
            # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:hp0;DE-ESO:sh1"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
            err.append({'class': 9016010, 'subclass': 1342331763, 'text': {'en': u'Sh semaphore signals cannot display Hp 0, but only Sh 0'}})

        # node[railway=signal]["railway:signal:minor"="DE-ESO:sh"]["railway:signal:minor:form"=light]["railway:signal:minor:states"~="DE-ESO:sh0"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:minor') == u'DE-ESO:sh' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:minor:form') == u'light' and mapcss.list_contains(mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:minor:states'), u'DE-ESO:sh0'))):
            # throwError:"Sh light signals cannot display Sh 0, but only Hp 0"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:hp0;DE-ESO:sh1"
            # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:sh0"
            # assertMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=light railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0"
            # assertNoMatch:"node railway=signal railway:signal:minor=DE-ESO:sh railway:signal:minor:form=semaphore railway:signal:minor:states=DE-ESO:sh0;DE-ESO:sh1"
            err.append({'class': 9016011, 'subclass': 1627617188, 'text': {'en': u'Sh light signals cannot display Sh 0, but only Hp 0'}})

        # node[railway=signal]["railway:signal:speed_limit_distant"="DE-ESO:zs3v"]["railway:signal:speed_limit_distant:form"=sign]["railway:signal:speed_limit_distant:speed"]["railway:signal:speed_limit_distant:speed"!~/^[1-9][0-9]?[05]$/]["railway:signal:speed_limit_distant:speed"!=5]
        # node[railway=signal]["railway:signal:speed_limit_distant"="DE-ESO:zs3v"]["railway:signal:speed_limit_distant:form"=sign]["railway:signal:speed_limit_distant:speed">160]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit_distant') == u'DE-ESO:zs3v' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit_distant:form') == u'sign' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:speed_limit_distant:speed') and not mapcss.regexp_test_(self.re_707f42a1, mapcss._tag_capture(capture_tags, 4, tags, u'railway:signal:speed_limit_distant:speed')) and mapcss._tag_capture(capture_tags, 5, tags, u'railway:signal:speed_limit_distant:speed') != 5) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit_distant') == u'DE-ESO:zs3v' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit_distant:form') == u'sign' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:speed_limit_distant:speed') > 160)):
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
            # assertMatch:"node railway=signal railway:signal:speed_limit_distant=\"DE-ESO:zs3v\" railway:signal:speed_limit_distant:form=sign railway:signal:speed_limit_distant:speed=foo"
            err.append({'class': 9016012, 'subclass': 343469741, 'text': {'en': u'Zs3v sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'}})

        # node[railway=signal]["railway:signal:speed_limit"="DE-ESO:zs3"]["railway:signal:speed_limit:form"=sign]["railway:signal:speed_limit:speed"]["railway:signal:speed_limit:speed"!~/^[1-9][0-9]?[05]$/]["railway:signal:speed_limit:speed"!=5]
        # node[railway=signal]["railway:signal:speed_limit"="DE-ESO:zs3"]["railway:signal:speed_limit:form"=sign]["railway:signal:speed_limit:speed">160]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit') == u'DE-ESO:zs3' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit:form') == u'sign' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:speed_limit:speed') and not mapcss.regexp_test_(self.re_707f42a1, mapcss._tag_capture(capture_tags, 4, tags, u'railway:signal:speed_limit:speed')) and mapcss._tag_capture(capture_tags, 5, tags, u'railway:signal:speed_limit:speed') != 5) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit') == u'DE-ESO:zs3' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit:form') == u'sign' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:speed_limit:speed') > 160)):
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
            # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:zs3\" railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=foo"
            err.append({'class': 9016013, 'subclass': 139311887, 'text': {'en': u'Zs3 sign signals can only have a single speed, are a multiple of 5 and cannot be greater than 160'}})

        # node[railway=signal]["railway:signal:speed_limit_distant"="DE-ESO:zs3v"]["railway:signal:speed_limit:form"=light]["railway:signal:speed_limit_distant:speed"]["railway:signal:speed_limit_distant:speed"!~/^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit_distant') == u'DE-ESO:zs3v' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit:form') == u'light' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:speed_limit_distant:speed') and not mapcss.regexp_test_(self.re_38b81466, mapcss._tag_capture(capture_tags, 4, tags, u'railway:signal:speed_limit_distant:speed')))):
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
            err.append({'class': 9016014, 'subclass': 720472651, 'text': {'en': u'Zs3v light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'}})

        # node[railway=signal]["railway:signal:speed_limit"="DE-ESO:zs3"]["railway:signal:speed_limit:form"=light]["railway:signal:speed_limit:speed"]["railway:signal:speed_limit:speed"!~/^([1-9]0|1[0-6]0|off|\?)(;([1-9]0|1[0-6]0|off|\?))*$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit') == u'DE-ESO:zs3' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit:form') == u'light' and mapcss._tag_capture(capture_tags, 3, tags, u'railway:signal:speed_limit:speed') and not mapcss.regexp_test_(self.re_38b81466, mapcss._tag_capture(capture_tags, 4, tags, u'railway:signal:speed_limit:speed')))):
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
            err.append({'class': 9016015, 'subclass': 1065351347, 'text': {'en': u'Zs3 light signal states should have the form \'speed[;speed …][;off][;?], speeds can only be multiples of 10'}})

        # node[railway=signal]["railway:signal:speed_limit"="DE-ESO:db:zs10"]["railway:signal:speed_limit:form"=light]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit') == u'DE-ESO:db:zs10' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit:form') == u'light')):
            # throwWarning:"It is unclear if Zs10 light signals have ever been placed, please double check."
            # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:db:zs1\" railway:signal:speed_limit:form=light"
            # assertMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:db:zs10\" railway:signal:speed_limit:form=light"
            # assertNoMatch:"node railway=signal railway:signal:speed_limit=\"DE-ESO:db:zs10\" railway:signal:speed_limit:form=sign"
            err.append({'class': 9016016, 'subclass': 504597862, 'text': {'en': u'It is unclear if Zs10 light signals have ever been placed, please double check.'}})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[railway][name=~/^KBS [0-9]*.*/]
        # way[railway][name=~/^Kursbuchstrecke [0-9]*.*/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_4fd6fb40, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_057dc3df, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwError:"Tracks should not be named by their timetable number (KBS xy). Use a route relation with route=railway, instead."
            # assertMatch:"way railway=light_rail name=\"Kursbuchstrecke 710.1\""
            # assertNoMatch:"way railway=light_rail ref=\"Kursbuchstrecke 710.1\""
            # assertMatch:"way railway=rail name=\"KBS 258\""
            # assertNoMatch:"way railway=rail name=Frankenbahn"
            err.append({'class': 9016017, 'subclass': 460679615, 'text': {'en': u'Tracks should not be named by their timetable number (KBS xy). Use a route relation with route=railway, instead.'}})

        # way[railway][ref=~/^KBS [0-9]*.*/]
        # way[railway][ref=~/^Kursbuchstrecke [0-9]*.*/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_4fd6fb40, mapcss._tag_capture(capture_tags, 1, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_057dc3df, mapcss._tag_capture(capture_tags, 1, tags, u'ref')))):
            # throwError:"ref=* should be a VzG number (without \"VzG\"). Use a route relation with route=railway for KBS numbers, instead."
            # assertMatch:"way railway=light_rail ref=\"Kursbuchstrecke 710.1\""
            # assertMatch:"way railway=rail ref=\"KBS 258\""
            # assertNoMatch:"way railway=rail ref=7400"
            err.append({'class': 9016018, 'subclass': 1307191883, 'text': {'en': u'ref=* should be a VzG number (without "VzG"). Use a route relation with route=railway for KBS numbers, instead.'}})

        # way[railway][ref=~/^VzG [0-9]*.*/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_480b052a, mapcss._tag_capture(capture_tags, 1, tags, u'ref')))):
            # throwError:"ref=* should be a VzG number without \"VzG\""
            # assertMatch:"way railway=rail ref=\"VzG 7400\""
            # assertNoMatch:"way railway=rail ref=7400"
            err.append({'class': 9016019, 'subclass': 1513071347, 'text': {'en': u'ref=* should be a VzG number without "VzG"'}})

        # way[railway][name=~/^VzG [0-9]*.*/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_480b052a, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwError:"VzG numbers should be tagged as ref=* without \"VzG\""
            # assertMatch:"way railway=rail name=\"VzG 7400\""
            # assertNoMatch:"way railway=rail name=7400"
            err.append({'class': 9016020, 'subclass': 498921024, 'text': {'en': u'VzG numbers should be tagged as ref=* without "VzG"'}})

        # way[railway][ref=~/^[0-9]{4}-[0-9]+/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_36ee52ff, mapcss._tag_capture(capture_tags, 1, tags, u'ref')))):
            # throwError:"ref=* should only be a VzG number, it should not contain the track number"
            # assertNoMatch:"way railway=rail ref=7400"
            # assertMatch:"way railway=rail ref=7400-1"
            err.append({'class': 9016021, 'subclass': 1211908367, 'text': {'en': u'ref=* should only be a VzG number, it should not contain the track number'}})

        # way[railway][name=~/^[0-9]{4}$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_555f3b4c, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwError:"Track names should be real names. VzG numbers should be tagged ref=*. KBS numbers should be mapped as a relation with route=railway."
            # suggestAlternative:"ref"
            # fixChangeKey:"name=>ref"
            # assertMatch:"way railway=rail name=\"7400\""
            # assertNoMatch:"way railway=rail name=\"750\""
            # assertNoMatch:"way railway=rail name=Hohenlohebahn"
            # assertNoMatch:"way railway=rail ref=7400"
            err.append({'class': 9016022, 'subclass': 1094567914, 'text': {'en': u'Track names should be real names. VzG numbers should be tagged ref=*. KBS numbers should be mapped as a relation with route=railway.'}, 'fix': {
                '+': dict([
                    [u'ref', mapcss.tag(tags, u'name')]]),
                '-': ([
                    u'name'])
            }})

        # way[railway][name=~/^[0-9]{3}\.[0-9]+$/]
        # way[railway][name=~/^[0-9]{3}\.[0-9]{1,2}[-.][0-9]{1,2}$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_12ca7ec2, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_27c794aa, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
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
            err.append({'class': 9016023, 'subclass': 1319009137, 'text': {'en': u'Track names should be real names. KBS numbers should be mapped as a relation with route=railway.'}})

        # way[railway][name=~/^[0-9]{3}$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_48fcc4a9, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
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
            err.append({'class': 9016024, 'subclass': 1536179499, 'text': {'en': u'Track names should be real names. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'}})

        # way[railway][ref=~/^[0-9]{3}\.[0-9]+$/]
        # way[railway][ref=~/^[0-9]{3}\.[0-9]{1,2}[-.][0-9]{1,2}$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_12ca7ec2, mapcss._tag_capture(capture_tags, 1, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_27c794aa, mapcss._tag_capture(capture_tags, 1, tags, u'ref')))):
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
            err.append({'class': 9016025, 'subclass': 1194218564, 'text': {'en': u'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway.'}})

        # way[railway][ref=~/^[0-9]{3}$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_48fcc4a9, mapcss._tag_capture(capture_tags, 1, tags, u'ref')))):
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
            err.append({'class': 9016026, 'subclass': 2032079245, 'text': {'en': u'Track refs should be VzG numbers in Germany. KBS numbers should be mapped as a relation with route=railway, track numbers as railway:track_ref=*.'}})

        # way[railway][workrules=EBO]
        # way[railway][workrules=ESBO]
        # way[railway][workrules=BOStrab]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'workrules') == u'EBO') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'workrules') == u'ESBO') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'workrules') == u'BOStrab')):
            # throwError:"workrules={1.value} is deprecated, change to workrules=DE:{1.value}"
            # fixAdd:"workrules=DE:{1.value}"
            # assertMatch:"way railway=rail workrules=BOStrab"
            # assertNoMatch:"way railway=rail workrules=DE:BOStrab"
            # assertNoMatch:"way railway=rail workrules=DE:EBO"
            # assertNoMatch:"way railway=rail workrules=DE:ESBO"
            # assertMatch:"way railway=rail workrules=EBO"
            # assertMatch:"way railway=rail workrules=ESBO"
            # assertNoMatch:"way railway=rail"
            err.append({'class': 9016027, 'subclass': 1085911640, 'text': {'en': u'workrules={1.value} is deprecated, change to workrules=DE:{1.value}'}, 'fix': {
                '+': dict([
                    [u'workrules',u'DE:{1.value}']])
            }})

        # way[railway][workrules=BOA]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'workrules') == u'BOA')):
            # throwError:"workrules=BOA is deprecated, replace by an adequate value"
            # assertMatch:"way railway=rail workrules=BOA"
            # assertNoMatch:"way railway=rail workrules=DE:BOStrab"
            # assertNoMatch:"way railway=rail"
            err.append({'class': 9016028, 'subclass': 219100574, 'text': {'en': u'workrules=BOA is deprecated, replace by an adequate value'}})

        # way[railway][workrules="DE-BOStrab"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'workrules') == u'DE-BOStrab')):
            # throwError:"workrules: separate country and ruleset by : , not by -"
            # suggestAlternative:"workrules=DE:BOStrab"
            # fixAdd:"workrules=DE:BOStrab"
            # assertMatch:"way railway=rail workrules=DE-BOStrab"
            # assertNoMatch:"way railway=rail workrules=DE:BOStrab"
            err.append({'class': 9016029, 'subclass': 2059785415, 'text': {'en': u'workrules: separate country and ruleset by : , not by -'}, 'fix': {
                '+': dict([
                    [u'workrules',u'DE:BOStrab']])
            }})

        # way[railway][workrules="DE-EBO"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'workrules') == u'DE-EBO')):
            # throwError:"workrules: separate country and ruleset by : , not by -"
            # suggestAlternative:"workrules=DE:EBO"
            # fixAdd:"workrules=DE:EBO"
            # assertMatch:"way railway=rail workrules=DE-EBO"
            # assertNoMatch:"way railway=rail workrules=DE:EBO"
            err.append({'class': 9016029, 'subclass': 2020708529, 'text': {'en': u'workrules: separate country and ruleset by : , not by -'}, 'fix': {
                '+': dict([
                    [u'workrules',u'DE:EBO']])
            }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_de_openrailwaymap(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hl', u'railway:signal:main:form': u'light'}), expected={'class': 9016001, 'subclass': 64936959})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hl', u'railway:signal:main:form': u'semaphore'}), expected={'class': 9016001, 'subclass': 64936959})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hl'}), expected={'class': 9016001, 'subclass': 64936959})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:ks', u'railway:signal:main:form': u'light'}), expected={'class': 9016001, 'subclass': 64936959})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:ks', u'railway:signal:main:form': u'semaphore'}), expected={'class': 9016001, 'subclass': 64936959})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:ks'}), expected={'class': 9016001, 'subclass': 64936959})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hp', u'railway:signal:main:form': u'light'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hp', u'railway:signal:main:form': u'semaphore'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hp', u'railway:signal:main:form': u'typo'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016002, 'subclass': 1455678760})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-KVB:hp', u'railway:signal:combined:form': u'light'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-KVB:hp', u'railway:signal:combined:form': u'light'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-KVB:hp', u'railway:signal:combined:form': u'semaphore'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-KVB:hp', u'railway:signal:combined:form': u'typo'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-KVB:hp'}), expected={'class': 9016003, 'subclass': 1610282655})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:form': u'light', u'railway:signal:distant:repeated': u'yes'}), expected={'class': 9016004, 'subclass': 377147416})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:form': u'semaphore', u'railway:signal:distant:repeated': u'yes'}), expected={'class': 9016004, 'subclass': 377147416})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes'}), expected={'class': 9016004, 'subclass': 377147416})
        self.check_err(n.node(data, {u'railway': u'derail', u'railway:signal:minor:states': u'DE-ESO:sh0;DE-ESO:gsp2'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_not_err(n.node(data, {u'railway': u'derail', u'railway:signal:minor:states': u'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_not_err(n.node(data, {u'railway': u'derail', u'railway:signal:minor:states': u'DE-ESO:sh0;DE-ESO:wn7'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor:states': u'sh0;gsp2'}), expected={'class': 9016005, 'subclass': 931682141})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016006, 'subclass': 1157239794})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:train_protection': u'DE-ESO:ne14', u'railway:signal:train_protection:type': u'block_marker'}), expected={'class': 9016006, 'subclass': 1157239794})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:train_protection': u'DE-ESO:ne14'}), expected={'class': 9016006, 'subclass': 1157239794})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'no', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes', u'railway:signal:main': u'DE-ESO:hp', u'railway:signal:main:states': u'DE-ESO:hp0;DE-ESO:hp1'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes', u'railway:signal:distant:shortened': u'yes', u'railway:signal:main': u'DE-ESO:hp', u'railway:signal:main:states': u'DE-ESO:hp0;DE-ESO:kennlicht'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016007, 'subclass': 1775285105})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:ks', u'railway:signal:distant:repeated': u'yes', u'railway:signal:distant:shortened': u'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes', u'railway:signal:distant:shortened': u'yes', u'railway:signal:main': u'DE-ESO:hp', u'railway:signal:main:states': u'DE-ESO:hp0;DE-ESO:hp1'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes', u'railway:signal:distant:shortened': u'yes', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes', u'railway:signal:distant:shortened': u'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant:repeated': u'yes', u'railway:signal:distant:shortened': u'yes', u'railway:signal:main': u'DE-ESO:hl'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:ks', u'railway:signal:distant:repeated': u'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:ks', u'railway:signal:distant:shortened': u'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes', u'railway:signal:distant:shortened': u'yes', u'railway:signal:main': u'DE-ESO:hp', u'railway:signal:main:states': u'DE-ESO:kennlicht;DE-ESO:hp1'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:repeated': u'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:distant:shortened': u'yes'}), expected={'class': 9016008, 'subclass': 331861787})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-ESO:ks', u'railway:signal:minor': u'DE-ESO:sh1'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:ks', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:main': u'DE-ESO:ks'}), expected={'class': 9016009, 'subclass': 832014689})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'light', u'railway:signal:minor:states': u'DE-ESO:hp0'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'light', u'railway:signal:minor:states': u'DE-ESO:hp0;DE-ESO:sh1'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'semaphore', u'railway:signal:minor:states': u'DE-ESO:hp0'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'semaphore', u'railway:signal:minor:states': u'DE-ESO:hp0;DE-ESO:sh1'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'semaphore', u'railway:signal:minor:states': u'DE-ESO:sh0'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'semaphore', u'railway:signal:minor:states': u'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016010, 'subclass': 1342331763})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'light', u'railway:signal:minor:states': u'DE-ESO:hp0'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'light', u'railway:signal:minor:states': u'DE-ESO:hp0;DE-ESO:sh1'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'light', u'railway:signal:minor:states': u'DE-ESO:sh0'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'light', u'railway:signal:minor:states': u'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'semaphore', u'railway:signal:minor:states': u'DE-ESO:sh0'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:minor': u'DE-ESO:sh', u'railway:signal:minor:form': u'semaphore', u'railway:signal:minor:states': u'DE-ESO:sh0;DE-ESO:sh1'}), expected={'class': 9016011, 'subclass': 1627617188})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'light', u'railway:signal:speed_limit_distant:speed': u'80;90'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'light', u'railway:signal:speed_limit_distant:speed': u'87'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'light', u'railway:signal:speed_limit_distant:speed': u'foo'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'80;90'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'05'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'200'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'5'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'80'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'85'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'87'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:form': u'sign', u'railway:signal:speed_limit_distant:speed': u'foo'}), expected={'class': 9016012, 'subclass': 343469741})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'80;90'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'87'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'foo'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'80;90'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'05'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'200'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'5'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'80'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'85'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'87'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'foo'}), expected={'class': 9016013, 'subclass': 139311887})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'80'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'80;120'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'80;120;off;?'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'80;?'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'80;foo'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'80;off'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'?;80;off;120'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'off;?'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'200'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'85'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit_distant': u'DE-ESO:zs3v', u'railway:signal:speed_limit_distant:speed': u'foo'}), expected={'class': 9016014, 'subclass': 720472651})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'80'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'80;120'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'80;120;off;?'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'80;?'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'80;foo'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'80;off'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'?;80;off;120'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'off;?'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'200'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'85'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:zs3', u'railway:signal:speed_limit:form': u'light', u'railway:signal:speed_limit:speed': u'foo'}), expected={'class': 9016015, 'subclass': 1065351347})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:db:zs1', u'railway:signal:speed_limit:form': u'light'}), expected={'class': 9016016, 'subclass': 504597862})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:db:zs10', u'railway:signal:speed_limit:form': u'light'}), expected={'class': 9016016, 'subclass': 504597862})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit': u'DE-ESO:db:zs10', u'railway:signal:speed_limit:form': u'sign'}), expected={'class': 9016016, 'subclass': 504597862})
        self.check_err(n.way(data, {u'name': u'Kursbuchstrecke 710.1', u'railway': u'light_rail'}), expected={'class': 9016017, 'subclass': 460679615})
        self.check_not_err(n.way(data, {u'railway': u'light_rail', u'ref': u'Kursbuchstrecke 710.1'}), expected={'class': 9016017, 'subclass': 460679615})
        self.check_err(n.way(data, {u'name': u'KBS 258', u'railway': u'rail'}), expected={'class': 9016017, 'subclass': 460679615})
        self.check_not_err(n.way(data, {u'name': u'Frankenbahn', u'railway': u'rail'}), expected={'class': 9016017, 'subclass': 460679615})
        self.check_err(n.way(data, {u'railway': u'light_rail', u'ref': u'Kursbuchstrecke 710.1'}), expected={'class': 9016018, 'subclass': 1307191883})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'KBS 258'}), expected={'class': 9016018, 'subclass': 1307191883})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400'}), expected={'class': 9016018, 'subclass': 1307191883})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'VzG 7400'}), expected={'class': 9016019, 'subclass': 1513071347})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400'}), expected={'class': 9016019, 'subclass': 1513071347})
        self.check_err(n.way(data, {u'name': u'VzG 7400', u'railway': u'rail'}), expected={'class': 9016020, 'subclass': 498921024})
        self.check_not_err(n.way(data, {u'name': u'7400', u'railway': u'rail'}), expected={'class': 9016020, 'subclass': 498921024})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400'}), expected={'class': 9016021, 'subclass': 1211908367})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'7400-1'}), expected={'class': 9016021, 'subclass': 1211908367})
        self.check_err(n.way(data, {u'name': u'7400', u'railway': u'rail'}), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_not_err(n.way(data, {u'name': u'750', u'railway': u'rail'}), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_not_err(n.way(data, {u'name': u'Hohenlohebahn', u'railway': u'rail'}), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400'}), expected={'class': 9016022, 'subclass': 1094567914})
        self.check_err(n.way(data, {u'name': u'740.4', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'780', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'790.4--5', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_err(n.way(data, {u'name': u'790.4-5', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'790.4..5', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_err(n.way(data, {u'name': u'790.4.5', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'790.4a5', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'7400', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'7400a', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'Hohenlohebahn', u'railway': u'rail'}), expected={'class': 9016023, 'subclass': 1319009137})
        self.check_not_err(n.way(data, {u'name': u'740.4', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_err(n.way(data, {u'name': u'780', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'790.4--5', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'790.4-5', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'790.4..5', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'790.4.5', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'790.4a5', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'7400', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'7400a', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_not_err(n.way(data, {u'name': u'Hohenlohebahn', u'railway': u'rail'}), expected={'class': 9016024, 'subclass': 1536179499})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'740.4'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'780'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4--5'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4-5'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4..5'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4.5'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4a5'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400a'}), expected={'class': 9016025, 'subclass': 1194218564})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'740.4'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'780'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4--5'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4-5'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4..5'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4.5'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'790.4a5'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'ref': u'7400a'}), expected={'class': 9016026, 'subclass': 2032079245})
        self.check_err(n.way(data, {u'railway': u'rail', u'workrules': u'BOStrab'}), expected={'class': 9016027, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE:BOStrab'}), expected={'class': 9016027, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE:EBO'}), expected={'class': 9016027, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE:ESBO'}), expected={'class': 9016027, 'subclass': 1085911640})
        self.check_err(n.way(data, {u'railway': u'rail', u'workrules': u'EBO'}), expected={'class': 9016027, 'subclass': 1085911640})
        self.check_err(n.way(data, {u'railway': u'rail', u'workrules': u'ESBO'}), expected={'class': 9016027, 'subclass': 1085911640})
        self.check_not_err(n.way(data, {u'railway': u'rail'}), expected={'class': 9016027, 'subclass': 1085911640})
        self.check_err(n.way(data, {u'railway': u'rail', u'workrules': u'BOA'}), expected={'class': 9016028, 'subclass': 219100574})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE:BOStrab'}), expected={'class': 9016028, 'subclass': 219100574})
        self.check_not_err(n.way(data, {u'railway': u'rail'}), expected={'class': 9016028, 'subclass': 219100574})
        self.check_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE-BOStrab'}), expected={'class': 9016029, 'subclass': 2059785415})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE:BOStrab'}), expected={'class': 9016029, 'subclass': 2059785415})
        self.check_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE-EBO'}), expected={'class': 9016029, 'subclass': 2020708529})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'workrules': u'DE:EBO'}), expected={'class': 9016029, 'subclass': 2020708529})
