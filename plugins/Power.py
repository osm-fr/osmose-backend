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
