#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_FranceSpecificRules(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[2] = {'item': 9999, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'Cette station vend-elle toujours du SP95, ou a-t\'il été remplacé par le SP95-E10 ?')}
        self.errors[20806] = {'item': 2080, 'level': 3, 'tag': mapcss.list_(u'parking', u'amenity', u'fix:chair'), 'desc': mapcss.tr(u'Missing tag carpool on area')}
        self.errors[21600] = {'item': 2160, 'level': 3, 'tag': mapcss.list_(u'tag', u'railway'), 'desc': mapcss.tr(u'Missing tag gauge on rail')}

        self.re_045a0f34 = re.compile(r'(?i)co.?voiturage')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[name=~/(?i)co.?voiturage/][amenity!=car_pooling][!carpool][inside("FR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_045a0f34), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'car_pooling', u'car_pooling') and not mapcss._tag_capture(capture_tags, 2, tags, u'carpool') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"2080/20806/3"
                # throwWarning:tr("Missing tag carpool on area")
                # fixAdd:"amenity=car_pooling"
                # fixAdd:"carpool=designated"
                # -osmoseAssertMatchWithContext:list("node name='Aire de Covoiturage' amenity=parking","inside=FR")
                err.append({'class': 20806, 'subclass': 0, 'text': mapcss.tr(u'Missing tag carpool on area'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'car_pooling'],
                    [u'carpool',u'designated']])
                }})

        # *[amenity=fuel][fuel:octane_95=yes][!fuel:e10][inside("FR")]
        if (u'amenity' in keys and u'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'fuel:e10') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Cette station vend-elle toujours du SP95, ou a-t'il été remplacé par le SP95-E10 ?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 2, 'subclass': 662274675, 'text': mapcss.tr(u'Cette station vend-elle toujours du SP95, ou a-t\'il été remplacé par le SP95-E10 ?')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[railway=rail][!gauge][inside("FR")]
        if (u'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'rail') and not mapcss._tag_capture(capture_tags, 1, tags, u'gauge') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag","railway")
                # -osmoseItemClassLevel:"2160/21600/3"
                # throwWarning:tr("Missing tag gauge on rail")
                # suggestAlternative:"gauge"
                # -osmoseAssertNoMatchWithContext:list("way railway=disused","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way railway=rail gauge=1435","inside=FR")
                # -osmoseAssertMatchWithContext:list("way railway=rail","inside=FR")
                err.append({'class': 21600, 'subclass': 0, 'text': mapcss.tr(u'Missing tag gauge on rail')})

        # *[name=~/(?i)co.?voiturage/][amenity!=car_pooling][!carpool][inside("FR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_045a0f34), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'car_pooling', u'car_pooling') and not mapcss._tag_capture(capture_tags, 2, tags, u'carpool') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"2080/20806/3"
                # throwWarning:tr("Missing tag carpool on area")
                # fixAdd:"amenity=car_pooling"
                # fixAdd:"carpool=designated"
                # -osmoseAssertNoMatchWithContext:list("way name='Aire de covoiturage' amenity=car_pooling","inside=FR")
                # -osmoseAssertMatchWithContext:list("way name='Aire de covoiturage' amenity=car_sharing","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way name='Aire de covoiturage' amenity=parking carpool=designated","inside=FR")
                err.append({'class': 20806, 'subclass': 0, 'text': mapcss.tr(u'Missing tag carpool on area'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'car_pooling'],
                    [u'carpool',u'designated']])
                }})

        # *[amenity=fuel][fuel:octane_95=yes][!fuel:e10][inside("FR")]
        if (u'amenity' in keys and u'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'fuel:e10') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Cette station vend-elle toujours du SP95, ou a-t'il été remplacé par le SP95-E10 ?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 2, 'subclass': 662274675, 'text': mapcss.tr(u'Cette station vend-elle toujours du SP95, ou a-t\'il été remplacé par le SP95-E10 ?')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[name=~/(?i)co.?voiturage/][amenity!=car_pooling][!carpool][inside("FR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_045a0f34), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'car_pooling', u'car_pooling') and not mapcss._tag_capture(capture_tags, 2, tags, u'carpool') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"2080/20806/3"
                # throwWarning:tr("Missing tag carpool on area")
                # fixAdd:"amenity=car_pooling"
                # fixAdd:"carpool=designated"
                err.append({'class': 20806, 'subclass': 0, 'text': mapcss.tr(u'Missing tag carpool on area'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'car_pooling'],
                    [u'carpool',u'designated']])
                }})

        # *[amenity=fuel][fuel:octane_95=yes][!fuel:e10][inside("FR")]
        if (u'amenity' in keys and u'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'fuel:e10') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Cette station vend-elle toujours du SP95, ou a-t'il été remplacé par le SP95-E10 ?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 2, 'subclass': 662274675, 'text': mapcss.tr(u'Cette station vend-elle toujours du SP95, ou a-t\'il été remplacé par le SP95-E10 ?')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_FranceSpecificRules(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {u'amenity': u'parking', u'name': u'Aire de Covoiturage'}), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'railway': u'disused'}, [0]), expected={'class': 21600, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'gauge': u'1435', u'railway': u'rail'}, [0]), expected={'class': 21600, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {u'railway': u'rail'}, [0]), expected={'class': 21600, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'amenity': u'car_pooling', u'name': u'Aire de covoiturage'}, [0]), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {u'amenity': u'car_sharing', u'name': u'Aire de covoiturage'}, [0]), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'amenity': u'parking', u'carpool': u'designated', u'name': u'Aire de covoiturage'}, [0]), expected={'class': 20806, 'subclass': 0})
