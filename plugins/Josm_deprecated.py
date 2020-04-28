#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_deprecated(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/deprecated.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9002001] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'deprecated tagging'))
        self.errors[9002002] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', u'access=designated', u'bicycle=designated'))
        self.errors[9002003] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', u'access=official', u'bicycle=official'))
        self.errors[9002004] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}')))
        self.errors[9002005] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')))
        self.errors[9002006] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, u'{0.tag}')))
        self.errors[9002007] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}')))
        self.errors[9002008] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')))
        self.errors[9002009] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0} = {1}; remove {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}')))
        self.errors[9002010] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'Unspecific tag {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')))
        self.errors[9002011] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'key with uncommon character'))
        self.errors[9002012] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'uncommon short key'))
        self.errors[9002013] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:bitcoin=yes', u'payment:litecoin=yes'))
        self.errors[9002014] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'questionable key (ending with a number)'))
        self.errors[9002015] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0}={1} is unspecific. Please replace \'\'{1}\'\' by \'\'left\'\', \'\'right\'\' or \'\'both\'\'.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}')))
        self.errors[9002016] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'{0} is not recommended. Use the Reverse Ways function from the Tools menu.', mapcss._tag_uncapture(capture_tags, u'{0.tag}')))
        self.errors[9002017] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, u'{1.key}')))
        self.errors[9002018] = self.def_class(item = 9002, level = 2, tags = ["tag", "deprecated"], title = mapcss.tr(u'misspelled value'))
        self.errors[9002019] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'wrong value: {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')))
        self.errors[9002020] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}')))

        self.re_01eb1711 = re.compile(r'^(yes|both|no)$')
        self.re_047d5648 = re.compile(r'^(1|2|3|4|5|grade1|grade2|grade3|grade4|grade5)$')
        self.re_0c5b5730 = re.compile(r'color:')
        self.re_0f294fdf = re.compile(r'^[1-9][0-9]*$')
        self.re_1f92073a = re.compile(r'^(?i)fixme$')
        self.re_27210286 = re.compile(r'^.$')
        self.re_2fd4cdcf = re.compile(r'^(crossover|siding|spur|yard)$')
        self.re_300dfa36 = re.compile(r'^[^t][^i][^g].+_[0-9]$')
        self.re_3185ac6d = re.compile(r'^note_[0-9]$')
        self.re_34c15d62 = re.compile(r'^..$')
        self.re_493fd1a6 = re.compile(r'^is_in:.*$')
        self.re_51df498f = re.compile(r'^(alley|drive-through|drive_through|driveway|emergency_access|parking_aisle|rest_area|slipway|yes)$')
        self.re_554de4c7 = re.compile(r':color')
        self.re_5ee0acf2 = re.compile(r'josm\/ignore')
        self.re_6029fe03 = re.compile(r'^diaper:')
        self.re_61b0be1b = re.compile(r'^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$')
        self.re_620f4d52 = re.compile(r'=|\+|\/|&|<|>|;|\'|\"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$')
        self.re_6d27b157 = re.compile(r'^description_[0-9]$')
        self.re_787405b1 = re.compile(r'^(yes|no|limited)$')
        self.re_7a045a17 = re.compile(r'^(irrigation|transportation|water_power)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_diaper___checked = set_diaper_checked = set_samecolor = False

        # *[barrier=wire_fence]
        if (u'barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wire_fence'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 1107799632, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'fence'],
                    [u'fence_type',u'chain_link']])
                }})

        # *[barrier=wood_fence]
        if (u'barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wood_fence'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=wood"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=wood"
                err.append({'class': 9002001, 'subclass': 1412230714, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'fence'],
                    [u'fence_type',u'wood']])
                }})

        # node[highway=ford]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'ford'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"ford=yes"
                # fixAdd:"ford=yes"
                # fixRemove:"highway"
                err.append({'class': 9002001, 'subclass': 1317841090, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'ford',u'yes']]),
                    '-': ([
                    u'highway'])
                }})

        # *[highway=stile]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stile'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=stile"
                # fixAdd:"barrier=stile"
                # fixRemove:"highway"
                err.append({'class': 9002001, 'subclass': 1435678043, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'stile']]),
                    '-': ([
                    u'highway'])
                }})

        # *[highway=incline]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'incline'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 765169083, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[highway=incline_steep]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'incline_steep'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 1966772390, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[highway=unsurfaced]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'unsurfaced'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"highway=* + surface=unpaved"
                # fixAdd:"highway=road"
                # fixAdd:"surface=unpaved"
                err.append({'class': 9002001, 'subclass': 20631498, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'highway',u'road'],
                    [u'surface',u'unpaved']])
                }})

        # *[landuse=wood]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'wood'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=forest"
                # suggestAlternative:"natural=wood"
                err.append({'class': 9002001, 'subclass': 469903103, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[natural=marsh]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'marsh'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=wetland + wetland=marsh"
                # fixAdd:"natural=wetland"
                # fixAdd:"wetland=marsh"
                err.append({'class': 9002001, 'subclass': 1459865523, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'natural',u'wetland'],
                    [u'wetland',u'marsh']])
                }})

        # *[highway=byway]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'byway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 1844620979, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power_source]
        if (u'power_source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power_source'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"generator:source"
                err.append({'class': 9002001, 'subclass': 34751027, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[power_rating]
        if (u'power_rating' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power_rating'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"generator:output"
                err.append({'class': 9002001, 'subclass': 904750343, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[shop=antique]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'antique'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=antiques"
                # fixAdd:"shop=antiques"
                err.append({'class': 9002001, 'subclass': 596668979, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'antiques']])
                }})

        # *[shop=bags]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'bags'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=bag"
                # fixAdd:"shop=bag"
                err.append({'class': 9002001, 'subclass': 1709003584, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'bag']])
                }})

        # *[shop=fashion]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fashion'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=clothes"
                # fixAdd:"shop=clothes"
                err.append({'class': 9002001, 'subclass': 985619804, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'clothes']])
                }})

        # *[shop=organic]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'organic'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=* + organic=only"
                # suggestAlternative:"shop=* + organic=yes"
                err.append({'class': 9002001, 'subclass': 1959365145, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=pets]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'pets'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet"
                # fixAdd:"shop=pet"
                err.append({'class': 9002001, 'subclass': 290270098, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'pet']])
                }})

        # *[shop=pharmacy]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'pharmacy'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=pharmacy"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 350722657, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'shop')]]),
                    '-': ([
                    u'shop'])
                }})

        # *[bicycle_parking=sheffield]
        if (u'bicycle_parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bicycle_parking') == mapcss._value_capture(capture_tags, 0, u'sheffield'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bicycle_parking=stands"
                # fixAdd:"bicycle_parking=stands"
                err.append({'class': 9002001, 'subclass': 718874663, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bicycle_parking',u'stands']])
                }})

        # *[amenity=emergency_phone]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'emergency_phone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"emergency=phone"
                # fixRemove:"amenity"
                # fixAdd:"emergency=phone"
                err.append({'class': 9002001, 'subclass': 1108230656, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'phone']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[sport=gaelic_football]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'gaelic_football'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=gaelic_games"
                # fixAdd:"sport=gaelic_games"
                err.append({'class': 9002001, 'subclass': 1768681881, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'gaelic_games']])
                }})

        # *[power=station]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=plant"
                # suggestAlternative:"power=substation"
                err.append({'class': 9002001, 'subclass': 52025933, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power=sub_station]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'sub_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=substation"
                # fixAdd:"power=substation"
                err.append({'class': 9002001, 'subclass': 1423074682, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'power',u'substation']])
                }})

        # *[location=rooftop]
        if (u'location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'location') == mapcss._value_capture(capture_tags, 0, u'rooftop'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location=roof"
                # fixAdd:"location=roof"
                err.append({'class': 9002001, 'subclass': 1028577225, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location',u'roof']])
                }})

        # *[generator:location]
        if (u'generator:location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:location'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"location"
                # fixChangeKey:"generator:location => location"
                err.append({'class': 9002001, 'subclass': 900615917, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location', mapcss.tag(tags, u'generator:location')]]),
                    '-': ([
                    u'generator:location'])
                }})

        # *[generator:method=dam]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'dam'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-storage"
                # fixAdd:"generator:method=water-storage"
                err.append({'class': 9002001, 'subclass': 248819368, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-storage']])
                }})

        # *[generator:method=pumped-storage]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'pumped-storage'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 93454158, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-pumped-storage']])
                }})

        # *[generator:method=pumping]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'pumping'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 2115673716, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-pumped-storage']])
                }})

        # *[fence_type=chain]
        if (u'fence_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fence_type') == mapcss._value_capture(capture_tags, 0, u'chain'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=chain"
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 19409288, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building=entrance]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'entrance'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"entrance"
                err.append({'class': 9002001, 'subclass': 306662985, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[board_type=board]
        if (u'board_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'board_type') == mapcss._value_capture(capture_tags, 0, u'board'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"board_type"
                err.append({'class': 9002001, 'subclass': 1150949316, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'board_type'])
                }})

        # *[man_made=measurement_station]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'measurement_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=monitoring_station"
                # fixAdd:"man_made=monitoring_station"
                err.append({'class': 9002001, 'subclass': 700465123, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'monitoring_station']])
                }})

        # *[measurement=water_level]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'water_level'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:water_level=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:water_level=yes"
                err.append({'class': 9002001, 'subclass': 634647702, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:water_level',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[measurement=weather]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'weather'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:weather=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:weather=yes"
                err.append({'class': 9002001, 'subclass': 336627227, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:weather',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[measurement=seismic]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'seismic'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:seismic_activity=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:seismic_activity=yes"
                err.append({'class': 9002001, 'subclass': 1402131289, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:seismic_activity',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[monitoring:river_level]
        if (u'monitoring:river_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'monitoring:river_level'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"monitoring:water_level"
                # fixChangeKey:"monitoring:river_level => monitoring:water_level"
                err.append({'class': 9002001, 'subclass': 264907924, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:water_level', mapcss.tag(tags, u'monitoring:river_level')]]),
                    '-': ([
                    u'monitoring:river_level'])
                }})

        # *[stay]
        if (u'stay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'stay'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"maxstay"
                # fixChangeKey:"stay => maxstay"
                err.append({'class': 9002001, 'subclass': 787370129, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'maxstay', mapcss.tag(tags, u'stay')]]),
                    '-': ([
                    u'stay'])
                }})

        # *[emergency=aed]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'aed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"emergency=defibrillator"
                # fixAdd:"emergency=defibrillator"
                err.append({'class': 9002001, 'subclass': 707111885, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'defibrillator']])
                }})

        # *[day_on][!restriction]
        # *[day_off][!restriction]
        # *[date_on][!restriction]
        # *[date_off][!restriction]
        # *[hour_on][!restriction]
        # *[hour_off][!restriction]
        if (u'date_off' in keys) or (u'date_on' in keys) or (u'day_off' in keys) or (u'day_on' in keys) or (u'hour_off' in keys) or (u'hour_on' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'day_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'day_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'date_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'date_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hour_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hour_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"*:conditional"
                # assertMatch:"node day_on=0-12"
                err.append({'class': 9002001, 'subclass': 294264920, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[access=designated]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'designated'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' is meaningless, use more specific tags, e.g. ''{1}''","access=designated","bicycle=designated")
                err.append({'class': 9002002, 'subclass': 2057594338, 'text': mapcss.tr(u'\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', u'access=designated', u'bicycle=designated')})

        # *[access=official]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'official'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' does not specify the official mode of transportation, use ''{1}'' for example","access=official","bicycle=official")
                err.append({'class': 9002003, 'subclass': 1909133836, 'text': mapcss.tr(u'\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', u'access=official', u'bicycle=official')})

        # *[fixme=yes]
        # *[FIXME=yes]
        if (u'FIXME' in keys) or (u'fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fixme') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'FIXME') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Instead of ''{1}'' please give more information about what exactly should be fixed.","{0.key}","{0.value}")
                err.append({'class': 9002004, 'subclass': 136657482, 'text': mapcss.tr(u'{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name][name=~/^(?i)fixme$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.","{0.key}","{0.tag}")
                # fixRemove:"name"
                # assertMatch:"node name=FIXME"
                # assertMatch:"node name=Fixme"
                # assertMatch:"node name=fixme"
                # assertNoMatch:"node name=valid name"
                err.append({'class': 9002005, 'subclass': 642340557, 'text': mapcss.tr(u'Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'name'])
                }})

        # *[note][note=~/^(?i)fixme$/]
        if (u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'note') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, u'note')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.","{0.tag}")
                err.append({'class': 9002006, 'subclass': 1243120287, 'text': mapcss.tr(u'{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[type=broad_leaved]
        # *[type=broad_leafed]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'broad_leaved'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'broad_leafed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=broadleaved"
                # fixAdd:"leaf_type=broadleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 293968062, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'broadleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[wood=coniferous]
        # *[type=coniferous]
        # *[type=conifer]
        if (u'type' in keys) or (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'coniferous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'coniferous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'conifer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=needleleaved"
                # fixAdd:"leaf_type=needleleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 50517650, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'needleleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[wood=mixed]
        if (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'mixed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=mixed"
                # fixAdd:"leaf_type=mixed"
                # fixRemove:"wood"
                err.append({'class': 9002001, 'subclass': 235914603, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'mixed']]),
                    '-': ([
                    u'wood'])
                }})

        # *[wood=evergreen]
        # *[type=evergreen]
        if (u'type' in keys) or (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'evergreen'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'evergreen'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=evergreen"
                # fixAdd:"leaf_cycle=evergreen"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 747964532, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_cycle',u'evergreen']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[type=deciduous]
        # *[type=deciduos]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'deciduous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'deciduos'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=deciduous"
                # fixAdd:"leaf_cycle=deciduous"
                # fixRemove:"type"
                err.append({'class': 9002001, 'subclass': 591116099, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_cycle',u'deciduous']]),
                    '-': ([
                    u'type'])
                }})

        # *[wood=deciduous]
        if (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'deciduous'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type + leaf_cycle"
                err.append({'class': 9002001, 'subclass': 1100223594, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[type=palm]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'palm'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type"
                # suggestAlternative:"species"
                # suggestAlternative:"trees"
                err.append({'class': 9002001, 'subclass': 1453672853, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[natural=land]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'land'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please use instead a multipolygon.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 94558529, 'text': mapcss.tr(u'{0} is deprecated. Please use instead a multipolygon.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=causeway]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'causeway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=low_water_crossing"
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"ford=yes"
                err.append({'class': 9002001, 'subclass': 461671124, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=swing]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'swing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge:movable=swing"
                # suggestAlternative:"bridge:structure=simple-suspension"
                err.append({'class': 9002001, 'subclass': 1047428067, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=suspension]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'suspension'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=yes + bridge:structure=suspension"
                # fixAdd:"bridge:structure=suspension"
                # fixAdd:"bridge=yes"
                err.append({'class': 9002001, 'subclass': 1157046268, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:structure',u'suspension'],
                    [u'bridge',u'yes']])
                }})

        # *[bridge=pontoon]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'pontoon'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=yes + bridge:structure=floating"
                # fixAdd:"bridge:structure=floating"
                # fixAdd:"bridge=yes"
                err.append({'class': 9002001, 'subclass': 1195531951, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:structure',u'floating'],
                    [u'bridge',u'yes']])
                }})

        # *[fee=interval]
        # *[lit=interval]
        # *[supervised=interval]
        if (u'fee' in keys) or (u'lit' in keys) or (u'supervised' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fee') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lit') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'supervised') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please specify interval by using opening_hours syntax","{0.tag}")
                err.append({'class': 9002001, 'subclass': 417886592, 'text': mapcss.tr(u'{0} is deprecated. Please specify interval by using opening_hours syntax', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[/josm\/ignore/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_5ee0acf2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwError:tr("{0} is deprecated. Please delete this object and use a private layer instead","{0.key}")
                # fixDeleteObject:this
                err.append({'class': 9002001, 'subclass': 1402743016, 'text': mapcss.tr(u'{0} is deprecated. Please delete this object and use a private layer instead', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[sport=diving]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'diving'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=cliff_diving"
                # suggestAlternative:"sport=scuba_diving"
                err.append({'class': 9002001, 'subclass': 590643159, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[parking=park_and_ride]
        if (u'parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'parking') == mapcss._value_capture(capture_tags, 0, u'park_and_ride'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + park_ride=yes"
                # fixAdd:"amenity=parking"
                # fixAdd:"park_ride=yes"
                # fixRemove:"parking"
                err.append({'class': 9002001, 'subclass': 1893516041, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'parking'],
                    [u'park_ride',u'yes']]),
                    '-': ([
                    u'parking'])
                }})

        # *[manhole=plain]
        # *[manhole=unknown]
        # *[manhole=yes]
        # *[police=yes]
        # *[traffic_calming=yes]
        # *[access=restricted]
        # *[barrier=yes]
        # *[aerialway=yes][!public_transport]
        # *[amenity=yes]
        # *[leisure=yes]
        # *[shop="*"]
        # *[shop=yes][amenity!=fuel]
        # *[craft=yes]
        # *[service=yes]
        # *[place=yes]
        if (u'access' in keys) or (u'aerialway' in keys) or (u'amenity' in keys) or (u'barrier' in keys) or (u'craft' in keys) or (u'leisure' in keys) or (u'manhole' in keys) or (u'place' in keys) or (u'police' in keys) or (u'service' in keys) or (u'shop' in keys) or (u'traffic_calming' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'plain'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'police') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'traffic_calming') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'restricted'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'yes') and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'*'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'fuel', u'fuel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'craft') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'service') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Please replace ''{1}'' by a specific value.","{0.key}","{0.value}")
                err.append({'class': 9002007, 'subclass': 1532935474, 'text': mapcss.tr(u'{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[place_name][!name]
        if (u'place_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be replaced with {1}","{0.key}","{1.key}")
                # fixChangeKey:"place_name => name"
                err.append({'class': 9002008, 'subclass': 1089331760, 'text': mapcss.tr(u'{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'name', mapcss.tag(tags, u'place_name')]]),
                    '-': ([
                    u'place_name'])
                }})

        # *[place][place_name=*name]
        if (u'place' in keys and u'place_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss._tag_capture(capture_tags, 1, tags, u'place_name') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} = {1}; remove {0}","{1.key}","{1.value}")
                # fixRemove:"{1.key}"
                err.append({'class': 9002009, 'subclass': 1116761280, 'text': mapcss.tr(u'{0} = {1}; remove {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # *[waterway=water_point]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'water_point'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=water_point"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 103347605, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'waterway')]]),
                    '-': ([
                    u'waterway'])
                }})

        # *[waterway=waste_disposal]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'waste_disposal'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_disposal"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 1963461348, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'waterway')]]),
                    '-': ([
                    u'waterway'])
                }})

        # *[waterway=mooring]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'mooring'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"mooring=yes"
                # fixAdd:"mooring=yes"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 81358738, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'mooring',u'yes']]),
                    '-': ([
                    u'waterway'])
                }})

        # *[building][levels]
        # *[building:part=yes][levels]
        if (u'building' in keys and u'levels' in keys) or (u'building:part' in keys and u'levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') and mapcss._tag_capture(capture_tags, 1, tags, u'levels'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:part') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'levels'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.key}")
                # suggestAlternative:"building:levels"
                # fixChangeKey:"levels => building:levels"
                err.append({'class': 9002001, 'subclass': 293177436, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building:levels', mapcss.tag(tags, u'levels')]]),
                    '-': ([
                    u'levels'])
                }})

        # *[protected_class]
        if (u'protected_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protected_class'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"protect_class"
                # fixChangeKey:"protected_class => protect_class"
                err.append({'class': 9002001, 'subclass': 716999373, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'protect_class', mapcss.tag(tags, u'protected_class')]]),
                    '-': ([
                    u'protected_class'])
                }})

        # *[kerb=unknown]
        # *[lock=unknown]
        # *[hide=unknown]
        # *[shelter=unknown]
        # *[access=unknown]
        # *[capacity:parent=unknown]
        # *[capacity:women=unknown]
        # *[capacity:disabled=unknown]
        # *[crossing=unknown]
        # *[foot=unknown]
        if (u'access' in keys) or (u'capacity:disabled' in keys) or (u'capacity:parent' in keys) or (u'capacity:women' in keys) or (u'crossing' in keys) or (u'foot' in keys) or (u'hide' in keys) or (u'kerb' in keys) or (u'lock' in keys) or (u'shelter' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kerb') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lock') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hide') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shelter') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:parent') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:women') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:disabled') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'foot') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unspecific tag {0}","{0.tag}")
                err.append({'class': 9002010, 'subclass': 1052866123, 'text': mapcss.tr(u'Unspecific tag {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=skiing]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'skiing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # suggestAlternative:tr("{0} + {1} + {2}","piste:type=*","piste:difficulty=*","piste:grooming=*")
                err.append({'class': 9002001, 'subclass': 1578959559, 'text': mapcss.tr(u'Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[waterway=wadi]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'wadi'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=valley"
                # suggestAlternative:"{0.key}=* + intermittent=yes"
                err.append({'class': 9002001, 'subclass': 719234223, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[drinkable]
        if (u'drinkable' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'drinkable'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"drinking_water"
                err.append({'class': 9002001, 'subclass': 1785584789, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[color][!colour]
        if (u'color' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'color') and not mapcss._tag_capture(capture_tags, 1, tags, u'colour'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour"
                # fixChangeKey:"color => colour"
                err.append({'class': 9002001, 'subclass': 1850270072, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'colour', mapcss.tag(tags, u'color')]]),
                    '-': ([
                    u'color'])
                }})

        # *[color][colour][color=*colour]
        if (u'color' in keys and u'colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'color') and mapcss._tag_capture(capture_tags, 1, tags, u'colour') and mapcss._tag_capture(capture_tags, 2, tags, u'color') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'colour')))
                except mapcss.RuleAbort: pass
            if match:
                # setsamecolor
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # suggestAlternative:"colour"
                # fixRemove:"color"
                set_samecolor = True
                err.append({'class': 9002001, 'subclass': 1825345743, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'color'])
                }})

        # *[color][colour]!.samecolor
        if (u'color' in keys and u'colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_samecolor and mapcss._tag_capture(capture_tags, 0, tags, u'color') and mapcss._tag_capture(capture_tags, 1, tags, u'colour'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                # suggestAlternative:"colour"
                err.append({'class': 9002001, 'subclass': 1064658218, 'text': mapcss.tr(u'{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[building:color][building:colour]!.samebuildingcolor
        # Use undeclared class samebuildingcolor

        # *[roof:color][roof:colour]!.sameroofcolor
        # Use undeclared class sameroofcolor

        # *[/:color/][!building:color][!roof:color][!gpxd:color]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_554de4c7) and not mapcss._tag_capture(capture_tags, 1, tags, u'building:color') and not mapcss._tag_capture(capture_tags, 2, tags, u'roof:color') and not mapcss._tag_capture(capture_tags, 3, tags, u'gpxd:color'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:":colour"
                err.append({'class': 9002001, 'subclass': 1632389707, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/color:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_0c5b5730))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour:"
                err.append({'class': 9002001, 'subclass': 1390370717, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/=|\+|\/|&|<|>|;|'|"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_620f4d52))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("key with uncommon character")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002011, 'subclass': 1752615188, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/^.$/]
        # node[/^..$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_27210286))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uncommon short key")
                # assertMatch:"node f=b"
                # assertMatch:"node fo=bar"
                err.append({'class': 9002012, 'subclass': 1803276827, 'text': mapcss.tr(u'uncommon short key')})

        # *[sport=hockey]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'hockey'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=field_hockey"
                # suggestAlternative:"sport=ice_hockey"
                err.append({'class': 9002001, 'subclass': 651933474, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=billard]
        # *[sport=billards]
        # *[sport=billiard]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billards'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billiard'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=billiards"
                # fixAdd:"sport=billiards"
                err.append({'class': 9002001, 'subclass': 1522897824, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'billiards']])
                }})

        # *[payment:credit_cards=yes]
        if (u'payment:credit_cards' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:credit_cards') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:mastercard=yes","payment:visa=yes")
                err.append({'class': 9002013, 'subclass': 705181097, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:mastercard=yes', u'payment:visa=yes')})

        # *[payment:debit_cards=yes]
        if (u'payment:debit_cards' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:debit_cards') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:maestro=yes","payment:girocard=yes")
                err.append({'class': 9002013, 'subclass': 679215558, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:maestro=yes', u'payment:girocard=yes')})

        # *[payment:electronic_purses=yes]
        if (u'payment:electronic_purses' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:electronic_purses') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:ep_geldkarte=yes","payment:ep_quick=yes")
                err.append({'class': 9002013, 'subclass': 1440457244, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:ep_geldkarte=yes', u'payment:ep_quick=yes')})

        # *[payment:cryptocurrencies=yes]
        if (u'payment:cryptocurrencies' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cryptocurrencies') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:bitcoin=yes","payment:litecoin=yes")
                err.append({'class': 9002013, 'subclass': 1325255949, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:bitcoin=yes', u'payment:litecoin=yes')})

        # *[payment:ep_quick]
        # *[payment:ep_cash]
        # *[payment:ep_proton]
        # *[payment:ep_chipknip]
        if (u'payment:ep_cash' in keys) or (u'payment:ep_chipknip' in keys) or (u'payment:ep_proton' in keys) or (u'payment:ep_quick' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_quick'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_cash'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_proton'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_chipknip'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 332575437, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[kp][highway=milestone]
        # *[kp][railway=milestone]
        # *[kp][waterway=milestone]
        if (u'highway' in keys and u'kp' in keys) or (u'kp' in keys and u'railway' in keys) or (u'kp' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"kp => distance"
                err.append({'class': 9002001, 'subclass': 1078799228, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'distance', mapcss.tag(tags, u'kp')]]),
                    '-': ([
                    u'kp'])
                }})

        # *[pk][highway=milestone]
        # *[pk][railway=milestone]
        # *[pk][waterway=milestone]
        if (u'highway' in keys and u'pk' in keys) or (u'pk' in keys and u'railway' in keys) or (u'pk' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"pk => distance"
                err.append({'class': 9002001, 'subclass': 719029418, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'distance', mapcss.tag(tags, u'pk')]]),
                    '-': ([
                    u'pk'])
                }})

        # *[postcode]
        if (u'postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'postcode'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"addr:postcode"
                # suggestAlternative:"postal_code"
                err.append({'class': 9002001, 'subclass': 1942523538, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[water=intermittent]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'intermittent'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"intermittent=yes"
                # fixAdd:"intermittent=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 813530321, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'intermittent',u'yes']]),
                    '-': ([
                    u'water'])
                }})

        # node[type][pipeline=marker]
        if (u'pipeline' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') and mapcss._tag_capture(capture_tags, 1, tags, u'pipeline') == mapcss._value_capture(capture_tags, 1, u'marker'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"substance"
                # fixChangeKey:"type => substance"
                err.append({'class': 9002001, 'subclass': 1878458659, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'substance', mapcss.tag(tags, u'type')]]),
                    '-': ([
                    u'type'])
                }})

        # *[landuse=farm]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'farm'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=farmland"
                # suggestAlternative:"landuse=farmyard"
                err.append({'class': 9002001, 'subclass': 1968473048, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[seamark=buoy]["seamark:type"=~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if (u'seamark' in keys and u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark') == mapcss._value_capture(capture_tags, 0, u'buoy') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_61b0be1b), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                # fixRemove:"seamark"
                err.append({'class': 9002001, 'subclass': 1224401740, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'seamark'])
                }})

        # *[seamark=buoy]["seamark:type"!~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if (u'seamark' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark') == mapcss._value_capture(capture_tags, 0, u'buoy') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61b0be1b, u'^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$'), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9002001, 'subclass': 1481035998, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[landuse=conservation]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'conservation'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"boundary=protected_area"
                # fixAdd:"boundary=protected_area"
                # fixRemove:"landuse"
                err.append({'class': 9002001, 'subclass': 824801072, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'boundary',u'protected_area']]),
                    '-': ([
                    u'landuse'])
                }})

        # *[amenity=kiosk]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'kiosk'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=kiosk"
                # fixChangeKey:"amenity => shop"
                err.append({'class': 9002001, 'subclass': 1331930630, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=shop]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'shop'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=*"
                err.append({'class': 9002001, 'subclass': 1562207150, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=fishmonger]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fishmonger'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=seafood"
                # fixAdd:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 1376789416, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'seafood']])
                }})

        # *[shop=fish]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fish'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=fishing"
                # suggestAlternative:"shop=pet"
                # suggestAlternative:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 47191734, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=betting]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'betting'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=adult_gaming_centre"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1035501389, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=perfume]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'perfume'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=perfumery"
                # fixAdd:"shop=perfumery"
                err.append({'class': 9002001, 'subclass': 2075099676, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'perfumery']])
                }})

        # *[amenity=exercise_point]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'exercise_point'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=fitness_station"
                # fixRemove:"amenity"
                # fixAdd:"leisure=fitness_station"
                err.append({'class': 9002001, 'subclass': 1514920202, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure',u'fitness_station']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[shop=auto_parts]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'auto_parts'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=car_parts"
                # fixAdd:"shop=car_parts"
                err.append({'class': 9002001, 'subclass': 1675828779, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'car_parts']])
                }})

        # *[amenity=car_repair]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'car_repair'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=car_repair"
                # fixChangeKey:"amenity => shop"
                err.append({'class': 9002001, 'subclass': 1681273585, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=studio][type=audio]
        # *[amenity=studio][type=radio]
        # *[amenity=studio][type=television]
        # *[amenity=studio][type=video]
        if (u'amenity' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'audio'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'radio'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'television'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'video'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"studio"
                # fixChangeKey:"type => studio"
                err.append({'class': 9002001, 'subclass': 413401822, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'studio', mapcss.tag(tags, u'type')]]),
                    '-': ([
                    u'type'])
                }})

        # *[power=cable_distribution_cabinet]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'cable_distribution_cabinet'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=street_cabinet + street_cabinet=*"
                # fixAdd:"man_made=street_cabinet"
                # fixRemove:"power"
                err.append({'class': 9002001, 'subclass': 1007567078, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'street_cabinet']]),
                    '-': ([
                    u'power'])
                }})

        # *[power][location=kiosk]
        if (u'location' in keys and u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') and mapcss._tag_capture(capture_tags, 1, tags, u'location') == mapcss._value_capture(capture_tags, 1, u'kiosk'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # fixRemove:"location"
                # fixAdd:"man_made=street_cabinet"
                # fixAdd:"street_cabinet=power"
                err.append({'class': 9002001, 'subclass': 182905067, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'street_cabinet'],
                    [u'street_cabinet',u'power']]),
                    '-': ([
                    u'location'])
                }})

        # *[man_made=well]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'well'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1740864107, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=dog_bin]
        # *[amenity=dog_waste_bin]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'dog_bin'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'dog_waste_bin'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_basket + waste=dog_excrement + vending=excrement_bags"
                # fixAdd:"amenity=waste_basket"
                # fixAdd:"vending=excrement_bags"
                # fixAdd:"waste=dog_excrement"
                err.append({'class': 9002001, 'subclass': 2091877281, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'waste_basket'],
                    [u'vending',u'excrement_bags'],
                    [u'waste',u'dog_excrement']])
                }})

        # *[amenity=artwork]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'artwork'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=artwork"
                # fixRemove:"amenity"
                # fixAdd:"tourism=artwork"
                err.append({'class': 9002001, 'subclass': 728429076, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tourism',u'artwork']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=community_center]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'community_center'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre"
                # fixAdd:"amenity=community_centre"
                err.append({'class': 9002001, 'subclass': 690512681, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'community_centre']])
                }})

        # *[man_made=cut_line]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'cut_line'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=cutline"
                # fixAdd:"man_made=cutline"
                err.append({'class': 9002001, 'subclass': 1008752382, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'cutline']])
                }})

        # *[amenity=park]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'park'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=park"
                # fixRemove:"amenity"
                # fixAdd:"leisure=park"
                err.append({'class': 9002001, 'subclass': 2085280194, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure',u'park']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=hotel]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hotel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=hotel"
                # fixRemove:"amenity"
                # fixAdd:"tourism=hotel"
                err.append({'class': 9002001, 'subclass': 1341786818, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tourism',u'hotel']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[shop=window]
        # *[shop=windows]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'window'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'windows'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=window_construction"
                # fixAdd:"craft=window_construction"
                # fixRemove:"shop"
                err.append({'class': 9002001, 'subclass': 532391183, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'craft',u'window_construction']]),
                    '-': ([
                    u'shop'])
                }})

        # *[amenity=education]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'education'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=college"
                # suggestAlternative:"amenity=school"
                # suggestAlternative:"amenity=university"
                err.append({'class': 9002001, 'subclass': 796960259, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=gallery]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gallery'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=art"
                # fixAdd:"shop=art"
                err.append({'class': 9002001, 'subclass': 1319611546, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'art']])
                }})

        # *[shop=gambling]
        # *[leisure=gambling]
        if (u'leisure' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gambling'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'gambling'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1955724853, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[office=real_estate]
        # *[office=real_estate_agent]
        if (u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'real_estate'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'real_estate_agent'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"office=estate_agent"
                # fixAdd:"office=estate_agent"
                err.append({'class': 9002001, 'subclass': 2027311706, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'office',u'estate_agent']])
                }})

        # *[shop=glass]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'glass'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=glaziery"
                # suggestAlternative:"shop=glaziery"
                err.append({'class': 9002001, 'subclass': 712020531, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=proposed]
        # *[amenity=proposed]
        # *[amenity=disused]
        # *[shop=disused]
        # *[highway=abandoned]
        # *[historic=abandoned]
        if (u'amenity' in keys) or (u'highway' in keys) or (u'historic' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Use the {1}: key prefix instead.","{0.tag}","{0.value}")
                err.append({'class': 9002001, 'subclass': 1169228401, 'text': mapcss.tr(u'{0} is deprecated. Use the {1}: key prefix instead.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=swimming_pool]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'swimming_pool'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=swimming_pool"
                # fixChangeKey:"amenity => leisure"
                err.append({'class': 9002001, 'subclass': 2012807801, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=sauna]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'sauna'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=sauna"
                # fixChangeKey:"amenity => leisure"
                err.append({'class': 9002001, 'subclass': 1450116742, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[/^[^t][^i][^g].+_[0-9]$/][!/^note_[0-9]$/][!/^description_[0-9]$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_300dfa36) and not mapcss._tag_capture(capture_tags, 1, tags, self.re_3185ac6d) and not mapcss._tag_capture(capture_tags, 2, tags, self.re_6d27b157))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable key (ending with a number)")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002014, 'subclass': 2081989305, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[sport=skating]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'skating'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=ice_skating"
                # suggestAlternative:"sport=roller_skating"
                err.append({'class': 9002001, 'subclass': 170699177, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=public_building]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'public_building'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"..."
                # suggestAlternative:"amenity=community_centre"
                # suggestAlternative:"amenity=hospital"
                # suggestAlternative:"amenity=townhall"
                # suggestAlternative:"building=hospital"
                # suggestAlternative:"building=public"
                # suggestAlternative:"leisure=sports_centre"
                # suggestAlternative:"office=government"
                err.append({'class': 9002001, 'subclass': 1295642010, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[office=administrative]
        if (u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'administrative'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"office=government"
                # fixAdd:"office=government"
                err.append({'class': 9002001, 'subclass': 213844674, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'office',u'government']])
                }})

        # *[vending=news_papers]
        if (u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'news_papers'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=newspapers"
                # fixAdd:"vending=newspapers"
                err.append({'class': 9002001, 'subclass': 1133820292, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'vending',u'newspapers']])
                }})

        # *[service=drive_through]
        if (u'service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'service') == mapcss._value_capture(capture_tags, 0, u'drive_through'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"service=drive-through"
                # fixAdd:"service=drive-through"
                err.append({'class': 9002001, 'subclass': 283545650, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'service',u'drive-through']])
                }})

        # *[noexit][noexit!=yes][noexit!=no]
        if (u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') and mapcss._tag_capture(capture_tags, 1, tags, u'noexit') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'noexit') != mapcss._value_const_capture(capture_tags, 2, u'no', u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The key {0} has an uncommon value.","{1.key}")
                err.append({'class': 9002017, 'subclass': 1357403556, 'text': mapcss.tr(u'The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name:botanical]
        if (u'name:botanical' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name:botanical'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"species"
                err.append({'class': 9002001, 'subclass': 1061429000, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[pole=air_to_ground]
        # node[pole=transition]
        if (u'pole' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pole') == mapcss._value_capture(capture_tags, 0, u'air_to_ground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pole') == mapcss._value_capture(capture_tags, 0, u'transition'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"pole"
                err.append({'class': 9002001, 'subclass': 647400518, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location:transition',u'yes']]),
                    '-': ([
                    u'pole'])
                }})

        # node[tower=air_to_ground]
        # node[tower=transition]
        if (u'tower' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower') == mapcss._value_capture(capture_tags, 0, u'air_to_ground'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower') == mapcss._value_capture(capture_tags, 0, u'transition'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"tower"
                err.append({'class': 9002001, 'subclass': 1616290060, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location:transition',u'yes']]),
                    '-': ([
                    u'tower'])
                }})

        # *[shop=souvenir]
        # *[shop=souvenirs]
        # *[shop=souveniers]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souvenir'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souvenirs'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souveniers'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=gift"
                # fixAdd:"shop=gift"
                err.append({'class': 9002001, 'subclass': 1794702946, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'gift']])
                }})

        # *[vending=animal_food]
        if (u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'animal_food'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=animal_feed"
                # fixAdd:"vending=animal_feed"
                err.append({'class': 9002001, 'subclass': 1077411296, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'vending',u'animal_feed']])
                }})

        # node[vending=photos][amenity=vending_machine]
        # node[vending=photo][amenity=vending_machine]
        if (u'amenity' in keys and u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'photos') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'vending_machine'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'photo') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'vending_machine'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=photo_booth"
                # fixAdd:"amenity=photo_booth"
                # fixRemove:"vending"
                err.append({'class': 9002001, 'subclass': 1387510120, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'photo_booth']]),
                    '-': ([
                    u'vending'])
                }})

        # node[vending=photos][amenity!=vending_machine]
        if (u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'photos') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'vending_machine', u'vending_machine'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=photo_booth"
                err.append({'class': 9002001, 'subclass': 1506790891, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[highway=emergency_access_point][phone][!emergency_telephone_code]
        if (u'highway' in keys and u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'emergency_access_point') and mapcss._tag_capture(capture_tags, 1, tags, u'phone') and not mapcss._tag_capture(capture_tags, 2, tags, u'emergency_telephone_code'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # fixChangeKey:"phone => emergency_telephone_code"
                # assertNoMatch:"node highway=emergency_access_point emergency_telephone_code=456"
                # assertNoMatch:"node highway=emergency_access_point phone=123 emergency_telephone_code=456"
                # assertMatch:"node highway=emergency_access_point phone=123"
                # assertNoMatch:"node phone=123"
                err.append({'class': 9002001, 'subclass': 1339208019, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency_telephone_code', mapcss.tag(tags, u'phone')]]),
                    '-': ([
                    u'phone'])
                }})

        # node[highway=emergency_access_point][phone=*emergency_telephone_code]
        if (u'highway' in keys and u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'emergency_access_point') and mapcss._tag_capture(capture_tags, 1, tags, u'phone') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'emergency_telephone_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # fixRemove:"phone"
                # assertNoMatch:"node highway=emergency_access_point emergency_telephone_code=123"
                # assertMatch:"node highway=emergency_access_point phone=123 emergency_telephone_code=123"
                # assertNoMatch:"node highway=emergency_access_point phone=123"
                err.append({'class': 9002001, 'subclass': 342466099, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'phone'])
                }})

        # node[highway=emergency_access_point][phone][emergency_telephone_code][phone!=*emergency_telephone_code]
        if (u'emergency_telephone_code' in keys and u'highway' in keys and u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'emergency_access_point') and mapcss._tag_capture(capture_tags, 1, tags, u'phone') and mapcss._tag_capture(capture_tags, 2, tags, u'emergency_telephone_code') and mapcss._tag_capture(capture_tags, 3, tags, u'phone') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'emergency_telephone_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # assertNoMatch:"node highway=emergency_access_point emergency_telephone_code=123"
                # assertNoMatch:"node highway=emergency_access_point phone=123 emergency_telephone_code=123"
                # assertNoMatch:"node highway=emergency_access_point phone=123"
                err.append({'class': 9002001, 'subclass': 663070970, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=hunting_stand][lock=yes]
        # *[amenity=hunting_stand][lock=no]
        if (u'amenity' in keys and u'lock' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hunting_stand') and mapcss._tag_capture(capture_tags, 1, tags, u'lock') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hunting_stand') and mapcss._tag_capture(capture_tags, 1, tags, u'lock') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"lockable"
                # fixChangeKey:"lock => lockable"
                err.append({'class': 9002001, 'subclass': 1939599742, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'lockable', mapcss.tag(tags, u'lock')]]),
                    '-': ([
                    u'lock'])
                }})

        # *[amenity=advertising][!advertising]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'advertising') and not mapcss._tag_capture(capture_tags, 1, tags, u'advertising'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"advertising=*"
                err.append({'class': 9002001, 'subclass': 1696784412, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=advertising][advertising]
        if (u'advertising' in keys and u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'advertising') and mapcss._tag_capture(capture_tags, 1, tags, u'advertising'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"advertising=*"
                # fixRemove:"amenity"
                err.append({'class': 9002001, 'subclass': 1538706366, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'amenity'])
                }})

        # *[building=true]
        # *[building="*"]
        # *[building=Y]
        # *[building=y]
        # *[building=1]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'true'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'*'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'Y'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'y'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"building=yes"
                # fixAdd:"building=yes"
                err.append({'class': 9002018, 'subclass': 596818855, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes']])
                }})

        # *[building=abandoned]
        # *[building=address]
        # *[building=bing]
        # *[building=collapsed]
        # *[building=damaged]
        # *[building=demolished]
        # *[building=disused]
        # *[building=fixme]
        # *[building=occupied]
        # *[building=razed]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'address'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'bing'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'collapsed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'damaged'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'demolished'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'fixme'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'occupied'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'razed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 938825828, 'text': mapcss.tr(u'{0} is not a building type.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building=other]
        # *[building=unclassified]
        # *[building=undefined]
        # *[building=unknown]
        # *[building=unidentified]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'other'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unclassified'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'undefined'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unidentified'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                # fixAdd:"building=yes"
                err.append({'class': 9002001, 'subclass': 48721080, 'text': mapcss.tr(u'{0} is not a building type.', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes']])
                }})

        # node[power=transformer][location=pole][transformer]
        if (u'location' in keys and u'power' in keys and u'transformer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer') and mapcss._tag_capture(capture_tags, 1, tags, u'location') == mapcss._value_capture(capture_tags, 1, u'pole') and mapcss._tag_capture(capture_tags, 2, tags, u'transformer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # fixChangeKey:"location => power"
                err.append({'class': 9002001, 'subclass': 161456790, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'power', mapcss.tag(tags, u'location')]]),
                    '-': ([
                    u'location'])
                }})

        # node[power=transformer][location=pole][!transformer]
        if (u'location' in keys and u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer') and mapcss._tag_capture(capture_tags, 1, tags, u'location') == mapcss._value_capture(capture_tags, 1, u'pole') and not mapcss._tag_capture(capture_tags, 2, tags, u'transformer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # fixChangeKey:"location => power"
                # fixAdd:"transformer=yes"
                err.append({'class': 9002001, 'subclass': 1830605870, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'power', mapcss.tag(tags, u'location')],
                    [u'transformer',u'yes']]),
                    '-': ([
                    u'location'])
                }})

        # node[tourism=picnic_table]
        # node[amenity=picnic_table]
        # node[leisure=picnic]
        # node[leisure=picnic_site]
        if (u'amenity' in keys) or (u'leisure' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'picnic_table'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'picnic_table'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'picnic'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'picnic_site'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=picnic_table"
                # suggestAlternative:"tourism=picnic_site"
                err.append({'class': 9002001, 'subclass': 480506019, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=toilet]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'toilet'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"amenity=toilets"
                # fixAdd:"amenity=toilets"
                err.append({'class': 9002018, 'subclass': 440018606, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'toilets']])
                }})

        # *[man_made=MDF]
        # *[man_made=telephone_exchange]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'MDF'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'telephone_exchange'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixRemove:"man_made"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 634698090, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'exchange']]),
                    '-': ([
                    u'man_made'])
                }})

        # *[building=central_office]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'central_office'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"building=yes"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1091970270, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes'],
                    [u'telecom',u'exchange']])
                }})

        # *[telecom=central_office]
        if (u'telecom' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'telecom') == mapcss._value_capture(capture_tags, 0, u'central_office'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1503278830, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'exchange']])
                }})

        # node[communication=outdoor_dslam]
        # node[man_made=outdoor_dslam]
        # node[street_cabinet=outdoor_dslam]
        if (u'communication' in keys) or (u'man_made' in keys) or (u'street_cabinet' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'communication') == mapcss._value_capture(capture_tags, 0, u'outdoor_dslam'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'outdoor_dslam'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'street_cabinet') == mapcss._value_capture(capture_tags, 0, u'outdoor_dslam'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=service_device"
                # fixAdd:"telecom=service_device"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1243371306, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'service_device']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # node[telecom=dslam]
        # node[telecom=outdoor_dslam]
        if (u'telecom' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'telecom') == mapcss._value_capture(capture_tags, 0, u'dslam'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'telecom') == mapcss._value_capture(capture_tags, 0, u'outdoor_dslam'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=service_device"
                # fixAdd:"telecom=service_device"
                err.append({'class': 9002001, 'subclass': 781930166, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'service_device']])
                }})

        # node[amenity=fire_hydrant]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fire_hydrant'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"emergency=fire_hydrant"
                # fixChangeKey:"amenity => emergency"
                err.append({'class': 9002001, 'subclass': 967497433, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # node[fire_hydrant:type=pond]
        if (u'fire_hydrant:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fire_hydrant:type') == mapcss._value_capture(capture_tags, 0, u'pond'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"water_source=pond"
                # fixAdd:"water_source=pond"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1583105855, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'water_source',u'pond']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # node[fire_hydrant:flow_capacity]
        if (u'fire_hydrant:flow_capacity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fire_hydrant:flow_capacity'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"flow_rate"
                err.append({'class': 9002001, 'subclass': 1864683984, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[emergency=fire_hydrant][in_service=no]
        if (u'emergency' in keys and u'in_service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'fire_hydrant') and mapcss._tag_capture(capture_tags, 1, tags, u'in_service') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"disused:emergency=fire_hydrant"
                # fixAdd:"disused:emergency=fire_hydrant"
                # fixRemove:"{0.key}"
                # fixRemove:"{1.key}"
                err.append({'class': 9002001, 'subclass': 552149777, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'disused:emergency',u'fire_hydrant']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}'),
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # node[fire_hydrant:water_source]
        if (u'fire_hydrant:water_source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fire_hydrant:water_source'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"water_source"
                # fixChangeKey:"fire_hydrant:water_source => water_source"
                err.append({'class': 9002001, 'subclass': 1207497718, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'water_source', mapcss.tag(tags, u'fire_hydrant:water_source')]]),
                    '-': ([
                    u'fire_hydrant:water_source'])
                }})

        # *[natural=waterfall]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'waterfall'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"waterway=waterfall"
                # fixChangeKey:"natural => waterway"
                err.append({'class': 9002001, 'subclass': 764711734, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'waterway', mapcss.tag(tags, u'natural')]]),
                    '-': ([
                    u'natural'])
                }})

        # *[religion=unitarian]
        if (u'religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'religion') == mapcss._value_capture(capture_tags, 0, u'unitarian'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"religion=unitarian_universalist"
                # fixAdd:"religion=unitarian_universalist"
                err.append({'class': 9002001, 'subclass': 9227331, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'religion',u'unitarian_universalist']])
                }})

        # *[shop=shopping_centre]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'shopping_centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=mall"
                # fixAdd:"shop=mall"
                err.append({'class': 9002001, 'subclass': 1448390566, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'mall']])
                }})

        # *[is_in]
        # node[/^is_in:.*$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'is_in'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_493fd1a6))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 355584917, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[sport=football]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'football'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=american_football"
                # suggestAlternative:"sport=australian_football"
                # suggestAlternative:"sport=canadian_football"
                # suggestAlternative:"sport=gaelic_games"
                # suggestAlternative:"sport=rugby_league"
                # suggestAlternative:"sport=rugby_union"
                # suggestAlternative:"sport=soccer"
                err.append({'class': 9002001, 'subclass': 73038577, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=common]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'common'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"designation=common"
                # suggestAlternative:"landuse=*"
                # suggestAlternative:"leisure=*"
                err.append({'class': 9002001, 'subclass': 157636301, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[cuisine=vegan]
        # *[cuisine=vegetarian]
        if (u'cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cuisine') == mapcss._value_capture(capture_tags, 0, u'vegan'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cuisine') == mapcss._value_capture(capture_tags, 0, u'vegetarian'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("diet:","{0.value}","=only")
                # suggestAlternative:concat("diet:","{0.value}","=yes")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 43604574, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[kitchen_hours]
        if (u'kitchen_hours' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kitchen_hours'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"opening_hours:kitchen"
                # fixChangeKey:"kitchen_hours => opening_hours:kitchen"
                err.append({'class': 9002001, 'subclass': 1088306802, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'opening_hours:kitchen', mapcss.tag(tags, u'kitchen_hours')]]),
                    '-': ([
                    u'kitchen_hours'])
                }})

        # *[shop=money_transfer]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'money_transfer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=money_transfer"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 1664997936, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'shop')]]),
                    '-': ([
                    u'shop'])
                }})

        # *[contact:google_plus]
        if (u'contact:google_plus' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'contact:google_plus'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"contact:google_plus"
                err.append({'class': 9002001, 'subclass': 1869461154, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'contact:google_plus'])
                }})

        # *[amenity=garages]
        # *[amenity=garage]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'garages'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'garage'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("building=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + parking=garage_boxes"
                # suggestAlternative:"landuse=garages"
                err.append({'class': 9002001, 'subclass': 863228118, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=winery]
        # *[amenity=winery]
        if (u'amenity' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'winery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'winery'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=winery"
                # suggestAlternative:"shop=wine"
                err.append({'class': 9002001, 'subclass': 1773574987, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=youth_centre]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'youth_centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre + community_centre=youth_centre"
                # fixAdd:"amenity=community_centre"
                # fixAdd:"community_centre=youth_centre"
                err.append({'class': 9002001, 'subclass': 1284929085, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'community_centre'],
                    [u'community_centre',u'youth_centre']])
                }})

        # *[building:type][building=yes]
        # *[building:type][!building]
        if (u'building' in keys and u'building:type' in keys) or (u'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and mapcss._tag_capture(capture_tags, 1, tags, u'building') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # fixChangeKey:"building:type => building"
                err.append({'class': 9002001, 'subclass': 1927794430, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building', mapcss.tag(tags, u'building:type')]]),
                    '-': ([
                    u'building:type'])
                }})

        # *[building:type][building][building!=yes]
        if (u'building' in keys and u'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != mapcss._value_const_capture(capture_tags, 2, u'yes', u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                err.append({'class': 9002001, 'subclass': 1133239698, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[escalator]
        if (u'escalator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'escalator'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"highway=steps + conveying=*"
                err.append({'class': 9002001, 'subclass': 967271828, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[fenced]
        if (u'fenced' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fenced'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"barrier=fence"
                err.append({'class': 9002001, 'subclass': 1141285220, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[historic_name][!old_name]
        if (u'historic_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"old_name"
                # fixChangeKey:"historic_name => old_name"
                err.append({'class': 9002001, 'subclass': 1034538127, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'old_name', mapcss.tag(tags, u'historic_name')]]),
                    '-': ([
                    u'historic_name'])
                }})

        # *[historic_name][old_name]
        if (u'historic_name' in keys and u'old_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic_name') and mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"old_name"
                err.append({'class': 9002001, 'subclass': 30762614, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[landuse=field]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'field'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=farmland"
                # fixAdd:"landuse=farmland"
                err.append({'class': 9002001, 'subclass': 426261497, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'landuse',u'farmland']])
                }})

        # *[leisure=beach]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'beach'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=beach_resort"
                # suggestAlternative:"natural=beach"
                err.append({'class': 9002001, 'subclass': 1767286055, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=club]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'club'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"club=*"
                err.append({'class': 9002001, 'subclass': 1282397509, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=video_arcade]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'video_arcade'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=adult_gaming_centre"
                # suggestAlternative:"leisure=amusement_arcade"
                err.append({'class': 9002001, 'subclass': 1463909830, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[man_made=jetty]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'jetty'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=pier"
                # fixAdd:"man_made=pier"
                err.append({'class': 9002001, 'subclass': 192707176, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'pier']])
                }})

        # *[man_made=village_pump]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'village_pump'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=water_well"
                # fixAdd:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 423232686, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'water_well']])
                }})

        # *[man_made=water_tank]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'water_tank'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=storage_tank + content=water"
                # fixAdd:"content=water"
                # fixAdd:"man_made=storage_tank"
                err.append({'class': 9002001, 'subclass': 563629665, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'content',u'water'],
                    [u'man_made',u'storage_tank']])
                }})

        # *[natural=moor]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'moor'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=meadow + meadow=agricultural"
                # suggestAlternative:"natural=fell"
                # suggestAlternative:"natural=grassland"
                # suggestAlternative:"natural=heath"
                # suggestAlternative:"natural=scrub"
                # suggestAlternative:"natural=tundra"
                # suggestAlternative:"natural=wetland"
                err.append({'class': 9002001, 'subclass': 374637717, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[noexit=no][!fixme]
        if (u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') == mapcss._value_capture(capture_tags, 0, u'no') and not mapcss._tag_capture(capture_tags, 1, tags, u'fixme'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"fixme=continue"
                # fixAdd:"fixme=continue"
                # fixRemove:"noexit"
                err.append({'class': 9002001, 'subclass': 647435126, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'fixme',u'continue']]),
                    '-': ([
                    u'noexit'])
                }})

        # *[noexit=no][fixme]
        if (u'fixme' in keys and u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') == mapcss._value_capture(capture_tags, 0, u'no') and mapcss._tag_capture(capture_tags, 1, tags, u'fixme'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"fixme=continue"
                err.append({'class': 9002001, 'subclass': 881828009, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=dive]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'dive'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=scuba_diving"
                # fixAdd:"shop=scuba_diving"
                err.append({'class': 9002001, 'subclass': 1582968978, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'scuba_diving']])
                }})

        # *[shop=furnace]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'furnace'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=plumber"
                # suggestAlternative:"shop=fireplace"
                err.append({'class': 9002001, 'subclass': 1155821104, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=paragliding]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'paragliding'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=free_flying"
                # fixAdd:"sport=free_flying"
                err.append({'class': 9002001, 'subclass': 1531788430, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'free_flying']])
                }})

        # *[tourism=bed_and_breakfast]
        if (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'bed_and_breakfast'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=guest_house + guest_house=bed_and_breakfast"
                # fixAdd:"guest_house=bed_and_breakfast"
                # fixAdd:"tourism=guest_house"
                err.append({'class': 9002001, 'subclass': 954237438, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'guest_house',u'bed_and_breakfast'],
                    [u'tourism',u'guest_house']])
                }})

        # *[diaper=yes]
        # *[diaper=no]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper => changing_table"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 1957125311, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table', mapcss.tag(tags, u'diaper')]]),
                    '-': ([
                    u'diaper'])
                }})

        # *[diaper][diaper=~/^[1-9][0-9]*$/]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0f294fdf), mapcss._tag_capture(capture_tags, 1, tags, u'diaper')))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=yes + changing_table:count=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixAdd:"changing_table=yes"
                # fixChangeKey:"diaper => changing_table:count"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 2105051472, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table',u'yes'],
                    [u'changing_table:count', mapcss.tag(tags, u'diaper')]]),
                    '-': ([
                    u'diaper'])
                }})

        # *[diaper=room]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'room'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table=dedicated_room"
                # suggestAlternative:"changing_table=room"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 883202329, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[diaper]!.diaper_checked
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_diaper_checked and mapcss._tag_capture(capture_tags, 0, tags, u'diaper'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"changing_table"
                err.append({'class': 9002001, 'subclass': 693675339, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[diaper:male=yes]
        if (u'diaper:male' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:male') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=male_toilet"
                # fixAdd:"changing_table:location=male_toilet"
                # fixRemove:"diaper:male"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 799035479, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'male_toilet']]),
                    '-': ([
                    u'diaper:male'])
                }})

        # *[diaper:female=yes]
        if (u'diaper:female' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:female') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=female_toilet"
                # fixAdd:"changing_table:location=female_toilet"
                # fixRemove:"diaper:female"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1450901137, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'female_toilet']]),
                    '-': ([
                    u'diaper:female'])
                }})

        # *[diaper:unisex=yes]
        if (u'diaper:unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:unisex') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=unisex_toilet"
                # fixAdd:"changing_table:location=unisex_toilet"
                # fixRemove:"diaper:unisex"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1460378712, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'unisex_toilet']]),
                    '-': ([
                    u'diaper:unisex'])
                }})

        # *[diaper:wheelchair=yes]
        # *[diaper:wheelchair=no]
        if (u'diaper:wheelchair' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:wheelchair=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:wheelchair => changing_table:wheelchair"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1951967281, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:wheelchair', mapcss.tag(tags, u'diaper:wheelchair')]]),
                    '-': ([
                    u'diaper:wheelchair'])
                }})

        # *[diaper:fee=yes]
        # *[diaper:fee=no]
        if (u'diaper:fee' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:fee') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:fee') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:fee=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:fee => changing_table:fee"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 2008573526, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:fee', mapcss.tag(tags, u'diaper:fee')]]),
                    '-': ([
                    u'diaper:fee'])
                }})

        # *[/^diaper:/]!.diaper___checked
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_diaper___checked and mapcss._tag_capture(capture_tags, 0, tags, self.re_6029fe03))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","diaper:*")
                # suggestAlternative:"changing_table:*"
                err.append({'class': 9002001, 'subclass': 26578864, 'text': mapcss.tr(u'{0} is deprecated', u'diaper:*')})

        # *[changing_table][changing_table!~/^(yes|no|limited)$/]
        if (u'changing_table' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'changing_table') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_787405b1, u'^(yes|no|limited)$'), mapcss._tag_capture(capture_tags, 1, tags, u'changing_table')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"changing_table=limited"
                # suggestAlternative:"changing_table=no"
                # suggestAlternative:"changing_table=yes"
                err.append({'class': 9002019, 'subclass': 1965225408, 'text': mapcss.tr(u'wrong value: {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[roof:shape=half_hipped]
        if (u'roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:shape') == mapcss._value_capture(capture_tags, 0, u'half_hipped'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"roof:shape=half-hipped"
                # fixAdd:"roof:shape=half-hipped"
                err.append({'class': 9002001, 'subclass': 1548347123, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'roof:shape',u'half-hipped']])
                }})

        # *[bridge_name]
        if (u'bridge_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"bridge:name"
                # fixChangeKey:"bridge_name => bridge:name"
                err.append({'class': 9002001, 'subclass': 80069399, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:name', mapcss.tag(tags, u'bridge_name')]]),
                    '-': ([
                    u'bridge_name'])
                }})

        # *[access=public]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'public'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"access=yes"
                # fixAdd:"access=yes"
                err.append({'class': 9002001, 'subclass': 1115157097, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'access',u'yes']])
                }})

        # *[crossing=island]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') == mapcss._value_capture(capture_tags, 0, u'island'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"crossing:island=yes"
                # fixRemove:"crossing"
                # fixAdd:"crossing:island=yes"
                err.append({'class': 9002001, 'subclass': 1512561318, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'crossing:island',u'yes']]),
                    '-': ([
                    u'crossing'])
                }})

        # *[recycling:metal]
        if (u'recycling:metal' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'recycling:metal'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"recycling:scrap_metal"
                # fixChangeKey:"recycling:metal => recycling:scrap_metal"
                err.append({'class': 9002001, 'subclass': 474491272, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'recycling:scrap_metal', mapcss.tag(tags, u'recycling:metal')]]),
                    '-': ([
                    u'recycling:metal'])
                }})

        # *[shop=dog_grooming]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'dog_grooming'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet_grooming"
                # fixAdd:"shop=pet_grooming"
                err.append({'class': 9002001, 'subclass': 1073412885, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'pet_grooming']])
                }})

        # *[tower:type=anchor]
        # *[tower:type=suspension]
        if (u'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower:type') == mapcss._value_capture(capture_tags, 0, u'anchor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower:type') == mapcss._value_capture(capture_tags, 0, u'suspension'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"tower:type => line_attachment"
                err.append({'class': 9002001, 'subclass': 180380605, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'line_attachment', mapcss.tag(tags, u'tower:type')]]),
                    '-': ([
                    u'tower:type'])
                }})

        # node[pole:type=anchor]
        # node[pole:type=suspension]
        if (u'pole:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pole:type') == mapcss._value_capture(capture_tags, 0, u'anchor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pole:type') == mapcss._value_capture(capture_tags, 0, u'suspension'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"pole:type => line_attachment"
                err.append({'class': 9002001, 'subclass': 1925507031, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'line_attachment', mapcss.tag(tags, u'pole:type')]]),
                    '-': ([
                    u'pole:type'])
                }})

        # node[man_made=pipeline_marker]
        # node[pipeline=marker]
        # node[power=marker]
        # node[cable=marker]
        if (u'cable' in keys) or (u'man_made' in keys) or (u'pipeline' in keys) or (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'pipeline_marker'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pipeline') == mapcss._value_capture(capture_tags, 0, u'marker'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'marker'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cable') == mapcss._value_capture(capture_tags, 0, u'marker'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"marker=* + utility=*"
                err.append({'class': 9002001, 'subclass': 296597752, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sloped_curb=yes][!kerb]
        # *[sloped_curb=both][!kerb]
        if (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'yes') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'both') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=lowered"
                # fixAdd:"kerb=lowered"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 1906002413, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'kerb',u'lowered']]),
                    '-': ([
                    u'sloped_curb'])
                }})

        # *[sloped_curb=no][!kerb]
        if (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'no') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=yes"
                # fixAdd:"kerb=yes"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 893727015, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'kerb',u'yes']]),
                    '-': ([
                    u'sloped_curb'])
                }})

        # *[sloped_curb][sloped_curb!~/^(yes|both|no)$/][!kerb]
        # *[sloped_curb][kerb]
        if (u'kerb' in keys and u'sloped_curb' in keys) or (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_01eb1711, u'^(yes|both|no)$'), mapcss._tag_capture(capture_tags, 1, tags, u'sloped_curb')) and not mapcss._tag_capture(capture_tags, 2, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') and mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"kerb=*"
                err.append({'class': 9002001, 'subclass': 1682376745, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[unnamed=yes]
        if (u'unnamed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unnamed') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"noname=yes"
                # fixChangeKey:"unnamed => noname"
                err.append({'class': 9002001, 'subclass': 1901447020, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'noname', mapcss.tag(tags, u'unnamed')]]),
                    '-': ([
                    u'unnamed'])
                }})

        # node[segregated][segregated!=yes][segregated!=no]
        if (u'segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'segregated') and mapcss._tag_capture(capture_tags, 1, tags, u'segregated') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'segregated') != mapcss._value_const_capture(capture_tags, 2, u'no', u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9002020, 'subclass': 1015641959, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[building:height]
        if (u'building:height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:height'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"height"
                # fixChangeKey:"building:height => height"
                err.append({'class': 9002001, 'subclass': 1328174745, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'height', mapcss.tag(tags, u'building:height')]]),
                    '-': ([
                    u'building:height'])
                }})

        # *[building:min_height]
        if (u'building:min_height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:min_height'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"min_height"
                # fixChangeKey:"building:min_height => min_height"
                err.append({'class': 9002001, 'subclass': 1042683921, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'min_height', mapcss.tag(tags, u'building:min_height')]]),
                    '-': ([
                    u'building:min_height'])
                }})

        # *[car][amenity=charging_station]
        if (u'amenity' in keys and u'car' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'car') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'charging_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"motorcar"
                # fixChangeKey:"car => motorcar"
                err.append({'class': 9002001, 'subclass': 1165117414, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'motorcar', mapcss.tag(tags, u'car')]]),
                    '-': ([
                    u'car'])
                }})

        # *[navigationaid=approach_light]
        # *[navigationaid="ALS (Approach lighting system)"]
        if (u'navigationaid' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'navigationaid') == mapcss._value_capture(capture_tags, 0, u'approach_light'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'navigationaid') == mapcss._value_capture(capture_tags, 0, u'ALS (Approach lighting system)'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"navigationaid=als"
                # fixAdd:"navigationaid=als"
                err.append({'class': 9002001, 'subclass': 1577817081, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'navigationaid',u'als']])
                }})

        # node[exit_to]
        if (u'exit_to' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'exit_to'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"destination"
                err.append({'class': 9002001, 'subclass': 2117439762, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[water=riverbank][!natural]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'riverbank') and not mapcss._tag_capture(capture_tags, 1, tags, u'natural'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                err.append({'class': 9002001, 'subclass': 186872153, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'natural',u'water'],
                    [u'water',u'river']])
                }})

        # *[water=riverbank][natural]
        if (u'natural' in keys and u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'riverbank') and mapcss._tag_capture(capture_tags, 1, tags, u'natural'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 630806094, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_diaper___checked = set_diaper_checked = set_samecolor = False

        # *[barrier=wire_fence]
        if (u'barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wire_fence'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=chain_link"
                # assertNoMatch:"way barrier=fence"
                # assertMatch:"way barrier=wire_fence"
                err.append({'class': 9002001, 'subclass': 1107799632, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'fence'],
                    [u'fence_type',u'chain_link']])
                }})

        # *[barrier=wood_fence]
        if (u'barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wood_fence'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=wood"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=wood"
                err.append({'class': 9002001, 'subclass': 1412230714, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'fence'],
                    [u'fence_type',u'wood']])
                }})

        # way[highway=ford]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'ford'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"highway=* + ford=yes"
                err.append({'class': 9002001, 'subclass': 591931361, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[class]
        if (u'class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'class'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"highway"
                err.append({'class': 9002001, 'subclass': 905310794, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[highway=stile]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stile'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=stile"
                # fixAdd:"barrier=stile"
                # fixRemove:"highway"
                err.append({'class': 9002001, 'subclass': 1435678043, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'stile']]),
                    '-': ([
                    u'highway'])
                }})

        # *[highway=incline]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'incline'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 765169083, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[highway=incline_steep]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'incline_steep'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 1966772390, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[highway=unsurfaced]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'unsurfaced'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"highway=* + surface=unpaved"
                # fixAdd:"highway=road"
                # fixAdd:"surface=unpaved"
                err.append({'class': 9002001, 'subclass': 20631498, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'highway',u'road'],
                    [u'surface',u'unpaved']])
                }})

        # *[landuse=wood]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'wood'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=forest"
                # suggestAlternative:"natural=wood"
                err.append({'class': 9002001, 'subclass': 469903103, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[natural=marsh]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'marsh'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=wetland + wetland=marsh"
                # fixAdd:"natural=wetland"
                # fixAdd:"wetland=marsh"
                err.append({'class': 9002001, 'subclass': 1459865523, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'natural',u'wetland'],
                    [u'wetland',u'marsh']])
                }})

        # *[highway=byway]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'byway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 1844620979, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power_source]
        if (u'power_source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power_source'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"generator:source"
                err.append({'class': 9002001, 'subclass': 34751027, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[power_rating]
        if (u'power_rating' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power_rating'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"generator:output"
                err.append({'class': 9002001, 'subclass': 904750343, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[shop=antique]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'antique'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=antiques"
                # fixAdd:"shop=antiques"
                err.append({'class': 9002001, 'subclass': 596668979, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'antiques']])
                }})

        # *[shop=bags]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'bags'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=bag"
                # fixAdd:"shop=bag"
                err.append({'class': 9002001, 'subclass': 1709003584, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'bag']])
                }})

        # *[shop=fashion]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fashion'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=clothes"
                # fixAdd:"shop=clothes"
                err.append({'class': 9002001, 'subclass': 985619804, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'clothes']])
                }})

        # *[shop=organic]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'organic'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=* + organic=only"
                # suggestAlternative:"shop=* + organic=yes"
                err.append({'class': 9002001, 'subclass': 1959365145, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=pets]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'pets'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet"
                # fixAdd:"shop=pet"
                err.append({'class': 9002001, 'subclass': 290270098, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'pet']])
                }})

        # *[shop=pharmacy]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'pharmacy'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=pharmacy"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 350722657, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'shop')]]),
                    '-': ([
                    u'shop'])
                }})

        # *[bicycle_parking=sheffield]
        if (u'bicycle_parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bicycle_parking') == mapcss._value_capture(capture_tags, 0, u'sheffield'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bicycle_parking=stands"
                # fixAdd:"bicycle_parking=stands"
                err.append({'class': 9002001, 'subclass': 718874663, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bicycle_parking',u'stands']])
                }})

        # *[amenity=emergency_phone]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'emergency_phone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"emergency=phone"
                # fixRemove:"amenity"
                # fixAdd:"emergency=phone"
                err.append({'class': 9002001, 'subclass': 1108230656, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'phone']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[sport=gaelic_football]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'gaelic_football'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=gaelic_games"
                # fixAdd:"sport=gaelic_games"
                err.append({'class': 9002001, 'subclass': 1768681881, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'gaelic_games']])
                }})

        # *[power=station]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=plant"
                # suggestAlternative:"power=substation"
                err.append({'class': 9002001, 'subclass': 52025933, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power=sub_station]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'sub_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=substation"
                # fixAdd:"power=substation"
                err.append({'class': 9002001, 'subclass': 1423074682, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'power',u'substation']])
                }})

        # *[location=rooftop]
        if (u'location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'location') == mapcss._value_capture(capture_tags, 0, u'rooftop'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location=roof"
                # fixAdd:"location=roof"
                err.append({'class': 9002001, 'subclass': 1028577225, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location',u'roof']])
                }})

        # *[generator:location]
        if (u'generator:location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:location'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"location"
                # fixChangeKey:"generator:location => location"
                err.append({'class': 9002001, 'subclass': 900615917, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location', mapcss.tag(tags, u'generator:location')]]),
                    '-': ([
                    u'generator:location'])
                }})

        # *[generator:method=dam]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'dam'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-storage"
                # fixAdd:"generator:method=water-storage"
                err.append({'class': 9002001, 'subclass': 248819368, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-storage']])
                }})

        # *[generator:method=pumped-storage]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'pumped-storage'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 93454158, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-pumped-storage']])
                }})

        # *[generator:method=pumping]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'pumping'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 2115673716, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-pumped-storage']])
                }})

        # *[fence_type=chain]
        if (u'fence_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fence_type') == mapcss._value_capture(capture_tags, 0, u'chain'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=chain"
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 19409288, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building=entrance]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'entrance'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"entrance"
                err.append({'class': 9002001, 'subclass': 306662985, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[board_type=board]
        if (u'board_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'board_type') == mapcss._value_capture(capture_tags, 0, u'board'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"board_type"
                err.append({'class': 9002001, 'subclass': 1150949316, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'board_type'])
                }})

        # *[man_made=measurement_station]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'measurement_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=monitoring_station"
                # fixAdd:"man_made=monitoring_station"
                err.append({'class': 9002001, 'subclass': 700465123, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'monitoring_station']])
                }})

        # *[measurement=water_level]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'water_level'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:water_level=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:water_level=yes"
                err.append({'class': 9002001, 'subclass': 634647702, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:water_level',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[measurement=weather]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'weather'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:weather=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:weather=yes"
                err.append({'class': 9002001, 'subclass': 336627227, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:weather',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[measurement=seismic]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'seismic'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:seismic_activity=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:seismic_activity=yes"
                err.append({'class': 9002001, 'subclass': 1402131289, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:seismic_activity',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[monitoring:river_level]
        if (u'monitoring:river_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'monitoring:river_level'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"monitoring:water_level"
                # fixChangeKey:"monitoring:river_level => monitoring:water_level"
                err.append({'class': 9002001, 'subclass': 264907924, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:water_level', mapcss.tag(tags, u'monitoring:river_level')]]),
                    '-': ([
                    u'monitoring:river_level'])
                }})

        # *[stay]
        if (u'stay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'stay'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"maxstay"
                # fixChangeKey:"stay => maxstay"
                err.append({'class': 9002001, 'subclass': 787370129, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'maxstay', mapcss.tag(tags, u'stay')]]),
                    '-': ([
                    u'stay'])
                }})

        # *[emergency=aed]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'aed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"emergency=defibrillator"
                # fixAdd:"emergency=defibrillator"
                err.append({'class': 9002001, 'subclass': 707111885, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'defibrillator']])
                }})

        # *[day_on][!restriction]
        # *[day_off][!restriction]
        # *[date_on][!restriction]
        # *[date_off][!restriction]
        # *[hour_on][!restriction]
        # *[hour_off][!restriction]
        if (u'date_off' in keys) or (u'date_on' in keys) or (u'day_off' in keys) or (u'day_on' in keys) or (u'hour_off' in keys) or (u'hour_on' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'day_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'day_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'date_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'date_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hour_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hour_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"*:conditional"
                err.append({'class': 9002001, 'subclass': 294264920, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[access=designated]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'designated'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' is meaningless, use more specific tags, e.g. ''{1}''","access=designated","bicycle=designated")
                # assertMatch:"way access=designated"
                err.append({'class': 9002002, 'subclass': 2057594338, 'text': mapcss.tr(u'\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', u'access=designated', u'bicycle=designated')})

        # *[access=official]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'official'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' does not specify the official mode of transportation, use ''{1}'' for example","access=official","bicycle=official")
                # assertMatch:"way access=official"
                err.append({'class': 9002003, 'subclass': 1909133836, 'text': mapcss.tr(u'\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', u'access=official', u'bicycle=official')})

        # *[fixme=yes]
        # *[FIXME=yes]
        if (u'FIXME' in keys) or (u'fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fixme') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'FIXME') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Instead of ''{1}'' please give more information about what exactly should be fixed.","{0.key}","{0.value}")
                # assertMatch:"way fixme=yes"
                err.append({'class': 9002004, 'subclass': 136657482, 'text': mapcss.tr(u'{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name][name=~/^(?i)fixme$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.","{0.key}","{0.tag}")
                # fixRemove:"name"
                err.append({'class': 9002005, 'subclass': 642340557, 'text': mapcss.tr(u'Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'name'])
                }})

        # *[note][note=~/^(?i)fixme$/]
        if (u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'note') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, u'note')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.","{0.tag}")
                err.append({'class': 9002006, 'subclass': 1243120287, 'text': mapcss.tr(u'{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[type=broad_leaved]
        # *[type=broad_leafed]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'broad_leaved'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'broad_leafed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=broadleaved"
                # fixAdd:"leaf_type=broadleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 293968062, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'broadleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[wood=coniferous]
        # *[type=coniferous]
        # *[type=conifer]
        if (u'type' in keys) or (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'coniferous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'coniferous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'conifer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=needleleaved"
                # fixAdd:"leaf_type=needleleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 50517650, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'needleleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[wood=mixed]
        if (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'mixed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=mixed"
                # fixAdd:"leaf_type=mixed"
                # fixRemove:"wood"
                err.append({'class': 9002001, 'subclass': 235914603, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'mixed']]),
                    '-': ([
                    u'wood'])
                }})

        # *[wood=evergreen]
        # *[type=evergreen]
        if (u'type' in keys) or (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'evergreen'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'evergreen'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=evergreen"
                # fixAdd:"leaf_cycle=evergreen"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 747964532, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_cycle',u'evergreen']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[type=deciduous]
        # *[type=deciduos]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'deciduous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'deciduos'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=deciduous"
                # fixAdd:"leaf_cycle=deciduous"
                # fixRemove:"type"
                err.append({'class': 9002001, 'subclass': 591116099, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_cycle',u'deciduous']]),
                    '-': ([
                    u'type'])
                }})

        # *[wood=deciduous]
        if (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'deciduous'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type + leaf_cycle"
                err.append({'class': 9002001, 'subclass': 1100223594, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[type=palm]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'palm'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type"
                # suggestAlternative:"species"
                # suggestAlternative:"trees"
                err.append({'class': 9002001, 'subclass': 1757132153, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[natural=land]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'land'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please use instead a multipolygon.","{0.tag}")
                # assertMatch:"way natural=land"
                err.append({'class': 9002001, 'subclass': 94558529, 'text': mapcss.tr(u'{0} is deprecated. Please use instead a multipolygon.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=causeway]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'causeway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=low_water_crossing"
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"ford=yes"
                err.append({'class': 9002001, 'subclass': 461671124, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=swing]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'swing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge:movable=swing"
                # suggestAlternative:"bridge:structure=simple-suspension"
                err.append({'class': 9002001, 'subclass': 1047428067, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=suspension]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'suspension'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=yes + bridge:structure=suspension"
                # fixAdd:"bridge:structure=suspension"
                # fixAdd:"bridge=yes"
                err.append({'class': 9002001, 'subclass': 1157046268, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:structure',u'suspension'],
                    [u'bridge',u'yes']])
                }})

        # *[bridge=pontoon]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'pontoon'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=yes + bridge:structure=floating"
                # fixAdd:"bridge:structure=floating"
                # fixAdd:"bridge=yes"
                err.append({'class': 9002001, 'subclass': 1195531951, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:structure',u'floating'],
                    [u'bridge',u'yes']])
                }})

        # *[fee=interval]
        # *[lit=interval]
        # *[supervised=interval]
        if (u'fee' in keys) or (u'lit' in keys) or (u'supervised' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fee') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lit') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'supervised') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please specify interval by using opening_hours syntax","{0.tag}")
                err.append({'class': 9002001, 'subclass': 417886592, 'text': mapcss.tr(u'{0} is deprecated. Please specify interval by using opening_hours syntax', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[/josm\/ignore/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_5ee0acf2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwError:tr("{0} is deprecated. Please delete this object and use a private layer instead","{0.key}")
                # fixDeleteObject:this
                err.append({'class': 9002001, 'subclass': 1402743016, 'text': mapcss.tr(u'{0} is deprecated. Please delete this object and use a private layer instead', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[sport=diving]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'diving'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=cliff_diving"
                # suggestAlternative:"sport=scuba_diving"
                err.append({'class': 9002001, 'subclass': 590643159, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[parking=park_and_ride]
        if (u'parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'parking') == mapcss._value_capture(capture_tags, 0, u'park_and_ride'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + park_ride=yes"
                # fixAdd:"amenity=parking"
                # fixAdd:"park_ride=yes"
                # fixRemove:"parking"
                err.append({'class': 9002001, 'subclass': 1893516041, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'parking'],
                    [u'park_ride',u'yes']]),
                    '-': ([
                    u'parking'])
                }})

        # *[manhole=plain]
        # *[manhole=unknown]
        # *[manhole=yes]
        # *[police=yes]
        # *[traffic_calming=yes]
        # *[access=restricted]
        # *[barrier=yes]
        # *[aerialway=yes][!public_transport]
        # *[amenity=yes]
        # *[leisure=yes]
        # *[shop="*"]
        # *[shop=yes][amenity!=fuel]
        # *[craft=yes]
        # *[service=yes]
        # *[place=yes]
        if (u'access' in keys) or (u'aerialway' in keys) or (u'amenity' in keys) or (u'barrier' in keys) or (u'craft' in keys) or (u'leisure' in keys) or (u'manhole' in keys) or (u'place' in keys) or (u'police' in keys) or (u'service' in keys) or (u'shop' in keys) or (u'traffic_calming' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'plain'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'police') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'traffic_calming') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'restricted'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'yes') and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'*'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'fuel', u'fuel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'craft') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'service') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Please replace ''{1}'' by a specific value.","{0.key}","{0.value}")
                err.append({'class': 9002007, 'subclass': 1532935474, 'text': mapcss.tr(u'{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[place_name][!name]
        if (u'place_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be replaced with {1}","{0.key}","{1.key}")
                # fixChangeKey:"place_name => name"
                err.append({'class': 9002008, 'subclass': 1089331760, 'text': mapcss.tr(u'{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'name', mapcss.tag(tags, u'place_name')]]),
                    '-': ([
                    u'place_name'])
                }})

        # *[place][place_name=*name]
        if (u'place' in keys and u'place_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss._tag_capture(capture_tags, 1, tags, u'place_name') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} = {1}; remove {0}","{1.key}","{1.value}")
                # fixRemove:"{1.key}"
                err.append({'class': 9002009, 'subclass': 1116761280, 'text': mapcss.tr(u'{0} = {1}; remove {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # way[sidewalk=yes]
        if (u'sidewalk' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sidewalk') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Please replace ''{1}'' by ''left'', ''right'' or ''both''.","{0.key}","{0.value}")
                err.append({'class': 9002015, 'subclass': 36539821, 'text': mapcss.tr(u'{0}={1} is unspecific. Please replace \'\'{1}\'\' by \'\'left\'\', \'\'right\'\' or \'\'both\'\'.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[waterway=water_point]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'water_point'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=water_point"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 103347605, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'waterway')]]),
                    '-': ([
                    u'waterway'])
                }})

        # *[waterway=waste_disposal]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'waste_disposal'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_disposal"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 1963461348, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'waterway')]]),
                    '-': ([
                    u'waterway'])
                }})

        # *[waterway=mooring]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'mooring'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"mooring=yes"
                # fixAdd:"mooring=yes"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 81358738, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'mooring',u'yes']]),
                    '-': ([
                    u'waterway'])
                }})

        # *[building][levels]
        # *[building:part=yes][levels]
        if (u'building' in keys and u'levels' in keys) or (u'building:part' in keys and u'levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') and mapcss._tag_capture(capture_tags, 1, tags, u'levels'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:part') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'levels'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.key}")
                # suggestAlternative:"building:levels"
                # fixChangeKey:"levels => building:levels"
                err.append({'class': 9002001, 'subclass': 293177436, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building:levels', mapcss.tag(tags, u'levels')]]),
                    '-': ([
                    u'levels'])
                }})

        # *[protected_class]
        if (u'protected_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protected_class'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"protect_class"
                # fixChangeKey:"protected_class => protect_class"
                err.append({'class': 9002001, 'subclass': 716999373, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'protect_class', mapcss.tag(tags, u'protected_class')]]),
                    '-': ([
                    u'protected_class'])
                }})

        # *[kerb=unknown]
        # *[lock=unknown]
        # *[hide=unknown]
        # *[shelter=unknown]
        # *[access=unknown]
        # *[capacity:parent=unknown]
        # *[capacity:women=unknown]
        # *[capacity:disabled=unknown]
        # *[crossing=unknown]
        # *[foot=unknown]
        if (u'access' in keys) or (u'capacity:disabled' in keys) or (u'capacity:parent' in keys) or (u'capacity:women' in keys) or (u'crossing' in keys) or (u'foot' in keys) or (u'hide' in keys) or (u'kerb' in keys) or (u'lock' in keys) or (u'shelter' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kerb') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lock') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hide') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shelter') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:parent') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:women') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:disabled') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'foot') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unspecific tag {0}","{0.tag}")
                err.append({'class': 9002010, 'subclass': 1052866123, 'text': mapcss.tr(u'Unspecific tag {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=skiing]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'skiing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # suggestAlternative:tr("{0} + {1} + {2}","piste:type=*","piste:difficulty=*","piste:grooming=*")
                err.append({'class': 9002001, 'subclass': 1578959559, 'text': mapcss.tr(u'Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[waterway=wadi]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'wadi'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=valley"
                # suggestAlternative:"{0.key}=* + intermittent=yes"
                err.append({'class': 9002001, 'subclass': 719234223, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[oneway=1][!waterway]
        if (u'oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') == mapcss._value_capture(capture_tags, 0, 1) and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"oneway=yes"
                # fixAdd:"oneway=yes"
                err.append({'class': 9002001, 'subclass': 430545008, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'oneway',u'yes']])
                }})

        # way[oneway=-1][!waterway]
        if (u'oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') == mapcss._value_capture(capture_tags, 0, -1) and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is not recommended. Use the Reverse Ways function from the Tools menu.","{0.tag}")
                err.append({'class': 9002016, 'subclass': 1448981670, 'text': mapcss.tr(u'{0} is not recommended. Use the Reverse Ways function from the Tools menu.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[drinkable]
        if (u'drinkable' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'drinkable'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"drinking_water"
                err.append({'class': 9002001, 'subclass': 1785584789, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[color][!colour]
        if (u'color' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'color') and not mapcss._tag_capture(capture_tags, 1, tags, u'colour'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour"
                # fixChangeKey:"color => colour"
                # assertNoMatch:"way color=red colour=red"
                # assertMatch:"way color=red"
                err.append({'class': 9002001, 'subclass': 1850270072, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'colour', mapcss.tag(tags, u'color')]]),
                    '-': ([
                    u'color'])
                }})

        # *[color][colour][color=*colour]
        if (u'color' in keys and u'colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'color') and mapcss._tag_capture(capture_tags, 1, tags, u'colour') and mapcss._tag_capture(capture_tags, 2, tags, u'color') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'colour')))
                except mapcss.RuleAbort: pass
            if match:
                # setsamecolor
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # suggestAlternative:"colour"
                # fixRemove:"color"
                # assertNoMatch:"way color=red colour=green"
                # assertMatch:"way color=red colour=red"
                set_samecolor = True
                err.append({'class': 9002001, 'subclass': 1825345743, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'color'])
                }})

        # *[color][colour]!.samecolor
        if (u'color' in keys and u'colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_samecolor and mapcss._tag_capture(capture_tags, 0, tags, u'color') and mapcss._tag_capture(capture_tags, 1, tags, u'colour'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                # suggestAlternative:"colour"
                # assertMatch:"way color=red colour=green"
                # assertNoMatch:"way color=red colour=red"
                err.append({'class': 9002001, 'subclass': 1064658218, 'text': mapcss.tr(u'{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[building:color][building:colour]!.samebuildingcolor
        # Use undeclared class samebuildingcolor

        # *[roof:color][roof:colour]!.sameroofcolor
        # Use undeclared class sameroofcolor

        # *[/:color/][!building:color][!roof:color][!gpxd:color]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_554de4c7) and not mapcss._tag_capture(capture_tags, 1, tags, u'building:color') and not mapcss._tag_capture(capture_tags, 2, tags, u'roof:color') and not mapcss._tag_capture(capture_tags, 3, tags, u'gpxd:color'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:":colour"
                # assertNoMatch:"way color=red"
                # assertMatch:"way cycleway:surface:color=grey"
                # assertNoMatch:"way roof:color=grey"
                err.append({'class': 9002001, 'subclass': 1632389707, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/color:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_0c5b5730))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour:"
                # assertMatch:"way color:back=grey"
                # assertNoMatch:"way color=red"
                err.append({'class': 9002001, 'subclass': 1390370717, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/=|\+|\/|&|<|>|;|'|"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_620f4d52))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("key with uncommon character")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002011, 'subclass': 1752615188, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/^.$/]
        # way[/^..$/][route=ferry][!to]
        # way[/^..$/][route!=ferry]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_27210286))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62) and mapcss._tag_capture(capture_tags, 1, tags, u'route') == mapcss._value_capture(capture_tags, 1, u'ferry') and not mapcss._tag_capture(capture_tags, 2, tags, u'to'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62) and mapcss._tag_capture(capture_tags, 1, tags, u'route') != mapcss._value_const_capture(capture_tags, 1, u'ferry', u'ferry'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uncommon short key")
                # assertNoMatch:"way to=Zuidschermer;Akersloot route=ferry"
                # assertMatch:"way to=bar"
                err.append({'class': 9002012, 'subclass': 1765060211, 'text': mapcss.tr(u'uncommon short key')})

        # *[sport=hockey]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'hockey'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=field_hockey"
                # suggestAlternative:"sport=ice_hockey"
                err.append({'class': 9002001, 'subclass': 651933474, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=billard]
        # *[sport=billards]
        # *[sport=billiard]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billards'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billiard'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=billiards"
                # fixAdd:"sport=billiards"
                err.append({'class': 9002001, 'subclass': 1522897824, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'billiards']])
                }})

        # *[payment:credit_cards=yes]
        if (u'payment:credit_cards' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:credit_cards') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:mastercard=yes","payment:visa=yes")
                err.append({'class': 9002013, 'subclass': 705181097, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:mastercard=yes', u'payment:visa=yes')})

        # *[payment:debit_cards=yes]
        if (u'payment:debit_cards' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:debit_cards') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:maestro=yes","payment:girocard=yes")
                err.append({'class': 9002013, 'subclass': 679215558, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:maestro=yes', u'payment:girocard=yes')})

        # *[payment:electronic_purses=yes]
        if (u'payment:electronic_purses' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:electronic_purses') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:ep_geldkarte=yes","payment:ep_quick=yes")
                err.append({'class': 9002013, 'subclass': 1440457244, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:ep_geldkarte=yes', u'payment:ep_quick=yes')})

        # *[payment:cryptocurrencies=yes]
        if (u'payment:cryptocurrencies' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cryptocurrencies') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:bitcoin=yes","payment:litecoin=yes")
                err.append({'class': 9002013, 'subclass': 1325255949, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:bitcoin=yes', u'payment:litecoin=yes')})

        # *[payment:ep_quick]
        # *[payment:ep_cash]
        # *[payment:ep_proton]
        # *[payment:ep_chipknip]
        if (u'payment:ep_cash' in keys) or (u'payment:ep_chipknip' in keys) or (u'payment:ep_proton' in keys) or (u'payment:ep_quick' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_quick'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_cash'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_proton'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_chipknip'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 332575437, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[kp][highway=milestone]
        # *[kp][railway=milestone]
        # *[kp][waterway=milestone]
        if (u'highway' in keys and u'kp' in keys) or (u'kp' in keys and u'railway' in keys) or (u'kp' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"kp => distance"
                err.append({'class': 9002001, 'subclass': 1078799228, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'distance', mapcss.tag(tags, u'kp')]]),
                    '-': ([
                    u'kp'])
                }})

        # *[pk][highway=milestone]
        # *[pk][railway=milestone]
        # *[pk][waterway=milestone]
        if (u'highway' in keys and u'pk' in keys) or (u'pk' in keys and u'railway' in keys) or (u'pk' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"pk => distance"
                err.append({'class': 9002001, 'subclass': 719029418, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'distance', mapcss.tag(tags, u'pk')]]),
                    '-': ([
                    u'pk'])
                }})

        # *[postcode]
        if (u'postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'postcode'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"addr:postcode"
                # suggestAlternative:"postal_code"
                err.append({'class': 9002001, 'subclass': 1942523538, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[water=intermittent]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'intermittent'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"intermittent=yes"
                # fixAdd:"intermittent=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 813530321, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'intermittent',u'yes']]),
                    '-': ([
                    u'water'])
                }})

        # way[type][type!=waterway][man_made=pipeline]
        if (u'man_made' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != mapcss._value_const_capture(capture_tags, 1, u'waterway', u'waterway') and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') == mapcss._value_capture(capture_tags, 2, u'pipeline'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"substance"
                # fixChangeKey:"type => substance"
                err.append({'class': 9002001, 'subclass': 877981524, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'substance', mapcss.tag(tags, u'type')]]),
                    '-': ([
                    u'type'])
                }})

        # *[landuse=farm]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'farm'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=farmland"
                # suggestAlternative:"landuse=farmyard"
                err.append({'class': 9002001, 'subclass': 1968473048, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[seamark=buoy]["seamark:type"=~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if (u'seamark' in keys and u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark') == mapcss._value_capture(capture_tags, 0, u'buoy') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_61b0be1b), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                # fixRemove:"seamark"
                err.append({'class': 9002001, 'subclass': 1224401740, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'seamark'])
                }})

        # *[seamark=buoy]["seamark:type"!~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if (u'seamark' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark') == mapcss._value_capture(capture_tags, 0, u'buoy') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61b0be1b, u'^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$'), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9002001, 'subclass': 1481035998, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[landuse=conservation]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'conservation'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"boundary=protected_area"
                # fixAdd:"boundary=protected_area"
                # fixRemove:"landuse"
                err.append({'class': 9002001, 'subclass': 824801072, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'boundary',u'protected_area']]),
                    '-': ([
                    u'landuse'])
                }})

        # *[amenity=kiosk]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'kiosk'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=kiosk"
                # fixChangeKey:"amenity => shop"
                err.append({'class': 9002001, 'subclass': 1331930630, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=shop]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'shop'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=*"
                err.append({'class': 9002001, 'subclass': 1562207150, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=fishmonger]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fishmonger'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=seafood"
                # fixAdd:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 1376789416, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'seafood']])
                }})

        # *[shop=fish]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fish'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=fishing"
                # suggestAlternative:"shop=pet"
                # suggestAlternative:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 47191734, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=betting]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'betting'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=adult_gaming_centre"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1035501389, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=perfume]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'perfume'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=perfumery"
                # fixAdd:"shop=perfumery"
                err.append({'class': 9002001, 'subclass': 2075099676, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'perfumery']])
                }})

        # *[amenity=exercise_point]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'exercise_point'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=fitness_station"
                # fixRemove:"amenity"
                # fixAdd:"leisure=fitness_station"
                err.append({'class': 9002001, 'subclass': 1514920202, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure',u'fitness_station']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[shop=auto_parts]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'auto_parts'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=car_parts"
                # fixAdd:"shop=car_parts"
                err.append({'class': 9002001, 'subclass': 1675828779, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'car_parts']])
                }})

        # *[amenity=car_repair]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'car_repair'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=car_repair"
                # fixChangeKey:"amenity => shop"
                err.append({'class': 9002001, 'subclass': 1681273585, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=studio][type=audio]
        # *[amenity=studio][type=radio]
        # *[amenity=studio][type=television]
        # *[amenity=studio][type=video]
        if (u'amenity' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'audio'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'radio'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'television'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'video'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"studio"
                # fixChangeKey:"type => studio"
                err.append({'class': 9002001, 'subclass': 413401822, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'studio', mapcss.tag(tags, u'type')]]),
                    '-': ([
                    u'type'])
                }})

        # *[power=cable_distribution_cabinet]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'cable_distribution_cabinet'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=street_cabinet + street_cabinet=*"
                # fixAdd:"man_made=street_cabinet"
                # fixRemove:"power"
                err.append({'class': 9002001, 'subclass': 1007567078, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'street_cabinet']]),
                    '-': ([
                    u'power'])
                }})

        # *[power][location=kiosk]
        if (u'location' in keys and u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') and mapcss._tag_capture(capture_tags, 1, tags, u'location') == mapcss._value_capture(capture_tags, 1, u'kiosk'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # fixRemove:"location"
                # fixAdd:"man_made=street_cabinet"
                # fixAdd:"street_cabinet=power"
                err.append({'class': 9002001, 'subclass': 182905067, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'street_cabinet'],
                    [u'street_cabinet',u'power']]),
                    '-': ([
                    u'location'])
                }})

        # *[man_made=well]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'well'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1740864107, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=dog_bin]
        # *[amenity=dog_waste_bin]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'dog_bin'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'dog_waste_bin'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_basket + waste=dog_excrement + vending=excrement_bags"
                # fixAdd:"amenity=waste_basket"
                # fixAdd:"vending=excrement_bags"
                # fixAdd:"waste=dog_excrement"
                err.append({'class': 9002001, 'subclass': 2091877281, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'waste_basket'],
                    [u'vending',u'excrement_bags'],
                    [u'waste',u'dog_excrement']])
                }})

        # *[amenity=artwork]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'artwork'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=artwork"
                # fixRemove:"amenity"
                # fixAdd:"tourism=artwork"
                err.append({'class': 9002001, 'subclass': 728429076, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tourism',u'artwork']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=community_center]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'community_center'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre"
                # fixAdd:"amenity=community_centre"
                err.append({'class': 9002001, 'subclass': 690512681, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'community_centre']])
                }})

        # *[man_made=cut_line]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'cut_line'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=cutline"
                # fixAdd:"man_made=cutline"
                err.append({'class': 9002001, 'subclass': 1008752382, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'cutline']])
                }})

        # *[amenity=park]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'park'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=park"
                # fixRemove:"amenity"
                # fixAdd:"leisure=park"
                err.append({'class': 9002001, 'subclass': 2085280194, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure',u'park']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=hotel]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hotel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=hotel"
                # fixRemove:"amenity"
                # fixAdd:"tourism=hotel"
                err.append({'class': 9002001, 'subclass': 1341786818, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tourism',u'hotel']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[shop=window]
        # *[shop=windows]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'window'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'windows'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=window_construction"
                # fixAdd:"craft=window_construction"
                # fixRemove:"shop"
                err.append({'class': 9002001, 'subclass': 532391183, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'craft',u'window_construction']]),
                    '-': ([
                    u'shop'])
                }})

        # *[amenity=education]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'education'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=college"
                # suggestAlternative:"amenity=school"
                # suggestAlternative:"amenity=university"
                err.append({'class': 9002001, 'subclass': 796960259, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=gallery]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gallery'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=art"
                # fixAdd:"shop=art"
                err.append({'class': 9002001, 'subclass': 1319611546, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'art']])
                }})

        # *[shop=gambling]
        # *[leisure=gambling]
        if (u'leisure' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gambling'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'gambling'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1955724853, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[office=real_estate]
        # *[office=real_estate_agent]
        if (u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'real_estate'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'real_estate_agent'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"office=estate_agent"
                # fixAdd:"office=estate_agent"
                err.append({'class': 9002001, 'subclass': 2027311706, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'office',u'estate_agent']])
                }})

        # *[shop=glass]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'glass'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=glaziery"
                # suggestAlternative:"shop=glaziery"
                err.append({'class': 9002001, 'subclass': 712020531, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=proposed]
        # *[amenity=proposed]
        # *[amenity=disused]
        # *[shop=disused]
        # *[highway=abandoned]
        # *[historic=abandoned]
        if (u'amenity' in keys) or (u'highway' in keys) or (u'historic' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Use the {1}: key prefix instead.","{0.tag}","{0.value}")
                err.append({'class': 9002001, 'subclass': 1169228401, 'text': mapcss.tr(u'{0} is deprecated. Use the {1}: key prefix instead.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=swimming_pool]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'swimming_pool'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=swimming_pool"
                # fixChangeKey:"amenity => leisure"
                err.append({'class': 9002001, 'subclass': 2012807801, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=sauna]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'sauna'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=sauna"
                # fixChangeKey:"amenity => leisure"
                err.append({'class': 9002001, 'subclass': 1450116742, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[/^[^t][^i][^g].+_[0-9]$/][!/^note_[0-9]$/][!/^description_[0-9]$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_300dfa36) and not mapcss._tag_capture(capture_tags, 1, tags, self.re_3185ac6d) and not mapcss._tag_capture(capture_tags, 2, tags, self.re_6d27b157))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable key (ending with a number)")
                # throwWarning:tr("{0}","{0.key}")
                # assertNoMatch:"way description_3=foo"
                # assertMatch:"way name_1=foo"
                # assertNoMatch:"way note_2=foo"
                # assertNoMatch:"way tiger:name_base_1=bar"
                err.append({'class': 9002014, 'subclass': 2081989305, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[sport=skating]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'skating'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=ice_skating"
                # suggestAlternative:"sport=roller_skating"
                err.append({'class': 9002001, 'subclass': 170699177, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[barrier=wall][type=noise_barrier][!wall]
        # way[barrier=wall][type=noise_barrier][wall=noise_barrier]
        if (u'barrier' in keys and u'type' in keys) or (u'barrier' in keys and u'type' in keys and u'wall' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wall') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'noise_barrier') and not mapcss._tag_capture(capture_tags, 2, tags, u'wall'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wall') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'noise_barrier') and mapcss._tag_capture(capture_tags, 2, tags, u'wall') == mapcss._value_capture(capture_tags, 2, u'noise_barrier'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"wall=noise_barrier"
                # fixChangeKey:"type => wall"
                err.append({'class': 9002001, 'subclass': 1513752031, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'wall', mapcss.tag(tags, u'type')]]),
                    '-': ([
                    u'type'])
                }})

        # way[barrier=wall][type=noise_barrier][wall][wall!=noise_barrier]
        if (u'barrier' in keys and u'type' in keys and u'wall' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wall') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'noise_barrier') and mapcss._tag_capture(capture_tags, 2, tags, u'wall') and mapcss._tag_capture(capture_tags, 3, tags, u'wall') != mapcss._value_const_capture(capture_tags, 3, u'noise_barrier', u'noise_barrier'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"wall=noise_barrier"
                err.append({'class': 9002001, 'subclass': 2130256462, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[amenity=public_building]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'public_building'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"..."
                # suggestAlternative:"amenity=community_centre"
                # suggestAlternative:"amenity=hospital"
                # suggestAlternative:"amenity=townhall"
                # suggestAlternative:"building=hospital"
                # suggestAlternative:"building=public"
                # suggestAlternative:"leisure=sports_centre"
                # suggestAlternative:"office=government"
                err.append({'class': 9002001, 'subclass': 1295642010, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[office=administrative]
        if (u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'administrative'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"office=government"
                # fixAdd:"office=government"
                err.append({'class': 9002001, 'subclass': 213844674, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'office',u'government']])
                }})

        # *[vending=news_papers]
        if (u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'news_papers'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=newspapers"
                # fixAdd:"vending=newspapers"
                err.append({'class': 9002001, 'subclass': 1133820292, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'vending',u'newspapers']])
                }})

        # *[service=drive_through]
        if (u'service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'service') == mapcss._value_capture(capture_tags, 0, u'drive_through'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"service=drive-through"
                # fixAdd:"service=drive-through"
                err.append({'class': 9002001, 'subclass': 283545650, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'service',u'drive-through']])
                }})

        # *[noexit][noexit!=yes][noexit!=no]
        # way[highway=service][service][service!~/^(alley|drive-through|drive_through|driveway|emergency_access|parking_aisle|rest_area|slipway|yes)$/]
        # way[railway=rail][service][service!~/^(crossover|siding|spur|yard)$/]
        # way[waterway=canal][service][service!~/^(irrigation|transportation|water_power)$/]
        if (u'highway' in keys and u'service' in keys) or (u'noexit' in keys) or (u'railway' in keys and u'service' in keys) or (u'service' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') and mapcss._tag_capture(capture_tags, 1, tags, u'noexit') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'noexit') != mapcss._value_const_capture(capture_tags, 2, u'no', u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'service') and mapcss._tag_capture(capture_tags, 1, tags, u'service') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_51df498f, u'^(alley|drive-through|drive_through|driveway|emergency_access|parking_aisle|rest_area|slipway|yes)$'), mapcss._tag_capture(capture_tags, 2, tags, u'service')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'rail') and mapcss._tag_capture(capture_tags, 1, tags, u'service') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2fd4cdcf, u'^(crossover|siding|spur|yard)$'), mapcss._tag_capture(capture_tags, 2, tags, u'service')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'canal') and mapcss._tag_capture(capture_tags, 1, tags, u'service') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7a045a17, u'^(irrigation|transportation|water_power)$'), mapcss._tag_capture(capture_tags, 2, tags, u'service')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The key {0} has an uncommon value.","{1.key}")
                err.append({'class': 9002017, 'subclass': 806344140, 'text': mapcss.tr(u'The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name:botanical]
        if (u'name:botanical' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name:botanical'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"species"
                err.append({'class': 9002001, 'subclass': 1061429000, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[shop=souvenir]
        # *[shop=souvenirs]
        # *[shop=souveniers]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souvenir'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souvenirs'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souveniers'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=gift"
                # fixAdd:"shop=gift"
                err.append({'class': 9002001, 'subclass': 1794702946, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'gift']])
                }})

        # *[vending=animal_food]
        if (u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'animal_food'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=animal_feed"
                # fixAdd:"vending=animal_feed"
                err.append({'class': 9002001, 'subclass': 1077411296, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'vending',u'animal_feed']])
                }})

        # way[highway=emergency_access_point][phone][!emergency_telephone_code]
        if (u'highway' in keys and u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'emergency_access_point') and mapcss._tag_capture(capture_tags, 1, tags, u'phone') and not mapcss._tag_capture(capture_tags, 2, tags, u'emergency_telephone_code'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # fixChangeKey:"phone => emergency_telephone_code"
                err.append({'class': 9002001, 'subclass': 904792316, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency_telephone_code', mapcss.tag(tags, u'phone')]]),
                    '-': ([
                    u'phone'])
                }})

        # way[highway=emergency_access_point][phone=*emergency_telephone_code]
        if (u'highway' in keys and u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'emergency_access_point') and mapcss._tag_capture(capture_tags, 1, tags, u'phone') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'emergency_telephone_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # fixRemove:"phone"
                err.append({'class': 9002001, 'subclass': 3132845, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'phone'])
                }})

        # way[highway=emergency_access_point][phone][emergency_telephone_code][phone!=*emergency_telephone_code]
        if (u'emergency_telephone_code' in keys and u'highway' in keys and u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'emergency_access_point') and mapcss._tag_capture(capture_tags, 1, tags, u'phone') and mapcss._tag_capture(capture_tags, 2, tags, u'emergency_telephone_code') and mapcss._tag_capture(capture_tags, 3, tags, u'phone') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'emergency_telephone_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                err.append({'class': 9002001, 'subclass': 144379729, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[tracktype=1]
        if (u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') == mapcss._value_capture(capture_tags, 0, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade1"
                # fixAdd:"tracktype=grade1"
                err.append({'class': 9002018, 'subclass': 823078782, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tracktype',u'grade1']])
                }})

        # way[tracktype=2]
        if (u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') == mapcss._value_capture(capture_tags, 0, 2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade2"
                # fixAdd:"tracktype=grade2"
                err.append({'class': 9002018, 'subclass': 652259155, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tracktype',u'grade2']])
                }})

        # way[tracktype=3]
        if (u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') == mapcss._value_capture(capture_tags, 0, 3))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade3"
                # fixAdd:"tracktype=grade3"
                err.append({'class': 9002018, 'subclass': 1624412111, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tracktype',u'grade3']])
                }})

        # way[tracktype=4]
        if (u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') == mapcss._value_capture(capture_tags, 0, 4))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade4"
                # fixAdd:"tracktype=grade4"
                err.append({'class': 9002018, 'subclass': 808384986, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tracktype',u'grade4']])
                }})

        # way[tracktype=5]
        if (u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') == mapcss._value_capture(capture_tags, 0, 5))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade5"
                # fixAdd:"tracktype=grade5"
                err.append({'class': 9002018, 'subclass': 1050276122, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tracktype',u'grade5']])
                }})

        # way[tracktype][tracktype!~/^(1|2|3|4|5|grade1|grade2|grade3|grade4|grade5)$/]
        if (u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_047d5648, u'^(1|2|3|4|5|grade1|grade2|grade3|grade4|grade5)$'), mapcss._tag_capture(capture_tags, 1, tags, u'tracktype')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"tracktype=grade1"
                # suggestAlternative:"tracktype=grade2"
                # suggestAlternative:"tracktype=grade3"
                # suggestAlternative:"tracktype=grade4"
                # suggestAlternative:"tracktype=grade5"
                err.append({'class': 9002019, 'subclass': 1665196665, 'text': mapcss.tr(u'wrong value: {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=hunting_stand][lock=yes]
        # *[amenity=hunting_stand][lock=no]
        if (u'amenity' in keys and u'lock' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hunting_stand') and mapcss._tag_capture(capture_tags, 1, tags, u'lock') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hunting_stand') and mapcss._tag_capture(capture_tags, 1, tags, u'lock') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"lockable"
                # fixChangeKey:"lock => lockable"
                err.append({'class': 9002001, 'subclass': 1939599742, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'lockable', mapcss.tag(tags, u'lock')]]),
                    '-': ([
                    u'lock'])
                }})

        # *[amenity=advertising][!advertising]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'advertising') and not mapcss._tag_capture(capture_tags, 1, tags, u'advertising'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"advertising=*"
                err.append({'class': 9002001, 'subclass': 1696784412, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=advertising][advertising]
        if (u'advertising' in keys and u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'advertising') and mapcss._tag_capture(capture_tags, 1, tags, u'advertising'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"advertising=*"
                # fixRemove:"amenity"
                err.append({'class': 9002001, 'subclass': 1538706366, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'amenity'])
                }})

        # way[direction=up][incline=up]
        # way[direction=down][incline=down]
        # way[direction=up][!incline]
        # way[direction=down][!incline]
        if (u'direction' in keys) or (u'direction' in keys and u'incline' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') == mapcss._value_capture(capture_tags, 0, u'up') and mapcss._tag_capture(capture_tags, 1, tags, u'incline') == mapcss._value_capture(capture_tags, 1, u'up'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') == mapcss._value_capture(capture_tags, 0, u'down') and mapcss._tag_capture(capture_tags, 1, tags, u'incline') == mapcss._value_capture(capture_tags, 1, u'down'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') == mapcss._value_capture(capture_tags, 0, u'up') and not mapcss._tag_capture(capture_tags, 1, tags, u'incline'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') == mapcss._value_capture(capture_tags, 0, u'down') and not mapcss._tag_capture(capture_tags, 1, tags, u'incline'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                # fixChangeKey:"direction => incline"
                err.append({'class': 9002001, 'subclass': 1707030473, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'incline', mapcss.tag(tags, u'direction')]]),
                    '-': ([
                    u'direction'])
                }})

        # way[direction=up][incline][incline!=up]
        # way[direction=down][incline][incline!=down]
        if (u'direction' in keys and u'incline' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') == mapcss._value_capture(capture_tags, 0, u'up') and mapcss._tag_capture(capture_tags, 1, tags, u'incline') and mapcss._tag_capture(capture_tags, 2, tags, u'incline') != mapcss._value_const_capture(capture_tags, 2, u'up', u'up'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'direction') == mapcss._value_capture(capture_tags, 0, u'down') and mapcss._tag_capture(capture_tags, 1, tags, u'incline') and mapcss._tag_capture(capture_tags, 2, tags, u'incline') != mapcss._value_const_capture(capture_tags, 2, u'down', u'down'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 937812227, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building=true]
        # *[building="*"]
        # *[building=Y]
        # *[building=y]
        # *[building=1]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'true'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'*'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'Y'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'y'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"building=yes"
                # fixAdd:"building=yes"
                err.append({'class': 9002018, 'subclass': 596818855, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes']])
                }})

        # *[building=abandoned]
        # *[building=address]
        # *[building=bing]
        # *[building=collapsed]
        # *[building=damaged]
        # *[building=demolished]
        # *[building=disused]
        # *[building=fixme]
        # *[building=occupied]
        # *[building=razed]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'address'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'bing'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'collapsed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'damaged'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'demolished'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'fixme'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'occupied'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'razed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 938825828, 'text': mapcss.tr(u'{0} is not a building type.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building=other]
        # *[building=unclassified]
        # *[building=undefined]
        # *[building=unknown]
        # *[building=unidentified]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'other'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unclassified'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'undefined'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unidentified'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                # fixAdd:"building=yes"
                err.append({'class': 9002001, 'subclass': 48721080, 'text': mapcss.tr(u'{0} is not a building type.', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes']])
                }})

        # way[water=salt]
        # way[water=salt_pool]
        # way[water=salt_panne]
        # way[water=salt_pond]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'salt'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'salt_pool'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'salt_panne'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'salt_pond'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=salt_pond"
                # suggestAlternative:"salt=yes"
                err.append({'class': 9002001, 'subclass': 403932956, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[water=tidal]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'tidal'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tidal=yes"
                # fixAdd:"tidal=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 1201030806, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tidal',u'yes']]),
                    '-': ([
                    u'water'])
                }})

        # *[amenity=toilet]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'toilet'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"amenity=toilets"
                # fixAdd:"amenity=toilets"
                err.append({'class': 9002018, 'subclass': 440018606, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'toilets']])
                }})

        # way[power=busbar]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'busbar'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=line + line=busbar"
                # fixAdd:"line=busbar"
                # fixAdd:"power=line"
                err.append({'class': 9002001, 'subclass': 2001565557, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'line',u'busbar'],
                    [u'power',u'line']])
                }})

        # *[man_made=MDF]
        # *[man_made=telephone_exchange]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'MDF'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'telephone_exchange'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixRemove:"man_made"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 634698090, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'exchange']]),
                    '-': ([
                    u'man_made'])
                }})

        # *[building=central_office]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'central_office'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"building=yes"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1091970270, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes'],
                    [u'telecom',u'exchange']])
                }})

        # *[telecom=central_office]
        if (u'telecom' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'telecom') == mapcss._value_capture(capture_tags, 0, u'central_office'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1503278830, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'exchange']])
                }})

        # *[natural=waterfall]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'waterfall'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"waterway=waterfall"
                # fixChangeKey:"natural => waterway"
                err.append({'class': 9002001, 'subclass': 764711734, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'waterway', mapcss.tag(tags, u'natural')]]),
                    '-': ([
                    u'natural'])
                }})

        # *[religion=unitarian]
        if (u'religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'religion') == mapcss._value_capture(capture_tags, 0, u'unitarian'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"religion=unitarian_universalist"
                # fixAdd:"religion=unitarian_universalist"
                err.append({'class': 9002001, 'subclass': 9227331, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'religion',u'unitarian_universalist']])
                }})

        # *[shop=shopping_centre]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'shopping_centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=mall"
                # fixAdd:"shop=mall"
                err.append({'class': 9002001, 'subclass': 1448390566, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'mall']])
                }})

        # *[is_in]
        # way[/^is_in:.*$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'is_in'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_493fd1a6))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1865068642, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[sport=football]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'football'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=american_football"
                # suggestAlternative:"sport=australian_football"
                # suggestAlternative:"sport=canadian_football"
                # suggestAlternative:"sport=gaelic_games"
                # suggestAlternative:"sport=rugby_league"
                # suggestAlternative:"sport=rugby_union"
                # suggestAlternative:"sport=soccer"
                err.append({'class': 9002001, 'subclass': 73038577, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=common]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'common'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"designation=common"
                # suggestAlternative:"landuse=*"
                # suggestAlternative:"leisure=*"
                err.append({'class': 9002001, 'subclass': 157636301, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[cuisine=vegan]
        # *[cuisine=vegetarian]
        if (u'cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cuisine') == mapcss._value_capture(capture_tags, 0, u'vegan'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cuisine') == mapcss._value_capture(capture_tags, 0, u'vegetarian'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("diet:","{0.value}","=only")
                # suggestAlternative:concat("diet:","{0.value}","=yes")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 43604574, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[kitchen_hours]
        if (u'kitchen_hours' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kitchen_hours'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"opening_hours:kitchen"
                # fixChangeKey:"kitchen_hours => opening_hours:kitchen"
                err.append({'class': 9002001, 'subclass': 1088306802, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'opening_hours:kitchen', mapcss.tag(tags, u'kitchen_hours')]]),
                    '-': ([
                    u'kitchen_hours'])
                }})

        # *[shop=money_transfer]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'money_transfer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=money_transfer"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 1664997936, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'shop')]]),
                    '-': ([
                    u'shop'])
                }})

        # *[contact:google_plus]
        if (u'contact:google_plus' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'contact:google_plus'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"contact:google_plus"
                err.append({'class': 9002001, 'subclass': 1869461154, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'contact:google_plus'])
                }})

        # *[amenity=garages]
        # *[amenity=garage]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'garages'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'garage'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("building=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + parking=garage_boxes"
                # suggestAlternative:"landuse=garages"
                err.append({'class': 9002001, 'subclass': 863228118, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=winery]
        # *[amenity=winery]
        if (u'amenity' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'winery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'winery'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=winery"
                # suggestAlternative:"shop=wine"
                err.append({'class': 9002001, 'subclass': 1773574987, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=youth_centre]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'youth_centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre + community_centre=youth_centre"
                # fixAdd:"amenity=community_centre"
                # fixAdd:"community_centre=youth_centre"
                err.append({'class': 9002001, 'subclass': 1284929085, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'community_centre'],
                    [u'community_centre',u'youth_centre']])
                }})

        # *[building:type][building=yes]
        # *[building:type][!building]
        if (u'building' in keys and u'building:type' in keys) or (u'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and mapcss._tag_capture(capture_tags, 1, tags, u'building') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # fixChangeKey:"building:type => building"
                # assertNoMatch:"way building:type=church building=supermarket"
                # assertMatch:"way building:type=church building=yes"
                # assertMatch:"way building:type=church"
                err.append({'class': 9002001, 'subclass': 1927794430, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building', mapcss.tag(tags, u'building:type')]]),
                    '-': ([
                    u'building:type'])
                }})

        # *[building:type][building][building!=yes]
        if (u'building' in keys and u'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != mapcss._value_const_capture(capture_tags, 2, u'yes', u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # assertMatch:"way building:type=church building=supermarket"
                # assertNoMatch:"way building:type=church building=yes"
                # assertNoMatch:"way building:type=church"
                err.append({'class': 9002001, 'subclass': 1133239698, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[escalator]
        if (u'escalator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'escalator'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"highway=steps + conveying=*"
                err.append({'class': 9002001, 'subclass': 967271828, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[fenced]
        if (u'fenced' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fenced'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"barrier=fence"
                err.append({'class': 9002001, 'subclass': 1141285220, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[historic_name][!old_name]
        if (u'historic_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"old_name"
                # fixChangeKey:"historic_name => old_name"
                err.append({'class': 9002001, 'subclass': 1034538127, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'old_name', mapcss.tag(tags, u'historic_name')]]),
                    '-': ([
                    u'historic_name'])
                }})

        # *[historic_name][old_name]
        if (u'historic_name' in keys and u'old_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic_name') and mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"old_name"
                err.append({'class': 9002001, 'subclass': 30762614, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[landuse=field]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'field'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=farmland"
                # fixAdd:"landuse=farmland"
                err.append({'class': 9002001, 'subclass': 426261497, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'landuse',u'farmland']])
                }})

        # *[leisure=beach]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'beach'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=beach_resort"
                # suggestAlternative:"natural=beach"
                err.append({'class': 9002001, 'subclass': 1767286055, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=club]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'club'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"club=*"
                err.append({'class': 9002001, 'subclass': 1282397509, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=video_arcade]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'video_arcade'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=adult_gaming_centre"
                # suggestAlternative:"leisure=amusement_arcade"
                err.append({'class': 9002001, 'subclass': 1463909830, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[man_made=jetty]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'jetty'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=pier"
                # fixAdd:"man_made=pier"
                err.append({'class': 9002001, 'subclass': 192707176, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'pier']])
                }})

        # *[man_made=village_pump]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'village_pump'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=water_well"
                # fixAdd:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 423232686, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'water_well']])
                }})

        # *[man_made=water_tank]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'water_tank'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=storage_tank + content=water"
                # fixAdd:"content=water"
                # fixAdd:"man_made=storage_tank"
                err.append({'class': 9002001, 'subclass': 563629665, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'content',u'water'],
                    [u'man_made',u'storage_tank']])
                }})

        # *[natural=moor]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'moor'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=meadow + meadow=agricultural"
                # suggestAlternative:"natural=fell"
                # suggestAlternative:"natural=grassland"
                # suggestAlternative:"natural=heath"
                # suggestAlternative:"natural=scrub"
                # suggestAlternative:"natural=tundra"
                # suggestAlternative:"natural=wetland"
                err.append({'class': 9002001, 'subclass': 374637717, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[noexit=no][!fixme]
        if (u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') == mapcss._value_capture(capture_tags, 0, u'no') and not mapcss._tag_capture(capture_tags, 1, tags, u'fixme'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"fixme=continue"
                # fixAdd:"fixme=continue"
                # fixRemove:"noexit"
                err.append({'class': 9002001, 'subclass': 647435126, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'fixme',u'continue']]),
                    '-': ([
                    u'noexit'])
                }})

        # *[noexit=no][fixme]
        if (u'fixme' in keys and u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') == mapcss._value_capture(capture_tags, 0, u'no') and mapcss._tag_capture(capture_tags, 1, tags, u'fixme'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"fixme=continue"
                err.append({'class': 9002001, 'subclass': 881828009, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=dive]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'dive'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=scuba_diving"
                # fixAdd:"shop=scuba_diving"
                err.append({'class': 9002001, 'subclass': 1582968978, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'scuba_diving']])
                }})

        # *[shop=furnace]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'furnace'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=plumber"
                # suggestAlternative:"shop=fireplace"
                err.append({'class': 9002001, 'subclass': 1155821104, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=paragliding]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'paragliding'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=free_flying"
                # fixAdd:"sport=free_flying"
                err.append({'class': 9002001, 'subclass': 1531788430, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'free_flying']])
                }})

        # *[tourism=bed_and_breakfast]
        if (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'bed_and_breakfast'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=guest_house + guest_house=bed_and_breakfast"
                # fixAdd:"guest_house=bed_and_breakfast"
                # fixAdd:"tourism=guest_house"
                err.append({'class': 9002001, 'subclass': 954237438, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'guest_house',u'bed_and_breakfast'],
                    [u'tourism',u'guest_house']])
                }})

        # *[diaper=yes]
        # *[diaper=no]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper => changing_table"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 1957125311, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table', mapcss.tag(tags, u'diaper')]]),
                    '-': ([
                    u'diaper'])
                }})

        # *[diaper][diaper=~/^[1-9][0-9]*$/]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0f294fdf), mapcss._tag_capture(capture_tags, 1, tags, u'diaper')))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=yes + changing_table:count=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixAdd:"changing_table=yes"
                # fixChangeKey:"diaper => changing_table:count"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 2105051472, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table',u'yes'],
                    [u'changing_table:count', mapcss.tag(tags, u'diaper')]]),
                    '-': ([
                    u'diaper'])
                }})

        # *[diaper=room]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'room'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table=dedicated_room"
                # suggestAlternative:"changing_table=room"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 883202329, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[diaper]!.diaper_checked
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_diaper_checked and mapcss._tag_capture(capture_tags, 0, tags, u'diaper'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"changing_table"
                err.append({'class': 9002001, 'subclass': 693675339, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[diaper:male=yes]
        if (u'diaper:male' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:male') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=male_toilet"
                # fixAdd:"changing_table:location=male_toilet"
                # fixRemove:"diaper:male"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 799035479, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'male_toilet']]),
                    '-': ([
                    u'diaper:male'])
                }})

        # *[diaper:female=yes]
        if (u'diaper:female' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:female') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=female_toilet"
                # fixAdd:"changing_table:location=female_toilet"
                # fixRemove:"diaper:female"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1450901137, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'female_toilet']]),
                    '-': ([
                    u'diaper:female'])
                }})

        # *[diaper:unisex=yes]
        if (u'diaper:unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:unisex') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=unisex_toilet"
                # fixAdd:"changing_table:location=unisex_toilet"
                # fixRemove:"diaper:unisex"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1460378712, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'unisex_toilet']]),
                    '-': ([
                    u'diaper:unisex'])
                }})

        # *[diaper:wheelchair=yes]
        # *[diaper:wheelchair=no]
        if (u'diaper:wheelchair' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:wheelchair=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:wheelchair => changing_table:wheelchair"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1951967281, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:wheelchair', mapcss.tag(tags, u'diaper:wheelchair')]]),
                    '-': ([
                    u'diaper:wheelchair'])
                }})

        # *[diaper:fee=yes]
        # *[diaper:fee=no]
        if (u'diaper:fee' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:fee') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:fee') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:fee=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:fee => changing_table:fee"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 2008573526, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:fee', mapcss.tag(tags, u'diaper:fee')]]),
                    '-': ([
                    u'diaper:fee'])
                }})

        # *[/^diaper:/]!.diaper___checked
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_diaper___checked and mapcss._tag_capture(capture_tags, 0, tags, self.re_6029fe03))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","diaper:*")
                # suggestAlternative:"changing_table:*"
                err.append({'class': 9002001, 'subclass': 26578864, 'text': mapcss.tr(u'{0} is deprecated', u'diaper:*')})

        # *[changing_table][changing_table!~/^(yes|no|limited)$/]
        if (u'changing_table' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'changing_table') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_787405b1, u'^(yes|no|limited)$'), mapcss._tag_capture(capture_tags, 1, tags, u'changing_table')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"changing_table=limited"
                # suggestAlternative:"changing_table=no"
                # suggestAlternative:"changing_table=yes"
                err.append({'class': 9002019, 'subclass': 1965225408, 'text': mapcss.tr(u'wrong value: {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[roof:shape=half_hipped]
        if (u'roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:shape') == mapcss._value_capture(capture_tags, 0, u'half_hipped'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"roof:shape=half-hipped"
                # fixAdd:"roof:shape=half-hipped"
                err.append({'class': 9002001, 'subclass': 1548347123, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'roof:shape',u'half-hipped']])
                }})

        # *[bridge_name]
        if (u'bridge_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"bridge:name"
                # fixChangeKey:"bridge_name => bridge:name"
                err.append({'class': 9002001, 'subclass': 80069399, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:name', mapcss.tag(tags, u'bridge_name')]]),
                    '-': ([
                    u'bridge_name'])
                }})

        # *[access=public]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'public'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"access=yes"
                # fixAdd:"access=yes"
                err.append({'class': 9002001, 'subclass': 1115157097, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'access',u'yes']])
                }})

        # *[crossing=island]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') == mapcss._value_capture(capture_tags, 0, u'island'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"crossing:island=yes"
                # fixRemove:"crossing"
                # fixAdd:"crossing:island=yes"
                err.append({'class': 9002001, 'subclass': 1512561318, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'crossing:island',u'yes']]),
                    '-': ([
                    u'crossing'])
                }})

        # *[recycling:metal]
        if (u'recycling:metal' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'recycling:metal'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"recycling:scrap_metal"
                # fixChangeKey:"recycling:metal => recycling:scrap_metal"
                err.append({'class': 9002001, 'subclass': 474491272, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'recycling:scrap_metal', mapcss.tag(tags, u'recycling:metal')]]),
                    '-': ([
                    u'recycling:metal'])
                }})

        # *[shop=dog_grooming]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'dog_grooming'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet_grooming"
                # fixAdd:"shop=pet_grooming"
                err.append({'class': 9002001, 'subclass': 1073412885, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'pet_grooming']])
                }})

        # *[tower:type=anchor]
        # *[tower:type=suspension]
        if (u'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower:type') == mapcss._value_capture(capture_tags, 0, u'anchor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower:type') == mapcss._value_capture(capture_tags, 0, u'suspension'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"tower:type => line_attachment"
                err.append({'class': 9002001, 'subclass': 180380605, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'line_attachment', mapcss.tag(tags, u'tower:type')]]),
                    '-': ([
                    u'tower:type'])
                }})

        # way[barrier=embankment]
        if (u'barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'embankment'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"man_made=embankment"
                err.append({'class': 9002001, 'subclass': 2131554464, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[landuse=churchyard]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'churchyard'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=graveyard"
                # suggestAlternative:"landuse=religious"
                err.append({'class': 9002001, 'subclass': 1973571425, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sloped_curb=yes][!kerb]
        # *[sloped_curb=both][!kerb]
        if (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'yes') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'both') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=lowered"
                # fixAdd:"kerb=lowered"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 1906002413, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'kerb',u'lowered']]),
                    '-': ([
                    u'sloped_curb'])
                }})

        # *[sloped_curb=no][!kerb]
        if (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'no') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=yes"
                # fixAdd:"kerb=yes"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 893727015, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'kerb',u'yes']]),
                    '-': ([
                    u'sloped_curb'])
                }})

        # *[sloped_curb][sloped_curb!~/^(yes|both|no)$/][!kerb]
        # *[sloped_curb][kerb]
        if (u'kerb' in keys and u'sloped_curb' in keys) or (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_01eb1711, u'^(yes|both|no)$'), mapcss._tag_capture(capture_tags, 1, tags, u'sloped_curb')) and not mapcss._tag_capture(capture_tags, 2, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') and mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"kerb=*"
                err.append({'class': 9002001, 'subclass': 1682376745, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[unnamed=yes]
        if (u'unnamed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unnamed') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"noname=yes"
                # fixChangeKey:"unnamed => noname"
                err.append({'class': 9002001, 'subclass': 1901447020, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'noname', mapcss.tag(tags, u'unnamed')]]),
                    '-': ([
                    u'unnamed'])
                }})

        # way[segregated][segregated!=yes][segregated!=no]
        if (u'segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'segregated') and mapcss._tag_capture(capture_tags, 1, tags, u'segregated') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'segregated') != mapcss._value_const_capture(capture_tags, 2, u'no', u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9002020, 'subclass': 1585094150, 'text': mapcss.tr(u'unusual value of {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[bicycle:oneway]
        if (u'bicycle:oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bicycle:oneway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"oneway:bicycle"
                # fixChangeKey:"bicycle:oneway => oneway:bicycle"
                err.append({'class': 9002001, 'subclass': 919622980, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'oneway:bicycle', mapcss.tag(tags, u'bicycle:oneway')]]),
                    '-': ([
                    u'bicycle:oneway'])
                }})

        # *[building:height]
        if (u'building:height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:height'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"height"
                # fixChangeKey:"building:height => height"
                err.append({'class': 9002001, 'subclass': 1328174745, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'height', mapcss.tag(tags, u'building:height')]]),
                    '-': ([
                    u'building:height'])
                }})

        # *[building:min_height]
        if (u'building:min_height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:min_height'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"min_height"
                # fixChangeKey:"building:min_height => min_height"
                err.append({'class': 9002001, 'subclass': 1042683921, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'min_height', mapcss.tag(tags, u'building:min_height')]]),
                    '-': ([
                    u'building:min_height'])
                }})

        # way[highway][construction=yes][highway!=construction]
        if (u'construction' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'construction') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_const_capture(capture_tags, 2, u'construction', u'construction'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("highway=construction + construction=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"construction=minor"
                err.append({'class': 9002001, 'subclass': 585996498, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[car][amenity=charging_station]
        if (u'amenity' in keys and u'car' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'car') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'charging_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"motorcar"
                # fixChangeKey:"car => motorcar"
                err.append({'class': 9002001, 'subclass': 1165117414, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'motorcar', mapcss.tag(tags, u'car')]]),
                    '-': ([
                    u'car'])
                }})

        # *[navigationaid=approach_light]
        # *[navigationaid="ALS (Approach lighting system)"]
        if (u'navigationaid' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'navigationaid') == mapcss._value_capture(capture_tags, 0, u'approach_light'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'navigationaid') == mapcss._value_capture(capture_tags, 0, u'ALS (Approach lighting system)'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"navigationaid=als"
                # fixAdd:"navigationaid=als"
                err.append({'class': 9002001, 'subclass': 1577817081, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'navigationaid',u'als']])
                }})

        # *[water=riverbank][!natural]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'riverbank') and not mapcss._tag_capture(capture_tags, 1, tags, u'natural'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                err.append({'class': 9002001, 'subclass': 186872153, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'natural',u'water'],
                    [u'water',u'river']])
                }})

        # *[water=riverbank][natural]
        if (u'natural' in keys and u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'riverbank') and mapcss._tag_capture(capture_tags, 1, tags, u'natural'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 630806094, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_diaper___checked = set_diaper_checked = set_samecolor = False

        # *[barrier=wire_fence]
        if (u'barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wire_fence'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 1107799632, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'fence'],
                    [u'fence_type',u'chain_link']])
                }})

        # *[barrier=wood_fence]
        if (u'barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'wood_fence'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=wood"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=wood"
                err.append({'class': 9002001, 'subclass': 1412230714, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'fence'],
                    [u'fence_type',u'wood']])
                }})

        # *[highway=stile]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stile'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=stile"
                # fixAdd:"barrier=stile"
                # fixRemove:"highway"
                err.append({'class': 9002001, 'subclass': 1435678043, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'barrier',u'stile']]),
                    '-': ([
                    u'highway'])
                }})

        # *[highway=incline]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'incline'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 765169083, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[highway=incline_steep]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'incline_steep'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 1966772390, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[highway=unsurfaced]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'unsurfaced'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"highway=* + surface=unpaved"
                # fixAdd:"highway=road"
                # fixAdd:"surface=unpaved"
                err.append({'class': 9002001, 'subclass': 20631498, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'highway',u'road'],
                    [u'surface',u'unpaved']])
                }})

        # *[landuse=wood]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'wood'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=forest"
                # suggestAlternative:"natural=wood"
                err.append({'class': 9002001, 'subclass': 469903103, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[natural=marsh]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'marsh'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=wetland + wetland=marsh"
                # fixAdd:"natural=wetland"
                # fixAdd:"wetland=marsh"
                err.append({'class': 9002001, 'subclass': 1459865523, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'natural',u'wetland'],
                    [u'wetland',u'marsh']])
                }})

        # *[highway=byway]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'byway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 1844620979, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power_source]
        if (u'power_source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power_source'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"generator:source"
                err.append({'class': 9002001, 'subclass': 34751027, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[power_rating]
        if (u'power_rating' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power_rating'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"generator:output"
                err.append({'class': 9002001, 'subclass': 904750343, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[shop=antique]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'antique'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=antiques"
                # fixAdd:"shop=antiques"
                err.append({'class': 9002001, 'subclass': 596668979, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'antiques']])
                }})

        # *[shop=bags]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'bags'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=bag"
                # fixAdd:"shop=bag"
                err.append({'class': 9002001, 'subclass': 1709003584, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'bag']])
                }})

        # *[shop=fashion]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fashion'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=clothes"
                # fixAdd:"shop=clothes"
                err.append({'class': 9002001, 'subclass': 985619804, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'clothes']])
                }})

        # *[shop=organic]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'organic'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=* + organic=only"
                # suggestAlternative:"shop=* + organic=yes"
                err.append({'class': 9002001, 'subclass': 1959365145, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=pets]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'pets'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet"
                # fixAdd:"shop=pet"
                err.append({'class': 9002001, 'subclass': 290270098, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'pet']])
                }})

        # *[shop=pharmacy]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'pharmacy'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=pharmacy"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 350722657, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'shop')]]),
                    '-': ([
                    u'shop'])
                }})

        # *[bicycle_parking=sheffield]
        if (u'bicycle_parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bicycle_parking') == mapcss._value_capture(capture_tags, 0, u'sheffield'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bicycle_parking=stands"
                # fixAdd:"bicycle_parking=stands"
                err.append({'class': 9002001, 'subclass': 718874663, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bicycle_parking',u'stands']])
                }})

        # *[amenity=emergency_phone]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'emergency_phone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"emergency=phone"
                # fixRemove:"amenity"
                # fixAdd:"emergency=phone"
                err.append({'class': 9002001, 'subclass': 1108230656, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'phone']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[sport=gaelic_football]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'gaelic_football'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=gaelic_games"
                # fixAdd:"sport=gaelic_games"
                err.append({'class': 9002001, 'subclass': 1768681881, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'gaelic_games']])
                }})

        # *[power=station]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=plant"
                # suggestAlternative:"power=substation"
                err.append({'class': 9002001, 'subclass': 52025933, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[power=sub_station]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'sub_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=substation"
                # fixAdd:"power=substation"
                err.append({'class': 9002001, 'subclass': 1423074682, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'power',u'substation']])
                }})

        # *[location=rooftop]
        if (u'location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'location') == mapcss._value_capture(capture_tags, 0, u'rooftop'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location=roof"
                # fixAdd:"location=roof"
                err.append({'class': 9002001, 'subclass': 1028577225, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location',u'roof']])
                }})

        # *[generator:location]
        if (u'generator:location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:location'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"location"
                # fixChangeKey:"generator:location => location"
                err.append({'class': 9002001, 'subclass': 900615917, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'location', mapcss.tag(tags, u'generator:location')]]),
                    '-': ([
                    u'generator:location'])
                }})

        # *[generator:method=dam]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'dam'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-storage"
                # fixAdd:"generator:method=water-storage"
                err.append({'class': 9002001, 'subclass': 248819368, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-storage']])
                }})

        # *[generator:method=pumped-storage]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'pumped-storage'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 93454158, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-pumped-storage']])
                }})

        # *[generator:method=pumping]
        if (u'generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'generator:method') == mapcss._value_capture(capture_tags, 0, u'pumping'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 2115673716, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'generator:method',u'water-pumped-storage']])
                }})

        # *[fence_type=chain]
        if (u'fence_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fence_type') == mapcss._value_capture(capture_tags, 0, u'chain'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=chain"
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 19409288, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building=entrance]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'entrance'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"entrance"
                err.append({'class': 9002001, 'subclass': 306662985, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[board_type=board]
        if (u'board_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'board_type') == mapcss._value_capture(capture_tags, 0, u'board'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"board_type"
                err.append({'class': 9002001, 'subclass': 1150949316, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'board_type'])
                }})

        # *[man_made=measurement_station]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'measurement_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=monitoring_station"
                # fixAdd:"man_made=monitoring_station"
                err.append({'class': 9002001, 'subclass': 700465123, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'monitoring_station']])
                }})

        # *[measurement=water_level]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'water_level'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:water_level=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:water_level=yes"
                err.append({'class': 9002001, 'subclass': 634647702, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:water_level',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[measurement=weather]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'weather'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:weather=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:weather=yes"
                err.append({'class': 9002001, 'subclass': 336627227, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:weather',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[measurement=seismic]
        if (u'measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'measurement') == mapcss._value_capture(capture_tags, 0, u'seismic'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:seismic_activity=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:seismic_activity=yes"
                err.append({'class': 9002001, 'subclass': 1402131289, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:seismic_activity',u'yes']]),
                    '-': ([
                    u'measurement'])
                }})

        # *[monitoring:river_level]
        if (u'monitoring:river_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'monitoring:river_level'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"monitoring:water_level"
                # fixChangeKey:"monitoring:river_level => monitoring:water_level"
                err.append({'class': 9002001, 'subclass': 264907924, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'monitoring:water_level', mapcss.tag(tags, u'monitoring:river_level')]]),
                    '-': ([
                    u'monitoring:river_level'])
                }})

        # *[stay]
        if (u'stay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'stay'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"maxstay"
                # fixChangeKey:"stay => maxstay"
                err.append({'class': 9002001, 'subclass': 787370129, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'maxstay', mapcss.tag(tags, u'stay')]]),
                    '-': ([
                    u'stay'])
                }})

        # *[emergency=aed]
        if (u'emergency' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'emergency') == mapcss._value_capture(capture_tags, 0, u'aed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"emergency=defibrillator"
                # fixAdd:"emergency=defibrillator"
                err.append({'class': 9002001, 'subclass': 707111885, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'emergency',u'defibrillator']])
                }})

        # *[day_on][!restriction]
        # *[day_off][!restriction]
        # *[date_on][!restriction]
        # *[date_off][!restriction]
        # *[hour_on][!restriction]
        # *[hour_off][!restriction]
        if (u'date_off' in keys) or (u'date_on' in keys) or (u'day_off' in keys) or (u'day_on' in keys) or (u'hour_off' in keys) or (u'hour_on' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'day_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'day_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'date_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'date_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hour_on') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hour_off') and not mapcss._tag_capture(capture_tags, 1, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"*:conditional"
                err.append({'class': 9002001, 'subclass': 294264920, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[access=designated]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'designated'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' is meaningless, use more specific tags, e.g. ''{1}''","access=designated","bicycle=designated")
                err.append({'class': 9002002, 'subclass': 2057594338, 'text': mapcss.tr(u'\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', u'access=designated', u'bicycle=designated')})

        # *[access=official]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'official'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' does not specify the official mode of transportation, use ''{1}'' for example","access=official","bicycle=official")
                err.append({'class': 9002003, 'subclass': 1909133836, 'text': mapcss.tr(u'\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', u'access=official', u'bicycle=official')})

        # *[fixme=yes]
        # *[FIXME=yes]
        if (u'FIXME' in keys) or (u'fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fixme') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'FIXME') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Instead of ''{1}'' please give more information about what exactly should be fixed.","{0.key}","{0.value}")
                err.append({'class': 9002004, 'subclass': 136657482, 'text': mapcss.tr(u'{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name][name=~/^(?i)fixme$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.","{0.key}","{0.tag}")
                # fixRemove:"name"
                err.append({'class': 9002005, 'subclass': 642340557, 'text': mapcss.tr(u'Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'name'])
                }})

        # *[note][note=~/^(?i)fixme$/]
        if (u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'note') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, u'note')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.","{0.tag}")
                err.append({'class': 9002006, 'subclass': 1243120287, 'text': mapcss.tr(u'{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[type=broad_leaved]
        # *[type=broad_leafed]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'broad_leaved'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'broad_leafed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=broadleaved"
                # fixAdd:"leaf_type=broadleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 293968062, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'broadleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[wood=coniferous]
        # *[type=coniferous]
        # *[type=conifer]
        if (u'type' in keys) or (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'coniferous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'coniferous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'conifer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=needleleaved"
                # fixAdd:"leaf_type=needleleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 50517650, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'needleleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[wood=mixed]
        if (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'mixed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=mixed"
                # fixAdd:"leaf_type=mixed"
                # fixRemove:"wood"
                err.append({'class': 9002001, 'subclass': 235914603, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_type',u'mixed']]),
                    '-': ([
                    u'wood'])
                }})

        # *[wood=evergreen]
        # *[type=evergreen]
        if (u'type' in keys) or (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'evergreen'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'evergreen'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=evergreen"
                # fixAdd:"leaf_cycle=evergreen"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 747964532, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_cycle',u'evergreen']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[type=deciduous]
        # *[type=deciduos]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'deciduous'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'deciduos'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=deciduous"
                # fixAdd:"leaf_cycle=deciduous"
                # fixRemove:"type"
                err.append({'class': 9002001, 'subclass': 591116099, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leaf_cycle',u'deciduous']]),
                    '-': ([
                    u'type'])
                }})

        # *[wood=deciduous]
        if (u'wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wood') == mapcss._value_capture(capture_tags, 0, u'deciduous'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type + leaf_cycle"
                err.append({'class': 9002001, 'subclass': 1100223594, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[natural=land]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'land'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please use instead a multipolygon.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 94558529, 'text': mapcss.tr(u'{0} is deprecated. Please use instead a multipolygon.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=causeway]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'causeway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=low_water_crossing"
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"ford=yes"
                err.append({'class': 9002001, 'subclass': 461671124, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=swing]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'swing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge:movable=swing"
                # suggestAlternative:"bridge:structure=simple-suspension"
                err.append({'class': 9002001, 'subclass': 1047428067, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[bridge=suspension]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'suspension'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=yes + bridge:structure=suspension"
                # fixAdd:"bridge:structure=suspension"
                # fixAdd:"bridge=yes"
                err.append({'class': 9002001, 'subclass': 1157046268, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:structure',u'suspension'],
                    [u'bridge',u'yes']])
                }})

        # *[bridge=pontoon]
        if (u'bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') == mapcss._value_capture(capture_tags, 0, u'pontoon'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=yes + bridge:structure=floating"
                # fixAdd:"bridge:structure=floating"
                # fixAdd:"bridge=yes"
                err.append({'class': 9002001, 'subclass': 1195531951, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:structure',u'floating'],
                    [u'bridge',u'yes']])
                }})

        # *[fee=interval]
        # *[lit=interval]
        # *[supervised=interval]
        if (u'fee' in keys) or (u'lit' in keys) or (u'supervised' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fee') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lit') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'supervised') == mapcss._value_capture(capture_tags, 0, u'interval'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please specify interval by using opening_hours syntax","{0.tag}")
                err.append({'class': 9002001, 'subclass': 417886592, 'text': mapcss.tr(u'{0} is deprecated. Please specify interval by using opening_hours syntax', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[/josm\/ignore/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_5ee0acf2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwError:tr("{0} is deprecated. Please delete this object and use a private layer instead","{0.key}")
                # fixDeleteObject:this
                err.append({'class': 9002001, 'subclass': 1402743016, 'text': mapcss.tr(u'{0} is deprecated. Please delete this object and use a private layer instead', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[sport=diving]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'diving'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=cliff_diving"
                # suggestAlternative:"sport=scuba_diving"
                err.append({'class': 9002001, 'subclass': 590643159, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[parking=park_and_ride]
        if (u'parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'parking') == mapcss._value_capture(capture_tags, 0, u'park_and_ride'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + park_ride=yes"
                # fixAdd:"amenity=parking"
                # fixAdd:"park_ride=yes"
                # fixRemove:"parking"
                err.append({'class': 9002001, 'subclass': 1893516041, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'parking'],
                    [u'park_ride',u'yes']]),
                    '-': ([
                    u'parking'])
                }})

        # *[manhole=plain]
        # *[manhole=unknown]
        # *[manhole=yes]
        # *[police=yes]
        # *[traffic_calming=yes]
        # *[access=restricted]
        # *[barrier=yes]
        # *[aerialway=yes][!public_transport]
        # *[amenity=yes]
        # *[leisure=yes]
        # *[shop="*"]
        # *[shop=yes][amenity!=fuel]
        # *[craft=yes]
        # *[service=yes]
        # *[place=yes]
        if (u'access' in keys) or (u'aerialway' in keys) or (u'amenity' in keys) or (u'barrier' in keys) or (u'craft' in keys) or (u'leisure' in keys) or (u'manhole' in keys) or (u'place' in keys) or (u'police' in keys) or (u'service' in keys) or (u'shop' in keys) or (u'traffic_calming' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'plain'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'manhole') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'police') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'traffic_calming') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'restricted'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'barrier') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'yes') and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'*'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'fuel', u'fuel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'craft') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'service') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Please replace ''{1}'' by a specific value.","{0.key}","{0.value}")
                err.append({'class': 9002007, 'subclass': 1532935474, 'text': mapcss.tr(u'{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[place_name][!name]
        if (u'place_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be replaced with {1}","{0.key}","{1.key}")
                # fixChangeKey:"place_name => name"
                err.append({'class': 9002008, 'subclass': 1089331760, 'text': mapcss.tr(u'{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'name', mapcss.tag(tags, u'place_name')]]),
                    '-': ([
                    u'place_name'])
                }})

        # *[place][place_name=*name]
        if (u'place' in keys and u'place_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss._tag_capture(capture_tags, 1, tags, u'place_name') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} = {1}; remove {0}","{1.key}","{1.value}")
                # fixRemove:"{1.key}"
                err.append({'class': 9002009, 'subclass': 1116761280, 'text': mapcss.tr(u'{0} = {1}; remove {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # *[waterway=water_point]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'water_point'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=water_point"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 103347605, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'waterway')]]),
                    '-': ([
                    u'waterway'])
                }})

        # *[waterway=waste_disposal]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'waste_disposal'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_disposal"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 1963461348, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'waterway')]]),
                    '-': ([
                    u'waterway'])
                }})

        # *[waterway=mooring]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'mooring'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"mooring=yes"
                # fixAdd:"mooring=yes"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 81358738, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'mooring',u'yes']]),
                    '-': ([
                    u'waterway'])
                }})

        # *[building][levels]
        # *[building:part=yes][levels]
        if (u'building' in keys and u'levels' in keys) or (u'building:part' in keys and u'levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') and mapcss._tag_capture(capture_tags, 1, tags, u'levels'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:part') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'levels'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.key}")
                # suggestAlternative:"building:levels"
                # fixChangeKey:"levels => building:levels"
                err.append({'class': 9002001, 'subclass': 293177436, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building:levels', mapcss.tag(tags, u'levels')]]),
                    '-': ([
                    u'levels'])
                }})

        # *[protected_class]
        if (u'protected_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protected_class'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"protect_class"
                # fixChangeKey:"protected_class => protect_class"
                err.append({'class': 9002001, 'subclass': 716999373, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'protect_class', mapcss.tag(tags, u'protected_class')]]),
                    '-': ([
                    u'protected_class'])
                }})

        # *[kerb=unknown]
        # *[lock=unknown]
        # *[hide=unknown]
        # *[shelter=unknown]
        # *[access=unknown]
        # *[capacity:parent=unknown]
        # *[capacity:women=unknown]
        # *[capacity:disabled=unknown]
        # *[crossing=unknown]
        # *[foot=unknown]
        if (u'access' in keys) or (u'capacity:disabled' in keys) or (u'capacity:parent' in keys) or (u'capacity:women' in keys) or (u'crossing' in keys) or (u'foot' in keys) or (u'hide' in keys) or (u'kerb' in keys) or (u'lock' in keys) or (u'shelter' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kerb') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lock') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hide') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shelter') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:parent') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:women') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'capacity:disabled') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'foot') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unspecific tag {0}","{0.tag}")
                err.append({'class': 9002010, 'subclass': 1052866123, 'text': mapcss.tr(u'Unspecific tag {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=skiing]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'skiing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # suggestAlternative:tr("{0} + {1} + {2}","piste:type=*","piste:difficulty=*","piste:grooming=*")
                err.append({'class': 9002001, 'subclass': 1578959559, 'text': mapcss.tr(u'Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[waterway=wadi]
        if (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'wadi'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=valley"
                # suggestAlternative:"{0.key}=* + intermittent=yes"
                err.append({'class': 9002001, 'subclass': 719234223, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[drinkable]
        if (u'drinkable' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'drinkable'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"drinking_water"
                err.append({'class': 9002001, 'subclass': 1785584789, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[color][!colour]
        if (u'color' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'color') and not mapcss._tag_capture(capture_tags, 1, tags, u'colour'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour"
                # fixChangeKey:"color => colour"
                err.append({'class': 9002001, 'subclass': 1850270072, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'colour', mapcss.tag(tags, u'color')]]),
                    '-': ([
                    u'color'])
                }})

        # *[color][colour][color=*colour]
        if (u'color' in keys and u'colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'color') and mapcss._tag_capture(capture_tags, 1, tags, u'colour') and mapcss._tag_capture(capture_tags, 2, tags, u'color') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'colour')))
                except mapcss.RuleAbort: pass
            if match:
                # setsamecolor
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # suggestAlternative:"colour"
                # fixRemove:"color"
                set_samecolor = True
                err.append({'class': 9002001, 'subclass': 1825345743, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'color'])
                }})

        # *[color][colour]!.samecolor
        if (u'color' in keys and u'colour' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_samecolor and mapcss._tag_capture(capture_tags, 0, tags, u'color') and mapcss._tag_capture(capture_tags, 1, tags, u'colour'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                # suggestAlternative:"colour"
                err.append({'class': 9002001, 'subclass': 1064658218, 'text': mapcss.tr(u'{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[building:color][building:colour]!.samebuildingcolor
        # Use undeclared class samebuildingcolor

        # *[roof:color][roof:colour]!.sameroofcolor
        # Use undeclared class sameroofcolor

        # *[/:color/][!building:color][!roof:color][!gpxd:color]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_554de4c7) and not mapcss._tag_capture(capture_tags, 1, tags, u'building:color') and not mapcss._tag_capture(capture_tags, 2, tags, u'roof:color') and not mapcss._tag_capture(capture_tags, 3, tags, u'gpxd:color'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:":colour"
                err.append({'class': 9002001, 'subclass': 1632389707, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/color:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_0c5b5730))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour:"
                err.append({'class': 9002001, 'subclass': 1390370717, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/=|\+|\/|&|<|>|;|'|"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_620f4d52))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("key with uncommon character")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002011, 'subclass': 1752615188, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[/^.$/]
        # relation[/^..$/][!to]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_27210286))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62) and not mapcss._tag_capture(capture_tags, 1, tags, u'to'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uncommon short key")
                # assertMatch:"relation fo=bar"
                # assertNoMatch:"relation to=Berlin"
                err.append({'class': 9002012, 'subclass': 518970721, 'text': mapcss.tr(u'uncommon short key')})

        # *[sport=hockey]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'hockey'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=field_hockey"
                # suggestAlternative:"sport=ice_hockey"
                err.append({'class': 9002001, 'subclass': 651933474, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=billard]
        # *[sport=billards]
        # *[sport=billiard]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billards'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'billiard'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=billiards"
                # fixAdd:"sport=billiards"
                err.append({'class': 9002001, 'subclass': 1522897824, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'billiards']])
                }})

        # *[payment:credit_cards=yes]
        if (u'payment:credit_cards' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:credit_cards') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:mastercard=yes","payment:visa=yes")
                err.append({'class': 9002013, 'subclass': 705181097, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:mastercard=yes', u'payment:visa=yes')})

        # *[payment:debit_cards=yes]
        if (u'payment:debit_cards' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:debit_cards') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:maestro=yes","payment:girocard=yes")
                err.append({'class': 9002013, 'subclass': 679215558, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:maestro=yes', u'payment:girocard=yes')})

        # *[payment:electronic_purses=yes]
        if (u'payment:electronic_purses' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:electronic_purses') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:ep_geldkarte=yes","payment:ep_quick=yes")
                err.append({'class': 9002013, 'subclass': 1440457244, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:ep_geldkarte=yes', u'payment:ep_quick=yes')})

        # *[payment:cryptocurrencies=yes]
        if (u'payment:cryptocurrencies' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:cryptocurrencies') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.","{0.tag}","payment:bitcoin=yes","payment:litecoin=yes")
                err.append({'class': 9002013, 'subclass': 1325255949, 'text': mapcss.tr(u'{0} is inaccurate. Use separate tags for each specific type, e.g. {1} or {2}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'payment:bitcoin=yes', u'payment:litecoin=yes')})

        # *[payment:ep_quick]
        # *[payment:ep_cash]
        # *[payment:ep_proton]
        # *[payment:ep_chipknip]
        if (u'payment:ep_cash' in keys) or (u'payment:ep_chipknip' in keys) or (u'payment:ep_proton' in keys) or (u'payment:ep_quick' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_quick'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_cash'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_proton'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'payment:ep_chipknip'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 332575437, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[kp][highway=milestone]
        # *[kp][railway=milestone]
        # *[kp][waterway=milestone]
        if (u'highway' in keys and u'kp' in keys) or (u'kp' in keys and u'railway' in keys) or (u'kp' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kp') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"kp => distance"
                err.append({'class': 9002001, 'subclass': 1078799228, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'distance', mapcss.tag(tags, u'kp')]]),
                    '-': ([
                    u'kp'])
                }})

        # *[pk][highway=milestone]
        # *[pk][railway=milestone]
        # *[pk][waterway=milestone]
        if (u'highway' in keys and u'pk' in keys) or (u'pk' in keys and u'railway' in keys) or (u'pk' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'railway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pk') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') == mapcss._value_capture(capture_tags, 1, u'milestone'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"pk => distance"
                err.append({'class': 9002001, 'subclass': 719029418, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'distance', mapcss.tag(tags, u'pk')]]),
                    '-': ([
                    u'pk'])
                }})

        # *[postcode]
        if (u'postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'postcode'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"addr:postcode"
                # suggestAlternative:"postal_code"
                err.append({'class': 9002001, 'subclass': 1942523538, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[water=intermittent]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'intermittent'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"intermittent=yes"
                # fixAdd:"intermittent=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 813530321, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'intermittent',u'yes']]),
                    '-': ([
                    u'water'])
                }})

        # *[landuse=farm]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'farm'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=farmland"
                # suggestAlternative:"landuse=farmyard"
                err.append({'class': 9002001, 'subclass': 1968473048, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[seamark=buoy]["seamark:type"=~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if (u'seamark' in keys and u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark') == mapcss._value_capture(capture_tags, 0, u'buoy') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_61b0be1b), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                # fixRemove:"seamark"
                err.append({'class': 9002001, 'subclass': 1224401740, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'seamark'])
                }})

        # *[seamark=buoy]["seamark:type"!~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if (u'seamark' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark') == mapcss._value_capture(capture_tags, 0, u'buoy') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61b0be1b, u'^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$'), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9002001, 'subclass': 1481035998, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[landuse=conservation]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'conservation'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"boundary=protected_area"
                # fixAdd:"boundary=protected_area"
                # fixRemove:"landuse"
                err.append({'class': 9002001, 'subclass': 824801072, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'boundary',u'protected_area']]),
                    '-': ([
                    u'landuse'])
                }})

        # *[amenity=kiosk]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'kiosk'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=kiosk"
                # fixChangeKey:"amenity => shop"
                err.append({'class': 9002001, 'subclass': 1331930630, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=shop]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'shop'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=*"
                err.append({'class': 9002001, 'subclass': 1562207150, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=fishmonger]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fishmonger'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=seafood"
                # fixAdd:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 1376789416, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'seafood']])
                }})

        # *[shop=fish]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'fish'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=fishing"
                # suggestAlternative:"shop=pet"
                # suggestAlternative:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 47191734, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=betting]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'betting'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=adult_gaming_centre"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1035501389, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=perfume]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'perfume'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=perfumery"
                # fixAdd:"shop=perfumery"
                err.append({'class': 9002001, 'subclass': 2075099676, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'perfumery']])
                }})

        # *[amenity=exercise_point]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'exercise_point'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=fitness_station"
                # fixRemove:"amenity"
                # fixAdd:"leisure=fitness_station"
                err.append({'class': 9002001, 'subclass': 1514920202, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure',u'fitness_station']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[shop=auto_parts]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'auto_parts'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=car_parts"
                # fixAdd:"shop=car_parts"
                err.append({'class': 9002001, 'subclass': 1675828779, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'car_parts']])
                }})

        # *[amenity=car_repair]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'car_repair'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=car_repair"
                # fixChangeKey:"amenity => shop"
                err.append({'class': 9002001, 'subclass': 1681273585, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=studio][type=audio]
        # *[amenity=studio][type=radio]
        # *[amenity=studio][type=television]
        # *[amenity=studio][type=video]
        if (u'amenity' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'audio'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'radio'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'television'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'studio') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'video'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"studio"
                # fixChangeKey:"type => studio"
                err.append({'class': 9002001, 'subclass': 413401822, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'studio', mapcss.tag(tags, u'type')]]),
                    '-': ([
                    u'type'])
                }})

        # *[power=cable_distribution_cabinet]
        if (u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'cable_distribution_cabinet'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=street_cabinet + street_cabinet=*"
                # fixAdd:"man_made=street_cabinet"
                # fixRemove:"power"
                err.append({'class': 9002001, 'subclass': 1007567078, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'street_cabinet']]),
                    '-': ([
                    u'power'])
                }})

        # *[power][location=kiosk]
        if (u'location' in keys and u'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') and mapcss._tag_capture(capture_tags, 1, tags, u'location') == mapcss._value_capture(capture_tags, 1, u'kiosk'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # fixRemove:"location"
                # fixAdd:"man_made=street_cabinet"
                # fixAdd:"street_cabinet=power"
                err.append({'class': 9002001, 'subclass': 182905067, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'street_cabinet'],
                    [u'street_cabinet',u'power']]),
                    '-': ([
                    u'location'])
                }})

        # *[man_made=well]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'well'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1740864107, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=dog_bin]
        # *[amenity=dog_waste_bin]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'dog_bin'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'dog_waste_bin'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_basket + waste=dog_excrement + vending=excrement_bags"
                # fixAdd:"amenity=waste_basket"
                # fixAdd:"vending=excrement_bags"
                # fixAdd:"waste=dog_excrement"
                err.append({'class': 9002001, 'subclass': 2091877281, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'waste_basket'],
                    [u'vending',u'excrement_bags'],
                    [u'waste',u'dog_excrement']])
                }})

        # *[amenity=artwork]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'artwork'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=artwork"
                # fixRemove:"amenity"
                # fixAdd:"tourism=artwork"
                err.append({'class': 9002001, 'subclass': 728429076, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tourism',u'artwork']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=community_center]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'community_center'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre"
                # fixAdd:"amenity=community_centre"
                err.append({'class': 9002001, 'subclass': 690512681, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'community_centre']])
                }})

        # *[man_made=cut_line]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'cut_line'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=cutline"
                # fixAdd:"man_made=cutline"
                err.append({'class': 9002001, 'subclass': 1008752382, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'cutline']])
                }})

        # *[amenity=park]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'park'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=park"
                # fixRemove:"amenity"
                # fixAdd:"leisure=park"
                err.append({'class': 9002001, 'subclass': 2085280194, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure',u'park']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=hotel]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hotel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=hotel"
                # fixRemove:"amenity"
                # fixAdd:"tourism=hotel"
                err.append({'class': 9002001, 'subclass': 1341786818, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'tourism',u'hotel']]),
                    '-': ([
                    u'amenity'])
                }})

        # *[shop=window]
        # *[shop=windows]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'window'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'windows'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=window_construction"
                # fixAdd:"craft=window_construction"
                # fixRemove:"shop"
                err.append({'class': 9002001, 'subclass': 532391183, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'craft',u'window_construction']]),
                    '-': ([
                    u'shop'])
                }})

        # *[amenity=education]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'education'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=college"
                # suggestAlternative:"amenity=school"
                # suggestAlternative:"amenity=university"
                err.append({'class': 9002001, 'subclass': 796960259, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=gallery]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gallery'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=art"
                # fixAdd:"shop=art"
                err.append({'class': 9002001, 'subclass': 1319611546, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'art']])
                }})

        # *[shop=gambling]
        # *[leisure=gambling]
        if (u'leisure' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gambling'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'gambling'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1955724853, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[office=real_estate]
        # *[office=real_estate_agent]
        if (u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'real_estate'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'real_estate_agent'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"office=estate_agent"
                # fixAdd:"office=estate_agent"
                err.append({'class': 9002001, 'subclass': 2027311706, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'office',u'estate_agent']])
                }})

        # *[shop=glass]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'glass'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=glaziery"
                # suggestAlternative:"shop=glaziery"
                err.append({'class': 9002001, 'subclass': 712020531, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=proposed]
        # *[amenity=proposed]
        # *[amenity=disused]
        # *[shop=disused]
        # *[highway=abandoned]
        # *[historic=abandoned]
        if (u'amenity' in keys) or (u'highway' in keys) or (u'historic' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'proposed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Use the {1}: key prefix instead.","{0.tag}","{0.value}")
                err.append({'class': 9002001, 'subclass': 1169228401, 'text': mapcss.tr(u'{0} is deprecated. Use the {1}: key prefix instead.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=swimming_pool]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'swimming_pool'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=swimming_pool"
                # fixChangeKey:"amenity => leisure"
                err.append({'class': 9002001, 'subclass': 2012807801, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[amenity=sauna]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'sauna'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=sauna"
                # fixChangeKey:"amenity => leisure"
                err.append({'class': 9002001, 'subclass': 1450116742, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'leisure', mapcss.tag(tags, u'amenity')]]),
                    '-': ([
                    u'amenity'])
                }})

        # *[/^[^t][^i][^g].+_[0-9]$/][!/^note_[0-9]$/][!/^description_[0-9]$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_300dfa36) and not mapcss._tag_capture(capture_tags, 1, tags, self.re_3185ac6d) and not mapcss._tag_capture(capture_tags, 2, tags, self.re_6d27b157))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable key (ending with a number)")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002014, 'subclass': 2081989305, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[sport=skating]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'skating'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=ice_skating"
                # suggestAlternative:"sport=roller_skating"
                err.append({'class': 9002001, 'subclass': 170699177, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=public_building]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'public_building'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"..."
                # suggestAlternative:"amenity=community_centre"
                # suggestAlternative:"amenity=hospital"
                # suggestAlternative:"amenity=townhall"
                # suggestAlternative:"building=hospital"
                # suggestAlternative:"building=public"
                # suggestAlternative:"leisure=sports_centre"
                # suggestAlternative:"office=government"
                err.append({'class': 9002001, 'subclass': 1295642010, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[office=administrative]
        if (u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'administrative'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"office=government"
                # fixAdd:"office=government"
                err.append({'class': 9002001, 'subclass': 213844674, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'office',u'government']])
                }})

        # *[vending=news_papers]
        if (u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'news_papers'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=newspapers"
                # fixAdd:"vending=newspapers"
                err.append({'class': 9002001, 'subclass': 1133820292, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'vending',u'newspapers']])
                }})

        # *[service=drive_through]
        if (u'service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'service') == mapcss._value_capture(capture_tags, 0, u'drive_through'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"service=drive-through"
                # fixAdd:"service=drive-through"
                err.append({'class': 9002001, 'subclass': 283545650, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'service',u'drive-through']])
                }})

        # *[noexit][noexit!=yes][noexit!=no]
        if (u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') and mapcss._tag_capture(capture_tags, 1, tags, u'noexit') != mapcss._value_const_capture(capture_tags, 1, u'yes', u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'noexit') != mapcss._value_const_capture(capture_tags, 2, u'no', u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The key {0} has an uncommon value.","{1.key}")
                err.append({'class': 9002017, 'subclass': 1357403556, 'text': mapcss.tr(u'The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name:botanical]
        if (u'name:botanical' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name:botanical'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"species"
                err.append({'class': 9002001, 'subclass': 1061429000, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[shop=souvenir]
        # *[shop=souvenirs]
        # *[shop=souveniers]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souvenir'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souvenirs'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'souveniers'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=gift"
                # fixAdd:"shop=gift"
                err.append({'class': 9002001, 'subclass': 1794702946, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'gift']])
                }})

        # *[vending=animal_food]
        if (u'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'vending') == mapcss._value_capture(capture_tags, 0, u'animal_food'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=animal_feed"
                # fixAdd:"vending=animal_feed"
                err.append({'class': 9002001, 'subclass': 1077411296, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'vending',u'animal_feed']])
                }})

        # *[amenity=hunting_stand][lock=yes]
        # *[amenity=hunting_stand][lock=no]
        if (u'amenity' in keys and u'lock' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hunting_stand') and mapcss._tag_capture(capture_tags, 1, tags, u'lock') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'hunting_stand') and mapcss._tag_capture(capture_tags, 1, tags, u'lock') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"lockable"
                # fixChangeKey:"lock => lockable"
                err.append({'class': 9002001, 'subclass': 1939599742, 'text': mapcss.tr(u'{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'lockable', mapcss.tag(tags, u'lock')]]),
                    '-': ([
                    u'lock'])
                }})

        # *[amenity=advertising][!advertising]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'advertising') and not mapcss._tag_capture(capture_tags, 1, tags, u'advertising'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"advertising=*"
                err.append({'class': 9002001, 'subclass': 1696784412, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=advertising][advertising]
        if (u'advertising' in keys and u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'advertising') and mapcss._tag_capture(capture_tags, 1, tags, u'advertising'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"advertising=*"
                # fixRemove:"amenity"
                err.append({'class': 9002001, 'subclass': 1538706366, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'amenity'])
                }})

        # *[building=true]
        # *[building="*"]
        # *[building=Y]
        # *[building=y]
        # *[building=1]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'true'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'*'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'Y'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'y'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"building=yes"
                # fixAdd:"building=yes"
                err.append({'class': 9002018, 'subclass': 596818855, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes']])
                }})

        # *[building=abandoned]
        # *[building=address]
        # *[building=bing]
        # *[building=collapsed]
        # *[building=damaged]
        # *[building=demolished]
        # *[building=disused]
        # *[building=fixme]
        # *[building=occupied]
        # *[building=razed]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'address'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'bing'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'collapsed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'damaged'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'demolished'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'fixme'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'occupied'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'razed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 938825828, 'text': mapcss.tr(u'{0} is not a building type.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[building=other]
        # *[building=unclassified]
        # *[building=undefined]
        # *[building=unknown]
        # *[building=unidentified]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'other'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unclassified'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'undefined'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unknown'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'unidentified'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                # fixAdd:"building=yes"
                err.append({'class': 9002001, 'subclass': 48721080, 'text': mapcss.tr(u'{0} is not a building type.', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes']])
                }})

        # relation[water=salt]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'salt'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=salt_pond"
                # suggestAlternative:"salt=yes"
                err.append({'class': 9002001, 'subclass': 1845964412, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=toilet]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'toilet'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"amenity=toilets"
                # fixAdd:"amenity=toilets"
                err.append({'class': 9002018, 'subclass': 440018606, 'text': mapcss.tr(u'{0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'toilets']])
                }})

        # *[man_made=MDF]
        # *[man_made=telephone_exchange]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'MDF'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'telephone_exchange'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixRemove:"man_made"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 634698090, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'exchange']]),
                    '-': ([
                    u'man_made'])
                }})

        # *[building=central_office]
        if (u'building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building') == mapcss._value_capture(capture_tags, 0, u'central_office'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"building=yes"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1091970270, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building',u'yes'],
                    [u'telecom',u'exchange']])
                }})

        # *[telecom=central_office]
        if (u'telecom' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'telecom') == mapcss._value_capture(capture_tags, 0, u'central_office'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1503278830, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'telecom',u'exchange']])
                }})

        # *[natural=waterfall]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'waterfall'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"waterway=waterfall"
                # fixChangeKey:"natural => waterway"
                err.append({'class': 9002001, 'subclass': 764711734, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'waterway', mapcss.tag(tags, u'natural')]]),
                    '-': ([
                    u'natural'])
                }})

        # *[religion=unitarian]
        if (u'religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'religion') == mapcss._value_capture(capture_tags, 0, u'unitarian'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"religion=unitarian_universalist"
                # fixAdd:"religion=unitarian_universalist"
                err.append({'class': 9002001, 'subclass': 9227331, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'religion',u'unitarian_universalist']])
                }})

        # *[shop=shopping_centre]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'shopping_centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=mall"
                # fixAdd:"shop=mall"
                err.append({'class': 9002001, 'subclass': 1448390566, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'mall']])
                }})

        # *[is_in]
        if (u'is_in' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'is_in'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 981454091, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        # *[sport=football]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'football'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=american_football"
                # suggestAlternative:"sport=australian_football"
                # suggestAlternative:"sport=canadian_football"
                # suggestAlternative:"sport=gaelic_games"
                # suggestAlternative:"sport=rugby_league"
                # suggestAlternative:"sport=rugby_union"
                # suggestAlternative:"sport=soccer"
                err.append({'class': 9002001, 'subclass': 73038577, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=common]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'common'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"designation=common"
                # suggestAlternative:"landuse=*"
                # suggestAlternative:"leisure=*"
                err.append({'class': 9002001, 'subclass': 157636301, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[cuisine=vegan]
        # *[cuisine=vegetarian]
        if (u'cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cuisine') == mapcss._value_capture(capture_tags, 0, u'vegan'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cuisine') == mapcss._value_capture(capture_tags, 0, u'vegetarian'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("diet:","{0.value}","=only")
                # suggestAlternative:concat("diet:","{0.value}","=yes")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 43604574, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[kitchen_hours]
        if (u'kitchen_hours' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kitchen_hours'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"opening_hours:kitchen"
                # fixChangeKey:"kitchen_hours => opening_hours:kitchen"
                err.append({'class': 9002001, 'subclass': 1088306802, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'opening_hours:kitchen', mapcss.tag(tags, u'kitchen_hours')]]),
                    '-': ([
                    u'kitchen_hours'])
                }})

        # *[shop=money_transfer]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'money_transfer'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=money_transfer"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 1664997936, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity', mapcss.tag(tags, u'shop')]]),
                    '-': ([
                    u'shop'])
                }})

        # *[contact:google_plus]
        if (u'contact:google_plus' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'contact:google_plus'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"contact:google_plus"
                err.append({'class': 9002001, 'subclass': 1869461154, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'contact:google_plus'])
                }})

        # *[amenity=garages]
        # *[amenity=garage]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'garages'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'garage'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("building=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + parking=garage_boxes"
                # suggestAlternative:"landuse=garages"
                err.append({'class': 9002001, 'subclass': 863228118, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=winery]
        # *[amenity=winery]
        if (u'amenity' in keys) or (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'winery'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'winery'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=winery"
                # suggestAlternative:"shop=wine"
                err.append({'class': 9002001, 'subclass': 1773574987, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[amenity=youth_centre]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'youth_centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre + community_centre=youth_centre"
                # fixAdd:"amenity=community_centre"
                # fixAdd:"community_centre=youth_centre"
                err.append({'class': 9002001, 'subclass': 1284929085, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'community_centre'],
                    [u'community_centre',u'youth_centre']])
                }})

        # *[building:type][building=yes]
        # *[building:type][!building]
        if (u'building' in keys and u'building:type' in keys) or (u'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and mapcss._tag_capture(capture_tags, 1, tags, u'building') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # fixChangeKey:"building:type => building"
                err.append({'class': 9002001, 'subclass': 1927794430, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'building', mapcss.tag(tags, u'building:type')]]),
                    '-': ([
                    u'building:type'])
                }})

        # *[building:type][building][building!=yes]
        if (u'building' in keys and u'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:type') and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != mapcss._value_const_capture(capture_tags, 2, u'yes', u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                err.append({'class': 9002001, 'subclass': 1133239698, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[escalator]
        if (u'escalator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'escalator'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"highway=steps + conveying=*"
                err.append({'class': 9002001, 'subclass': 967271828, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[fenced]
        if (u'fenced' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fenced'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"barrier=fence"
                err.append({'class': 9002001, 'subclass': 1141285220, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[historic_name][!old_name]
        if (u'historic_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"old_name"
                # fixChangeKey:"historic_name => old_name"
                err.append({'class': 9002001, 'subclass': 1034538127, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'old_name', mapcss.tag(tags, u'historic_name')]]),
                    '-': ([
                    u'historic_name'])
                }})

        # *[historic_name][old_name]
        if (u'historic_name' in keys and u'old_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'historic_name') and mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"old_name"
                err.append({'class': 9002001, 'subclass': 30762614, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[landuse=field]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') == mapcss._value_capture(capture_tags, 0, u'field'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=farmland"
                # fixAdd:"landuse=farmland"
                err.append({'class': 9002001, 'subclass': 426261497, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'landuse',u'farmland']])
                }})

        # *[leisure=beach]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'beach'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=beach_resort"
                # suggestAlternative:"natural=beach"
                err.append({'class': 9002001, 'subclass': 1767286055, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=club]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'club'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"club=*"
                err.append({'class': 9002001, 'subclass': 1282397509, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=video_arcade]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'video_arcade'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=adult_gaming_centre"
                # suggestAlternative:"leisure=amusement_arcade"
                err.append({'class': 9002001, 'subclass': 1463909830, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[man_made=jetty]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'jetty'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=pier"
                # fixAdd:"man_made=pier"
                err.append({'class': 9002001, 'subclass': 192707176, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'pier']])
                }})

        # *[man_made=village_pump]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'village_pump'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=water_well"
                # fixAdd:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 423232686, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'water_well']])
                }})

        # *[man_made=water_tank]
        if (u'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'water_tank'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=storage_tank + content=water"
                # fixAdd:"content=water"
                # fixAdd:"man_made=storage_tank"
                err.append({'class': 9002001, 'subclass': 563629665, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'content',u'water'],
                    [u'man_made',u'storage_tank']])
                }})

        # *[natural=moor]
        if (u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'moor'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=meadow + meadow=agricultural"
                # suggestAlternative:"natural=fell"
                # suggestAlternative:"natural=grassland"
                # suggestAlternative:"natural=heath"
                # suggestAlternative:"natural=scrub"
                # suggestAlternative:"natural=tundra"
                # suggestAlternative:"natural=wetland"
                err.append({'class': 9002001, 'subclass': 374637717, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[noexit=no][!fixme]
        if (u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') == mapcss._value_capture(capture_tags, 0, u'no') and not mapcss._tag_capture(capture_tags, 1, tags, u'fixme'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"fixme=continue"
                # fixAdd:"fixme=continue"
                # fixRemove:"noexit"
                err.append({'class': 9002001, 'subclass': 647435126, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'fixme',u'continue']]),
                    '-': ([
                    u'noexit'])
                }})

        # *[noexit=no][fixme]
        if (u'fixme' in keys and u'noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noexit') == mapcss._value_capture(capture_tags, 0, u'no') and mapcss._tag_capture(capture_tags, 1, tags, u'fixme'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"fixme=continue"
                err.append({'class': 9002001, 'subclass': 881828009, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[shop=dive]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'dive'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=scuba_diving"
                # fixAdd:"shop=scuba_diving"
                err.append({'class': 9002001, 'subclass': 1582968978, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'scuba_diving']])
                }})

        # *[shop=furnace]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'furnace'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=plumber"
                # suggestAlternative:"shop=fireplace"
                err.append({'class': 9002001, 'subclass': 1155821104, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[sport=paragliding]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') == mapcss._value_capture(capture_tags, 0, u'paragliding'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=free_flying"
                # fixAdd:"sport=free_flying"
                err.append({'class': 9002001, 'subclass': 1531788430, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sport',u'free_flying']])
                }})

        # *[tourism=bed_and_breakfast]
        if (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'bed_and_breakfast'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tourism=guest_house + guest_house=bed_and_breakfast"
                # fixAdd:"guest_house=bed_and_breakfast"
                # fixAdd:"tourism=guest_house"
                err.append({'class': 9002001, 'subclass': 954237438, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'guest_house',u'bed_and_breakfast'],
                    [u'tourism',u'guest_house']])
                }})

        # *[diaper=yes]
        # *[diaper=no]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper => changing_table"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 1957125311, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table', mapcss.tag(tags, u'diaper')]]),
                    '-': ([
                    u'diaper'])
                }})

        # *[diaper][diaper=~/^[1-9][0-9]*$/]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0f294fdf), mapcss._tag_capture(capture_tags, 1, tags, u'diaper')))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=yes + changing_table:count=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixAdd:"changing_table=yes"
                # fixChangeKey:"diaper => changing_table:count"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 2105051472, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table',u'yes'],
                    [u'changing_table:count', mapcss.tag(tags, u'diaper')]]),
                    '-': ([
                    u'diaper'])
                }})

        # *[diaper=room]
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper') == mapcss._value_capture(capture_tags, 0, u'room'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper_checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table=dedicated_room"
                # suggestAlternative:"changing_table=room"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 883202329, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[diaper]!.diaper_checked
        if (u'diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_diaper_checked and mapcss._tag_capture(capture_tags, 0, tags, u'diaper'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"changing_table"
                err.append({'class': 9002001, 'subclass': 693675339, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[diaper:male=yes]
        if (u'diaper:male' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:male') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=male_toilet"
                # fixAdd:"changing_table:location=male_toilet"
                # fixRemove:"diaper:male"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 799035479, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'male_toilet']]),
                    '-': ([
                    u'diaper:male'])
                }})

        # *[diaper:female=yes]
        if (u'diaper:female' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:female') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=female_toilet"
                # fixAdd:"changing_table:location=female_toilet"
                # fixRemove:"diaper:female"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1450901137, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'female_toilet']]),
                    '-': ([
                    u'diaper:female'])
                }})

        # *[diaper:unisex=yes]
        if (u'diaper:unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:unisex') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=unisex_toilet"
                # fixAdd:"changing_table:location=unisex_toilet"
                # fixRemove:"diaper:unisex"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1460378712, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:location',u'unisex_toilet']]),
                    '-': ([
                    u'diaper:unisex'])
                }})

        # *[diaper:wheelchair=yes]
        # *[diaper:wheelchair=no]
        if (u'diaper:wheelchair' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:wheelchair=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:wheelchair => changing_table:wheelchair"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1951967281, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:wheelchair', mapcss.tag(tags, u'diaper:wheelchair')]]),
                    '-': ([
                    u'diaper:wheelchair'])
                }})

        # *[diaper:fee=yes]
        # *[diaper:fee=no]
        if (u'diaper:fee' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:fee') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'diaper:fee') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setdiaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:fee=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:fee => changing_table:fee"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 2008573526, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'changing_table:fee', mapcss.tag(tags, u'diaper:fee')]]),
                    '-': ([
                    u'diaper:fee'])
                }})

        # *[/^diaper:/]!.diaper___checked
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_diaper___checked and mapcss._tag_capture(capture_tags, 0, tags, self.re_6029fe03))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","diaper:*")
                # suggestAlternative:"changing_table:*"
                err.append({'class': 9002001, 'subclass': 26578864, 'text': mapcss.tr(u'{0} is deprecated', u'diaper:*')})

        # *[changing_table][changing_table!~/^(yes|no|limited)$/]
        if (u'changing_table' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'changing_table') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_787405b1, u'^(yes|no|limited)$'), mapcss._tag_capture(capture_tags, 1, tags, u'changing_table')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"changing_table=limited"
                # suggestAlternative:"changing_table=no"
                # suggestAlternative:"changing_table=yes"
                err.append({'class': 9002019, 'subclass': 1965225408, 'text': mapcss.tr(u'wrong value: {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[roof:shape=half_hipped]
        if (u'roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'roof:shape') == mapcss._value_capture(capture_tags, 0, u'half_hipped'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"roof:shape=half-hipped"
                # fixAdd:"roof:shape=half-hipped"
                err.append({'class': 9002001, 'subclass': 1548347123, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'roof:shape',u'half-hipped']])
                }})

        # *[bridge_name]
        if (u'bridge_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge_name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"bridge:name"
                # fixChangeKey:"bridge_name => bridge:name"
                err.append({'class': 9002001, 'subclass': 80069399, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge:name', mapcss.tag(tags, u'bridge_name')]]),
                    '-': ([
                    u'bridge_name'])
                }})

        # *[access=public]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'public'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"access=yes"
                # fixAdd:"access=yes"
                err.append({'class': 9002001, 'subclass': 1115157097, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'access',u'yes']])
                }})

        # *[crossing=island]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') == mapcss._value_capture(capture_tags, 0, u'island'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"crossing:island=yes"
                # fixRemove:"crossing"
                # fixAdd:"crossing:island=yes"
                err.append({'class': 9002001, 'subclass': 1512561318, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'crossing:island',u'yes']]),
                    '-': ([
                    u'crossing'])
                }})

        # *[recycling:metal]
        if (u'recycling:metal' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'recycling:metal'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"recycling:scrap_metal"
                # fixChangeKey:"recycling:metal => recycling:scrap_metal"
                err.append({'class': 9002001, 'subclass': 474491272, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'recycling:scrap_metal', mapcss.tag(tags, u'recycling:metal')]]),
                    '-': ([
                    u'recycling:metal'])
                }})

        # *[shop=dog_grooming]
        if (u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'dog_grooming'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet_grooming"
                # fixAdd:"shop=pet_grooming"
                err.append({'class': 9002001, 'subclass': 1073412885, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'shop',u'pet_grooming']])
                }})

        # *[tower:type=anchor]
        # *[tower:type=suspension]
        if (u'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower:type') == mapcss._value_capture(capture_tags, 0, u'anchor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tower:type') == mapcss._value_capture(capture_tags, 0, u'suspension'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"tower:type => line_attachment"
                err.append({'class': 9002001, 'subclass': 180380605, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'line_attachment', mapcss.tag(tags, u'tower:type')]]),
                    '-': ([
                    u'tower:type'])
                }})

        # *[sloped_curb=yes][!kerb]
        # *[sloped_curb=both][!kerb]
        if (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'yes') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'both') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=lowered"
                # fixAdd:"kerb=lowered"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 1906002413, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'kerb',u'lowered']]),
                    '-': ([
                    u'sloped_curb'])
                }})

        # *[sloped_curb=no][!kerb]
        if (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') == mapcss._value_capture(capture_tags, 0, u'no') and not mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=yes"
                # fixAdd:"kerb=yes"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 893727015, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'kerb',u'yes']]),
                    '-': ([
                    u'sloped_curb'])
                }})

        # *[sloped_curb][sloped_curb!~/^(yes|both|no)$/][!kerb]
        # *[sloped_curb][kerb]
        if (u'kerb' in keys and u'sloped_curb' in keys) or (u'sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_01eb1711, u'^(yes|both|no)$'), mapcss._tag_capture(capture_tags, 1, tags, u'sloped_curb')) and not mapcss._tag_capture(capture_tags, 2, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sloped_curb') and mapcss._tag_capture(capture_tags, 1, tags, u'kerb'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"kerb=*"
                err.append({'class': 9002001, 'subclass': 1682376745, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[unnamed=yes]
        if (u'unnamed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unnamed') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"noname=yes"
                # fixChangeKey:"unnamed => noname"
                err.append({'class': 9002001, 'subclass': 1901447020, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'noname', mapcss.tag(tags, u'unnamed')]]),
                    '-': ([
                    u'unnamed'])
                }})

        # *[building:height]
        if (u'building:height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:height'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"height"
                # fixChangeKey:"building:height => height"
                err.append({'class': 9002001, 'subclass': 1328174745, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'height', mapcss.tag(tags, u'building:height')]]),
                    '-': ([
                    u'building:height'])
                }})

        # *[building:min_height]
        if (u'building:min_height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:min_height'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"min_height"
                # fixChangeKey:"building:min_height => min_height"
                err.append({'class': 9002001, 'subclass': 1042683921, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'min_height', mapcss.tag(tags, u'building:min_height')]]),
                    '-': ([
                    u'building:min_height'])
                }})

        # *[car][amenity=charging_station]
        if (u'amenity' in keys and u'car' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'car') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'charging_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"motorcar"
                # fixChangeKey:"car => motorcar"
                err.append({'class': 9002001, 'subclass': 1165117414, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'motorcar', mapcss.tag(tags, u'car')]]),
                    '-': ([
                    u'car'])
                }})

        # *[navigationaid=approach_light]
        # *[navigationaid="ALS (Approach lighting system)"]
        if (u'navigationaid' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'navigationaid') == mapcss._value_capture(capture_tags, 0, u'approach_light'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'navigationaid') == mapcss._value_capture(capture_tags, 0, u'ALS (Approach lighting system)'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"navigationaid=als"
                # fixAdd:"navigationaid=als"
                err.append({'class': 9002001, 'subclass': 1577817081, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'navigationaid',u'als']])
                }})

        # *[water=riverbank][!natural]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'riverbank') and not mapcss._tag_capture(capture_tags, 1, tags, u'natural'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                err.append({'class': 9002001, 'subclass': 186872153, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'natural',u'water'],
                    [u'water',u'river']])
                }})

        # *[water=riverbank][natural]
        if (u'natural' in keys and u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') == mapcss._value_capture(capture_tags, 0, u'riverbank') and mapcss._tag_capture(capture_tags, 1, tags, u'natural'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 630806094, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_deprecated(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'day_on': u'0-12'}), expected={'class': 9002001, 'subclass': 294264920})
        self.check_err(n.node(data, {u'name': u'FIXME'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_err(n.node(data, {u'name': u'Fixme'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_err(n.node(data, {u'name': u'fixme'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_not_err(n.node(data, {u'name': u'valid name'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_err(n.node(data, {u'f': u'b'}), expected={'class': 9002012, 'subclass': 1803276827})
        self.check_err(n.node(data, {u'fo': u'bar'}), expected={'class': 9002012, 'subclass': 1803276827})
        self.check_not_err(n.node(data, {u'emergency_telephone_code': u'456', u'highway': u'emergency_access_point'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_not_err(n.node(data, {u'emergency_telephone_code': u'456', u'highway': u'emergency_access_point', u'phone': u'123'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_err(n.node(data, {u'highway': u'emergency_access_point', u'phone': u'123'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_not_err(n.node(data, {u'phone': u'123'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_not_err(n.node(data, {u'emergency_telephone_code': u'123', u'highway': u'emergency_access_point'}), expected={'class': 9002001, 'subclass': 342466099})
        self.check_err(n.node(data, {u'emergency_telephone_code': u'123', u'highway': u'emergency_access_point', u'phone': u'123'}), expected={'class': 9002001, 'subclass': 342466099})
        self.check_not_err(n.node(data, {u'highway': u'emergency_access_point', u'phone': u'123'}), expected={'class': 9002001, 'subclass': 342466099})
        self.check_not_err(n.node(data, {u'emergency_telephone_code': u'123', u'highway': u'emergency_access_point'}), expected={'class': 9002001, 'subclass': 663070970})
        self.check_not_err(n.node(data, {u'emergency_telephone_code': u'123', u'highway': u'emergency_access_point', u'phone': u'123'}), expected={'class': 9002001, 'subclass': 663070970})
        self.check_not_err(n.node(data, {u'highway': u'emergency_access_point', u'phone': u'123'}), expected={'class': 9002001, 'subclass': 663070970})
        self.check_not_err(n.way(data, {u'barrier': u'fence'}, [0]), expected={'class': 9002001, 'subclass': 1107799632})
        self.check_err(n.way(data, {u'barrier': u'wire_fence'}, [0]), expected={'class': 9002001, 'subclass': 1107799632})
        self.check_err(n.way(data, {u'access': u'designated'}, [0]), expected={'class': 9002002, 'subclass': 2057594338})
        self.check_err(n.way(data, {u'access': u'official'}, [0]), expected={'class': 9002003, 'subclass': 1909133836})
        self.check_err(n.way(data, {u'fixme': u'yes'}, [0]), expected={'class': 9002004, 'subclass': 136657482})
        self.check_err(n.way(data, {u'natural': u'land'}, [0]), expected={'class': 9002001, 'subclass': 94558529})
        self.check_not_err(n.way(data, {u'color': u'red', u'colour': u'red'}, [0]), expected={'class': 9002001, 'subclass': 1850270072})
        self.check_err(n.way(data, {u'color': u'red'}, [0]), expected={'class': 9002001, 'subclass': 1850270072})
        self.check_not_err(n.way(data, {u'color': u'red', u'colour': u'green'}, [0]), expected={'class': 9002001, 'subclass': 1825345743})
        self.check_err(n.way(data, {u'color': u'red', u'colour': u'red'}, [0]), expected={'class': 9002001, 'subclass': 1825345743})
        self.check_err(n.way(data, {u'color': u'red', u'colour': u'green'}, [0]), expected={'class': 9002001, 'subclass': 1064658218})
        self.check_not_err(n.way(data, {u'color': u'red', u'colour': u'red'}, [0]), expected={'class': 9002001, 'subclass': 1064658218})
        self.check_not_err(n.way(data, {u'color': u'red'}, [0]), expected={'class': 9002001, 'subclass': 1632389707})
        self.check_err(n.way(data, {u'cycleway:surface:color': u'grey'}, [0]), expected={'class': 9002001, 'subclass': 1632389707})
        self.check_not_err(n.way(data, {u'roof:color': u'grey'}, [0]), expected={'class': 9002001, 'subclass': 1632389707})
        self.check_err(n.way(data, {u'color:back': u'grey'}, [0]), expected={'class': 9002001, 'subclass': 1390370717})
        self.check_not_err(n.way(data, {u'color': u'red'}, [0]), expected={'class': 9002001, 'subclass': 1390370717})
        self.check_not_err(n.way(data, {u'route': u'ferry', u'to': u'Zuidschermer;Akersloot'}, [0]), expected={'class': 9002012, 'subclass': 1765060211})
        self.check_err(n.way(data, {u'to': u'bar'}, [0]), expected={'class': 9002012, 'subclass': 1765060211})
        self.check_not_err(n.way(data, {u'description_3': u'foo'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_err(n.way(data, {u'name_1': u'foo'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_not_err(n.way(data, {u'note_2': u'foo'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_not_err(n.way(data, {u'tiger:name_base_1': u'bar'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_not_err(n.way(data, {u'building': u'supermarket', u'building:type': u'church'}, [0]), expected={'class': 9002001, 'subclass': 1927794430})
        self.check_err(n.way(data, {u'building': u'yes', u'building:type': u'church'}, [0]), expected={'class': 9002001, 'subclass': 1927794430})
        self.check_err(n.way(data, {u'building:type': u'church'}, [0]), expected={'class': 9002001, 'subclass': 1927794430})
        self.check_err(n.way(data, {u'building': u'supermarket', u'building:type': u'church'}, [0]), expected={'class': 9002001, 'subclass': 1133239698})
        self.check_not_err(n.way(data, {u'building': u'yes', u'building:type': u'church'}, [0]), expected={'class': 9002001, 'subclass': 1133239698})
        self.check_not_err(n.way(data, {u'building:type': u'church'}, [0]), expected={'class': 9002001, 'subclass': 1133239698})
        self.check_err(n.relation(data, {u'fo': u'bar'}, []), expected={'class': 9002012, 'subclass': 518970721})
        self.check_not_err(n.relation(data, {u'to': u'Berlin'}, []), expected={'class': 9002012, 'subclass': 518970721})
