#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Rules_FranceSpecificRules(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9016030] = {'item': 9016, 'level': 3, 'tag': ['railway', 'fix:chair'], 'desc': mapcss.tr(u'Tag gauge manquant sur rail')}



    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[railway=rail][!gauge][inside("FR")]
        if (u'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'rail') and not mapcss._tag_capture(capture_tags, 1, tags, u'gauge') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Tag gauge manquant sur rail")
                # suggestAlternative:"gauge"
                # assertNoMatch:"way railway=disused"
                # assertNoMatch:"way railway=rail gauge=1435"
                # assertMatch:"way railway=rail"
                err.append({'class': 9016030, 'subclass': 941231690, 'text': mapcss.tr(u'Tag gauge manquant sur rail')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Rules_FranceSpecificRules(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.way(data, {u'railway': u'disused'}, [0]), expected={'class': 9016030, 'subclass': 941231690})
        self.check_not_err(n.way(data, {u'gauge': u'1435', u'railway': u'rail'}, [0]), expected={'class': 9016030, 'subclass': 941231690})
        self.check_err(n.way(data, {u'railway': u'rail'}, [0]), expected={'class': 9016030, 'subclass': 941231690})
