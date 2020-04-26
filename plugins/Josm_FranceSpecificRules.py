#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import with_options
from plugins.PluginMapCSS import PluginMapCSS


class Josm_FranceSpecificRules(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/wiki/Rules/FranceSpecificRules'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {}
        self.errors[20806] = self.def_class(item = 2080, level = 3, tags = mapcss.list_(u'parking', u'amenity', u'fix:chair'), title = mapcss.tr(u'Missing tag carpool on area'))
        self.errors[21600] = self.def_class(item = 2160, level = 3, tags = mapcss.list_(u'tag', u'railway'), title = mapcss.tr(u'Missing tag gauge on rail'))
        self.errors[30401] = self.def_class(item = 3040, level = 3, tags = mapcss.list_(u'ref', u'infrastructure'), title = mapcss.tr(u'{0} is invalid', mapcss._tag_uncapture(capture_tags, u'{0.tag}')))
        self.errors[30402] = self.def_class(item = 3040, level = 3, tags = mapcss.list_(u'ref', u'infrastructure'), title = mapcss.tr(u'missing tag'))
        self.errors[30403] = self.def_class(item = 3040, level = 3, tags = mapcss.list_(u'ref', u'infrastructure'), title = mapcss.tr(u'missing tag'))
        self.errors[40103] = self.def_class(item = 4010, level = 3, tags = mapcss.list_(u'tag', u'infrastructure'), title = mapcss.tr(u'deprecated tagging'))
        self.errors[40104] = self.def_class(item = 4010, level = 3, tags = mapcss.list_(u'ref', u'infrastructure'), title = mapcss.tr(u'deprecated tagging'))
        self.errors[40612] = self.def_class(item = 4061, level = 2, tags = mapcss.list_(u'parking', u'amenity', u'fix:chair'), title = mapcss.tr(u'Does this station still sell SP95, or has it been replaced by the SP95-E10?'))
        self.errors[9019001] = self.def_class(item = 9019, level = 3, tags = mapcss.list_(u'ref', u'highway'), title = mapcss.tr(u'validation rules highway milestone'))
        self.errors[9019002] = self.def_class(item = 9019, level = 3, tags = mapcss.list_(u'ref', u'highway'), title = mapcss.tr(u'validation rules nat_ref in France'))

        self.re_045a0f34 = re.compile(r'(?i)co.?voiturage')
        self.re_0a66a902 = re.compile(r'^([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9])$')
        self.re_299ea34e = re.compile(r'^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$')
        self.re_30299d59 = re.compile(r'^(Enedis|GRDF)$')
        self.re_322a74e0 = re.compile(r'^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$')
        self.re_4bae79a8 = re.compile(r'[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}')
        self.re_55ee32ac = re.compile(r'^(motorway|trunk|primary|secondary|tertiary)$')
        self.re_6388df2b = re.compile(r'^(75Periph_Paris_[0-9]{2}_(1[0-9]|[1-9]))$')
        self.re_7510958f = re.compile(r'^(([1-9][0-9]|0[1-9])PR([0-9]|[1-9][0-9]|[1-9][0-9][0-9])[DGU](|C))$')


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

        # *[amenity=fuel]["fuel:octane_95"=yes][!"fuel:e10"][inside("FR")]
        if (u'amenity' in keys and u'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'fuel:e10') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"4061/40612/2"
                # throwWarning:tr("Does this station still sell SP95, or has it been replaced by the SP95-E10?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 40612, 'subclass': 0, 'text': mapcss.tr(u'Does this station still sell SP95, or has it been replaced by the SP95-E10?')})

        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'operator') == mapcss._value_capture(capture_tags, 0, u'ERDF') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("tag","infrastructure")
                # -osmoseItemClassLevel:"4010/40103/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 40103, 'subclass': 0, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'operator',u'Enedis']])
                }})

        # *["ref:ERDF:gdo"][inside("FR")]
        if (u'ref:ERDF:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:ERDF:gdo') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"4010/40104/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"ref:FR:gdo"
                # fixChangeKey:"ref:ERDF:gdo=>ref:FR:gdo"
                err.append({'class': 40104, 'subclass': 0, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'ref:FR:gdo', mapcss.tag(tags, u'ref:ERDF:gdo')]]),
                    '-': ([
                    u'ref:ERDF:gdo'])
                }})

        # *["ref:FR:gdo"]["ref:FR:gdo"!~/[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}/][inside("FR")]
        if (u'ref:FR:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:gdo') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4bae79a8, u'[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}'), mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr(u'{0} is invalid', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power=substation][!"ref:FR:gdo"][ref][operator=~/^(Enedis|GRDF)$/][inside("FR")]
        # *[power=switch][!"ref:FR:gdo"][ref][operator=Enedis][inside("FR")]
        if (u'operator' in keys and u'power' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'substation') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_30299d59), mapcss._tag_capture(capture_tags, 3, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'switch') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss._tag_capture(capture_tags, 3, tags, u'operator') == mapcss._value_capture(capture_tags, 3, u'Enedis') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30402/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 30402, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *["ref:FR:ARCEP"][telecom!=connection_point]
        # *["ref:FR:ARCEP"]["telecom:medium"!=fibre]
        # *["ref:FR:Orange"]["telecom:medium"!=fibre]
        # *["ref:FR:SFR"]["telecom:medium"!=fibre]
        # *["ref:FR:PTT"]["telecom:medium"!=copper]
        if (u'ref:FR:ARCEP' in keys) or (u'ref:FR:Orange' in keys) or (u'ref:FR:PTT' in keys) or (u'ref:FR:SFR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:ARCEP') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom') != mapcss._value_const_capture(capture_tags, 1, u'connection_point', u'connection_point'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:ARCEP') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:Orange') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:SFR') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:PTT') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'copper', u'copper'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # node[highway=milestone][operator][nat_ref][nat_ref!~/^(([1-9][0-9]|0[1-9])PR([0-9]|[1-9][0-9]|[1-9][0-9][0-9])[DGU](|C))$/][inside("FR")]
        if (u'highway' in keys and u'nat_ref' in keys and u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'milestone') and mapcss._tag_capture(capture_tags, 1, tags, u'operator') and mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_7510958f, u'^(([1-9][0-9]|0[1-9])PR([0-9]|[1-9][0-9]|[1-9][0-9][0-9])[DGU](|C))$'), mapcss._tag_capture(capture_tags, 3, tags, u'nat_ref')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules highway milestone")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} is not a milestone valid reference RIU","{2.tag}")
                # -osmoseAssertNoMatchWithContext:list("node highway=milestone ref=A4 distance=38 nat_ref=77PR38DC operator=SANEF","inside=FR")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr(u'{0} is not a milestone valid reference RIU', mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # node[highway=milestone][operator][nat_ref][!ref][inside("FR")]
        if (u'highway' in keys and u'nat_ref' in keys and u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'milestone') and mapcss._tag_capture(capture_tags, 1, tags, u'operator') and mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref') and not mapcss._tag_capture(capture_tags, 3, tags, u'ref') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules highway milestone")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019001/3"
                # throwWarning:tr("missing ref")
                # -osmoseAssertMatchWithContext:list("node highway=milestone distance=38 nat_ref=77PR38DC operator=SANEF","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("node highway=milestone ref=A4 distance=38 nat_ref=77PR38DC operator=SANEF","inside=FR")
                err.append({'class': 9019001, 'subclass': 0, 'text': mapcss.tr(u'missing ref')})

        # node[highway=milestone][operator][nat_ref][!distance][inside("FR")]
        if (u'highway' in keys and u'nat_ref' in keys and u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'milestone') and mapcss._tag_capture(capture_tags, 1, tags, u'operator') and mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref') and not mapcss._tag_capture(capture_tags, 3, tags, u'distance') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules highway milestone")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019001/3"
                # throwWarning:tr("missing distance")
                # -osmoseAssertNoMatchWithContext:list("node highway=milestone ref=A4 distance=38 nat_ref=77PR38DC operator=SANEF","inside=FR")
                # -osmoseAssertMatchWithContext:list("node highway=milestone ref=A4 nat_ref=77PR38DC operator=SANEF","inside=FR")
                err.append({'class': 9019001, 'subclass': 0, 'text': mapcss.tr(u'missing distance')})

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

        # *[amenity=fuel]["fuel:octane_95"=yes][!"fuel:e10"][inside("FR")]
        if (u'amenity' in keys and u'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'fuel:e10') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"4061/40612/2"
                # throwWarning:tr("Does this station still sell SP95, or has it been replaced by the SP95-E10?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 40612, 'subclass': 0, 'text': mapcss.tr(u'Does this station still sell SP95, or has it been replaced by the SP95-E10?')})

        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'operator') == mapcss._value_capture(capture_tags, 0, u'ERDF') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("tag","infrastructure")
                # -osmoseItemClassLevel:"4010/40103/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 40103, 'subclass': 0, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'operator',u'Enedis']])
                }})

        # *["ref:ERDF:gdo"][inside("FR")]
        if (u'ref:ERDF:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:ERDF:gdo') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"4010/40104/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"ref:FR:gdo"
                # fixChangeKey:"ref:ERDF:gdo=>ref:FR:gdo"
                err.append({'class': 40104, 'subclass': 0, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'ref:FR:gdo', mapcss.tag(tags, u'ref:ERDF:gdo')]]),
                    '-': ([
                    u'ref:ERDF:gdo'])
                }})

        # *["ref:FR:gdo"]["ref:FR:gdo"!~/[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}/][inside("FR")]
        if (u'ref:FR:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:gdo') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4bae79a8, u'[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}'), mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr(u'{0} is invalid', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power=substation][!"ref:FR:gdo"][ref][operator=~/^(Enedis|GRDF)$/][inside("FR")]
        # *[power=switch][!"ref:FR:gdo"][ref][operator=Enedis][inside("FR")]
        if (u'operator' in keys and u'power' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'substation') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_30299d59), mapcss._tag_capture(capture_tags, 3, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'switch') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss._tag_capture(capture_tags, 3, tags, u'operator') == mapcss._value_capture(capture_tags, 3, u'Enedis') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30402/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 30402, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *["ref:FR:ARCEP"][telecom!=connection_point]
        # *["ref:FR:ARCEP"]["telecom:medium"!=fibre]
        # *["ref:FR:Orange"]["telecom:medium"!=fibre]
        # *["ref:FR:SFR"]["telecom:medium"!=fibre]
        # *["ref:FR:PTT"]["telecom:medium"!=copper]
        if (u'ref:FR:ARCEP' in keys) or (u'ref:FR:Orange' in keys) or (u'ref:FR:PTT' in keys) or (u'ref:FR:SFR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:ARCEP') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom') != mapcss._value_const_capture(capture_tags, 1, u'connection_point', u'connection_point'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:ARCEP') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:Orange') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:SFR') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:PTT') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'copper', u'copper'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/][nat_ref][operator][!junction][inside("FR")]
        if (u'highway' in keys and u'nat_ref' in keys and u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'nat_ref') and mapcss._tag_capture(capture_tags, 2, tags, u'operator') and not mapcss._tag_capture(capture_tags, 3, tags, u'junction') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} must be a link road or roundabout","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=primary junction=roundabout nat_ref=62A901609CD_2 operator=SANEF","inside=FR")
                # -osmoseAssertMatchWithContext:list("way highway=primary nat_ref=62A901609CD_2 operator=SANEF","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'{0} must be a link road or roundabout', mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/]["nat_ref:backward"][operator][inside("FR")]
        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/]["nat_ref:forward"][operator][inside("FR")]
        if (u'highway' in keys and u'nat_ref:backward' in keys and u'operator' in keys) or (u'highway' in keys and u'nat_ref:forward' in keys and u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'nat_ref:backward') and mapcss._tag_capture(capture_tags, 2, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'nat_ref:forward') and mapcss._tag_capture(capture_tags, 2, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} must be a link road ","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=motorway_link nat_ref:forward=62A902615CD_1 nat_ref:backward=62A902615CD_2 operator='SANEF'","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'{0} must be a link road ', mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/][nat_ref][nat_ref!~/^([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9])$/][operator!="VILLE DE PARIS"][inside("FR")]
        if (u'highway' in keys and u'nat_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'nat_ref') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_0a66a902, u'^([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9])$'), mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref')) and mapcss._tag_capture(capture_tags, 3, tags, u'operator') != mapcss._value_const_capture(capture_tags, 3, u'VILLE DE PARIS', u'VILLE DE PARIS') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=motorway_link nat_ref=80A901645CD_6 operator=SANEF","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'{0} is not a valid reference', mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[junction=roundabout][highway=~/^(motorway|trunk|primary|secondary|tertiary)$/][nat_ref][nat_ref!~/^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$/][inside("FR")]
        if (u'highway' in keys and u'junction' in keys and u'nat_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'junction') == mapcss._value_capture(capture_tags, 0, u'roundabout') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_322a74e0, u'^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 3, tags, u'nat_ref')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference","{2.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=primary junction=roundabout nat_ref=80A901645_6 operator=DIRN","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'{0} is not a valid reference', mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/][nat_ref][nat_ref!~/^(75Periph_Paris_[0-9]{2}_(1[0-9]|[1-9]))$/][operator="VILLE DE PARIS"][inside("FR")]
        if (u'highway' in keys and u'nat_ref' in keys and u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'nat_ref') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6388df2b, u'^(75Periph_Paris_[0-9]{2}_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref')) and mapcss._tag_capture(capture_tags, 3, tags, u'operator') == mapcss._value_capture(capture_tags, 3, u'VILLE DE PARIS') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference (Paris)","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=trunk_link nat_ref=75Periph_Paris_05_3 operator=\"VILLE DE PARIS\"","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'{0} is not a valid reference (Paris)', mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:forward"]["nat_ref:forward"!~/^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$/][inside("FR")]
        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:backward"]["nat_ref:backward"!~/^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$/][inside("FR")]
        if (u'highway' in keys and u'nat_ref:backward' in keys) or (u'highway' in keys and u'nat_ref:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'nat_ref:forward') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_322a74e0, u'^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref:forward')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'nat_ref:backward') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_322a74e0, u'^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref:backward')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=motorway_link nat_ref:forward=62A902615CD_1 nat_ref:backward=62A902615CD_2 operator=SANEF","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'{0} is not a valid reference', mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[highway][highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/][nat_ref][!operator][inside("FR")]
        if (u'highway' in keys and u'nat_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_299ea34e), mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref') and not mapcss._tag_capture(capture_tags, 3, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("Missing tag operator with nat_ref")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'Missing tag operator with nat_ref')})

        # way[highway][highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:forward"][!operator][inside("FR")]
        # way[highway][highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:backward"][!operator][inside("FR")]
        if (u'highway' in keys and u'nat_ref:backward' in keys) or (u'highway' in keys and u'nat_ref:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_299ea34e), mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref:forward') and not mapcss._tag_capture(capture_tags, 3, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_299ea34e), mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'nat_ref:backward') and not mapcss._tag_capture(capture_tags, 3, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("Missing tag operator with nat_ref")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr(u'Missing tag operator with nat_ref')})

        # way.link_road["nat_ref:forward"][oneway=~/^(yes|1|-1)$/][inside("FR")]
        # way.link_road["nat_ref:backward"][oneway=~/^(yes|1|-1)$/][inside("FR")]
        # Use undeclared class link_road

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

        # *[amenity=fuel]["fuel:octane_95"=yes][!"fuel:e10"][inside("FR")]
        if (u'amenity' in keys and u'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'fuel:e10') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"4061/40612/2"
                # throwWarning:tr("Does this station still sell SP95, or has it been replaced by the SP95-E10?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 40612, 'subclass': 0, 'text': mapcss.tr(u'Does this station still sell SP95, or has it been replaced by the SP95-E10?')})

        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'operator') == mapcss._value_capture(capture_tags, 0, u'ERDF') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("tag","infrastructure")
                # -osmoseItemClassLevel:"4010/40103/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 40103, 'subclass': 0, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'operator',u'Enedis']])
                }})

        # *["ref:ERDF:gdo"][inside("FR")]
        if (u'ref:ERDF:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:ERDF:gdo') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"4010/40104/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"ref:FR:gdo"
                # fixChangeKey:"ref:ERDF:gdo=>ref:FR:gdo"
                err.append({'class': 40104, 'subclass': 0, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'ref:FR:gdo', mapcss.tag(tags, u'ref:ERDF:gdo')]]),
                    '-': ([
                    u'ref:ERDF:gdo'])
                }})

        # *["ref:FR:gdo"]["ref:FR:gdo"!~/[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}/][inside("FR")]
        if (u'ref:FR:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:gdo') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4bae79a8, u'[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}'), mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr(u'{0} is invalid', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power=substation][!"ref:FR:gdo"][ref][operator=~/^(Enedis|GRDF)$/][inside("FR")]
        # *[power=switch][!"ref:FR:gdo"][ref][operator=Enedis][inside("FR")]
        if (u'operator' in keys and u'power' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'substation') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_30299d59), mapcss._tag_capture(capture_tags, 3, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'switch') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:FR:gdo') and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss._tag_capture(capture_tags, 3, tags, u'operator') == mapcss._value_capture(capture_tags, 3, u'Enedis') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30402/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 30402, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *["ref:FR:ARCEP"][telecom!=connection_point]
        # *["ref:FR:ARCEP"]["telecom:medium"!=fibre]
        # *["ref:FR:Orange"]["telecom:medium"!=fibre]
        # *["ref:FR:SFR"]["telecom:medium"!=fibre]
        # *["ref:FR:PTT"]["telecom:medium"!=copper]
        if (u'ref:FR:ARCEP' in keys) or (u'ref:FR:Orange' in keys) or (u'ref:FR:PTT' in keys) or (u'ref:FR:SFR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:ARCEP') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom') != mapcss._value_const_capture(capture_tags, 1, u'connection_point', u'connection_point'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:ARCEP') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:Orange') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:SFR') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'fibre', u'fibre'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:FR:PTT') and mapcss._tag_capture(capture_tags, 1, tags, u'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, u'copper', u'copper'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

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
            self.check_not_err(n.node(data, {u'distance': u'38', u'highway': u'milestone', u'nat_ref': u'77PR38DC', u'operator': u'SANEF', u'ref': u'A4'}), expected={'class': 30403, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {u'distance': u'38', u'highway': u'milestone', u'nat_ref': u'77PR38DC', u'operator': u'SANEF'}), expected={'class': 9019001, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.node(data, {u'distance': u'38', u'highway': u'milestone', u'nat_ref': u'77PR38DC', u'operator': u'SANEF', u'ref': u'A4'}), expected={'class': 9019001, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.node(data, {u'distance': u'38', u'highway': u'milestone', u'nat_ref': u'77PR38DC', u'operator': u'SANEF', u'ref': u'A4'}), expected={'class': 9019001, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {u'highway': u'milestone', u'nat_ref': u'77PR38DC', u'operator': u'SANEF', u'ref': u'A4'}), expected={'class': 9019001, 'subclass': 0})
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
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'highway': u'primary', u'junction': u'roundabout', u'nat_ref': u'62A901609CD_2', u'operator': u'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {u'highway': u'primary', u'nat_ref': u'62A901609CD_2', u'operator': u'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'highway': u'motorway_link', u'nat_ref:backward': u'62A902615CD_2', u'nat_ref:forward': u'62A902615CD_1', u'operator': u'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'highway': u'motorway_link', u'nat_ref': u'80A901645CD_6', u'operator': u'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'highway': u'primary', u'junction': u'roundabout', u'nat_ref': u'80A901645_6', u'operator': u'DIRN'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'highway': u'trunk_link', u'nat_ref': u'75Periph_Paris_05_3', u'operator': u'VILLE DE PARIS'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {u'highway': u'motorway_link', u'nat_ref:backward': u'62A902615CD_2', u'nat_ref:forward': u'62A902615CD_1', u'operator': u'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
