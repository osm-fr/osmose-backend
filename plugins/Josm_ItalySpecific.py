#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import with_options
from plugins.PluginMapCSS import PluginMapCSS


class Josm_ItalySpecific(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/wiki/Rules/ItalySpecific'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {}
        self.errors[21001] = self.def_class(item = 2100, level = 3, tags = mapcss.list_(u'fix:chair'), title = mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[amenity=pharmacy][!dispensing][inside("IT")]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'pharmacy') and not mapcss._tag_capture(capture_tags, 1, tags, u'dispensing') and mapcss.inside(self.father.config.options, u'IT'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"2100/21001/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 21001, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[amenity=pharmacy][!dispensing][inside("IT")]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'pharmacy') and not mapcss._tag_capture(capture_tags, 1, tags, u'dispensing') and mapcss.inside(self.father.config.options, u'IT'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"2100/21001/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 21001, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[amenity=pharmacy][!dispensing][inside("IT")]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'pharmacy') and not mapcss._tag_capture(capture_tags, 1, tags, u'dispensing') and mapcss.inside(self.father.config.options, u'IT'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"2100/21001/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 21001, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_ItalySpecific(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


