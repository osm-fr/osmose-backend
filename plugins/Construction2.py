#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Construction2(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[40701] = {'item': 4070, 'level': 1, 'tag': mapcss.list_(u'tag', u'highway'), 'desc': mapcss.tr(u'Inconsistent tagging of {0}', capture_tags, u'{1.key}')}



    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[highway][construction][highway!=construction]
        # way[highway][proposed][highway!=proposed]
        # way[railway][construction][railway!=construction]
        # way[railway][proposed][railway!=proposed]
        if u'highway' in keys or u'railway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'construction') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'construction')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'proposed') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'proposed')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'construction') and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != mapcss._value_capture(capture_tags, 2, u'construction')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'proposed') and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != mapcss._value_capture(capture_tags, 2, u'proposed')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway")
                # osmoseItemClassLevel:"4070/40701/1"
                # throwError:tr("Inconsistent tagging of {0}","{1.key}")
                # assertNoMatch:"way highway=construction construction=primary"
                # assertMatch:"way highway=primary construction=primary"
                err.append({'class': 40701, 'subclass': 0, 'text': mapcss.tr(u'Inconsistent tagging of {0}', capture_tags, u'{1.key}')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Construction2(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.way(data, {u'construction': u'primary', u'highway': u'construction'}), expected={'class': 40701, 'subclass': 0})
        self.check_err(n.way(data, {u'construction': u'primary', u'highway': u'primary'}), expected={'class': 40701, 'subclass': 0})
