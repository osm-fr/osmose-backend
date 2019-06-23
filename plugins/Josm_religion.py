#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_religion(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9008005] = {'item': 9008, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=catholic]
        if (u'religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'religion') == mapcss._value_capture(capture_tags, 0, u'catholic'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}","{0.tag}")
                # suggestAlternative:"religion=christian + denomination=catholic"
                # fixChangeKey:"religion => denomination"
                # fixAdd:"religion=christian"
                err.append({'class': 9008005, 'subclass': 97466527, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'denomination', mapcss.tag(tags, u'religion')],
                    [u'religion',u'christian']]),
                    '-': ([
                    u'religion'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=catholic]
        if (u'religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'religion') == mapcss._value_capture(capture_tags, 0, u'catholic'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}","{0.tag}")
                # suggestAlternative:"religion=christian + denomination=catholic"
                # fixChangeKey:"religion => denomination"
                # fixAdd:"religion=christian"
                err.append({'class': 9008005, 'subclass': 97466527, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'denomination', mapcss.tag(tags, u'religion')],
                    [u'religion',u'christian']]),
                    '-': ([
                    u'religion'])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=catholic]
        if (u'religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'religion') == mapcss._value_capture(capture_tags, 0, u'catholic'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}","{0.tag}")
                # suggestAlternative:"religion=christian + denomination=catholic"
                # fixChangeKey:"religion => denomination"
                # fixAdd:"religion=christian"
                err.append({'class': 9008005, 'subclass': 97466527, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'denomination', mapcss.tag(tags, u'religion')],
                    [u'religion',u'christian']]),
                    '-': ([
                    u'religion'])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_religion(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


