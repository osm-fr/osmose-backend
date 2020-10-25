#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_unnecessary(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/unnecessary.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9010001] = self.def_class(item = 9010, level = 3, tags = ["tag"], title = mapcss.tr('unnecessary tag'))
        self.errors[9010002] = self.def_class(item = 9010, level = 3, tags = ["tag"], title = mapcss.tr('{0} makes no sense', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9010003] = self.def_class(item = 9010, level = 3, tags = ["tag"], title = mapcss.tr('descriptive name'))

        self.re_017d2728 = re.compile(r'^(?i)(restaurant)$')
        self.re_07d0fe8d = re.compile(r'^(?i)(library|biblioteca|biblioteka|bibliothek|bibliotheek)$')
        self.re_0a40c79a = re.compile(r'^(?i)(Аптека|farmacia|pharmacy|pharmacie)$')
        self.re_106eed50 = re.compile(r'^(?i)(shop|boutique)$')
        self.re_10870b34 = re.compile(r'^(?i)(parc|park)$')
        self.re_14b2be23 = re.compile(r'^(?i)(lycée)$')
        self.re_1b9641aa = re.compile(r'^(?i)(post office)$')
        self.re_1ba0f749 = re.compile(r'^(?i)(pond)$')
        self.re_251cae80 = re.compile(r'^(?i)(parking|parkplatz)$')
        self.re_29150b73 = re.compile(r'^(?i)(casa)$')
        self.re_2b5b04af = re.compile(r'^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$')
        self.re_337f006b = re.compile(r'^(?i)(school|école|Школа)$')
        self.re_33dfa05b = re.compile(r'^(?i)(church|église|biserica)$')
        self.re_3ad2c525 = re.compile(r'^(?i)(école primaire)$')
        self.re_3ad9e1f5 = re.compile(r'^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$')
        self.re_480c7ba6 = re.compile(r'^(?i)(building|bangunan)$')
        self.re_480ecdbb = re.compile(r'^(?i)(école élémentaire)$')
        self.re_519078ac = re.compile(r'^(?i)(collège)$')
        self.re_5276c7e0 = re.compile(r'^(?i)(house|maison|rumah|vivienda)$')
        self.re_56dafa68 = re.compile(r'^(?i)(hydrant)$')
        self.re_577104db = re.compile(r'^(?i)(kiosk)$')
        self.re_58f52447 = re.compile(r'^(?i)(house|rumah|vivienda)$')
        self.re_5b729ae4 = re.compile(r'^(?i)(toilets?)$')
        self.re_644827a8 = re.compile(r'^(?i)(jalan)$')
        self.re_69efe08d = re.compile(r'^(gpx|gpxx|gpxd):')
        self.re_6d34128b = re.compile(r'^(?i)(АГЗС|АЗС)$')
        self.re_702b1034 = re.compile(r'^(?i)(path)$')
        self.re_73411d88 = re.compile(r'^(?i)(mosque|cami|masjid|مسجد)$')
        self.re_740e0d70 = re.compile(r'^(?i)(école maternelle)$')
        self.re_76c4f24d = re.compile(r'^(?i)(silo)$')
        self.re_76f94888 = re.compile(r'^(?i)(monument aux morts|war memorial)$')
        self.re_7c3e64db = re.compile(r'^(?i)(chapel|chapelle|kapelle)$')
        self.re_7dc8f17a = re.compile(r'^(?i)(playground|spielplatz)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][!vehicle][!access][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if ('access' in keys and 'highway' in keys) or ('bridge' in keys) or ('building' in keys) or ('elevation' in keys) or ('highway' in keys and 'motor_vehicle' in keys) or ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'access') and mapcss._tag_capture(capture_tags, 1, tags, 'highway') == mapcss._value_capture(capture_tags, 1, 'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'motor_vehicle') in ('yes', 'true', '1') and not mapcss._tag_capture(capture_tags, 1, tags, 'vehicle') and not mapcss._tag_capture(capture_tags, 2, tags, 'access') and mapcss._tag_capture(capture_tags, 3, tags, 'bicycle_road') != mapcss._value_const_capture(capture_tags, 3, 'yes', 'yes') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'bridge') == mapcss._value_capture(capture_tags, 0, 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'elevation') == mapcss._value_capture(capture_tags, 0, '0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'layer') == mapcss._value_capture(capture_tags, 0, '0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 2110229428, 'text': mapcss.tr('{0} is unnecessary', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[gnis:Class="Populated Place"][place=city]
        # *[gnis:Class="Populated Place"][place=town]
        # *[gnis:Class="Populated Place"][place=village]
        # *[gnis:Class="Populated Place"][place=hamlet]
        # *[gnis:Class=Summit][natural=peak]
        if ('gnis:Class' in keys and 'natural' in keys) or ('gnis:Class' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'city'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'town'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'village'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'hamlet'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Summit') and mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'peak'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{1.tag}")
                # fixRemove:"{0.key}"
                # assertNoMatch:"node gnis:Class=\"Populated Place\" place=locality"
                # assertMatch:"node gnis:Class=\"Populated Place\" place=village"
                err.append({'class': 9010001, 'subclass': 1667787383, 'text': mapcss.tr('{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[emergency=permissive]
        if ('emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag}")
                # fixAdd:"emergency=yes"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr('{0} makes no sense', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['emergency','yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if ('payment:cash' in keys and 'payment:coins' in keys and 'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, 'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, 'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr('{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'payment:cash'])
                }})

        # node[emergency=fire_hydrant][fire_hydrant:count=1]
        if ('emergency' in keys and 'fire_hydrant:count' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'fire_hydrant') and mapcss._tag_capture(capture_tags, 1, tags, 'fire_hydrant:count') == mapcss._value_capture(capture_tags, 1, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{1.tag}","{0.tag}")
                # fixRemove:"{1.key}"
                err.append({'class': 9010001, 'subclass': 178896259, 'text': mapcss.tr('{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{1.key}')])
                }})

        # *[name][name=~/^(?i)(library|biblioteca|biblioteka|bibliothek|bibliotheek)$/][amenity=library]
        # *[name][name=~/^(?i)(parc|park)$/][leisure=park]
        # *[name][name=~/^(?i)(pond)$/][water=pond]
        # *[name][name=~/^(?i)(church|église|biserica)$/][amenity=place_of_worship][religion=christian]
        # *[name][name=~/^(?i)(mosque|cami|masjid|مسجد)$/][amenity=place_of_worship][religion=muslim]
        # *[name][name=~/^(?i)(parking|parkplatz)$/][amenity=parking]
        # *[name][name=~/^(?i)(post office)$/][amenity=post_office]
        # *[name][name=~/^(?i)(restaurant)$/][amenity=restaurant]
        # *[name][name=~/^(?i)(toilets?)$/][amenity=toilets]
        # *[name][name=~/^(?i)(playground|spielplatz)$/][leisure=playground]
        # *[name][name=~/^(?i)(shop|boutique)$/][shop][shop!=no]
        # *[name][name=~/^(?i)(building|bangunan)$/][building][building!=no]
        # *[name][name=~/^(?i)(house|maison|rumah|vivienda)$/][building=house]
        # *[name][name=~/^(?i)(casa)$/][building=house][outside("FR")]
        # *[name][name=~/^(?i)(kiosk)$/][shop=kiosk][outside("NL")]
        # *[name][name=~/^(?i)(path)$/][highway=path]
        # *[name][name=~/^(?i)(jalan)$/][highway]
        # *[name][name=~/^(?i)(silo)$/][man_made=silo]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][amenity=grave_yard]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][landuse=cemetery]
        # *[name][name=~/^(?i)(monument aux morts|war memorial)$/][historic=memorial][memorial=war_memorial]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity=school]
        # *[name][name=~/^(?i)(école élémentaire)$/][amenity=school]["school:FR"="élémentaire"]
        # *[name][name=~/^(?i)(école maternelle)$/][amenity=school]["school:FR"="maternelle"]
        # *[name][name=~/^(?i)(école primaire)$/][amenity=school]["school:FR"="primaire"]
        # *[name][name=~/^(?i)(collège)$/][amenity=school]["school:FR"="collège"]
        # *[name][name=~/^(?i)(lycée)$/][amenity=school]["school:FR"="lycée"]
        # *[name][name=~/^(?i)(Аптека|farmacia|pharmacy|pharmacie)$/][amenity=pharmacy]
        # *[name][name=~/^(?i)(hydrant)$/][emergency=fire_hydrant]
        # *[name][name=~/^(?i)(АГЗС|АЗС)$/][amenity=fuel]
        if ('amenity' in keys and 'name' in keys) or ('amenity' in keys and 'name' in keys and 'religion' in keys) or ('amenity' in keys and 'name' in keys and 'school:FR' in keys) or ('building' in keys and 'name' in keys) or ('emergency' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('historic' in keys and 'memorial' in keys and 'name' in keys) or ('landuse' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('man_made' in keys and 'name' in keys) or ('name' in keys and 'shop' in keys) or ('name' in keys and 'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_07d0fe8d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'library'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_10870b34), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'leisure') == mapcss._value_capture(capture_tags, 2, 'park'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1ba0f749), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'pond'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33dfa05b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, 'religion') == mapcss._value_capture(capture_tags, 3, 'christian'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_73411d88), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, 'religion') == mapcss._value_capture(capture_tags, 3, 'muslim'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251cae80), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'parking'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b9641aa), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'post_office'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_017d2728), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'restaurant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5b729ae4), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'toilets'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7dc8f17a), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'leisure') == mapcss._value_capture(capture_tags, 2, 'playground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_106eed50), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'shop') and mapcss._tag_capture(capture_tags, 3, tags, 'shop') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480c7ba6), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5276c7e0), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') == mapcss._value_capture(capture_tags, 2, 'house'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_29150b73), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') == mapcss._value_capture(capture_tags, 2, 'house') and mapcss.outside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_577104db), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'shop') == mapcss._value_capture(capture_tags, 2, 'kiosk') and mapcss.outside(self.father.config.options, 'NL'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_702b1034), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'highway') == mapcss._value_capture(capture_tags, 2, 'path'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_644827a8), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'man_made') == mapcss._value_capture(capture_tags, 2, 'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'grave_yard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'landuse') == mapcss._value_capture(capture_tags, 2, 'cemetery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76f94888), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'historic') == mapcss._value_capture(capture_tags, 2, 'memorial') and mapcss._tag_capture(capture_tags, 3, tags, 'memorial') == mapcss._value_capture(capture_tags, 3, 'war_memorial'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480ecdbb), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'élémentaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_740e0d70), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'maternelle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3ad2c525), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'primaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_519078ac), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'collège'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_14b2be23), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'lycée'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0a40c79a), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'pharmacy'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_56dafa68), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'emergency') == mapcss._value_capture(capture_tags, 2, 'fire_hydrant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d34128b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'fuel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                # fixRemove:"name"
                # assertNoMatch:"node name=Megaparking amenity=parking"
                # assertMatch:"node name=PLaYGrOUNd leisure=playground"
                # assertMatch:"node name=Parking amenity=parking"
                # assertNoMatch:"node name=Parking_with_suffix amenity=parking"
                # assertMatch:"node name=parking amenity=parking"
                # assertNoMatch:"node name=shop shop=no"
                # assertMatch:"node name=shop shop=whatever"
                err.append({'class': 9010003, 'subclass': 773913345, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'name'])
                }})

        # *[name][name=~/^(?i)(chapel|chapelle|kapelle)$/]
        # *[name][name=~/^(?i)(silo)$/][man_made!=silo]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity!=school]
        # *[name][name=~/^(?i)(house|rumah|vivienda)$/][building][building!=house][building!=no]
        # *[name][name=~/^(?i)(casa)$/][building][building!=house][building!=no][outside("FR")]
        if ('building' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7c3e64db), mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'silo', 'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'school', 'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_58f52447), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'house', 'house') and mapcss._tag_capture(capture_tags, 4, tags, 'building') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_29150b73), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'house', 'house') and mapcss._tag_capture(capture_tags, 4, tags, 'building') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no') and mapcss.outside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                err.append({'class': 9010003, 'subclass': 107322852, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/^(gpx|gpxx|gpxd):/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_69efe08d))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} should not be uploaded","{0.key}")
                # fixRemove:"{0.key}"
                # assertMatch:"node gpx:time=2018-01-01T12:00:00Z"
                # assertMatch:"node gpxd:color=#FF0000"
                # assertNoMatch:"node source=gpx:foo"
                err.append({'class': 9010001, 'subclass': 764820177, 'text': mapcss.tr('{0} should not be uploaded', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][!vehicle][!access][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if ('access' in keys and 'highway' in keys) or ('bridge' in keys) or ('building' in keys) or ('elevation' in keys) or ('highway' in keys and 'motor_vehicle' in keys) or ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'access') and mapcss._tag_capture(capture_tags, 1, tags, 'highway') == mapcss._value_capture(capture_tags, 1, 'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'motor_vehicle') in ('yes', 'true', '1') and not mapcss._tag_capture(capture_tags, 1, tags, 'vehicle') and not mapcss._tag_capture(capture_tags, 2, tags, 'access') and mapcss._tag_capture(capture_tags, 3, tags, 'bicycle_road') != mapcss._value_const_capture(capture_tags, 3, 'yes', 'yes') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'bridge') == mapcss._value_capture(capture_tags, 0, 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'elevation') == mapcss._value_capture(capture_tags, 0, '0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'layer') == mapcss._value_capture(capture_tags, 0, '0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                # assertMatch:"way bridge=no"
                # assertNoMatch:"way highway=motorway access=no motor_vehicle=yes"
                # assertMatch:"way highway=motorway motor_vehicle=yes"
                # assertMatch:"way highway=proposed access=no"
                # assertMatch:"way layer=0"
                err.append({'class': 9010001, 'subclass': 2110229428, 'text': mapcss.tr('{0} is unnecessary', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[gnis:Class="Populated Place"][place=city]
        # *[gnis:Class="Populated Place"][place=town]
        # *[gnis:Class="Populated Place"][place=village]
        # *[gnis:Class="Populated Place"][place=hamlet]
        # *[gnis:Class=Summit][natural=peak]
        if ('gnis:Class' in keys and 'natural' in keys) or ('gnis:Class' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'city'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'town'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'village'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'hamlet'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Summit') and mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'peak'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{1.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 1667787383, 'text': mapcss.tr('{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[emergency=permissive]
        if ('emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag}")
                # fixAdd:"emergency=yes"
                # assertNoMatch:"way emergency=designated"
                # assertMatch:"way emergency=permissive"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr('{0} makes no sense', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['emergency','yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if ('payment:cash' in keys and 'payment:coins' in keys and 'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, 'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, 'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr('{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'payment:cash'])
                }})

        # *[name][name=~/^(?i)(library|biblioteca|biblioteka|bibliothek|bibliotheek)$/][amenity=library]
        # *[name][name=~/^(?i)(parc|park)$/][leisure=park]
        # *[name][name=~/^(?i)(pond)$/][water=pond]
        # *[name][name=~/^(?i)(church|église|biserica)$/][amenity=place_of_worship][religion=christian]
        # *[name][name=~/^(?i)(mosque|cami|masjid|مسجد)$/][amenity=place_of_worship][religion=muslim]
        # *[name][name=~/^(?i)(parking|parkplatz)$/][amenity=parking]
        # *[name][name=~/^(?i)(post office)$/][amenity=post_office]
        # *[name][name=~/^(?i)(restaurant)$/][amenity=restaurant]
        # *[name][name=~/^(?i)(toilets?)$/][amenity=toilets]
        # *[name][name=~/^(?i)(playground|spielplatz)$/][leisure=playground]
        # *[name][name=~/^(?i)(shop|boutique)$/][shop][shop!=no]
        # *[name][name=~/^(?i)(building|bangunan)$/][building][building!=no]
        # *[name][name=~/^(?i)(house|maison|rumah|vivienda)$/][building=house]
        # *[name][name=~/^(?i)(casa)$/][building=house][outside("FR")]
        # *[name][name=~/^(?i)(kiosk)$/][shop=kiosk][outside("NL")]
        # *[name][name=~/^(?i)(path)$/][highway=path]
        # *[name][name=~/^(?i)(jalan)$/][highway]
        # *[name][name=~/^(?i)(silo)$/][man_made=silo]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][amenity=grave_yard]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][landuse=cemetery]
        # *[name][name=~/^(?i)(monument aux morts|war memorial)$/][historic=memorial][memorial=war_memorial]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity=school]
        # *[name][name=~/^(?i)(école élémentaire)$/][amenity=school]["school:FR"="élémentaire"]
        # *[name][name=~/^(?i)(école maternelle)$/][amenity=school]["school:FR"="maternelle"]
        # *[name][name=~/^(?i)(école primaire)$/][amenity=school]["school:FR"="primaire"]
        # *[name][name=~/^(?i)(collège)$/][amenity=school]["school:FR"="collège"]
        # *[name][name=~/^(?i)(lycée)$/][amenity=school]["school:FR"="lycée"]
        # *[name][name=~/^(?i)(Аптека|farmacia|pharmacy|pharmacie)$/][amenity=pharmacy]
        # *[name][name=~/^(?i)(hydrant)$/][emergency=fire_hydrant]
        # *[name][name=~/^(?i)(АГЗС|АЗС)$/][amenity=fuel]
        if ('amenity' in keys and 'name' in keys) or ('amenity' in keys and 'name' in keys and 'religion' in keys) or ('amenity' in keys and 'name' in keys and 'school:FR' in keys) or ('building' in keys and 'name' in keys) or ('emergency' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('historic' in keys and 'memorial' in keys and 'name' in keys) or ('landuse' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('man_made' in keys and 'name' in keys) or ('name' in keys and 'shop' in keys) or ('name' in keys and 'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_07d0fe8d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'library'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_10870b34), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'leisure') == mapcss._value_capture(capture_tags, 2, 'park'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1ba0f749), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'pond'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33dfa05b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, 'religion') == mapcss._value_capture(capture_tags, 3, 'christian'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_73411d88), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, 'religion') == mapcss._value_capture(capture_tags, 3, 'muslim'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251cae80), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'parking'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b9641aa), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'post_office'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_017d2728), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'restaurant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5b729ae4), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'toilets'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7dc8f17a), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'leisure') == mapcss._value_capture(capture_tags, 2, 'playground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_106eed50), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'shop') and mapcss._tag_capture(capture_tags, 3, tags, 'shop') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480c7ba6), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5276c7e0), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') == mapcss._value_capture(capture_tags, 2, 'house'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_29150b73), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') == mapcss._value_capture(capture_tags, 2, 'house') and mapcss.outside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_577104db), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'shop') == mapcss._value_capture(capture_tags, 2, 'kiosk') and mapcss.outside(self.father.config.options, 'NL'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_702b1034), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'highway') == mapcss._value_capture(capture_tags, 2, 'path'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_644827a8), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'man_made') == mapcss._value_capture(capture_tags, 2, 'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'grave_yard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'landuse') == mapcss._value_capture(capture_tags, 2, 'cemetery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76f94888), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'historic') == mapcss._value_capture(capture_tags, 2, 'memorial') and mapcss._tag_capture(capture_tags, 3, tags, 'memorial') == mapcss._value_capture(capture_tags, 3, 'war_memorial'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480ecdbb), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'élémentaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_740e0d70), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'maternelle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3ad2c525), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'primaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_519078ac), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'collège'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_14b2be23), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'lycée'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0a40c79a), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'pharmacy'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_56dafa68), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'emergency') == mapcss._value_capture(capture_tags, 2, 'fire_hydrant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d34128b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'fuel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                # fixRemove:"name"
                # assertMatch:"way name=Cmentarz amenity=grave_yard"
                # assertMatch:"way name=Rumah building=house"
                # assertNoMatch:"way name=Rumah building=yes"
                # assertNoMatch:"way name=Silo building=silo"
                # assertMatch:"way name=Silo man_made=silo building=silo"
                # assertMatch:"way name=building building=house"
                # assertMatch:"way name=building building=yes"
                # assertMatch:"way name=cemetery amenity=grave_yard"
                # assertMatch:"way name=house building=house"
                # assertNoMatch:"way name=house building=yes"
                # assertNoMatch:"way name=kiosk amenity=grave_yard"
                # assertMatch:"way name=kiosk building=yes shop=kiosk"
                # assertNoMatch:"way name=kiosk building=yes"
                # assertNoMatch:"way name=parking"
                # assertNoMatch:"way name=shop leisure=playground"
                # assertMatch:"way name=silo man_made=silo"
                err.append({'class': 9010003, 'subclass': 773913345, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'name'])
                }})

        # *[name][name=~/^(?i)(chapel|chapelle|kapelle)$/]
        # *[name][name=~/^(?i)(silo)$/][man_made!=silo]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity!=school]
        # *[name][name=~/^(?i)(house|rumah|vivienda)$/][building][building!=house][building!=no]
        # *[name][name=~/^(?i)(casa)$/][building][building!=house][building!=no][outside("FR")]
        if ('building' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7c3e64db), mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'silo', 'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'school', 'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_58f52447), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'house', 'house') and mapcss._tag_capture(capture_tags, 4, tags, 'building') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_29150b73), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'house', 'house') and mapcss._tag_capture(capture_tags, 4, tags, 'building') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no') and mapcss.outside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                # assertNoMatch:"way name=Rumah building=house"
                # assertMatch:"way name=Rumah building=yes"
                # assertMatch:"way name=Silo building=silo"
                # assertNoMatch:"way name=building building=house"
                # assertNoMatch:"way name=building building=yes"
                # assertNoMatch:"way name=house building=house"
                # assertMatch:"way name=house building=yes"
                err.append({'class': 9010003, 'subclass': 107322852, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/^(gpx|gpxx|gpxd):/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_69efe08d))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} should not be uploaded","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 764820177, 'text': mapcss.tr('{0} should not be uploaded', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[access][highway=proposed]
        # *[motor_vehicle?][!vehicle][!access][bicycle_road!=yes][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        # *[bridge=no]
        # *[building=no]
        # *[elevation="0"]
        # *[layer="0"]
        if ('access' in keys and 'highway' in keys) or ('bridge' in keys) or ('building' in keys) or ('elevation' in keys) or ('highway' in keys and 'motor_vehicle' in keys) or ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'access') and mapcss._tag_capture(capture_tags, 1, tags, 'highway') == mapcss._value_capture(capture_tags, 1, 'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'motor_vehicle') in ('yes', 'true', '1') and not mapcss._tag_capture(capture_tags, 1, tags, 'vehicle') and not mapcss._tag_capture(capture_tags, 2, tags, 'access') and mapcss._tag_capture(capture_tags, 3, tags, 'bicycle_road') != mapcss._value_const_capture(capture_tags, 3, 'yes', 'yes') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'bridge') == mapcss._value_capture(capture_tags, 0, 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'elevation') == mapcss._value_capture(capture_tags, 0, '0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'layer') == mapcss._value_capture(capture_tags, 0, '0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 2110229428, 'text': mapcss.tr('{0} is unnecessary', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[gnis:Class="Populated Place"][place=city]
        # *[gnis:Class="Populated Place"][place=town]
        # *[gnis:Class="Populated Place"][place=village]
        # *[gnis:Class="Populated Place"][place=hamlet]
        # *[gnis:Class=Summit][natural=peak]
        if ('gnis:Class' in keys and 'natural' in keys) or ('gnis:Class' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'city'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'town'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'village'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, 'place') == mapcss._value_capture(capture_tags, 1, 'hamlet'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'gnis:Class') == mapcss._value_capture(capture_tags, 0, 'Summit') and mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'peak'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{1.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 1667787383, 'text': mapcss.tr('{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[emergency=permissive]
        if ('emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag}")
                # fixAdd:"emergency=yes"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr('{0} makes no sense', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['emergency','yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if ('payment:cash' in keys and 'payment:coins' in keys and 'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, 'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, 'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr('{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'payment:cash'])
                }})

        # *[name][name=~/^(?i)(library|biblioteca|biblioteka|bibliothek|bibliotheek)$/][amenity=library]
        # *[name][name=~/^(?i)(parc|park)$/][leisure=park]
        # *[name][name=~/^(?i)(pond)$/][water=pond]
        # *[name][name=~/^(?i)(church|église|biserica)$/][amenity=place_of_worship][religion=christian]
        # *[name][name=~/^(?i)(mosque|cami|masjid|مسجد)$/][amenity=place_of_worship][religion=muslim]
        # *[name][name=~/^(?i)(parking|parkplatz)$/][amenity=parking]
        # *[name][name=~/^(?i)(post office)$/][amenity=post_office]
        # *[name][name=~/^(?i)(restaurant)$/][amenity=restaurant]
        # *[name][name=~/^(?i)(toilets?)$/][amenity=toilets]
        # *[name][name=~/^(?i)(playground|spielplatz)$/][leisure=playground]
        # *[name][name=~/^(?i)(shop|boutique)$/][shop][shop!=no]
        # *[name][name=~/^(?i)(building|bangunan)$/][building][building!=no]
        # *[name][name=~/^(?i)(house|maison|rumah|vivienda)$/][building=house]
        # *[name][name=~/^(?i)(casa)$/][building=house][outside("FR")]
        # *[name][name=~/^(?i)(kiosk)$/][shop=kiosk][outside("NL")]
        # *[name][name=~/^(?i)(path)$/][highway=path]
        # *[name][name=~/^(?i)(jalan)$/][highway]
        # *[name][name=~/^(?i)(silo)$/][man_made=silo]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][amenity=grave_yard]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][landuse=cemetery]
        # *[name][name=~/^(?i)(monument aux morts|war memorial)$/][historic=memorial][memorial=war_memorial]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity=school]
        # *[name][name=~/^(?i)(école élémentaire)$/][amenity=school]["school:FR"="élémentaire"]
        # *[name][name=~/^(?i)(école maternelle)$/][amenity=school]["school:FR"="maternelle"]
        # *[name][name=~/^(?i)(école primaire)$/][amenity=school]["school:FR"="primaire"]
        # *[name][name=~/^(?i)(collège)$/][amenity=school]["school:FR"="collège"]
        # *[name][name=~/^(?i)(lycée)$/][amenity=school]["school:FR"="lycée"]
        # *[name][name=~/^(?i)(Аптека|farmacia|pharmacy|pharmacie)$/][amenity=pharmacy]
        # *[name][name=~/^(?i)(hydrant)$/][emergency=fire_hydrant]
        # *[name][name=~/^(?i)(АГЗС|АЗС)$/][amenity=fuel]
        if ('amenity' in keys and 'name' in keys) or ('amenity' in keys and 'name' in keys and 'religion' in keys) or ('amenity' in keys and 'name' in keys and 'school:FR' in keys) or ('building' in keys and 'name' in keys) or ('emergency' in keys and 'name' in keys) or ('highway' in keys and 'name' in keys) or ('historic' in keys and 'memorial' in keys and 'name' in keys) or ('landuse' in keys and 'name' in keys) or ('leisure' in keys and 'name' in keys) or ('man_made' in keys and 'name' in keys) or ('name' in keys and 'shop' in keys) or ('name' in keys and 'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_07d0fe8d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'library'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_10870b34), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'leisure') == mapcss._value_capture(capture_tags, 2, 'park'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1ba0f749), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'pond'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33dfa05b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, 'religion') == mapcss._value_capture(capture_tags, 3, 'christian'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_73411d88), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, 'religion') == mapcss._value_capture(capture_tags, 3, 'muslim'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251cae80), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'parking'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b9641aa), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'post_office'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_017d2728), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'restaurant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5b729ae4), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'toilets'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7dc8f17a), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'leisure') == mapcss._value_capture(capture_tags, 2, 'playground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_106eed50), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'shop') and mapcss._tag_capture(capture_tags, 3, tags, 'shop') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480c7ba6), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5276c7e0), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') == mapcss._value_capture(capture_tags, 2, 'house'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_29150b73), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') == mapcss._value_capture(capture_tags, 2, 'house') and mapcss.outside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_577104db), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'shop') == mapcss._value_capture(capture_tags, 2, 'kiosk') and mapcss.outside(self.father.config.options, 'NL'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_702b1034), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'highway') == mapcss._value_capture(capture_tags, 2, 'path'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_644827a8), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'man_made') == mapcss._value_capture(capture_tags, 2, 'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'grave_yard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'landuse') == mapcss._value_capture(capture_tags, 2, 'cemetery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76f94888), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'historic') == mapcss._value_capture(capture_tags, 2, 'memorial') and mapcss._tag_capture(capture_tags, 3, tags, 'memorial') == mapcss._value_capture(capture_tags, 3, 'war_memorial'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480ecdbb), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'élémentaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_740e0d70), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'maternelle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3ad2c525), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'primaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_519078ac), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'collège'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_14b2be23), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'school') and mapcss._tag_capture(capture_tags, 3, tags, 'school:FR') == mapcss._value_capture(capture_tags, 3, 'lycée'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0a40c79a), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'pharmacy'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_56dafa68), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'emergency') == mapcss._value_capture(capture_tags, 2, 'fire_hydrant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d34128b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'fuel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                # fixRemove:"name"
                # assertMatch:"relation name=PLAYGROUND leisure=playground type=multipolygon"
                # assertMatch:"relation name=Parking amenity=parking type=multipolygon"
                # assertMatch:"relation name=parking amenity=parking type=multipolygon"
                err.append({'class': 9010003, 'subclass': 773913345, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'name'])
                }})

        # *[name][name=~/^(?i)(chapel|chapelle|kapelle)$/]
        # *[name][name=~/^(?i)(silo)$/][man_made!=silo]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity!=school]
        # *[name][name=~/^(?i)(house|rumah|vivienda)$/][building][building!=house][building!=no]
        # *[name][name=~/^(?i)(casa)$/][building][building!=house][building!=no][outside("FR")]
        if ('building' in keys and 'name' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7c3e64db), mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'silo', 'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'school', 'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_58f52447), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'house', 'house') and mapcss._tag_capture(capture_tags, 4, tags, 'building') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_29150b73), mapcss._tag_capture(capture_tags, 1, tags, 'name')) and mapcss._tag_capture(capture_tags, 2, tags, 'building') and mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'house', 'house') and mapcss._tag_capture(capture_tags, 4, tags, 'building') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no') and mapcss.outside(self.father.config.options, 'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                err.append({'class': 9010003, 'subclass': 107322852, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/^(gpx|gpxx|gpxd):/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_69efe08d))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} should not be uploaded","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 764820177, 'text': mapcss.tr('{0} should not be uploaded', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_unnecessary(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {'gnis:Class': 'Populated Place', 'place': 'locality'}), expected={'class': 9010001, 'subclass': 1667787383})
        self.check_err(n.node(data, {'gnis:Class': 'Populated Place', 'place': 'village'}), expected={'class': 9010001, 'subclass': 1667787383})
        self.check_not_err(n.node(data, {'amenity': 'parking', 'name': 'Megaparking'}), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.node(data, {'leisure': 'playground', 'name': 'PLaYGrOUNd'}), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.node(data, {'amenity': 'parking', 'name': 'Parking'}), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.node(data, {'amenity': 'parking', 'name': 'Parking_with_suffix'}), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.node(data, {'amenity': 'parking', 'name': 'parking'}), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.node(data, {'name': 'shop', 'shop': 'no'}), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.node(data, {'name': 'shop', 'shop': 'whatever'}), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.node(data, {'gpx:time': '2018-01-01T12:00:00Z'}), expected={'class': 9010001, 'subclass': 764820177})
        self.check_err(n.node(data, {'gpxd:color': '#FF0000'}), expected={'class': 9010001, 'subclass': 764820177})
        self.check_not_err(n.node(data, {'source': 'gpx:foo'}), expected={'class': 9010001, 'subclass': 764820177})
        self.check_err(n.way(data, {'bridge': 'no'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_not_err(n.way(data, {'access': 'no', 'highway': 'motorway', 'motor_vehicle': 'yes'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_err(n.way(data, {'highway': 'motorway', 'motor_vehicle': 'yes'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_err(n.way(data, {'access': 'no', 'highway': 'proposed'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_err(n.way(data, {'layer': '0'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_not_err(n.way(data, {'emergency': 'designated'}, [0]), expected={'class': 9010002, 'subclass': 325672362})
        self.check_err(n.way(data, {'emergency': 'permissive'}, [0]), expected={'class': 9010002, 'subclass': 325672362})
        self.check_err(n.way(data, {'amenity': 'grave_yard', 'name': 'Cmentarz'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'building': 'house', 'name': 'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'building': 'yes', 'name': 'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'building': 'silo', 'name': 'Silo'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'building': 'silo', 'man_made': 'silo', 'name': 'Silo'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'building': 'house', 'name': 'building'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'building': 'yes', 'name': 'building'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'amenity': 'grave_yard', 'name': 'cemetery'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'building': 'house', 'name': 'house'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'building': 'yes', 'name': 'house'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'amenity': 'grave_yard', 'name': 'kiosk'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'building': 'yes', 'name': 'kiosk', 'shop': 'kiosk'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'building': 'yes', 'name': 'kiosk'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'name': 'parking'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'leisure': 'playground', 'name': 'shop'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.way(data, {'man_made': 'silo', 'name': 'silo'}, [0]), expected={'class': 9010003, 'subclass': 773913345})
        self.check_not_err(n.way(data, {'building': 'house', 'name': 'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 107322852})
        self.check_err(n.way(data, {'building': 'yes', 'name': 'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 107322852})
        self.check_err(n.way(data, {'building': 'silo', 'name': 'Silo'}, [0]), expected={'class': 9010003, 'subclass': 107322852})
        self.check_not_err(n.way(data, {'building': 'house', 'name': 'building'}, [0]), expected={'class': 9010003, 'subclass': 107322852})
        self.check_not_err(n.way(data, {'building': 'yes', 'name': 'building'}, [0]), expected={'class': 9010003, 'subclass': 107322852})
        self.check_not_err(n.way(data, {'building': 'house', 'name': 'house'}, [0]), expected={'class': 9010003, 'subclass': 107322852})
        self.check_err(n.way(data, {'building': 'yes', 'name': 'house'}, [0]), expected={'class': 9010003, 'subclass': 107322852})
        self.check_err(n.relation(data, {'leisure': 'playground', 'name': 'PLAYGROUND', 'type': 'multipolygon'}, []), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.relation(data, {'amenity': 'parking', 'name': 'Parking', 'type': 'multipolygon'}, []), expected={'class': 9010003, 'subclass': 773913345})
        self.check_err(n.relation(data, {'amenity': 'parking', 'name': 'parking', 'type': 'multipolygon'}, []), expected={'class': 9010003, 'subclass': 773913345})
