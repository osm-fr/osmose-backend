#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_numeric(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/numeric.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9006001] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('numerical key'))
        self.errors[9006002] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('{0} value with + sign', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006003] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006004] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006008] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006009] = self.def_class(item = 9006, level = 2, tags = ["tag", "value"], title = mapcss.tr('{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006010] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006011] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006013] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('voltage should be in volts with no units/delimiter/spaces'))
        self.errors[9006017] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006021] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('Unnecessary amount of decimal places'))
        self.errors[9006022] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('Airport tagging'))
        self.errors[9006023] = self.def_class(item = 9006, level = 2, tags = ["tag", "value"], title = mapcss.tr('negative {0} value', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006024] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unusual value of {0}: use abbreviation for unit and space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006025] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unnecessary tag'))
        self.errors[9006026] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('kilometers')))
        self.errors[9006027] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9006028] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'))
        self.errors[9006029] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('imprecise value of {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9006030] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('suspicious tag combination'))
        self.errors[9006031] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unusual value of {0}: use \'\' for foot and " for inches, no spaces', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006032] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('unusual value of {0}: meters is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9006033] = self.def_class(item = 9006, level = 3, tags = ["tag", "value"], title = mapcss.tr('Unusually large value of {0} in meters, possibly centimeter units are meant?', mapcss._tag_uncapture(capture_tags, '{0.key}')))

        self.re_066203d3 = re.compile(r'^[0-9]+$')
        self.re_09e9525d = re.compile(r'^[0-9]+,[0-9][0-9]?( (t|kg|st|lbs))?$')
        self.re_0ae2edfd = re.compile(r'^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$')
        self.re_0b0f0f56 = re.compile(r'^0$|^(-|\+)?[1-5]$')
        self.re_0f74b227 = re.compile(r'^(0|1|2|3|4|5|6|7|8)((;|-)(1|2|3|4|5|6|7|8))*$')
        self.re_12c23878 = re.compile(r'^(?i)-?[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$')
        self.re_17733c6c = re.compile(r'^(([1-9][0-9]*(\.[0-9]+)?( (minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)))|(no|unlimited|0|load-unload))$')
        self.re_19ef4172 = re.compile(r'^([1-9][0-9]*(\.[0-9]+)? h)$')
        self.re_1b78ea82 = re.compile(r'^([1-9][0-9]*(\.[0-9]+)? min)$')
        self.re_21cf6a81 = re.compile(r'^-?[0-9]+,[0-9][0-9]?( m|\')?$')
        self.re_23eb7c0d = re.compile(r'^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)((-|;)([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$')
        self.re_270eb4ce = re.compile(r'^(?i)[1-9][0-9]*([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$')
        self.re_288e587a = re.compile(r'^\+\d')
        self.re_2a784076 = re.compile(r'^(([0-9]|[1-9][0-9]*)(\.5)?)$')
        self.re_2b4f97f5 = re.compile(r'^([0-9]+(\.[0-9]+)?( (t|kg|st|lbs))?)$')
        self.re_2b84c9ab = re.compile(r'^[0-9]+,[0-9][0-9]?$')
        self.re_330da7b0 = re.compile(r'^([1-9][0-9]*(\.[0-9]+)? hr)$')
        self.re_33ecb9da = re.compile(r'^((14(?:3[0-4]|[4-9])|(?:14[0-2]|(?:1[0-3]|9)[0-9])[0-9]?|143|(?:[2-7][0-9]|1[5-9])[0-9]|8(?:[0-8][0-9]|9[0-9]?));?)+$')
        self.re_3c02ab12 = re.compile(r'^0*(\.0*)?( (m|ft))?$')
        self.re_40277cab = re.compile(r'^(([1-9][0-9]*(\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$')
        self.re_41726192 = re.compile(r'^(([0-9]+(\.[0-9]+)?( (m|km|mi|nmi))?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$')
        self.re_43c55ce5 = re.compile(r'(.*[A-Za-z].*)|.*,.*|.*( ).*')
        self.re_45b46d60 = re.compile(r'^-?[0-9]+(\.[0-9]+)?$')
        self.re_45e73e1b = re.compile(r'^(up|down|-?([0-9]+?(\.[1-9]%)?|100)[%°]?)$')
        self.re_470ea515 = re.compile(r'^(-?([0-9]+(\.[0-9]+)?( m)?)|(-?[1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$')
        self.re_4a678586 = re.compile(r'^(([0-9]+(\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$')
        self.re_4d44d8e0 = re.compile(r'^(0|[1-9][0-9]*(\.[0-9]+)?)( (kHz|MHz|GHz|THz))?$')
        self.re_52f27115 = re.compile(r'^([1-9][0-9]*(\.[0-9]+)?h)$')
        self.re_5478d8af = re.compile(r'^[1-9]([0-9]*)$')
        self.re_549d66c4 = re.compile(r'^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$')
        self.re_55d147d6 = re.compile(r'^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$')
        self.re_58d78904 = re.compile(r'^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*)$')
        self.re_5a7f47b9 = re.compile(r'^-?[0-9]+\.[0-9][0-9][0-9]+$')
        self.re_5a9b9c26 = re.compile(r'^(broad|standard|narrow)$')
        self.re_5dbcb7bc = re.compile(r'^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$')
        self.re_5f1f731d = re.compile(r'^([0-9][0-9]?[0-9]?|[0-9]+[0-9]:[0-5][0-9](:[0-5][0-9])?)$')
        self.re_6a0eca39 = re.compile(r'^[0-9]+,[0-9][0-9]?( m|\')?$')
        self.re_6aa93c30 = re.compile(r'^[A-Z]{3}$')
        self.re_6ae26377 = re.compile(r'([0-9.,]+) *.+')
        self.re_70dc3282 = re.compile(r'^narrow_gauge$')
        self.re_762a1d1d = re.compile(r'^-?[0-9]+(\.[0-9]+)? ?m$')
        self.re_76fe90df = re.compile(r'^(([0-9]+(\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$')
        self.re_7afc6883 = re.compile(r'^[A-Z]{4}$')
        self.re_7b1365b7 = re.compile(r'^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)')
        self.re_7e626945 = re.compile(r'railway$')
        self.re_7f163374 = re.compile(r'^(1|2|3|4|5|6|7|8|9|10|11|12)$')
        self.re_7f19b94b = re.compile(r'^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set__unit_auto_fix = set_ele_meter_remove_autofix = set_ele_separator_autofix = set_imprecise_gauge = set_maxstay_autofix = set_negative_value = set_unusual_gauge = set_zero_roof_height_flat = False

        # *[/^[0-9]+$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("numerical key")
                err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr('numerical key')})

        # *[layer=~/^\+\d/]
        if ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_288e587a), mapcss._tag_capture(capture_tags, 0, tags, 'layer'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value with + sign","{0.key}")
                # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
                # assertMatch:"node layer=+1"
                # assertNoMatch:"node layer=+foo"
                # assertNoMatch:"node layer=-1"
                # assertNoMatch:"node layer=1"
                err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr('{0} value with + sign', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('layer=', mapcss.replace(mapcss.tag(tags, 'layer'), '+', ''))).split('=', 1)])
                }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'layer')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0b0f0f56, '^0$|^(-|\\+)?[1-5]$'), mapcss._tag_capture(capture_tags, 1, tags, 'layer'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be an integer value between -5 and 5","{0.key}")
                # assertMatch:"node layer=+10"
                # assertNoMatch:"node layer=+5"
                # assertNoMatch:"node layer=-5"
                # assertMatch:"node layer=-50"
                # assertNoMatch:"node layer=0"
                # assertMatch:"node layer=0.5"
                # assertMatch:"node layer=0;1"
                # assertNoMatch:"node layer=2"
                # assertMatch:"node layer=6"
                err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr('{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[building:levels^="-"]
        if ('building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'building:levels'), mapcss._value_capture(capture_tags, 0, '-'))))
                except mapcss.RuleAbort: pass
            if match:
                # set negative_value
                # throwError:tr("negative {0} value","{0.key}")
                # assertNoMatch:"node building:levels=+1"
                # assertMatch:"node building:levels=-1"
                # assertMatch:"node building:levels=-foo"
                # assertNoMatch:"node building:levels=1"
                # assertNoMatch:"node building:levels=foo"
                # assertNoMatch:"node level=-1"
                set_negative_value = True
                err.append({'class': 9006023, 'subclass': 29188290, 'text': mapcss.tr('negative {0} value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]!.negative_value
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if ('building:levels' in keys) or ('level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_negative_value) and (mapcss._tag_capture(capture_tags, 0, tags, 'building:levels')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2a784076, '^(([0-9]|[1-9][0-9]*)(\\.5)?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'building:levels'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7f19b94b, '^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\\.5)?)|-0\\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\\.5)?)|-0\\.5))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
                # assertNoMatch:"node building:levels=-1"
                # assertNoMatch:"node building:levels=0"
                # assertNoMatch:"node building:levels=1.5"
                # assertMatch:"node building:levels=1A"
                # assertMatch:"node level=-0"
                # assertNoMatch:"node level=-0.5"
                # assertNoMatch:"node level=-0.5;0"
                # assertMatch:"node level=-01.5"
                # assertMatch:"node level=-03"
                # assertNoMatch:"node level=-1"
                # assertNoMatch:"node level=-1;-0.5"
                # assertNoMatch:"node level=0"
                # assertMatch:"node level=01"
                # assertNoMatch:"node level=0;-0.5"
                # assertNoMatch:"node level=0;1"
                # assertNoMatch:"node level=1"
                # assertNoMatch:"node level=1.5"
                # assertNoMatch:"node level=12"
                # assertNoMatch:"node level=1;0.5"
                # assertNoMatch:"node level=1;1.5"
                # assertMatch:"node level=2.3"
                # assertMatch:"node level=one"
                err.append({'class': 9006004, 'subclass': 1292315112, 'text': mapcss.tr('{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[roof:height][roof:height=~/^0*(\.0*)?( (m|ft))?$/][roof:shape=flat]
        if ('roof:height' in keys and 'roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3c02ab12), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'roof:shape') == mapcss._value_capture(capture_tags, 2, 'flat')))
                except mapcss.RuleAbort: pass
            if match:
                # set zero_roof_height_flat
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{2.tag}")
                # fixRemove:"{0.key}"
                # assertMatch:"node roof:height=0 roof:shape=flat"
                # assertNoMatch:"node roof:height=0 roof:shape=gabled"
                # assertMatch:"node roof:shape=flat roof:height=\"00.00000 ft\" roof:shape=flat"
                # assertNoMatch:"node roof:shape=flat roof:height=2 m roof:shape=flat"
                set_zero_roof_height_flat = True
                err.append({'class': 9006025, 'subclass': 1379670484, 'text': mapcss.tr('{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[height][height=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[roof:height][roof:height=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]!.zero_roof_height_flat
        # *[width][width=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxwidth][maxwidth=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[min_height][min_height=~/^(?i)-?[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxheight][maxheight=~/^(?i)[1-9][0-9]*([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxlength][maxlength=~/^(?i)[1-9][0-9]*([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_12c23878), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_270eb4ce), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_270eb4ce), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use abbreviation for unit and space between value and unit","{0.key}")
                # fixAdd:concat("{0.key}","=",get(regexp_match("([0-9.,]+) *.+","{0.value}"),1)," m")
                # assertNoMatch:"node height=2 m"
                # assertMatch:"node height=2m"
                # assertMatch:"node height=5  metre"
                # assertNoMatch:"node height=5"
                # assertMatch:"node height=6,78 meters"
                # assertMatch:"node height=6.78 meters"
                # assertNoMatch:"node maxheight=2 m"
                # assertMatch:"node maxheight=2m"
                # assertMatch:"node maxheight=5  metre"
                # assertNoMatch:"node maxheight=5"
                # assertMatch:"node maxheight=6.78 meters"
                # assertNoMatch:"node maxlength=2 m"
                # assertMatch:"node maxlength=2m"
                # assertMatch:"node maxlength=5  metre"
                # assertNoMatch:"node maxlength=5"
                # assertMatch:"node maxlength=6.78 meters"
                # assertNoMatch:"node maxwidth=2 m"
                # assertMatch:"node maxwidth=2m"
                # assertMatch:"node maxwidth=5  metre"
                # assertNoMatch:"node maxwidth=5"
                # assertMatch:"node maxwidth=6.78 meters"
                # assertNoMatch:"node min_height=2 m"
                # assertMatch:"node min_height=2m"
                # assertMatch:"node min_height=5  metre"
                # assertNoMatch:"node min_height=5"
                # assertMatch:"node min_height=6.78 meters"
                # assertNoMatch:"node roof:height=2 m"
                # assertMatch:"node roof:height=2m"
                # assertMatch:"node roof:height=5  metre"
                # assertNoMatch:"node roof:height=5"
                # assertMatch:"node roof:height=6.78 meters"
                # assertNoMatch:"node width=2 m"
                # assertMatch:"node width=2m"
                # assertMatch:"node width=5  metre"
                # assertNoMatch:"node width=5"
                # assertMatch:"node width=6.78 meters"
                set__unit_auto_fix = True
                err.append({'class': 9006024, 'subclass': 1245344673, 'text': mapcss.tr('unusual value of {0}: use abbreviation for unit and space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.get(mapcss.regexp_match(self.re_6ae26377, mapcss._tag_uncapture(capture_tags, '{0.value}')), 1), ' m')).split('=', 1)])
                }})

        # *[height][height=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[maxheight][maxheight=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[roof:height][roof:height=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]!.zero_roof_height_flat
        # *[maxlength][maxlength=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[width][width=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[maxwidth][maxwidth=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use '' for foot and \" for inches, no spaces","{0.key}")
                # fixAdd:concat("{0.key}","=",get(regexp_match("([0-9.,]+) *.+","{0.value}"),1),"'")
                # assertMatch:"node height=2 '"
                # assertNoMatch:"node height=2'"
                # assertMatch:"node maxheight=2 '"
                # assertNoMatch:"node maxheight=2'"
                # assertMatch:"node maxlength=2 '"
                # assertNoMatch:"node maxlength=2'"
                # assertMatch:"node maxwidth=2 '"
                # assertNoMatch:"node maxwidth=2'"
                # assertMatch:"node roof:height=2 '"
                # assertNoMatch:"node roof:height=2'"
                # assertMatch:"node width=2 '"
                # assertNoMatch:"node width=2'"
                # assertMatch:"node height=5  Feet"
                # assertNoMatch:"node height=5"
                # assertMatch:"node height=6.78 foot"
                # assertMatch:"node maxheight=5  Feet"
                # assertNoMatch:"node maxheight=5"
                # assertMatch:"node maxheight=6.78 foot"
                # assertMatch:"node maxlength=5  Feet"
                # assertNoMatch:"node maxlength=5"
                # assertMatch:"node maxlength=6.78 foot"
                # assertMatch:"node maxwidth=5  Feet"
                # assertNoMatch:"node maxwidth=5"
                # assertMatch:"node maxwidth=6.78 foot"
                # assertMatch:"node roof:height=5  Feet"
                # assertNoMatch:"node roof:height=5"
                # assertMatch:"node roof:height=6.78 foot"
                # assertMatch:"node width=5  Feet"
                # assertNoMatch:"node width=5"
                # assertMatch:"node width=6.78 foot"
                set__unit_auto_fix = True
                err.append({'class': 9006031, 'subclass': 1118826626, 'text': mapcss.tr('unusual value of {0}: use \'\' for foot and " for inches, no spaces', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.get(mapcss.regexp_match(self.re_6ae26377, mapcss._tag_uncapture(capture_tags, '{0.value}')), 1), '\'')).split('=', 1)])
                }})

        # *[height][height=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxheight][maxheight=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[roof:height][roof:height=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxlength][maxlength=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[width][width=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxwidth][maxwidth=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[min_height][min_height=~/^-?[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxaxleload][maxaxleload=~/^[0-9]+,[0-9][0-9]?( (t|kg|st|lbs))?$/]
        # *[maxweight][maxweight=~/^[0-9]+,[0-9][0-9]?( (t|kg|st|lbs))?$/]
        # *[distance][distance=~/^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$/]
        if ('distance' in keys) or ('height' in keys) or ('maxaxleload' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxweight' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_21cf6a81), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxaxleload')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_09e9525d), mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxweight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_09e9525d), mapcss._tag_capture(capture_tags, 1, tags, 'maxweight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_55d147d6), mapcss._tag_capture(capture_tags, 1, tags, 'distance'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("{0.key}","=",replace(tag("{0.key}"),",","."))
                # assertMatch:"node height=12,5'"
                # assertMatch:"node maxheight=12,5'"
                # assertMatch:"node maxlength=12,5'"
                # assertMatch:"node min_height=12,5'"
                # assertMatch:"node roof:height=12,5'"
                # assertMatch:"node distance=12,00"
                # assertNoMatch:"node distance=12,000"
                # assertNoMatch:"node distance=3,50,5"
                # assertNoMatch:"node distance=3.5"
                # assertNoMatch:"node distance=4"
                # assertMatch:"node distance=5,5"
                # assertMatch:"node height=12,00"
                # assertNoMatch:"node height=12,000"
                # assertNoMatch:"node height=3,50,5"
                # assertNoMatch:"node height=3.5"
                # assertNoMatch:"node height=4"
                # assertMatch:"node height=5,5"
                # assertMatch:"node maxaxleload=12,00"
                # assertNoMatch:"node maxaxleload=12,000"
                # assertNoMatch:"node maxaxleload=3,50,5"
                # assertNoMatch:"node maxaxleload=3.5"
                # assertNoMatch:"node maxaxleload=4"
                # assertMatch:"node maxaxleload=5,5"
                # assertMatch:"node maxheight=12,00"
                # assertNoMatch:"node maxheight=12,000"
                # assertNoMatch:"node maxheight=3,50,5"
                # assertNoMatch:"node maxheight=3.5"
                # assertNoMatch:"node maxheight=4"
                # assertMatch:"node maxheight=5,5"
                # assertMatch:"node maxlength=12,00"
                # assertNoMatch:"node maxlength=12,000"
                # assertNoMatch:"node maxlength=3,50,5"
                # assertNoMatch:"node maxlength=3.5"
                # assertNoMatch:"node maxlength=4"
                # assertMatch:"node maxlength=5,5"
                # assertMatch:"node maxweight=12,00"
                # assertNoMatch:"node maxweight=12,000"
                # assertNoMatch:"node maxweight=3,50,5"
                # assertNoMatch:"node maxweight=3.5"
                # assertNoMatch:"node maxweight=4"
                # assertMatch:"node maxweight=5,5"
                # assertMatch:"node maxwidth=12,00"
                # assertNoMatch:"node maxwidth=12,000"
                # assertNoMatch:"node maxwidth=3,50,5"
                # assertNoMatch:"node maxwidth=3.5"
                # assertNoMatch:"node maxwidth=4"
                # assertMatch:"node maxwidth=5,5"
                # assertMatch:"node min_height=12,00"
                # assertNoMatch:"node min_height=12,000"
                # assertNoMatch:"node min_height=3,50,5"
                # assertNoMatch:"node min_height=3.5"
                # assertNoMatch:"node min_height=4"
                # assertMatch:"node min_height=5,5"
                # assertMatch:"node roof:height=12,00"
                # assertNoMatch:"node roof:height=12,000"
                # assertNoMatch:"node roof:height=3,50,5"
                # assertNoMatch:"node roof:height=3.5"
                # assertNoMatch:"node roof:height=4"
                # assertMatch:"node roof:height=5,5"
                # assertMatch:"node width=12,00"
                # assertNoMatch:"node width=12,000"
                # assertNoMatch:"node width=3,50,5"
                # assertNoMatch:"node width=3.5"
                # assertNoMatch:"node width=4"
                # assertMatch:"node width=5,5"
                set__unit_auto_fix = True
                err.append({'class': 9006017, 'subclass': 1619669445, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.replace(mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}')), ',', '.'))).split('=', 1)])
                }})

        # *[height][height!~/^(([0-9]+(\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!._unit_auto_fix
        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!._unit_auto_fix
        # *[min_height][min_height!~/^(-?([0-9]+(\.[0-9]+)?( m)?)|(-?[1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!._unit_auto_fix
        # *[roof:height][roof:height!~/^(([0-9]+(\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!.zero_roof_height_flat!._unit_auto_fix
        # *[maxlength][maxlength!~/^(([1-9][0-9]*(\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!._unit_auto_fix
        # *[width][width!~/^(([0-9]+(\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]!._unit_auto_fix
        # *[maxwidth][maxwidth!~/^(([0-9]+(\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]!._unit_auto_fix
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_76fe90df, '^(([0-9]+(\\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_40277cab, '^(([1-9][0-9]*(\\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\\.[0-9]*)?\\")?)|none|default|below_default)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_470ea515, '^(-?([0-9]+(\\.[0-9]+)?( m)?)|(-?[1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_76fe90df, '^(([0-9]+(\\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_40277cab, '^(([1-9][0-9]*(\\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\\.[0-9]*)?\\")?)|none|default|below_default)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4a678586, '^(([0-9]+(\\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4a678586, '^(([0-9]+(\\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}")
                # assertNoMatch:"node height=22'"
                # assertNoMatch:"node maxwidth=7'"
                # assertNoMatch:"node width=10'"
                # assertMatch:"node height=\"12. m\""
                # assertNoMatch:"node height=2 m"
                # assertNoMatch:"node height=2.22 m"
                # assertNoMatch:"node height=3"
                # assertNoMatch:"node height=5  m"
                # assertNoMatch:"node height=6.78 m"
                # assertNoMatch:"node height=7.8"
                # assertMatch:"node height=medium"
                # assertMatch:"node maxheight=\"2. m\""
                # assertMatch:"node maxheight=-5"
                # assertMatch:"node maxlength=0"
                # assertMatch:"node maxlength=10'13\""
                # assertMatch:"node min_height=\"12. m\""
                # assertNoMatch:"node min_height=-5"
                # assertMatch:"node width=10'2.\""
                # assertNoMatch:"node width=10'5\""
                err.append({'class': 9006032, 'subclass': 516585238, 'text': mapcss.tr('unusual value of {0}: meters is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[maxaxleload][maxaxleload!~/^([0-9]+(\.[0-9]+)?( (t|kg|st|lbs))?)$/]
        # *[maxweight][maxweight!~/^([0-9]+(\.[0-9]+)?( (t|kg|st|lbs))?)$/]
        if ('maxaxleload' in keys) or ('maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxaxleload')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2b4f97f5, '^([0-9]+(\\.[0-9]+)?( (t|kg|st|lbs))?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxweight')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2b4f97f5, '^([0-9]+(\\.[0-9]+)?( (t|kg|st|lbs))?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxweight'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}",tr("tonne"))
                # assertNoMatch:"node maxaxleload=2"
                # assertNoMatch:"node maxaxleload=2.5"
                # assertNoMatch:"node maxaxleload=7 kg"
                # assertMatch:"node maxaxleload=something"
                # assertMatch:"node maxweight=-5"
                err.append({'class': 9006026, 'subclass': 326659919, 'text': mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('tonne'))})

        # *[distance][distance!~/^(([0-9]+(\.[0-9]+)?( (m|km|mi|nmi))?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]
        if ('distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_41726192, '^(([0-9]+(\\.[0-9]+)?( (m|km|mi|nmi))?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'distance'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}",tr("kilometers"))
                err.append({'class': 9006026, 'subclass': 1210743405, 'text': mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('kilometers'))})

        # *[population][population!~/^[0-9]+$/]
        if ('population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'population')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_066203d3, '^[0-9]+$'), mapcss._tag_capture(capture_tags, 1, tags, 'population'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value","{0.key}")
                err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr('{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[seats][seats!~/^[1-9]([0-9]*)$/][amenity=bench]
        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if ('amenity' in keys and 'screen' in keys) or ('amenity' in keys and 'seats' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seats')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'seats'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'bench')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'screen')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'screen'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'cinema')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} must be a positive integer number","{0.key}")
                # assertNoMatch:"node amenity=cinema screen=8"
                # assertMatch:"node amenity=cinema screen=led"
                err.append({'class': 9006009, 'subclass': 2104305963, 'text': mapcss.tr('{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if ('admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'admin_level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7f163374, '^(1|2|3|4|5|6|7|8|9|10|11|12)$'), mapcss._tag_capture(capture_tags, 1, tags, 'admin_level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertMatch:"node admin_level=-1"
                # assertMatch:"node admin_level=0"
                # assertMatch:"node admin_level=13"
                # assertNoMatch:"node admin_level=5"
                err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)((-|;)([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if ('direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'direction') < mapcss._value_capture(capture_tags, 1, 0)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'direction') >= mapcss._value_capture(capture_tags, 1, 360)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23eb7c0d, '^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)((-|;)([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'direction'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertMatch:"node direction=-10"
                # assertNoMatch:"node direction=0"
                # assertNoMatch:"node direction=0-360"
                # assertMatch:"node direction=1360"
                # assertMatch:"node direction=360"
                # assertNoMatch:"node direction=45"
                # assertNoMatch:"node direction=45-100;190-250;300"
                # assertMatch:"node direction=45-100;190-250;300-"
                # assertNoMatch:"node direction=45-100;190-250;300-360"
                # assertNoMatch:"node direction=90;270"
                # assertMatch:"node direction=C"
                # assertNoMatch:"node direction=N"
                # assertNoMatch:"node direction=NE-S"
                # assertNoMatch:"node direction=NNE"
                # assertMatch:"node direction=NNNE"
                # assertNoMatch:"node direction=anti-clockwise"
                # assertNoMatch:"node direction=anticlockwise"
                # assertNoMatch:"node direction=down"
                # assertNoMatch:"node direction=forward"
                # assertMatch:"node direction=north-down"
                # assertMatch:"node direction=north-east"
                # assertMatch:"node direction=north-south"
                # assertMatch:"node direction=rome"
                # assertNoMatch:"node direction=up"
                # assertNoMatch:"node direction=west"
                err.append({'class': 9006010, 'subclass': 51356092, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_762a1d1d), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # set ele_meter_remove_autofix
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
                # assertMatch:"node ele=-12.1 m"
                # assertMatch:"node ele=12 m"
                # assertNoMatch:"node ele=12"
                # assertMatch:"node ele=12.1m"
                # assertNoMatch:"node ele=12km"
                # assertMatch:"node ele=12m"
                # assertNoMatch:"node ele=high"
                set_ele_meter_remove_autofix = True
                err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr('{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, 'ele'), 'm', '')))).split('=', 1)])
                }})

        # *[ele][ele=~/^[0-9]+,[0-9][0-9]?$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b84c9ab), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # set ele_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("ele=",replace(tag("ele"),",","."))
                # assertMatch:"node ele=12,00"
                # assertNoMatch:"node ele=3,50,5"
                # assertNoMatch:"node ele=3.5"
                # assertNoMatch:"node ele=4"
                # assertMatch:"node ele=5,5"
                # assertNoMatch:"node ele=8,848"
                set_ele_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 202511106, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.replace(mapcss.tag(tags, 'ele'), ',', '.'))).split('=', 1)])
                }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_meter_remove_autofix!.ele_separator_autofix
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_ele_meter_remove_autofix) and (not set_ele_separator_autofix) and (mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_45b46d60, '^-?[0-9]+(\\.[0-9]+)?$'), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                # assertNoMatch:"node ele=-12.1 m"
                # assertNoMatch:"node ele=12 m"
                # assertNoMatch:"node ele=12"
                # assertNoMatch:"node ele=12.1m"
                # assertMatch:"node ele=12km"
                # assertNoMatch:"node ele=12m"
                # assertMatch:"node ele=high"
                err.append({'class': 9006011, 'subclass': 1781084832, 'text': mapcss.tr('{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+\.[0-9][0-9][0-9]+$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5a7f47b9), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Unnecessary amount of decimal places")
                # throwWarning:tr("{0}","{0.tag}")
                # fixAdd:concat("ele=",round(tag("ele")*100)/100)
                # assertMatch:"node ele=-12.6789"
                # assertNoMatch:"node ele=1.12"
                # assertNoMatch:"node ele=12"
                # assertNoMatch:"node ele=12.123 m"
                # assertMatch:"node ele=12.123"
                # assertMatch:"node ele=12.1234"
                # assertNoMatch:"node ele=high"
                err.append({'class': 9006021, 'subclass': 185098060, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.round_(mapcss.tag(tags, 'ele')*100)/100)).split('=', 1)])
                }})

        # node[fire_hydrant:pressure="#"]
        if ('fire_hydrant:pressure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fire_hydrant:pressure') == mapcss._value_capture(capture_tags, 0, '#')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 256087474, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[interval][interval!~/^([0-9][0-9]?[0-9]?|[0-9]+[0-9]:[0-5][0-9](:[0-5][0-9])?)$/]
        if ('interval' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'interval')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5f1f731d, '^([0-9][0-9]?[0-9]?|[0-9]+[0-9]:[0-5][0-9](:[0-5][0-9])?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'interval'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 234727583, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[aeroway=helipad][iata][iata!~/^[A-Z]{3}$/]
        # *[aeroway=aerodrome][iata][iata!~/^[A-Z]{3}$/]
        if ('aeroway' in keys and 'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'iata')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6aa93c30, '^[A-Z]{3}$'), mapcss._tag_capture(capture_tags, 2, tags, 'iata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'iata')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6aa93c30, '^[A-Z]{3}$'), mapcss._tag_capture(capture_tags, 2, tags, 'iata'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                err.append({'class': 9006022, 'subclass': 206938530, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[aeroway=helipad][icao][icao!~/^[A-Z]{4}$/]
        # *[aeroway=aerodrome][icao][icao!~/^[A-Z]{4}$/]
        if ('aeroway' in keys and 'icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7afc6883, '^[A-Z]{4}$'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7afc6883, '^[A-Z]{4}$'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                err.append({'class': 9006022, 'subclass': 311618853, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[aeroway=helipad][icao][icao!~/^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)/]
        # *[aeroway=aerodrome][icao][icao!~/^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)/]
        if ('aeroway' in keys and 'icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7b1365b7, '^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7b1365b7, '^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                err.append({'class': 9006022, 'subclass': 345477776, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[isced:level][isced:level!~/^(0|1|2|3|4|5|6|7|8)((;|-)(1|2|3|4|5|6|7|8))*$/]
        if ('isced:level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'isced:level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0f74b227, '^(0|1|2|3|4|5|6|7|8)((;|-)(1|2|3|4|5|6|7|8))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'isced:level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"node isced:level=0"
                # assertMatch:"node isced:level=0,1,2,3"
                # assertNoMatch:"node isced:level=0-3"
                # assertNoMatch:"node isced:level=0;1;2;3"
                # assertMatch:"node isced:level=10"
                # assertNoMatch:"node isced:level=5"
                # assertMatch:"node isced:level=9"
                # assertMatch:"node isced:level=secondary"
                err.append({'class': 9006010, 'subclass': 1091907371, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[maxstay=0]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # assertMatch:"node maxstay=0"
                # assertNoMatch:"node maxstay=2"
                err.append({'class': 9006027, 'subclass': 1756130010, 'text': mapcss.tr('Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? min)$/][maxstay!="1 min"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b78ea82), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 min', '1 min')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"min","minutes"))
                # assertNoMatch:"node maxstay=\"02 minutes\""
                # assertNoMatch:"node maxstay=\"1 min\""
                # assertMatch:"node maxstay=\"15 min\""
                # assertNoMatch:"node maxstay=\"2 minutes\""
                # assertMatch:"node maxstay=\"5 min\""
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 606655085, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'min', 'minutes'))).split('=', 1)])
                }})

        # *[maxstay="1h"]
        # *[maxstay="1 h"]
        # *[maxstay="1 hr"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1h')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1 h')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1 hr')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:"maxstay=1 hour"
                # assertMatch:"node maxstay=\"1 h\""
                # assertMatch:"node maxstay=\"1 hr\""
                # assertMatch:"node maxstay=1h"
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 872535915, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxstay','1 hour']])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? h)$/][maxstay!="1 h"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19ef4172), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 h', '1 h')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"h","hours"))
                # assertNoMatch:"node maxstay=\"02 hours\""
                # assertNoMatch:"node maxstay=\"1 h\""
                # assertMatch:"node maxstay=\"15 h\""
                # assertNoMatch:"node maxstay=\"2 hours\""
                # assertMatch:"node maxstay=\"5 h\""
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 59629984, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'h', 'hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? hr)$/][maxstay!="1 hr"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_330da7b0), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 hr', '1 hr')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"hr","hours"))
                # assertNoMatch:"node maxstay=\"02 hours\""
                # assertNoMatch:"node maxstay=\"1 hr\""
                # assertMatch:"node maxstay=\"15 hr\""
                # assertNoMatch:"node maxstay=\"2 hours\""
                # assertMatch:"node maxstay=\"5 hr\""
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 814970301, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'hr', 'hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)?h)$/][maxstay!="1h"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_52f27115), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1h', '1h')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"h"," hours"))
                # assertNoMatch:"node maxstay=\"2 h\""
                # assertNoMatch:"node maxstay=\"2 hr\""
                # assertNoMatch:"node maxstay=02hours"
                # assertMatch:"node maxstay=15h"
                # assertNoMatch:"node maxstay=1h"
                # assertNoMatch:"node maxstay=2hours"
                # assertMatch:"node maxstay=5h"
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 1721471777, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'h', ' hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay!~/^(([1-9][0-9]*(\.[0-9]+)?( (minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)))|(no|unlimited|0|load-unload))$/]!.maxstay_autofix
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_maxstay_autofix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_17733c6c, '^(([1-9][0-9]*(\\.[0-9]+)?( (minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)))|(no|unlimited|0|load-unload))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # assertMatch:"node maxstay=\"0 minutes\""
                # assertMatch:"node maxstay=\"1. hours\""
                # assertNoMatch:"node maxstay=\"2.5 hours\""
                # assertNoMatch:"node maxstay=\"66 minutes\""
                # assertNoMatch:"node maxstay=\"7 h\""
                # assertNoMatch:"node maxstay=\"7 hr\""
                # assertMatch:"node maxstay=-5"
                # assertNoMatch:"node maxstay=0"
                # assertMatch:"node maxstay=180"
                # assertMatch:"node maxstay=66minutes"
                # assertNoMatch:"node maxstay=load-unload"
                # assertNoMatch:"node maxstay=no"
                # assertMatch:"node maxstay=something"
                # assertNoMatch:"node maxstay=unlimited"
                err.append({'class': 9006028, 'subclass': 1976092293, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours')})

        # node[natural=tree][circumference][siunit_length(tag(circumference))>45]
        if ('circumference' in keys and 'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'tree')) and (mapcss._tag_capture(capture_tags, 1, tags, 'circumference')) and (mapcss.siunit_length(mapcss.tag(tags, 'circumference')) > 45))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unusually large value of {0} in meters, possibly centimeter units are meant?","{0.key}")
                # assertNoMatch:"node natural=tree circumference=\"100 cm\""
                # assertNoMatch:"node natural=tree circumference=18.4"
                # assertMatch:"node natural=tree circumference=200"
                # assertNoMatch:"node natural=tree circumference=43"
                # assertMatch:"node natural=tree circumference=82.4"
                err.append({'class': 9006033, 'subclass': 556959007, 'text': mapcss.tr('Unusually large value of {0} in meters, possibly centimeter units are meant?', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set__unit_auto_fix = set_ele_meter_remove_autofix = set_ele_separator_autofix = set_imprecise_gauge = set_maxstay_autofix = set_negative_value = set_unusual_gauge = set_zero_roof_height_flat = False

        # *[/^[0-9]+$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("numerical key")
                # assertMatch:"way 123=foo"
                # assertNoMatch:"way ref.1=foo"
                err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr('numerical key')})

        # *[layer=~/^\+\d/]
        if ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_288e587a), mapcss._tag_capture(capture_tags, 0, tags, 'layer'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value with + sign","{0.key}")
                # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
                err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr('{0} value with + sign', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('layer=', mapcss.replace(mapcss.tag(tags, 'layer'), '+', ''))).split('=', 1)])
                }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'layer')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0b0f0f56, '^0$|^(-|\\+)?[1-5]$'), mapcss._tag_capture(capture_tags, 1, tags, 'layer'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be an integer value between -5 and 5","{0.key}")
                err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr('{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[building:levels^="-"]
        if ('building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'building:levels'), mapcss._value_capture(capture_tags, 0, '-'))))
                except mapcss.RuleAbort: pass
            if match:
                # set negative_value
                # throwError:tr("negative {0} value","{0.key}")
                set_negative_value = True
                err.append({'class': 9006023, 'subclass': 29188290, 'text': mapcss.tr('negative {0} value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]!.negative_value
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if ('building:levels' in keys) or ('level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_negative_value) and (mapcss._tag_capture(capture_tags, 0, tags, 'building:levels')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2a784076, '^(([0-9]|[1-9][0-9]*)(\\.5)?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'building:levels'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7f19b94b, '^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\\.5)?)|-0\\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\\.5)?)|-0\\.5))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
                err.append({'class': 9006004, 'subclass': 1292315112, 'text': mapcss.tr('{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[roof:height][roof:height=~/^0*(\.0*)?( (m|ft))?$/][roof:shape=flat]
        if ('roof:height' in keys and 'roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3c02ab12), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'roof:shape') == mapcss._value_capture(capture_tags, 2, 'flat')))
                except mapcss.RuleAbort: pass
            if match:
                # set zero_roof_height_flat
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{2.tag}")
                # fixRemove:"{0.key}"
                set_zero_roof_height_flat = True
                err.append({'class': 9006025, 'subclass': 1379670484, 'text': mapcss.tr('{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[height][height=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[roof:height][roof:height=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]!.zero_roof_height_flat
        # *[width][width=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxwidth][maxwidth=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[min_height][min_height=~/^(?i)-?[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxheight][maxheight=~/^(?i)[1-9][0-9]*([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxlength][maxlength=~/^(?i)[1-9][0-9]*([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_12c23878), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_270eb4ce), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_270eb4ce), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use abbreviation for unit and space between value and unit","{0.key}")
                # fixAdd:concat("{0.key}","=",get(regexp_match("([0-9.,]+) *.+","{0.value}"),1)," m")
                set__unit_auto_fix = True
                err.append({'class': 9006024, 'subclass': 1245344673, 'text': mapcss.tr('unusual value of {0}: use abbreviation for unit and space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.get(mapcss.regexp_match(self.re_6ae26377, mapcss._tag_uncapture(capture_tags, '{0.value}')), 1), ' m')).split('=', 1)])
                }})

        # *[height][height=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[maxheight][maxheight=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[roof:height][roof:height=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]!.zero_roof_height_flat
        # *[maxlength][maxlength=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[width][width=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[maxwidth][maxwidth=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use '' for foot and \" for inches, no spaces","{0.key}")
                # fixAdd:concat("{0.key}","=",get(regexp_match("([0-9.,]+) *.+","{0.value}"),1),"'")
                set__unit_auto_fix = True
                err.append({'class': 9006031, 'subclass': 1118826626, 'text': mapcss.tr('unusual value of {0}: use \'\' for foot and " for inches, no spaces', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.get(mapcss.regexp_match(self.re_6ae26377, mapcss._tag_uncapture(capture_tags, '{0.value}')), 1), '\'')).split('=', 1)])
                }})

        # *[height][height=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxheight][maxheight=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[roof:height][roof:height=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxlength][maxlength=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[width][width=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxwidth][maxwidth=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[min_height][min_height=~/^-?[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxaxleload][maxaxleload=~/^[0-9]+,[0-9][0-9]?( (t|kg|st|lbs))?$/]
        # *[maxweight][maxweight=~/^[0-9]+,[0-9][0-9]?( (t|kg|st|lbs))?$/]
        # *[distance][distance=~/^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$/]
        if ('distance' in keys) or ('height' in keys) or ('maxaxleload' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxweight' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_21cf6a81), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxaxleload')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_09e9525d), mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxweight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_09e9525d), mapcss._tag_capture(capture_tags, 1, tags, 'maxweight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_55d147d6), mapcss._tag_capture(capture_tags, 1, tags, 'distance'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("{0.key}","=",replace(tag("{0.key}"),",","."))
                set__unit_auto_fix = True
                err.append({'class': 9006017, 'subclass': 1619669445, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.replace(mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}')), ',', '.'))).split('=', 1)])
                }})

        # *[height][height!~/^(([0-9]+(\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!._unit_auto_fix
        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!._unit_auto_fix
        # *[min_height][min_height!~/^(-?([0-9]+(\.[0-9]+)?( m)?)|(-?[1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!._unit_auto_fix
        # *[roof:height][roof:height!~/^(([0-9]+(\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!.zero_roof_height_flat!._unit_auto_fix
        # *[maxlength][maxlength!~/^(([1-9][0-9]*(\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!._unit_auto_fix
        # *[width][width!~/^(([0-9]+(\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]!._unit_auto_fix
        # *[maxwidth][maxwidth!~/^(([0-9]+(\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]!._unit_auto_fix
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_76fe90df, '^(([0-9]+(\\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_40277cab, '^(([1-9][0-9]*(\\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\\.[0-9]*)?\\")?)|none|default|below_default)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_470ea515, '^(-?([0-9]+(\\.[0-9]+)?( m)?)|(-?[1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_76fe90df, '^(([0-9]+(\\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_40277cab, '^(([1-9][0-9]*(\\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\\.[0-9]*)?\\")?)|none|default|below_default)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4a678586, '^(([0-9]+(\\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4a678586, '^(([0-9]+(\\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006032, 'subclass': 516585238, 'text': mapcss.tr('unusual value of {0}: meters is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[maxaxleload][maxaxleload!~/^([0-9]+(\.[0-9]+)?( (t|kg|st|lbs))?)$/]
        # *[maxweight][maxweight!~/^([0-9]+(\.[0-9]+)?( (t|kg|st|lbs))?)$/]
        if ('maxaxleload' in keys) or ('maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxaxleload')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2b4f97f5, '^([0-9]+(\\.[0-9]+)?( (t|kg|st|lbs))?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxweight')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2b4f97f5, '^([0-9]+(\\.[0-9]+)?( (t|kg|st|lbs))?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxweight'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}",tr("tonne"))
                err.append({'class': 9006026, 'subclass': 326659919, 'text': mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('tonne'))})

        # way[maxspeed][maxspeed!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        # way[maxspeed:forward][maxspeed:forward!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        # way[maxspeed:backward][maxspeed:backward!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        if ('maxspeed' in keys) or ('maxspeed:backward' in keys) or ('maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0ae2edfd, '^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:forward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0ae2edfd, '^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:forward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:backward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0ae2edfd, '^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}",tr("km/h"))
                # assertMatch:"way maxspeed=-50"
                # assertMatch:"way maxspeed=0"
                # assertNoMatch:"way maxspeed=30 mph"
                # assertNoMatch:"way maxspeed=50"
                # assertNoMatch:"way maxspeed=DE:motorway"
                # assertNoMatch:"way maxspeed=RO:urban"
                # assertNoMatch:"way maxspeed=RU:living_street"
                # assertNoMatch:"way maxspeed=RU:rural"
                # assertNoMatch:"way maxspeed=none"
                # assertNoMatch:"way maxspeed=signals"
                # assertMatch:"way maxspeed=something"
                # assertNoMatch:"way maxspeed=variable"
                err.append({'class': 9006026, 'subclass': 683878293, 'text': mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('km/h'))})

        # *[distance][distance!~/^(([0-9]+(\.[0-9]+)?( (m|km|mi|nmi))?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]
        if ('distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_41726192, '^(([0-9]+(\\.[0-9]+)?( (m|km|mi|nmi))?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'distance'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}",tr("kilometers"))
                # assertMatch:"way distance=-5"
                # assertNoMatch:"way distance=2"
                # assertNoMatch:"way distance=2.5"
                # assertMatch:"way distance=5."
                # assertNoMatch:"way distance=7 mi"
                # assertMatch:"way distance=something"
                err.append({'class': 9006026, 'subclass': 1210743405, 'text': mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('kilometers'))})

        # way[voltage][voltage=~/(.*[A-Za-z].*)|.*,.*|.*( ).*/]
        # way[voltage:primary][voltage:primary=~/(.*[A-Za-z].*)|.*,.*|.*( ).*/]
        # way[voltage:secondary][voltage:secondary=~/(.*[A-Za-z].*)|.*,.*|.*( ).*/]
        # way[voltage:tertiary][voltage:tertiary=~/(.*[A-Za-z].*)|.*,.*|.*( ).*/]
        if ('voltage' in keys) or ('voltage:primary' in keys) or ('voltage:secondary' in keys) or ('voltage:tertiary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_43c55ce5), mapcss._tag_capture(capture_tags, 1, tags, 'voltage'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:primary')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_43c55ce5), mapcss._tag_capture(capture_tags, 1, tags, 'voltage:primary'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:secondary')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_43c55ce5), mapcss._tag_capture(capture_tags, 1, tags, 'voltage:secondary'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:tertiary')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_43c55ce5), mapcss._tag_capture(capture_tags, 1, tags, 'voltage:tertiary'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("voltage should be in volts with no units/delimiter/spaces")
                # assertNoMatch:"way voltage=15000"
                # assertMatch:"way voltage=medium"
                err.append({'class': 9006013, 'subclass': 44019535, 'text': mapcss.tr('voltage should be in volts with no units/delimiter/spaces')})

        # way[frequency][frequency!~/^(0|[1-9][0-9]*(\.[0-9]+)?)( (kHz|MHz|GHz|THz))?$/]
        if ('frequency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'frequency')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4d44d8e0, '^(0|[1-9][0-9]*(\\.[0-9]+)?)( (kHz|MHz|GHz|THz))?$'), mapcss._tag_capture(capture_tags, 1, tags, 'frequency'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"way frequency=0"
                # assertNoMatch:"way frequency=123.5 MHz"
                # assertNoMatch:"way frequency=16.7"
                # assertNoMatch:"way frequency=50"
                # assertNoMatch:"way frequency=680 kHz"
                # assertMatch:"way frequency=something"
                err.append({'class': 9006010, 'subclass': 582321238, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[gauge][gauge=~/^(broad|standard|narrow)$/]
        if ('gauge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'gauge')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5a9b9c26), mapcss._tag_capture(capture_tags, 1, tags, 'gauge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set imprecise_gauge
                # suggestAlternative:tr("an integer value in millimeters, without unit")
                # throwWarning:tr("imprecise value of {0}","{0.tag}")
                # assertNoMatch:"way gauge=2''10'"
                # assertNoMatch:"way gauge=1000;1435"
                # assertNoMatch:"way gauge=1435"
                # assertMatch:"way gauge=narrow"
                # assertNoMatch:"way gauge=something"
                # assertMatch:"way gauge=standard"
                set_imprecise_gauge = True
                err.append({'class': 9006029, 'subclass': 1280409235, 'text': mapcss.tr('imprecise value of {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[gauge][gauge!~/^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*)$/]!.imprecise_gauge
        if ('gauge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_imprecise_gauge) and (mapcss._tag_capture(capture_tags, 0, tags, 'gauge')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_58d78904, '^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'gauge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set unusual_gauge
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertMatch:"way gauge=2''10'"
                # assertNoMatch:"way gauge=1000;1435"
                # assertNoMatch:"way gauge=1435"
                # assertNoMatch:"way gauge=narrow"
                # assertMatch:"way gauge=something"
                # assertNoMatch:"way gauge=standard"
                set_unusual_gauge = True
                err.append({'class': 9006010, 'subclass': 2055848679, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[/railway$/=~/^narrow_gauge$/][gauge][gauge!~/^((14(?:3[0-4]|[4-9])|(?:14[0-2]|(?:1[0-3]|9)[0-9])[0-9]?|143|(?:[2-7][0-9]|1[5-9])[0-9]|8(?:[0-8][0-9]|9[0-9]?));?)+$/]!.imprecise_gauge!.unusual_gauge
        if ('gauge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_imprecise_gauge) and (not set_unusual_gauge) and (mapcss.regexp_test(self.re_70dc3282, mapcss._match_regex(tags, self.re_7e626945))) and (mapcss._tag_capture(capture_tags, 1, tags, 'gauge')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_33ecb9da, '^((14(?:3[0-4]|[4-9])|(?:14[0-2]|(?:1[0-3]|9)[0-9])[0-9]?|143|(?:[2-7][0-9]|1[5-9])[0-9]|8(?:[0-8][0-9]|9[0-9]?));?)+$'), mapcss._tag_capture(capture_tags, 2, tags, 'gauge'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("unusual {0} value on narrow gauge railway","{1.key}")
                # assertNoMatch:"way railway=narrow_gauge gauge=2''10'"
                # assertNoMatch:"way railway=narrow_gauge gauge=1434"
                # assertMatch:"way railway=narrow_gauge gauge=1435"
                # assertMatch:"way railway=narrow_gauge gauge=1435;1500"
                # assertMatch:"way railway=narrow_gauge gauge=60;600"
                # assertMatch:"way railway=narrow_gauge gauge=88"
                # assertNoMatch:"way railway=narrow_gauge gauge=89"
                # assertNoMatch:"way railway=narrow_gauge gauge=narrow"
                # assertNoMatch:"way railway=narrow_gauge gauge=something"
                err.append({'class': 9006030, 'subclass': 2028551999, 'text': mapcss.tr('unusual {0} value on narrow gauge railway', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[incline][incline!~/^(up|down|-?([0-9]+?(\.[1-9]%)?|100)[%°]?)$/]
        if ('incline' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'incline')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_45e73e1b, '^(up|down|-?([0-9]+?(\\.[1-9]%)?|100)[%°]?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'incline'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # suggestAlternative:"down"
                # suggestAlternative:"up"
                # suggestAlternative:"x%"
                # suggestAlternative:"x°"
                # assertNoMatch:"way incline=-5%"
                # assertNoMatch:"way incline=10%"
                # assertNoMatch:"way incline=10°"
                # assertNoMatch:"way incline=down"
                # assertMatch:"way incline=extreme"
                # assertNoMatch:"way incline=up"
                err.append({'class': 9006010, 'subclass': 901779967, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[population][population!~/^[0-9]+$/]
        if ('population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'population')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_066203d3, '^[0-9]+$'), mapcss._tag_capture(capture_tags, 1, tags, 'population'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value","{0.key}")
                err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr('{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[seats][seats!~/^[1-9]([0-9]*)$/][amenity=bench]
        # way[lanes][lanes!~/^[1-9]([0-9]*)$/][highway]
        # way["lanes:backward"]["lanes:backward"!~/^[1-9]([0-9]*)$/][highway]
        # way["lanes:forward"]["lanes:forward"!~/^[1-9]([0-9]*)$/][highway]
        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if ('amenity' in keys and 'screen' in keys) or ('amenity' in keys and 'seats' in keys) or ('highway' in keys and 'lanes' in keys) or ('highway' in keys and 'lanes:backward' in keys) or ('highway' in keys and 'lanes:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seats')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'seats'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'bench')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lanes')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'lanes'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lanes:backward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'lanes:backward'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lanes:forward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'lanes:forward'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'screen')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'screen'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'cinema')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} must be a positive integer number","{0.key}")
                # assertMatch:"way highway=residential lanes:backward=-1"
                # assertMatch:"way highway=residential lanes:forward=-1"
                # assertMatch:"way highway=residential lanes=-1"
                # assertNoMatch:"way highway=residential lanes=1"
                # assertMatch:"way highway=residential lanes=1;2"
                # assertMatch:"way highway=residential lanes=5.5"
                err.append({'class': 9006009, 'subclass': 2089206793, 'text': mapcss.tr('{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if ('admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'admin_level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7f163374, '^(1|2|3|4|5|6|7|8|9|10|11|12)$'), mapcss._tag_capture(capture_tags, 1, tags, 'admin_level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)((-|;)([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if ('direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'direction') < mapcss._value_capture(capture_tags, 1, 0)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'direction') >= mapcss._value_capture(capture_tags, 1, 360)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23eb7c0d, '^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)((-|;)([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'direction'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 51356092, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_762a1d1d), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # set ele_meter_remove_autofix
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
                set_ele_meter_remove_autofix = True
                err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr('{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, 'ele'), 'm', '')))).split('=', 1)])
                }})

        # *[ele][ele=~/^[0-9]+,[0-9][0-9]?$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b84c9ab), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # set ele_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("ele=",replace(tag("ele"),",","."))
                set_ele_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 202511106, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.replace(mapcss.tag(tags, 'ele'), ',', '.'))).split('=', 1)])
                }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_meter_remove_autofix!.ele_separator_autofix
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_ele_meter_remove_autofix) and (not set_ele_separator_autofix) and (mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_45b46d60, '^-?[0-9]+(\\.[0-9]+)?$'), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                err.append({'class': 9006011, 'subclass': 1781084832, 'text': mapcss.tr('{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+\.[0-9][0-9][0-9]+$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5a7f47b9), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Unnecessary amount of decimal places")
                # throwWarning:tr("{0}","{0.tag}")
                # fixAdd:concat("ele=",round(tag("ele")*100)/100)
                err.append({'class': 9006021, 'subclass': 185098060, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.round_(mapcss.tag(tags, 'ele')*100)/100)).split('=', 1)])
                }})

        # *[interval][interval!~/^([0-9][0-9]?[0-9]?|[0-9]+[0-9]:[0-5][0-9](:[0-5][0-9])?)$/]
        if ('interval' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'interval')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5f1f731d, '^([0-9][0-9]?[0-9]?|[0-9]+[0-9]:[0-5][0-9](:[0-5][0-9])?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'interval'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"way interval=00:05"
                # assertNoMatch:"way interval=00:05:00"
                # assertMatch:"way interval=00:15:90"
                # assertMatch:"way interval=00:65:00"
                # assertNoMatch:"way interval=03:00:00"
                # assertMatch:"way interval=0:5:0"
                # assertNoMatch:"way interval=20"
                # assertNoMatch:"way interval=5"
                err.append({'class': 9006010, 'subclass': 234727583, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[aeroway=helipad][iata][iata!~/^[A-Z]{3}$/]
        # *[aeroway=aerodrome][iata][iata!~/^[A-Z]{3}$/]
        if ('aeroway' in keys and 'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'iata')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6aa93c30, '^[A-Z]{3}$'), mapcss._tag_capture(capture_tags, 2, tags, 'iata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'iata')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6aa93c30, '^[A-Z]{3}$'), mapcss._tag_capture(capture_tags, 2, tags, 'iata'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                # assertMatch:"way aeroway=aerodrome iata=BE"
                # assertNoMatch:"way aeroway=aerodrome iata=BER"
                # assertMatch:"way aeroway=aerodrome iata=BERL"
                # assertMatch:"way aeroway=aerodrome iata=ber"
                err.append({'class': 9006022, 'subclass': 206938530, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[aeroway=helipad][icao][icao!~/^[A-Z]{4}$/]
        # *[aeroway=aerodrome][icao][icao!~/^[A-Z]{4}$/]
        if ('aeroway' in keys and 'icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7afc6883, '^[A-Z]{4}$'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7afc6883, '^[A-Z]{4}$'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                # assertMatch:"way aeroway=aerodrome icao=EDD"
                # assertNoMatch:"way aeroway=aerodrome icao=EDDB"
                # assertMatch:"way aeroway=aerodrome icao=EDDBA"
                # assertMatch:"way aeroway=aerodrome icao=eddb"
                err.append({'class': 9006022, 'subclass': 311618853, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[aeroway=helipad][icao][icao!~/^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)/]
        # *[aeroway=aerodrome][icao][icao!~/^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)/]
        if ('aeroway' in keys and 'icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7b1365b7, '^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7b1365b7, '^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                # assertNoMatch:"way aeroway=aerodrome icao=EDDB"
                # assertMatch:"way aeroway=aerodrome icao=EQQQ"
                err.append({'class': 9006022, 'subclass': 345477776, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[isced:level][isced:level!~/^(0|1|2|3|4|5|6|7|8)((;|-)(1|2|3|4|5|6|7|8))*$/]
        if ('isced:level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'isced:level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0f74b227, '^(0|1|2|3|4|5|6|7|8)((;|-)(1|2|3|4|5|6|7|8))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'isced:level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1091907371, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[maxstay=0]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # assertMatch:"way maxstay=0"
                # assertNoMatch:"way maxstay=no"
                err.append({'class': 9006027, 'subclass': 1756130010, 'text': mapcss.tr('Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? min)$/][maxstay!="1 min"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b78ea82), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 min', '1 min')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"min","minutes"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 606655085, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'min', 'minutes'))).split('=', 1)])
                }})

        # *[maxstay="1h"]
        # *[maxstay="1 h"]
        # *[maxstay="1 hr"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1h')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1 h')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1 hr')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:"maxstay=1 hour"
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 872535915, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxstay','1 hour']])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? h)$/][maxstay!="1 h"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19ef4172), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 h', '1 h')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"h","hours"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 59629984, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'h', 'hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? hr)$/][maxstay!="1 hr"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_330da7b0), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 hr', '1 hr')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"hr","hours"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 814970301, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'hr', 'hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)?h)$/][maxstay!="1h"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_52f27115), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1h', '1h')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"h"," hours"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 1721471777, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'h', ' hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay!~/^(([1-9][0-9]*(\.[0-9]+)?( (minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)))|(no|unlimited|0|load-unload))$/]!.maxstay_autofix
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_maxstay_autofix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_17733c6c, '^(([1-9][0-9]*(\\.[0-9]+)?( (minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)))|(no|unlimited|0|load-unload))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                err.append({'class': 9006028, 'subclass': 1976092293, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set__unit_auto_fix = set_ele_meter_remove_autofix = set_ele_separator_autofix = set_imprecise_gauge = set_maxstay_autofix = set_negative_value = set_unusual_gauge = set_zero_roof_height_flat = False

        # *[/^[0-9]+$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("numerical key")
                err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr('numerical key')})

        # *[layer=~/^\+\d/]
        if ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_288e587a), mapcss._tag_capture(capture_tags, 0, tags, 'layer'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value with + sign","{0.key}")
                # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
                err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr('{0} value with + sign', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('layer=', mapcss.replace(mapcss.tag(tags, 'layer'), '+', ''))).split('=', 1)])
                }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if ('layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'layer')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0b0f0f56, '^0$|^(-|\\+)?[1-5]$'), mapcss._tag_capture(capture_tags, 1, tags, 'layer'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be an integer value between -5 and 5","{0.key}")
                err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr('{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[building:levels^="-"]
        if ('building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'building:levels'), mapcss._value_capture(capture_tags, 0, '-'))))
                except mapcss.RuleAbort: pass
            if match:
                # set negative_value
                # throwError:tr("negative {0} value","{0.key}")
                set_negative_value = True
                err.append({'class': 9006023, 'subclass': 29188290, 'text': mapcss.tr('negative {0} value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]!.negative_value
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if ('building:levels' in keys) or ('level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_negative_value) and (mapcss._tag_capture(capture_tags, 0, tags, 'building:levels')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2a784076, '^(([0-9]|[1-9][0-9]*)(\\.5)?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'building:levels'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7f19b94b, '^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\\.5)?)|-0\\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\\.5)?)|-0\\.5))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
                err.append({'class': 9006004, 'subclass': 1292315112, 'text': mapcss.tr('{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[roof:height][roof:height=~/^0*(\.0*)?( (m|ft))?$/][roof:shape=flat]
        if ('roof:height' in keys and 'roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3c02ab12), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'roof:shape') == mapcss._value_capture(capture_tags, 2, 'flat')))
                except mapcss.RuleAbort: pass
            if match:
                # set zero_roof_height_flat
                # group:tr("unnecessary tag")
                # throwWarning:tr("{0} is unnecessary for {1}","{0.tag}","{2.tag}")
                # fixRemove:"{0.key}"
                set_zero_roof_height_flat = True
                err.append({'class': 9006025, 'subclass': 1379670484, 'text': mapcss.tr('{0} is unnecessary for {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[height][height=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[roof:height][roof:height=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]!.zero_roof_height_flat
        # *[width][width=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxwidth][maxwidth=~/^(?i)[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[min_height][min_height=~/^(?i)-?[0-9]+([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxheight][maxheight=~/^(?i)[1-9][0-9]*([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        # *[maxlength][maxlength=~/^(?i)[1-9][0-9]*([.,][0-9]+)?( *(metres?|meters?)|m| {2,}m)$/]
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5dbcb7bc), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_12c23878), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_270eb4ce), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_270eb4ce), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use abbreviation for unit and space between value and unit","{0.key}")
                # fixAdd:concat("{0.key}","=",get(regexp_match("([0-9.,]+) *.+","{0.value}"),1)," m")
                set__unit_auto_fix = True
                err.append({'class': 9006024, 'subclass': 1245344673, 'text': mapcss.tr('unusual value of {0}: use abbreviation for unit and space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.get(mapcss.regexp_match(self.re_6ae26377, mapcss._tag_uncapture(capture_tags, '{0.value}')), 1), ' m')).split('=', 1)])
                }})

        # *[height][height=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[maxheight][maxheight=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[roof:height][roof:height=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]!.zero_roof_height_flat
        # *[maxlength][maxlength=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[width][width=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        # *[maxwidth][maxwidth=~/^(?i)[0-9]+([.,][0-9]+)?( *(foot|feet|ft)| +\')$/]
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_549d66c4), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use '' for foot and \" for inches, no spaces","{0.key}")
                # fixAdd:concat("{0.key}","=",get(regexp_match("([0-9.,]+) *.+","{0.value}"),1),"'")
                set__unit_auto_fix = True
                err.append({'class': 9006031, 'subclass': 1118826626, 'text': mapcss.tr('unusual value of {0}: use \'\' for foot and " for inches, no spaces', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.get(mapcss.regexp_match(self.re_6ae26377, mapcss._tag_uncapture(capture_tags, '{0.value}')), 1), '\'')).split('=', 1)])
                }})

        # *[height][height=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxheight][maxheight=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[roof:height][roof:height=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxlength][maxlength=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[width][width=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxwidth][maxwidth=~/^[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[min_height][min_height=~/^-?[0-9]+,[0-9][0-9]?( m|\')?$/]
        # *[maxaxleload][maxaxleload=~/^[0-9]+,[0-9][0-9]?( (t|kg|st|lbs))?$/]
        # *[maxweight][maxweight=~/^[0-9]+,[0-9][0-9]?( (t|kg|st|lbs))?$/]
        # *[distance][distance=~/^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$/]
        if ('distance' in keys) or ('height' in keys) or ('maxaxleload' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxweight' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6a0eca39), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_21cf6a81), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxaxleload')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_09e9525d), mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxweight')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_09e9525d), mapcss._tag_capture(capture_tags, 1, tags, 'maxweight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_55d147d6), mapcss._tag_capture(capture_tags, 1, tags, 'distance'))))
                except mapcss.RuleAbort: pass
            if match:
                # set _unit_auto_fix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("{0.key}","=",replace(tag("{0.key}"),",","."))
                set__unit_auto_fix = True
                err.append({'class': 9006017, 'subclass': 1619669445, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=', mapcss.replace(mapcss.tag(tags, mapcss._tag_uncapture(capture_tags, '{0.key}')), ',', '.'))).split('=', 1)])
                }})

        # *[height][height!~/^(([0-9]+(\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!._unit_auto_fix
        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!._unit_auto_fix
        # *[min_height][min_height!~/^(-?([0-9]+(\.[0-9]+)?( m)?)|(-?[1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!._unit_auto_fix
        # *[roof:height][roof:height!~/^(([0-9]+(\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!.zero_roof_height_flat!._unit_auto_fix
        # *[maxlength][maxlength!~/^(([1-9][0-9]*(\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!._unit_auto_fix
        # *[width][width!~/^(([0-9]+(\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]!._unit_auto_fix
        # *[maxwidth][maxwidth!~/^(([0-9]+(\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]!._unit_auto_fix
        if ('height' in keys) or ('maxheight' in keys) or ('maxlength' in keys) or ('maxwidth' in keys) or ('min_height' in keys) or ('roof:height' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_76fe90df, '^(([0-9]+(\\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxheight')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_40277cab, '^(([1-9][0-9]*(\\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\\.[0-9]*)?\\")?)|none|default|below_default)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxheight'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_470ea515, '^(-?([0-9]+(\\.[0-9]+)?( m)?)|(-?[1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'min_height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_zero_roof_height_flat) and (not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'roof:height')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_76fe90df, '^(([0-9]+(\\.[0-9]+)?( m)?)|([1-9][0-9]*\'((10|11|[0-9])((\\.[0-9]+)?)\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'roof:height'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxlength')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_40277cab, '^(([1-9][0-9]*(\\.[0-9]+)?( m)?)|([0-9]+\'(([0-9]|10|11)(\\.[0-9]*)?\\")?)|none|default|below_default)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxlength'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4a678586, '^(([0-9]+(\\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'width'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set__unit_auto_fix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxwidth')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4a678586, '^(([0-9]+(\\.[0-9]+)?( m)?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxwidth'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006032, 'subclass': 516585238, 'text': mapcss.tr('unusual value of {0}: meters is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[maxaxleload][maxaxleload!~/^([0-9]+(\.[0-9]+)?( (t|kg|st|lbs))?)$/]
        # *[maxweight][maxweight!~/^([0-9]+(\.[0-9]+)?( (t|kg|st|lbs))?)$/]
        if ('maxaxleload' in keys) or ('maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxaxleload')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2b4f97f5, '^([0-9]+(\\.[0-9]+)?( (t|kg|st|lbs))?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxweight')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2b4f97f5, '^([0-9]+(\\.[0-9]+)?( (t|kg|st|lbs))?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxweight'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}",tr("tonne"))
                err.append({'class': 9006026, 'subclass': 326659919, 'text': mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('tonne'))})

        # *[distance][distance!~/^(([0-9]+(\.[0-9]+)?( (m|km|mi|nmi))?)|([0-9]+\'([0-9]+(\.[0-9]+)?\")?))$/]
        if ('distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_41726192, '^(([0-9]+(\\.[0-9]+)?( (m|km|mi|nmi))?)|([0-9]+\'([0-9]+(\\.[0-9]+)?\\")?))$'), mapcss._tag_capture(capture_tags, 1, tags, 'distance'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit","{0.key}",tr("kilometers"))
                err.append({'class': 9006026, 'subclass': 1210743405, 'text': mapcss.tr('unusual value of {0}: {1} is default; only positive values; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss.tr('kilometers'))})

        # relation[gauge][gauge=~/^(broad|standard|narrow)$/]
        if ('gauge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'gauge')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5a9b9c26), mapcss._tag_capture(capture_tags, 1, tags, 'gauge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set imprecise_gauge
                # suggestAlternative:tr("an integer value in millimeters, without unit")
                # throwWarning:tr("imprecise value of {0}","{0.tag}")
                set_imprecise_gauge = True
                err.append({'class': 9006029, 'subclass': 1590792813, 'text': mapcss.tr('imprecise value of {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # relation[gauge][gauge!~/^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*)$/]!.imprecise_gauge
        if ('gauge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_imprecise_gauge) and (mapcss._tag_capture(capture_tags, 0, tags, 'gauge')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_58d78904, '^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'gauge'))))
                except mapcss.RuleAbort: pass
            if match:
                # set unusual_gauge
                # throwWarning:tr("unusual value of {0}","{0.key}")
                set_unusual_gauge = True
                err.append({'class': 9006010, 'subclass': 1964213800, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # relation[/railway$/=~/^narrow_gauge$/][gauge][gauge!~/^((14(?:3[0-4]|[4-9])|(?:14[0-2]|(?:1[0-3]|9)[0-9])[0-9]?|143|(?:[2-7][0-9]|1[5-9])[0-9]|8(?:[0-8][0-9]|9[0-9]?));?)+$/]!.imprecise_gauge!.unusual_gauge[type=route]
        if ('gauge' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_imprecise_gauge) and (not set_unusual_gauge) and (mapcss.regexp_test(self.re_70dc3282, mapcss._match_regex(tags, self.re_7e626945))) and (mapcss._tag_capture(capture_tags, 1, tags, 'gauge')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_33ecb9da, '^((14(?:3[0-4]|[4-9])|(?:14[0-2]|(?:1[0-3]|9)[0-9])[0-9]?|143|(?:[2-7][0-9]|1[5-9])[0-9]|8(?:[0-8][0-9]|9[0-9]?));?)+$'), mapcss._tag_capture(capture_tags, 2, tags, 'gauge'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'type') == mapcss._value_capture(capture_tags, 5, 'route')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("unusual {0} value on narrow gauge railway","{1.key}")
                err.append({'class': 9006030, 'subclass': 1005704701, 'text': mapcss.tr('unusual {0} value on narrow gauge railway', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[population][population!~/^[0-9]+$/]
        if ('population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'population')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_066203d3, '^[0-9]+$'), mapcss._tag_capture(capture_tags, 1, tags, 'population'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value","{0.key}")
                err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr('{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if ('amenity' in keys and 'screen' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'screen')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5478d8af, '^[1-9]([0-9]*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'screen'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') == mapcss._value_capture(capture_tags, 2, 'cinema')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} must be a positive integer number","{0.key}")
                err.append({'class': 9006009, 'subclass': 1499065449, 'text': mapcss.tr('{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if ('admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'admin_level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7f163374, '^(1|2|3|4|5|6|7|8|9|10|11|12)$'), mapcss._tag_capture(capture_tags, 1, tags, 'admin_level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)((-|;)([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if ('direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'direction') < mapcss._value_capture(capture_tags, 1, 0)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'direction') >= mapcss._value_capture(capture_tags, 1, 360)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23eb7c0d, '^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)((-|;)([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'direction'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 51356092, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_762a1d1d), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # set ele_meter_remove_autofix
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
                set_ele_meter_remove_autofix = True
                err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr('{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, 'ele'), 'm', '')))).split('=', 1)])
                }})

        # *[ele][ele=~/^[0-9]+,[0-9][0-9]?$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2b84c9ab), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # set ele_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("ele=",replace(tag("ele"),",","."))
                set_ele_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 202511106, 'text': mapcss.tr('unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.replace(mapcss.tag(tags, 'ele'), ',', '.'))).split('=', 1)])
                }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_meter_remove_autofix!.ele_separator_autofix
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_ele_meter_remove_autofix) and (not set_ele_separator_autofix) and (mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_45b46d60, '^-?[0-9]+(\\.[0-9]+)?$'), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                err.append({'class': 9006011, 'subclass': 1781084832, 'text': mapcss.tr('{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+\.[0-9][0-9][0-9]+$/]
        if ('ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ele')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5a7f47b9), mapcss._tag_capture(capture_tags, 1, tags, 'ele'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Unnecessary amount of decimal places")
                # throwWarning:tr("{0}","{0.tag}")
                # fixAdd:concat("ele=",round(tag("ele")*100)/100)
                err.append({'class': 9006021, 'subclass': 185098060, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('ele=', mapcss.round_(mapcss.tag(tags, 'ele')*100)/100)).split('=', 1)])
                }})

        # *[interval][interval!~/^([0-9][0-9]?[0-9]?|[0-9]+[0-9]:[0-5][0-9](:[0-5][0-9])?)$/]
        if ('interval' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'interval')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5f1f731d, '^([0-9][0-9]?[0-9]?|[0-9]+[0-9]:[0-5][0-9](:[0-5][0-9])?)$'), mapcss._tag_capture(capture_tags, 1, tags, 'interval'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"relation interval=120"
                # assertNoMatch:"relation interval=168:00:00"
                err.append({'class': 9006010, 'subclass': 234727583, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[aeroway=helipad][iata][iata!~/^[A-Z]{3}$/]
        # *[aeroway=aerodrome][iata][iata!~/^[A-Z]{3}$/]
        if ('aeroway' in keys and 'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'iata')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6aa93c30, '^[A-Z]{3}$'), mapcss._tag_capture(capture_tags, 2, tags, 'iata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'iata')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6aa93c30, '^[A-Z]{3}$'), mapcss._tag_capture(capture_tags, 2, tags, 'iata'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                err.append({'class': 9006022, 'subclass': 206938530, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[aeroway=helipad][icao][icao!~/^[A-Z]{4}$/]
        # *[aeroway=aerodrome][icao][icao!~/^[A-Z]{4}$/]
        if ('aeroway' in keys and 'icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7afc6883, '^[A-Z]{4}$'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7afc6883, '^[A-Z]{4}$'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                err.append({'class': 9006022, 'subclass': 311618853, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[aeroway=helipad][icao][icao!~/^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)/]
        # *[aeroway=aerodrome][icao][icao!~/^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)/]
        if ('aeroway' in keys and 'icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'helipad')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7b1365b7, '^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'aerodrome')) and (mapcss._tag_capture(capture_tags, 1, tags, 'icao')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7b1365b7, '^(AG|AN|AY|BG|BI|BK|C|DA|DB|DF|DG|DI|DN|DR|DT|DX|EB|ED|EE|EF|EG|EH|EI|EK|EL|EN|EP|ES|ET|EV|EY|FA|FB|FC|FD|FE|FG|FH|FI|FJ|FK|FL|FM|FN|FO|FP|FQ|FS|FT|FV|FW|FX|FY|FZ|GA|GB|GC|GE|GF|GG|GL|GM|GO|GQ|GS|GU|GV|HA|HB|HC|HD|HE|HH|HK|HL|HR|HS|HT|HU|K|LA|LB|LC|LD|LE|LF|LG|LH|LI|LJ|LK|LL|LM|LN|LO|LP|LQ|LR|LS|LT|LU|LV|LW|LX|LY|LZ|MB|MD|MG|MH|MK|MM|MN|MP|MR|MS|MT|MU|MW|MY|MZ|NC|NF|NG|NI|NL|NS|NT|NV|NW|NZ|OA|OB|OE|OI|OJ|OK|OL|OM|OO|OP|OR|OS|OT|OY|PA|PB|PC|PF|PG|PH|PJ|PK|PL|PM|PO|PP|PT|PW|RC|RJ|RK|RO|RP|SA|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SP|SS|SU|SV|SW|SY|TA|TB|TD|TF|TG|TI|TJ|TK|TL|TN|TQ|TR|TT|TU|TV|TX|U|UA|UB|UC|UD|UG|UK|UM|UT|VA|VC|VD|VE|VG|VH|VI|VL|VM|VN|VO|VQ|VR|VT|VV|VY|WA|WB|WI|WM|WP|WQ|WR|WS|Y|Z|ZK|ZM)'), mapcss._tag_capture(capture_tags, 2, tags, 'icao'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Airport tagging")
                # throwWarning:tr("wrong value: {0}","{1.tag}")
                err.append({'class': 9006022, 'subclass': 345477776, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[isced:level][isced:level!~/^(0|1|2|3|4|5|6|7|8)((;|-)(1|2|3|4|5|6|7|8))*$/]
        if ('isced:level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'isced:level')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_0f74b227, '^(0|1|2|3|4|5|6|7|8)((;|-)(1|2|3|4|5|6|7|8))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'isced:level'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1091907371, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[maxstay=0]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                err.append({'class': 9006027, 'subclass': 1756130010, 'text': mapcss.tr('Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? min)$/][maxstay!="1 min"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1b78ea82), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 min', '1 min')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"min","minutes"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 606655085, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'min', 'minutes'))).split('=', 1)])
                }})

        # *[maxstay="1h"]
        # *[maxstay="1 h"]
        # *[maxstay="1 hr"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1h')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1 h')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay') == mapcss._value_capture(capture_tags, 0, '1 hr')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:"maxstay=1 hour"
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 872535915, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxstay','1 hour']])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? h)$/][maxstay!="1 h"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_19ef4172), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 h', '1 h')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"h","hours"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 59629984, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'h', 'hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)? hr)$/][maxstay!="1 hr"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_330da7b0), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1 hr', '1 hr')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"hr","hours"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 814970301, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'hr', 'hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay=~/^([1-9][0-9]*(\.[0-9]+)?h)$/][maxstay!="1h"]
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_52f27115), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxstay') != mapcss._value_const_capture(capture_tags, 2, '1h', '1h')))
                except mapcss.RuleAbort: pass
            if match:
                # set maxstay_autofix
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                # fixAdd:concat("maxstay=",replace(tag("maxstay"),"h"," hours"))
                set_maxstay_autofix = True
                err.append({'class': 9006028, 'subclass': 1721471777, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('maxstay=', mapcss.replace(mapcss.tag(tags, 'maxstay'), 'h', ' hours'))).split('=', 1)])
                }})

        # *[maxstay][maxstay!~/^(([1-9][0-9]*(\.[0-9]+)?( (minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)))|(no|unlimited|0|load-unload))$/]!.maxstay_autofix
        if ('maxstay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_maxstay_autofix) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxstay')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_17733c6c, '^(([1-9][0-9]*(\\.[0-9]+)?( (minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)))|(no|unlimited|0|load-unload))$'), mapcss._tag_capture(capture_tags, 1, tags, 'maxstay'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit","{0.key}","minutes","hours")
                err.append({'class': 9006028, 'subclass': 1976092293, 'text': mapcss.tr('unusual value of {0}: set unit e.g. {1} or {2}; only positive values; point is decimal separator; space between value and unit', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'minutes', 'hours')})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_numeric(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'layer': '+1'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_not_err(n.node(data, {'layer': '+foo'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_not_err(n.node(data, {'layer': '-1'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_not_err(n.node(data, {'layer': '1'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_err(n.node(data, {'layer': '+10'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {'layer': '+5'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {'layer': '-5'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {'layer': '-50'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {'layer': '0'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {'layer': '0.5'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {'layer': '0;1'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {'layer': '2'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {'layer': '6'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {'building:levels': '+1'}), expected={'class': 9006023, 'subclass': 29188290})
        self.check_err(n.node(data, {'building:levels': '-1'}), expected={'class': 9006023, 'subclass': 29188290})
        self.check_err(n.node(data, {'building:levels': '-foo'}), expected={'class': 9006023, 'subclass': 29188290})
        self.check_not_err(n.node(data, {'building:levels': '1'}), expected={'class': 9006023, 'subclass': 29188290})
        self.check_not_err(n.node(data, {'building:levels': 'foo'}), expected={'class': 9006023, 'subclass': 29188290})
        self.check_not_err(n.node(data, {'level': '-1'}), expected={'class': 9006023, 'subclass': 29188290})
        self.check_not_err(n.node(data, {'building:levels': '-1'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'building:levels': '0'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'building:levels': '1.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'building:levels': '1A'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'level': '-0'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '-0.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '-0.5;0'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'level': '-01.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'level': '-03'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '-1'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '-1;-0.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '0'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'level': '01'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '0;-0.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '0;1'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '1'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '1.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '12'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '1;0.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_not_err(n.node(data, {'level': '1;1.5'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'level': '2.3'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'level': 'one'}), expected={'class': 9006004, 'subclass': 1292315112})
        self.check_err(n.node(data, {'roof:height': '0', 'roof:shape': 'flat'}), expected={'class': 9006025, 'subclass': 1379670484})
        self.check_not_err(n.node(data, {'roof:height': '0', 'roof:shape': 'gabled'}), expected={'class': 9006025, 'subclass': 1379670484})
        self.check_err(n.node(data, {'roof:height': '00.00000 ft', 'roof:shape': 'flat'}), expected={'class': 9006025, 'subclass': 1379670484})
        self.check_not_err(n.node(data, {'roof:height': '2 m', 'roof:shape': 'flat'}), expected={'class': 9006025, 'subclass': 1379670484})
        self.check_not_err(n.node(data, {'height': '2 m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'height': '2m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'height': '5  metre'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'height': '5'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'height': '6,78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'height': '6.78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'maxheight': '2 m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxheight': '2m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxheight': '5  metre'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'maxheight': '5'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxheight': '6.78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'maxlength': '2 m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxlength': '2m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxlength': '5  metre'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'maxlength': '5'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxlength': '6.78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'maxwidth': '2 m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxwidth': '2m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxwidth': '5  metre'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'maxwidth': '5'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'maxwidth': '6.78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'min_height': '2 m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'min_height': '2m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'min_height': '5  metre'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'min_height': '5'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'min_height': '6.78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'roof:height': '2 m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'roof:height': '2m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'roof:height': '5  metre'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'roof:height': '5'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'roof:height': '6.78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'width': '2 m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'width': '2m'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'width': '5  metre'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_not_err(n.node(data, {'width': '5'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'width': '6.78 meters'}), expected={'class': 9006024, 'subclass': 1245344673})
        self.check_err(n.node(data, {'height': '2 \''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'height': '2\''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxheight': '2 \''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'maxheight': '2\''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxlength': '2 \''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'maxlength': '2\''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxwidth': '2 \''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'maxwidth': '2\''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'roof:height': '2 \''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'roof:height': '2\''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'width': '2 \''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'width': '2\''}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'height': '5  Feet'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'height': '5'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'height': '6.78 foot'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxheight': '5  Feet'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'maxheight': '5'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxheight': '6.78 foot'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxlength': '5  Feet'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'maxlength': '5'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxlength': '6.78 foot'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxwidth': '5  Feet'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'maxwidth': '5'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'maxwidth': '6.78 foot'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'roof:height': '5  Feet'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'roof:height': '5'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'roof:height': '6.78 foot'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'width': '5  Feet'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_not_err(n.node(data, {'width': '5'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'width': '6.78 foot'}), expected={'class': 9006031, 'subclass': 1118826626})
        self.check_err(n.node(data, {'height': '12,5\''}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxheight': '12,5\''}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxlength': '12,5\''}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'min_height': '12,5\''}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'roof:height': '12,5\''}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'distance': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'distance': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'distance': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'distance': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'distance': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'distance': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'height': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'height': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'height': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'height': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'height': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'height': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxaxleload': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxaxleload': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxaxleload': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxaxleload': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxaxleload': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxaxleload': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxheight': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxheight': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxheight': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxheight': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxheight': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxheight': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxlength': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxlength': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxlength': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxlength': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxlength': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxlength': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxweight': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxweight': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxweight': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxweight': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxweight': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxweight': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxwidth': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxwidth': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxwidth': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxwidth': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'maxwidth': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'maxwidth': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'min_height': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'min_height': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'min_height': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'min_height': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'min_height': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'min_height': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'roof:height': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'roof:height': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'roof:height': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'roof:height': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'roof:height': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'roof:height': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'width': '12,00'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'width': '12,000'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'width': '3,50,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'width': '3.5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'width': '4'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_err(n.node(data, {'width': '5,5'}), expected={'class': 9006017, 'subclass': 1619669445})
        self.check_not_err(n.node(data, {'height': '22\''}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'maxwidth': '7\''}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'width': '10\''}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'height': '12. m'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'height': '2 m'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'height': '2.22 m'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'height': '3'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'height': '5  m'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'height': '6.78 m'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'height': '7.8'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'height': 'medium'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'maxheight': '2. m'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'maxheight': '-5'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'maxlength': '0'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'maxlength': '10\'13"'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'min_height': '12. m'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'min_height': '-5'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_err(n.node(data, {'width': '10\'2."'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'width': '10\'5"'}), expected={'class': 9006032, 'subclass': 516585238})
        self.check_not_err(n.node(data, {'maxaxleload': '2'}), expected={'class': 9006026, 'subclass': 326659919})
        self.check_not_err(n.node(data, {'maxaxleload': '2.5'}), expected={'class': 9006026, 'subclass': 326659919})
        self.check_not_err(n.node(data, {'maxaxleload': '7 kg'}), expected={'class': 9006026, 'subclass': 326659919})
        self.check_err(n.node(data, {'maxaxleload': 'something'}), expected={'class': 9006026, 'subclass': 326659919})
        self.check_err(n.node(data, {'maxweight': '-5'}), expected={'class': 9006026, 'subclass': 326659919})
        self.check_not_err(n.node(data, {'amenity': 'cinema', 'screen': '8'}), expected={'class': 9006009, 'subclass': 2104305963})
        self.check_err(n.node(data, {'amenity': 'cinema', 'screen': 'led'}), expected={'class': 9006009, 'subclass': 2104305963})
        self.check_err(n.node(data, {'admin_level': '-1'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_err(n.node(data, {'admin_level': '0'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_err(n.node(data, {'admin_level': '13'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_not_err(n.node(data, {'admin_level': '5'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_err(n.node(data, {'direction': '-10'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': '0'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': '0-360'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': '1360'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': '360'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': '45'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': '45-100;190-250;300'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': '45-100;190-250;300-'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': '45-100;190-250;300-360'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': '90;270'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': 'C'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'N'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'NE-S'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'NNE'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': 'NNNE'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'anti-clockwise'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'anticlockwise'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'down'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'forward'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': 'north-down'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': 'north-east'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': 'north-south'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'direction': 'rome'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'up'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_not_err(n.node(data, {'direction': 'west'}), expected={'class': 9006010, 'subclass': 51356092})
        self.check_err(n.node(data, {'ele': '-12.1 m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {'ele': '12 m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_not_err(n.node(data, {'ele': '12'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {'ele': '12.1m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_not_err(n.node(data, {'ele': '12km'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {'ele': '12m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_not_err(n.node(data, {'ele': 'high'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {'ele': '12,00'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {'ele': '3,50,5'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {'ele': '3.5'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {'ele': '4'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_err(n.node(data, {'ele': '5,5'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {'ele': '8,848'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {'ele': '-12.1 m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {'ele': '12 m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {'ele': '12'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {'ele': '12.1m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_err(n.node(data, {'ele': '12km'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {'ele': '12m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_err(n.node(data, {'ele': 'high'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_err(n.node(data, {'ele': '-12.6789'}), expected={'class': 9006021, 'subclass': 185098060})
        self.check_not_err(n.node(data, {'ele': '1.12'}), expected={'class': 9006021, 'subclass': 185098060})
        self.check_not_err(n.node(data, {'ele': '12'}), expected={'class': 9006021, 'subclass': 185098060})
        self.check_not_err(n.node(data, {'ele': '12.123 m'}), expected={'class': 9006021, 'subclass': 185098060})
        self.check_err(n.node(data, {'ele': '12.123'}), expected={'class': 9006021, 'subclass': 185098060})
        self.check_err(n.node(data, {'ele': '12.1234'}), expected={'class': 9006021, 'subclass': 185098060})
        self.check_not_err(n.node(data, {'ele': 'high'}), expected={'class': 9006021, 'subclass': 185098060})
        self.check_not_err(n.node(data, {'isced:level': '0'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_err(n.node(data, {'isced:level': '0,1,2,3'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_not_err(n.node(data, {'isced:level': '0-3'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_not_err(n.node(data, {'isced:level': '0;1;2;3'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_err(n.node(data, {'isced:level': '10'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_not_err(n.node(data, {'isced:level': '5'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_err(n.node(data, {'isced:level': '9'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_err(n.node(data, {'isced:level': 'secondary'}), expected={'class': 9006010, 'subclass': 1091907371})
        self.check_err(n.node(data, {'maxstay': '0'}), expected={'class': 9006027, 'subclass': 1756130010})
        self.check_not_err(n.node(data, {'maxstay': '2'}), expected={'class': 9006027, 'subclass': 1756130010})
        self.check_not_err(n.node(data, {'maxstay': '02 minutes'}), expected={'class': 9006028, 'subclass': 606655085})
        self.check_not_err(n.node(data, {'maxstay': '1 min'}), expected={'class': 9006028, 'subclass': 606655085})
        self.check_err(n.node(data, {'maxstay': '15 min'}), expected={'class': 9006028, 'subclass': 606655085})
        self.check_not_err(n.node(data, {'maxstay': '2 minutes'}), expected={'class': 9006028, 'subclass': 606655085})
        self.check_err(n.node(data, {'maxstay': '5 min'}), expected={'class': 9006028, 'subclass': 606655085})
        self.check_err(n.node(data, {'maxstay': '1 h'}), expected={'class': 9006028, 'subclass': 872535915})
        self.check_err(n.node(data, {'maxstay': '1 hr'}), expected={'class': 9006028, 'subclass': 872535915})
        self.check_err(n.node(data, {'maxstay': '1h'}), expected={'class': 9006028, 'subclass': 872535915})
        self.check_not_err(n.node(data, {'maxstay': '02 hours'}), expected={'class': 9006028, 'subclass': 59629984})
        self.check_not_err(n.node(data, {'maxstay': '1 h'}), expected={'class': 9006028, 'subclass': 59629984})
        self.check_err(n.node(data, {'maxstay': '15 h'}), expected={'class': 9006028, 'subclass': 59629984})
        self.check_not_err(n.node(data, {'maxstay': '2 hours'}), expected={'class': 9006028, 'subclass': 59629984})
        self.check_err(n.node(data, {'maxstay': '5 h'}), expected={'class': 9006028, 'subclass': 59629984})
        self.check_not_err(n.node(data, {'maxstay': '02 hours'}), expected={'class': 9006028, 'subclass': 814970301})
        self.check_not_err(n.node(data, {'maxstay': '1 hr'}), expected={'class': 9006028, 'subclass': 814970301})
        self.check_err(n.node(data, {'maxstay': '15 hr'}), expected={'class': 9006028, 'subclass': 814970301})
        self.check_not_err(n.node(data, {'maxstay': '2 hours'}), expected={'class': 9006028, 'subclass': 814970301})
        self.check_err(n.node(data, {'maxstay': '5 hr'}), expected={'class': 9006028, 'subclass': 814970301})
        self.check_not_err(n.node(data, {'maxstay': '2 h'}), expected={'class': 9006028, 'subclass': 1721471777})
        self.check_not_err(n.node(data, {'maxstay': '2 hr'}), expected={'class': 9006028, 'subclass': 1721471777})
        self.check_not_err(n.node(data, {'maxstay': '02hours'}), expected={'class': 9006028, 'subclass': 1721471777})
        self.check_err(n.node(data, {'maxstay': '15h'}), expected={'class': 9006028, 'subclass': 1721471777})
        self.check_not_err(n.node(data, {'maxstay': '1h'}), expected={'class': 9006028, 'subclass': 1721471777})
        self.check_not_err(n.node(data, {'maxstay': '2hours'}), expected={'class': 9006028, 'subclass': 1721471777})
        self.check_err(n.node(data, {'maxstay': '5h'}), expected={'class': 9006028, 'subclass': 1721471777})
        self.check_err(n.node(data, {'maxstay': '0 minutes'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_err(n.node(data, {'maxstay': '1. hours'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': '2.5 hours'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': '66 minutes'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': '7 h'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': '7 hr'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_err(n.node(data, {'maxstay': '-5'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': '0'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_err(n.node(data, {'maxstay': '180'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_err(n.node(data, {'maxstay': '66minutes'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': 'load-unload'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': 'no'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_err(n.node(data, {'maxstay': 'something'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'maxstay': 'unlimited'}), expected={'class': 9006028, 'subclass': 1976092293})
        self.check_not_err(n.node(data, {'circumference': '100 cm', 'natural': 'tree'}), expected={'class': 9006033, 'subclass': 556959007})
        self.check_not_err(n.node(data, {'circumference': '18.4', 'natural': 'tree'}), expected={'class': 9006033, 'subclass': 556959007})
        self.check_err(n.node(data, {'circumference': '200', 'natural': 'tree'}), expected={'class': 9006033, 'subclass': 556959007})
        self.check_not_err(n.node(data, {'circumference': '43', 'natural': 'tree'}), expected={'class': 9006033, 'subclass': 556959007})
        self.check_err(n.node(data, {'circumference': '82.4', 'natural': 'tree'}), expected={'class': 9006033, 'subclass': 556959007})
        self.check_err(n.way(data, {'123': 'foo'}, [0]), expected={'class': 9006001, 'subclass': 750700308})
        self.check_not_err(n.way(data, {'ref.1': 'foo'}, [0]), expected={'class': 9006001, 'subclass': 750700308})
        self.check_err(n.way(data, {'maxspeed': '-50'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_err(n.way(data, {'maxspeed': '0'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': '30 mph'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': '50'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': 'DE:motorway'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': 'RO:urban'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': 'RU:living_street'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': 'RU:rural'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': 'none'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': 'signals'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_err(n.way(data, {'maxspeed': 'something'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_not_err(n.way(data, {'maxspeed': 'variable'}, [0]), expected={'class': 9006026, 'subclass': 683878293})
        self.check_err(n.way(data, {'distance': '-5'}, [0]), expected={'class': 9006026, 'subclass': 1210743405})
        self.check_not_err(n.way(data, {'distance': '2'}, [0]), expected={'class': 9006026, 'subclass': 1210743405})
        self.check_not_err(n.way(data, {'distance': '2.5'}, [0]), expected={'class': 9006026, 'subclass': 1210743405})
        self.check_err(n.way(data, {'distance': '5.'}, [0]), expected={'class': 9006026, 'subclass': 1210743405})
        self.check_not_err(n.way(data, {'distance': '7 mi'}, [0]), expected={'class': 9006026, 'subclass': 1210743405})
        self.check_err(n.way(data, {'distance': 'something'}, [0]), expected={'class': 9006026, 'subclass': 1210743405})
        self.check_not_err(n.way(data, {'voltage': '15000'}, [0]), expected={'class': 9006013, 'subclass': 44019535})
        self.check_err(n.way(data, {'voltage': 'medium'}, [0]), expected={'class': 9006013, 'subclass': 44019535})
        self.check_not_err(n.way(data, {'frequency': '0'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {'frequency': '123.5 MHz'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {'frequency': '16.7'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {'frequency': '50'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {'frequency': '680 kHz'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_err(n.way(data, {'frequency': 'something'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {'gauge': '2\'\'10\''}, [0]), expected={'class': 9006029, 'subclass': 1280409235})
        self.check_not_err(n.way(data, {'gauge': '1000;1435'}, [0]), expected={'class': 9006029, 'subclass': 1280409235})
        self.check_not_err(n.way(data, {'gauge': '1435'}, [0]), expected={'class': 9006029, 'subclass': 1280409235})
        self.check_err(n.way(data, {'gauge': 'narrow'}, [0]), expected={'class': 9006029, 'subclass': 1280409235})
        self.check_not_err(n.way(data, {'gauge': 'something'}, [0]), expected={'class': 9006029, 'subclass': 1280409235})
        self.check_err(n.way(data, {'gauge': 'standard'}, [0]), expected={'class': 9006029, 'subclass': 1280409235})
        self.check_err(n.way(data, {'gauge': '2\'\'10\''}, [0]), expected={'class': 9006010, 'subclass': 2055848679})
        self.check_not_err(n.way(data, {'gauge': '1000;1435'}, [0]), expected={'class': 9006010, 'subclass': 2055848679})
        self.check_not_err(n.way(data, {'gauge': '1435'}, [0]), expected={'class': 9006010, 'subclass': 2055848679})
        self.check_not_err(n.way(data, {'gauge': 'narrow'}, [0]), expected={'class': 9006010, 'subclass': 2055848679})
        self.check_err(n.way(data, {'gauge': 'something'}, [0]), expected={'class': 9006010, 'subclass': 2055848679})
        self.check_not_err(n.way(data, {'gauge': 'standard'}, [0]), expected={'class': 9006010, 'subclass': 2055848679})
        self.check_not_err(n.way(data, {'gauge': '2\'\'10\'', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_not_err(n.way(data, {'gauge': '1434', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_err(n.way(data, {'gauge': '1435', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_err(n.way(data, {'gauge': '1435;1500', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_err(n.way(data, {'gauge': '60;600', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_err(n.way(data, {'gauge': '88', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_not_err(n.way(data, {'gauge': '89', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_not_err(n.way(data, {'gauge': 'narrow', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_not_err(n.way(data, {'gauge': 'something', 'railway': 'narrow_gauge'}, [0]), expected={'class': 9006030, 'subclass': 2028551999})
        self.check_not_err(n.way(data, {'incline': '-5%'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {'incline': '10%'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {'incline': '10°'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {'incline': 'down'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_err(n.way(data, {'incline': 'extreme'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {'incline': 'up'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_err(n.way(data, {'highway': 'residential', 'lanes:backward': '-1'}, [0]), expected={'class': 9006009, 'subclass': 2089206793})
        self.check_err(n.way(data, {'highway': 'residential', 'lanes:forward': '-1'}, [0]), expected={'class': 9006009, 'subclass': 2089206793})
        self.check_err(n.way(data, {'highway': 'residential', 'lanes': '-1'}, [0]), expected={'class': 9006009, 'subclass': 2089206793})
        self.check_not_err(n.way(data, {'highway': 'residential', 'lanes': '1'}, [0]), expected={'class': 9006009, 'subclass': 2089206793})
        self.check_err(n.way(data, {'highway': 'residential', 'lanes': '1;2'}, [0]), expected={'class': 9006009, 'subclass': 2089206793})
        self.check_err(n.way(data, {'highway': 'residential', 'lanes': '5.5'}, [0]), expected={'class': 9006009, 'subclass': 2089206793})
        self.check_not_err(n.way(data, {'interval': '00:05'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_not_err(n.way(data, {'interval': '00:05:00'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_err(n.way(data, {'interval': '00:15:90'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_err(n.way(data, {'interval': '00:65:00'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_not_err(n.way(data, {'interval': '03:00:00'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_err(n.way(data, {'interval': '0:5:0'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_not_err(n.way(data, {'interval': '20'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_not_err(n.way(data, {'interval': '5'}, [0]), expected={'class': 9006010, 'subclass': 234727583})
        self.check_err(n.way(data, {'aeroway': 'aerodrome', 'iata': 'BE'}, [0]), expected={'class': 9006022, 'subclass': 206938530})
        self.check_not_err(n.way(data, {'aeroway': 'aerodrome', 'iata': 'BER'}, [0]), expected={'class': 9006022, 'subclass': 206938530})
        self.check_err(n.way(data, {'aeroway': 'aerodrome', 'iata': 'BERL'}, [0]), expected={'class': 9006022, 'subclass': 206938530})
        self.check_err(n.way(data, {'aeroway': 'aerodrome', 'iata': 'ber'}, [0]), expected={'class': 9006022, 'subclass': 206938530})
        self.check_err(n.way(data, {'aeroway': 'aerodrome', 'icao': 'EDD'}, [0]), expected={'class': 9006022, 'subclass': 311618853})
        self.check_not_err(n.way(data, {'aeroway': 'aerodrome', 'icao': 'EDDB'}, [0]), expected={'class': 9006022, 'subclass': 311618853})
        self.check_err(n.way(data, {'aeroway': 'aerodrome', 'icao': 'EDDBA'}, [0]), expected={'class': 9006022, 'subclass': 311618853})
        self.check_err(n.way(data, {'aeroway': 'aerodrome', 'icao': 'eddb'}, [0]), expected={'class': 9006022, 'subclass': 311618853})
        self.check_not_err(n.way(data, {'aeroway': 'aerodrome', 'icao': 'EDDB'}, [0]), expected={'class': 9006022, 'subclass': 345477776})
        self.check_err(n.way(data, {'aeroway': 'aerodrome', 'icao': 'EQQQ'}, [0]), expected={'class': 9006022, 'subclass': 345477776})
        self.check_err(n.way(data, {'maxstay': '0'}, [0]), expected={'class': 9006027, 'subclass': 1756130010})
        self.check_not_err(n.way(data, {'maxstay': 'no'}, [0]), expected={'class': 9006027, 'subclass': 1756130010})
        self.check_not_err(n.relation(data, {'interval': '120'}, []), expected={'class': 9006010, 'subclass': 234727583})
        self.check_not_err(n.relation(data, {'interval': '168:00:00'}, []), expected={'class': 9006010, 'subclass': 234727583})
