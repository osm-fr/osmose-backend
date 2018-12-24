#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_numeric(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9006001] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'numerical key')}
        self.errors[9006002] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'{0} value with + sign', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006003] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006004] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006008] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006009] = {'item': 9006, 'level': 2, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006010] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006011] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006013] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'voltage should be in volts with no units/delimiter/spaces')}
        self.errors[9006017] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006018] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006019] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'unusual value of {0}: tonne is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9006020] = {'item': 9006, 'level': 3, 'tag': ["tag", "value"], 'desc': mapcss.tr(u'unusual value of {0}: kilometers is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}

        self.re_035d45f0 = re.compile(ur'^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$')
        self.re_066203d3 = re.compile(ur'^[0-9]+$')
        self.re_0ae2edfd = re.compile(ur'^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$')
        self.re_0b0f0f56 = re.compile(ur'^0$|^(-|\+)?[1-5]$')
        self.re_18424cc6 = re.compile(ur'^[0-9]+,[0-9][0-9]?( (m|ft))?$')
        self.re_1d428b19 = re.compile(ur'^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$')
        self.re_1e934345 = re.compile(ur'^[0-9]+,[0-9][0-9]?( (t|kg|lbs))?$')
        self.re_288e587a = re.compile(ur'^\+\d')
        self.re_29d73dcf = re.compile(ur'^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$')
        self.re_2a784076 = re.compile(ur'^(([0-9]|[1-9][0-9]*)(\.5)?)$')
        self.re_2b84c9ab = re.compile(ur'^[0-9]+,[0-9][0-9]?$')
        self.re_43c55ce5 = re.compile(ur'(.*[A-Za-z].*)|.*,.*|.*( ).*')
        self.re_45b46d60 = re.compile(ur'^-?[0-9]+(\.[0-9]+)?$')
        self.re_45e73e1b = re.compile(ur'^(up|down|-?([0-9]+?(\.[1-9]%)?|100)[%°]?)$')
        self.re_49888e30 = re.compile(ur'^(([0-9]+\.?[0-9]*( [a-z]+)?)|([0-9]+\'([0-9]+\.?[0-9]*\")?))$')
        self.re_4b9c2b6a = re.compile(ur'^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$')
        self.re_4d44d8e0 = re.compile(ur'^(0|[1-9][0-9]*(\.[0-9]+)?)( (kHz|MHz|GHz|THz))?$')
        self.re_4e26566a = re.compile(ur'^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*|broad|standard|narrow)$')
        self.re_5478d8af = re.compile(ur'^[1-9]([0-9]*)$')
        self.re_55d147d6 = re.compile(ur'^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$')
        self.re_597f003d = re.compile(ur'^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$')
        self.re_63a07204 = re.compile(ur'^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$')
        self.re_762a1d1d = re.compile(ur'^-?[0-9]+(\.[0-9]+)? ?m$')
        self.re_7f163374 = re.compile(ur'^(1|2|3|4|5|6|7|8|9|10|11|12)$')
        self.re_7f19b94b = re.compile(ur'^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_distance_separator_autofix = set_ele_meter_remove_autofix = set_ele_separator_autofix = set_height_separator_autofix = set_maxheight_separator_autofix = set_maxweight_separator_autofix = set_maxwidth_separator_autofix = set_width_separator_autofix = False

        # *[/^[0-9]+$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("numerical key")
                err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr(u'numerical key')})

        # *[layer=~/^\+\d/]
        if (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_288e587a), mapcss._tag_capture(capture_tags, 0, tags, u'layer')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value with + sign","{0.key}")
                # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
                # assertMatch:"node layer=+1"
                # assertNoMatch:"node layer=+foo"
                # assertNoMatch:"node layer=-1"
                # assertNoMatch:"node layer=1"
                err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr(u'{0} value with + sign', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'layer=', mapcss.replace(mapcss.tag(tags, u'layer'), u'+', u''))).split('=', 1)])
                }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_0b0f0f56), mapcss._tag_capture(capture_tags, 1, tags, u'layer')))
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
                err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr(u'{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if (u'building:levels' in keys) or (u'level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_2a784076), mapcss._tag_capture(capture_tags, 1, tags, u'building:levels')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'level') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f19b94b), mapcss._tag_capture(capture_tags, 1, tags, u'level')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
                # assertMatch:"node building:levels=-1"
                # assertNoMatch:"node building:levels=0"
                # assertNoMatch:"node building:levels=1.5"
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
                err.append({'class': 9006004, 'subclass': 1004173499, 'text': mapcss.tr(u'{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[height][height=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'height') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'height')))
                except mapcss.RuleAbort: pass
            if match:
                # setheight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("height=",replace(tag("height"),",","."))
                # assertMatch:"node height=12,00"
                # assertNoMatch:"node height=12,000"
                # assertMatch:"node height=12,5 ft"
                # assertNoMatch:"node height=3,50,5"
                # assertNoMatch:"node height=3.5"
                # assertNoMatch:"node height=4"
                # assertMatch:"node height=5,5"
                set_height_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1079140059, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'height=', mapcss.replace(mapcss.tag(tags, u'height'), u',', u'.'))).split('=', 1)])
                }})

        # *[height][height!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!.height_separator_autofix
        if (u'height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_height_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'height') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_597f003d), mapcss._tag_capture(capture_tags, 1, tags, u'height')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                # assertNoMatch:"node height=22'"
                # assertMatch:"node height=-5"
                # assertNoMatch:"node height=2 m"
                # assertNoMatch:"node height=20 ft"
                # assertNoMatch:"node height=5"
                # assertNoMatch:"node height=7.8"
                # assertMatch:"node height=medium"
                err.append({'class': 9006018, 'subclass': 929433247, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxheight][maxheight=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'maxheight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxheight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxheight=",replace(tag("maxheight"),",","."))
                # assertMatch:"node maxheight=12,00"
                # assertNoMatch:"node maxheight=12,000"
                # assertMatch:"node maxheight=12,5 ft"
                # assertNoMatch:"node maxheight=3,50,5"
                # assertNoMatch:"node maxheight=3.5"
                # assertNoMatch:"node maxheight=4"
                # assertMatch:"node maxheight=5,5"
                set_maxheight_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 72165305, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxheight=', mapcss.replace(mapcss.tag(tags, u'maxheight'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!.maxheight_separator_autofix
        if (u'maxheight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxheight_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_29d73dcf), mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                # assertNoMatch:"node maxheight=10'"
                # assertMatch:"node maxheight=-5"
                # assertMatch:"node maxheight=0"
                # assertNoMatch:"node maxheight=14 ft"
                # assertNoMatch:"node maxheight=16'3\""
                # assertNoMatch:"node maxheight=2 m"
                # assertNoMatch:"node maxheight=3.5"
                # assertNoMatch:"node maxheight=4"
                # assertMatch:"node maxheight=something"
                err.append({'class': 9006018, 'subclass': 1179691550, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[width][width=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'width') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'width')))
                except mapcss.RuleAbort: pass
            if match:
                # setwidth_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("width=",replace(tag("width"),",","."))
                # assertMatch:"node width=12,00"
                # assertNoMatch:"node width=12,000"
                # assertNoMatch:"node width=3,50,5"
                # assertNoMatch:"node width=3.5"
                # assertNoMatch:"node width=4"
                # assertMatch:"node width=5,5"
                set_width_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1422350111, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'width=', mapcss.replace(mapcss.tag(tags, u'width'), u',', u'.'))).split('=', 1)])
                }})

        # *[width][width!~/^(([0-9]+\.?[0-9]*( [a-z]+)?)|([0-9]+\'([0-9]+\.?[0-9]*\")?))$/]!.width_separator_autofix
        if (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_width_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'width') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_49888e30), mapcss._tag_capture(capture_tags, 1, tags, u'width')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 587682576, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxwidth][maxwidth=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'maxwidth' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxwidth_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxwidth=",replace(tag("maxwidth"),",","."))
                # assertMatch:"node maxwidth=12,00"
                # assertNoMatch:"node maxwidth=12,000"
                # assertNoMatch:"node maxwidth=3,50,5"
                # assertNoMatch:"node maxwidth=3.5"
                # assertNoMatch:"node maxwidth=4"
                # assertMatch:"node maxwidth=5,5"
                set_maxwidth_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1276502300, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxwidth=', mapcss.replace(mapcss.tag(tags, u'maxwidth'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxwidth][maxwidth!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.maxwidth_separator_autofix
        if (u'maxwidth' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxwidth_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1d428b19), mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 1600821089, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxweight][maxweight=~/^[0-9]+,[0-9][0-9]?( (t|kg|lbs))?$/]
        if (u'maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1e934345), mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxweight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxweight=",replace(tag("maxweight"),",","."))
                # assertMatch:"node maxweight=12,00"
                # assertNoMatch:"node maxweight=12,000"
                # assertNoMatch:"node maxweight=3,50,5"
                # assertNoMatch:"node maxweight=3.5"
                # assertNoMatch:"node maxweight=4"
                # assertMatch:"node maxweight=5,5"
                set_maxweight_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1860114154, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxweight=', mapcss.replace(mapcss.tag(tags, u'maxweight'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxweight][maxweight!~/^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.maxweight_separator_autofix
        if (u'maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxweight_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_035d45f0), mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: tonne is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006019, 'subclass': 280688781, 'text': mapcss.tr(u'unusual value of {0}: tonne is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[distance][distance=~/^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$/]
        if (u'distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'distance') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_55d147d6), mapcss._tag_capture(capture_tags, 1, tags, u'distance')))
                except mapcss.RuleAbort: pass
            if match:
                # setdistance_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("distance=",replace(tag("distance"),",","."))
                # assertMatch:"node distance=12,00"
                # assertNoMatch:"node distance=12,000"
                # assertNoMatch:"node distance=3,50,5"
                # assertNoMatch:"node distance=3.5"
                # assertNoMatch:"node distance=4"
                # assertMatch:"node distance=5,5"
                set_distance_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 13385038, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'distance=', mapcss.replace(mapcss.tag(tags, u'distance'), u',', u'.'))).split('=', 1)])
                }})

        # *[distance][distance!~/^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.distance_separator_autofix
        if (u'distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_distance_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'distance') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4b9c2b6a), mapcss._tag_capture(capture_tags, 1, tags, u'distance')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: kilometers is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006020, 'subclass': 1603863445, 'text': mapcss.tr(u'unusual value of {0}: kilometers is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[population][population!~/^[0-9]+$/]
        if (u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'population') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_066203d3), mapcss._tag_capture(capture_tags, 1, tags, u'population')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value","{0.key}")
                err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr(u'{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if (u'amenity' in keys and u'screen' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'screen') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5478d8af), mapcss._tag_capture(capture_tags, 1, tags, u'screen')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'cinema'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} must be a positive integer number","{0.key}")
                # assertNoMatch:"node amenity=cinema screen=8"
                # assertMatch:"node amenity=cinema screen=led"
                err.append({'class': 9006009, 'subclass': 1499065449, 'text': mapcss.tr(u'{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if (u'admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f163374), mapcss._tag_capture(capture_tags, 1, tags, u'admin_level')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertMatch:"node admin_level=-1"
                # assertMatch:"node admin_level=0"
                # assertMatch:"node admin_level=13"
                # assertNoMatch:"node admin_level=5"
                err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        if (u'direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') < mapcss._value_capture(capture_tags, 1, 0))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') >= mapcss._value_capture(capture_tags, 1, 360))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertMatch:"node direction=-10"
                # assertNoMatch:"node direction=0"
                # assertMatch:"node direction=360"
                err.append({'class': 9006010, 'subclass': 76996599, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if (u'direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_63a07204), mapcss._tag_capture(capture_tags, 1, tags, u'direction')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"node direction=0"
                # assertNoMatch:"node direction=0-360"
                # assertMatch:"node direction=1360"
                # assertNoMatch:"node direction=360"
                # assertNoMatch:"node direction=45"
                # assertMatch:"node direction=45-100;190-250;300"
                # assertNoMatch:"node direction=45-100;190-250;300-360"
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
                err.append({'class': 9006010, 'subclass': 1961301012, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_762a1d1d), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # setele_meter_remove_autofix
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
                err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, u'ele'), u'm', u'')))).split('=', 1)])
                }})

        # *[ele][ele=~/^[0-9]+,[0-9][0-9]?$/]
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_2b84c9ab), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # setele_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("ele=",replace(tag("ele"),",","."))
                # assertMatch:"node ele=12,00"
                # assertNoMatch:"node ele=3,50,5"
                # assertNoMatch:"node ele=3.5"
                # assertNoMatch:"node ele=4"
                # assertMatch:"node ele=5,5"
                # assertNoMatch:"node ele=8,848"
                set_ele_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 202511106, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ele=', mapcss.replace(mapcss.tag(tags, u'ele'), u',', u'.'))).split('=', 1)])
                }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_meter_remove_autofix!.ele_separator_autofix
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_ele_meter_remove_autofix and not set_ele_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'ele') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_45b46d60), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
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
                err.append({'class': 9006011, 'subclass': 1781084832, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_distance_separator_autofix = set_ele_meter_remove_autofix = set_ele_separator_autofix = set_height_separator_autofix = set_maxheight_separator_autofix = set_maxweight_separator_autofix = set_maxwidth_separator_autofix = set_width_separator_autofix = False

        # *[/^[0-9]+$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("numerical key")
                # assertMatch:"way 123=foo"
                # assertNoMatch:"way ref.1=foo"
                err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr(u'numerical key')})

        # *[layer=~/^\+\d/]
        if (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_288e587a), mapcss._tag_capture(capture_tags, 0, tags, u'layer')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value with + sign","{0.key}")
                # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
                err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr(u'{0} value with + sign', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'layer=', mapcss.replace(mapcss.tag(tags, u'layer'), u'+', u''))).split('=', 1)])
                }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_0b0f0f56), mapcss._tag_capture(capture_tags, 1, tags, u'layer')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be an integer value between -5 and 5","{0.key}")
                err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr(u'{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if (u'building:levels' in keys) or (u'level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_2a784076), mapcss._tag_capture(capture_tags, 1, tags, u'building:levels')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'level') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f19b94b), mapcss._tag_capture(capture_tags, 1, tags, u'level')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
                err.append({'class': 9006004, 'subclass': 1004173499, 'text': mapcss.tr(u'{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[height][height=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'height') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'height')))
                except mapcss.RuleAbort: pass
            if match:
                # setheight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("height=",replace(tag("height"),",","."))
                set_height_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1079140059, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'height=', mapcss.replace(mapcss.tag(tags, u'height'), u',', u'.'))).split('=', 1)])
                }})

        # *[height][height!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!.height_separator_autofix
        if (u'height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_height_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'height') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_597f003d), mapcss._tag_capture(capture_tags, 1, tags, u'height')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 929433247, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxheight][maxheight=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'maxheight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxheight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxheight=",replace(tag("maxheight"),",","."))
                set_maxheight_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 72165305, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxheight=', mapcss.replace(mapcss.tag(tags, u'maxheight'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!.maxheight_separator_autofix
        if (u'maxheight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxheight_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_29d73dcf), mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 1179691550, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[width][width=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'width') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'width')))
                except mapcss.RuleAbort: pass
            if match:
                # setwidth_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("width=",replace(tag("width"),",","."))
                set_width_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1422350111, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'width=', mapcss.replace(mapcss.tag(tags, u'width'), u',', u'.'))).split('=', 1)])
                }})

        # *[width][width!~/^(([0-9]+\.?[0-9]*( [a-z]+)?)|([0-9]+\'([0-9]+\.?[0-9]*\")?))$/]!.width_separator_autofix
        if (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_width_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'width') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_49888e30), mapcss._tag_capture(capture_tags, 1, tags, u'width')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                # assertNoMatch:"way width=1'"
                # assertMatch:"way width=-5"
                # assertNoMatch:"way width=0.5"
                # assertNoMatch:"way width=1 m"
                # assertNoMatch:"way width=10 ft"
                # assertNoMatch:"way width=10'5\""
                # assertNoMatch:"way width=3"
                # assertMatch:"way width=something"
                err.append({'class': 9006018, 'subclass': 587682576, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxwidth][maxwidth=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'maxwidth' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxwidth_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxwidth=",replace(tag("maxwidth"),",","."))
                set_maxwidth_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1276502300, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxwidth=', mapcss.replace(mapcss.tag(tags, u'maxwidth'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxwidth][maxwidth!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.maxwidth_separator_autofix
        if (u'maxwidth' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxwidth_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1d428b19), mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                # assertMatch:"way maxwidth=-5"
                # assertNoMatch:"way maxwidth=2"
                # assertNoMatch:"way maxwidth=2.5"
                # assertNoMatch:"way maxwidth=6'6\""
                # assertNoMatch:"way maxwidth=7 ft"
                # assertMatch:"way maxwidth=something"
                err.append({'class': 9006018, 'subclass': 1600821089, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxweight][maxweight=~/^[0-9]+,[0-9][0-9]?( (t|kg|lbs))?$/]
        if (u'maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1e934345), mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxweight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxweight=",replace(tag("maxweight"),",","."))
                set_maxweight_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1860114154, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxweight=', mapcss.replace(mapcss.tag(tags, u'maxweight'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxweight][maxweight!~/^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.maxweight_separator_autofix
        if (u'maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxweight_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_035d45f0), mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: tonne is default; point is decimal separator; if units, put space then unit","{0.key}")
                # assertMatch:"way maxweight=-5"
                # assertNoMatch:"way maxweight=2"
                # assertNoMatch:"way maxweight=2.5"
                # assertNoMatch:"way maxweight=6'6\""
                # assertNoMatch:"way maxweight=7 kg"
                # assertMatch:"way maxweight=something"
                err.append({'class': 9006019, 'subclass': 280688781, 'text': mapcss.tr(u'unusual value of {0}: tonne is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[maxspeed][maxspeed!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        # way[maxspeed:forward][maxspeed:forward!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        # way[maxspeed:backward][maxspeed:backward!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        if (u'maxspeed' in keys) or (u'maxspeed:backward' in keys) or (u'maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_0ae2edfd), mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:forward') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_0ae2edfd), mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:forward')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:backward') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_0ae2edfd), mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:backward')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
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
                err.append({'class': 9006010, 'subclass': 683878293, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[distance][distance=~/^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$/]
        if (u'distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'distance') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_55d147d6), mapcss._tag_capture(capture_tags, 1, tags, u'distance')))
                except mapcss.RuleAbort: pass
            if match:
                # setdistance_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("distance=",replace(tag("distance"),",","."))
                set_distance_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 13385038, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'distance=', mapcss.replace(mapcss.tag(tags, u'distance'), u',', u'.'))).split('=', 1)])
                }})

        # *[distance][distance!~/^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.distance_separator_autofix
        if (u'distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_distance_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'distance') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4b9c2b6a), mapcss._tag_capture(capture_tags, 1, tags, u'distance')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: kilometers is default; point is decimal separator; if units, put space then unit","{0.key}")
                # assertMatch:"way distance=-5"
                # assertNoMatch:"way distance=2"
                # assertNoMatch:"way distance=2.5"
                # assertNoMatch:"way distance=7 mi"
                # assertMatch:"way distance=something"
                err.append({'class': 9006020, 'subclass': 1603863445, 'text': mapcss.tr(u'unusual value of {0}: kilometers is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[voltage][voltage=~/(.*[A-Za-z].*)|.*,.*|.*( ).*/]
        if (u'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'voltage') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_43c55ce5), mapcss._tag_capture(capture_tags, 1, tags, u'voltage')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("voltage should be in volts with no units/delimiter/spaces")
                # assertNoMatch:"way voltage=15000"
                # assertMatch:"way voltage=medium"
                err.append({'class': 9006013, 'subclass': 300093258, 'text': mapcss.tr(u'voltage should be in volts with no units/delimiter/spaces')})

        # way[frequency][frequency!~/^(0|[1-9][0-9]*(\.[0-9]+)?)( (kHz|MHz|GHz|THz))?$/]
        if (u'frequency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'frequency') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4d44d8e0), mapcss._tag_capture(capture_tags, 1, tags, u'frequency')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"way frequency=0"
                # assertNoMatch:"way frequency=123.5 MHz"
                # assertNoMatch:"way frequency=16.7"
                # assertNoMatch:"way frequency=50"
                # assertNoMatch:"way frequency=680 kHz"
                # assertMatch:"way frequency=something"
                err.append({'class': 9006010, 'subclass': 582321238, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[gauge][gauge!~/^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*|broad|standard|narrow)$/]
        if (u'gauge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gauge') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4e26566a), mapcss._tag_capture(capture_tags, 1, tags, u'gauge')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"way gauge=1000;1435"
                # assertNoMatch:"way gauge=1435"
                # assertNoMatch:"way gauge=narrow"
                # assertMatch:"way gauge=something"
                # assertNoMatch:"way gauge=standard"
                err.append({'class': 9006010, 'subclass': 415876153, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[incline][incline!~/^(up|down|-?([0-9]+?(\.[1-9]%)?|100)[%°]?)$/]
        if (u'incline' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'incline') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_45e73e1b), mapcss._tag_capture(capture_tags, 1, tags, u'incline')))
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
                err.append({'class': 9006010, 'subclass': 901779967, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[population][population!~/^[0-9]+$/]
        if (u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'population') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_066203d3), mapcss._tag_capture(capture_tags, 1, tags, u'population')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value","{0.key}")
                err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr(u'{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[lanes][lanes!~/^[1-9]([0-9]*)$/][highway]
        # way["lanes:backward"]["lanes:backward"!~/^[1-9]([0-9]*)$/][highway]
        # way["lanes:forward"]["lanes:forward"!~/^[1-9]([0-9]*)$/][highway]
        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if (u'amenity' in keys and u'screen' in keys) or (u'highway' in keys and u'lanes' in keys) or (u'highway' in keys and u'lanes:backward' in keys) or (u'highway' in keys and u'lanes:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lanes') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5478d8af), mapcss._tag_capture(capture_tags, 1, tags, u'lanes')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lanes:backward') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5478d8af), mapcss._tag_capture(capture_tags, 1, tags, u'lanes:backward')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lanes:forward') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5478d8af), mapcss._tag_capture(capture_tags, 1, tags, u'lanes:forward')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'screen') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5478d8af), mapcss._tag_capture(capture_tags, 1, tags, u'screen')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'cinema'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} must be a positive integer number","{0.key}")
                # assertMatch:"way highway=residential lanes:backward=-1"
                # assertMatch:"way highway=residential lanes:forward=-1"
                # assertMatch:"way highway=residential lanes=-1"
                # assertNoMatch:"way highway=residential lanes=1"
                # assertMatch:"way highway=residential lanes=1;2"
                # assertMatch:"way highway=residential lanes=5.5"
                err.append({'class': 9006009, 'subclass': 10320184, 'text': mapcss.tr(u'{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if (u'admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f163374), mapcss._tag_capture(capture_tags, 1, tags, u'admin_level')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        if (u'direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') < mapcss._value_capture(capture_tags, 1, 0))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') >= mapcss._value_capture(capture_tags, 1, 360))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 76996599, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if (u'direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_63a07204), mapcss._tag_capture(capture_tags, 1, tags, u'direction')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1961301012, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_762a1d1d), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # setele_meter_remove_autofix
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
                set_ele_meter_remove_autofix = True
                err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, u'ele'), u'm', u'')))).split('=', 1)])
                }})

        # *[ele][ele=~/^[0-9]+,[0-9][0-9]?$/]
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_2b84c9ab), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # setele_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("ele=",replace(tag("ele"),",","."))
                set_ele_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 202511106, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ele=', mapcss.replace(mapcss.tag(tags, u'ele'), u',', u'.'))).split('=', 1)])
                }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_meter_remove_autofix!.ele_separator_autofix
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_ele_meter_remove_autofix and not set_ele_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'ele') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_45b46d60), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                err.append({'class': 9006011, 'subclass': 1781084832, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_distance_separator_autofix = set_ele_meter_remove_autofix = set_ele_separator_autofix = set_height_separator_autofix = set_maxheight_separator_autofix = set_maxweight_separator_autofix = set_maxwidth_separator_autofix = set_width_separator_autofix = False

        # *[/^[0-9]+$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("numerical key")
                err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr(u'numerical key')})

        # *[layer=~/^\+\d/]
        if (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_288e587a), mapcss._tag_capture(capture_tags, 0, tags, u'layer')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value with + sign","{0.key}")
                # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
                err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr(u'{0} value with + sign', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'layer=', mapcss.replace(mapcss.tag(tags, u'layer'), u'+', u''))).split('=', 1)])
                }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if (u'layer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_0b0f0f56), mapcss._tag_capture(capture_tags, 1, tags, u'layer')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be an integer value between -5 and 5","{0.key}")
                err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr(u'{0} should be an integer value between -5 and 5', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if (u'building:levels' in keys) or (u'level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_2a784076), mapcss._tag_capture(capture_tags, 1, tags, u'building:levels')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'level') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f19b94b), mapcss._tag_capture(capture_tags, 1, tags, u'level')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
                err.append({'class': 9006004, 'subclass': 1004173499, 'text': mapcss.tr(u'{0} should have numbers only with optional .5 increments', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[height][height=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'height') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'height')))
                except mapcss.RuleAbort: pass
            if match:
                # setheight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("height=",replace(tag("height"),",","."))
                set_height_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1079140059, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'height=', mapcss.replace(mapcss.tag(tags, u'height'), u',', u'.'))).split('=', 1)])
                }})

        # *[height][height!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]!.height_separator_autofix
        if (u'height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_height_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'height') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_597f003d), mapcss._tag_capture(capture_tags, 1, tags, u'height')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 929433247, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxheight][maxheight=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'maxheight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxheight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxheight=",replace(tag("maxheight"),",","."))
                set_maxheight_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 72165305, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxheight=', mapcss.replace(mapcss.tag(tags, u'maxheight'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default|below_default)$/]!.maxheight_separator_autofix
        if (u'maxheight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxheight_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_29d73dcf), mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 1179691550, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[width][width=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'width') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'width')))
                except mapcss.RuleAbort: pass
            if match:
                # setwidth_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("width=",replace(tag("width"),",","."))
                set_width_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1422350111, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'width=', mapcss.replace(mapcss.tag(tags, u'width'), u',', u'.'))).split('=', 1)])
                }})

        # *[width][width!~/^(([0-9]+\.?[0-9]*( [a-z]+)?)|([0-9]+\'([0-9]+\.?[0-9]*\")?))$/]!.width_separator_autofix
        if (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_width_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'width') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_49888e30), mapcss._tag_capture(capture_tags, 1, tags, u'width')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 587682576, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxwidth][maxwidth=~/^[0-9]+,[0-9][0-9]?( (m|ft))?$/]
        if (u'maxwidth' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_18424cc6), mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxwidth_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxwidth=",replace(tag("maxwidth"),",","."))
                set_maxwidth_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1276502300, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxwidth=', mapcss.replace(mapcss.tag(tags, u'maxwidth'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxwidth][maxwidth!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.maxwidth_separator_autofix
        if (u'maxwidth' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxwidth_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1d428b19), mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006018, 'subclass': 1600821089, 'text': mapcss.tr(u'unusual value of {0}: meters is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[maxweight][maxweight=~/^[0-9]+,[0-9][0-9]?( (t|kg|lbs))?$/]
        if (u'maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1e934345), mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))
                except mapcss.RuleAbort: pass
            if match:
                # setmaxweight_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("maxweight=",replace(tag("maxweight"),",","."))
                set_maxweight_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 1860114154, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'maxweight=', mapcss.replace(mapcss.tag(tags, u'maxweight'), u',', u'.'))).split('=', 1)])
                }})

        # *[maxweight][maxweight!~/^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.maxweight_separator_autofix
        if (u'maxweight' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_maxweight_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_035d45f0), mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: tonne is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006019, 'subclass': 280688781, 'text': mapcss.tr(u'unusual value of {0}: tonne is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[distance][distance=~/^[0-9]+,[0-9][0-9]?( (m|km|mi|nmi))?$/]
        if (u'distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'distance') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_55d147d6), mapcss._tag_capture(capture_tags, 1, tags, u'distance')))
                except mapcss.RuleAbort: pass
            if match:
                # setdistance_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("distance=",replace(tag("distance"),",","."))
                set_distance_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 13385038, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'distance=', mapcss.replace(mapcss.tag(tags, u'distance'), u',', u'.'))).split('=', 1)])
                }})

        # *[distance][distance!~/^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]!.distance_separator_autofix
        if (u'distance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_distance_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'distance') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4b9c2b6a), mapcss._tag_capture(capture_tags, 1, tags, u'distance')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}: kilometers is default; point is decimal separator; if units, put space then unit","{0.key}")
                err.append({'class': 9006020, 'subclass': 1603863445, 'text': mapcss.tr(u'unusual value of {0}: kilometers is default; point is decimal separator; if units, put space then unit', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[population][population!~/^[0-9]+$/]
        if (u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'population') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_066203d3), mapcss._tag_capture(capture_tags, 1, tags, u'population')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value","{0.key}")
                err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr(u'{0} must be a numeric value', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if (u'amenity' in keys and u'screen' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'screen') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5478d8af), mapcss._tag_capture(capture_tags, 1, tags, u'screen')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == mapcss._value_capture(capture_tags, 2, u'cinema'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} must be a positive integer number","{0.key}")
                err.append({'class': 9006009, 'subclass': 1499065449, 'text': mapcss.tr(u'{0} must be a positive integer number', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if (u'admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f163374), mapcss._tag_capture(capture_tags, 1, tags, u'admin_level')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        if (u'direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') < mapcss._value_capture(capture_tags, 1, 0))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') >= mapcss._value_capture(capture_tags, 1, 360))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 76996599, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if (u'direction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_63a07204), mapcss._tag_capture(capture_tags, 1, tags, u'direction')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9006010, 'subclass': 1961301012, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_762a1d1d), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # setele_meter_remove_autofix
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
                set_ele_meter_remove_autofix = True
                err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, u'ele'), u'm', u'')))).split('=', 1)])
                }})

        # *[ele][ele=~/^[0-9]+,[0-9][0-9]?$/]
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_2b84c9ab), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # setele_separator_autofix
                # throwWarning:tr("unusual value of {0}: use . instead of , as decimal separator","{0.key}")
                # fixAdd:concat("ele=",replace(tag("ele"),",","."))
                set_ele_separator_autofix = True
                err.append({'class': 9006017, 'subclass': 202511106, 'text': mapcss.tr(u'unusual value of {0}: use . instead of , as decimal separator', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ele=', mapcss.replace(mapcss.tag(tags, u'ele'), u',', u'.'))).split('=', 1)])
                }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_meter_remove_autofix!.ele_separator_autofix
        if (u'ele' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_ele_meter_remove_autofix and not set_ele_separator_autofix and mapcss._tag_capture(capture_tags, 0, tags, u'ele') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_45b46d60), mapcss._tag_capture(capture_tags, 1, tags, u'ele')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
                err.append({'class': 9006011, 'subclass': 1781084832, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_numeric(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'layer': u'+1'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_not_err(n.node(data, {u'layer': u'+foo'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_not_err(n.node(data, {u'layer': u'-1'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_not_err(n.node(data, {u'layer': u'1'}), expected={'class': 9006002, 'subclass': 873121454})
        self.check_err(n.node(data, {u'layer': u'+10'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {u'layer': u'+5'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {u'layer': u'-5'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {u'layer': u'-50'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {u'layer': u'0'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {u'layer': u'0.5'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {u'layer': u'0;1'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_not_err(n.node(data, {u'layer': u'2'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {u'layer': u'6'}), expected={'class': 9006003, 'subclass': 1089386010})
        self.check_err(n.node(data, {u'building:levels': u'-1'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'building:levels': u'0'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'building:levels': u'1.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_err(n.node(data, {u'level': u'-0'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'-0.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'-0.5;0'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_err(n.node(data, {u'level': u'-01.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_err(n.node(data, {u'level': u'-03'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'-1'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'-1;-0.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'0'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_err(n.node(data, {u'level': u'01'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'0;-0.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'0;1'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'1'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'1.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'12'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'1;0.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_not_err(n.node(data, {u'level': u'1;1.5'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_err(n.node(data, {u'level': u'2.3'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_err(n.node(data, {u'level': u'one'}), expected={'class': 9006004, 'subclass': 1004173499})
        self.check_err(n.node(data, {u'height': u'12,00'}), expected={'class': 9006017, 'subclass': 1079140059})
        self.check_not_err(n.node(data, {u'height': u'12,000'}), expected={'class': 9006017, 'subclass': 1079140059})
        self.check_err(n.node(data, {u'height': u'12,5 ft'}), expected={'class': 9006017, 'subclass': 1079140059})
        self.check_not_err(n.node(data, {u'height': u'3,50,5'}), expected={'class': 9006017, 'subclass': 1079140059})
        self.check_not_err(n.node(data, {u'height': u'3.5'}), expected={'class': 9006017, 'subclass': 1079140059})
        self.check_not_err(n.node(data, {u'height': u'4'}), expected={'class': 9006017, 'subclass': 1079140059})
        self.check_err(n.node(data, {u'height': u'5,5'}), expected={'class': 9006017, 'subclass': 1079140059})
        self.check_not_err(n.node(data, {u'height': u'22\''}), expected={'class': 9006018, 'subclass': 929433247})
        self.check_err(n.node(data, {u'height': u'-5'}), expected={'class': 9006018, 'subclass': 929433247})
        self.check_not_err(n.node(data, {u'height': u'2 m'}), expected={'class': 9006018, 'subclass': 929433247})
        self.check_not_err(n.node(data, {u'height': u'20 ft'}), expected={'class': 9006018, 'subclass': 929433247})
        self.check_not_err(n.node(data, {u'height': u'5'}), expected={'class': 9006018, 'subclass': 929433247})
        self.check_not_err(n.node(data, {u'height': u'7.8'}), expected={'class': 9006018, 'subclass': 929433247})
        self.check_err(n.node(data, {u'height': u'medium'}), expected={'class': 9006018, 'subclass': 929433247})
        self.check_err(n.node(data, {u'maxheight': u'12,00'}), expected={'class': 9006017, 'subclass': 72165305})
        self.check_not_err(n.node(data, {u'maxheight': u'12,000'}), expected={'class': 9006017, 'subclass': 72165305})
        self.check_err(n.node(data, {u'maxheight': u'12,5 ft'}), expected={'class': 9006017, 'subclass': 72165305})
        self.check_not_err(n.node(data, {u'maxheight': u'3,50,5'}), expected={'class': 9006017, 'subclass': 72165305})
        self.check_not_err(n.node(data, {u'maxheight': u'3.5'}), expected={'class': 9006017, 'subclass': 72165305})
        self.check_not_err(n.node(data, {u'maxheight': u'4'}), expected={'class': 9006017, 'subclass': 72165305})
        self.check_err(n.node(data, {u'maxheight': u'5,5'}), expected={'class': 9006017, 'subclass': 72165305})
        self.check_not_err(n.node(data, {u'maxheight': u'10\''}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_err(n.node(data, {u'maxheight': u'-5'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_err(n.node(data, {u'maxheight': u'0'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_not_err(n.node(data, {u'maxheight': u'14 ft'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_not_err(n.node(data, {u'maxheight': u'16\'3"'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_not_err(n.node(data, {u'maxheight': u'2 m'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_not_err(n.node(data, {u'maxheight': u'3.5'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_not_err(n.node(data, {u'maxheight': u'4'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_err(n.node(data, {u'maxheight': u'something'}), expected={'class': 9006018, 'subclass': 1179691550})
        self.check_err(n.node(data, {u'width': u'12,00'}), expected={'class': 9006017, 'subclass': 1422350111})
        self.check_not_err(n.node(data, {u'width': u'12,000'}), expected={'class': 9006017, 'subclass': 1422350111})
        self.check_not_err(n.node(data, {u'width': u'3,50,5'}), expected={'class': 9006017, 'subclass': 1422350111})
        self.check_not_err(n.node(data, {u'width': u'3.5'}), expected={'class': 9006017, 'subclass': 1422350111})
        self.check_not_err(n.node(data, {u'width': u'4'}), expected={'class': 9006017, 'subclass': 1422350111})
        self.check_err(n.node(data, {u'width': u'5,5'}), expected={'class': 9006017, 'subclass': 1422350111})
        self.check_err(n.node(data, {u'maxwidth': u'12,00'}), expected={'class': 9006017, 'subclass': 1276502300})
        self.check_not_err(n.node(data, {u'maxwidth': u'12,000'}), expected={'class': 9006017, 'subclass': 1276502300})
        self.check_not_err(n.node(data, {u'maxwidth': u'3,50,5'}), expected={'class': 9006017, 'subclass': 1276502300})
        self.check_not_err(n.node(data, {u'maxwidth': u'3.5'}), expected={'class': 9006017, 'subclass': 1276502300})
        self.check_not_err(n.node(data, {u'maxwidth': u'4'}), expected={'class': 9006017, 'subclass': 1276502300})
        self.check_err(n.node(data, {u'maxwidth': u'5,5'}), expected={'class': 9006017, 'subclass': 1276502300})
        self.check_err(n.node(data, {u'maxweight': u'12,00'}), expected={'class': 9006017, 'subclass': 1860114154})
        self.check_not_err(n.node(data, {u'maxweight': u'12,000'}), expected={'class': 9006017, 'subclass': 1860114154})
        self.check_not_err(n.node(data, {u'maxweight': u'3,50,5'}), expected={'class': 9006017, 'subclass': 1860114154})
        self.check_not_err(n.node(data, {u'maxweight': u'3.5'}), expected={'class': 9006017, 'subclass': 1860114154})
        self.check_not_err(n.node(data, {u'maxweight': u'4'}), expected={'class': 9006017, 'subclass': 1860114154})
        self.check_err(n.node(data, {u'maxweight': u'5,5'}), expected={'class': 9006017, 'subclass': 1860114154})
        self.check_err(n.node(data, {u'distance': u'12,00'}), expected={'class': 9006017, 'subclass': 13385038})
        self.check_not_err(n.node(data, {u'distance': u'12,000'}), expected={'class': 9006017, 'subclass': 13385038})
        self.check_not_err(n.node(data, {u'distance': u'3,50,5'}), expected={'class': 9006017, 'subclass': 13385038})
        self.check_not_err(n.node(data, {u'distance': u'3.5'}), expected={'class': 9006017, 'subclass': 13385038})
        self.check_not_err(n.node(data, {u'distance': u'4'}), expected={'class': 9006017, 'subclass': 13385038})
        self.check_err(n.node(data, {u'distance': u'5,5'}), expected={'class': 9006017, 'subclass': 13385038})
        self.check_not_err(n.node(data, {u'amenity': u'cinema', u'screen': u'8'}), expected={'class': 9006009, 'subclass': 1499065449})
        self.check_err(n.node(data, {u'amenity': u'cinema', u'screen': u'led'}), expected={'class': 9006009, 'subclass': 1499065449})
        self.check_err(n.node(data, {u'admin_level': u'-1'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_err(n.node(data, {u'admin_level': u'0'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_err(n.node(data, {u'admin_level': u'13'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_not_err(n.node(data, {u'admin_level': u'5'}), expected={'class': 9006010, 'subclass': 1514270237})
        self.check_err(n.node(data, {u'direction': u'-10'}), expected={'class': 9006010, 'subclass': 76996599})
        self.check_not_err(n.node(data, {u'direction': u'0'}), expected={'class': 9006010, 'subclass': 76996599})
        self.check_err(n.node(data, {u'direction': u'360'}), expected={'class': 9006010, 'subclass': 76996599})
        self.check_not_err(n.node(data, {u'direction': u'0'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'0-360'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'1360'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'360'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'45'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'45-100;190-250;300'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'45-100;190-250;300-360'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'C'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'N'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'NE-S'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'NNE'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'NNNE'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'anti-clockwise'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'anticlockwise'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'down'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'forward'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'north-down'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'north-east'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'north-south'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'direction': u'rome'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'up'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_not_err(n.node(data, {u'direction': u'west'}), expected={'class': 9006010, 'subclass': 1961301012})
        self.check_err(n.node(data, {u'ele': u'-12.1 m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {u'ele': u'12 m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_not_err(n.node(data, {u'ele': u'12'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {u'ele': u'12.1m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_not_err(n.node(data, {u'ele': u'12km'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {u'ele': u'12m'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_not_err(n.node(data, {u'ele': u'high'}), expected={'class': 9006011, 'subclass': 1672584043})
        self.check_err(n.node(data, {u'ele': u'12,00'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {u'ele': u'3,50,5'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {u'ele': u'3.5'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {u'ele': u'4'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_err(n.node(data, {u'ele': u'5,5'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {u'ele': u'8,848'}), expected={'class': 9006017, 'subclass': 202511106})
        self.check_not_err(n.node(data, {u'ele': u'-12.1 m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {u'ele': u'12 m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {u'ele': u'12'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {u'ele': u'12.1m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_err(n.node(data, {u'ele': u'12km'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_not_err(n.node(data, {u'ele': u'12m'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_err(n.node(data, {u'ele': u'high'}), expected={'class': 9006011, 'subclass': 1781084832})
        self.check_err(n.way(data, {u'123': u'foo'}, [0]), expected={'class': 9006001, 'subclass': 750700308})
        self.check_not_err(n.way(data, {u'ref.1': u'foo'}, [0]), expected={'class': 9006001, 'subclass': 750700308})
        self.check_not_err(n.way(data, {u'width': u'1\''}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_err(n.way(data, {u'width': u'-5'}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_not_err(n.way(data, {u'width': u'0.5'}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_not_err(n.way(data, {u'width': u'1 m'}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_not_err(n.way(data, {u'width': u'10 ft'}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_not_err(n.way(data, {u'width': u'10\'5"'}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_not_err(n.way(data, {u'width': u'3'}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_err(n.way(data, {u'width': u'something'}, [0]), expected={'class': 9006018, 'subclass': 587682576})
        self.check_err(n.way(data, {u'maxwidth': u'-5'}, [0]), expected={'class': 9006018, 'subclass': 1600821089})
        self.check_not_err(n.way(data, {u'maxwidth': u'2'}, [0]), expected={'class': 9006018, 'subclass': 1600821089})
        self.check_not_err(n.way(data, {u'maxwidth': u'2.5'}, [0]), expected={'class': 9006018, 'subclass': 1600821089})
        self.check_not_err(n.way(data, {u'maxwidth': u'6\'6"'}, [0]), expected={'class': 9006018, 'subclass': 1600821089})
        self.check_not_err(n.way(data, {u'maxwidth': u'7 ft'}, [0]), expected={'class': 9006018, 'subclass': 1600821089})
        self.check_err(n.way(data, {u'maxwidth': u'something'}, [0]), expected={'class': 9006018, 'subclass': 1600821089})
        self.check_err(n.way(data, {u'maxweight': u'-5'}, [0]), expected={'class': 9006019, 'subclass': 280688781})
        self.check_not_err(n.way(data, {u'maxweight': u'2'}, [0]), expected={'class': 9006019, 'subclass': 280688781})
        self.check_not_err(n.way(data, {u'maxweight': u'2.5'}, [0]), expected={'class': 9006019, 'subclass': 280688781})
        self.check_not_err(n.way(data, {u'maxweight': u'6\'6"'}, [0]), expected={'class': 9006019, 'subclass': 280688781})
        self.check_not_err(n.way(data, {u'maxweight': u'7 kg'}, [0]), expected={'class': 9006019, 'subclass': 280688781})
        self.check_err(n.way(data, {u'maxweight': u'something'}, [0]), expected={'class': 9006019, 'subclass': 280688781})
        self.check_err(n.way(data, {u'maxspeed': u'-50'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_err(n.way(data, {u'maxspeed': u'0'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'30 mph'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'50'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'DE:motorway'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'RO:urban'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'RU:living_street'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'RU:rural'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'none'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'signals'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_err(n.way(data, {u'maxspeed': u'something'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'variable'}, [0]), expected={'class': 9006010, 'subclass': 683878293})
        self.check_err(n.way(data, {u'distance': u'-5'}, [0]), expected={'class': 9006020, 'subclass': 1603863445})
        self.check_not_err(n.way(data, {u'distance': u'2'}, [0]), expected={'class': 9006020, 'subclass': 1603863445})
        self.check_not_err(n.way(data, {u'distance': u'2.5'}, [0]), expected={'class': 9006020, 'subclass': 1603863445})
        self.check_not_err(n.way(data, {u'distance': u'7 mi'}, [0]), expected={'class': 9006020, 'subclass': 1603863445})
        self.check_err(n.way(data, {u'distance': u'something'}, [0]), expected={'class': 9006020, 'subclass': 1603863445})
        self.check_not_err(n.way(data, {u'voltage': u'15000'}, [0]), expected={'class': 9006013, 'subclass': 300093258})
        self.check_err(n.way(data, {u'voltage': u'medium'}, [0]), expected={'class': 9006013, 'subclass': 300093258})
        self.check_not_err(n.way(data, {u'frequency': u'0'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'123.5 MHz'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'16.7'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'50'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'680 kHz'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_err(n.way(data, {u'frequency': u'something'}, [0]), expected={'class': 9006010, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'gauge': u'1000;1435'}, [0]), expected={'class': 9006010, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'gauge': u'1435'}, [0]), expected={'class': 9006010, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'gauge': u'narrow'}, [0]), expected={'class': 9006010, 'subclass': 415876153})
        self.check_err(n.way(data, {u'gauge': u'something'}, [0]), expected={'class': 9006010, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'gauge': u'standard'}, [0]), expected={'class': 9006010, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'incline': u'-5%'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'10%'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'10°'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'down'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_err(n.way(data, {u'incline': u'extreme'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'up'}, [0]), expected={'class': 9006010, 'subclass': 901779967})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes:backward': u'-1'}, [0]), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes:forward': u'-1'}, [0]), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes': u'-1'}, [0]), expected={'class': 9006009, 'subclass': 10320184})
        self.check_not_err(n.way(data, {u'highway': u'residential', u'lanes': u'1'}, [0]), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes': u'1;2'}, [0]), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes': u'5.5'}, [0]), expected={'class': 9006009, 'subclass': 10320184})
