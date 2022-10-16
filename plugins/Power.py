#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Power(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[91001] = self.def_class(item = 9100, level = 2, tags = mapcss.list_('power', 'fix:chair') + mapcss.list_('geom'), title = mapcss.tr('Power Transformers should always be on a node'))
        self.errors[91002] = self.def_class(item = 9100, level = 2, tags = mapcss.list_('power', 'fix:chair') + mapcss.list_('tag'), title = mapcss.tr('On Power Transformers use voltage:primary=* and voltage:secondary=* in place of voltage'))
        self.errors[91003] = self.def_class(item = 9100, level = 3, tags = mapcss.list_('power', 'fix:chair') + mapcss.list_('tag'), title = mapcss.tr('Power Transformers should have a frequency tag'))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[power=transformer][voltage]
        if ('power' in keys and 'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'transformer')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag")
                # -osmoseItemClassLevel:"9100/91002/2"
                # throwWarning:tr("On Power Transformers use voltage:primary=* and voltage:secondary=* in place of voltage")
                err.append({'class': 91002, 'subclass': 0, 'text': mapcss.tr('On Power Transformers use voltage:primary=* and voltage:secondary=* in place of voltage')})

        # node[power=transformer][!frequency]
        if ('power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'transformer')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'frequency')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag")
                # -osmoseItemClassLevel:"9100/91003/3"
                # throwWarning:tr("Power Transformers should have a frequency tag")
                # assertNoMatch:"node power=transformer frequency=50"
                # assertMatch:"node power=transformer"
                err.append({'class': 91003, 'subclass': 0, 'text': mapcss.tr('Power Transformers should have a frequency tag')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[power=transformer]
        if ('power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'transformer')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("geom")
                # -osmoseItemClassLevel:"9100/91001/2"
                # throwWarning:tr("Power Transformers should always be on a node")
                err.append({'class': 91001, 'subclass': 0, 'text': mapcss.tr('Power Transformers should always be on a node')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Power(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {'frequency': '50', 'power': 'transformer'}), expected={'class': 91003, 'subclass': 0})
        self.check_err(n.node(data, {'power': 'transformer'}), expected={'class': 91003, 'subclass': 0}, disallowed_str_in_text = ['{', '}'])
