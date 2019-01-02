#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_mtb(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9013001] = {'item': 9013, 'level': 3, 'tag': ["tag", "sport"], 'desc': mapcss.tr(u'Way contains \'\'{0}\'\' but not \'\'{1}\'\'.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9013002] = {'item': 9013, 'level': 3, 'tag': ["tag", "sport"], 'desc': mapcss.tr(u'Way contains \'\'{0}\'\' but is neither a track nor a path.', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9013003] = {'item': 9013, 'level': 3, 'tag': ["tag", "sport"], 'desc': mapcss.tr(u'Invalid \'\'{0}\'\' value: \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))}

        self.re_1b95e3e9 = re.compile(ur'^[0-6][-+]?$')
        self.re_3d3b0752 = re.compile(ur'^[0-5]$')
        self.re_6937bec1 = re.compile(ur'path|track')
        self.re_731f6ce6 = re.compile(ur'^[0-4]$')


    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way["mtb:scale:uphill"][!incline]
        if (u'mtb:scale:uphill' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'mtb:scale:uphill') and not mapcss._tag_capture(capture_tags, 1, tags, u'incline'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Way contains ''{0}'' but not ''{1}''.","{0.key}","{1.key}")
                err.append({'class': 9013001, 'subclass': 1368047539, 'text': mapcss.tr(u'Way contains \'\'{0}\'\' but not \'\'{1}\'\'.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way["mtb:scale:uphill"][highway][highway!~/path|track/]
        if (u'highway' in keys and u'mtb:scale:uphill' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'mtb:scale:uphill') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_6937bec1), mapcss._tag_capture(capture_tags, 2, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Way contains ''{0}'' but is neither a track nor a path.","{0.key}")
                err.append({'class': 9013002, 'subclass': 139842783, 'text': mapcss.tr(u'Way contains \'\'{0}\'\' but is neither a track nor a path.', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way["mtb:scale"]["mtb:scale"!~/^[0-6][-+]?$/]
        if (u'mtb:scale' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'mtb:scale') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1b95e3e9), mapcss._tag_capture(capture_tags, 1, tags, u'mtb:scale')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Invalid ''{0}'' value: ''{1}''","{0.key}","{0.value}")
                err.append({'class': 9013003, 'subclass': 1229830952, 'text': mapcss.tr(u'Invalid \'\'{0}\'\' value: \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # way["mtb:scale:uphill"]["mtb:scale:uphill"!~/^[0-5]$/]
        if (u'mtb:scale:uphill' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'mtb:scale:uphill') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3d3b0752), mapcss._tag_capture(capture_tags, 1, tags, u'mtb:scale:uphill')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Invalid ''{0}'' value: ''{1}''","{0.key}","{0.value}")
                err.append({'class': 9013003, 'subclass': 86930524, 'text': mapcss.tr(u'Invalid \'\'{0}\'\' value: \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # way["mtb:scale:imba"]["mtb:scale:imba"!~/^[0-4]$/]
        if (u'mtb:scale:imba' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'mtb:scale:imba') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_731f6ce6), mapcss._tag_capture(capture_tags, 1, tags, u'mtb:scale:imba')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Invalid ''{0}'' value: ''{1}''","{0.key}","{0.value}")
                err.append({'class': 9013003, 'subclass': 2005358544, 'text': mapcss.tr(u'Invalid \'\'{0}\'\' value: \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_mtb(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


