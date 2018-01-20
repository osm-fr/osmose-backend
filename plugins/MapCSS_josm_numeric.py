#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_numeric(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9006001] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'numerical key', capture_tags)}
        self.errors[9006002] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} value with + sign', capture_tags, u'{0.key}')}
        self.errors[9006003] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} should be an integer value between -5 and 5', capture_tags, u'{0.key}')}
        self.errors[9006004] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} should have numbers only with optional .5 increments', capture_tags, u'{0.key}')}
        self.errors[9006005] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'maxwidth')}
        self.errors[9006006] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0}: tonne is default; period is separator; if units, put space then unit', capture_tags, u'maxweight')}
        self.errors[9006007] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0}: kilometers is default; period is separator; if units, put space then unit', capture_tags, u'distance')}
        self.errors[9006008] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} must be a numeric value', capture_tags, u'{0.key}')}
        self.errors[9006009] = {'item': 9006, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'{0} must be a positive integer number', capture_tags, u'{0.key}')}
        self.errors[9006010] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')}
        self.errors[9006011] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} must be a numeric value, in meters and without units', capture_tags, u'{0.key}')}
        self.errors[9006012] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'unusual {0} format', capture_tags, u'maxspeed')}
        self.errors[9006013] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'voltage should be in volts with no units/delimiter/spaces', capture_tags)}
        self.errors[9006014] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'unusual {0} specification', capture_tags, u'frequency')}
        self.errors[9006015] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'unusual train track gauge; use mm with no separator', capture_tags)}
        self.errors[9006016] = {'item': 9006, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'unusual incline; use percentages/degrees or up/down', capture_tags)}

        self.re_035d45f0 = re.compile(ur'^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$')
        self.re_066203d3 = re.compile(ur'^[0-9]+$')
        self.re_0ae2edfd = re.compile(ur'^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$')
        self.re_0b0f0f56 = re.compile(ur'^0$|^(-|\+)?[1-5]$')
        self.re_1d428b19 = re.compile(ur'^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$')
        self.re_288e587a = re.compile(ur'^\+\d')
        self.re_2a784076 = re.compile(ur'^(([0-9]|[1-9][0-9]*)(\.5)?)$')
        self.re_43c55ce5 = re.compile(ur'(.*[A-Za-z].*)|.*,.*|.*( ).*')
        self.re_45b46d60 = re.compile(ur'^-?[0-9]+(\.[0-9]+)?$')
        self.re_45e73e1b = re.compile(ur'^(up|down|-?([0-9]+?(\.[1-9]%)?|100)[%°]?)$')
        self.re_49888e30 = re.compile(ur'^(([0-9]+\.?[0-9]*( [a-z]+)?)|([0-9]+\'([0-9]+\.?[0-9]*\")?))$')
        self.re_4b9c2b6a = re.compile(ur'^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$')
        self.re_4d44d8e0 = re.compile(ur'^(0|[1-9][0-9]*(\.[0-9]+)?)( (kHz|MHz|GHz|THz))?$')
        self.re_4e26566a = re.compile(ur'^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*|broad|standard|narrow)$')
        self.re_5478d8af = re.compile(ur'^[1-9]([0-9]*)$')
        self.re_597f003d = re.compile(ur'^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$')
        self.re_63a07204 = re.compile(ur'^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$')
        self.re_762a1d1d = re.compile(ur'^-?[0-9]+(\.[0-9]+)? ?m$')
        self.re_768a3762 = re.compile(ur'^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default)$')
        self.re_7f163374 = re.compile(ur'^(1|2|3|4|5|6|7|8|9|10|11|12)$')
        self.re_7f19b94b = re.compile(ur'^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_ele_is_fixable = False

        # *[/^[0-9]+$/]
        if ((mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3))):
            # throwWarning:tr("numerical key")
            err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr(u'numerical key', capture_tags)})

        # *[layer=~/^\+\d/]
        if (u'layer' in keys) and \
            ((mapcss.regexp_test_(self.re_288e587a, mapcss._tag_capture(capture_tags, 0, tags, u'layer')))):
            # throwWarning:tr("{0} value with + sign","{0.key}")
            # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
            # assertMatch:"node layer=+1"
            # assertNoMatch:"node layer=+foo"
            # assertNoMatch:"node layer=-1"
            # assertNoMatch:"node layer=1"
            err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr(u'{0} value with + sign', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'layer=', mapcss.replace(mapcss.tag(tags, u'layer'), u'+', u''))).split('=', 1)])
            }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if (u'layer' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss.regexp_test_(self.re_0b0f0f56, mapcss._tag_capture(capture_tags, 1, tags, u'layer')))):
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
            err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr(u'{0} should be an integer value between -5 and 5', capture_tags, u'{0.key}')})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if (u'building:levels' in keys or u'level' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss.regexp_test_(self.re_2a784076, mapcss._tag_capture(capture_tags, 1, tags, u'building:levels'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'level') and not mapcss.regexp_test_(self.re_7f19b94b, mapcss._tag_capture(capture_tags, 1, tags, u'level')))):
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
            err.append({'class': 9006004, 'subclass': 1004173499, 'text': mapcss.tr(u'{0} should have numbers only with optional .5 increments', capture_tags, u'{0.key}')})

        # *[height][height!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]
        if (u'height' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'height') and not mapcss.regexp_test_(self.re_597f003d, mapcss._tag_capture(capture_tags, 1, tags, u'height')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","height")
            # assertNoMatch:"node height=22'"
            # assertMatch:"node height=-5"
            # assertNoMatch:"node height=2 m"
            # assertNoMatch:"node height=20 ft"
            # assertNoMatch:"node height=5"
            # assertNoMatch:"node height=7.8"
            # assertMatch:"node height=medium"
            err.append({'class': 9006005, 'subclass': 1885029007, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'height')})

        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default)$/]
        if (u'maxheight' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and not mapcss.regexp_test_(self.re_768a3762, mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","maxheight")
            # assertNoMatch:"node maxheight=10'"
            # assertMatch:"node maxheight=-5"
            # assertMatch:"node maxheight=0"
            # assertNoMatch:"node maxheight=14 ft"
            # assertNoMatch:"node maxheight=16'3\""
            # assertNoMatch:"node maxheight=2 m"
            # assertNoMatch:"node maxheight=3.5"
            # assertNoMatch:"node maxheight=4"
            # assertMatch:"node maxheight=something"
            err.append({'class': 9006005, 'subclass': 1339141103, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'maxheight')})

        # *[maxwidth][maxwidth!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'maxwidth' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and not mapcss.regexp_test_(self.re_1d428b19, mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","maxwidth")
            err.append({'class': 9006005, 'subclass': 873145686, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'maxwidth')})

        # *[maxweight][maxweight!~/^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'maxweight' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and not mapcss.regexp_test_(self.re_035d45f0, mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))):
            # throwWarning:tr("{0}: tonne is default; period is separator; if units, put space then unit","maxweight")
            err.append({'class': 9006006, 'subclass': 1776650332, 'text': mapcss.tr(u'{0}: tonne is default; period is separator; if units, put space then unit', capture_tags, u'maxweight')})

        # *[distance][distance!~/^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'distance' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'distance') and not mapcss.regexp_test_(self.re_4b9c2b6a, mapcss._tag_capture(capture_tags, 1, tags, u'distance')))):
            # throwWarning:tr("{0}: kilometers is default; period is separator; if units, put space then unit","distance")
            err.append({'class': 9006007, 'subclass': 131693430, 'text': mapcss.tr(u'{0}: kilometers is default; period is separator; if units, put space then unit', capture_tags, u'distance')})

        # *[population][population!~/^[0-9]+$/]
        if (u'population' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'population') and not mapcss.regexp_test_(self.re_066203d3, mapcss._tag_capture(capture_tags, 1, tags, u'population')))):
            # throwWarning:tr("{0} must be a numeric value","{0.key}")
            err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr(u'{0} must be a numeric value', capture_tags, u'{0.key}')})

        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if (u'screen' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'screen') and not mapcss.regexp_test_(self.re_5478d8af, mapcss._tag_capture(capture_tags, 1, tags, u'screen')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == u'cinema')):
            # throwError:tr("{0} must be a positive integer number","{0.key}")
            # assertNoMatch:"node amenity=cinema screen=8"
            # assertMatch:"node amenity=cinema screen=led"
            err.append({'class': 9006009, 'subclass': 1499065449, 'text': mapcss.tr(u'{0} must be a positive integer number', capture_tags, u'{0.key}')})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if (u'admin_level' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss.regexp_test_(self.re_7f163374, mapcss._tag_capture(capture_tags, 1, tags, u'admin_level')))):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            # assertMatch:"node admin_level=-1"
            # assertMatch:"node admin_level=0"
            # assertMatch:"node admin_level=13"
            # assertNoMatch:"node admin_level=5"
            err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        if (u'direction' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') < 0) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') >= 360)):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            # assertMatch:"node direction=-10"
            # assertNoMatch:"node direction=0"
            # assertMatch:"node direction=360"
            err.append({'class': 9006010, 'subclass': 76996599, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if (u'direction' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'direction') and not mapcss.regexp_test_(self.re_63a07204, mapcss._tag_capture(capture_tags, 1, tags, u'direction')))):
            # throwWarning:tr("unusual value of {0}","{1.key}")
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
            err.append({'class': 9006010, 'subclass': 1961301012, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if (u'ele' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(self.re_762a1d1d, mapcss._tag_capture(capture_tags, 1, tags, u'ele')))):
            # set.ele_is_fixable
            # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
            # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
            # assertMatch:"node ele=-12.1 m"
            # assertMatch:"node ele=12 m"
            # assertNoMatch:"node ele=12"
            # assertMatch:"node ele=12.1m"
            # assertNoMatch:"node ele=12km"
            # assertMatch:"node ele=12m"
            # assertNoMatch:"node ele=high"
            set_ele_is_fixable = True
            err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, u'ele'), u'm', u'')))).split('=', 1)])
            }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_is_fixable
        if (u'ele' in keys) and \
            ((not set_ele_is_fixable and mapcss._tag_capture(capture_tags, 0, tags, u'ele') and not mapcss.regexp_test_(self.re_45b46d60, mapcss._tag_capture(capture_tags, 1, tags, u'ele')))):
            # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
            # assertNoMatch:"node ele=-12.1 m"
            # assertNoMatch:"node ele=12 m"
            # assertNoMatch:"node ele=12"
            # assertNoMatch:"node ele=12.1m"
            # assertMatch:"node ele=12km"
            # assertNoMatch:"node ele=12m"
            # assertMatch:"node ele=high"
            err.append({'class': 9006011, 'subclass': 1575083251, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', capture_tags, u'{0.key}')})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_ele_is_fixable = False

        # *[/^[0-9]+$/]
        if ((mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3))):
            # throwWarning:tr("numerical key")
            # assertMatch:"way 123=foo"
            # assertNoMatch:"way ref.1=foo"
            err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr(u'numerical key', capture_tags)})

        # *[layer=~/^\+\d/]
        if (u'layer' in keys) and \
            ((mapcss.regexp_test_(self.re_288e587a, mapcss._tag_capture(capture_tags, 0, tags, u'layer')))):
            # throwWarning:tr("{0} value with + sign","{0.key}")
            # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
            err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr(u'{0} value with + sign', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'layer=', mapcss.replace(mapcss.tag(tags, u'layer'), u'+', u''))).split('=', 1)])
            }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if (u'layer' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss.regexp_test_(self.re_0b0f0f56, mapcss._tag_capture(capture_tags, 1, tags, u'layer')))):
            # throwWarning:tr("{0} should be an integer value between -5 and 5","{0.key}")
            err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr(u'{0} should be an integer value between -5 and 5', capture_tags, u'{0.key}')})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if (u'building:levels' in keys or u'level' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss.regexp_test_(self.re_2a784076, mapcss._tag_capture(capture_tags, 1, tags, u'building:levels'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'level') and not mapcss.regexp_test_(self.re_7f19b94b, mapcss._tag_capture(capture_tags, 1, tags, u'level')))):
            # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
            err.append({'class': 9006004, 'subclass': 1004173499, 'text': mapcss.tr(u'{0} should have numbers only with optional .5 increments', capture_tags, u'{0.key}')})

        # *[height][height!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]
        if (u'height' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'height') and not mapcss.regexp_test_(self.re_597f003d, mapcss._tag_capture(capture_tags, 1, tags, u'height')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","height")
            err.append({'class': 9006005, 'subclass': 1885029007, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'height')})

        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default)$/]
        if (u'maxheight' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and not mapcss.regexp_test_(self.re_768a3762, mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","maxheight")
            err.append({'class': 9006005, 'subclass': 1339141103, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'maxheight')})

        # way[width][width!~/^(([0-9]+\.?[0-9]*( [a-z]+)?)|([0-9]+\'([0-9]+\.?[0-9]*\")?))$/]
        if (u'width' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'width') and not mapcss.regexp_test_(self.re_49888e30, mapcss._tag_capture(capture_tags, 1, tags, u'width')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","width")
            # assertNoMatch:"way width=1'"
            # assertMatch:"way width=-5"
            # assertNoMatch:"way width=0.5"
            # assertNoMatch:"way width=1 m"
            # assertNoMatch:"way width=10 ft"
            # assertNoMatch:"way width=10'5\""
            # assertNoMatch:"way width=3"
            # assertMatch:"way width=something"
            err.append({'class': 9006005, 'subclass': 1430721814, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'width')})

        # *[maxwidth][maxwidth!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'maxwidth' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and not mapcss.regexp_test_(self.re_1d428b19, mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","maxwidth")
            # assertMatch:"way maxwidth=-5"
            # assertNoMatch:"way maxwidth=2"
            # assertNoMatch:"way maxwidth=2.5"
            # assertNoMatch:"way maxwidth=6'6\""
            # assertNoMatch:"way maxwidth=7 ft"
            # assertMatch:"way maxwidth=something"
            err.append({'class': 9006005, 'subclass': 873145686, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'maxwidth')})

        # *[maxweight][maxweight!~/^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'maxweight' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and not mapcss.regexp_test_(self.re_035d45f0, mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))):
            # throwWarning:tr("{0}: tonne is default; period is separator; if units, put space then unit","maxweight")
            # assertMatch:"way maxweight=-5"
            # assertNoMatch:"way maxweight=2"
            # assertNoMatch:"way maxweight=2.5"
            # assertNoMatch:"way maxweight=6'6\""
            # assertNoMatch:"way maxweight=7 kg"
            # assertMatch:"way maxweight=something"
            err.append({'class': 9006006, 'subclass': 1776650332, 'text': mapcss.tr(u'{0}: tonne is default; period is separator; if units, put space then unit', capture_tags, u'maxweight')})

        # way[maxspeed][maxspeed!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        # way[maxspeed:forward][maxspeed:forward!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        # way[maxspeed:backward][maxspeed:backward!~/^(signals|none|unposted|variable|walk|[1-9][0-9]*( [a-z]+)?|[A-Z][A-Z]:(urban|rural|living_street|motorway))$/]
        if (u'maxspeed' in keys or u'maxspeed:backward' in keys or u'maxspeed:forward' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and not mapcss.regexp_test_(self.re_0ae2edfd, mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:forward') and not mapcss.regexp_test_(self.re_0ae2edfd, mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:forward'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:backward') and not mapcss.regexp_test_(self.re_0ae2edfd, mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:backward')))):
            # throwWarning:tr("unusual {0} format","maxspeed")
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
            err.append({'class': 9006012, 'subclass': 683878293, 'text': mapcss.tr(u'unusual {0} format', capture_tags, u'maxspeed')})

        # *[distance][distance!~/^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'distance' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'distance') and not mapcss.regexp_test_(self.re_4b9c2b6a, mapcss._tag_capture(capture_tags, 1, tags, u'distance')))):
            # throwWarning:tr("{0}: kilometers is default; period is separator; if units, put space then unit","distance")
            # assertMatch:"way distance=-5"
            # assertNoMatch:"way distance=2"
            # assertNoMatch:"way distance=2.5"
            # assertNoMatch:"way distance=7 mi"
            # assertMatch:"way distance=something"
            err.append({'class': 9006007, 'subclass': 131693430, 'text': mapcss.tr(u'{0}: kilometers is default; period is separator; if units, put space then unit', capture_tags, u'distance')})

        # way[voltage][voltage=~/(.*[A-Za-z].*)|.*,.*|.*( ).*/]
        if (u'voltage' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'voltage') and mapcss.regexp_test_(self.re_43c55ce5, mapcss._tag_capture(capture_tags, 1, tags, u'voltage')))):
            # throwWarning:tr("voltage should be in volts with no units/delimiter/spaces")
            # assertNoMatch:"way voltage=15000"
            # assertMatch:"way voltage=medium"
            err.append({'class': 9006013, 'subclass': 300093258, 'text': mapcss.tr(u'voltage should be in volts with no units/delimiter/spaces', capture_tags)})

        # way[frequency][frequency!~/^(0|[1-9][0-9]*(\.[0-9]+)?)( (kHz|MHz|GHz|THz))?$/]
        if (u'frequency' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'frequency') and not mapcss.regexp_test_(self.re_4d44d8e0, mapcss._tag_capture(capture_tags, 1, tags, u'frequency')))):
            # throwWarning:tr("unusual {0} specification","frequency")
            # assertNoMatch:"way frequency=0"
            # assertNoMatch:"way frequency=123.5 MHz"
            # assertNoMatch:"way frequency=16.7"
            # assertNoMatch:"way frequency=50"
            # assertNoMatch:"way frequency=680 kHz"
            # assertMatch:"way frequency=something"
            err.append({'class': 9006014, 'subclass': 582321238, 'text': mapcss.tr(u'unusual {0} specification', capture_tags, u'frequency')})

        # way[gauge][gauge!~/^([1-9][0-9]{1,3}(;[1-9][0-9]{1,3})*|broad|standard|narrow)$/]
        if (u'gauge' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'gauge') and not mapcss.regexp_test_(self.re_4e26566a, mapcss._tag_capture(capture_tags, 1, tags, u'gauge')))):
            # throwWarning:tr("unusual train track gauge; use mm with no separator")
            # assertNoMatch:"way gauge=1000;1435"
            # assertNoMatch:"way gauge=1435"
            # assertNoMatch:"way gauge=narrow"
            # assertMatch:"way gauge=something"
            # assertNoMatch:"way gauge=standard"
            err.append({'class': 9006015, 'subclass': 415876153, 'text': mapcss.tr(u'unusual train track gauge; use mm with no separator', capture_tags)})

        # way[incline][incline!~/^(up|down|-?([0-9]+?(\.[1-9]%)?|100)[%°]?)$/]
        if (u'incline' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'incline') and not mapcss.regexp_test_(self.re_45e73e1b, mapcss._tag_capture(capture_tags, 1, tags, u'incline')))):
            # throwWarning:tr("unusual incline; use percentages/degrees or up/down")
            # assertNoMatch:"way incline=-5%"
            # assertNoMatch:"way incline=10%"
            # assertNoMatch:"way incline=10°"
            # assertNoMatch:"way incline=down"
            # assertMatch:"way incline=extreme"
            # assertNoMatch:"way incline=up"
            err.append({'class': 9006016, 'subclass': 901779967, 'text': mapcss.tr(u'unusual incline; use percentages/degrees or up/down', capture_tags)})

        # *[population][population!~/^[0-9]+$/]
        if (u'population' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'population') and not mapcss.regexp_test_(self.re_066203d3, mapcss._tag_capture(capture_tags, 1, tags, u'population')))):
            # throwWarning:tr("{0} must be a numeric value","{0.key}")
            err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr(u'{0} must be a numeric value', capture_tags, u'{0.key}')})

        # way[lanes][lanes!~/^[1-9]([0-9]*)$/][highway]
        # way["lanes:backward"]["lanes:backward"!~/^[1-9]([0-9]*)$/][highway]
        # way["lanes:forward"]["lanes:forward"!~/^[1-9]([0-9]*)$/][highway]
        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if (u'lanes' in keys or u'lanes:backward' in keys or u'lanes:forward' in keys or u'screen' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'lanes') and not mapcss.regexp_test_(self.re_5478d8af, mapcss._tag_capture(capture_tags, 1, tags, u'lanes')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'lanes:backward') and not mapcss.regexp_test_(self.re_5478d8af, mapcss._tag_capture(capture_tags, 1, tags, u'lanes:backward')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'lanes:forward') and not mapcss.regexp_test_(self.re_5478d8af, mapcss._tag_capture(capture_tags, 1, tags, u'lanes:forward')) and mapcss._tag_capture(capture_tags, 2, tags, u'highway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'screen') and not mapcss.regexp_test_(self.re_5478d8af, mapcss._tag_capture(capture_tags, 1, tags, u'screen')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == u'cinema')):
            # throwError:tr("{0} must be a positive integer number","{0.key}")
            # assertMatch:"way highway=residential lanes:backward=-1"
            # assertMatch:"way highway=residential lanes:forward=-1"
            # assertMatch:"way highway=residential lanes=-1"
            # assertNoMatch:"way highway=residential lanes=1"
            # assertMatch:"way highway=residential lanes=1;2"
            # assertMatch:"way highway=residential lanes=5.5"
            err.append({'class': 9006009, 'subclass': 10320184, 'text': mapcss.tr(u'{0} must be a positive integer number', capture_tags, u'{0.key}')})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if (u'admin_level' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss.regexp_test_(self.re_7f163374, mapcss._tag_capture(capture_tags, 1, tags, u'admin_level')))):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        if (u'direction' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') < 0) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') >= 360)):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            err.append({'class': 9006010, 'subclass': 76996599, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if (u'direction' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'direction') and not mapcss.regexp_test_(self.re_63a07204, mapcss._tag_capture(capture_tags, 1, tags, u'direction')))):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            err.append({'class': 9006010, 'subclass': 1961301012, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if (u'ele' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(self.re_762a1d1d, mapcss._tag_capture(capture_tags, 1, tags, u'ele')))):
            # set.ele_is_fixable
            # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
            # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
            set_ele_is_fixable = True
            err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, u'ele'), u'm', u'')))).split('=', 1)])
            }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_is_fixable
        if (u'ele' in keys) and \
            ((not set_ele_is_fixable and mapcss._tag_capture(capture_tags, 0, tags, u'ele') and not mapcss.regexp_test_(self.re_45b46d60, mapcss._tag_capture(capture_tags, 1, tags, u'ele')))):
            # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
            err.append({'class': 9006011, 'subclass': 1575083251, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', capture_tags, u'{0.key}')})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_ele_is_fixable = False

        # *[/^[0-9]+$/]
        if ((mapcss._tag_capture(capture_tags, 0, tags, self.re_066203d3))):
            # throwWarning:tr("numerical key")
            err.append({'class': 9006001, 'subclass': 750700308, 'text': mapcss.tr(u'numerical key', capture_tags)})

        # *[layer=~/^\+\d/]
        if (u'layer' in keys) and \
            ((mapcss.regexp_test_(self.re_288e587a, mapcss._tag_capture(capture_tags, 0, tags, u'layer')))):
            # throwWarning:tr("{0} value with + sign","{0.key}")
            # fixAdd:concat("layer=",replace(tag("layer"),"+",""))
            err.append({'class': 9006002, 'subclass': 873121454, 'text': mapcss.tr(u'{0} value with + sign', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'layer=', mapcss.replace(mapcss.tag(tags, u'layer'), u'+', u''))).split('=', 1)])
            }})

        # *[layer][layer!~/^0$|^(-|\+)?[1-5]$/]
        if (u'layer' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss.regexp_test_(self.re_0b0f0f56, mapcss._tag_capture(capture_tags, 1, tags, u'layer')))):
            # throwWarning:tr("{0} should be an integer value between -5 and 5","{0.key}")
            err.append({'class': 9006003, 'subclass': 1089386010, 'text': mapcss.tr(u'{0} should be an integer value between -5 and 5', capture_tags, u'{0.key}')})

        # *[building:levels][building:levels!~/^(([0-9]|[1-9][0-9]*)(\.5)?)$/]
        # *[level][level!~/^((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5)(;((((-*[1-9]|[0-9])|-*[1-9][0-9]*)(\.5)?)|-0\.5))*$/]
        if (u'building:levels' in keys or u'level' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss.regexp_test_(self.re_2a784076, mapcss._tag_capture(capture_tags, 1, tags, u'building:levels'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'level') and not mapcss.regexp_test_(self.re_7f19b94b, mapcss._tag_capture(capture_tags, 1, tags, u'level')))):
            # throwWarning:tr("{0} should have numbers only with optional .5 increments","{0.key}")
            err.append({'class': 9006004, 'subclass': 1004173499, 'text': mapcss.tr(u'{0} should have numbers only with optional .5 increments', capture_tags, u'{0.key}')})

        # *[height][height!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([1-9][0-9]*\'((10|11|[0-9])((\.[0-9]+)?)\")?))$/]
        if (u'height' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'height') and not mapcss.regexp_test_(self.re_597f003d, mapcss._tag_capture(capture_tags, 1, tags, u'height')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","height")
            err.append({'class': 9006005, 'subclass': 1885029007, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'height')})

        # *[maxheight][maxheight!~/^(([1-9][0-9]*(\.[0-9]+)?( (m|ft))?)|([0-9]+\'(([0-9]|10|11)(\.[0-9]*)?\")?)|none|default)$/]
        if (u'maxheight' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and not mapcss.regexp_test_(self.re_768a3762, mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","maxheight")
            err.append({'class': 9006005, 'subclass': 1339141103, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'maxheight')})

        # *[maxwidth][maxwidth!~/^(([0-9]+\.?[0-9]*( (m|ft))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'maxwidth' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxwidth') and not mapcss.regexp_test_(self.re_1d428b19, mapcss._tag_capture(capture_tags, 1, tags, u'maxwidth')))):
            # throwWarning:tr("{0}: meters is default; period is separator; if units, put space then unit","maxwidth")
            err.append({'class': 9006005, 'subclass': 873145686, 'text': mapcss.tr(u'{0}: meters is default; period is separator; if units, put space then unit', capture_tags, u'maxwidth')})

        # *[maxweight][maxweight!~/^(([0-9]+\.?[0-9]*( (t|kg|lbs))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'maxweight' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxweight') and not mapcss.regexp_test_(self.re_035d45f0, mapcss._tag_capture(capture_tags, 1, tags, u'maxweight')))):
            # throwWarning:tr("{0}: tonne is default; period is separator; if units, put space then unit","maxweight")
            err.append({'class': 9006006, 'subclass': 1776650332, 'text': mapcss.tr(u'{0}: tonne is default; period is separator; if units, put space then unit', capture_tags, u'maxweight')})

        # *[distance][distance!~/^(([0-9]+\.?[0-9]*( (m|km|mi|nmi))?)|([0-9]+\'[0-9]+\.?[0-9]*\"))$/]
        if (u'distance' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'distance') and not mapcss.regexp_test_(self.re_4b9c2b6a, mapcss._tag_capture(capture_tags, 1, tags, u'distance')))):
            # throwWarning:tr("{0}: kilometers is default; period is separator; if units, put space then unit","distance")
            err.append({'class': 9006007, 'subclass': 131693430, 'text': mapcss.tr(u'{0}: kilometers is default; period is separator; if units, put space then unit', capture_tags, u'distance')})

        # *[population][population!~/^[0-9]+$/]
        if (u'population' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'population') and not mapcss.regexp_test_(self.re_066203d3, mapcss._tag_capture(capture_tags, 1, tags, u'population')))):
            # throwWarning:tr("{0} must be a numeric value","{0.key}")
            err.append({'class': 9006008, 'subclass': 313743521, 'text': mapcss.tr(u'{0} must be a numeric value', capture_tags, u'{0.key}')})

        # *[screen][screen!~/^[1-9]([0-9]*)$/][amenity=cinema]
        if (u'screen' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'screen') and not mapcss.regexp_test_(self.re_5478d8af, mapcss._tag_capture(capture_tags, 1, tags, u'screen')) and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') == u'cinema')):
            # throwError:tr("{0} must be a positive integer number","{0.key}")
            err.append({'class': 9006009, 'subclass': 1499065449, 'text': mapcss.tr(u'{0} must be a positive integer number', capture_tags, u'{0.key}')})

        # *[admin_level][admin_level!~/^(1|2|3|4|5|6|7|8|9|10|11|12)$/]
        if (u'admin_level' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss.regexp_test_(self.re_7f163374, mapcss._tag_capture(capture_tags, 1, tags, u'admin_level')))):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            err.append({'class': 9006010, 'subclass': 1514270237, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[direction][direction<0]
        # *[direction][direction>=360]
        if (u'direction' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') < 0) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'direction') and mapcss._tag_capture(capture_tags, 1, tags, u'direction') >= 360)):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            err.append({'class': 9006010, 'subclass': 76996599, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[direction][direction!~/^([0-9][0-9]?[0-9]?|north|east|south|west|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW|forward|backward|both|clockwise|anti-clockwise|anticlockwise|up|down)(-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))?(;([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW)-([0-9][0-9]?[0-9]?|N|E|S|W|NE|SE|SW|NW|NNE|ENE|ESE|SSE|SSW|WSW|WNW|NNW))*$/]
        if (u'direction' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'direction') and not mapcss.regexp_test_(self.re_63a07204, mapcss._tag_capture(capture_tags, 1, tags, u'direction')))):
            # throwWarning:tr("unusual value of {0}","{1.key}")
            err.append({'class': 9006010, 'subclass': 1961301012, 'text': mapcss.tr(u'unusual value of {0}', capture_tags, u'{1.key}')})

        # *[ele][ele=~/^-?[0-9]+(\.[0-9]+)? ?m$/]
        if (u'ele' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'ele') and mapcss.regexp_test_(self.re_762a1d1d, mapcss._tag_capture(capture_tags, 1, tags, u'ele')))):
            # set.ele_is_fixable
            # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
            # fixAdd:concat("ele=",trim(replace(tag("ele"),"m","")))
            set_ele_is_fixable = True
            err.append({'class': 9006011, 'subclass': 1672584043, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'ele=', mapcss.trim(mapcss.replace(mapcss.tag(tags, u'ele'), u'm', u'')))).split('=', 1)])
            }})

        # *[ele][ele!~/^-?[0-9]+(\.[0-9]+)?$/]!.ele_is_fixable
        if (u'ele' in keys) and \
            ((not set_ele_is_fixable and mapcss._tag_capture(capture_tags, 0, tags, u'ele') and not mapcss.regexp_test_(self.re_45b46d60, mapcss._tag_capture(capture_tags, 1, tags, u'ele')))):
            # throwWarning:tr("{0} must be a numeric value, in meters and without units","{0.key}")
            err.append({'class': 9006011, 'subclass': 1575083251, 'text': mapcss.tr(u'{0} must be a numeric value, in meters and without units', capture_tags, u'{0.key}')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_numeric(None)
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
        self.check_not_err(n.node(data, {u'height': u'22\''}), expected={'class': 9006005, 'subclass': 1885029007})
        self.check_err(n.node(data, {u'height': u'-5'}), expected={'class': 9006005, 'subclass': 1885029007})
        self.check_not_err(n.node(data, {u'height': u'2 m'}), expected={'class': 9006005, 'subclass': 1885029007})
        self.check_not_err(n.node(data, {u'height': u'20 ft'}), expected={'class': 9006005, 'subclass': 1885029007})
        self.check_not_err(n.node(data, {u'height': u'5'}), expected={'class': 9006005, 'subclass': 1885029007})
        self.check_not_err(n.node(data, {u'height': u'7.8'}), expected={'class': 9006005, 'subclass': 1885029007})
        self.check_err(n.node(data, {u'height': u'medium'}), expected={'class': 9006005, 'subclass': 1885029007})
        self.check_not_err(n.node(data, {u'maxheight': u'10\''}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_err(n.node(data, {u'maxheight': u'-5'}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_err(n.node(data, {u'maxheight': u'0'}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_not_err(n.node(data, {u'maxheight': u'14 ft'}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_not_err(n.node(data, {u'maxheight': u'16\'3"'}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_not_err(n.node(data, {u'maxheight': u'2 m'}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_not_err(n.node(data, {u'maxheight': u'3.5'}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_not_err(n.node(data, {u'maxheight': u'4'}), expected={'class': 9006005, 'subclass': 1339141103})
        self.check_err(n.node(data, {u'maxheight': u'something'}), expected={'class': 9006005, 'subclass': 1339141103})
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
        self.check_not_err(n.node(data, {u'ele': u'-12.1 m'}), expected={'class': 9006011, 'subclass': 1575083251})
        self.check_not_err(n.node(data, {u'ele': u'12 m'}), expected={'class': 9006011, 'subclass': 1575083251})
        self.check_not_err(n.node(data, {u'ele': u'12'}), expected={'class': 9006011, 'subclass': 1575083251})
        self.check_not_err(n.node(data, {u'ele': u'12.1m'}), expected={'class': 9006011, 'subclass': 1575083251})
        self.check_err(n.node(data, {u'ele': u'12km'}), expected={'class': 9006011, 'subclass': 1575083251})
        self.check_not_err(n.node(data, {u'ele': u'12m'}), expected={'class': 9006011, 'subclass': 1575083251})
        self.check_err(n.node(data, {u'ele': u'high'}), expected={'class': 9006011, 'subclass': 1575083251})
        self.check_err(n.way(data, {u'123': u'foo'}), expected={'class': 9006001, 'subclass': 750700308})
        self.check_not_err(n.way(data, {u'ref.1': u'foo'}), expected={'class': 9006001, 'subclass': 750700308})
        self.check_not_err(n.way(data, {u'width': u'1\''}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_err(n.way(data, {u'width': u'-5'}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_not_err(n.way(data, {u'width': u'0.5'}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_not_err(n.way(data, {u'width': u'1 m'}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_not_err(n.way(data, {u'width': u'10 ft'}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_not_err(n.way(data, {u'width': u'10\'5"'}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_not_err(n.way(data, {u'width': u'3'}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_err(n.way(data, {u'width': u'something'}), expected={'class': 9006005, 'subclass': 1430721814})
        self.check_err(n.way(data, {u'maxwidth': u'-5'}), expected={'class': 9006005, 'subclass': 873145686})
        self.check_not_err(n.way(data, {u'maxwidth': u'2'}), expected={'class': 9006005, 'subclass': 873145686})
        self.check_not_err(n.way(data, {u'maxwidth': u'2.5'}), expected={'class': 9006005, 'subclass': 873145686})
        self.check_not_err(n.way(data, {u'maxwidth': u'6\'6"'}), expected={'class': 9006005, 'subclass': 873145686})
        self.check_not_err(n.way(data, {u'maxwidth': u'7 ft'}), expected={'class': 9006005, 'subclass': 873145686})
        self.check_err(n.way(data, {u'maxwidth': u'something'}), expected={'class': 9006005, 'subclass': 873145686})
        self.check_err(n.way(data, {u'maxweight': u'-5'}), expected={'class': 9006006, 'subclass': 1776650332})
        self.check_not_err(n.way(data, {u'maxweight': u'2'}), expected={'class': 9006006, 'subclass': 1776650332})
        self.check_not_err(n.way(data, {u'maxweight': u'2.5'}), expected={'class': 9006006, 'subclass': 1776650332})
        self.check_not_err(n.way(data, {u'maxweight': u'6\'6"'}), expected={'class': 9006006, 'subclass': 1776650332})
        self.check_not_err(n.way(data, {u'maxweight': u'7 kg'}), expected={'class': 9006006, 'subclass': 1776650332})
        self.check_err(n.way(data, {u'maxweight': u'something'}), expected={'class': 9006006, 'subclass': 1776650332})
        self.check_err(n.way(data, {u'maxspeed': u'-50'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_err(n.way(data, {u'maxspeed': u'0'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'30 mph'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'50'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'DE:motorway'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'RO:urban'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'RU:living_street'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'RU:rural'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'none'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'signals'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_err(n.way(data, {u'maxspeed': u'something'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_not_err(n.way(data, {u'maxspeed': u'variable'}), expected={'class': 9006012, 'subclass': 683878293})
        self.check_err(n.way(data, {u'distance': u'-5'}), expected={'class': 9006007, 'subclass': 131693430})
        self.check_not_err(n.way(data, {u'distance': u'2'}), expected={'class': 9006007, 'subclass': 131693430})
        self.check_not_err(n.way(data, {u'distance': u'2.5'}), expected={'class': 9006007, 'subclass': 131693430})
        self.check_not_err(n.way(data, {u'distance': u'7 mi'}), expected={'class': 9006007, 'subclass': 131693430})
        self.check_err(n.way(data, {u'distance': u'something'}), expected={'class': 9006007, 'subclass': 131693430})
        self.check_not_err(n.way(data, {u'voltage': u'15000'}), expected={'class': 9006013, 'subclass': 300093258})
        self.check_err(n.way(data, {u'voltage': u'medium'}), expected={'class': 9006013, 'subclass': 300093258})
        self.check_not_err(n.way(data, {u'frequency': u'0'}), expected={'class': 9006014, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'123.5 MHz'}), expected={'class': 9006014, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'16.7'}), expected={'class': 9006014, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'50'}), expected={'class': 9006014, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'frequency': u'680 kHz'}), expected={'class': 9006014, 'subclass': 582321238})
        self.check_err(n.way(data, {u'frequency': u'something'}), expected={'class': 9006014, 'subclass': 582321238})
        self.check_not_err(n.way(data, {u'gauge': u'1000;1435'}), expected={'class': 9006015, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'gauge': u'1435'}), expected={'class': 9006015, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'gauge': u'narrow'}), expected={'class': 9006015, 'subclass': 415876153})
        self.check_err(n.way(data, {u'gauge': u'something'}), expected={'class': 9006015, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'gauge': u'standard'}), expected={'class': 9006015, 'subclass': 415876153})
        self.check_not_err(n.way(data, {u'incline': u'-5%'}), expected={'class': 9006016, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'10%'}), expected={'class': 9006016, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'10°'}), expected={'class': 9006016, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'down'}), expected={'class': 9006016, 'subclass': 901779967})
        self.check_err(n.way(data, {u'incline': u'extreme'}), expected={'class': 9006016, 'subclass': 901779967})
        self.check_not_err(n.way(data, {u'incline': u'up'}), expected={'class': 9006016, 'subclass': 901779967})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes:backward': u'-1'}), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes:forward': u'-1'}), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes': u'-1'}), expected={'class': 9006009, 'subclass': 10320184})
        self.check_not_err(n.way(data, {u'highway': u'residential', u'lanes': u'1'}), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes': u'1;2'}), expected={'class': 9006009, 'subclass': 10320184})
        self.check_err(n.way(data, {u'highway': u'residential', u'lanes': u'5.5'}), expected={'class': 9006009, 'subclass': 10320184})
