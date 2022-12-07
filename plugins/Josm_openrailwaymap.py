#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_openrailwaymap(PluginMapCSS):

    MAPCSS_URL = 'https://www.openrailwaymap.org/validator/openrailwaymap.validator.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9015001] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'Track tagged with usage=* AND service=* - remove one of these tags'})
        self.errors[9015002] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'Station mapped as a way, but should be mapped as a node'})
        self.errors[9015004] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'Key traffic_mode is deprecated'})
        self.errors[9015005] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'usage=freight is deprecated'})
        self.errors[9015007] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'track numbers inside a station should be railway:track_ref, not name'})
        self.errors[9015008] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'platforms should have the numbers in ref, not railway:track_ref'})
        self.errors[9015009] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'track names or refs should not include the word \'track\', tag those numbers as railway:track_ref'})
        self.errors[9015010] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'platform names or refs should not include the word \'track\', write that as \'description\', put the bare numbers in \'ref\', separated by \';\''})
        self.errors[9015011] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'power:type=overhead is deprecated'})
        self.errors[9015012] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = mapcss.tr('power:type=overhead is deprecated, conflict between {0} and {1}', 'power:type=overhead', 'electrified=*'))
        self.errors[9015013] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'power:type is deprecated, change to proper electrified value'})
        self.errors[9015014] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'priority on railway objects is deprecated, remove it'})
        self.errors[9015015] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'tracks=1 not necessary if detail=track is tagged.'})
        self.errors[9015016] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'If tracks are tagged with service=*, they should be mapped as one way per track.'})
        self.errors[9015017] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'Crossings and level crossings should be mapped as nodes'})
        self.errors[9015018] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'radio=GSM-R is deprecated'})
        self.errors[9015019] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'radio=* is deprecated, change to proper railway:radio value'})
        self.errors[9015020] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'track tagged with \'tunnel\' in name, consider using tunnel:name instead and put the track name into name'})
        self.errors[9015021] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'track tagged with \'tunnel\' in wikipedia, consider using tunnel:wikipedia instead and put the track wikipedia entry into wikipedia'})
        self.errors[9015022] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'track tagged with \'bridge\' in name, consider using bridge:name instead and put the track name into name'})
        self.errors[9015023] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'track tagged with \'bridge\' in wikipedia, consider using bridge:wikipedia instead and put track wikipedia entry into wikipedia'})
        self.errors[9015024] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'lanes=* is used for highways, not railways'})
        self.errors[9015025] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'maxspeed=signals is deprecated, tag the highest possible speed instead'})
        self.errors[9015026] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'maxspeed should contain the value as it is shown on the line with mph as unit'})
        self.errors[9015028] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'Milestone without position, add railway:position=*'})
        self.errors[9015030] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'signal specification given but node is not tagged as signal or equivalent type'})
        self.errors[9015031] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'A sign cannot have different states.'})
        self.errors[9015032] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'railway=flat_crossing is deprecated'})
        self.errors[9015033] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'railway:signal:stop:description is deprecated and has been replaced by railway:signal:stop:caption'})
        self.errors[9015034] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'railway:signal:stop:description is deprecated, replace by appropiate railway:signal:stop:caption value'})
        self.errors[9015035] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'main and combined signal at the same place'})
        self.errors[9015036] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'signals should be tagged with ref, not railway:ref'})
        self.errors[9015037] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'signals should have a railway:signal:direction=* tag'})
        self.errors[9015038] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'signal names should be prefixed with an operator or country prefix'})
        self.errors[9015039] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = mapcss.tr('{0} identification should be tagged as ref, not as name', mapcss._tag_uncapture(capture_tags, '{0.value}')))
        self.errors[9015040] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'Tagging for resetting switch is deprecated, change railway:switch=* to proper value'})
        self.errors[9015041] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = {'en': 'controlled_area relations are deprecated'})
        self.errors[9015042] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'interlocking relation without type=railway'})
        self.errors[9015043] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'interlocking relation with type other than railway'})
        self.errors[9015044] = self.def_class(item = 9015, level = 3, tags = ["tag", "railway"], title = mapcss.tr('{0}={1} without name', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}')))
        self.errors[9015045] = self.def_class(item = 9015, level = 2, tags = ["tag", "railway"], title = {'en': 'track numbers inside a station should be railway:track_ref, not ref'})

        self.re_066203d3 = re.compile(r'^[0-9]+$')
        self.re_0e3375d5 = re.compile(r'[Vv]iadu[ck]t')
        self.re_14388f34 = re.compile(r'^[0-9]+[a-z]*.*')
        self.re_18e8cc14 = re.compile(r'[Bb]rücke')
        self.re_25833d04 = re.compile(r'[Bb]ridge')
        self.re_32cef8e4 = re.compile(r'.+:.+')
        self.re_3d75a7eb = re.compile(r'^[Vv]oie [0-9]+[a-z]*.*')
        self.re_4399527a = re.compile(r';')
        self.re_473b08ca = re.compile(r'^railway:signal:')
        self.re_4b2a9052 = re.compile(r'^[Tt]rack [0-9]+[a-z]*.*')
        self.re_5bca804b = re.compile(r'[Tt]unnel')
        self.re_61639c68 = re.compile(r'^(passenger|mixed)$')
        self.re_63c39ff3 = re.compile(r'^[0-9]+ mph$')
        self.re_7cf15856 = re.compile(r'^[Gg]leis [0-9]+[a-z]*.*')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[railway=milestone][!railway:position]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'milestone')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway:position')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"Milestone without position, add railway:position=*"
                # assertNoMatch:"node railway=milestone railway:position=42.0"
                # assertMatch:"node railway=milestone"
                err.append({'class': 9015028, 'subclass': 1237934683, 'text': {'en': 'Milestone without position, add railway:position=*'}})

        # node[railway=level_crossing][supervised]
        # node[railway=crossing][supervised]
        # Rule Blacklisted

        # node[/^railway:signal:/][railway!=signal][railway!=buffer_stop][railway!=derail]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_473b08ca)) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'signal', 'signal')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway') != mapcss._value_const_capture(capture_tags, 2, 'buffer_stop', 'buffer_stop')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway') != mapcss._value_const_capture(capture_tags, 3, 'derail', 'derail')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"signal specification given but node is not tagged as signal or equivalent type"
                # assertMatch:"node railway:signal:direction=forward"
                # assertMatch:"node railway:signal:position=right railway=level_crossing"
                # assertNoMatch:"node railway:signal:position=right railway=signal"
                # assertNoMatch:"node railway=buffer_stop railway:signal:minor=sh2"
                # assertNoMatch:"node railway=derail railway:signal:minor=sh"
                # assertNoMatch:"node railway=signal railway:signal:direction=forward"
                err.append({'class': 9015030, 'subclass': 908641862, 'text': {'en': 'signal specification given but node is not tagged as signal or equivalent type'}})

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
        if ('railway' in keys and 'railway:signal:brake_test:form' in keys and 'railway:signal:brake_test:states' in keys) or ('railway' in keys and 'railway:signal:combined:form' in keys and 'railway:signal:combined:states' in keys) or ('railway' in keys and 'railway:signal:crossing:form' in keys and 'railway:signal:crossing:states' in keys) or ('railway' in keys and 'railway:signal:crossing_distant:form' in keys and 'railway:signal:crossing_distant:states' in keys) or ('railway' in keys and 'railway:signal:departure:form' in keys and 'railway:signal:departure:states' in keys) or ('railway' in keys and 'railway:signal:distant:form' in keys and 'railway:signal:distant:states' in keys) or ('railway' in keys and 'railway:signal:humping:form' in keys and 'railway:signal:humping:states' in keys) or ('railway' in keys and 'railway:signal:main:form' in keys and 'railway:signal:main:states' in keys) or ('railway' in keys and 'railway:signal:main_repeated:form' in keys and 'railway:signal:main_repeated:states' in keys) or ('railway' in keys and 'railway:signal:minor:form' in keys and 'railway:signal:minor:states' in keys) or ('railway' in keys and 'railway:signal:minor_distant:form' in keys and 'railway:signal:minor_distant:states' in keys) or ('railway' in keys and 'railway:signal:resetting_switch:form' in keys and 'railway:signal:resetting_switch:states' in keys) or ('railway' in keys and 'railway:signal:route:form' in keys and 'railway:signal:route:states' in keys) or ('railway' in keys and 'railway:signal:route_distant:form' in keys and 'railway:signal:route_distant:states' in keys) or ('railway' in keys and 'railway:signal:short_route:form' in keys and 'railway:signal:short_route:states' in keys) or ('railway' in keys and 'railway:signal:shunting:form' in keys and 'railway:signal:shunting:states' in keys) or ('railway' in keys and 'railway:signal:speed_limit:form' in keys and 'railway:signal:speed_limit:speed' in keys) or ('railway' in keys and 'railway:signal:speed_limit_distant:form' in keys and 'railway:signal:speed_limit_distant:speed' in keys) or ('railway' in keys and 'railway:signal:stop_demand:form' in keys and 'railway:signal:stop_demand:states' in keys) or ('railway' in keys and 'railway:signal:wrong_road:form' in keys and 'railway:signal:wrong_road:states' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:combined:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:combined:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:shunting:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:shunting:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main_repeated:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main_repeated:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:minor:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:minor:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:minor_distant:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:minor_distant:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:crossing:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:crossing:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:crossing_distant:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:crossing_distant:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:humping:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:humping:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4399527a), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit:speed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit_distant:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4399527a), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit_distant:speed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:route:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:route:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:route_distant:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:route_distant:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:wrong_road:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:wrong_road:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:stop_demand:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:stop_demand:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:departure:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:departure:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:resetting_switch:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:resetting_switch:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:short_route:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:short_route:states')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:brake_test:form') == mapcss._value_capture(capture_tags, 1, 'sign')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:brake_test:states')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"A sign cannot have different states."
                # assertNoMatch:"node railway=signal railway:signal:main:states=hp0;hp1 railway:signal:main:form=light"
                # assertNoMatch:"node railway=signal railway:signal:main:states=hp0;hp1 railway:signal:main:form=semaphore"
                # assertMatch:"node railway=signal railway:signal:main:states=hp0;hp1 railway:signal:main:form=sign"
                # assertNoMatch:"node railway=signal railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=80"
                # assertMatch:"node railway=signal railway:signal:speed_limit:form=sign railway:signal:speed_limit:speed=80;90"
                err.append({'class': 9015031, 'subclass': 285269206, 'text': {'en': 'A sign cannot have different states.'}})

        # node[railway][priority]
        if ('priority' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'priority')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"priority on railway objects is deprecated, remove it"
                # fixRemove:"priority"
                # assertMatch:"node railway=buffer_stop priority=yard"
                err.append({'class': 9015014, 'subclass': 1264446053, 'text': {'en': 'priority on railway objects is deprecated, remove it'}, 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'priority'])
                }})

        # node[railway=flat_crossing]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'flat_crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"railway=flat_crossing is deprecated"
                # suggestAlternative:"railway=railway_crossing"
                # fixAdd:"railway=railway_crossing"
                # assertNoMatch:"node railway=crossing"
                # assertMatch:"node railway=flat_crossing"
                # assertNoMatch:"node railway=railway_crossing"
                err.append({'class': 9015032, 'subclass': 719449462, 'text': {'en': 'railway=flat_crossing is deprecated'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway','railway_crossing']])
                }})

        # node[railway:signal:stop:description][!railway:signal:stop:caption]
        if ('railway:signal:stop:description' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:stop:description')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:stop:caption')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"railway:signal:stop:caption"
                # throwWarning:"railway:signal:stop:description is deprecated and has been replaced by railway:signal:stop:caption"
                # fixChangeKey:"railway:signal:stop:description=>railway:signal:stop:caption"
                # assertNoMatch:"node railway=signal railway:signal:stop:caption=70"
                # assertNoMatch:"node railway=signal railway:signal:stop:description=70 railway:signal:stop:caption=70"
                # assertMatch:"node railway=signal railway:signal:stop:description=70"
                err.append({'class': 9015033, 'subclass': 1175712267, 'text': {'en': 'railway:signal:stop:description is deprecated and has been replaced by railway:signal:stop:caption'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:signal:stop:caption', mapcss.tag(tags, 'railway:signal:stop:description')]]),
                    '-': ([
                    'railway:signal:stop:description'])
                }})

        # node[railway:signal:stop:description][railway:signal:stop:caption]
        if ('railway:signal:stop:caption' in keys and 'railway:signal:stop:description' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:stop:description')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:stop:caption')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"railway:signal:stop:description is deprecated, replace by appropiate railway:signal:stop:caption value"
                # assertNoMatch:"node railway=signal railway:signal:stop:caption=70"
                # assertMatch:"node railway=signal railway:signal:stop:description=70 railway:signal:stop:caption=70"
                # assertNoMatch:"node railway=signal railway:signal:stop:description=70"
                err.append({'class': 9015034, 'subclass': 1820225369, 'text': {'en': 'railway:signal:stop:description is deprecated, replace by appropiate railway:signal:stop:caption value'}})

        # node["railway:signal:combined"]["railway:signal:main"]
        if ('railway:signal:combined' in keys and 'railway:signal:main' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:combined')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"main and combined signal at the same place"
                # assertMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:main=DE-ESO:hp"
                # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:minor=DE-ESO:sh1"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp"
                err.append({'class': 9015035, 'subclass': 371617473, 'text': {'en': 'main and combined signal at the same place'}})

        # node["railway:signal:combined"]["railway:signal:distant"]
        if ('railway:signal:combined' in keys and 'railway:signal:distant' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:signal:combined')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"main and combined signal at the same place"
                # assertMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:distant=DE-ESO:vr"
                # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks railway:signal:minor=DE-ESO:sh1"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:vr railway:signal:main=DE-ESO:hp"
                err.append({'class': 9015035, 'subclass': 570327409, 'text': {'en': 'main and combined signal at the same place'}})

        # node[railway=signal]["railway:ref"][!ref]
        if ('railway' in keys and 'railway:ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:ref')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"ref"
                # throwError:"signals should be tagged with ref, not railway:ref"
                # fixChangeKey:"railway:ref=>ref"
                # assertNoMatch:"node railway=signal railway:ref=N1 ref=N1"
                # assertMatch:"node railway=signal railway:ref=N1"
                # assertNoMatch:"node railway=signal ref=N1"
                err.append({'class': 9015036, 'subclass': 257553969, 'text': {'en': 'signals should be tagged with ref, not railway:ref'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref', mapcss.tag(tags, 'railway:ref')]]),
                    '-': ([
                    'railway:ref'])
                }})

        # node[railway=signal]["railway:ref"][ref]
        if ('railway' in keys and 'railway:ref' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:ref')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"ref"
                # throwError:"signals should be tagged with ref, not railway:ref"
                # fixChangeKey:"railway:ref=>ref"
                # assertMatch:"node railway=signal railway:ref=N1 ref=N1"
                # assertNoMatch:"node railway=signal railway:ref=N1"
                # assertNoMatch:"node railway=signal ref=N1"
                err.append({'class': 9015036, 'subclass': 1443995005, 'text': {'en': 'signals should be tagged with ref, not railway:ref'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref', mapcss.tag(tags, 'railway:ref')]]),
                    '-': ([
                    'railway:ref'])
                }})

        # node[railway=signal][!"railway:signal:direction"]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:direction')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"signals should have a railway:signal:direction=* tag"
                # assertNoMatch:"node railway=signal railway:signal:direction=forward"
                # assertMatch:"node railway=signal"
                err.append({'class': 9015037, 'subclass': 1288245325, 'text': {'en': 'signals should have a railway:signal:direction=* tag'}})

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
        if ('railway' in keys and 'railway:signal:brake_test' in keys) or ('railway' in keys and 'railway:signal:combined' in keys) or ('railway' in keys and 'railway:signal:crossing' in keys) or ('railway' in keys and 'railway:signal:crossing_distant' in keys) or ('railway' in keys and 'railway:signal:departure' in keys) or ('railway' in keys and 'railway:signal:distant' in keys) or ('railway' in keys and 'railway:signal:humping' in keys) or ('railway' in keys and 'railway:signal:main' in keys) or ('railway' in keys and 'railway:signal:main_repeated' in keys) or ('railway' in keys and 'railway:signal:minor' in keys) or ('railway' in keys and 'railway:signal:minor_distant' in keys) or ('railway' in keys and 'railway:signal:resetting_switch' in keys) or ('railway' in keys and 'railway:signal:route' in keys) or ('railway' in keys and 'railway:signal:route_distant' in keys) or ('railway' in keys and 'railway:signal:short_route' in keys) or ('railway' in keys and 'railway:signal:shunting' in keys) or ('railway' in keys and 'railway:signal:speed_limit' in keys) or ('railway' in keys and 'railway:signal:speed_limit_distant' in keys) or ('railway' in keys and 'railway:signal:stop_demand' in keys) or ('railway' in keys and 'railway:signal:wrong_road' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:combined')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:combined'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:distant')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:distant'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:shunting')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:shunting'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:main_repeated')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:main_repeated'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:minor')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:minor'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:minor_distant')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:minor_distant'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:crossing')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:crossing'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:crossing_distant')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:crossing_distant'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:humping')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:humping'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:speed_limit_distant')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:speed_limit_distant'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:route')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:route'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:route_distant')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:route_distant'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:wrong_road')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:wrong_road'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:stop_demand')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:stop_demand'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:departure')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:departure'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:resetting_switch')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:resetting_switch'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:short_route')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:short_route'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:signal:brake_test')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_32cef8e4, '.+:.+'), mapcss._tag_capture(capture_tags, 2, tags, 'railway:signal:brake_test'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"signal names should be prefixed with an operator or country prefix"
                # assertNoMatch:"node railway=signal railway:signal:combined=DE-ESO:ks"
                # assertMatch:"node railway=signal railway:signal:combined=ks"
                # assertNoMatch:"node railway=signal railway:signal:distant=DE-ESO:ks"
                # assertMatch:"node railway=signal railway:signal:distant=vr"
                # assertNoMatch:"node railway=signal railway:signal:main=DE-ESO:ks"
                # assertMatch:"node railway=signal railway:signal:main=ks"
                # assertNoMatch:"node railway=signal railway:signal:route=DE-ESO:zs2"
                # assertMatch:"node railway=signal railway:signal:route=zs2"
                err.append({'class': 9015038, 'subclass': 946563032, 'text': {'en': 'signal names should be prefixed with an operator or country prefix'}})

        # node[railway=signal][name][!ref]
        # node[railway=signal][name][ref=*name]
        # node[railway=switch][name][!ref]
        # node[railway=switch][name][ref=*name]
        if ('name' in keys and 'railway' in keys) or ('name' in keys and 'railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'signal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'switch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'switch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
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
                err.append({'class': 9015039, 'subclass': 1244137190, 'text': mapcss.tr('{0} identification should be tagged as ref, not as name', mapcss._tag_uncapture(capture_tags, '{0.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref', mapcss.tag(tags, 'name')]]),
                    '-': ([
                    'name'])
                }})

        # node[railway=switch]["railway:switch"=resetting]
        if ('railway' in keys and 'railway:switch' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'switch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:switch') == mapcss._value_capture(capture_tags, 1, 'resetting')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Tagging for resetting switch is deprecated, change railway:switch=* to proper value"
                # suggestAlternative:"railway:switch + railway:switch:resetting=yes"
                # fixAdd:"railway:switch:resetting=yes"
                # assertNoMatch:"node railway=switch railway:switch=default railway:switch:resetting=yes"
                # assertNoMatch:"node railway=switch railway:switch=default"
                # assertMatch:"node railway=switch railway:switch=resetting ref=2"
                # assertNoMatch:"node railway=switch"
                err.append({'class': 9015040, 'subclass': 967663151, 'text': {'en': 'Tagging for resetting switch is deprecated, change railway:switch=* to proper value'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:switch:resetting','yes']])
                }})

        # node[railway=station][station!=funicular][!name]
        # node[railway=halt][!name]
        # node[railway=junction][!name]
        # node[railway=spur_junction][!name]
        # node[railway=service_station][!name]
        # node[railway=site][!name]
        # node[railway=tram_stop][!name]
        # node[railway=yard][!name]
        # node[railway=crossover][!name]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'station')) and (mapcss._tag_capture(capture_tags, 1, tags, 'station') != mapcss._value_const_capture(capture_tags, 1, 'funicular', 'funicular')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'halt')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'junction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'spur_junction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'service_station')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'site')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'tram_stop')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'yard')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'crossover')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} without name","{0.key}","{0.value}")
                # assertNoMatch:"node railway=crossover name=foo"
                # assertMatch:"node railway=crossover"
                # assertNoMatch:"node railway=halt name=foo"
                # assertMatch:"node railway=halt"
                # assertNoMatch:"node railway=junction name=foo"
                # assertMatch:"node railway=junction"
                # assertNoMatch:"node railway=service_station name=foo"
                # assertMatch:"node railway=service_station"
                # assertNoMatch:"node railway=site name=foo"
                # assertMatch:"node railway=site"
                # assertNoMatch:"node railway=spur_junction name=foo"
                # assertMatch:"node railway=spur_junction"
                # assertNoMatch:"node railway=station name=foo"
                # assertMatch:"node railway=station"
                # assertNoMatch:"node railway=tram_stop name=foo"
                # assertMatch:"node railway=tram_stop"
                # assertNoMatch:"node railway=yard name=foo"
                # assertMatch:"node railway=yard"
                err.append({'class': 9015044, 'subclass': 1433036676, 'text': mapcss.tr('{0}={1} without name', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[railway][usage][usage!=industrial][usage!=military][service]
        if ('railway' in keys and 'service' in keys and 'usage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'usage')) and (mapcss._tag_capture(capture_tags, 2, tags, 'usage') != mapcss._value_const_capture(capture_tags, 2, 'industrial', 'industrial')) and (mapcss._tag_capture(capture_tags, 3, tags, 'usage') != mapcss._value_const_capture(capture_tags, 3, 'military', 'military')) and (mapcss._tag_capture(capture_tags, 4, tags, 'service')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Track tagged with usage=* AND service=* - remove one of these tags"
                # fixRemove:"service"
                # assertNoMatch:"way railway=rail service=siding"
                # assertNoMatch:"way railway=rail usage=industrial service=yard"
                # assertMatch:"way railway=rail usage=main service=siding"
                # assertNoMatch:"way railway=rail usage=main"
                # assertNoMatch:"way railway=rail usage=military service=yard"
                err.append({'class': 9015001, 'subclass': 1888453557, 'text': {'en': 'Track tagged with usage=* AND service=* - remove one of these tags'}, 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'service'])
                }})

        # way[railway=station]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'station')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Station mapped as a way, but should be mapped as a node"
                # assertMatch:"way railway=station"
                err.append({'class': 9015002, 'subclass': 1498103253, 'text': {'en': 'Station mapped as a way, but should be mapped as a node'}})

        # way[railway][traffic_mode]
        if ('railway' in keys and 'traffic_mode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'traffic_mode')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Key traffic_mode is deprecated"
                # suggestAlternative:"railway:traffic_mode"
                # fixChangeKey:"traffic_mode=>railway:traffic_mode"
                # assertNoMatch:"way railway=rail railway:traffic_mode=passenger"
                # assertMatch:"way railway=rail traffic_mode=passenger"
                # assertNoMatch:"way railway=rail"
                err.append({'class': 9015004, 'subclass': 1755442170, 'text': {'en': 'Key traffic_mode is deprecated'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:traffic_mode', mapcss.tag(tags, 'traffic_mode')]]),
                    '-': ([
                    'traffic_mode'])
                }})

        # way[railway][usage=freight][!railway:traffic_mode]
        # way[railway][usage=freight][railway:traffic_mode=freight]
        if ('railway' in keys and 'railway:traffic_mode' in keys and 'usage' in keys) or ('railway' in keys and 'usage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'usage') == mapcss._value_capture(capture_tags, 1, 'freight')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'railway:traffic_mode')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'usage') == mapcss._value_capture(capture_tags, 1, 'freight')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:traffic_mode') == mapcss._value_capture(capture_tags, 2, 'freight')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"railway:traffic_mode=freight"
                # throwError:"usage=freight is deprecated"
                # fixChangeKey:"usage=>railway:traffic_mode"
                # assertNoMatch:"way railway=rail railway:traffic_mode"
                # assertNoMatch:"way railway=rail usage=branch"
                # assertMatch:"way railway=rail usage=freight railway:traffic_mode=freight"
                # assertMatch:"way railway=rail usage=freight"
                # assertNoMatch:"way railway=rail usage=industrial"
                # assertNoMatch:"way railway=rail usage=main"
                err.append({'class': 9015005, 'subclass': 331669407, 'text': {'en': 'usage=freight is deprecated'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:traffic_mode', mapcss.tag(tags, 'usage')]]),
                    '-': ([
                    'usage'])
                }})

        # way[railway][usage=freight][railway:traffic_mode=~/^(passenger|mixed)$/]
        if ('railway' in keys and 'railway:traffic_mode' in keys and 'usage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'usage') == mapcss._value_capture(capture_tags, 1, 'freight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_61639c68), mapcss._tag_capture(capture_tags, 2, tags, 'railway:traffic_mode'))))
                except mapcss.RuleAbort: pass
            if match:
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
                err.append({'class': 9015005, 'subclass': 1212704987, 'text': {'en': 'usage=freight is deprecated'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:traffic_mode','mixed']]),
                    '-': ([
                    'usage'])
                }})

        # way[railway][railway!=platform][name=~/^[0-9]+[a-z]*.*/]["railway:track_ref"=*name]
        if ('name' in keys and 'railway' in keys and 'railway:track_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_14388f34), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:track_ref') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
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
                err.append({'class': 9015007, 'subclass': 2091521035, 'text': {'en': 'track numbers inside a station should be railway:track_ref, not name'}, 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'name'])
                }})

        # way[railway][railway!=platform][name=~/^[0-9]+[a-z]*.*/][!"railway:track_ref"]
        if ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_14388f34), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway:track_ref')))
                except mapcss.RuleAbort: pass
            if match:
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
                err.append({'class': 9015007, 'subclass': 85438379, 'text': {'en': 'track numbers inside a station should be railway:track_ref, not name'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:track_ref', mapcss.tag(tags, 'name')]]),
                    '-': ([
                    'name'])
                }})

        # way[railway][railway!=platform][service][ref]
        if ('railway' in keys and 'ref' in keys and 'service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss._tag_capture(capture_tags, 2, tags, 'service')) and (mapcss._tag_capture(capture_tags, 3, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"railway:track_ref"
                # throwError:"track numbers inside a station should be railway:track_ref, not ref"
                # fixChangeKey:"ref=>railway:track_ref"
                # assertMatch:"way railway=light_rail service=siding ref=14"
                # assertNoMatch:"way railway=platform ref=3"
                # assertNoMatch:"way railway=rail ref=1234"
                # assertMatch:"way railway=rail service=crossover ref=4a"
                # assertNoMatch:"way railway=rail service=siding railway:track_ref=14b"
                # assertMatch:"way railway=rail service=siding ref=4"
                err.append({'class': 9015045, 'subclass': 194113748, 'text': {'en': 'track numbers inside a station should be railway:track_ref, not ref'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:track_ref', mapcss.tag(tags, 'ref')]]),
                    '-': ([
                    'ref'])
                }})

        # way[railway=platform]["railway:track_ref"][!ref]
        # way[railway=platform]["railway:track_ref"]["railway:track_ref"=*ref]
        if ('railway' in keys and 'railway:track_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:track_ref')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:track_ref')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:track_ref') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"platforms should have the numbers in ref, not railway:track_ref"
                # suggestAlternative:"ref"
                # fixChangeKey:"railway:track_ref=>ref"
                # assertMatch:"way railway=platform railway:track_ref=3 ref=3"
                # assertNoMatch:"way railway=platform railway:track_ref=3 ref=4"
                # assertMatch:"way railway=platform railway:track_ref=3"
                # assertNoMatch:"way railway=rail railway:track_ref=3"
                err.append({'class': 9015008, 'subclass': 226422824, 'text': {'en': 'platforms should have the numbers in ref, not railway:track_ref'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref', mapcss.tag(tags, 'railway:track_ref')]]),
                    '-': ([
                    'railway:track_ref'])
                }})

        # way[railway=platform]["railway:track_ref"]["ref"]["railway:track_ref"!=*ref]
        if ('railway' in keys and 'railway:track_ref' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway:track_ref')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:track_ref') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"platforms should have the numbers in ref, not railway:track_ref"
                # assertNoMatch:"way railway=platform railway:track_ref=3 ref=3"
                # assertMatch:"way railway=platform railway:track_ref=3 ref=4"
                # assertNoMatch:"way railway=platform railway:track_ref=3"
                # assertNoMatch:"way railway=rail railway:track_ref=3"
                err.append({'class': 9015008, 'subclass': 1676742857, 'text': {'en': 'platforms should have the numbers in ref, not railway:track_ref'}})

        # way[railway][railway!=platform][name=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform]["name:de"=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][name=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][name=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform]["name:fr"=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][ref=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][ref=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway][railway!=platform][ref=~/^[Vv]oie [0-9]+[a-z]*.*/]
        if ('name' in keys and 'railway' in keys) or ('name:de' in keys and 'railway' in keys) or ('name:fr' in keys and 'railway' in keys) or ('railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'name:de'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'name:fr'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"track names or refs should not include the word 'track', tag those numbers as railway:track_ref"
                # assertMatch:"way railway=rail name=\"Gleis 14b\""
                # assertNoMatch:"way railway=rail name=14b"
                # assertMatch:"way railway=rail ref=\"track 4b\""
                err.append({'class': 9015009, 'subclass': 1420092530, 'text': {'en': 'track names or refs should not include the word \'track\', tag those numbers as railway:track_ref'}})

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
        if ('description' in keys and 'name' in keys and 'railway' in keys) or ('description' in keys and 'name:de' in keys and 'railway' in keys) or ('description' in keys and 'name:fr' in keys and 'railway' in keys) or ('description' in keys and 'railway' in keys and 'ref' in keys) or ('name' in keys and 'railway' in keys) or ('name:de' in keys and 'railway' in keys) or ('name:fr' in keys and 'railway' in keys) or ('railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'name:de'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'name:fr'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'name'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'name:de'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'name:de'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'name'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'name'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'name:fr'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'name:fr'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'ref'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7cf15856), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'ref'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'ref'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 2, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
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
                err.append({'class': 9015010, 'subclass': 1156420508, 'text': {'en': 'platform names or refs should not include the word \'track\', write that as \'description\', put the bare numbers in \'ref\', separated by \';\''}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, '{2.key}=>description')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, '{2.key}=>description')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, '{2.key}=>description')).split('=>', 1)[0].strip()])
                }})

        # way[railway=platform][description][description!=*name][name=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*"name:de"]["name:de"=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*name][name=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*name][name=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*"name:fr"]["name:fr"=~/^[Vv]oie [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*ref][ref=~/^[Gg]leis [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*ref][ref=~/^[Tt]rack [0-9]+[a-z]*.*/]
        # way[railway=platform][description][description!=*ref][ref=~/^[Vv]oie [0-9]+[a-z]*.*/]
        if ('description' in keys and 'name' in keys and 'railway' in keys) or ('description' in keys and 'name:de' in keys and 'railway' in keys) or ('description' in keys and 'name:fr' in keys and 'railway' in keys) or ('description' in keys and 'railway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_7cf15856), mapcss._tag_capture(capture_tags, 3, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name:de'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_7cf15856), mapcss._tag_capture(capture_tags, 3, tags, 'name:de'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 3, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 3, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name:fr'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 3, tags, 'name:fr'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'ref'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_7cf15856), mapcss._tag_capture(capture_tags, 3, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'ref'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_4b2a9052), mapcss._tag_capture(capture_tags, 3, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'platform')) and (mapcss._tag_capture(capture_tags, 1, tags, 'description')) and (mapcss._tag_capture(capture_tags, 2, tags, 'description') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'ref'))) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_3d75a7eb), mapcss._tag_capture(capture_tags, 3, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"platform names or refs should not include the word 'track', write that as 'description', put the bare numbers in 'ref', separated by ';'"
                # assertMatch:"way railway=platform name=\"Gleis 14b\" description=other"
                # assertNoMatch:"way railway=platform name=14b description=14b"
                # assertNoMatch:"way railway=platform name=14b"
                # assertMatch:"way railway=platform ref=\"track 4b\" description=other"
                err.append({'class': 9015010, 'subclass': 1149450895, 'text': {'en': 'platform names or refs should not include the word \'track\', write that as \'description\', put the bare numbers in \'ref\', separated by \';\''}})

        # way[railway]["power:type"=overhead][electrified=contact_line]
        if ('electrified' in keys and 'power:type' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power:type') == mapcss._value_capture(capture_tags, 1, 'overhead')) and (mapcss._tag_capture(capture_tags, 2, tags, 'electrified') == mapcss._value_capture(capture_tags, 2, 'contact_line')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"electrified=contact_line"
                # throwError:"power:type=overhead is deprecated"
                # fixRemove:"power:type"
                # assertMatch:"way railway=rail power:type=overhead electrified=contact_line"
                # assertNoMatch:"way railway=rail power:type=overhead electrified=something"
                err.append({'class': 9015011, 'subclass': 1012477221, 'text': {'en': 'power:type=overhead is deprecated'}, 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'power:type'])
                }})

        # way[railway]["power:type"=overhead][electrified=yes]
        # way[railway]["power:type"=overhead][!electrified]
        if ('electrified' in keys and 'power:type' in keys and 'railway' in keys) or ('power:type' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power:type') == mapcss._value_capture(capture_tags, 1, 'overhead')) and (mapcss._tag_capture(capture_tags, 2, tags, 'electrified') == mapcss._value_capture(capture_tags, 2, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power:type') == mapcss._value_capture(capture_tags, 1, 'overhead')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'electrified')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"electrified=contact_line"
                # throwError:"power:type=overhead is deprecated"
                # fixAdd:"electrified=contact_line"
                # fixRemove:"power:type"
                # assertNoMatch:"way railway=rail power:type=overhead electrified=something"
                # assertMatch:"way railway=rail power:type=overhead electrified=yes"
                # assertMatch:"way railway=rail power:type=overhead"
                err.append({'class': 9015011, 'subclass': 1909233042, 'text': {'en': 'power:type=overhead is deprecated'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['electrified','contact_line']]),
                    '-': ([
                    'power:type'])
                }})

        # way[railway]["power:type"=overhead][electrified][electrified!=yes][electrified!=contact_line]
        if ('electrified' in keys and 'power:type' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power:type') == mapcss._value_capture(capture_tags, 1, 'overhead')) and (mapcss._tag_capture(capture_tags, 2, tags, 'electrified')) and (mapcss._tag_capture(capture_tags, 3, tags, 'electrified') != mapcss._value_const_capture(capture_tags, 3, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 4, tags, 'electrified') != mapcss._value_const_capture(capture_tags, 4, 'contact_line', 'contact_line')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("power:type=overhead is deprecated, conflict between {0} and {1}","power:type=overhead","electrified=*")
                # assertMatch:"way railway=rail power:type=overhead electrified=other"
                # assertNoMatch:"way railway=rail power:type=overhead electrified=yes"
                err.append({'class': 9015012, 'subclass': 1465196539, 'text': mapcss.tr('power:type=overhead is deprecated, conflict between {0} and {1}', 'power:type=overhead', 'electrified=*')})

        # way[railway]["power:type"]["power:type"!=overhead][electrified]
        if ('electrified' in keys and 'power:type' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power:type')) and (mapcss._tag_capture(capture_tags, 2, tags, 'power:type') != mapcss._value_const_capture(capture_tags, 2, 'overhead', 'overhead')) and (mapcss._tag_capture(capture_tags, 3, tags, 'electrified')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"power:type is deprecated, change to proper electrified value"
                # assertNoMatch:"way railway=rail power:type=overhead electrified=yes"
                # assertMatch:"way railway=rail power:type=something electrified=yes"
                err.append({'class': 9015013, 'subclass': 356393984, 'text': {'en': 'power:type is deprecated, change to proper electrified value'}})

        # way[railway]["power:type"]["power:type"!=overhead][!electrified]
        if ('power:type' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power:type')) and (mapcss._tag_capture(capture_tags, 2, tags, 'power:type') != mapcss._value_const_capture(capture_tags, 2, 'overhead', 'overhead')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'electrified')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"power:type is deprecated, change to proper electrified value"
                # assertNoMatch:"way railway=rail power:type=overhead electrified=yes"
                # assertMatch:"way railway=rail power:type=something"
                err.append({'class': 9015013, 'subclass': 410100568, 'text': {'en': 'power:type is deprecated, change to proper electrified value'}})

        # way[railway][priority]
        if ('priority' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'priority')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"priority on railway objects is deprecated, remove it"
                # fixRemove:"priority"
                # assertNoMatch:"way highway=primary priority=primary"
                # assertMatch:"way railway=rail priority=primary service=siding"
                # assertMatch:"way railway=rail priority=primary usage=main"
                # assertMatch:"way railway=rail priority=primary"
                err.append({'class': 9015014, 'subclass': 2122288452, 'text': {'en': 'priority on railway objects is deprecated, remove it'}, 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'priority'])
                }})

        # way[railway][tracks=1][detail=track]
        if ('detail' in keys and 'railway' in keys and 'tracks' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tracks') == mapcss._value_capture(capture_tags, 1, 1)) and (mapcss._tag_capture(capture_tags, 2, tags, 'detail') == mapcss._value_capture(capture_tags, 2, 'track')))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"detail=track"
                # throwWarning:"tracks=1 not necessary if detail=track is tagged."
                # fixRemove:"tracks"
                # assertNoMatch:"way railway=rail tracks=1 detail!=track"
                # assertMatch:"way railway=rail tracks=1 detail=track"
                # assertNoMatch:"way railway=rail tracks=2 detail=track"
                err.append({'class': 9015015, 'subclass': 986004687, 'text': {'en': 'tracks=1 not necessary if detail=track is tagged.'}, 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'tracks'])
                }})

        # way[railway][tracks!=1][tracks][service]
        if ('railway' in keys and 'service' in keys and 'tracks' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tracks') != mapcss._value_capture(capture_tags, 1, 1)) and (mapcss._tag_capture(capture_tags, 2, tags, 'tracks')) and (mapcss._tag_capture(capture_tags, 3, tags, 'service')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"If tracks are tagged with service=*, they should be mapped as one way per track."
                # assertNoMatch:"way railway=rail tracks=1"
                # assertMatch:"way railway=rail tracks=2 service=foo"
                # assertNoMatch:"way railway=rail tracks=2 usage=bar"
                err.append({'class': 9015016, 'subclass': 256757521, 'text': {'en': 'If tracks are tagged with service=*, they should be mapped as one way per track.'}})

        # way[railway=crossing]
        # way[railway=level_crossing]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'level_crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"Crossings and level crossings should be mapped as nodes"
                # assertMatch:"way railway=crossing railway:position:exact=2.4"
                # assertMatch:"way railway=level_crossing railway:position:exact=2.4"
                err.append({'class': 9015017, 'subclass': 2146160181, 'text': {'en': 'Crossings and level crossings should be mapped as nodes'}})

        # way[railway][radio="GSM-R"][!"railway:radio"]
        # way[railway][radio="GSM-R"]["railway:radio"="gsm-r"]
        if ('radio' in keys and 'railway' in keys) or ('radio' in keys and 'railway' in keys and 'railway:radio' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'radio') == mapcss._value_capture(capture_tags, 1, 'GSM-R')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'railway:radio')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'radio') == mapcss._value_capture(capture_tags, 1, 'GSM-R')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:radio') == mapcss._value_capture(capture_tags, 2, 'gsm-r')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"radio=GSM-R is deprecated"
                # suggestAlternative:"railway:radio=gsm-r"
                # fixRemove:"radio"
                # fixAdd:"railway:radio=gsm-r"
                # assertNoMatch:"way railway=rail radio=\"GSM\""
                # assertNoMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm\""
                # assertMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm-r\""
                # assertMatch:"way railway=rail radio=\"GSM-R\""
                err.append({'class': 9015018, 'subclass': 2078132492, 'text': {'en': 'radio=GSM-R is deprecated'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:radio','gsm-r']]),
                    '-': ([
                    'radio'])
                }})

        # way[railway][radio="GSM-R"]["railway:radio"]["railway:radio"!="gsm-r"]
        # way[railway][radio][radio!="GSM-R"]
        if ('radio' in keys and 'railway' in keys) or ('radio' in keys and 'railway' in keys and 'railway:radio' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'radio') == mapcss._value_capture(capture_tags, 1, 'GSM-R')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway:radio')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway:radio') != mapcss._value_const_capture(capture_tags, 3, 'gsm-r', 'gsm-r')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'radio')) and (mapcss._tag_capture(capture_tags, 2, tags, 'radio') != mapcss._value_const_capture(capture_tags, 2, 'GSM-R', 'GSM-R')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"radio=* is deprecated, change to proper railway:radio value"
                # assertMatch:"way railway=rail radio=\"GSM\""
                # assertMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm\""
                # assertNoMatch:"way railway=rail radio=\"GSM-R\" \"railway:radio\"=\"gsm-r\""
                # assertNoMatch:"way railway=rail radio=\"GSM-R\""
                err.append({'class': 9015019, 'subclass': 406318522, 'text': {'en': 'radio=* is deprecated, change to proper railway:radio value'}})

        # way[railway][railway!=platform][name=~/[Tt]unnel/][!"tunnel:name"]
        # way[railway][railway!=platform][name=~/[Tt]unnel/]["tunnel:name"=*name]
        if ('name' in keys and 'railway' in keys) or ('name' in keys and 'railway' in keys and 'tunnel:name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5bca804b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'tunnel:name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5bca804b), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'tunnel:name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"track tagged with 'tunnel' in name, consider using tunnel:name instead and put the track name into name"
                # suggestAlternative:"tunnel:name"
                # fixChangeKey:"name=>tunnel:name"
                # assertMatch:"way railway=light_rail name=Bartunnel tunnel:name=Bartunnel"
                # assertNoMatch:"way railway=platform name=Footunnel"
                # assertMatch:"way railway=rail name=Footunnel"
                # assertNoMatch:"way railway=rail tunnel:name=Baztunnel"
                err.append({'class': 9015020, 'subclass': 1651250819, 'text': {'en': 'track tagged with \'tunnel\' in name, consider using tunnel:name instead and put the track name into name'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tunnel:name', mapcss.tag(tags, 'name')]]),
                    '-': ([
                    'name'])
                }})

        # way[railway][railway!=platform][wikipedia=~/[Tt]unnel/][!"tunnel:wikipedia"]
        # way[railway][railway!=platform][wikipedia=~/[Tt]unnel/]["tunnel:wikipedia"=*wikipedia]
        if ('railway' in keys and 'tunnel:wikipedia' in keys and 'wikipedia' in keys) or ('railway' in keys and 'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5bca804b), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'tunnel:wikipedia')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_5bca804b), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'tunnel:wikipedia') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'wikipedia'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"track tagged with 'tunnel' in wikipedia, consider using tunnel:wikipedia instead and put the track wikipedia entry into wikipedia"
                # suggestAlternative:"tunnel:wikipedia"
                # fixChangeKey:"wikipedia=>tunnel:wikipedia"
                # assertMatch:"way railway=light_rail wikipedia=Bartunnel tunnel:wikipedia=Bartunnel"
                # assertNoMatch:"way railway=platform wikipedia=Footunnel"
                # assertNoMatch:"way railway=rail tunnel:wikipedia=Baztunnel"
                # assertMatch:"way railway=rail wikipedia=Footunnel"
                err.append({'class': 9015021, 'subclass': 1581548500, 'text': {'en': 'track tagged with \'tunnel\' in wikipedia, consider using tunnel:wikipedia instead and put the track wikipedia entry into wikipedia'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tunnel:wikipedia', mapcss.tag(tags, 'wikipedia')]]),
                    '-': ([
                    'wikipedia'])
                }})

        # way[railway][railway!=platform][name=~/[Bb]ridge/][!"bridge:name"]
        # way[railway][railway!=platform][name=~/[Bb]ridge/]["bridge:name"=*name]
        # way[railway][railway!=platform][name=~/[Vv]iadu[ck]t/][!"bridge:name"]
        # way[railway][railway!=platform][name=~/[Vv]iadu[ck]t/]["bridge:name"=*name]
        # way[railway][railway!=platform][name=~/[Bb]rücke/][!"bridge:name"]
        # way[railway][railway!=platform][name=~/[Bb]rücke/]["bridge:name"=*name]
        if ('bridge:name' in keys and 'name' in keys and 'railway' in keys) or ('name' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_25833d04), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bridge:name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_25833d04), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'bridge:name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0e3375d5), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bridge:name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0e3375d5), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'bridge:name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_18e8cc14), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bridge:name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_18e8cc14), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'bridge:name') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"track tagged with 'bridge' in name, consider using bridge:name instead and put the track name into name"
                # suggestAlternative:"bridge:name"
                # fixChangeKey:"name=>bridge:name"
                # assertMatch:"way railway=light_rail name=\"Bar bridge\" bridge:name=\"Bar bridge\""
                # assertNoMatch:"way railway=platform name=Noltemeyerbrücke"
                # assertNoMatch:"way railway=rail bridge:name=Foo-Viadukt"
                # assertMatch:"way railway=rail name=\"Bay bridge\""
                # assertMatch:"way railway=rail name=\"Baz viaduct\""
                # assertMatch:"way railway=rail name=Foobrücke"
                err.append({'class': 9015022, 'subclass': 359430532, 'text': {'en': 'track tagged with \'bridge\' in name, consider using bridge:name instead and put the track name into name'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bridge:name', mapcss.tag(tags, 'name')]]),
                    '-': ([
                    'name'])
                }})

        # way[railway][railway!=platform][wikipedia=~/[Bb]ridge/][!"bridge:wikipedia"]
        # way[railway][railway!=platform][wikipedia=~/[Bb]ridge/]["bridge:wikipedia"=*wikipedia]
        # way[railway][railway!=platform][wikipedia=~/[Vv]iadu[ck]t/][!"bridge:wikipedia"]
        # way[railway][railway!=platform][wikipedia=~/[Vv]iadu[ck]t/]["bridge:wikipedia"=*wikipedia]
        # way[railway][railway!=platform][wikipedia=~/[Bb]rücke/][!"bridge:wikipedia"]
        # way[railway][railway!=platform][wikipedia=~/[Bb]rücke/]["bridge:wikipedia"=*wikipedia]
        if ('bridge:wikipedia' in keys and 'railway' in keys and 'wikipedia' in keys) or ('railway' in keys and 'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_25833d04), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bridge:wikipedia')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_25833d04), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'bridge:wikipedia') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'wikipedia'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0e3375d5), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bridge:wikipedia')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_0e3375d5), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'bridge:wikipedia') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'wikipedia'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_18e8cc14), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bridge:wikipedia')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'platform', 'platform')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_18e8cc14), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'bridge:wikipedia') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'wikipedia'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"track tagged with 'bridge' in wikipedia, consider using bridge:wikipedia instead and put track wikipedia entry into wikipedia"
                # suggestAlternative:"bridge:wikipedia"
                # fixChangeKey:"wikipedia=>bridge:wikipedia"
                # assertMatch:"way railway=light_rail wikipedia=\"Bar bridge\" bridge:wikipedia=\"Bar bridge\""
                # assertNoMatch:"way railway=platform wikipedia=Foobrücke"
                # assertNoMatch:"way railway=rail bridge:wikipedia=Foo-Viadukt"
                # assertMatch:"way railway=rail wikipedia=\"Bay bridge\""
                # assertMatch:"way railway=rail wikipedia=\"Baz viaduct\""
                # assertMatch:"way railway=rail wikipedia=Foobrücke"
                err.append({'class': 9015023, 'subclass': 1594751596, 'text': {'en': 'track tagged with \'bridge\' in wikipedia, consider using bridge:wikipedia instead and put track wikipedia entry into wikipedia'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bridge:wikipedia', mapcss.tag(tags, 'wikipedia')]]),
                    '-': ([
                    'wikipedia'])
                }})

        # way[railway][!highway][lanes]
        if ('lanes' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'lanes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"lanes=* is used for highways, not railways"
                # suggestAlternative:"tracks"
                # fixChangeKey:"lanes=>tracks"
                # assertNoMatch:"way railway=abandoned highway=tertiary lanes=3"
                # assertMatch:"way railway=rail lanes=2"
                # assertNoMatch:"way railway=rail tracks=1"
                # assertNoMatch:"way railway=razed highway=tertiary lanes=3"
                # assertMatch:"way railway=subway lanes=2 tracks=2"
                err.append({'class': 9015024, 'subclass': 245965100, 'text': {'en': 'lanes=* is used for highways, not railways'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tracks', mapcss.tag(tags, 'lanes')]]),
                    '-': ([
                    'lanes'])
                }})

        # way[railway][maxspeed=signals]
        if ('maxspeed' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed') == mapcss._value_capture(capture_tags, 1, 'signals')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"maxspeed=signals is deprecated, tag the highest possible speed instead"
                # assertMatch:"way railway=rail maxspeed=signals"
                # assertNoMatch:"way railway=subway maxspeed=100"
                err.append({'class': 9015025, 'subclass': 650821308, 'text': {'en': 'maxspeed=signals is deprecated, tag the highest possible speed instead'}})

        # way[railway]["mph:maxspeed"=~/^[0-9]+$/]["maxspeed"]
        if ('maxspeed' in keys and 'mph:maxspeed' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_066203d3), mapcss._tag_capture(capture_tags, 1, tags, 'mph:maxspeed'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"maxspeed should contain the value as it is shown on the line with mph as unit"
                # suggestAlternative:"maxspeed"
                # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\" maxspeed=161"
                # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\""
                # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50\""
                # assertMatch:"way railway=rail \"mph:maxspeed\"=100 maxspeed=161"
                err.append({'class': 9015026, 'subclass': 317587071, 'text': {'en': 'maxspeed should contain the value as it is shown on the line with mph as unit'}})

        # way[railway]["mph:maxspeed"=~/^[0-9]+ mph$/]["maxspeed"]
        if ('maxspeed' in keys and 'mph:maxspeed' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_63c39ff3), mapcss._tag_capture(capture_tags, 1, tags, 'mph:maxspeed'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"maxspeed should contain the value as it is shown on the line with mph as unit"
                # suggestAlternative:"maxspeed"
                # fixChangeKey:"mph:maxspeed=>maxspeed"
                # assertMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\" maxspeed=161"
                # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50 mph\""
                # assertNoMatch:"way railway=rail \"mph:maxspeed\"=\"50\""
                # assertNoMatch:"way railway=rail \"mph:maxspeed\"=100 maxspeed=161"
                err.append({'class': 9015026, 'subclass': 2074447149, 'text': {'en': 'maxspeed should contain the value as it is shown on the line with mph as unit'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxspeed', mapcss.tag(tags, 'mph:maxspeed')]]),
                    '-': ([
                    'mph:maxspeed'])
                }})

        # way|z9-[railway=disused][!"disused:railway"]
        # way|z9-[railway=abandoned][!"abandoned:railway"]
        # way|z9-[railway=razed][!"razed:railway"]
        # way|z9-[railway=proposed][!"proposed:railway"]
        # way|z9-[railway=construction][!"construction:railway"]
        # Rule Blacklisted

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[railway=controlled_area]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'controlled_area')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"controlled_area relations are deprecated"
                # suggestAlternative:"railway=interlocking"
                # fixAdd:"railway=interlocking"
                # assertMatch:"relation railway=controlled_area"
                # assertNoMatch:"relation railway=interlocking"
                err.append({'class': 9015041, 'subclass': 53808548, 'text': {'en': 'controlled_area relations are deprecated'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway','interlocking']])
                }})

        # relation[railway=interlocking][!type]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'interlocking')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'type')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"interlocking relation without type=railway"
                # suggestAlternative:"type=railway"
                # fixAdd:"type=railway"
                # assertNoMatch:"relation railway=interlocking type=railway"
                # assertMatch:"relation railway=interlocking"
                err.append({'class': 9015042, 'subclass': 1490437342, 'text': {'en': 'interlocking relation without type=railway'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['type','railway']])
                }})

        # relation[railway=interlocking][type][type!=railway]
        if ('railway' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'interlocking')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"interlocking relation with type other than railway"
                # assertMatch:"relation railway=interlocking type=public_transport"
                # assertNoMatch:"relation railway=interlocking type=railway"
                err.append({'class': 9015043, 'subclass': 1419769139, 'text': {'en': 'interlocking relation with type other than railway'}})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_openrailwaymap(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {'railway': 'milestone', 'railway:position': '42.0'}), expected={'class': 9015028, 'subclass': 1237934683})
        self.check_err(n.node(data, {'railway': 'milestone'}), expected={'class': 9015028, 'subclass': 1237934683})
        self.check_err(n.node(data, {'railway:signal:direction': 'forward'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_err(n.node(data, {'railway': 'level_crossing', 'railway:signal:position': 'right'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:position': 'right'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {'railway': 'buffer_stop', 'railway:signal:minor': 'sh2'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {'railway': 'derail', 'railway:signal:minor': 'sh'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:direction': 'forward'}), expected={'class': 9015030, 'subclass': 908641862})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main:form': 'light', 'railway:signal:main:states': 'hp0;hp1'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main:form': 'semaphore', 'railway:signal:main:states': 'hp0;hp1'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main:form': 'sign', 'railway:signal:main:states': 'hp0;hp1'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '80'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:speed_limit:form': 'sign', 'railway:signal:speed_limit:speed': '80;90'}), expected={'class': 9015031, 'subclass': 285269206})
        self.check_err(n.node(data, {'priority': 'yard', 'railway': 'buffer_stop'}), expected={'class': 9015014, 'subclass': 1264446053})
        self.check_not_err(n.node(data, {'railway': 'crossing'}), expected={'class': 9015032, 'subclass': 719449462})
        self.check_err(n.node(data, {'railway': 'flat_crossing'}), expected={'class': 9015032, 'subclass': 719449462})
        self.check_not_err(n.node(data, {'railway': 'railway_crossing'}), expected={'class': 9015032, 'subclass': 719449462})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:stop:caption': '70'}), expected={'class': 9015033, 'subclass': 1175712267})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:stop:caption': '70', 'railway:signal:stop:description': '70'}), expected={'class': 9015033, 'subclass': 1175712267})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:stop:description': '70'}), expected={'class': 9015033, 'subclass': 1175712267})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:stop:caption': '70'}), expected={'class': 9015034, 'subclass': 1820225369})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:stop:caption': '70', 'railway:signal:stop:description': '70'}), expected={'class': 9015034, 'subclass': 1820225369})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:stop:description': '70'}), expected={'class': 9015034, 'subclass': 1820225369})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-ESO:ks', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9015035, 'subclass': 371617473})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-ESO:ks', 'railway:signal:minor': 'DE-ESO:sh1'}), expected={'class': 9015035, 'subclass': 371617473})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9015035, 'subclass': 371617473})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-ESO:ks', 'railway:signal:distant': 'DE-ESO:vr'}), expected={'class': 9015035, 'subclass': 570327409})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-ESO:ks', 'railway:signal:minor': 'DE-ESO:sh1'}), expected={'class': 9015035, 'subclass': 570327409})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:vr', 'railway:signal:main': 'DE-ESO:hp'}), expected={'class': 9015035, 'subclass': 570327409})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:ref': 'N1', 'ref': 'N1'}), expected={'class': 9015036, 'subclass': 257553969})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:ref': 'N1'}), expected={'class': 9015036, 'subclass': 257553969})
        self.check_not_err(n.node(data, {'railway': 'signal', 'ref': 'N1'}), expected={'class': 9015036, 'subclass': 257553969})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:ref': 'N1', 'ref': 'N1'}), expected={'class': 9015036, 'subclass': 1443995005})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:ref': 'N1'}), expected={'class': 9015036, 'subclass': 1443995005})
        self.check_not_err(n.node(data, {'railway': 'signal', 'ref': 'N1'}), expected={'class': 9015036, 'subclass': 1443995005})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:direction': 'forward'}), expected={'class': 9015037, 'subclass': 1288245325})
        self.check_err(n.node(data, {'railway': 'signal'}), expected={'class': 9015037, 'subclass': 1288245325})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'DE-ESO:ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:combined': 'ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'DE-ESO:ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:distant': 'vr'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'DE-ESO:ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:main': 'ks'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_not_err(n.node(data, {'railway': 'signal', 'railway:signal:route': 'DE-ESO:zs2'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {'railway': 'signal', 'railway:signal:route': 'zs2'}), expected={'class': 9015038, 'subclass': 946563032})
        self.check_err(n.node(data, {'name': 'FF', 'railway': 'signal', 'ref': 'FF'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_err(n.node(data, {'name': 'FF', 'railway': 'signal'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {'name': 'GG', 'railway': 'signal', 'ref': 'FF'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {'railway': 'signal', 'ref': 'FF'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_err(n.node(data, {'name': '12', 'railway': 'switch', 'ref': '12'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_err(n.node(data, {'name': '12', 'railway': 'switch'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {'name': '13', 'railway': 'switch', 'ref': '12'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {'railway': 'switch', 'ref': '12'}), expected={'class': 9015039, 'subclass': 1244137190})
        self.check_not_err(n.node(data, {'railway': 'switch', 'railway:switch': 'default', 'railway:switch:resetting': 'yes'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_not_err(n.node(data, {'railway': 'switch', 'railway:switch': 'default'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_err(n.node(data, {'railway': 'switch', 'railway:switch': 'resetting', 'ref': '2'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_not_err(n.node(data, {'railway': 'switch'}), expected={'class': 9015040, 'subclass': 967663151})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'crossover'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'crossover'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'halt'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'halt'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'junction'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'junction'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'service_station'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'service_station'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'site'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'site'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'spur_junction'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'spur_junction'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'station'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'station'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'tram_stop'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'tram_stop'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.node(data, {'name': 'foo', 'railway': 'yard'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_err(n.node(data, {'railway': 'yard'}), expected={'class': 9015044, 'subclass': 1433036676})
        self.check_not_err(n.way(data, {'railway': 'rail', 'service': 'siding'}, [0]), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_not_err(n.way(data, {'railway': 'rail', 'service': 'yard', 'usage': 'industrial'}, [0]), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_err(n.way(data, {'railway': 'rail', 'service': 'siding', 'usage': 'main'}, [0]), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_not_err(n.way(data, {'railway': 'rail', 'usage': 'main'}, [0]), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_not_err(n.way(data, {'railway': 'rail', 'service': 'yard', 'usage': 'military'}, [0]), expected={'class': 9015001, 'subclass': 1888453557})
        self.check_err(n.way(data, {'railway': 'station'}, [0]), expected={'class': 9015002, 'subclass': 1498103253})
        self.check_not_err(n.way(data, {'railway': 'rail', 'railway:traffic_mode': 'passenger'}, [0]), expected={'class': 9015004, 'subclass': 1755442170})
        self.check_err(n.way(data, {'railway': 'rail', 'traffic_mode': 'passenger'}, [0]), expected={'class': 9015004, 'subclass': 1755442170})
        self.check_not_err(n.way(data, {'railway': 'rail'}, [0]), expected={'class': 9015004, 'subclass': 1755442170})
        self.check_not_err(n.way(data, {'railway': 'rail railway:traffic_mode'}, [0]), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {'railway': 'rail', 'usage': 'branch'}, [0]), expected={'class': 9015005, 'subclass': 331669407})
        self.check_err(n.way(data, {'railway': 'rail', 'railway:traffic_mode': 'freight', 'usage': 'freight'}, [0]), expected={'class': 9015005, 'subclass': 331669407})
        self.check_err(n.way(data, {'railway': 'rail', 'usage': 'freight'}, [0]), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {'railway': 'rail', 'usage': 'industrial'}, [0]), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {'railway': 'rail', 'usage': 'main'}, [0]), expected={'class': 9015005, 'subclass': 331669407})
        self.check_not_err(n.way(data, {'railway': 'rail', 'railway:traffic_mode': 'freight', 'usage': 'freight'}, [0]), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {'railway': 'rail railway:traffic_mode'}, [0]), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {'railway': 'rail', 'usage': 'branch'}, [0]), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_err(n.way(data, {'railway': 'rail', 'railway:traffic_mode': 'mixed', 'usage': 'freight'}, [0]), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_err(n.way(data, {'railway': 'rail', 'railway:traffic_mode': 'passenger', 'usage': 'freight'}, [0]), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {'railway': 'rail', 'usage': 'industrial'}, [0]), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_not_err(n.way(data, {'railway': 'rail', 'usage': 'main'}, [0]), expected={'class': 9015005, 'subclass': 1212704987})
        self.check_err(n.way(data, {'name': '14', 'railway': 'light_rail', 'railway:track_ref': '14'}, [0]), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_not_err(n.way(data, {'name': 'Gleis 14b', 'railway': 'rail', 'railway:track_ref': '14b'}, [0]), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_not_err(n.way(data, {'name': 'Gleis 14b', 'railway': 'rail'}, [0]), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {'name': '14b', 'railway': 'rail', 'railway:track_ref': '14b'}, [0]), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_not_err(n.way(data, {'name': '3', 'railway': 'rail'}, [0]), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {'name': '4', 'railway': 'rail', 'railway:track_ref': '4'}, [0]), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {'name': '4a', 'railway': 'rail', 'railway:track_ref': '4a'}, [0]), expected={'class': 9015007, 'subclass': 2091521035})
        self.check_err(n.way(data, {'name': '14', 'railway': 'light_rail'}, [0]), expected={'class': 9015007, 'subclass': 85438379})
        self.check_not_err(n.way(data, {'name': '3', 'railway': 'platform'}, [0]), expected={'class': 9015007, 'subclass': 85438379})
        self.check_not_err(n.way(data, {'name': 'Gleis 14b', 'railway': 'rail'}, [0]), expected={'class': 9015007, 'subclass': 85438379})
        self.check_not_err(n.way(data, {'name': 'track 4b', 'railway': 'rail'}, [0]), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {'name': '14b', 'railway': 'rail'}, [0]), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {'name': '4', 'railway': 'rail'}, [0]), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {'name': '4a', 'railway': 'rail'}, [0]), expected={'class': 9015007, 'subclass': 85438379})
        self.check_err(n.way(data, {'railway': 'light_rail', 'ref': '14', 'service': 'siding'}, [0]), expected={'class': 9015045, 'subclass': 194113748})
        self.check_not_err(n.way(data, {'railway': 'platform', 'ref': '3'}, [0]), expected={'class': 9015045, 'subclass': 194113748})
        self.check_not_err(n.way(data, {'railway': 'rail', 'ref': '1234'}, [0]), expected={'class': 9015045, 'subclass': 194113748})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': '4a', 'service': 'crossover'}, [0]), expected={'class': 9015045, 'subclass': 194113748})
        self.check_not_err(n.way(data, {'railway': 'rail', 'railway:track_ref': '14b', 'service': 'siding'}, [0]), expected={'class': 9015045, 'subclass': 194113748})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': '4', 'service': 'siding'}, [0]), expected={'class': 9015045, 'subclass': 194113748})
        self.check_err(n.way(data, {'railway': 'platform', 'railway:track_ref': '3', 'ref': '3'}, [0]), expected={'class': 9015008, 'subclass': 226422824})
        self.check_not_err(n.way(data, {'railway': 'platform', 'railway:track_ref': '3', 'ref': '4'}, [0]), expected={'class': 9015008, 'subclass': 226422824})
        self.check_err(n.way(data, {'railway': 'platform', 'railway:track_ref': '3'}, [0]), expected={'class': 9015008, 'subclass': 226422824})
        self.check_not_err(n.way(data, {'railway': 'rail', 'railway:track_ref': '3'}, [0]), expected={'class': 9015008, 'subclass': 226422824})
        self.check_not_err(n.way(data, {'railway': 'platform', 'railway:track_ref': '3', 'ref': '3'}, [0]), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_err(n.way(data, {'railway': 'platform', 'railway:track_ref': '3', 'ref': '4'}, [0]), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_not_err(n.way(data, {'railway': 'platform', 'railway:track_ref': '3'}, [0]), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_not_err(n.way(data, {'railway': 'rail', 'railway:track_ref': '3'}, [0]), expected={'class': 9015008, 'subclass': 1676742857})
        self.check_err(n.way(data, {'name': 'Gleis 14b', 'railway': 'rail'}, [0]), expected={'class': 9015009, 'subclass': 1420092530})
        self.check_not_err(n.way(data, {'name': '14b', 'railway': 'rail'}, [0]), expected={'class': 9015009, 'subclass': 1420092530})
        self.check_err(n.way(data, {'railway': 'rail', 'ref': 'track 4b'}, [0]), expected={'class': 9015009, 'subclass': 1420092530})
        self.check_err(n.way(data, {'description': 'Gleis 14b', 'name': 'Gleis 14b', 'railway': 'platform'}, [0]), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {'name': 'Gleis 14b', 'railway': 'platform'}, [0]), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_not_err(n.way(data, {'description': 'other', 'name': '14b', 'railway': 'platform'}, [0]), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_not_err(n.way(data, {'name': '14b', 'railway': 'platform'}, [0]), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {'railway': 'platform', 'ref': 'track 4b'}, [0]), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {'railway': 'platform', 'ref': 'track 4b'}, [0]), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_not_err(n.way(data, {'name': '14b', 'railway': 'rail'}, [0]), expected={'class': 9015010, 'subclass': 1156420508})
        self.check_err(n.way(data, {'description': 'other', 'name': 'Gleis 14b', 'railway': 'platform'}, [0]), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_not_err(n.way(data, {'description': '14b', 'name': '14b', 'railway': 'platform'}, [0]), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_not_err(n.way(data, {'name': '14b', 'railway': 'platform'}, [0]), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_err(n.way(data, {'description': 'other', 'railway': 'platform', 'ref': 'track 4b'}, [0]), expected={'class': 9015010, 'subclass': 1149450895})
        self.check_err(n.way(data, {'electrified': 'contact_line', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015011, 'subclass': 1012477221})
        self.check_not_err(n.way(data, {'electrified': 'something', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015011, 'subclass': 1012477221})
        self.check_not_err(n.way(data, {'electrified': 'something', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015011, 'subclass': 1909233042})
        self.check_err(n.way(data, {'electrified': 'yes', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015011, 'subclass': 1909233042})
        self.check_err(n.way(data, {'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015011, 'subclass': 1909233042})
        self.check_err(n.way(data, {'electrified': 'other', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015012, 'subclass': 1465196539})
        self.check_not_err(n.way(data, {'electrified': 'yes', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015012, 'subclass': 1465196539})
        self.check_not_err(n.way(data, {'electrified': 'yes', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015013, 'subclass': 356393984})
        self.check_err(n.way(data, {'electrified': 'yes', 'power:type': 'something', 'railway': 'rail'}, [0]), expected={'class': 9015013, 'subclass': 356393984})
        self.check_not_err(n.way(data, {'electrified': 'yes', 'power:type': 'overhead', 'railway': 'rail'}, [0]), expected={'class': 9015013, 'subclass': 410100568})
        self.check_err(n.way(data, {'power:type': 'something', 'railway': 'rail'}, [0]), expected={'class': 9015013, 'subclass': 410100568})
        self.check_not_err(n.way(data, {'highway': 'primary', 'priority': 'primary'}, [0]), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_err(n.way(data, {'priority': 'primary', 'railway': 'rail', 'service': 'siding'}, [0]), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_err(n.way(data, {'priority': 'primary', 'railway': 'rail', 'usage': 'main'}, [0]), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_err(n.way(data, {'priority': 'primary', 'railway': 'rail'}, [0]), expected={'class': 9015014, 'subclass': 2122288452})
        self.check_not_err(n.way(data, {'detail!': 'track', 'railway': 'rail', 'tracks': '1'}, [0]), expected={'class': 9015015, 'subclass': 986004687})
        self.check_err(n.way(data, {'detail': 'track', 'railway': 'rail', 'tracks': '1'}, [0]), expected={'class': 9015015, 'subclass': 986004687})
        self.check_not_err(n.way(data, {'detail': 'track', 'railway': 'rail', 'tracks': '2'}, [0]), expected={'class': 9015015, 'subclass': 986004687})
        self.check_not_err(n.way(data, {'railway': 'rail', 'tracks': '1'}, [0]), expected={'class': 9015016, 'subclass': 256757521})
        self.check_err(n.way(data, {'railway': 'rail', 'service': 'foo', 'tracks': '2'}, [0]), expected={'class': 9015016, 'subclass': 256757521})
        self.check_not_err(n.way(data, {'railway': 'rail', 'tracks': '2', 'usage': 'bar'}, [0]), expected={'class': 9015016, 'subclass': 256757521})
        self.check_err(n.way(data, {'railway': 'crossing', 'railway:position:exact': '2.4'}, [0]), expected={'class': 9015017, 'subclass': 2146160181})
        self.check_err(n.way(data, {'railway': 'level_crossing', 'railway:position:exact': '2.4'}, [0]), expected={'class': 9015017, 'subclass': 2146160181})
        self.check_not_err(n.way(data, {'radio': 'GSM', 'railway': 'rail'}, [0]), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_not_err(n.way(data, {'radio': 'GSM-R', 'railway': 'rail', 'railway:radio': 'gsm'}, [0]), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_err(n.way(data, {'radio': 'GSM-R', 'railway': 'rail', 'railway:radio': 'gsm-r'}, [0]), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_err(n.way(data, {'radio': 'GSM-R', 'railway': 'rail'}, [0]), expected={'class': 9015018, 'subclass': 2078132492})
        self.check_err(n.way(data, {'radio': 'GSM', 'railway': 'rail'}, [0]), expected={'class': 9015019, 'subclass': 406318522})
        self.check_err(n.way(data, {'radio': 'GSM-R', 'railway': 'rail', 'railway:radio': 'gsm'}, [0]), expected={'class': 9015019, 'subclass': 406318522})
        self.check_not_err(n.way(data, {'radio': 'GSM-R', 'railway': 'rail', 'railway:radio': 'gsm-r'}, [0]), expected={'class': 9015019, 'subclass': 406318522})
        self.check_not_err(n.way(data, {'radio': 'GSM-R', 'railway': 'rail'}, [0]), expected={'class': 9015019, 'subclass': 406318522})
        self.check_err(n.way(data, {'name': 'Bartunnel', 'railway': 'light_rail', 'tunnel:name': 'Bartunnel'}, [0]), expected={'class': 9015020, 'subclass': 1651250819})
        self.check_not_err(n.way(data, {'name': 'Footunnel', 'railway': 'platform'}, [0]), expected={'class': 9015020, 'subclass': 1651250819})
        self.check_err(n.way(data, {'name': 'Footunnel', 'railway': 'rail'}, [0]), expected={'class': 9015020, 'subclass': 1651250819})
        self.check_not_err(n.way(data, {'railway': 'rail', 'tunnel:name': 'Baztunnel'}, [0]), expected={'class': 9015020, 'subclass': 1651250819})
        self.check_err(n.way(data, {'railway': 'light_rail', 'tunnel:wikipedia': 'Bartunnel', 'wikipedia': 'Bartunnel'}, [0]), expected={'class': 9015021, 'subclass': 1581548500})
        self.check_not_err(n.way(data, {'railway': 'platform', 'wikipedia': 'Footunnel'}, [0]), expected={'class': 9015021, 'subclass': 1581548500})
        self.check_not_err(n.way(data, {'railway': 'rail', 'tunnel:wikipedia': 'Baztunnel'}, [0]), expected={'class': 9015021, 'subclass': 1581548500})
        self.check_err(n.way(data, {'railway': 'rail', 'wikipedia': 'Footunnel'}, [0]), expected={'class': 9015021, 'subclass': 1581548500})
        self.check_err(n.way(data, {'bridge:name': 'Bar bridge', 'name': 'Bar bridge', 'railway': 'light_rail'}, [0]), expected={'class': 9015022, 'subclass': 359430532})
        self.check_not_err(n.way(data, {'name': 'Noltemeyerbrücke', 'railway': 'platform'}, [0]), expected={'class': 9015022, 'subclass': 359430532})
        self.check_not_err(n.way(data, {'bridge:name': 'Foo-Viadukt', 'railway': 'rail'}, [0]), expected={'class': 9015022, 'subclass': 359430532})
        self.check_err(n.way(data, {'name': 'Bay bridge', 'railway': 'rail'}, [0]), expected={'class': 9015022, 'subclass': 359430532})
        self.check_err(n.way(data, {'name': 'Baz viaduct', 'railway': 'rail'}, [0]), expected={'class': 9015022, 'subclass': 359430532})
        self.check_err(n.way(data, {'name': 'Foobrücke', 'railway': 'rail'}, [0]), expected={'class': 9015022, 'subclass': 359430532})
        self.check_err(n.way(data, {'bridge:wikipedia': 'Bar bridge', 'railway': 'light_rail', 'wikipedia': 'Bar bridge'}, [0]), expected={'class': 9015023, 'subclass': 1594751596})
        self.check_not_err(n.way(data, {'railway': 'platform', 'wikipedia': 'Foobrücke'}, [0]), expected={'class': 9015023, 'subclass': 1594751596})
        self.check_not_err(n.way(data, {'bridge:wikipedia': 'Foo-Viadukt', 'railway': 'rail'}, [0]), expected={'class': 9015023, 'subclass': 1594751596})
        self.check_err(n.way(data, {'railway': 'rail', 'wikipedia': 'Bay bridge'}, [0]), expected={'class': 9015023, 'subclass': 1594751596})
        self.check_err(n.way(data, {'railway': 'rail', 'wikipedia': 'Baz viaduct'}, [0]), expected={'class': 9015023, 'subclass': 1594751596})
        self.check_err(n.way(data, {'railway': 'rail', 'wikipedia': 'Foobrücke'}, [0]), expected={'class': 9015023, 'subclass': 1594751596})
        self.check_not_err(n.way(data, {'highway': 'tertiary', 'lanes': '3', 'railway': 'abandoned'}, [0]), expected={'class': 9015024, 'subclass': 245965100})
        self.check_err(n.way(data, {'lanes': '2', 'railway': 'rail'}, [0]), expected={'class': 9015024, 'subclass': 245965100})
        self.check_not_err(n.way(data, {'railway': 'rail', 'tracks': '1'}, [0]), expected={'class': 9015024, 'subclass': 245965100})
        self.check_not_err(n.way(data, {'highway': 'tertiary', 'lanes': '3', 'railway': 'razed'}, [0]), expected={'class': 9015024, 'subclass': 245965100})
        self.check_err(n.way(data, {'lanes': '2', 'railway': 'subway', 'tracks': '2'}, [0]), expected={'class': 9015024, 'subclass': 245965100})
        self.check_err(n.way(data, {'maxspeed': 'signals', 'railway': 'rail'}, [0]), expected={'class': 9015025, 'subclass': 650821308})
        self.check_not_err(n.way(data, {'maxspeed': '100', 'railway': 'subway'}, [0]), expected={'class': 9015025, 'subclass': 650821308})
        self.check_not_err(n.way(data, {'maxspeed': '161', 'mph:maxspeed': '50 mph', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 317587071})
        self.check_not_err(n.way(data, {'mph:maxspeed': '50 mph', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 317587071})
        self.check_not_err(n.way(data, {'mph:maxspeed': '50', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 317587071})
        self.check_err(n.way(data, {'maxspeed': '161', 'mph:maxspeed': '100', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 317587071})
        self.check_err(n.way(data, {'maxspeed': '161', 'mph:maxspeed': '50 mph', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_not_err(n.way(data, {'mph:maxspeed': '50 mph', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_not_err(n.way(data, {'mph:maxspeed': '50', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_not_err(n.way(data, {'maxspeed': '161', 'mph:maxspeed': '100', 'railway': 'rail'}, [0]), expected={'class': 9015026, 'subclass': 2074447149})
        self.check_err(n.relation(data, {'railway': 'controlled_area'}, []), expected={'class': 9015041, 'subclass': 53808548})
        self.check_not_err(n.relation(data, {'railway': 'interlocking'}, []), expected={'class': 9015041, 'subclass': 53808548})
        self.check_not_err(n.relation(data, {'railway': 'interlocking', 'type': 'railway'}, []), expected={'class': 9015042, 'subclass': 1490437342})
        self.check_err(n.relation(data, {'railway': 'interlocking'}, []), expected={'class': 9015042, 'subclass': 1490437342})
        self.check_err(n.relation(data, {'railway': 'interlocking', 'type': 'public_transport'}, []), expected={'class': 9015043, 'subclass': 1419769139})
        self.check_not_err(n.relation(data, {'railway': 'interlocking', 'type': 'railway'}, []), expected={'class': 9015043, 'subclass': 1419769139})
