#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_multiple(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/multiple.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9005001] = self.def_class(item = 9005, level = 3, tags = ["tag", "value"], title = mapcss.tr('{0} with multiple values', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9005002] = self.def_class(item = 9005, level = 3, tags = ["tag", "value"], title = mapcss.tr('empty value in semicolon-separated \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')))

        self.re_53db61ac = re.compile(r'.+;(.+)?')
        self.re_579c7c6a = re.compile(r'^(;.*|.*;;.*|.*;)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["telecom:medium"=~/.+;(.+)?/]
        # *["addr:street"=~/.+;(.+)?/]
        # *[highway=~/.+;(.+)?/]
        # *[lanes=~/.+;(.+)?/]
        # *[maxspeed=~/.+;(.+)?/]
        # *[name=~/.+;(.+)?/]
        # *[surface=~/.+;(.+)?/]
        # *[water=~/.+;(.+)?/]
        if ('addr:street' in keys) or ('highway' in keys) or ('lanes' in keys) or ('maxspeed' in keys) or ('name' in keys) or ('surface' in keys) or ('telecom:medium' in keys) or ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'telecom:medium'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'lanes'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'water'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} with multiple values","{0.key}")
                err.append({'class': 9005001, 'subclass': 126367661, 'text': mapcss.tr('{0} with multiple values', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[source=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:addr"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:maxspeed"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:name"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:position"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:postcode"=~/^(;.*|.*;;.*|.*;)$/]
        # *[ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[int_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[old_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[source_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[route_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[attribution=~/^(;.*|.*;;.*|.*;)$/]
        # *[name=~/^(;.*|.*;;.*|.*;)$/]
        # *[alt_name=~/^(;.*|.*;;.*|.*;)$/]
        # *[note=~/^(;.*|.*;;.*|.*;)$/]
        # *[fixme=~/^(;.*|.*;;.*|.*;)$/]
        # *["addr:housenumber"=~/^(;.*|.*;;.*|.*;)$/]
        # *[destination=~/^(;.*|.*;;.*|.*;)$/]
        # *[exit_to=~/^(;.*|.*;;.*|.*;)$/]
        # *[surface=~/^(;.*|.*;;.*|.*;)$/]
        # *["building:use"=~/^(;.*|.*;;.*|.*;)$/]
        # *[traffic_sign=~/^(;.*|.*;;.*|.*;)$/]
        # *[voltage=~/^(;.*|.*;;.*|.*;)$/]
        # *[sport=~/^(;.*|.*;;.*|.*;)$/]
        # *[cuisine=~/^(;.*|.*;;.*|.*;)$/]
        if ('addr:housenumber' in keys) or ('alt_name' in keys) or ('attribution' in keys) or ('building:use' in keys) or ('cuisine' in keys) or ('destination' in keys) or ('exit_to' in keys) or ('fixme' in keys) or ('int_ref' in keys) or ('name' in keys) or ('note' in keys) or ('old_ref' in keys) or ('ref' in keys) or ('route_ref' in keys) or ('source' in keys) or ('source:addr' in keys) or ('source:maxspeed' in keys) or ('source:name' in keys) or ('source:position' in keys) or ('source:postcode' in keys) or ('source_ref' in keys) or ('sport' in keys) or ('surface' in keys) or ('traffic_sign' in keys) or ('voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:addr'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:position'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:postcode'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'int_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'old_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'route_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'attribution'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'alt_name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'note'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'fixme'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'addr:housenumber'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'destination'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'exit_to'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'building:use'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'voltage'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'sport'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("empty value in semicolon-separated ''{0}''","{0.key}")
                # assertMatch:"node ref=;"
                # assertMatch:"node ref=;A1"
                # assertNoMatch:"node ref=A1"
                # assertMatch:"node ref=A1;"
                # assertMatch:"node ref=A1;;A2"
                # assertNoMatch:"node ref=A1;A2"
                err.append({'class': 9005002, 'subclass': 1082723721, 'text': mapcss.tr('empty value in semicolon-separated \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["telecom:medium"=~/.+;(.+)?/]
        # *["addr:street"=~/.+;(.+)?/]
        # *[highway=~/.+;(.+)?/]
        # *[lanes=~/.+;(.+)?/]
        # *[maxspeed=~/.+;(.+)?/]
        # *[name=~/.+;(.+)?/]
        # *[surface=~/.+;(.+)?/]
        # *[water=~/.+;(.+)?/]
        if ('addr:street' in keys) or ('highway' in keys) or ('lanes' in keys) or ('maxspeed' in keys) or ('name' in keys) or ('surface' in keys) or ('telecom:medium' in keys) or ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'telecom:medium'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'lanes'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'water'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} with multiple values","{0.key}")
                err.append({'class': 9005001, 'subclass': 126367661, 'text': mapcss.tr('{0} with multiple values', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[source=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:addr"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:maxspeed"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:name"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:position"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:postcode"=~/^(;.*|.*;;.*|.*;)$/]
        # *[ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[int_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[old_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[source_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[route_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[attribution=~/^(;.*|.*;;.*|.*;)$/]
        # *[name=~/^(;.*|.*;;.*|.*;)$/]
        # *[alt_name=~/^(;.*|.*;;.*|.*;)$/]
        # *[note=~/^(;.*|.*;;.*|.*;)$/]
        # *[fixme=~/^(;.*|.*;;.*|.*;)$/]
        # *["addr:housenumber"=~/^(;.*|.*;;.*|.*;)$/]
        # *[destination=~/^(;.*|.*;;.*|.*;)$/]
        # *[exit_to=~/^(;.*|.*;;.*|.*;)$/]
        # *[surface=~/^(;.*|.*;;.*|.*;)$/]
        # *["building:use"=~/^(;.*|.*;;.*|.*;)$/]
        # *[traffic_sign=~/^(;.*|.*;;.*|.*;)$/]
        # *[voltage=~/^(;.*|.*;;.*|.*;)$/]
        # *[sport=~/^(;.*|.*;;.*|.*;)$/]
        # *[cuisine=~/^(;.*|.*;;.*|.*;)$/]
        if ('addr:housenumber' in keys) or ('alt_name' in keys) or ('attribution' in keys) or ('building:use' in keys) or ('cuisine' in keys) or ('destination' in keys) or ('exit_to' in keys) or ('fixme' in keys) or ('int_ref' in keys) or ('name' in keys) or ('note' in keys) or ('old_ref' in keys) or ('ref' in keys) or ('route_ref' in keys) or ('source' in keys) or ('source:addr' in keys) or ('source:maxspeed' in keys) or ('source:name' in keys) or ('source:position' in keys) or ('source:postcode' in keys) or ('source_ref' in keys) or ('sport' in keys) or ('surface' in keys) or ('traffic_sign' in keys) or ('voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:addr'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:position'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:postcode'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'int_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'old_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'route_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'attribution'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'alt_name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'note'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'fixme'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'addr:housenumber'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'destination'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'exit_to'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'building:use'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'voltage'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'sport'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("empty value in semicolon-separated ''{0}''","{0.key}")
                err.append({'class': 9005002, 'subclass': 1082723721, 'text': mapcss.tr('empty value in semicolon-separated \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["telecom:medium"=~/.+;(.+)?/]
        # *["addr:street"=~/.+;(.+)?/]
        # *[highway=~/.+;(.+)?/]
        # *[lanes=~/.+;(.+)?/]
        # *[maxspeed=~/.+;(.+)?/]
        # *[name=~/.+;(.+)?/]
        # *[surface=~/.+;(.+)?/]
        # *[water=~/.+;(.+)?/]
        if ('addr:street' in keys) or ('highway' in keys) or ('lanes' in keys) or ('maxspeed' in keys) or ('name' in keys) or ('surface' in keys) or ('telecom:medium' in keys) or ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'telecom:medium'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'lanes'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53db61ac), mapcss._tag_capture(capture_tags, 0, tags, 'water'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} with multiple values","{0.key}")
                err.append({'class': 9005001, 'subclass': 126367661, 'text': mapcss.tr('{0} with multiple values', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[source=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:addr"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:maxspeed"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:name"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:position"=~/^(;.*|.*;;.*|.*;)$/]
        # *["source:postcode"=~/^(;.*|.*;;.*|.*;)$/]
        # *[ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[int_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[old_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[source_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[route_ref=~/^(;.*|.*;;.*|.*;)$/]
        # *[attribution=~/^(;.*|.*;;.*|.*;)$/]
        # *[name=~/^(;.*|.*;;.*|.*;)$/]
        # *[alt_name=~/^(;.*|.*;;.*|.*;)$/]
        # *[note=~/^(;.*|.*;;.*|.*;)$/]
        # *[fixme=~/^(;.*|.*;;.*|.*;)$/]
        # *["addr:housenumber"=~/^(;.*|.*;;.*|.*;)$/]
        # *[destination=~/^(;.*|.*;;.*|.*;)$/]
        # *[exit_to=~/^(;.*|.*;;.*|.*;)$/]
        # *[surface=~/^(;.*|.*;;.*|.*;)$/]
        # *["building:use"=~/^(;.*|.*;;.*|.*;)$/]
        # *[traffic_sign=~/^(;.*|.*;;.*|.*;)$/]
        # *[voltage=~/^(;.*|.*;;.*|.*;)$/]
        # *[sport=~/^(;.*|.*;;.*|.*;)$/]
        # *[cuisine=~/^(;.*|.*;;.*|.*;)$/]
        if ('addr:housenumber' in keys) or ('alt_name' in keys) or ('attribution' in keys) or ('building:use' in keys) or ('cuisine' in keys) or ('destination' in keys) or ('exit_to' in keys) or ('fixme' in keys) or ('int_ref' in keys) or ('name' in keys) or ('note' in keys) or ('old_ref' in keys) or ('ref' in keys) or ('route_ref' in keys) or ('source' in keys) or ('source:addr' in keys) or ('source:maxspeed' in keys) or ('source:name' in keys) or ('source:position' in keys) or ('source:postcode' in keys) or ('source_ref' in keys) or ('sport' in keys) or ('surface' in keys) or ('traffic_sign' in keys) or ('voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:addr'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:position'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source:postcode'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'int_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'old_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'source_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'route_ref'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'attribution'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'alt_name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'note'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'fixme'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'addr:housenumber'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'destination'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'exit_to'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'building:use'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'voltage'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'sport'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_579c7c6a), mapcss._tag_capture(capture_tags, 0, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("empty value in semicolon-separated ''{0}''","{0.key}")
                err.append({'class': 9005002, 'subclass': 1082723721, 'text': mapcss.tr('empty value in semicolon-separated \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_multiple(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'ref': ';'}), expected={'class': 9005002, 'subclass': 1082723721}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.node(data, {'ref': ';A1'}), expected={'class': 9005002, 'subclass': 1082723721}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'ref': 'A1'}), expected={'class': 9005002, 'subclass': 1082723721}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.node(data, {'ref': 'A1;'}), expected={'class': 9005002, 'subclass': 1082723721}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.node(data, {'ref': 'A1;;A2'}), expected={'class': 9005002, 'subclass': 1082723721}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'ref': 'A1;A2'}), expected={'class': 9005002, 'subclass': 1082723721}, disallowed_str_in_text = ['{', '}'])
