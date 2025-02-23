#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_ItalySpecific(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/wiki/Rules/ItalySpecific'

    only_for = ['IT']


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[21001] = self.def_class(item = 2100, level = 3, tags = mapcss.list_('fix:chair'), title = mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}')))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[amenity=pharmacy][!dispensing][inside("IT")]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'pharmacy')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'dispensing')) and (mapcss.inside(self.father.config.options, 'IT')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"2100/21001/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 21001, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[amenity=pharmacy][!dispensing][inside("IT")]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'pharmacy')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'dispensing')) and (mapcss.inside(self.father.config.options, 'IT')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"2100/21001/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 21001, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[amenity=pharmacy][!dispensing][inside("IT")]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'pharmacy')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'dispensing')) and (mapcss.inside(self.father.config.options, 'IT')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"2100/21001/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 21001, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err
