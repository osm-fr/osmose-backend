#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Construction2(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[40701] = self.def_class(item = 4070, level = 2, tags = mapcss.list_('tag', 'highway', 'fix:survey'), title = mapcss.tr('Inconsistent tagging of {0}', mapcss._tag_uncapture(capture_tags, '{1.key}')))



    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[highway][proposed][highway!=proposed]
        # way[railway][proposed][railway!=proposed][railway!=abandoned][railway!=razed][railway!=dismantled][railway!=disused]
        if ('highway' in keys and 'proposed' in keys) or ('proposed' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'proposed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'proposed', 'proposed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'proposed')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway') != mapcss._value_const_capture(capture_tags, 2, 'proposed', 'proposed')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway') != mapcss._value_const_capture(capture_tags, 3, 'abandoned', 'abandoned')) and (mapcss._tag_capture(capture_tags, 4, tags, 'railway') != mapcss._value_const_capture(capture_tags, 4, 'razed', 'razed')) and (mapcss._tag_capture(capture_tags, 5, tags, 'railway') != mapcss._value_const_capture(capture_tags, 5, 'dismantled', 'dismantled')) and (mapcss._tag_capture(capture_tags, 6, tags, 'railway') != mapcss._value_const_capture(capture_tags, 6, 'disused', 'disused')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4070/40701/2"
                # throwError:tr("Inconsistent tagging of {0}","{1.key}")
                # assertMatch:"way highway=primary proposed=secondary"
                # assertNoMatch:"way highway=proposed proposed=primary"
                err.append({'class': 40701, 'subclass': 0, 'text': mapcss.tr('Inconsistent tagging of {0}', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Construction2(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {'highway': 'primary', 'proposed': 'secondary'}, [0]), expected={'class': 40701, 'subclass': 0})
        self.check_not_err(n.way(data, {'highway': 'proposed', 'proposed': 'primary'}, [0]), expected={'class': 40701, 'subclass': 0})
