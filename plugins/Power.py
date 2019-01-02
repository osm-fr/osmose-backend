#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Power(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[91001] = {'item': 9100, 'level': 2, 'tag': mapcss.list_(u'power', u'fix:chair') + mapcss.list_(u'geom'), 'desc': mapcss.tr(u'Power Transformers should always be on a node')}
        self.errors[91002] = {'item': 9100, 'level': 2, 'tag': mapcss.list_(u'power', u'fix:chair') + mapcss.list_(u'tag'), 'desc': mapcss.tr(u'On Power Transformers use voltage:primary=* and voltage:secondary=* in place of voltage')}
        self.errors[91003] = {'item': 9100, 'level': 3, 'tag': mapcss.list_(u'power', u'fix:chair') + mapcss.list_(u'tag'), 'desc': mapcss.tr(u'Power Transformers should have a frequency tag')}



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[power=transformer][voltage]
        if (u'power' in keys and u'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer') and mapcss._tag_capture(capture_tags, 1, tags, u'voltage'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag")
                # -osmoseItemClassLevel:"9100/91002/2"
                # throwWarning:tr("On Power Transformers use voltage:primary=* and voltage:secondary=* in place of voltage")
                err.append({'class': 91002, 'subclass': 0, 'text': mapcss.tr(u'On Power Transformers use voltage:primary=* and voltage:secondary=* in place of voltage')})

        # node[power=transformer][!frequency]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer') and not mapcss._tag_capture(capture_tags, 1, tags, u'frequency'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag")
                # -osmoseItemClassLevel:"9100/91003/3"
                # throwWarning:tr("Power Transformers should have a frequency tag")
                # assertNoMatch:"node power=transformer frequency=50"
                # assertMatch:"node power=transformer"
                err.append({'class': 91003, 'subclass': 0, 'text': mapcss.tr(u'Power Transformers should have a frequency tag')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[power=transformer]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("geom")
                # -osmoseItemClassLevel:"9100/91001/2"
                # throwWarning:tr("Power Transformers should always be on a node")
                err.append({'class': 91001, 'subclass': 0, 'text': mapcss.tr(u'Power Transformers should always be on a node')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[power=transformer]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("geom")
                # -osmoseItemClassLevel:"9100/91001/2"
                # throwWarning:tr("Power Transformers should always be on a node")
                err.append({'class': 91001, 'subclass': 0, 'text': mapcss.tr(u'Power Transformers should always be on a node')})

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

        self.check_not_err(n.node(data, {u'frequency': u'50', u'power': u'transformer'}), expected={'class': 91003, 'subclass': 0})
        self.check_err(n.node(data, {u'power': u'transformer'}), expected={'class': 91003, 'subclass': 0})
