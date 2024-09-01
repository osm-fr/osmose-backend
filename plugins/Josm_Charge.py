#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_Charge(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/wiki/Rules/ChargeRules'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[30916] = self.def_class(item = 3091, level = 3, tags = ["tag"], title = mapcss.tr('Invalid value of charge'))

        self.re_08865a26 = re.compile(r'\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w)$')
        self.re_144caed9 = re.compile(r'^[0-9]+(?:\.[0-9]+)?( ?@| ?\/)')
        self.re_1fcedb6f = re.compile(r'^[^@]+\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+( ?@| ?\/).')
        self.re_2b54497a = re.compile(r'^[A-Z]{3} ?[0-9]')
        self.re_2e5fc639 = re.compile(r'^[0-9]+(?:\.[0-9]+)? ?[A-Z]{3}')
        self.re_31192e6e = re.compile(r'^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})?(?:; ?(?!$)|$))+$')
        self.re_33603a31 = re.compile(r'^(yes|no) ?@')
        self.re_37963245 = re.compile(r'^.*(\p{Sc}).*$')
        self.re_3e47ea39 = re.compile(r'\p{Sc}')
        self.re_45863706 = re.compile(r'\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+($| ?\/)')
        self.re_467f0986 = re.compile(r'^([0-9]+(?:\.[0-9]+)? ?[A-Za-z _-]+|[A-Za-z _-]+ ?[0-9]+(?:\.[0-9]+)?)')
        self.re_5d52f832 = re.compile(r'^[0-9]+(?:\.[0-9]+)?($| ?\/)')
        self.re_61f9f7ad = re.compile(r'^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})? ?@).')
        self.re_6221e95a = re.compile(r'(^|\/ ?|; ?)[0-9]+,[0-9]')
        self.re_639ef0ac = re.compile(r'^[0-9]+(?:\.[0-9]+)?[A-Z]{3}')
        self.re_641b0e32 = re.compile(r'^[^@]+\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w) ?@.')
        self.re_703b3dbd = re.compile(r'^(yes|no)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_hasSimpleChargeFix = False

        # *[charge:conditional=~/\p{Sc}/]
        # *[charge=~/\p{Sc}/]
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3e47ea39), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3e47ea39), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:1/3"
                # throwWarning:tr("Expected 3-character currency code in {0}, found {1} instead","{0.key}",get(regexp_match("^.*(\\p{Sc}).*$",tag("{0.key}")),1))
                # assertMatch:"node charge:conditional=\"0.22 $/liter @ (Mo-Fr)\""
                # assertNoMatch:"node charge=\"0.223 USD/m³\""
                # assertMatch:"node charge=€12"
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 1, 'text': mapcss.tr('Expected 3-character currency code in {0}, found {1} instead', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.get(mapcss.regexp_match(self.re_37963245, mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}'))), 1))})

        # *[charge:conditional=~/^[A-Z]{3} ?[0-9]/]!.hasSimpleChargeFix
        # *[charge=~/^[A-Z]{3} ?[0-9]/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2b54497a), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2b54497a), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:2/3"
                # throwWarning:tr("The value should be before the currency code {0} in {1}",substring(tag("{0.key}"),0,3),"{0.key}")
                # assertNoMatch:"node charge=\"0.223 USD/m³\""
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 2, 'text': mapcss.tr('The value should be before the currency code {0} in {1}', mapcss.substring(mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}')), 0, 3), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[0-9]+(?:\.[0-9]+)?[A-Z]{3}/]!.hasSimpleChargeFix
        # *[charge=~/^[0-9]+(?:\.[0-9]+)?[A-Z]{3}/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_639ef0ac), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_639ef0ac), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:3/3"
                # throwWarning:tr("The value and the currency symbol in {0} should be separated by a space","{0.key}")
                # assertNoMatch:"node charge=\"0.223 USD/m³\""
                # assertNoMatch:"node charge=\"12 EUR\""
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 3, 'text': mapcss.tr('The value and the currency symbol in {0} should be separated by a space', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[0-9]+(?:\.[0-9]+)?( ?@| ?\/)/]!.hasSimpleChargeFix
        # *[charge=~/^[0-9]+(?:\.[0-9]+)?($| ?\/)/][charge!=0]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_144caed9), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5d52f832), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'charge') != mapcss._value_capture(capture_tags, 1, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:4/3"
                # throwWarning:tr("Currency not specified in {0}","{0.key}")
                # assertNoMatch:"node charge=\"0.223 USD/m³\""
                # assertNoMatch:"node charge=0"
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 4, 'text': mapcss.tr('Currency not specified in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional][charge:conditional=~/^(yes|no) ?@/]
        # *[charge][charge=~/^(yes|no)$/]
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33603a31), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'charge')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_703b3dbd), mapcss._tag_capture(capture_tags, 1, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:5/3"
                # throwWarning:tr("Key {0} should contain the amount charged","{0.key}")
                # suggestAlternative:"fee:conditional={0.value} @ ..."
                # suggestAlternative:"fee={0.value}"
                # suggestAlternative:"toll:conditional={0.value} @ ..."
                # suggestAlternative:"toll={0.value}"
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 5, 'text': mapcss.tr('Key {0} should contain the amount charged', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/(^|\/ ?|; ?)[0-9]+,[0-9]/]!.hasSimpleChargeFix
        # *[charge=~/(^|\/ ?|; ?)[0-9]+,[0-9]/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6221e95a), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6221e95a), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:6/3"
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # assertNoMatch:"node charge=\"0.223 USD/30.4 m³\""
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 6, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^([0-9]+(?:\.[0-9]+)? ?[A-Za-z _-]+|[A-Za-z _-]+ ?[0-9]+(?:\.[0-9]+)?)/][charge:conditional!~/^[0-9]+(?:\.[0-9]+)? ?[A-Z]{3}/]!.hasSimpleChargeFix
        # *[charge=~/^([0-9]+(?:\.[0-9]+)? ?[A-Za-z _-]+|[A-Za-z _-]+ ?[0-9]+(?:\.[0-9]+)?)/][charge!~/^[0-9]+(?:\.[0-9]+)? ?[A-Z]{3}/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_467f0986), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2e5fc639, '^[0-9]+(?:\\.[0-9]+)? ?[A-Z]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_467f0986), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2e5fc639, '^[0-9]+(?:\\.[0-9]+)? ?[A-Z]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:7/3"
                # throwWarning:tr("Invalid currency code in {0}, should be a 3-letter (uppercase) code after the value","{0.key}")
                # assertNoMatch:"node charge:conditional=\"0.223 USD @ (Mo-Fr)\""
                # assertNoMatch:"node charge=\"0.223 USD/m³\""
                # assertNoMatch:"node charge=\"0.223USD\""
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 7, 'text': mapcss.tr('Invalid currency code in {0}, should be a 3-letter (uppercase) code after the value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[^@]+\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w) ?@./]!.hasSimpleChargeFix
        # *[charge=~/\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w)$/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_641b0e32), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_08865a26), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:8/3"
                # throwWarning:tr("Abbreviated time unit in {0}","{0.key}")
                # assertNoMatch:"node charge=\"0.22 USD/liter/hour\""
                # assertNoMatch:"node charge=\"12.223 YEN/12.4 m³/30.1 minutes\""
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 8, 'text': mapcss.tr('Abbreviated time unit in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[^@]+\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+( ?@| ?\/)./]!.hasSimpleChargeFix
        # *[charge=~/\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+($| ?\/)/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_1fcedb6f), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_45863706), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:9/3"
                # throwWarning:tr("No space between value and unit in {0}","{0.key}")
                # assertNoMatch:"node charge=\"0.22 USD/liter/hour\""
                # assertNoMatch:"node charge=\"12.223 YEN/12.4 m³/30.1 minutes\""
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 9, 'text': mapcss.tr('No space between value and unit in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional][charge:conditional!~/^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})? ?@)./]!.hasSimpleChargeFix
        # *[charge][charge!=0][charge!~/^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})?(?:; ?(?!$)|$))+$/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61f9f7ad, '^(?:[0-9]+(?:\\.[0-9]+)? [A-Z]{3}(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-z]{3,})? ?@).'), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'charge')) and (mapcss._tag_capture(capture_tags, 1, tags, 'charge') != mapcss._value_capture(capture_tags, 1, 0)) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_31192e6e, '^(?:[0-9]+(?:\\.[0-9]+)? [A-Z]{3}(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-z]{3,})?(?:; ?(?!$)|$))+$'), mapcss._tag_capture(capture_tags, 2, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:999/3"
                # throwWarning:tr("The charge in {0} should be structured as <(decimal) number><space><(uppercase) three letter currency code>[/optional unit][/optional time unit]","{0.key}")
                # assertNoMatch:"node charge:conditional=\"12.223 YEN/12.4 m³/30.1 minutes @ Fr-Su\""
                # assertNoMatch:"node charge=\"0.22 USD / liter / hour\""
                # assertNoMatch:"node charge=\"0.22 USD/liter/hour\""
                # assertNoMatch:"node charge=\"0.223 USD/liter\""
                # assertNoMatch:"node charge=\"12 EUR\""
                # assertNoMatch:"node charge=\"12 EUR/person; 6 EUR/child\""
                # assertNoMatch:"node charge=\"12.223 YEN/1 person/1 hour\""
                # assertNoMatch:"node charge=\"12.223 YEN/100 kWh/day\""
                # assertNoMatch:"node charge=\"12.223 YEN/12.4 m³/30.1 minutes\""
                # assertNoMatch:"node charge=0"
                err.append({'class': 30916, 'subclass': 999, 'text': mapcss.tr('The charge in {0} should be structured as <(decimal) number><space><(uppercase) three letter currency code>[/optional unit][/optional time unit]', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_hasSimpleChargeFix = False

        # *[charge:conditional=~/\p{Sc}/]
        # *[charge=~/\p{Sc}/]
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3e47ea39), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3e47ea39), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:1/3"
                # throwWarning:tr("Expected 3-character currency code in {0}, found {1} instead","{0.key}",get(regexp_match("^.*(\\p{Sc}).*$",tag("{0.key}")),1))
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 1, 'text': mapcss.tr('Expected 3-character currency code in {0}, found {1} instead', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.get(mapcss.regexp_match(self.re_37963245, mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}'))), 1))})

        # *[charge:conditional=~/^[A-Z]{3} ?[0-9]/]!.hasSimpleChargeFix
        # *[charge=~/^[A-Z]{3} ?[0-9]/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2b54497a), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2b54497a), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:2/3"
                # throwWarning:tr("The value should be before the currency code {0} in {1}",substring(tag("{0.key}"),0,3),"{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 2, 'text': mapcss.tr('The value should be before the currency code {0} in {1}', mapcss.substring(mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}')), 0, 3), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[0-9]+(?:\.[0-9]+)?[A-Z]{3}/]!.hasSimpleChargeFix
        # *[charge=~/^[0-9]+(?:\.[0-9]+)?[A-Z]{3}/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_639ef0ac), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_639ef0ac), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:3/3"
                # throwWarning:tr("The value and the currency symbol in {0} should be separated by a space","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 3, 'text': mapcss.tr('The value and the currency symbol in {0} should be separated by a space', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[0-9]+(?:\.[0-9]+)?( ?@| ?\/)/]!.hasSimpleChargeFix
        # *[charge=~/^[0-9]+(?:\.[0-9]+)?($| ?\/)/][charge!=0]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_144caed9), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5d52f832), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'charge') != mapcss._value_capture(capture_tags, 1, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:4/3"
                # throwWarning:tr("Currency not specified in {0}","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 4, 'text': mapcss.tr('Currency not specified in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional][charge:conditional=~/^(yes|no) ?@/]
        # *[charge][charge=~/^(yes|no)$/]
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33603a31), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'charge')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_703b3dbd), mapcss._tag_capture(capture_tags, 1, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:5/3"
                # throwWarning:tr("Key {0} should contain the amount charged","{0.key}")
                # suggestAlternative:"fee:conditional={0.value} @ ..."
                # suggestAlternative:"fee={0.value}"
                # suggestAlternative:"toll:conditional={0.value} @ ..."
                # suggestAlternative:"toll={0.value}"
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 5, 'text': mapcss.tr('Key {0} should contain the amount charged', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/(^|\/ ?|; ?)[0-9]+,[0-9]/]!.hasSimpleChargeFix
        # *[charge=~/(^|\/ ?|; ?)[0-9]+,[0-9]/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6221e95a), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6221e95a), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:6/3"
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 6, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^([0-9]+(?:\.[0-9]+)? ?[A-Za-z _-]+|[A-Za-z _-]+ ?[0-9]+(?:\.[0-9]+)?)/][charge:conditional!~/^[0-9]+(?:\.[0-9]+)? ?[A-Z]{3}/]!.hasSimpleChargeFix
        # *[charge=~/^([0-9]+(?:\.[0-9]+)? ?[A-Za-z _-]+|[A-Za-z _-]+ ?[0-9]+(?:\.[0-9]+)?)/][charge!~/^[0-9]+(?:\.[0-9]+)? ?[A-Z]{3}/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_467f0986), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2e5fc639, '^[0-9]+(?:\\.[0-9]+)? ?[A-Z]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_467f0986), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2e5fc639, '^[0-9]+(?:\\.[0-9]+)? ?[A-Z]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:7/3"
                # throwWarning:tr("Invalid currency code in {0}, should be a 3-letter (uppercase) code after the value","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 7, 'text': mapcss.tr('Invalid currency code in {0}, should be a 3-letter (uppercase) code after the value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[^@]+\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w) ?@./]!.hasSimpleChargeFix
        # *[charge=~/\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w)$/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_641b0e32), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_08865a26), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:8/3"
                # throwWarning:tr("Abbreviated time unit in {0}","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 8, 'text': mapcss.tr('Abbreviated time unit in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[^@]+\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+( ?@| ?\/)./]!.hasSimpleChargeFix
        # *[charge=~/\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+($| ?\/)/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_1fcedb6f), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_45863706), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:9/3"
                # throwWarning:tr("No space between value and unit in {0}","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 9, 'text': mapcss.tr('No space between value and unit in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional][charge:conditional!~/^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})? ?@)./]!.hasSimpleChargeFix
        # *[charge][charge!=0][charge!~/^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})?(?:; ?(?!$)|$))+$/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61f9f7ad, '^(?:[0-9]+(?:\\.[0-9]+)? [A-Z]{3}(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-z]{3,})? ?@).'), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'charge')) and (mapcss._tag_capture(capture_tags, 1, tags, 'charge') != mapcss._value_capture(capture_tags, 1, 0)) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_31192e6e, '^(?:[0-9]+(?:\\.[0-9]+)? [A-Z]{3}(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-z]{3,})?(?:; ?(?!$)|$))+$'), mapcss._tag_capture(capture_tags, 2, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:999/3"
                # throwWarning:tr("The charge in {0} should be structured as <(decimal) number><space><(uppercase) three letter currency code>[/optional unit][/optional time unit]","{0.key}")
                err.append({'class': 30916, 'subclass': 999, 'text': mapcss.tr('The charge in {0} should be structured as <(decimal) number><space><(uppercase) three letter currency code>[/optional unit][/optional time unit]', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_hasSimpleChargeFix = False

        # *[charge:conditional=~/\p{Sc}/]
        # *[charge=~/\p{Sc}/]
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3e47ea39), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3e47ea39), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:1/3"
                # throwWarning:tr("Expected 3-character currency code in {0}, found {1} instead","{0.key}",get(regexp_match("^.*(\\p{Sc}).*$",tag("{0.key}")),1))
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 1, 'text': mapcss.tr('Expected 3-character currency code in {0}, found {1} instead', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.get(mapcss.regexp_match(self.re_37963245, mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}'))), 1))})

        # *[charge:conditional=~/^[A-Z]{3} ?[0-9]/]!.hasSimpleChargeFix
        # *[charge=~/^[A-Z]{3} ?[0-9]/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2b54497a), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2b54497a), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:2/3"
                # throwWarning:tr("The value should be before the currency code {0} in {1}",substring(tag("{0.key}"),0,3),"{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 2, 'text': mapcss.tr('The value should be before the currency code {0} in {1}', mapcss.substring(mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}')), 0, 3), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[0-9]+(?:\.[0-9]+)?[A-Z]{3}/]!.hasSimpleChargeFix
        # *[charge=~/^[0-9]+(?:\.[0-9]+)?[A-Z]{3}/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_639ef0ac), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_639ef0ac), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:3/3"
                # throwWarning:tr("The value and the currency symbol in {0} should be separated by a space","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 3, 'text': mapcss.tr('The value and the currency symbol in {0} should be separated by a space', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[0-9]+(?:\.[0-9]+)?( ?@| ?\/)/]!.hasSimpleChargeFix
        # *[charge=~/^[0-9]+(?:\.[0-9]+)?($| ?\/)/][charge!=0]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_144caed9), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5d52f832), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'charge') != mapcss._value_capture(capture_tags, 1, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:4/3"
                # throwWarning:tr("Currency not specified in {0}","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 4, 'text': mapcss.tr('Currency not specified in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional][charge:conditional=~/^(yes|no) ?@/]
        # *[charge][charge=~/^(yes|no)$/]
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_33603a31), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'charge')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_703b3dbd), mapcss._tag_capture(capture_tags, 1, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:5/3"
                # throwWarning:tr("Key {0} should contain the amount charged","{0.key}")
                # suggestAlternative:"fee:conditional={0.value} @ ..."
                # suggestAlternative:"fee={0.value}"
                # suggestAlternative:"toll:conditional={0.value} @ ..."
                # suggestAlternative:"toll={0.value}"
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 5, 'text': mapcss.tr('Key {0} should contain the amount charged', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/(^|\/ ?|; ?)[0-9]+,[0-9]/]!.hasSimpleChargeFix
        # *[charge=~/(^|\/ ?|; ?)[0-9]+,[0-9]/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6221e95a), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6221e95a), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:6/3"
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 6, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^([0-9]+(?:\.[0-9]+)? ?[A-Za-z _-]+|[A-Za-z _-]+ ?[0-9]+(?:\.[0-9]+)?)/][charge:conditional!~/^[0-9]+(?:\.[0-9]+)? ?[A-Z]{3}/]!.hasSimpleChargeFix
        # *[charge=~/^([0-9]+(?:\.[0-9]+)? ?[A-Za-z _-]+|[A-Za-z _-]+ ?[0-9]+(?:\.[0-9]+)?)/][charge!~/^[0-9]+(?:\.[0-9]+)? ?[A-Z]{3}/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_467f0986), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2e5fc639, '^[0-9]+(?:\\.[0-9]+)? ?[A-Z]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_467f0986), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2e5fc639, '^[0-9]+(?:\\.[0-9]+)? ?[A-Z]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:7/3"
                # throwWarning:tr("Invalid currency code in {0}, should be a 3-letter (uppercase) code after the value","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 7, 'text': mapcss.tr('Invalid currency code in {0}, should be a 3-letter (uppercase) code after the value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[^@]+\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w) ?@./]!.hasSimpleChargeFix
        # *[charge=~/\/ ?(?:[0-9]+(?:\.[0-9]+)? ?)?(min|s|h|d|w)$/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_641b0e32), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_08865a26), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:8/3"
                # throwWarning:tr("Abbreviated time unit in {0}","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 8, 'text': mapcss.tr('Abbreviated time unit in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional=~/^[^@]+\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+( ?@| ?\/)./]!.hasSimpleChargeFix
        # *[charge=~/\/ ?[0-9]+(?:\.[0-9]+)?[a-zA-Z³]+($| ?\/)/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_1fcedb6f), mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_45863706), mapcss._tag_capture(capture_tags, 0, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set .hasSimpleChargeFix
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:9/3"
                # throwWarning:tr("No space between value and unit in {0}","{0.key}")
                set_hasSimpleChargeFix = True
                err.append({'class': 30916, 'subclass': 9, 'text': mapcss.tr('No space between value and unit in {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[charge:conditional][charge:conditional!~/^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})? ?@)./]!.hasSimpleChargeFix
        # *[charge][charge!=0][charge!~/^(?:[0-9]+(?:\.[0-9]+)? [A-Z]{3}(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\/ ?(?:[0-9]+(?:\.[0-9]+)? )?[a-z]{3,})?(?:; ?(?!$)|$))+$/]!.hasSimpleChargeFix
        if ('charge' in keys) or ('charge:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'charge:conditional')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61f9f7ad, '^(?:[0-9]+(?:\\.[0-9]+)? [A-Z]{3}(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-z]{3,})? ?@).'), mapcss._tag_capture(capture_tags, 1, tags, 'charge:conditional'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_hasSimpleChargeFix) and (mapcss._tag_capture(capture_tags, 0, tags, 'charge')) and (mapcss._tag_capture(capture_tags, 1, tags, 'charge') != mapcss._value_capture(capture_tags, 1, 0)) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_31192e6e, '^(?:[0-9]+(?:\\.[0-9]+)? [A-Z]{3}(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-zA-Z³]+)?(?: ?\\/ ?(?:[0-9]+(?:\\.[0-9]+)? )?[a-z]{3,})?(?:; ?(?!$)|$))+$'), mapcss._tag_capture(capture_tags, 2, tags, 'charge'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Invalid value of charge")
                # -osmoseItemClassLevel:"3091/30916:999/3"
                # throwWarning:tr("The charge in {0} should be structured as <(decimal) number><space><(uppercase) three letter currency code>[/optional unit][/optional time unit]","{0.key}")
                err.append({'class': 30916, 'subclass': 999, 'text': mapcss.tr('The charge in {0} should be structured as <(decimal) number><space><(uppercase) three letter currency code>[/optional unit][/optional time unit]', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_Charge(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'charge:conditional': '0.22 $/liter @ (Mo-Fr)'}), expected={'class': 30916, 'subclass': 1})
        self.check_not_err(n.node(data, {'charge': '0.223 USD/m³'}), expected={'class': 30916, 'subclass': 1})
        self.check_err(n.node(data, {'charge': '€12'}), expected={'class': 30916, 'subclass': 1})
        self.check_not_err(n.node(data, {'charge': '0.223 USD/m³'}), expected={'class': 30916, 'subclass': 2})
        self.check_not_err(n.node(data, {'charge': '0.223 USD/m³'}), expected={'class': 30916, 'subclass': 3})
        self.check_not_err(n.node(data, {'charge': '12 EUR'}), expected={'class': 30916, 'subclass': 3})
        self.check_not_err(n.node(data, {'charge': '0.223 USD/m³'}), expected={'class': 30916, 'subclass': 4})
        self.check_not_err(n.node(data, {'charge': '0'}), expected={'class': 30916, 'subclass': 4})
        self.check_not_err(n.node(data, {'charge': '0.223 USD/30.4 m³'}), expected={'class': 30916, 'subclass': 6})
        self.check_not_err(n.node(data, {'charge:conditional': '0.223 USD @ (Mo-Fr)'}), expected={'class': 30916, 'subclass': 7})
        self.check_not_err(n.node(data, {'charge': '0.223 USD/m³'}), expected={'class': 30916, 'subclass': 7})
        self.check_not_err(n.node(data, {'charge': '0.223USD'}), expected={'class': 30916, 'subclass': 7})
        self.check_not_err(n.node(data, {'charge': '0.22 USD/liter/hour'}), expected={'class': 30916, 'subclass': 8})
        self.check_not_err(n.node(data, {'charge': '12.223 YEN/12.4 m³/30.1 minutes'}), expected={'class': 30916, 'subclass': 8})
        self.check_not_err(n.node(data, {'charge': '0.22 USD/liter/hour'}), expected={'class': 30916, 'subclass': 9})
        self.check_not_err(n.node(data, {'charge': '12.223 YEN/12.4 m³/30.1 minutes'}), expected={'class': 30916, 'subclass': 9})
        self.check_not_err(n.node(data, {'charge:conditional': '12.223 YEN/12.4 m³/30.1 minutes @ Fr-Su'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '0.22 USD / liter / hour'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '0.22 USD/liter/hour'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '0.223 USD/liter'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '12 EUR'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '12 EUR/person; 6 EUR/child'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '12.223 YEN/1 person/1 hour'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '12.223 YEN/100 kWh/day'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '12.223 YEN/12.4 m³/30.1 minutes'}), expected={'class': 30916, 'subclass': 999})
        self.check_not_err(n.node(data, {'charge': '0'}), expected={'class': 30916, 'subclass': 999})
