#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_openrailwaymap(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9015001] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'Track tagged with usage=* AND service=* - remove one of these tags'}}
        self.errors[9015002] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'Station mapped as a way, but should be mapped as a node'}}
        self.errors[9015003] = {'item': 9015, 'level': 3, 'tag': [], 'desc': {'en': u'Track without operator'}}
        self.errors[9015004] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'Key traffic_mode is deprecated'}}
        self.errors[9015005] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'usage=freight is deprecated'}}
        self.errors[9015006] = {'item': 9015, 'level': 3, 'tag': [], 'desc': {'en': u'Track without workrules'}}
        self.errors[9015007] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'track numbers inside a station should be railway:track_ref, not name'}}
        self.errors[9015008] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'platforms should have the numbers in ref, not railway:track_ref'}}
        self.errors[9015009] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'track names or refs should not include the word \'track\', tag those numbers as railway:track_ref'}}
        self.errors[9015010] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'platform names or refs should not include the word \'track\', write that as \'description\', put the bare numbers in \'ref\', separated by \';\''}}
        self.errors[9015011] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'power:type=overhead is deprecated'}}
        self.errors[9015012] = {'item': 9015, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'power:type=overhead is deprecated, conflict between {0} and {1}', capture_tags, u'power:type=overhead', u'electrified=*')}
        self.errors[9015013] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'power:type is deprecated, change to proper electrified value'}}
        self.errors[9015014] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'priority on railway objects is deprecated, remove it'}}
        self.errors[9015015] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'tracks=1 not necessary if detail=track is tagged.'}}
        self.errors[9015016] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'If tracks are tagged with service=*, they should be mapped as one way per track.'}}
        self.errors[9015017] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'Crossings and level crossings should be mapped as nodes'}}
        self.errors[9015018] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'radio=GSM-R is deprecated'}}
        self.errors[9015019] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'radio=* is deprecated, change to proper railway:radio value'}}
        self.errors[9015020] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'track tagged with \'tunnel\' in name, consider using tunnel:name instead and put the track name into name'}}
        self.errors[9015021] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'track tagged with \'tunnel\' in wikipedia, consider using tunnel:wikipedia instead and put the track wikipedia entry into wikipedia'}}
        self.errors[9015022] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'track tagged with \'bridge\' in name, consider using bridge:name instead and put the track name into name'}}
        self.errors[9015023] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'track tagged with \'bridge\' in wikipedia, consider using bridge:wikipedia instead and put track wikipedia entry into wikipedia'}}
        self.errors[9015024] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'lanes=* is used for highways, not railways'}}
        self.errors[9015025] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'maxspeed=signals is deprecated, tag the highest possible speed instead'}}
        self.errors[9015026] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'maxspeed should contain the value as it is shown on the line with mph as unit'}}
        self.errors[9015027] = {'item': 9015, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0}={1} without {2}:railway', capture_tags, u'{0.key}', u'{0.value}', u'{0.value}')}
        self.errors[9015028] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'Milestone without position, add railway:position=*'}}
        self.errors[9015029] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'supervised=* is deprecated'}}
        self.errors[9015030] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'signal specification given but node is not tagged as signal or equivalent type'}}
        self.errors[9015031] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'A sign cannot have different states.'}}
        self.errors[9015032] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'railway=flat_crossing is deprecated'}}
        self.errors[9015033] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'railway:signal:stop:description is deprecated and has been replaced by railway:signal:stop:caption'}}
        self.errors[9015034] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'railway:signal:stop:description is deprecated, replace by appropiate railway:signal:stop:caption value'}}
        self.errors[9015035] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'main and combined signal at the same place'}}
        self.errors[9015036] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'signals should be tagged with ref, not railway:ref'}}
        self.errors[9015037] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'signals should have a railway:signal:direction=* tag'}}
        self.errors[9015038] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'signal names should be prefixed with an operator or country prefix'}}
        self.errors[9015039] = {'item': 9015, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} identification should be tagged as ref, not as name', capture_tags, u'{0.value}')}
        self.errors[9015040] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'Tagging for resetting switch is deprecated, change railway:switch=* to proper value'}}
        self.errors[9015041] = {'item': 9015, 'level': 2, 'tag': [], 'desc': {'en': u'controlled_area relations are deprecated'}}
        self.errors[9015042] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'interlocking relation without type=railway'}}
        self.errors[9015043] = {'item': 9015, 'level': 1, 'tag': [], 'desc': {'en': u'interlocking relation with type other than railway'}}

        self.re_066203d3 = re.compile(ur'^[0-9]+$')
        self.re_0e3375d5 = re.compile(ur'[Vv]iadu[ck]t')
        self.re_14388f34 = re.compile(ur'^[0-9]+[a-z]*.*')
        self.re_18e8cc14 = re.compile(ur'[Bb]rücke')
        self.re_25833d04 = re.compile(ur'[Bb]ridge')
        self.re_32cef8e4 = re.compile(ur'.+:.+')
        self.re_3d75a7eb = re.compile(ur'^[Vv]oie [0-9]+[a-z]*.*')
        self.re_4399527a = re.compile(ur';')
        self.re_473b08ca = re.compile(ur'^railway:signal:')
        self.re_4b2a9052 = re.compile(ur'^[Tt]rack [0-9]+[a-z]*.*')
        self.re_5bca804b = re.compile(ur'[Tt]unnel')
        self.re_61639c68 = re.compile(ur'^(passenger|mixed)$')
        self.re_63c39ff3 = re.compile(ur'^[0-9]+ mph$')
        self.re_7cf15856 = re.compile(ur'^[Gg]leis [0-9]+[a-z]*.*')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[railway=milestone][!railway:position]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'milestone' and not mapcss._tag_capture(capture_tags, 1, tags, u'railway:position'))):
            # throwWarning:"Milestone without position, add railway:position=*"
            # assertNoMatch:"node railway=milestone railway:position=42.0"
            # assertMatch:"node railway=milestone"
            err.append({'class': 9015028, 'subclass': 1237934683, 'text': {'en': u'Milestone without position, add railway:position=*'}})

        # node[railway=level_crossing][supervised]
        # node[railway=crossing][supervised]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'level_crossing' and mapcss._tag_capture(capture_tags, 1, tags, u'supervised')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'crossing' and mapcss._tag_capture(capture_tags, 1, tags, u'supervised'))):
            # suggestAlternative:"crossing:supervision"
            # throwWarning:"supervised=* is deprecated"
            # fixChangeKey:"supervised=>crossing:supervision"
            # assertMatch:"node railway=level_crossing supervised=yes"
            # assertNoMatch:"node railway=level_crossing"
            err.append({'class': 9015029, 'subclass': 321695123, 'text': {'en': u'supervised=* is deprecated'}, 'fix': {
                '+': dict([
                    [u'crossing:supervision', mapcss.tag(tags, u'supervised')]]),
                '-': ([
                    u'supervised'])
            }})

        # node[/^railway:signal:/][railway!=signal][railway!=buffer_stop][railway!=derail]
        if ((mapcss._tag_capture(capture_tags, 0, tags, self.re_473b08ca) and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'signal' and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != u'buffer_stop' and mapcss._tag_capture(capture_tags, 3, tags, u'railway') != u'derail')):
            # throwWarning:"signal specification given but node is not tagged as signal or equivalent type"
            # assertMatch:"node railway:signal:direction=forward"
            # assertMatch:"node railway:signal:position=right railway=level_crossing"
            # assertNoMatch:"node railway:signal:position=right railway=signal"
            # assertNoMatch:"node railway=buffer_stop railway:signal:minor=sh2"
            # assertNoMatch:"node railway=derail railway:signal:minor=sh"
            # assertNoMatch:"node railway=signal railway:signal:direction=forward"
            err.append({'class': 9015030, 'subclass': 908641862, 'text': {'en': u'signal specification given but node is not tagged as signal or equivalent type'}})

        # node[railway=signal]["railway:signal:main:form"=sign]["railway:signal:main:states"]
        # node[railway=signal]["railway:signal:distant:form"=sign]["railway:signal:distant:states"]
        # node[railway=signal]["railway:signal:combined:form"=sign]["railway:signal:combined:states"]
        # node[railway=signal]["railway:signal:shunting:form"=sign]["railway:signal:shunting:states"]
        # node[railway=signal]["railway:signal:main_repeated:form"=sign]["railway:signal:main_repeated:states"]
        # node[railway=signal]["railway:signal:minor:form"=sign]["railway:signal:minor:states"]
        # node[railway=signal]["railway:signal:minor_distant:form"=sign]["railway:signal:minor_distant:states"]
        # node[railway=signal]["railway:signal:crossing:form"=sign]["railway:signal:crossing:states"]
        # node[railway=signal]["railway:signal:crossing_distant:form"=sign]["railway:signal:crossing_distant:states"]
        # node[railway=signal]["railway:signal:humping:form"=sign]["railway:signal:humping:states"]
        # node[railway=signal]["railway:signal:speed_limit:form"=sign]["railway:signal:speed_limit:speed"=~/;/]
        # node[railway=signal]["railway:signal:speed_limit_distant:form"=sign]["railway:signal:speed_limit_distant:speed"=~/;/]
        # node[railway=signal]["railway:signal:route:form"=sign]["railway:signal:route:states"]
        # node[railway=signal]["railway:signal:route_distant:form"=sign]["railway:signal:route_distant:states"]
        # node[railway=signal]["railway:signal:wrong_road:form"=sign]["railway:signal:wrong_road:states"]
        # node[railway=signal]["railway:signal:stop_demand:form"=sign]["railway:signal:stop_demand:states"]
        # node[railway=signal]["railway:signal:departure:form"=sign]["railway:signal:departure:states"]
        # node[railway=signal]["railway:signal:resetting_switch:form"=sign]["railway:signal:resetting_switch:states"]
        # node[railway=signal]["railway:signal:short_route:form"=sign]["railway:signal:short_route:states"]
        # node[railway=signal]["railway:signal:brake_test:form"=sign]["railway:signal:brake_test:states"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:combined:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:combined:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:shunting:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:shunting:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main_repeated:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main_repeated:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:minor:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:minor:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:minor_distant:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:minor_distant:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:crossing:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:crossing:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:crossing_distant:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:crossing_distant:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:humping:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:humping:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit:form') == u'sign' and mapcss.regexp_test_(self.re_4399527a, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit:speed'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit_distant:form') == u'sign' and mapcss.regexp_test_(self.re_4399527a, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit_distant:speed'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:route:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:route:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:route_distant:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:route_distant:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:wrong_road:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:wrong_road:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:stop_demand:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:stop_demand:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:departure:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:departure:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:resetting_switch:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:resetting_switch:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:short_route:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:short_route:states')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:brake_test:form') == u'sign' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:brake_test:states'))):
            # throwError:"A sign cannot have different states."
            # assertNoMatch:"node railway=signal railway:signal:main:states=hp0;hp1 railway:signal:main:form=light"
            # assertNoMatch:"node railway=signal railway:signal:main:states=hp0;hp1 railway:signal:main:form=semaphore"
            # assertMatch:"node railway=signal railway:signal:main:states=hp0;hp1 railway:signal:main:form=sign"
            # assertNoMatch:"node railway=signal railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=80"
            # assertMatch:"node railway=signal railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=80;90"
            err.append({'class': 9015031, 'subclass': 285269206, 'text': {'en': u'A sign cannot have different states.'}})

        # node[railway][priority]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'priority'))):
            # throwError:"priority on railway objects is deprecated, remove it"
            # fixRemove:"priority"
            # assertMatch:"node railway=buffer_stop priority=yard"
            err.append({'class': 9015014, 'subclass': 1264446053, 'text': {'en': u'priority on railway objects is deprecated, remove it'}, 'fix': {
                '-': ([
                    u'priority'])
            }})

        # node[railway=flat_crossing]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'flat_crossing')):
            # throwError:"railway=flat_crossing is deprecated"
            # suggestAlternative:"railway=railway_crossing"
            # fixAdd:"railway=railway_crossing"
            # assertNoMatch:"node railway=crossing"
            # assertMatch:"node railway=flat_crossing"
            # assertNoMatch:"node railway=railway_crossing"
            err.append({'class': 9015032, 'subclass': 719449462, 'text': {'en': u'railway=flat_crossing is deprecated'}, 'fix': {
                '+': dict([
                    [u'railway',u'railway_crossing']])
            }})

        # node[railway:signal:stop:description][!railway:signal:stop:caption]
        if (u'railway:signal:stop:description' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:stop:description') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:stop:caption'))):
            # suggestAlternative:"railway:signal:stop:caption"
            # throwWarning:"railway:signal:stop:description is deprecated and has been replaced by railway:signal:stop:caption"
            # fixChangeKey:"railway:signal:stop:description=>railway:signal:stop:caption"
            # assertNoMatch:"node railway=signal railway:signal:stop:caption=70"
            # assertNoMatch:"node railway=signal railway:signal:stop:description=70 railway:signal:stop:caption=70"
            # assertMatch:"node railway=signal railway:signal:stop:description=70"
            err.append({'class': 9015033, 'subclass': 1175712267, 'text': {'en': u'railway:signal:stop:description is deprecated and has been replaced by railway:signal:stop:caption'}, 'fix': {
                '+': dict([
                    [u'railway:signal:stop:caption', mapcss.tag(tags, u'railway:signal:stop:description')]]),
                '-': ([
                    u'railway:signal:stop:description'])
            }})

        # node[railway:signal:stop:description][railway:signal:stop:caption]
        if (u'railway:signal:stop:description' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:stop:description') and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:stop:caption'))):
            # throwWarning:"railway:signal:stop:description is deprecated, replace by appropiate railway:signal:stop:caption value"
            # assertNoMatch:"node railway=signal railway:signal:stop:caption=70"
            # assertMatch:"node railway=signal railway:signal:stop:description=70 railway:signal:stop:caption=70"
            # assertNoMatch:"node railway=signal railway:signal:stop:description=70"
            err.append({'class': 9015034, 'subclass': 1820225369, 'text': {'en': u'railway:signal:stop:description is deprecated, replace by appropiate railway:signal:stop:caption value'}})

        # node["railway:signal:combined"]["railway:signal:main"]
        if (u'railway:signal:combined' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:combined') and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main'))):
            # throwError:"main and combined signal at the same place"
            # assertMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:main=DE-ESO:hp"
            # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:minor=DE-ESO:sh1"
            # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp"
            err.append({'class': 9015035, 'subclass': 371617473, 'text': {'en': u'main and combined signal at the same place'}})

        # node["railway:signal:combined"]["railway:signal:distant"]
        if (u'railway:signal:combined' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway:signal:combined') and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant'))):
            # throwError:"main and combined signal at the same place"
            # assertMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:distant=DE-ESO:vr"
            # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:minor=DE-ESO:sh1"
            # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp"
            err.append({'class': 9015035, 'subclass': 570327409, 'text': {'en': u'main and combined signal at the same place'}})

        # node[railway=signal]["railway:ref"][!ref]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:ref') and not mapcss._tag_capture(capture_tags, 2, tags, u'ref'))):
            # suggestAlternative:"ref"
            # throwError:"signals should be tagged with ref, not railway:ref"
            # fixChangeKey:"railway:ref=>ref"
            # assertNoMatch:"node railway=signal railway:ref=N1 ref=N1"
            # assertMatch:"node railway=signal railway:ref=N1"
            # assertNoMatch:"node railway=signal ref=N1"
            err.append({'class': 9015036, 'subclass': 257553969, 'text': {'en': u'signals should be tagged with ref, not railway:ref'}, 'fix': {
                '+': dict([
                    [u'ref', mapcss.tag(tags, u'railway:ref')]]),
                '-': ([
                    u'railway:ref'])
            }})

        # node[railway=signal]["railway:ref"][ref]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:ref') and mapcss._tag_capture(capture_tags, 2, tags, u'ref'))):
            # suggestAlternative:"ref"
            # throwError:"signals should be tagged with ref, not railway:ref"
            # fixChangeKey:"railway:ref=>ref"
            # assertMatch:"node railway=signal railway:ref=N1 ref=N1"
            # assertNoMatch:"node railway=signal railway:ref=N1"
            # assertNoMatch:"node railway=signal ref=N1"
            err.append({'class': 9015036, 'subclass': 1443995005, 'text': {'en': u'signals should be tagged with ref, not railway:ref'}, 'fix': {
                '+': dict([
                    [u'ref', mapcss.tag(tags, u'railway:ref')]]),
                '-': ([
                    u'railway:ref'])
            }})

        # node[railway=signal][!"railway:signal:direction"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and not mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:direction'))):
            # throwError:"signals should have a railway:signal:direction=* tag"
            # assertNoMatch:"node railway=signal railway:signal:direction=forward"
            # assertMatch:"node railway=signal"
            err.append({'class': 9015037, 'subclass': 1288245325, 'text': {'en': u'signals should have a railway:signal:direction=* tag'}})

        # node[railway=signal]["railway:signal:main"]["railway:signal:main"!~/.+:.+/]
        # node[railway=signal]["railway:signal:combined"]["railway:signal:combined"!~/.+:.+/]
        # node[railway=signal]["railway:signal:distant"]["railway:signal:distant"!~/.+:.+/]
        # node[railway=signal]["railway:signal:shunting"]["railway:signal:shunting"!~/.+:.+/]
        # node[railway=signal]["railway:signal:main_repeated"]["railway:signal:main_repeated"!~/.+:.+/]
        # node[railway=signal]["railway:signal:minor"]["railway:signal:minor"!~/.+:.+/]
        # node[railway=signal]["railway:signal:minor_distant"]["railway:signal:minor_distant"!~/.+:.+/]
        # node[railway=signal]["railway:signal:crossing"]["railway:signal:crossing"!~/.+:.+/]
        # node[railway=signal]["railway:signal:crossing_distant"]["railway:signal:crossing_distant"!~/.+:.+/]
        # node[railway=signal]["railway:signal:humping"]["railway:signal:humping"!~/.+:.+/]
        # node[railway=signal]["railway:signal:speed_limit"]["railway:signal:speed_limit"!~/.+:.+/]
        # node[railway=signal]["railway:signal:speed_limit_distant"]["railway:signal:speed_limit_distant"!~/.+:.+/]
        # node[railway=signal]["railway:signal:route"]["railway:signal:route"!~/.+:.+/]
        # node[railway=signal]["railway:signal:route_distant"]["railway:signal:route_distant"!~/.+:.+/]
        # node[railway=signal]["railway:signal:wrong_road"]["railway:signal:wrong_road"!~/.+:.+/]
        # node[railway=signal]["railway:signal:stop_demand"]["railway:signal:stop_demand"!~/.+:.+/]
        # node[railway=signal]["railway:signal:departure"]["railway:signal:departure"!~/.+:.+/]
        # node[railway=signal]["railway:signal:resetting_switch"]["railway:signal:resetting_switch"!~/.+:.+/]
        # node[railway=signal]["railway:signal:short_route"]["railway:signal:short_route"!~/.+:.+/]
        # node[railway=signal]["railway:signal:brake_test"]["railway:signal:brake_test"!~/.+:.+/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:combined') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:combined'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:distant') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:distant'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:shunting') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:shunting'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:main_repeated') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:main_repeated'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:minor') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:minor'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:minor_distant') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:minor_distant'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:crossing') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:crossing'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:crossing_distant') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:crossing_distant'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:humping') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:humping'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:speed_limit_distant') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:speed_limit_distant'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:route') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:route'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:route_distant') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:route_distant'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:wrong_road') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:wrong_road'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:stop_demand') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:stop_demand'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:departure') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:departure'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:resetting_switch') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:resetting_switch'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:short_route') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:short_route'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:signal:brake_test') and not mapcss.regexp_test_(self.re_32cef8e4, mapcss._tag_capture(capture_tags, 2, tags, u'railway:signal:brake_test')))):
            # throwWarning:"signal names should be prefixed with an operator or country prefix"
            # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks"
            # assertMatch:"node railway=signal railway:signal:combined=ks"
            # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:ks"
            # assertMatch:"node railway=signal railway:signal:distant=vr"
            # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:ks"
            # assertMatch:"node railway=signal railway:signal:main=ks"
            # assertNoMatch:"node railway=signal railway:signal:route=DE-ESO:zs2"
            # assertMatch:"node railway=signal railway:signal:route=zs2"
            err.append({'class': 9015038, 'subclass': 946563032, 'text': {'en': u'signal names should be prefixed with an operator or country prefix'}})

        # node[railway=signal][name][!ref]
        # node[railway=signal][name][ref=*name]
        # node[railway=switch][name][!ref]
        # node[railway=switch][name][ref=*name]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'ref')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'signal' and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') == mapcss.tag(tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'switch' and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'ref')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'switch' and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') == mapcss.tag(tags, u'name'))):
            # throwWarning:tr("{0} identification should be tagged as ref, not as name","{0.value}")
            # suggestAlternative:"ref"
            # fixChangeKey:"name=>ref"
            # assertMatch:"node railway=signal name=FF ref=FF"
            # assertMatch:"node railway=signal name=FF"
            # assertNoMatch:"node railway=signal ref=FF name=GG"
            # assertNoMatch:"node railway=signal ref=FF"
            # assertMatch:"node railway=switch name=12 ref=12"
            # assertMatch:"node railway=switch name=12"
            # assertNoMatch:"node railway=switch ref=12 name=13"
            # assertNoMatch:"node railway=switch ref=12"
            err.append({'class': 9015039, 'subclass': 1244137190, 'text': mapcss.tr(u'{0} identification should be tagged as ref, not as name', capture_tags, u'{0.value}'), 'fix': {
                '+': dict([
                    [u'ref', mapcss.tag(tags, u'name')]]),
                '-': ([
                    u'name'])
            }})

        # node[railway=switch]["railway:switch"=resetting]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'switch' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:switch') == u'resetting')):
            # throwError:"Tagging for resetting switch is deprecated, change railway:switch=* to proper value"
            # suggestAlternative:"railway:switch + railway:switch:resetting=yes"
            # fixAdd:"railway:switch:resetting=yes"
            # assertNoMatch:"node railway=switch railway:switch=default railway:switch:resetting=yes"
            # assertNoMatch:"node railway=switch railway:switch=default"
            # assertMatch:"node railway=switch railway:switch=resetting ref=2"
            # assertNoMatch:"node railway=switch"
            err.append({'class': 9015040, 'subclass': 967663151, 'text': {'en': u'Tagging for resetting switch is deprecated, change railway:switch=* to proper value'}, 'fix': {
                '+': dict([
                    [u'railway:switch:resetting',u'yes']])
            }})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[railway][usage][usage!=industrial][usage!=military][service]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'usage') and mapcss._tag_capture(capture_tags, 2, tags, u'usage') != u'industrial' and mapcss._tag_capture(capture_tags, 3, tags, u'usage') != u'military' and mapcss._tag_capture(capture_tags, 4, tags, u'service'))):
            # throwError:"Track tagged with usage=* AND service=* - remove one of these tags"
            # fixRemove:"service"
            # assertNoMatch:"way railway=rail service=siding"
            # assertNoMatch:"way railway=rail usage=industrial service=yard"
            # assertMatch:"way railway=rail usage=main service=siding"
            # assertNoMatch:"way railway=rail usage=main"
            # assertNoMatch:"way railway=rail usage=military service=yard"
            err.append({'class': 9015001, 'subclass': 1888453557, 'text': {'en': u'Track tagged with usage=* AND service=* - remove one of these tags'}, 'fix': {
                '-': ([
                    u'service'])
            }})

        # way[railway=station]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'station')):
            # throwError:"Station mapped as a way, but should be mapped as a node"
            # assertMatch:"way railway=station"
            err.append({'class': 9015002, 'subclass': 1498103253, 'text': {'en': u'Station mapped as a way, but should be mapped as a node'}})

        # way[railway][!operator]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and not mapcss._tag_capture(capture_tags, 1, tags, u'operator'))):
            # throwOther:"Track without operator"
            # assertNoMatch:"way railway=rail operator=SNCF"
            # assertMatch:"way railway=rail"
            err.append({'class': 9015003, 'subclass': 1686027167, 'text': {'en': u'Track without operator'}})

        # way[railway][traffic_mode]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'traffic_mode'))):
            # throwError:"Key traffic_mode is deprecated"
            # suggestAlternative:"railway:traffic_mode"
            # fixChangeKey:"traffic_mode=>railway:traffic_mode"
            # assertNoMatch:"way railway=rail railway:traffic_mode=passenger"
            # assertMatch:"way railway=rail traffic_mode=passenger"
            # assertNoMatch:"way railway=rail"
            err.append({'class': 9015004, 'subclass': 1755442170, 'text': {'en': u'Key traffic_mode is deprecated'}, 'fix': {
                '+': dict([
                    [u'railway:traffic_mode', mapcss.tag(tags, u'traffic_mode')]]),
                '-': ([
                    u'traffic_mode'])
            }})

        # way[railway][usage=freight][!railway:traffic_mode]
        # way[railway][usage=freight][railway:traffic_mode=freight]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'usage') == u'freight' and not mapcss._tag_capture(capture_tags, 2, tags, u'railway:traffic_mode')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'usage') == u'freight' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:traffic_mode') == u'freight')):
            # suggestAlternative:"railway:traffic_mode=freight"
            # throwError:"usage=freight is deprecated"
            # fixChangeKey:"usage=>railway:traffic_mode"
            # assertNoMatch:"way railway=rail railway:traffic_mode"
            # assertNoMatch:"way railway=rail usage=branch"
            # assertMatch:"way railway=rail usage=freight railway:traffic_mode=freight"
            # assertMatch:"way railway=rail usage=freight"
            # assertNoMatch:"way railway=rail usage=industrial"
            # assertNoMatch:"way railway=rail usage=main"
            err.append({'class': 9015005, 'subclass': 331669407, 'text': {'en': u'usage=freight is deprecated'}, 'fix': {
                '+': dict([
                    [u'railway:traffic_mode', mapcss.tag(tags, u'usage')]]),
                '-': ([
                    u'usage'])
            }})

        # way[railway][usage=freight][railway:traffic_mode=~/^(passenger|mixed)$/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'usage') == u'freight' and mapcss.regexp_test_(self.re_61639c68, mapcss._tag_capture(capture_tags, 2, tags, u'railway:traffic_mode')))):
            # suggestAlternative:"railway:traffic_mode=mixed"
            # throwError:"usage=freight is deprecated"
            # fixAdd:"railway:traffic_mode=mixed"
            # fixRemove:"usage"
            # assertNoMatch:"way railway=rail usage=freight 'railway:traffic_mode'=freight"
            # assertNoMatch:"way railway=rail railway:traffic_mode"
            # assertNoMatch:"way railway=rail usage=branch"
            # assertMatch:"way railway=rail usage=freight railway:traffic_mode=mixed"
            # assertMatch:"way railway=rail usage=freight railway:traffic_mode=passenger"
            # assertNoMatch:"way railway=rail usage=industrial"
            # assertNoMatch:"way railway=rail usage=main"
            err.append({'class': 9015005, 'subclass': 1212704987, 'text': {'en': u'usage=freight is deprecated'}, 'fix': {
                '+': dict([
                    [u'railway:traffic_mode',u'mixed']]),
                '-': ([
                    u'usage'])
            }})

        # way[railway][railway!=platform][!workrules]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and not mapcss._tag_capture(capture_tags, 2, tags, u'workrules'))):
            # throwOther:"Track without workrules"
            # assertNoMatch:"way railway=rail workrules=EBO"
            # assertMatch:"way railway=rail"
            err.append({'class': 9015006, 'subclass': 1310604175, 'text': {'en': u'Track without workrules'}})

        # way[railway][railway!=platform][name=~/^[0-9]+[a-z]*.*/]["railway:track_ref"=*name]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_14388f34, mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss._tag_capture(capture_tags, 3, tags, u'railway:track_ref') == mapcss.tag(tags, u'name'))):
            # suggestAlternative:"railway:track_ref"
            # throwError:"track numbers inside a station should be railway:track_ref, not name"
            # fixRemove:"name"
            # assertMatch:"way railway=light_rail name=14 railway:track_ref=14"
            # assertNoMatch:"way railway=rail name=\"Gleis 14b\" railway:track_ref=14b"
            # assertNoMatch:"way railway=rail name=\"Gleis 14b\""
            # assertMatch:"way railway=rail name=14b railway:track_ref=14b"
            # assertNoMatch:"way railway=rail name=3"
            # assertMatch:"way railway=rail name=4 railway:track_ref=4"
            # assertMatch:"way railway=rail name=4a railway:track_ref=4a"
            err.append({'class': 9015007, 'subclass': 2091521035, 'text': {'en': u'track numbers inside a station should be railway:track_ref, not name'}, 'fix': {
                '-': ([
                    u'name'])
            }})

        # way[railway][railway!=platform][name=~/^[0-9]+[a-z]*.*/][!"railway:track_ref"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_14388f34, mapcss._tag_capture(capture_tags, 2, tags, u'name')) and not mapcss._tag_capture(capture_tags, 3, tags, u'railway:track_ref'))):
            # suggestAlternative:"railway:track_ref"
            # throwError:"track numbers inside a station should be railway:track_ref, not name"
            # fixChangeKey:"name=>railway:track_ref"
            # assertMatch:"way railway=light_rail name=14"
            # assertNoMatch:"way railway=platform name=3"
            # assertNoMatch:"way railway=rail name=\"Gleis 14b\""
            # assertNoMatch:"way railway=rail name=\"track 4b\""
            # assertMatch:"way railway=rail name=14b"
            # assertMatch:"way railway=rail name=4"
            # assertMatch:"way railway=rail name=4a"
            err.append({'class': 9015007, 'subclass': 85438379, 'text': {'en': u'track numbers inside a station should be railway:track_ref, not name'}, 'fix': {
                '+': dict([
                    [u'railway:track_ref', mapcss.tag(tags, u'name')]]),
                '-': ([
                    u'name'])
            }})

        # way[railway=platform]["railway:track_ref"][!ref]
        # way[railway=platform]["railway:track_ref"]["railway:track_ref"=*ref]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:track_ref') and not mapcss._tag_capture(capture_tags, 2, tags, u'ref')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:track_ref') and mapcss._tag_capture(capture_tags, 2, tags, u'railway:track_ref') == mapcss.tag(tags, u'ref'))):
            # throwError:"platforms should have the numbers in ref, not railway:track_ref"
            # suggestAlternative:"ref"
            # fixChangeKey:"railway:track_ref=>ref"
            # assertMatch:"way railway=platform railway:track_ref=3 ref=3"
            # assertNoMatch:"way railway=platform railway:track_ref=3 ref=4"
            # assertMatch:"way railway=platform railway:track_ref=3"
            # assertNoMatch:"way railway=rail railway:track_ref=3"
            err.append({'class': 9015008, 'subclass': 226422824, 'text': {'en': u'platforms should have the numbers in ref, not railway:track_ref'}, 'fix': {
                '+': dict([
                    [u'ref', mapcss.tag(tags, u'railway:track_ref')]]),
                '-': ([
                    u'railway:track_ref'])
            }})

        # way[railway=platform]["railway:track_ref"]["ref"]["railway:track_ref"!=*ref]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'railway:track_ref') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss._tag_capture(capture_tags, 3, tags, u'railway:track_ref') != mapcss.tag(tags, u'ref'))):
            # throwError:"platforms should have the numbers in ref, not railway:track_ref"
            # assertNoMatch:"way railway=platform railway:track_ref=3 ref=3"
            # assertMatch:"way railway=platform railway:track_ref=3 ref=4"
            # assertNoMatch:"way railway=platform railway:track_ref=3"
            # assertNoMatch:"way railway=rail railway:track_ref=3"
            err.append({'class': 9015008, 'subclass': 1676742857, 'text': {'en': u'platforms should have the numbers in ref, not railway:track_ref'}})

        # way[railway][railway!=platform][name=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform]["name:de"=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][name=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][name=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform]["name:fr"=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][ref=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][ref=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][ref=~/^[Vv]oie [0-9]+[a-z]*.*/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'name:de'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'name:fr'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 2, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') != u'platform' and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'ref')))):
            # throwError:"track names or refs should not include the word 'track', tag those numbers as railway:track_ref"
            # assertMatch:"way railway=rail name=\"Gleis 14b\""
            # assertNoMatch:"way railway=rail name=14b"
            # assertMatch:"way railway=rail ref=\"track 4b\""
            err.append({'class': 9015009, 'subclass': 1420092530, 'text': {'en': u'track names or refs should not include the word \'track\', tag those numbers as railway:track_ref'}})

        # way[railway=platform][!description][name=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][!description]["name:de"=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][!description][name=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][!description][name=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][!description]["name:fr"=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][!description][ref=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][!description][ref=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][!description][ref=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*name][name=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*"name:de"]["name:de"=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*name][name=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*name][name=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*"name:fr"]["name:fr"=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*ref][ref=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*ref][ref=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][description=*ref][ref=~/^[Vv]oie [0-9]+[a-z]*.*/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'name:de'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'name:fr'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 2, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'name') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'name:de') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'name:de'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'name') and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'name') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'name:fr') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'name:fr'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'ref') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 2, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'ref') and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 2, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') == mapcss.tag(tags, u'ref') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 2, tags, u'ref')))):
            # throwError:"platform names or refs should not include the word 'track', write that as 'description', put the bare numbers in 'ref', separated by ';'"
            # suggestAlternative:"description"
            # fixChangeKey:"{2.key}=>description"
            # assertMatch:"way railway=platform name=\"Gleis 14b\" description=\"Gleis 14b\""
            # assertMatch:"way railway=platform name=\"Gleis 14b\""
            # assertNoMatch:"way railway=platform name=14b description=other"
            # assertNoMatch:"way railway=platform name=14b"
            # assertMatch:"way railway=platform ref=\"track 4b\" ref=\"track 4b\""
            # assertMatch:"way railway=platform ref=\"track 4b\""
            # assertNoMatch:"way railway=rail name=14b"
            err.append({'class': 9015010, 'subclass': 1156420508, 'text': {'en': u'platform names or refs should not include the word \'track\', write that as \'description\', put the bare numbers in \'ref\', separated by \';\''}, 'fix': {
                '+': dict([
                    [u'description', mapcss.tag(tags, u'{2.key}')]]),
                '-': ([
                    u'{2.key}'])
            }})

        # way[railway=platform][description][description!=*name][name=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*"name:de"]["name:de"=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*name][name=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*name][name=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*"name:fr"]["name:fr"=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*ref][ref=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*ref][ref=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*ref][ref=~/^[Vv]oie [0-9]+[a-z]*.*/]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'name') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 3, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'name:de') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 3, tags, u'name:de'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'name') and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 3, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'name') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 3, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'name:fr') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 3, tags, u'name:fr'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'ref') and mapcss.regexp_test_(self.re_7cf15856, mapcss._tag_capture(capture_tags, 3, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'ref') and mapcss.regexp_test_(self.re_4b2a9052, mapcss._tag_capture(capture_tags, 3, tags, u'ref'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'description') and mapcss._tag_capture(capture_tags, 2, tags, u'description') != mapcss.tag(tags, u'ref') and mapcss.regexp_test_(self.re_3d75a7eb, mapcss._tag_capture(capture_tags, 3, tags, u'ref')))):
            # throwError:"platform names or refs should not include the word 'track', write that as 'description', put the bare numbers in 'ref', separated by ';'"
            # assertMatch:"way railway=platform name=\"Gleis 14b\" description=other"
            # assertNoMatch:"way railway=platform name=14b description=14b"
            # assertNoMatch:"way railway=platform name=14b"
            # assertMatch:"way railway=platform ref=\"track 4b\" description=other"
            err.append({'class': 9015010, 'subclass': 1149450895, 'text': {'en': u'platform names or refs should not include the word \'track\', write that as \'description\', put the bare numbers in \'ref\', separated by \';\''}})

        # way[railway]["power:type"=overhead][electrified=contact_line]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'power:type') == u'overhead' and mapcss._tag_capture(capture_tags, 2, tags, u'electrified') == u'contact_line')):
            # suggestAlternative:"electrified=contact_line"
            # throwError:"power:type=overhead is deprecated"
            # fixRemove:"power:type"
            # assertMatch:"way railway=rail power:type=overhead electrified=contact_line"
            # assertNoMatch:"way railway=rail power:type=overhead electrified=something"
            err.append({'class': 9015011, 'subclass': 1012477221, 'text': {'en': u'power:type=overhead is deprecated'}, 'fix': {
                '-': ([
                    u'power:type'])
            }})

        # way[railway]["power:type"=overhead][electrified=yes]
        # way[railway]["power:type"=overhead][!electrified]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'power:type') == u'overhead' and mapcss._tag_capture(capture_tags, 2, tags, u'electrified') == u'yes') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'power:type') == u'overhead' and not mapcss._tag_capture(capture_tags, 2, tags, u'electrified'))):
            # suggestAlternative:"electrified=contact_line"
            # throwError:"power:type=overhead is deprecated"
            # fixAdd:"electrified=contact_line"
            # fixRemove:"power:type"
            # assertNoMatch:"way railway=rail power:type=overhead electrified=something"
            # assertMatch:"way railway=rail power:type=overhead electrified=yes"
            # assertMatch:"way railway=rail power:type=overhead"
            err.append({'class': 9015011, 'subclass': 1909233042, 'text': {'en': u'power:type=overhead is deprecated'}, 'fix': {
                '+': dict([
                    [u'electrified',u'contact_line']]),
                '-': ([
                    u'power:type'])
            }})

        # way[railway]["power:type"=overhead][electrified][electrified!=yes][electrified!=contact_line]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'power:type') == u'overhead' and mapcss._tag_capture(capture_tags, 2, tags, u'electrified') and mapcss._tag_capture(capture_tags, 3, tags, u'electrified') != u'yes' and mapcss._tag_capture(capture_tags, 4, tags, u'electrified') != u'contact_line')):
            # throwError:tr("power:type=overhead is deprecated, conflict between {0} and {1}","power:type=overhead","electrified=*")
            # assertMatch:"way railway=rail power:type=overhead electrified=other"
            # assertNoMatch:"way railway=rail power:type=overhead electrified=yes"
            err.append({'class': 9015012, 'subclass': 1465196539, 'text': mapcss.tr(u'power:type=overhead is deprecated, conflict between {0} and {1}', capture_tags, u'power:type=overhead', u'electrified=*')})

        # way[railway]["power:type"]["power:type"!=overhead][electrified]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'power:type') and mapcss._tag_capture(capture_tags, 2, tags, u'power:type') != u'overhead' and mapcss._tag_capture(capture_tags, 3, tags, u'electrified'))):
            # throwError:"power:type is deprecated, change to proper electrified value"
            # assertNoMatch:"way railway=rail power:type=overhead electrified=yes"
            # assertMatch:"way railway=rail power:type=something electrified=yes"
            err.append({'class': 9015013, 'subclass': 356393984, 'text': {'en': u'power:type is deprecated, change to proper electrified value'}})

        # way[railway]["power:type"]["power:type"!=overhead][!electrified]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'power:type') and mapcss._tag_capture(capture_tags, 2, tags, u'power:type') != u'overhead' and not mapcss._tag_capture(capture_tags, 3, tags, u'electrified'))):
            # throwError:"power:type is deprecated, change to proper electrified value"
            # assertNoMatch:"way railway=rail power:type=overhead electrified=yes"
            # assertMatch:"way railway=rail power:type=something"
            err.append({'class': 9015013, 'subclass': 410100568, 'text': {'en': u'power:type is deprecated, change to proper electrified value'}})

        # way[railway][priority]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'priority'))):
            # throwError:"priority on railway objects is deprecated, remove it"
            # fixRemove:"priority"
            # assertNoMatch:"way highway=primary priority=primary"
            # assertMatch:"way railway=rail priority=primary service=siding"
            # assertMatch:"way railway=rail priority=primary usage=main"
            # assertMatch:"way railway=rail priority=primary"
            err.append({'class': 9015014, 'subclass': 2122288452, 'text': {'en': u'priority on railway objects is deprecated, remove it'}, 'fix': {
                '-': ([
                    u'priority'])
            }})

        # way[railway][tracks=1][detail=track]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'tracks') == 1 and mapcss._tag_capture(capture_tags, 2, tags, u'detail') == u'track')):
            # suggestAlternative:"detail=track"
            # throwWarning:"tracks=1 not necessary if detail=track is tagged."
            # fixRemove:"tracks"
            # assertNoMatch:"way railway=rail tracks=1 detail!=track"
            # assertMatch:"way railway=rail tracks=1 detail=track"
            # assertNoMatch:"way railway=rail tracks=2 detail=track"
            err.append({'class': 9015015, 'subclass': 986004687, 'text': {'en': u'tracks=1 not necessary if detail=track is tagged.'}, 'fix': {
                '-': ([
                    u'tracks'])
            }})

        # way[railway][tracks!=1][tracks][service]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'tracks') != 1 and mapcss._tag_capture(capture_tags, 2, tags, u'tracks') and mapcss._tag_capture(capture_tags, 3, tags, u'service'))):
            # throwWarning:"If tracks are tagged with service=*, they should be mapped as one way per track."
            # assertNoMatch:"way railway=rail tracks=1"
            # assertMatch:"way railway=rail tracks=2 service=foo"
            # assertNoMatch:"way railway=rail tracks=2 usage=bar"
            err.append({'class': 9015016, 'subclass': 256757521, 'text': {'en': u'If tracks are tagged with service=*, they should be mapped as one way per track.'}})

        # way[railway=crossing]
        # way[railway=level_crossing]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'crossing') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'level_crossing')):
            # throwError:"Crossings and level crossings should be mapped as nodes"
            # assertMatch:"way railway=crossing railway:position:exact=2.4"
            # assertMatch:"way railway=level_crossing railway:position:exact=2.4"
            err.append({'class': 9015017, 'subclass': 2146160181, 'text': {'en': u'Crossings and level crossings should be mapped as nodes'}})

        # way[railway][radio="GSM-R"][!"railway:radio"]
        # way[railway][radio="GSM-R"]["railway:radio"="gsm-r"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'radio') == u'GSM-R' and not mapcss._tag_capture(capture_tags, 2, tags, u'railway:radio')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'radio') == u'GSM-R' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:radio') == u'gsm-r')):
            # throwWarning:"radio=GSM-R is deprecated"
            # suggestAlternative:"railway:radio=gsm-r"
            # fixRemove:"radio"
            # fixAdd:"railway:radio=gsm-r"
            # assertNoMatch:"way railway=rail radio=\"GSM\""
            # assertNoMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm\""
            # assertMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm-r\""
            # assertMatch:"way railway=rail radio=\"GSM-R\""
            err.append({'class': 9015018, 'subclass': 2078132492, 'text': {'en': u'radio=GSM-R is deprecated'}, 'fix': {
                '+': dict([
                    [u'railway:radio',u'gsm-r']]),
                '-': ([
                    u'radio'])
            }})

        # way[railway][radio="GSM-R"]["railway:radio"]["railway:radio"!="gsm-r"]
        # way[railway][radio][radio!="GSM-R"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'radio') == u'GSM-R' and mapcss._tag_capture(capture_tags, 2, tags, u'railway:radio') and mapcss._tag_capture(capture_tags, 3, tags, u'railway:radio') != u'gsm-r') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'radio') and mapcss._tag_capture(capture_tags, 2, tags, u'radio') != u'GSM-R')):
            # throwWarning:"radio=* is deprecated, change to proper railway:radio value"
            # assertMatch:"way railway=rail radio=\"GSM\""
            # assertMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm\""
            # assertNoMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm-r\""
            # assertNoMatch:"way railway=rail radio=\"GSM-R\""
            err.append({'class': 9015019, 'subclass': 406318522, 'text': {'en': u'radio=* is deprecated, change to proper railway:radio value'}})

        # way[railway][name=~/[Tt]unnel/][!"tunnel:name"]
        # way[railway][name=~/[Tt]unnel/]["tunnel:name"=*name]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_5bca804b, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel:name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_5bca804b, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'tunnel:name') == mapcss.tag(tags, u'name'))):
            # throwWarning:"track tagged with 'tunnel' in name, consider using tunnel:name instead and put the track name into name"
            # suggestAlternative:"tunnel:name"
            # fixChangeKey:"name=>tunnel:name"
            # assertMatch:"way railway=light_rail name=Bartunnel tunnel:name=Bartunnel"
            # assertMatch:"way railway=rail name=Footunnel"
            # assertNoMatch:"way railway=rail tunnel:name=Baztunnel"
            err.append({'class': 9015020, 'subclass': 843755814, 'text': {'en': u'track tagged with \'tunnel\' in name, consider using tunnel:name instead and put the track name into name'}, 'fix': {
                '+': dict([
                    [u'tunnel:name', mapcss.tag(tags, u'name')]]),
                '-': ([
                    u'name'])
            }})

        # way[railway][wikipedia=~/[Tt]unnel/][!"tunnel:wikipedia"]
        # way[railway][wikipedia=~/[Tt]unnel/]["tunnel:wikipedia"=*wikipedia]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_5bca804b, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel:wikipedia')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_5bca804b, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and mapcss._tag_capture(capture_tags, 2, tags, u'tunnel:wikipedia') == mapcss.tag(tags, u'wikipedia'))):
            # throwWarning:"track tagged with 'tunnel' in wikipedia, consider using tunnel:wikipedia instead and put the track wikipedia entry into wikipedia"
            # suggestAlternative:"tunnel:wikipedia"
            # fixChangeKey:"wikipedia=>tunnel:wikipedia"
            # assertMatch:"way railway=light_rail wikipedia=Bartunnel tunnel:wikipedia=Bartunnel"
            # assertNoMatch:"way railway=rail tunnel:wikipedia=Baztunnel"
            # assertMatch:"way railway=rail wikipedia=Footunnel"
            err.append({'class': 9015021, 'subclass': 596570286, 'text': {'en': u'track tagged with \'tunnel\' in wikipedia, consider using tunnel:wikipedia instead and put the track wikipedia entry into wikipedia'}, 'fix': {
                '+': dict([
                    [u'tunnel:wikipedia', mapcss.tag(tags, u'wikipedia')]]),
                '-': ([
                    u'wikipedia'])
            }})

        # way[railway][name=~/[Bb]ridge/][!"bridge:name"]
        # way[railway][name=~/[Bb]ridge/]["bridge:name"=*name]
        # way[railway][name=~/[Vv]iadu[ck]t/][!"bridge:name"]
        # way[railway][name=~/[Vv]iadu[ck]t/]["bridge:name"=*name]
        # way[railway][name=~/[Bb]rücke/][!"bridge:name"]
        # way[railway][name=~/[Bb]rücke/]["bridge:name"=*name]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_25833d04, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge:name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_25833d04, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'bridge:name') == mapcss.tag(tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_0e3375d5, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge:name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_0e3375d5, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'bridge:name') == mapcss.tag(tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_18e8cc14, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge:name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_18e8cc14, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'bridge:name') == mapcss.tag(tags, u'name'))):
            # throwWarning:"track tagged with 'bridge' in name, consider using bridge:name instead and put the track name into name"
            # suggestAlternative:"bridge:name"
            # fixChangeKey:"name=>bridge:name"
            # assertMatch:"way railway=light_rail name=\"Bar bridge\" bridge:name=\"Bar bridge\""
            # assertNoMatch:"way railway=rail bridge:name=Foo-Viadukt"
            # assertMatch:"way railway=rail name=\"Bay bridge\""
            # assertMatch:"way railway=rail name=\"Baz viaduct\""
            # assertMatch:"way railway=rail name=Foobrücke"
            err.append({'class': 9015022, 'subclass': 441252968, 'text': {'en': u'track tagged with \'bridge\' in name, consider using bridge:name instead and put the track name into name'}, 'fix': {
                '+': dict([
                    [u'bridge:name', mapcss.tag(tags, u'name')]]),
                '-': ([
                    u'name'])
            }})

        # way[railway][wikipedia=~/[Bb]ridge/][!"bridge:wikipedia"]
        # way[railway][wikipedia=~/[Bb]ridge/]["bridge:wikipedia"=*wikipedia]
        # way[railway][wikipedia=~/[Vv]iadu[ck]t/][!"bridge:wikipedia"]
        # way[railway][wikipedia=~/[Vv]iadu[ck]t/]["bridge:wikipedia"=*wikipedia]
        # way[railway][wikipedia=~/[Bb]rücke/][!"bridge:wikipedia"]
        # way[railway][wikipedia=~/[Bb]rücke/]["bridge:wikipedia"=*wikipedia]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_25833d04, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge:wikipedia')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_25833d04, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and mapcss._tag_capture(capture_tags, 2, tags, u'bridge:wikipedia') == mapcss.tag(tags, u'wikipedia')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_0e3375d5, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge:wikipedia')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_0e3375d5, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and mapcss._tag_capture(capture_tags, 2, tags, u'bridge:wikipedia') == mapcss.tag(tags, u'wikipedia')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_18e8cc14, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge:wikipedia')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_18e8cc14, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and mapcss._tag_capture(capture_tags, 2, tags, u'bridge:wikipedia') == mapcss.tag(tags, u'wikipedia'))):
            # throwWarning:"track tagged with 'bridge' in wikipedia, consider using bridge:wikipedia instead and put track wikipedia entry into wikipedia"
            # suggestAlternative:"bridge:wikipedia"
            # fixChangeKey:"wikipedia=>bridge:wikipedia"
            # assertMatch:"way railway=light_rail wikipedia=\"Bar bridge\" bridge:wikipedia=\"Bar bridge\""
            # assertNoMatch:"way railway=rail bridge:wikipedia=Foo-Viadukt"
            # assertMatch:"way railway=rail wikipedia=\"Bay bridge\""
            # assertMatch:"way railway=rail wikipedia=\"Baz viaduct\""
            # assertMatch:"way railway=rail wikipedia=Foobrücke"
            err.append({'class': 9015023, 'subclass': 1872164964, 'text': {'en': u'track tagged with \'bridge\' in wikipedia, consider using bridge:wikipedia instead and put track wikipedia entry into wikipedia'}, 'fix': {
                '+': dict([
                    [u'bridge:wikipedia', mapcss.tag(tags, u'wikipedia')]]),
                '-': ([
                    u'wikipedia'])
            }})

        # way[railway][lanes]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'lanes'))):
            # throwWarning:"lanes=* is used for highways, not railways"
            # suggestAlternative:"tracks"
            # fixChangeKey:"lanes=>tracks"
            # assertMatch:"way railway=rail lanes=2"
            # assertNoMatch:"way railway=rail tracks=1"
            # assertMatch:"way railway=subway lanes=2 tracks=2"
            err.append({'class': 9015024, 'subclass': 1292450822, 'text': {'en': u'lanes=* is used for highways, not railways'}, 'fix': {
                '+': dict([
                    [u'tracks', mapcss.tag(tags, u'lanes')]]),
                '-': ([
                    u'lanes'])
            }})

        # way[railway][maxspeed=signals]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') == u'signals')):
            # throwWarning:"maxspeed=signals is deprecated, tag the highest possible speed instead"
            # assertMatch:"way railway=rail maxspeed=signals"
            # assertNoMatch:"way railway=subway maxspeed=100"
            err.append({'class': 9015025, 'subclass': 650821308, 'text': {'en': u'maxspeed=signals is deprecated, tag the highest possible speed instead'}})

        # way[railway]["mph:maxspeed"=~/^[0-9]+$/]["maxspeed"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_066203d3, mapcss._tag_capture(capture_tags, 1, tags, u'mph:maxspeed')) and mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))):
            # throwWarning:"maxspeed should contain the value as it is shown on the line with mph as unit"
            # suggestAlternative:"maxspeed"
            # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\" maxspeed=161"
            # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\""
            # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50\""
            # assertMatch:"way railway=rail \"mph:maxspeed\"=100 maxspeed=161"
            err.append({'class': 9015026, 'subclass': 317587071, 'text': {'en': u'maxspeed should contain the value as it is shown on the line with mph as unit'}})

        # way[railway]["mph:maxspeed"=~/^[0-9]+ mph$/]["maxspeed"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss.regexp_test_(self.re_63c39ff3, mapcss._tag_capture(capture_tags, 1, tags, u'mph:maxspeed')) and mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))):
            # throwWarning:"maxspeed should contain the value as it is shown on the line with mph as unit"
            # suggestAlternative:"maxspeed"
            # fixChangeKey:"mph:maxspeed=>maxspeed"
            # assertMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\" maxspeed=161"
            # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\""
            # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50\""
            # assertNoMatch:"way railway=rail \"mph:maxspeed\"=100 maxspeed=161"
            err.append({'class': 9015026, 'subclass': 2074447149, 'text': {'en': u'maxspeed should contain the value as it is shown on the line with mph as unit'}, 'fix': {
                '+': dict([
                    [u'maxspeed', mapcss.tag(tags, u'mph:maxspeed')]]),
                '-': ([
                    u'mph:maxspeed'])
            }})

        # way|z9-[railway=disused][!"disused:railway"]
        # way|z9-[railway=abandoned][!"abandoned:railway"]
        # way|z9-[railway=razed][!"razed:railway"]
        # way|z9-[railway=proposed][!"proposed:railway"]
        # way|z9-[railway=construction][!"construction:railway"]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'disused' and not mapcss._tag_capture(capture_tags, 1, tags, u'disused:railway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'abandoned' and not mapcss._tag_capture(capture_tags, 1, tags, u'abandoned:railway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'razed' and not mapcss._tag_capture(capture_tags, 1, tags, u'razed:railway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'proposed' and not mapcss._tag_capture(capture_tags, 1, tags, u'proposed:railway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'construction' and not mapcss._tag_capture(capture_tags, 1, tags, u'construction:railway'))):
            # throwWarning:tr("{0}={1} without {2}:railway","{0.key}","{0.value}","{0.value}")
            # assertNoMatch:"way railway=abandoned abandoned:railway=rail"
            # assertMatch:"way railway=abandoned"
            # assertNoMatch:"way railway=construction construction:railway=rail"
            # assertMatch:"way railway=construction"
            # assertNoMatch:"way railway=disused disused:railway=rail"
            # assertMatch:"way railway=disused"
            # assertNoMatch:"way railway=proposed proposed:railway=rail"
            # assertMatch:"way railway=proposed"
            # assertNoMatch:"way railway=razed razed:railway=rail"
            # assertMatch:"way railway=razed"
            err.append({'class': 9015027, 'subclass': 160705788, 'text': mapcss.tr(u'{0}={1} without {2}:railway', capture_tags, u'{0.key}', u'{0.value}', u'{0.value}')})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[railway=controlled_area]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'controlled_area')):
            # throwWarning:"controlled_area relations are deprecated"
            # suggestAlternative:"railway=interlocking"
            # fixAdd:"railway=interlocking"
            # assertMatch:"relation railway=controlled_area"
            # assertNoMatch:"relation railway=interlocking"
            err.append({'class': 9015041, 'subclass': 53808548, 'text': {'en': u'controlled_area relations are deprecated'}, 'fix': {
                '+': dict([
                    [u'railway',u'interlocking']])
            }})

        # relation[railway=interlocking][!type]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'interlocking' and not mapcss._tag_capture(capture_tags, 1, tags, u'type'))):
            # throwError:"interlocking relation without type=railway"
            # suggestAlternative:"type=railway"
            # fixAdd:"type=railway"
            # assertNoMatch:"relation railway=interlocking type=railway"
            # assertMatch:"relation railway=interlocking"
            err.append({'class': 9015042, 'subclass': 1490437342, 'text': {'en': u'interlocking relation without type=railway'}, 'fix': {
                '+': dict([
                    [u'type',u'railway']])
            }})

        # relation[railway=interlocking][type][type!=railway]
        if (u'railway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'interlocking' and mapcss._tag_capture(capture_tags, 1, tags, u'type') and mapcss._tag_capture(capture_tags, 2, tags, u'type') != u'railway')):
            # throwError:"interlocking relation with type other than railway"
            # assertMatch:"relation railway=interlocking type=public_transport"
            # assertNoMatch:"relation railway=interlocking type=railway"
            err.append({'class': 9015043, 'subclass': 1419769139, 'text': {'en': u'interlocking relation with type other than railway'}})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_openrailwaymap(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {u'railway': u'milestone', u'railway:position': u'42.0'}), expected={'class': 9015028, 'subclass': 1237934683})
        self.check_err(n.node(data, {u'railway': u'milestone'}), expected={'class': 9015028, 'subclass': 1237934683})
        self.check_err(n.node(data, {u'railway': u'level_crossing', u'supervised': u'yes'}), expected={'class': 9015029, 'subclass': 321695123})
        self.check_not_err(n.node(data, {u'railway': u'level_crossing'}), expected={'class': 9015029, 'subclass': 321695123})
        self.check_err(n.node(data, {u'railway:signal:direction': u'forward'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_err(n.node(data, {u'railway': u'level_crossing', u'railway:signal:position': u'right'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:position': u'right'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {u'railway': u'buffer_stop', u'railway:signal:minor': u'sh2'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {u'railway': u'derail', u'railway:signal:minor': u'sh'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:direction': u'forward'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main:form': u'light', u'railway:signal:main:states': u'hp0;hp1'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main:form': u'semaphore', u'railway:signal:main:states': u'hp0;hp1'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main:form': u'sign', u'railway:signal:main:states': u'hp0;hp1'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'80'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:speed_limit:form': u'sign', u'railway:signal:speed_limit:speed': u'80;90'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_err(n.node(data, {u'priority': u'yard', u'railway': u'buffer_stop'}), expected={'class': 9015014, 'subclass': 1264446053})
        self.check_not_err(n.node(data, {u'railway': u'crossing'}), expected={'class': 9015032, 'subclass': 719449462})
        self.check_err(n.node(data, {u'railway': u'flat_crossing'}), expected={'class': 9015032, 'subclass': 719449462})
        self.check_not_err(n.node(data, {u'railway': u'railway_crossing'}), expected={'class': 9015032, 'subclass': 719449462})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:stop:caption': u'70'}), expected={'class': 9015033, 'subclass': 1175712267})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:stop:caption': u'70', u'railway:signal:stop:description': u'70'}), expected={'class': 9015033, 'subclass': 1175712267})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:stop:description': u'70'}), expected={'class': 9015033, 'subclass': 1175712267})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:stop:caption': u'70'}), expected={'class': 9015034, 'subclass': 1820225369})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:stop:caption': u'70', u'railway:signal:stop:description': u'70'}), expected={'class': 9015034, 'subclass': 1820225369})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:stop:description': u'70'}), expected={'class': 9015034, 'subclass': 1820225369})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-ESO:ks', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9015035, 'subclass': 371617473})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-ESO:ks', u'railway:signal:minor': u'DE-ESO:sh1'}), expected={'class': 9015035, 'subclass': 371617473})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9015035, 'subclass': 371617473})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-ESO:ks', u'railway:signal:distant': u'DE-ESO:vr'}), expected={'class': 9015035, 'subclass': 570327409})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-ESO:ks', u'railway:signal:minor': u'DE-ESO:sh1'}), expected={'class': 9015035, 'subclass': 570327409})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:vr', u'railway:signal:main': u'DE-ESO:hp'}), expected={'class': 9015035, 'subclass': 570327409})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:ref': u'N1', u'ref': u'N1'}), expected={'class': 9015036, 'subclass': 257553969})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:ref': u'N1'}), expected={'class': 9015036, 'subclass': 257553969})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'ref': u'N1'}), expected={'class': 9015036, 'subclass': 257553969})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:ref': u'N1', u'ref': u'N1'}), expected={'class': 9015036, 'subclass': 1443995005})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:ref': u'N1'}), expected={'class': 9015036, 'subclass': 1443995005})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'ref': u'N1'}), expected={'class': 9015036, 'subclass': 1443995005})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:direction': u'forward'}), expected={'class': 9015037, 'subclass': 1288245325})
        self.check_err(n.node(data, {u'railway': u'signal'}), expected={'class': 9015037, 'subclass': 1288245325})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'DE-ESO:ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:combined': u'ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'DE-ESO:ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:distant': u'vr'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'DE-ESO:ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:main': u'ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'railway:signal:route': u'DE-ESO:zs2'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {u'railway': u'signal', u'railway:signal:route': u'zs2'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {u'name': u'FF', u'railway': u'signal', u'ref': u'FF'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_err(n.node(data, {u'name': u'FF', u'railway': u'signal'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {u'name': u'GG', u'railway': u'signal', u'ref': u'FF'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {u'railway': u'signal', u'ref': u'FF'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_err(n.node(data, {u'name': u'12', u'railway': u'switch', u'ref': u'12'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_err(n.node(data, {u'name': u'12', u'railway': u'switch'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {u'name': u'13', u'railway': u'switch', u'ref': u'12'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {u'railway': u'switch', u'ref': u'12'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {u'railway': u'switch', u'railway:switch': u'default', u'railway:switch:resetting': u'yes'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_not_err(n.node(data, {u'railway': u'switch', u'railway:switch': u'default'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_err(n.node(data, {u'railway': u'switch', u'railway:switch': u'resetting', u'ref': u'2'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_not_err(n.node(data, {u'railway': u'switch'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'service': u'siding'}), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'service': u'yard', u'usage': u'industrial'}), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_err(n.way(data, {u'railway': u'rail', u'service': u'siding', u'usage': u'main'}), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'usage': u'main'}), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'service': u'yard', u'usage': u'military'}), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_err(n.way(data, {u'railway': u'station'}), expected={'class': 9015002, 'subclass': 1498103253})
        self.check_not_err(n.way(data, {u'operator': u'SNCF', u'railway': u'rail'}), expected={'class': 9015003, 'subclass': 1686027167})
        self.check_err(n.way(data, {u'railway': u'rail'}), expected={'class': 9015003, 'subclass': 1686027167})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'railway:traffic_mode': u'passenger'}), expected={'class': 9015004, 'subclass': 1755442170})
        self.check_err(n.way(data, {u'railway': u'rail', u'traffic_mode': u'passenger'}), expected={'class': 9015004, 'subclass': 1755442170})
        self.check_not_err(n.way(data, {u'railway': u'rail'}), expected={'class': 9015004, 'subclass': 1755442170})
        self.check_not_err(n.way(data, {u'railway': u'rail railway:traffic_mode'}), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'usage': u'branch'}), expected={'class': 9015005, 'subclass': 331669407})
        self.check_err(n.way(data, {u'railway': u'rail', u'railway:traffic_mode': u'freight', u'usage': u'freight'}), expected={'class': 9015005, 'subclass': 331669407})
        self.check_err(n.way(data, {u'railway': u'rail', u'usage': u'freight'}), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'usage': u'industrial'}), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'usage': u'main'}), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'railway:traffic_mode': u'freight', u'usage': u'freight'}), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {u'railway': u'rail railway:traffic_mode'}), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'usage': u'branch'}), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_err(n.way(data, {u'railway': u'rail', u'railway:traffic_mode': u'mixed', u'usage': u'freight'}), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_err(n.way(data, {u'railway': u'rail', u'railway:traffic_mode': u'passenger', u'usage': u'freight'}), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'usage': u'industrial'}), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'usage': u'main'}), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'workrules': u'EBO'}), expected={'class': 9015006, 'subclass': 1310604175})
        self.check_err(n.way(data, {u'railway': u'rail'}), expected={'class': 9015006, 'subclass': 1310604175})
        self.check_err(n.way(data, {u'name': u'14', u'railway': u'light_rail', u'railway:track_ref': u'14'}), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_not_err(n.way(data, {u'name': u'Gleis 14b', u'railway': u'rail', u'railway:track_ref': u'14b'}), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_not_err(n.way(data, {u'name': u'Gleis 14b', u'railway': u'rail'}), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {u'name': u'14b', u'railway': u'rail', u'railway:track_ref': u'14b'}), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_not_err(n.way(data, {u'name': u'3', u'railway': u'rail'}), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {u'name': u'4', u'railway': u'rail', u'railway:track_ref': u'4'}), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {u'name': u'4a', u'railway': u'rail', u'railway:track_ref': u'4a'}), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {u'name': u'14', u'railway': u'light_rail'}), expected={'class': 9015007, 'subclass': 85438379})
        self.check_not_err(n.way(data, {u'name': u'3', u'railway': u'platform'}), expected={'class': 9015007, 'subclass': 85438379})
        self.check_not_err(n.way(data, {u'name': u'Gleis 14b', u'railway': u'rail'}), expected={'class': 9015007, 'subclass': 85438379})
        self.check_not_err(n.way(data, {u'name': u'track 4b', u'railway': u'rail'}), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {u'name': u'14b', u'railway': u'rail'}), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {u'name': u'4', u'railway': u'rail'}), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {u'name': u'4a', u'railway': u'rail'}), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {u'railway': u'platform', u'railway:track_ref': u'3', u'ref': u'3'}), expected={'class': 9015008, 'subclass': 226422824})
        self.check_not_err(n.way(data, {u'railway': u'platform', u'railway:track_ref': u'3', u'ref': u'4'}), expected={'class': 9015008, 'subclass': 226422824})
        self.check_err(n.way(data, {u'railway': u'platform', u'railway:track_ref': u'3'}), expected={'class': 9015008, 'subclass': 226422824})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'railway:track_ref': u'3'}), expected={'class': 9015008, 'subclass': 226422824})
        self.check_not_err(n.way(data, {u'railway': u'platform', u'railway:track_ref': u'3', u'ref': u'3'}), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_err(n.way(data, {u'railway': u'platform', u'railway:track_ref': u'3', u'ref': u'4'}), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_not_err(n.way(data, {u'railway': u'platform', u'railway:track_ref': u'3'}), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'railway:track_ref': u'3'}), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_err(n.way(data, {u'name': u'Gleis 14b', u'railway': u'rail'}), expected={'class': 9015009, 'subclass': 1420092530})
        self.check_not_err(n.way(data, {u'name': u'14b', u'railway': u'rail'}), expected={'class': 9015009, 'subclass': 1420092530})
        self.check_err(n.way(data, {u'railway': u'rail', u'ref': u'track 4b'}), expected={'class': 9015009, 'subclass': 1420092530})
        self.check_err(n.way(data, {u'description': u'Gleis 14b', u'name': u'Gleis 14b', u'railway': u'platform'}), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {u'name': u'Gleis 14b', u'railway': u'platform'}), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_not_err(n.way(data, {u'description': u'other', u'name': u'14b', u'railway': u'platform'}), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_not_err(n.way(data, {u'name': u'14b', u'railway': u'platform'}), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {u'railway': u'platform', u'ref': u'track 4b'}), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {u'railway': u'platform', u'ref': u'track 4b'}), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_not_err(n.way(data, {u'name': u'14b', u'railway': u'rail'}), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {u'description': u'other', u'name': u'Gleis 14b', u'railway': u'platform'}), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_not_err(n.way(data, {u'description': u'14b', u'name': u'14b', u'railway': u'platform'}), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_not_err(n.way(data, {u'name': u'14b', u'railway': u'platform'}), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_err(n.way(data, {u'description': u'other', u'railway': u'platform', u'ref': u'track 4b'}), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_err(n.way(data, {u'electrified': u'contact_line', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015011, 'subclass': 1012477221})
        self.check_not_err(n.way(data, {u'electrified': u'something', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015011, 'subclass': 1012477221})
        self.check_not_err(n.way(data, {u'electrified': u'something', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015011, 'subclass': 1909233042})
        self.check_err(n.way(data, {u'electrified': u'yes', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015011, 'subclass': 1909233042})
        self.check_err(n.way(data, {u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015011, 'subclass': 1909233042})
        self.check_err(n.way(data, {u'electrified': u'other', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015012, 'subclass': 1465196539})
        self.check_not_err(n.way(data, {u'electrified': u'yes', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015012, 'subclass': 1465196539})
        self.check_not_err(n.way(data, {u'electrified': u'yes', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015013, 'subclass': 356393984})
        self.check_err(n.way(data, {u'electrified': u'yes', u'power:type': u'something', u'railway': u'rail'}), expected={'class': 9015013, 'subclass': 356393984})
        self.check_not_err(n.way(data, {u'electrified': u'yes', u'power:type': u'overhead', u'railway': u'rail'}), expected={'class': 9015013, 'subclass': 410100568})
        self.check_err(n.way(data, {u'power:type': u'something', u'railway': u'rail'}), expected={'class': 9015013, 'subclass': 410100568})
        self.check_not_err(n.way(data, {u'highway': u'primary', u'priority': u'primary'}), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_err(n.way(data, {u'priority': u'primary', u'railway': u'rail', u'service': u'siding'}), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_err(n.way(data, {u'priority': u'primary', u'railway': u'rail', u'usage': u'main'}), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_err(n.way(data, {u'priority': u'primary', u'railway': u'rail'}), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_not_err(n.way(data, {u'detail!': u'track', u'railway': u'rail', u'tracks': u'1'}), expected={'class': 9015015, 'subclass': 986004687})
        self.check_err(n.way(data, {u'detail': u'track', u'railway': u'rail', u'tracks': u'1'}), expected={'class': 9015015, 'subclass': 986004687})
        self.check_not_err(n.way(data, {u'detail': u'track', u'railway': u'rail', u'tracks': u'2'}), expected={'class': 9015015, 'subclass': 986004687})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'tracks': u'1'}), expected={'class': 9015016, 'subclass': 256757521})
        self.check_err(n.way(data, {u'railway': u'rail', u'service': u'foo', u'tracks': u'2'}), expected={'class': 9015016, 'subclass': 256757521})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'tracks': u'2', u'usage': u'bar'}), expected={'class': 9015016, 'subclass': 256757521})
        self.check_err(n.way(data, {u'railway': u'crossing', u'railway:position:exact': u'2.4'}), expected={'class': 9015017, 'subclass': 2146160181})
        self.check_err(n.way(data, {u'railway': u'level_crossing', u'railway:position:exact': u'2.4'}), expected={'class': 9015017, 'subclass': 2146160181})
        self.check_not_err(n.way(data, {u'radio': u'GSM', u'railway': u'rail'}), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_not_err(n.way(data, {u'radio': u'GSM-R', u'railway': u'rail', u'railway:radio': u'gsm'}), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_err(n.way(data, {u'radio': u'GSM-R', u'railway': u'rail', u'railway:radio': u'gsm-r'}), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_err(n.way(data, {u'radio': u'GSM-R', u'railway': u'rail'}), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_err(n.way(data, {u'radio': u'GSM', u'railway': u'rail'}), expected={'class': 9015019, 'subclass': 406318522})
        self.check_err(n.way(data, {u'radio': u'GSM-R', u'railway': u'rail', u'railway:radio': u'gsm'}), expected={'class': 9015019, 'subclass': 406318522})
        self.check_not_err(n.way(data, {u'radio': u'GSM-R', u'railway': u'rail', u'railway:radio': u'gsm-r'}), expected={'class': 9015019, 'subclass': 406318522})
        self.check_not_err(n.way(data, {u'radio': u'GSM-R', u'railway': u'rail'}), expected={'class': 9015019, 'subclass': 406318522})
        self.check_err(n.way(data, {u'name': u'Bartunnel', u'railway': u'light_rail', u'tunnel:name': u'Bartunnel'}), expected={'class': 9015020, 'subclass': 843755814})
        self.check_err(n.way(data, {u'name': u'Footunnel', u'railway': u'rail'}), expected={'class': 9015020, 'subclass': 843755814})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'tunnel:name': u'Baztunnel'}), expected={'class': 9015020, 'subclass': 843755814})
        self.check_err(n.way(data, {u'railway': u'light_rail', u'tunnel:wikipedia': u'Bartunnel', u'wikipedia': u'Bartunnel'}), expected={'class': 9015021, 'subclass': 596570286})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'tunnel:wikipedia': u'Baztunnel'}), expected={'class': 9015021, 'subclass': 596570286})
        self.check_err(n.way(data, {u'railway': u'rail', u'wikipedia': u'Footunnel'}), expected={'class': 9015021, 'subclass': 596570286})
        self.check_err(n.way(data, {u'bridge:name': u'Bar bridge', u'name': u'Bar bridge', u'railway': u'light_rail'}), expected={'class': 9015022, 'subclass': 441252968})
        self.check_not_err(n.way(data, {u'bridge:name': u'Foo-Viadukt', u'railway': u'rail'}), expected={'class': 9015022, 'subclass': 441252968})
        self.check_err(n.way(data, {u'name': u'Bay bridge', u'railway': u'rail'}), expected={'class': 9015022, 'subclass': 441252968})
        self.check_err(n.way(data, {u'name': u'Baz viaduct', u'railway': u'rail'}), expected={'class': 9015022, 'subclass': 441252968})
        self.check_err(n.way(data, {u'name': u'Foobrücke', u'railway': u'rail'}), expected={'class': 9015022, 'subclass': 441252968})
        self.check_err(n.way(data, {u'bridge:wikipedia': u'Bar bridge', u'railway': u'light_rail', u'wikipedia': u'Bar bridge'}), expected={'class': 9015023, 'subclass': 1872164964})
        self.check_not_err(n.way(data, {u'bridge:wikipedia': u'Foo-Viadukt', u'railway': u'rail'}), expected={'class': 9015023, 'subclass': 1872164964})
        self.check_err(n.way(data, {u'railway': u'rail', u'wikipedia': u'Bay bridge'}), expected={'class': 9015023, 'subclass': 1872164964})
        self.check_err(n.way(data, {u'railway': u'rail', u'wikipedia': u'Baz viaduct'}), expected={'class': 9015023, 'subclass': 1872164964})
        self.check_err(n.way(data, {u'railway': u'rail', u'wikipedia': u'Foobrücke'}), expected={'class': 9015023, 'subclass': 1872164964})
        self.check_err(n.way(data, {u'lanes': u'2', u'railway': u'rail'}), expected={'class': 9015024, 'subclass': 1292450822})
        self.check_not_err(n.way(data, {u'railway': u'rail', u'tracks': u'1'}), expected={'class': 9015024, 'subclass': 1292450822})
        self.check_err(n.way(data, {u'lanes': u'2', u'railway': u'subway', u'tracks': u'2'}), expected={'class': 9015024, 'subclass': 1292450822})
        self.check_err(n.way(data, {u'maxspeed': u'signals', u'railway': u'rail'}), expected={'class': 9015025, 'subclass': 650821308})
        self.check_not_err(n.way(data, {u'maxspeed': u'100', u'railway': u'subway'}), expected={'class': 9015025, 'subclass': 650821308})
        self.check_not_err(n.way(data, {u'maxspeed': u'161', u'mph:maxspeed': u'50 mph', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 317587071})
        self.check_not_err(n.way(data, {u'mph:maxspeed': u'50 mph', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 317587071})
        self.check_not_err(n.way(data, {u'mph:maxspeed': u'50', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 317587071})
        self.check_err(n.way(data, {u'maxspeed': u'161', u'mph:maxspeed': u'100', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 317587071})
        self.check_err(n.way(data, {u'maxspeed': u'161', u'mph:maxspeed': u'50 mph', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_not_err(n.way(data, {u'mph:maxspeed': u'50 mph', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_not_err(n.way(data, {u'mph:maxspeed': u'50', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_not_err(n.way(data, {u'maxspeed': u'161', u'mph:maxspeed': u'100', u'railway': u'rail'}), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_not_err(n.way(data, {u'abandoned:railway': u'rail', u'railway': u'abandoned'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_err(n.way(data, {u'railway': u'abandoned'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_not_err(n.way(data, {u'construction:railway': u'rail', u'railway': u'construction'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_err(n.way(data, {u'railway': u'construction'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_not_err(n.way(data, {u'disused:railway': u'rail', u'railway': u'disused'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_err(n.way(data, {u'railway': u'disused'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_not_err(n.way(data, {u'proposed:railway': u'rail', u'railway': u'proposed'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_err(n.way(data, {u'railway': u'proposed'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_not_err(n.way(data, {u'railway': u'razed', u'razed:railway': u'rail'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_err(n.way(data, {u'railway': u'razed'}), expected={'class': 9015027, 'subclass': 160705788})
        self.check_err(n.relation(data, {u'railway': u'controlled_area'}), expected={'class': 9015041, 'subclass': 53808548})
        self.check_not_err(n.relation(data, {u'railway': u'interlocking'}), expected={'class': 9015041, 'subclass': 53808548})
        self.check_not_err(n.relation(data, {u'railway': u'interlocking', u'type': u'railway'}), expected={'class': 9015042, 'subclass': 1490437342})
        self.check_err(n.relation(data, {u'railway': u'interlocking'}), expected={'class': 9015042, 'subclass': 1490437342})
        self.check_err(n.relation(data, {u'railway': u'interlocking', u'type': u'public_transport'}), expected={'class': 9015043, 'subclass': 1419769139})
        self.check_not_err(n.relation(data, {u'railway': u'interlocking', u'type': u'railway'}), expected={'class': 9015043, 'subclass': 1419769139})
