#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Construction2(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[40701] = self.def_class(item = 4070, level = 1, tags = mapcss.list_(u'tag', u'highway', u'fix:survey'), title = mapcss.tr(u'Inconsistent tagging of {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}')))



    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[highway][construction][highway!=construction][construction!=minor]
        # way[highway][proposed][highway!=proposed]
        # way[railway][construction][railway!=construction][railway!=abandoned][railway!=razed][railway!=dismantled][construction!=minor]
        # way[railway][proposed][railway!=proposed][railway!=abandoned][railway!=razed][railway!=dismantled][railway!=disused]
        if (u'construction' in keys and u'highway' in keys) or (u'construction' in keys and u'railway' in keys) or (u'highway' in keys and u'proposed' in keys) or (u'proposed' in keys and u'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'construction') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_const_capture(capture_tags, 2, u'construction', u'construction') and mapcss._tag_capture(capture_tags, 3, tags, u'construction') != mapcss._value_const_capture(capture_tags, 3, u'minor', u'minor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'proposed') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_const_capture(capture_tags, 2, u'proposed', u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'construction') and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != mapcss._value_const_capture(capture_tags, 2, u'construction', u'construction') and mapcss._tag_capture(capture_tags, 3, tags, u'railway') != mapcss._value_const_capture(capture_tags, 3, u'abandoned', u'abandoned') and mapcss._tag_capture(capture_tags, 4, tags, u'railway') != mapcss._value_const_capture(capture_tags, 4, u'razed', u'razed') and mapcss._tag_capture(capture_tags, 5, tags, u'railway') != mapcss._value_const_capture(capture_tags, 5, u'dismantled', u'dismantled') and mapcss._tag_capture(capture_tags, 6, tags, u'construction') != mapcss._value_const_capture(capture_tags, 6, u'minor', u'minor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') and mapcss._tag_capture(capture_tags, 1, tags, u'proposed') and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != mapcss._value_const_capture(capture_tags, 2, u'proposed', u'proposed') and mapcss._tag_capture(capture_tags, 3, tags, u'railway') != mapcss._value_const_capture(capture_tags, 3, u'abandoned', u'abandoned') and mapcss._tag_capture(capture_tags, 4, tags, u'railway') != mapcss._value_const_capture(capture_tags, 4, u'razed', u'razed') and mapcss._tag_capture(capture_tags, 5, tags, u'railway') != mapcss._value_const_capture(capture_tags, 5, u'dismantled', u'dismantled') and mapcss._tag_capture(capture_tags, 6, tags, u'railway') != mapcss._value_const_capture(capture_tags, 6, u'disused', u'disused'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4070/40701/1"
                # throwError:tr("Inconsistent tagging of {0}","{1.key}")
                # assertNoMatch:"way highway=construction construction=primary"
                # assertNoMatch:"way highway=primary construction=minor"
                # assertMatch:"way highway=primary construction=primary"
                err.append({'class': 40701, 'subclass': 0, 'text': mapcss.tr(u'Inconsistent tagging of {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

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

        self.check_not_err(n.way(data, {u'construction': u'primary', u'highway': u'construction'}, [0]), expected={'class': 40701, 'subclass': 0})
        self.check_not_err(n.way(data, {u'construction': u'minor', u'highway': u'primary'}, [0]), expected={'class': 40701, 'subclass': 0})
        self.check_err(n.way(data, {u'construction': u'primary', u'highway': u'primary'}, [0]), expected={'class': 40701, 'subclass': 0})
