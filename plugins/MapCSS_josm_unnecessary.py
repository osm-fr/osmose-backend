#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_unnecessary(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9010001] = {'item': 9010, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'unnecessary tag', capture_tags)}
        self.errors[9010002] = {'item': 9010, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} makes no sense', capture_tags, u'{0.tag')}

        self.re_3ad9e1f5 = re.compile(ur'^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][vehicle!=no][access!=no][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if (u'access' in keys or u'bridge' in keys or u'building' in keys or u'elevation' in keys or u'layer' in keys or u'motor_vehicle' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == u'proposed') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') != u'no' and mapcss._tag_capture(capture_tags, 2, tags, u'access') != u'no' and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != u'yes' and mapcss.regexp_test_(self.re_3ad9e1f5, mapcss._tag_capture(capture_tags, 4, tags, u'highway'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == u'no') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'building') == u'no') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == u'0') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == u'0')):
            # group:tr("unnecessary tag")
            # throwWarning:tr("{0} is unnecessary","{0.tag}")
            # fixRemove:"{0.key}"
            err.append({'class': 9010001, 'subclass': 1949087363, 'text': mapcss.tr(u'{0} is unnecessary', capture_tags, u'{0.tag}'), 'fix': {
                '-': ([
                    u'{0.key}'])
            }})

        # *[emergency=permissive]
        if (u'emergency' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == u'permissive')):
            # throwWarning:tr("{0} makes no sense","{0.tag")
            # fixAdd:"emergency=yes"
            err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', capture_tags, u'{0.tag'), 'fix': {
                '+': dict([
                    [u'emergency',u'yes']])
            }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))):
            # group:tr("unnecessary tag")
            # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
            # fixRemove:"payment:cash"
            err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}'), 'fix': {
                '-': ([
                    u'payment:cash'])
            }})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][vehicle!=no][access!=no][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if (u'access' in keys or u'bridge' in keys or u'building' in keys or u'elevation' in keys or u'layer' in keys or u'motor_vehicle' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == u'proposed') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') != u'no' and mapcss._tag_capture(capture_tags, 2, tags, u'access') != u'no' and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != u'yes' and mapcss.regexp_test_(self.re_3ad9e1f5, mapcss._tag_capture(capture_tags, 4, tags, u'highway'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == u'no') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'building') == u'no') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == u'0') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == u'0')):
            # group:tr("unnecessary tag")
            # throwWarning:tr("{0} is unnecessary","{0.tag}")
            # fixRemove:"{0.key}"
            # assertMatch:"way bridge=no"
            # assertMatch:"way highway=proposed access=no"
            # assertMatch:"way layer=0"
            err.append({'class': 9010001, 'subclass': 1949087363, 'text': mapcss.tr(u'{0} is unnecessary', capture_tags, u'{0.tag}'), 'fix': {
                '-': ([
                    u'{0.key}'])
            }})

        # *[emergency=permissive]
        if (u'emergency' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == u'permissive')):
            # throwWarning:tr("{0} makes no sense","{0.tag")
            # fixAdd:"emergency=yes"
            # assertNoMatch:"way emergency=designated"
            # assertMatch:"way emergency=permissive"
            err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', capture_tags, u'{0.tag'), 'fix': {
                '+': dict([
                    [u'emergency',u'yes']])
            }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))):
            # group:tr("unnecessary tag")
            # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
            # fixRemove:"payment:cash"
            err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}'), 'fix': {
                '-': ([
                    u'payment:cash'])
            }})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][vehicle!=no][access!=no][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if (u'access' in keys or u'bridge' in keys or u'building' in keys or u'elevation' in keys or u'layer' in keys or u'motor_vehicle' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == u'proposed') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') != u'no' and mapcss._tag_capture(capture_tags, 2, tags, u'access') != u'no' and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != u'yes' and mapcss.regexp_test_(self.re_3ad9e1f5, mapcss._tag_capture(capture_tags, 4, tags, u'highway'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == u'no') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'building') == u'no') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == u'0') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == u'0')):
            # group:tr("unnecessary tag")
            # throwWarning:tr("{0} is unnecessary","{0.tag}")
            # fixRemove:"{0.key}"
            err.append({'class': 9010001, 'subclass': 1949087363, 'text': mapcss.tr(u'{0} is unnecessary', capture_tags, u'{0.tag}'), 'fix': {
                '-': ([
                    u'{0.key}'])
            }})

        # *[emergency=permissive]
        if (u'emergency' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == u'permissive')):
            # throwWarning:tr("{0} makes no sense","{0.tag")
            # fixAdd:"emergency=yes"
            err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', capture_tags, u'{0.tag'), 'fix': {
                '+': dict([
                    [u'emergency',u'yes']])
            }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))):
            # group:tr("unnecessary tag")
            # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
            # fixRemove:"payment:cash"
            err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}'), 'fix': {
                '-': ([
                    u'payment:cash'])
            }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_unnecessary(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {u'bridge': u'no'}), expected={'class': 9010001, 'subclass': 1949087363})
        self.check_err(n.way(data, {u'access': u'no', u'highway': u'proposed'}), expected={'class': 9010001, 'subclass': 1949087363})
        self.check_err(n.way(data, {u'layer': u'0'}), expected={'class': 9010001, 'subclass': 1949087363})
        self.check_not_err(n.way(data, {u'emergency': u'designated'}), expected={'class': 9010002, 'subclass': 325672362})
        self.check_err(n.way(data, {u'emergency': u'permissive'}), expected={'class': 9010002, 'subclass': 325672362})
