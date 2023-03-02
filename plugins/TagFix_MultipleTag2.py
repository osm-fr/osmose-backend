#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class TagFix_MultipleTag2(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[20802] = self.def_class(item = 2080, level = 2, tags = mapcss.list_('tag') + mapcss.list_('highway'), title = mapcss.tr('Missing tag ref for emergency access point'))
        self.errors[30320] = self.def_class(item = 3032, level = 1, tags = mapcss.list_('tag') + mapcss.list_('fix:chair', 'highway', 'tag'), title = mapcss.tr('Watch multiple tags'))
        self.errors[30322] = self.def_class(item = 3032, level = 3, tags = mapcss.list_('tag'), title = mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}')))
        self.errors[32301] = self.def_class(item = 3230, level = 2, tags = mapcss.list_('tag') + mapcss.list_('fix:chair'), title = mapcss.tr('Probably only for bottles, not any type of glass'))
        self.errors[32302] = self.def_class(item = 3230, level = 2, tags = mapcss.list_('tag') + mapcss.list_('fix:chair'), title = mapcss.tr('Suspicious name for a container'))
        self.errors[40201] = self.def_class(item = 4020, level = 1, tags = mapcss.list_('tag') + mapcss.list_('fix:chair', 'highway', 'roundabout'), title = mapcss.tr('Roundabout as area'))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter][parking!=rooftop]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'rooftop', 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[highway=emergency_access_point][!ref]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("highway")
                # -osmoseItemClassLevel:"2080/20802:1/2"
                # throwWarning:tr("Missing tag ref for emergency access point")
                err.append({'class': 20802, 'subclass': 1, 'text': mapcss.tr('Missing tag ref for emergency access point')})

        # *[amenity=recycling][recycling_type!=centre][recycling:glass=yes][outside("CZ")]
        if ('amenity' in keys and 'recycling:glass' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling:glass') == mapcss._value_capture(capture_tags, 2, 'yes')) and (mapcss.outside(self.father.config.options, 'CZ')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32301/2"
                # throwWarning:tr("Probably only for bottles, not any type of glass")
                # fixRemove:"recycling:glass"
                # fixAdd:"recycling:glass_bottles=yes"
                # -osmoseAssertNoMatchWithContext:list("node amenity=recycling recycling_type=container recycling:glass=yes","inside=CZ")
                # -osmoseAssertMatchWithContext:list("node amenity=recycling recycling_type=container recycling:glass=yes","inside=FR")
                err.append({'class': 32301, 'subclass': 0, 'text': mapcss.tr('Probably only for bottles, not any type of glass'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:glass_bottles','yes']]),
                    '-': ([
                    'recycling:glass'])
                }})

        # *[amenity=recycling][recycling_type!=centre][name]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32302/2"
                # throwWarning:tr("Suspicious name for a container")
                # assertMatch:"node amenity=recycling recycling_type=container name=\"My nice awesome container\""
                err.append({'class': 32302, 'subclass': 0, 'text': mapcss.tr('Suspicious name for a container')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter][parking!=rooftop]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'rooftop', 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                # assertMatch:"way building=roof amenity=fuel"
                # assertNoMatch:"way building=roof amenity=parking parking=rooftop"
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[highway=emergency_access_point][!ref]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("highway")
                # -osmoseItemClassLevel:"2080/20802:1/2"
                # throwWarning:tr("Missing tag ref for emergency access point")
                err.append({'class': 20802, 'subclass': 1, 'text': mapcss.tr('Missing tag ref for emergency access point')})

        # *[amenity=recycling][recycling_type!=centre][recycling:glass=yes][outside("CZ")]
        if ('amenity' in keys and 'recycling:glass' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling:glass') == mapcss._value_capture(capture_tags, 2, 'yes')) and (mapcss.outside(self.father.config.options, 'CZ')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32301/2"
                # throwWarning:tr("Probably only for bottles, not any type of glass")
                # fixRemove:"recycling:glass"
                # fixAdd:"recycling:glass_bottles=yes"
                err.append({'class': 32301, 'subclass': 0, 'text': mapcss.tr('Probably only for bottles, not any type of glass'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:glass_bottles','yes']]),
                    '-': ([
                    'recycling:glass'])
                }})

        # *[amenity=recycling][recycling_type!=centre][name]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32302/2"
                # throwWarning:tr("Suspicious name for a container")
                err.append({'class': 32302, 'subclass': 0, 'text': mapcss.tr('Suspicious name for a container')})

        # way[highway][fee]
        if ('fee' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'fee')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Watch multiple tags")
                # -osmoseTags:list("fix:chair","highway","tag")
                # -osmoseItemClassLevel:"3032/30320:1000/1"
                # throwWarning:tr("Use tag \"toll\" instead of \"fee\"")
                # fixChangeKey:"fee=>toll"
                # assertMatch:"way highway=primary fee=yes"
                err.append({'class': 30320, 'subclass': 1000, 'text': mapcss.tr('Use tag "toll" instead of "fee"'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['toll', mapcss.tag(tags, 'fee')]]),
                    '-': ([
                    'fee'])
                }})

        # way[highway][junction=roundabout][area][area!=no]
        if ('area' in keys and 'highway' in keys and 'junction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'junction') == mapcss._value_capture(capture_tags, 1, 'roundabout')) and (mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (mapcss._tag_capture(capture_tags, 3, tags, 'area') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair","highway","roundabout")
                # -osmoseItemClassLevel:"4020/40201:0/1"
                # throwWarning:tr("Roundabout as area")
                # fixRemove:"area"
                # assertMatch:"way area=yes highway=secondary junction=roundabout"
                err.append({'class': 40201, 'subclass': 0, 'text': mapcss.tr('Roundabout as area'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'area'])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[building=roof][amenity][amenity!=shelter][parking!=rooftop]
        if ('amenity' in keys and 'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'roof')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'shelter', 'shelter')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'rooftop', 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"3032/30322/3"
                # throwWarning:tr("{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.","{0.tag}","{1.tag}","{0.value}","{1.key}")
                err.append({'class': 30322, 'subclass': 0, 'text': mapcss.tr('{0} together with {1}, usually {1} is located underneath the {2}. Tag the {3} as a separate object.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[highway=emergency_access_point][!ref]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("highway")
                # -osmoseItemClassLevel:"2080/20802:1/2"
                # throwWarning:tr("Missing tag ref for emergency access point")
                err.append({'class': 20802, 'subclass': 1, 'text': mapcss.tr('Missing tag ref for emergency access point')})

        # *[amenity=recycling][recycling_type!=centre][recycling:glass=yes][outside("CZ")]
        if ('amenity' in keys and 'recycling:glass' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling:glass') == mapcss._value_capture(capture_tags, 2, 'yes')) and (mapcss.outside(self.father.config.options, 'CZ')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32301/2"
                # throwWarning:tr("Probably only for bottles, not any type of glass")
                # fixRemove:"recycling:glass"
                # fixAdd:"recycling:glass_bottles=yes"
                err.append({'class': 32301, 'subclass': 0, 'text': mapcss.tr('Probably only for bottles, not any type of glass'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:glass_bottles','yes']]),
                    '-': ([
                    'recycling:glass'])
                }})

        # *[amenity=recycling][recycling_type!=centre][name]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'centre', 'centre')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:chair")
                # -osmoseItemClassLevel:"3230/32302/2"
                # throwWarning:tr("Suspicious name for a container")
                err.append({'class': 32302, 'subclass': 0, 'text': mapcss.tr('Suspicious name for a container')})

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

        with with_options(n, {'country': 'CZ'}):
            self.check_not_err(n.node(data, {'amenity': 'recycling', 'recycling:glass': 'yes', 'recycling_type': 'container'}), expected={'class': 32301, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'amenity': 'recycling', 'recycling:glass': 'yes', 'recycling_type': 'container'}), expected={'class': 32301, 'subclass': 0})
        self.check_err(n.node(data, {'amenity': 'recycling', 'name': 'My nice awesome container', 'recycling_type': 'container'}), expected={'class': 32302, 'subclass': 0})
        self.check_err(n.way(data, {'amenity': 'fuel', 'building': 'roof'}, [0]), expected={'class': 30322, 'subclass': 0})
        self.check_not_err(n.way(data, {'amenity': 'parking', 'building': 'roof', 'parking': 'rooftop'}, [0]), expected={'class': 30322, 'subclass': 0})
        self.check_err(n.way(data, {'fee': 'yes', 'highway': 'primary'}, [0]), expected={'class': 30320, 'subclass': 1000})
        self.check_err(n.way(data, {'area': 'yes', 'highway': 'secondary', 'junction': 'roundabout'}, [0]), expected={'class': 40201, 'subclass': 0})
