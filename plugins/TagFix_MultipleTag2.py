#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class TagFix_MultipleTag2(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[30322] = self.def_class(item = 3032, level = 3, tags = mapcss.list_('tag'), title = mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}')))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                # assertMatch:"way building=roof amenity=fuel"
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = TagFix_MultipleTag2(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {'amenity': 'fuel', 'building': 'roof'}, [0]), expected={'class': 30322, 'subclass': 0})
