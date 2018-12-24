#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_addresses(Plugin):


    not_for = ['CA']

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9000003] = {'item': 9000, 'level': 3, 'tag': ["tag", "addr"], 'desc': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housename' in keys and u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                # assertMatch:"node addr:housename=1 addr:housenumber=1"
                # assertNoMatch:"node addr:housename=1 addr:housenumber=2"
                err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housename' in keys and u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housename' in keys and u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_addresses(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'addr:housename': u'1', u'addr:housenumber': u'1'}), expected={'class': 9000003, 'subclass': 1820984183})
        self.check_not_err(n.node(data, {u'addr:housename': u'1', u'addr:housenumber': u'2'}), expected={'class': 9000003, 'subclass': 1820984183})
