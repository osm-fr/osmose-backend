#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_multiple(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9005001] = {'item': 9005, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} with multiple values', capture_tags, u'{0.key}')}
        self.errors[9005002] = {'item': 9005, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'empty value in semicolon-separated \'\'{0}\'\'', capture_tags, u'{0.key}')}

        self.re_53db61ac = re.compile(ur'.+;(.+)?')
        self.re_579c7c6a = re.compile(ur'^(;.*|.*;;.*|.*;)$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["addr:street"=~/.+;(.+)?/]
        # *[highway=~/.+;(.+)?/]
        # *[lanes=~/.+;(.+)?/]
        # *[maxspeed=~/.+;(.+)?/]
        # *[name=~/.+;(.+)?/]
        # *[surface=~/.+;(.+)?/]
        # *[water=~/.+;(.+)?/]
        if (u'addr:street' in keys or u'highway' in keys or u'lanes' in keys or u'maxspeed' in keys or u'name' in keys or u'surface' in keys or u'water' in keys) and \
            ((mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'highway'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'lanes'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'surface'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'water')))):
            # throwWarning:tr("{0} with multiple values","{0.key}")
            err.append({'class': 9005001, 'subclass': 1911063816, 'text': mapcss.tr(u'{0} with multiple values', capture_tags, u'{0.key}')})

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
        # *[cuisine=~/^(;.*|.*;;.*|.*;)$/]
        if (u'addr:housenumber' in keys or u'alt_name' in keys or u'attribution' in keys or u'building:use' in keys or u'cuisine' in keys or u'destination' in keys or u'exit_to' in keys or u'fixme' in keys or u'int_ref' in keys or u'name' in keys or u'note' in keys or u'old_ref' in keys or u'ref' in keys or u'route_ref' in keys or u'source' in keys or u'source:addr' in keys or u'source:maxspeed' in keys or u'source:name' in keys or u'source:position' in keys or u'source:postcode' in keys or u'source_ref' in keys or u'surface' in keys or u'traffic_sign' in keys or u'voltage' in keys) and \
            ((mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:addr'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:position'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:postcode'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'int_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'old_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'route_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'attribution'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'alt_name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'note'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'fixme'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'destination'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'exit_to'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'surface'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'building:use'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'traffic_sign'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'voltage'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'cuisine')))):
            # throwWarning:tr("empty value in semicolon-separated ''{0}''","{0.key}")
            # assertMatch:"node ref=;"
            # assertMatch:"node ref=;A1"
            # assertNoMatch:"node ref=A1"
            # assertMatch:"node ref=A1;"
            # assertMatch:"node ref=A1;;A2"
            # assertNoMatch:"node ref=A1;A2"
            err.append({'class': 9005002, 'subclass': 978530936, 'text': mapcss.tr(u'empty value in semicolon-separated \'\'{0}\'\'', capture_tags, u'{0.key}')})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["addr:street"=~/.+;(.+)?/]
        # *[highway=~/.+;(.+)?/]
        # *[lanes=~/.+;(.+)?/]
        # *[maxspeed=~/.+;(.+)?/]
        # *[name=~/.+;(.+)?/]
        # *[surface=~/.+;(.+)?/]
        # *[water=~/.+;(.+)?/]
        if (u'addr:street' in keys or u'highway' in keys or u'lanes' in keys or u'maxspeed' in keys or u'name' in keys or u'surface' in keys or u'water' in keys) and \
            ((mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'highway'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'lanes'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'surface'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'water')))):
            # throwWarning:tr("{0} with multiple values","{0.key}")
            err.append({'class': 9005001, 'subclass': 1911063816, 'text': mapcss.tr(u'{0} with multiple values', capture_tags, u'{0.key}')})

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
        # *[cuisine=~/^(;.*|.*;;.*|.*;)$/]
        if (u'addr:housenumber' in keys or u'alt_name' in keys or u'attribution' in keys or u'building:use' in keys or u'cuisine' in keys or u'destination' in keys or u'exit_to' in keys or u'fixme' in keys or u'int_ref' in keys or u'name' in keys or u'note' in keys or u'old_ref' in keys or u'ref' in keys or u'route_ref' in keys or u'source' in keys or u'source:addr' in keys or u'source:maxspeed' in keys or u'source:name' in keys or u'source:position' in keys or u'source:postcode' in keys or u'source_ref' in keys or u'surface' in keys or u'traffic_sign' in keys or u'voltage' in keys) and \
            ((mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:addr'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:position'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:postcode'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'int_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'old_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'route_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'attribution'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'alt_name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'note'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'fixme'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'destination'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'exit_to'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'surface'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'building:use'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'traffic_sign'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'voltage'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'cuisine')))):
            # throwWarning:tr("empty value in semicolon-separated ''{0}''","{0.key}")
            err.append({'class': 9005002, 'subclass': 978530936, 'text': mapcss.tr(u'empty value in semicolon-separated \'\'{0}\'\'', capture_tags, u'{0.key}')})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["addr:street"=~/.+;(.+)?/]
        # *[highway=~/.+;(.+)?/]
        # *[lanes=~/.+;(.+)?/]
        # *[maxspeed=~/.+;(.+)?/]
        # *[name=~/.+;(.+)?/]
        # *[surface=~/.+;(.+)?/]
        # *[water=~/.+;(.+)?/]
        if (u'addr:street' in keys or u'highway' in keys or u'lanes' in keys or u'maxspeed' in keys or u'name' in keys or u'surface' in keys or u'water' in keys) and \
            ((mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'highway'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'lanes'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'surface'))) or \
            (mapcss.regexp_test_(self.re_53db61ac, mapcss._tag_capture(capture_tags, 0, tags, u'water')))):
            # throwWarning:tr("{0} with multiple values","{0.key}")
            err.append({'class': 9005001, 'subclass': 1911063816, 'text': mapcss.tr(u'{0} with multiple values', capture_tags, u'{0.key}')})

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
        # *[cuisine=~/^(;.*|.*;;.*|.*;)$/]
        if (u'addr:housenumber' in keys or u'alt_name' in keys or u'attribution' in keys or u'building:use' in keys or u'cuisine' in keys or u'destination' in keys or u'exit_to' in keys or u'fixme' in keys or u'int_ref' in keys or u'name' in keys or u'note' in keys or u'old_ref' in keys or u'ref' in keys or u'route_ref' in keys or u'source' in keys or u'source:addr' in keys or u'source:maxspeed' in keys or u'source:name' in keys or u'source:position' in keys or u'source:postcode' in keys or u'source_ref' in keys or u'surface' in keys or u'traffic_sign' in keys or u'voltage' in keys) and \
            ((mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:addr'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:position'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source:postcode'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'int_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'old_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'source_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'route_ref'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'attribution'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'alt_name'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'note'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'fixme'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'destination'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'exit_to'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'surface'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'building:use'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'traffic_sign'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'voltage'))) or \
            (mapcss.regexp_test_(self.re_579c7c6a, mapcss._tag_capture(capture_tags, 0, tags, u'cuisine')))):
            # throwWarning:tr("empty value in semicolon-separated ''{0}''","{0.key}")
            err.append({'class': 9005002, 'subclass': 978530936, 'text': mapcss.tr(u'empty value in semicolon-separated \'\'{0}\'\'', capture_tags, u'{0.key}')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_multiple(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'ref': u';'}), expected={'class': 9005002, 'subclass': 978530936})
        self.check_err(n.node(data, {u'ref': u';A1'}), expected={'class': 9005002, 'subclass': 978530936})
        self.check_not_err(n.node(data, {u'ref': u'A1'}), expected={'class': 9005002, 'subclass': 978530936})
        self.check_err(n.node(data, {u'ref': u'A1;'}), expected={'class': 9005002, 'subclass': 978530936})
        self.check_err(n.node(data, {u'ref': u'A1;;A2'}), expected={'class': 9005002, 'subclass': 978530936})
        self.check_not_err(n.node(data, {u'ref': u'A1;A2'}), expected={'class': 9005002, 'subclass': 978530936})
