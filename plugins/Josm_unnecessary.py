#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_unnecessary(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9010001] = {'item': 9010, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'unnecessary tag')}
        self.errors[9010002] = {'item': 9010, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} makes no sense', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9010003] = {'item': 9010, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'descriptive name')}

        self.re_017d2728 = re.compile(r'^(?i)(restaurant)$')
        self.re_053f39fb = re.compile(r'^(?i)(house|casa|rumah|vivienda)$')
        self.re_0a40c79a = re.compile(r'^(?i)(Аптека|farmacia|pharmacy|pharmacie)$')
        self.re_106eed50 = re.compile(r'^(?i)(shop|boutique)$')
        self.re_10870b34 = re.compile(r'^(?i)(parc|park)$')
        self.re_14b2be23 = re.compile(r'^(?i)(lycée)$')
        self.re_1b9641aa = re.compile(r'^(?i)(post office)$')
        self.re_1ba0f749 = re.compile(r'^(?i)(pond)$')
        self.re_1e5aeb3d = re.compile(r'^(footway|pedestrian)$')
        self.re_2335ac87 = re.compile(r'^(?i)(house|casa|maison|rumah|vivienda)$')
        self.re_251cae80 = re.compile(r'^(?i)(parking|parkplatz)$')
        self.re_2a48de72 = re.compile(r'^(?i)(mairie|rathaus)$')
        self.re_2b5b04af = re.compile(r'^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$')
        self.re_337f006b = re.compile(r'^(?i)(school|école|Школа)$')
        self.re_33dfa05b = re.compile(r'^(?i)(church|église|biserica)$')
        self.re_3ad2c525 = re.compile(r'^(?i)(école primaire)$')
        self.re_3ad9e1f5 = re.compile(r'^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$')
        self.re_47aaa0f7 = re.compile(r'^(yes|designated)$')
        self.re_480c7ba6 = re.compile(r'^(?i)(building|bangunan)$')
        self.re_480ecdbb = re.compile(r'^(?i)(école élémentaire)$')
        self.re_519078ac = re.compile(r'^(?i)(collège)$')
        self.re_577104db = re.compile(r'^(?i)(kiosk)$')
        self.re_5b729ae4 = re.compile(r'^(?i)(toilets?)$')
        self.re_644827a8 = re.compile(r'^(?i)(jalan)$')
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
        if (u'access' in keys and u'highway' in keys) or (u'bridge' in keys) or (u'building' in keys) or (u'elevation' in keys) or (u'highway' in keys and u'motor_vehicle' in keys) or (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and not mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') and not mapcss._tag_capture(capture_tags, 2, tags, u'access') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != mapcss._value_capture(capture_tags, 3, u'yes') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 2110229428, 'text': mapcss.tr(u'{0} is unnecessary', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[gnis:Class="Populated Place"][place=city]
        # *[gnis:Class="Populated Place"][place=town]
        # *[gnis:Class="Populated Place"][place=village]
        # *[gnis:Class="Populated Place"][place=hamlet]
        # *[gnis:Class=Summit][natural=peak]
        if (u'gnis:Class' in keys and u'natural' in keys) or (u'gnis:Class' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'city'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'town'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'village'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'hamlet'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Summit') and mapcss._tag_capture(capture_tags, 1, tags, u'natural') == mapcss._value_capture(capture_tags, 1, u'peak'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{1.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 1667787383, 'text': mapcss.tr(u'{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[emergency=permissive]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag}")
                # fixAdd:"emergency=yes"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys and u'payment:coins' in keys and u'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'payment:cash'])
                }})

        # node[emergency=fire_hydrant][fire_hydrant:count=1]
        if (u'emergency' in keys and u'fire_hydrant:count' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'fire_hydrant') and mapcss._tag_capture(capture_tags, 1, tags, u'fire_hydrant:count') == mapcss._value_capture(capture_tags, 1, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{1.tag}","{0.tag}")
                # fixRemove:"{1.key}"
                err.append({'class': 9010001, 'subclass': 178896259, 'text': mapcss.tr(u'{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # *[name][name=~/^(?i)(parc|park)$/][leisure=park]
        # *[name][name=~/^(?i)(pond)$/][water=pond]
        # *[name][name=~/^(?i)(chapel|chapelle|kapelle)$/][building=chapel]
        # *[name][name=~/^(?i)(church|église|biserica)$/][amenity=place_of_worship][religion=christian]
        # *[name][name=~/^(?i)(mosque|cami|masjid|مسجد)$/][amenity=place_of_worship][religion=muslim]
        # *[name][name=~/^(?i)(parking|parkplatz)$/][amenity=parking]
        # *[name][name=~/^(?i)(post office)$/][amenity=post_office]
        # *[name][name=~/^(?i)(restaurant)$/][amenity=restaurant]
        # *[name][name=~/^(?i)(toilets?)$/][amenity=toilets]
        # *[name][name=~/^(?i)(playground|spielplatz)$/][leisure=playground]
        # *[name][name=~/^(?i)(shop|boutique)$/][shop][shop!=no]
        # *[name][name=~/^(?i)(building|bangunan)$/][building][building!=no]
        # *[name][name=~/^(?i)(house|casa|maison|rumah|vivienda)$/][building=house]
        # *[name][name=~/^(?i)(kiosk)$/][shop=kiosk]
        # *[name][name=~/^(?i)(path)$/][highway=path]
        # *[name][name=~/^(?i)(jalan)$/][highway]
        # *[name][name=~/^(?i)(silo)$/][man_made=silo]
        # *[name][name=~/^(?i)(silo)$/][building=silo]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][amenity=grave_yard]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][landuse=cemetery]
        # *[name][name=~/^(?i)(mairie|rathaus)$/][amenity=townhall]
        # *[name][name=~/^(?i)(monument aux morts|war memorial)$/][historic=memorial][memorial=war_memorial]
        # *[name][name=~/^(?i)(school|école|Школа)$/][building=school]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity=school]
        # *[name][name=~/^(?i)(école élémentaire)$/][amenity=school]["school:FR"="élémentaire"]
        # *[name][name=~/^(?i)(école maternelle)$/][amenity=school]["school:FR"="maternelle"]
        # *[name][name=~/^(?i)(école primaire)$/][amenity=school]["school:FR"="primaire"]
        # *[name][name=~/^(?i)(collège)$/][amenity=school]["school:FR"="collège"]
        # *[name][name=~/^(?i)(lycée)$/][amenity=school]["school:FR"="lycée"]
        # *[name][name=~/^(?i)(Аптека|farmacia|pharmacy|pharmacie)$/][amenity=pharmacy]
        # *[name][name=~/^(?i)(АГЗС|АЗС)$/][amenity=fuel]
        if (u'amenity' in keys and u'name' in keys) or (u'amenity' in keys and u'name' in keys and u'religion' in keys) or (u'amenity' in keys and u'name' in keys and u'school:FR' in keys) or (u'building' in keys and u'name' in keys) or (u'highway' in keys and u'name' in keys) or (u'historic' in keys and u'memorial' in keys and u'name' in keys) or (u'landuse' in keys and u'name' in keys) or (u'leisure' in keys and u'name' in keys) or (u'man_made' in keys and u'name' in keys) or (u'name' in keys and u'shop' in keys) or (u'name' in keys and u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_10870b34), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') == mapcss._value_capture(capture_tags, 2, u'park'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1ba0f749), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'water') == mapcss._value_capture(capture_tags, 2, u'pond'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7c3e64db), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'chapel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33dfa05b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, u'religion') == mapcss._value_capture(capture_tags, 3, u'christian'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_73411d88), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, u'religion') == mapcss._value_capture(capture_tags, 3, u'muslim'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251cae80), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'parking'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b9641aa), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'post_office'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_017d2728), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'restaurant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5b729ae4), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'toilets'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7dc8f17a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') == mapcss._value_capture(capture_tags, 2, u'playground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_106eed50), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'shop') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') != mapcss._value_capture(capture_tags, 3, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480c7ba6), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2335ac87), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'house'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_577104db), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'shop') == mapcss._value_capture(capture_tags, 2, u'kiosk'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_702b1034), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway') == mapcss._value_capture(capture_tags, 2, u'path'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_644827a8), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') == mapcss._value_capture(capture_tags, 2, u'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'grave_yard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'landuse') == mapcss._value_capture(capture_tags, 2, u'cemetery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2a48de72), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'townhall'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76f94888), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'historic') == mapcss._value_capture(capture_tags, 2, u'memorial') and mapcss._tag_capture(capture_tags, 3, tags, u'memorial') == mapcss._value_capture(capture_tags, 3, u'war_memorial'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480ecdbb), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'élémentaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_740e0d70), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'maternelle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3ad2c525), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'primaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_519078ac), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'collège'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_14b2be23), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'lycée'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0a40c79a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'pharmacy'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d34128b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'fuel'))
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
                err.append({'class': 9010003, 'subclass': 1160398162, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'name'])
                }})

        # *[name][name=~/^(?i)(school|école|Школа)$/][building][building!=school][building!=no]
        # *[name][name=~/^(?i)(house|casa|rumah|vivienda)$/][building][building!=house][building!=no]
        if (u'building' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'school') and mapcss._tag_capture(capture_tags, 4, tags, u'building') != mapcss._value_capture(capture_tags, 4, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_053f39fb), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'house') and mapcss._tag_capture(capture_tags, 4, tags, u'building') != mapcss._value_capture(capture_tags, 4, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                err.append({'class': 9010003, 'subclass': 1173941116, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

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
        if (u'access' in keys and u'highway' in keys) or (u'bridge' in keys) or (u'building' in keys) or (u'elevation' in keys) or (u'highway' in keys and u'motor_vehicle' in keys) or (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and not mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') and not mapcss._tag_capture(capture_tags, 2, tags, u'access') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != mapcss._value_capture(capture_tags, 3, u'yes') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == mapcss._value_capture(capture_tags, 0, u'0'))
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
                err.append({'class': 9010001, 'subclass': 2110229428, 'text': mapcss.tr(u'{0} is unnecessary', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # way[foot=~/^(yes|designated)$/][highway=~/^(footway|pedestrian)$/][!access]
        # way[bicycle=~/^(yes|designated)$/][highway=cycleway][!vehicle][!access][foot!=designated]
        # *[gnis:Class="Populated Place"][place=city]
        # *[gnis:Class="Populated Place"][place=town]
        # *[gnis:Class="Populated Place"][place=village]
        # *[gnis:Class="Populated Place"][place=hamlet]
        # *[gnis:Class=Summit][natural=peak]
        if (u'bicycle' in keys and u'highway' in keys) or (u'foot' in keys and u'highway' in keys) or (u'gnis:Class' in keys and u'natural' in keys) or (u'gnis:Class' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 0, tags, u'foot')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1e5aeb3d), mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and not mapcss._tag_capture(capture_tags, 2, tags, u'access'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_47aaa0f7), mapcss._tag_capture(capture_tags, 0, tags, u'bicycle')) and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'cycleway') and not mapcss._tag_capture(capture_tags, 2, tags, u'vehicle') and not mapcss._tag_capture(capture_tags, 3, tags, u'access') and mapcss._tag_capture(capture_tags, 4, tags, u'foot') != mapcss._value_capture(capture_tags, 4, u'designated'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'city'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'town'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'village'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'hamlet'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Summit') and mapcss._tag_capture(capture_tags, 1, tags, u'natural') == mapcss._value_capture(capture_tags, 1, u'peak'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{1.tag}")
                # fixRemove:"{0.key}"
                # assertNoMatch:"way highway=pedestrian access=no foot=designated"
                # assertMatch:"way highway=pedestrian foot=designated"
                err.append({'class': 9010001, 'subclass': 92001477, 'text': mapcss.tr(u'{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[emergency=permissive]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag}")
                # fixAdd:"emergency=yes"
                # assertNoMatch:"way emergency=designated"
                # assertMatch:"way emergency=permissive"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys and u'payment:coins' in keys and u'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'payment:cash'])
                }})

        # way[waterway][oneway?]
        if (u'oneway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{1.key}","{0.key}")
                # fixRemove:"{1.key}"
                err.append({'class': 9010001, 'subclass': 877465780, 'text': mapcss.tr(u'{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # way[waterway][oneway=-1]
        if (u'oneway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, -1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}. The flow direction is defined by the way direction.","{1.key}","{0.key}")
                err.append({'class': 9010001, 'subclass': 1802985931, 'text': mapcss.tr(u'{0} is unnecessary for {1}. The flow direction is defined by the way direction.', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name][name=~/^(?i)(parc|park)$/][leisure=park]
        # *[name][name=~/^(?i)(pond)$/][water=pond]
        # *[name][name=~/^(?i)(chapel|chapelle|kapelle)$/][building=chapel]
        # *[name][name=~/^(?i)(church|église|biserica)$/][amenity=place_of_worship][religion=christian]
        # *[name][name=~/^(?i)(mosque|cami|masjid|مسجد)$/][amenity=place_of_worship][religion=muslim]
        # *[name][name=~/^(?i)(parking|parkplatz)$/][amenity=parking]
        # *[name][name=~/^(?i)(post office)$/][amenity=post_office]
        # *[name][name=~/^(?i)(restaurant)$/][amenity=restaurant]
        # *[name][name=~/^(?i)(toilets?)$/][amenity=toilets]
        # *[name][name=~/^(?i)(playground|spielplatz)$/][leisure=playground]
        # *[name][name=~/^(?i)(shop|boutique)$/][shop][shop!=no]
        # *[name][name=~/^(?i)(building|bangunan)$/][building][building!=no]
        # *[name][name=~/^(?i)(house|casa|maison|rumah|vivienda)$/][building=house]
        # *[name][name=~/^(?i)(kiosk)$/][shop=kiosk]
        # *[name][name=~/^(?i)(path)$/][highway=path]
        # *[name][name=~/^(?i)(jalan)$/][highway]
        # *[name][name=~/^(?i)(silo)$/][man_made=silo]
        # *[name][name=~/^(?i)(silo)$/][building=silo]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][amenity=grave_yard]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][landuse=cemetery]
        # *[name][name=~/^(?i)(mairie|rathaus)$/][amenity=townhall]
        # *[name][name=~/^(?i)(monument aux morts|war memorial)$/][historic=memorial][memorial=war_memorial]
        # *[name][name=~/^(?i)(school|école|Школа)$/][building=school]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity=school]
        # *[name][name=~/^(?i)(école élémentaire)$/][amenity=school]["school:FR"="élémentaire"]
        # *[name][name=~/^(?i)(école maternelle)$/][amenity=school]["school:FR"="maternelle"]
        # *[name][name=~/^(?i)(école primaire)$/][amenity=school]["school:FR"="primaire"]
        # *[name][name=~/^(?i)(collège)$/][amenity=school]["school:FR"="collège"]
        # *[name][name=~/^(?i)(lycée)$/][amenity=school]["school:FR"="lycée"]
        # *[name][name=~/^(?i)(Аптека|farmacia|pharmacy|pharmacie)$/][amenity=pharmacy]
        # *[name][name=~/^(?i)(АГЗС|АЗС)$/][amenity=fuel]
        if (u'amenity' in keys and u'name' in keys) or (u'amenity' in keys and u'name' in keys and u'religion' in keys) or (u'amenity' in keys and u'name' in keys and u'school:FR' in keys) or (u'building' in keys and u'name' in keys) or (u'highway' in keys and u'name' in keys) or (u'historic' in keys and u'memorial' in keys and u'name' in keys) or (u'landuse' in keys and u'name' in keys) or (u'leisure' in keys and u'name' in keys) or (u'man_made' in keys and u'name' in keys) or (u'name' in keys and u'shop' in keys) or (u'name' in keys and u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_10870b34), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') == mapcss._value_capture(capture_tags, 2, u'park'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1ba0f749), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'water') == mapcss._value_capture(capture_tags, 2, u'pond'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7c3e64db), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'chapel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33dfa05b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, u'religion') == mapcss._value_capture(capture_tags, 3, u'christian'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_73411d88), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, u'religion') == mapcss._value_capture(capture_tags, 3, u'muslim'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251cae80), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'parking'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b9641aa), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'post_office'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_017d2728), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'restaurant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5b729ae4), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'toilets'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7dc8f17a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') == mapcss._value_capture(capture_tags, 2, u'playground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_106eed50), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'shop') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') != mapcss._value_capture(capture_tags, 3, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480c7ba6), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2335ac87), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'house'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_577104db), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'shop') == mapcss._value_capture(capture_tags, 2, u'kiosk'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_702b1034), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway') == mapcss._value_capture(capture_tags, 2, u'path'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_644827a8), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') == mapcss._value_capture(capture_tags, 2, u'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'grave_yard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'landuse') == mapcss._value_capture(capture_tags, 2, u'cemetery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2a48de72), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'townhall'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76f94888), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'historic') == mapcss._value_capture(capture_tags, 2, u'memorial') and mapcss._tag_capture(capture_tags, 3, tags, u'memorial') == mapcss._value_capture(capture_tags, 3, u'war_memorial'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480ecdbb), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'élémentaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_740e0d70), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'maternelle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3ad2c525), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'primaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_519078ac), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'collège'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_14b2be23), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'lycée'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0a40c79a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'pharmacy'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d34128b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'fuel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                # fixRemove:"name"
                # assertMatch:"way name=Cmentarz amenity=grave_yard"
                # assertMatch:"way name=Rumah building=house"
                # assertNoMatch:"way name=Rumah building=yes"
                # assertMatch:"way name=Silo building=silo"
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
                err.append({'class': 9010003, 'subclass': 1160398162, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'name'])
                }})

        # *[name][name=~/^(?i)(school|école|Школа)$/][building][building!=school][building!=no]
        # *[name][name=~/^(?i)(house|casa|rumah|vivienda)$/][building][building!=house][building!=no]
        if (u'building' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'school') and mapcss._tag_capture(capture_tags, 4, tags, u'building') != mapcss._value_capture(capture_tags, 4, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_053f39fb), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'house') and mapcss._tag_capture(capture_tags, 4, tags, u'building') != mapcss._value_capture(capture_tags, 4, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                # assertNoMatch:"way name=Rumah building=house"
                # assertMatch:"way name=Rumah building=yes"
                # assertNoMatch:"way name=building building=house"
                # assertNoMatch:"way name=building building=yes"
                # assertNoMatch:"way name=house building=house"
                # assertMatch:"way name=house building=yes"
                err.append({'class': 9010003, 'subclass': 1173941116, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

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
        if (u'access' in keys and u'highway' in keys) or (u'bridge' in keys) or (u'building' in keys) or (u'elevation' in keys) or (u'highway' in keys and u'motor_vehicle' in keys) or (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'motor_vehicle') in ('yes', 'true', '1') and not mapcss._tag_capture(capture_tags, 1, tags, u'vehicle') and not mapcss._tag_capture(capture_tags, 2, tags, u'access') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle_road') != mapcss._value_capture(capture_tags, 3, u'yes') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 4, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 4, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'elevation') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary","{0.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 2110229428, 'text': mapcss.tr(u'{0} is unnecessary', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[gnis:Class="Populated Place"][place=city]
        # *[gnis:Class="Populated Place"][place=town]
        # *[gnis:Class="Populated Place"][place=village]
        # *[gnis:Class="Populated Place"][place=hamlet]
        # *[gnis:Class=Summit][natural=peak]
        if (u'gnis:Class' in keys and u'natural' in keys) or (u'gnis:Class' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'city'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'town'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'village'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Populated Place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') == mapcss._value_capture(capture_tags, 1, u'hamlet'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gnis:Class') == mapcss._value_capture(capture_tags, 0, u'Summit') and mapcss._tag_capture(capture_tags, 1, tags, u'natural') == mapcss._value_capture(capture_tags, 1, u'peak'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{1.tag}")
                # fixRemove:"{0.key}"
                err.append({'class': 9010001, 'subclass': 1667787383, 'text': mapcss.tr(u'{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[emergency=permissive]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} makes no sense","{0.tag}")
                # fixAdd:"emergency=yes"
                err.append({'class': 9010002, 'subclass': 325672362, 'text': mapcss.tr(u'{0} makes no sense', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'yes']])
                }})

        # *[payment:cash][payment:coins][payment:notes]
        if (u'payment:cash' in keys and u'payment:coins' in keys and u'payment:notes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cash') and mapcss._tag_capture(capture_tags, 1, tags, u'payment:coins') and mapcss._tag_capture(capture_tags, 2, tags, u'payment:notes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {0}.","{0.key}","{1.key}","{2.key}")
                # fixRemove:"payment:cash"
                err.append({'class': 9010001, 'subclass': 1340792439, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {0}.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'payment:cash'])
                }})

        # *[name][name=~/^(?i)(parc|park)$/][leisure=park]
        # *[name][name=~/^(?i)(pond)$/][water=pond]
        # *[name][name=~/^(?i)(chapel|chapelle|kapelle)$/][building=chapel]
        # *[name][name=~/^(?i)(church|église|biserica)$/][amenity=place_of_worship][religion=christian]
        # *[name][name=~/^(?i)(mosque|cami|masjid|مسجد)$/][amenity=place_of_worship][religion=muslim]
        # *[name][name=~/^(?i)(parking|parkplatz)$/][amenity=parking]
        # *[name][name=~/^(?i)(post office)$/][amenity=post_office]
        # *[name][name=~/^(?i)(restaurant)$/][amenity=restaurant]
        # *[name][name=~/^(?i)(toilets?)$/][amenity=toilets]
        # *[name][name=~/^(?i)(playground|spielplatz)$/][leisure=playground]
        # *[name][name=~/^(?i)(shop|boutique)$/][shop][shop!=no]
        # *[name][name=~/^(?i)(building|bangunan)$/][building][building!=no]
        # *[name][name=~/^(?i)(house|casa|maison|rumah|vivienda)$/][building=house]
        # *[name][name=~/^(?i)(kiosk)$/][shop=kiosk]
        # *[name][name=~/^(?i)(path)$/][highway=path]
        # *[name][name=~/^(?i)(jalan)$/][highway]
        # *[name][name=~/^(?i)(silo)$/][man_made=silo]
        # *[name][name=~/^(?i)(silo)$/][building=silo]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][amenity=grave_yard]
        # *[name][name=~/^(?i)(cemetery|cementerio|cimetière|cmentarz|friedhof)$/][landuse=cemetery]
        # *[name][name=~/^(?i)(mairie|rathaus)$/][amenity=townhall]
        # *[name][name=~/^(?i)(monument aux morts|war memorial)$/][historic=memorial][memorial=war_memorial]
        # *[name][name=~/^(?i)(school|école|Школа)$/][building=school]
        # *[name][name=~/^(?i)(school|école|Школа)$/][amenity=school]
        # *[name][name=~/^(?i)(école élémentaire)$/][amenity=school]["school:FR"="élémentaire"]
        # *[name][name=~/^(?i)(école maternelle)$/][amenity=school]["school:FR"="maternelle"]
        # *[name][name=~/^(?i)(école primaire)$/][amenity=school]["school:FR"="primaire"]
        # *[name][name=~/^(?i)(collège)$/][amenity=school]["school:FR"="collège"]
        # *[name][name=~/^(?i)(lycée)$/][amenity=school]["school:FR"="lycée"]
        # *[name][name=~/^(?i)(Аптека|farmacia|pharmacy|pharmacie)$/][amenity=pharmacy]
        # *[name][name=~/^(?i)(АГЗС|АЗС)$/][amenity=fuel]
        if (u'amenity' in keys and u'name' in keys) or (u'amenity' in keys and u'name' in keys and u'religion' in keys) or (u'amenity' in keys and u'name' in keys and u'school:FR' in keys) or (u'building' in keys and u'name' in keys) or (u'highway' in keys and u'name' in keys) or (u'historic' in keys and u'memorial' in keys and u'name' in keys) or (u'landuse' in keys and u'name' in keys) or (u'leisure' in keys and u'name' in keys) or (u'man_made' in keys and u'name' in keys) or (u'name' in keys and u'shop' in keys) or (u'name' in keys and u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_10870b34), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') == mapcss._value_capture(capture_tags, 2, u'park'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1ba0f749), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'water') == mapcss._value_capture(capture_tags, 2, u'pond'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7c3e64db), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'chapel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33dfa05b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, u'religion') == mapcss._value_capture(capture_tags, 3, u'christian'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_73411d88), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'place_of_worship') and mapcss._tag_capture(capture_tags, 3, tags, u'religion') == mapcss._value_capture(capture_tags, 3, u'muslim'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_251cae80), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'parking'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b9641aa), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'post_office'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_017d2728), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'restaurant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5b729ae4), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'toilets'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7dc8f17a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') == mapcss._value_capture(capture_tags, 2, u'playground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_106eed50), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'shop') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') != mapcss._value_capture(capture_tags, 3, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480c7ba6), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2335ac87), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'house'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_577104db), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'shop') == mapcss._value_capture(capture_tags, 2, u'kiosk'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_702b1034), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway') == mapcss._value_capture(capture_tags, 2, u'path'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_644827a8), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') == mapcss._value_capture(capture_tags, 2, u'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76c4f24d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'silo'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'grave_yard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b5b04af), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'landuse') == mapcss._value_capture(capture_tags, 2, u'cemetery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2a48de72), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'townhall'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_76f94888), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'historic') == mapcss._value_capture(capture_tags, 2, u'memorial') and mapcss._tag_capture(capture_tags, 3, tags, u'memorial') == mapcss._value_capture(capture_tags, 3, u'war_memorial'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') == mapcss._value_capture(capture_tags, 2, u'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_480ecdbb), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'élémentaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_740e0d70), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'maternelle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3ad2c525), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'primaire'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_519078ac), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'collège'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_14b2be23), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'school') and mapcss._tag_capture(capture_tags, 3, tags, u'school:FR') == mapcss._value_capture(capture_tags, 3, u'lycée'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0a40c79a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'pharmacy'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6d34128b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'fuel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                # fixRemove:"name"
                # assertMatch:"relation name=PLAYGROUND leisure=playground type=multipolygon"
                # assertMatch:"relation name=Parking amenity=parking type=multipolygon"
                # assertMatch:"relation name=parking amenity=parking type=multipolygon"
                err.append({'class': 9010003, 'subclass': 1160398162, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'name'])
                }})

        # *[name][name=~/^(?i)(school|école|Школа)$/][building][building!=school][building!=no]
        # *[name][name=~/^(?i)(house|casa|rumah|vivienda)$/][building][building!=house][building!=no]
        if (u'building' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_337f006b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'school') and mapcss._tag_capture(capture_tags, 4, tags, u'building') != mapcss._value_capture(capture_tags, 4, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_053f39fb), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'building') and mapcss._tag_capture(capture_tags, 3, tags, u'building') != mapcss._value_capture(capture_tags, 3, u'house') and mapcss._tag_capture(capture_tags, 4, tags, u'building') != mapcss._value_capture(capture_tags, 4, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("descriptive name")
                # throwWarning:tr("{0}","{0.tag}")
                err.append({'class': 9010003, 'subclass': 1173941116, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

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

        self.check_not_err(n.node(data, {u'amenity': u'parking', u'name': u'Megaparking'}), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.node(data, {u'leisure': u'playground', u'name': u'PLaYGrOUNd'}), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.node(data, {u'amenity': u'parking', u'name': u'Parking'}), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.node(data, {u'amenity': u'parking', u'name': u'Parking_with_suffix'}), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.node(data, {u'amenity': u'parking', u'name': u'parking'}), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.node(data, {u'name': u'shop', u'shop': u'no'}), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.node(data, {u'name': u'shop', u'shop': u'whatever'}), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'bridge': u'no'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_not_err(n.way(data, {u'access': u'no', u'highway': u'motorway', u'motor_vehicle': u'yes'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_err(n.way(data, {u'highway': u'motorway', u'motor_vehicle': u'yes'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_err(n.way(data, {u'access': u'no', u'highway': u'proposed'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_err(n.way(data, {u'layer': u'0'}, [0]), expected={'class': 9010001, 'subclass': 2110229428})
        self.check_not_err(n.way(data, {u'access': u'no', u'foot': u'designated', u'highway': u'pedestrian'}, [0]), expected={'class': 9010001, 'subclass': 92001477})
        self.check_err(n.way(data, {u'foot': u'designated', u'highway': u'pedestrian'}, [0]), expected={'class': 9010001, 'subclass': 92001477})
        self.check_not_err(n.way(data, {u'emergency': u'designated'}, [0]), expected={'class': 9010002, 'subclass': 325672362})
        self.check_err(n.way(data, {u'emergency': u'permissive'}, [0]), expected={'class': 9010002, 'subclass': 325672362})
        self.check_err(n.way(data, {u'amenity': u'grave_yard', u'name': u'Cmentarz'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'building': u'house', u'name': u'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.way(data, {u'building': u'yes', u'name': u'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'building': u'silo', u'name': u'Silo'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'building': u'silo', u'man_made': u'silo', u'name': u'Silo'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'building': u'house', u'name': u'building'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'building': u'yes', u'name': u'building'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'amenity': u'grave_yard', u'name': u'cemetery'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'building': u'house', u'name': u'house'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.way(data, {u'building': u'yes', u'name': u'house'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.way(data, {u'amenity': u'grave_yard', u'name': u'kiosk'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'building': u'yes', u'name': u'kiosk', u'shop': u'kiosk'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.way(data, {u'building': u'yes', u'name': u'kiosk'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.way(data, {u'name': u'parking'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.way(data, {u'leisure': u'playground', u'name': u'shop'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.way(data, {u'man_made': u'silo', u'name': u'silo'}, [0]), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_not_err(n.way(data, {u'building': u'house', u'name': u'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 1173941116})
        self.check_err(n.way(data, {u'building': u'yes', u'name': u'Rumah'}, [0]), expected={'class': 9010003, 'subclass': 1173941116})
        self.check_not_err(n.way(data, {u'building': u'house', u'name': u'building'}, [0]), expected={'class': 9010003, 'subclass': 1173941116})
        self.check_not_err(n.way(data, {u'building': u'yes', u'name': u'building'}, [0]), expected={'class': 9010003, 'subclass': 1173941116})
        self.check_not_err(n.way(data, {u'building': u'house', u'name': u'house'}, [0]), expected={'class': 9010003, 'subclass': 1173941116})
        self.check_err(n.way(data, {u'building': u'yes', u'name': u'house'}, [0]), expected={'class': 9010003, 'subclass': 1173941116})
        self.check_err(n.relation(data, {u'leisure': u'playground', u'name': u'PLAYGROUND', u'type': u'multipolygon'}, []), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.relation(data, {u'amenity': u'parking', u'name': u'Parking', u'type': u'multipolygon'}, []), expected={'class': 9010003, 'subclass': 1160398162})
        self.check_err(n.relation(data, {u'amenity': u'parking', u'name': u'parking', u'type': u'multipolygon'}, []), expected={'class': 9010003, 'subclass': 1160398162})
