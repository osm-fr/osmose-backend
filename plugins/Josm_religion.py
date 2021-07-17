#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_religion(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/religion.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9008005] = self.def_class(item = 9008, level = 3, tags = ["tag"], title = mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=catholic]
        if ('religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'religion') == mapcss._value_capture(capture_tags, 0, 'catholic')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}","{0.tag}")
                # suggestAlternative:"religion=christian + denomination=catholic"
                # fixChangeKey:"religion => denomination"
                # fixAdd:"religion=christian"
                err.append({'class': 9008005, 'subclass': 97466527, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['denomination', mapcss.tag(tags, 'religion')],
                    ['religion','christian']]),
                    '-': ([
                    'religion'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=catholic]
        if ('religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'religion') == mapcss._value_capture(capture_tags, 0, 'catholic')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}","{0.tag}")
                # suggestAlternative:"religion=christian + denomination=catholic"
                # fixChangeKey:"religion => denomination"
                # fixAdd:"religion=christian"
                err.append({'class': 9008005, 'subclass': 97466527, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['denomination', mapcss.tag(tags, 'religion')],
                    ['religion','christian']]),
                    '-': ([
                    'religion'])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=catholic]
        if ('religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'religion') == mapcss._value_capture(capture_tags, 0, 'catholic')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}","{0.tag}")
                # suggestAlternative:"religion=christian + denomination=catholic"
                # fixChangeKey:"religion => denomination"
                # fixAdd:"religion=christian"
                err.append({'class': 9008005, 'subclass': 97466527, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['denomination', mapcss.tag(tags, 'religion')],
                    ['religion','christian']]),
                    '-': ([
                    'religion'])
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


