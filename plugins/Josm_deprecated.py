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
        self.errors[9002001] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('deprecated tagging'))
        self.errors[9002002] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', 'access=designated', 'bicycle=designated'))
        self.errors[9002003] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', 'access=official', 'bicycle=official'))
        self.errors[9002004] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}')))
        self.errors[9002005] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9002006] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9002007] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}')))
        self.errors[9002008] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), 'archaeological_site'))
        self.errors[9002011] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('key with uncommon character'))
        self.errors[9002012] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('uncommon short key'))
        self.errors[9002014] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('questionable key (ending with a number)'))
        self.errors[9002016] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('{0} is not recommended. Use the Reverse Ways function from the Tools menu.', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9002017] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, '{1.key}')))
        self.errors[9002018] = self.def_class(item = 9002, level = 2, tags = ["tag", "deprecated"], title = mapcss.tr('misspelled value'))
        self.errors[9002019] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9002020] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9002021] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('Unusual key {0}, maybe {1} or {2} is meant', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'level', 'building:levels'))
        self.errors[9002023] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('{0} with a temporary URL which may be outdated very soon', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9002024] = self.def_class(item = 9002, level = 3, tags = ["tag", "deprecated"], title = mapcss.tr('{0} is unspecific', mapcss._tag_uncapture(capture_tags, '{0.tag}')))

        self.re_01eb1711 = re.compile(r'^(yes|both|no)$')
        self.re_047d5648 = re.compile(r'^(1|2|3|4|5|grade1|grade2|grade3|grade4|grade5)$')
        self.re_0c5b5730 = re.compile(r'color:')
        self.re_0f294fdf = re.compile(r'^[1-9][0-9]*$')
        self.re_0fbae48f = re.compile(r'^https:\/\/westnordost.de\/p\/')
        self.re_1f92073a = re.compile(r'^(?i)fixme$')
        self.re_24dfeb95 = re.compile(r'^(tower|pole|insulator|portal|terminal)$')
        self.re_27210286 = re.compile(r'^.$')
        self.re_2f881233 = re.compile(r'^(?i)(bbq)$')
        self.re_2fd4cdcf = re.compile(r'^(crossover|siding|spur|yard)$')
        self.re_300dfa36 = re.compile(r'^[^t][^i][^g].+_[0-9]$')
        self.re_3185ac6d = re.compile(r'^note_[0-9]$')
        self.re_340a2b31 = re.compile(r'(?i)(;bbq|bbq;)')
        self.re_34c15d62 = re.compile(r'^..$')
        self.re_51df498f = re.compile(r'^(alley|drive-through|drive_through|driveway|emergency_access|parking_aisle|rest_area|slipway|yes)$')
        self.re_554de4c7 = re.compile(r':color')
        self.re_5ee0acf2 = re.compile(r'josm\/ignore')
        self.re_6029fe03 = re.compile(r'^diaper:')
        self.re_61b0be1b = re.compile(r'^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$')
        self.re_620f4d52 = re.compile(r'=|\+|\/|&|<|>|;|\'|\"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$')
        self.re_69ec353a = re.compile(r'^is_in:')
        self.re_6d27b157 = re.compile(r'^description_[0-9]$')
        self.re_787405b1 = re.compile(r'^(yes|no|limited)$')
        self.re_7a045a17 = re.compile(r'^(irrigation|transportation|water_power)$')
        self.re_7d409ed5 = re.compile(r'(?i)(_bbq)')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_bbq_autofix = set_beam_pump_no_mech = set_diaper___checked = set_diaper_checked = set_generic_power_tower_type_warning = set_levels_building = set_power_pole_type_warning = set_power_tower_type_warning = set_pumping_ring_no_mech = False

        # *[barrier=wire_fence]
        if ('barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wire_fence')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 1107799632, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['barrier','fence'],
                    ['fence_type','chain_link']])
                }})

        # *[barrier=wood_fence]
        if ('barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wood_fence')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=wood"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=wood"
                err.append({'class': 9002001, 'subclass': 1412230714, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['barrier','fence'],
                    ['fence_type','wood']])
                }})

        # node[highway=ford]
        # Rule Blacklisted (id: 1317841090)

        # *[highway=stile]
        # Rule Blacklisted (id: 1435678043)

        # *[highway=incline]
        # Rule Blacklisted (id: 765169083)

        # *[highway=incline_steep]
        # Rule Blacklisted (id: 1966772390)

        # *[highway=unsurfaced]
        # Rule Blacklisted (id: 20631498)

        # *[landuse=wood]
        # Rule Blacklisted (id: 469903103)

        # *[natural=marsh]
        # Rule Blacklisted (id: 1459865523)

        # *[highway=byway]
        # Rule Blacklisted (id: 1844620979)

        # *[power_source]
        # Rule Blacklisted (id: 34751027)

        # *[power_rating]
        # Rule Blacklisted (id: 904750343)

        # *[shop=antique]
        # Rule Blacklisted (id: 596668979)

        # *[shop=bags]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'bags')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=bag"
                # fixAdd:"shop=bag"
                err.append({'class': 9002001, 'subclass': 1709003584, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','bag']])
                }})

        # *[shop=fashion]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'fashion')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=clothes"
                # fixAdd:"shop=clothes"
                err.append({'class': 9002001, 'subclass': 985619804, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','clothes']])
                }})

        # *[shop=organic]
        # Rule Blacklisted (id: 1959365145)

        # *[shop=pets]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'pets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet"
                # fixAdd:"shop=pet"
                err.append({'class': 9002001, 'subclass': 290270098, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','pet']])
                }})

        # *[shop=pharmacy]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'pharmacy')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=pharmacy"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 350722657, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'shop')]]),
                    '-': ([
                    'shop'])
                }})

        # *[bicycle_parking=sheffield]
        if ('bicycle_parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle_parking') == mapcss._value_capture(capture_tags, 0, 'sheffield')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bicycle_parking=stands"
                # fixAdd:"bicycle_parking=stands"
                err.append({'class': 9002001, 'subclass': 718874663, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bicycle_parking','stands']])
                }})

        # *[amenity=emergency_phone]
        # Rule Blacklisted (id: 1108230656)

        # *[sport=gaelic_football]
        # Rule Blacklisted (id: 1768681881)

        # *[power=station]
        # Rule Blacklisted (id: 52025933)

        # *[power=sub_station]
        # Rule Blacklisted (id: 1423074682)

        # *[location=rooftop]
        if ('location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'location') == mapcss._value_capture(capture_tags, 0, 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location=roof"
                # fixAdd:"location=roof"
                err.append({'class': 9002001, 'subclass': 1028577225, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location','roof']])
                }})

        # *[generator:location]
        if ('generator:location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:location')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"location"
                # fixChangeKey:"generator:location => location"
                err.append({'class': 9002001, 'subclass': 900615917, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location', mapcss.tag(tags, 'generator:location')]]),
                    '-': ([
                    'generator:location'])
                }})

        # *[generator:method=dam]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'dam')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-storage"
                # fixAdd:"generator:method=water-storage"
                err.append({'class': 9002001, 'subclass': 248819368, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-storage']])
                }})

        # *[generator:method=pumped-storage]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'pumped-storage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 93454158, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-pumped-storage']])
                }})

        # *[generator:method=pumping]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'pumping')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 2115673716, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-pumped-storage']])
                }})

        # *[fence_type=chain]
        if ('fence_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fence_type') == mapcss._value_capture(capture_tags, 0, 'chain')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=chain"
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 19409288, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building=entrance]
        # Rule Blacklisted (id: 306662985)

        # *[board_type=board]
        if ('board_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'board_type') == mapcss._value_capture(capture_tags, 0, 'board')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"board_type"
                err.append({'class': 9002001, 'subclass': 1150949316, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'board_type'])
                }})

        # *[man_made=measurement_station]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'measurement_station')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=monitoring_station"
                # fixAdd:"man_made=monitoring_station"
                err.append({'class': 9002001, 'subclass': 700465123, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['man_made','monitoring_station']])
                }})

        # *[measurement=water_level]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'water_level')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:water_level=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:water_level=yes"
                err.append({'class': 9002001, 'subclass': 634647702, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:water_level','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[measurement=weather]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'weather')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:weather=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:weather=yes"
                err.append({'class': 9002001, 'subclass': 336627227, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:weather','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[measurement=seismic]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'seismic')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:seismic_activity=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:seismic_activity=yes"
                err.append({'class': 9002001, 'subclass': 1402131289, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:seismic_activity','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[monitoring:river_level]
        if ('monitoring:river_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'monitoring:river_level')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"monitoring:water_level"
                # fixChangeKey:"monitoring:river_level => monitoring:water_level"
                err.append({'class': 9002001, 'subclass': 264907924, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:water_level', mapcss.tag(tags, 'monitoring:river_level')]]),
                    '-': ([
                    'monitoring:river_level'])
                }})

        # *[stay]
        if ('stay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'stay')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"maxstay"
                # fixChangeKey:"stay => maxstay"
                err.append({'class': 9002001, 'subclass': 787370129, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxstay', mapcss.tag(tags, 'stay')]]),
                    '-': ([
                    'stay'])
                }})

        # *[emergency=aed]
        # Rule Blacklisted (id: 707111885)

        # *[day_on][!restriction]
        # *[day_off][!restriction]
        # *[date_on][!restriction]
        # *[date_off][!restriction]
        # *[hour_on][!restriction]
        # *[hour_off][!restriction]
        # Rule Blacklisted (id: 294264920)

        # *[access=designated]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'designated')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' is meaningless, use more specific tags, e.g. ''{1}''","access=designated","bicycle=designated")
                err.append({'class': 9002002, 'subclass': 2057594338, 'text': mapcss.tr('\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', 'access=designated', 'bicycle=designated')})

        # *[access=official]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'official')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' does not specify the official mode of transportation, use ''{1}'' for example","access=official","bicycle=official")
                err.append({'class': 9002003, 'subclass': 1909133836, 'text': mapcss.tr('\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', 'access=official', 'bicycle=official')})

        # *[fixme=yes]
        # *[FIXME=yes]
        if ('FIXME' in keys) or ('fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fixme') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'FIXME') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Instead of ''{1}'' please give more information about what exactly should be fixed.","{0.key}","{0.value}")
                err.append({'class': 9002004, 'subclass': 136657482, 'text': mapcss.tr('{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # *[name][name=~/^(?i)fixme$/]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.","{0.key}","{0.tag}")
                # fixRemove:"name"
                # assertMatch:"node name=FIXME"
                # assertMatch:"node name=Fixme"
                # assertMatch:"node name=fixme"
                # assertNoMatch:"node name=valid name"
                err.append({'class': 9002005, 'subclass': 642340557, 'text': mapcss.tr('Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'name'])
                }})

        # *[note][note=~/^(?i)fixme$/]
        if ('note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'note')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, 'note'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.","{0.tag}")
                err.append({'class': 9002006, 'subclass': 1243120287, 'text': mapcss.tr('{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[type=broad_leaved]
        # *[type=broad_leafed]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'broad_leaved')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'broad_leafed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=broadleaved"
                # fixAdd:"leaf_type=broadleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 293968062, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','broadleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=coniferous]
        # *[type=coniferous]
        # *[type=conifer]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'coniferous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'coniferous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'conifer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=needleleaved"
                # fixAdd:"leaf_type=needleleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 50517650, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','needleleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=mixed]
        if ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'mixed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=mixed"
                # fixAdd:"leaf_type=mixed"
                # fixRemove:"wood"
                err.append({'class': 9002001, 'subclass': 235914603, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','mixed']]),
                    '-': ([
                    'wood'])
                }})

        # *[wood=evergreen]
        # *[type=evergreen]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'evergreen')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'evergreen')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=evergreen"
                # fixAdd:"leaf_cycle=evergreen"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 747964532, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_cycle','evergreen']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=deciduous]
        # *[type=deciduous]
        # *[type=deciduos]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'deciduous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'deciduous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'deciduos')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=deciduous"
                # fixAdd:"leaf_cycle=deciduous"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1458103800, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_cycle','deciduous']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # node[type=palm]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'palm')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type"
                # suggestAlternative:"species"
                # suggestAlternative:"trees"
                err.append({'class': 9002001, 'subclass': 1453672853, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[natural=land]
        # Rule Blacklisted (id: 94558529)

        # *[bridge=causeway]
        if ('bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge') == mapcss._value_capture(capture_tags, 0, 'causeway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=low_water_crossing"
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"ford=yes"
                err.append({'class': 9002001, 'subclass': 461671124, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[bridge=swing]
        # Rule Blacklisted (id: 1047428067)

        # *[bridge=suspension]
        # Rule Blacklisted (id: 1157046268)

        # *[bridge=pontoon]
        # Rule Blacklisted (id: 1195531951)

        # *[fee=interval]
        # *[lit=interval]
        # *[supervised=interval]
        if ('fee' in keys) or ('lit' in keys) or ('supervised' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fee') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lit') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'supervised') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please specify interval by using opening_hours syntax","{0.tag}")
                err.append({'class': 9002001, 'subclass': 417886592, 'text': mapcss.tr('{0} is deprecated. Please specify interval by using opening_hours syntax', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/josm\/ignore/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_5ee0acf2)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwError:tr("{0} is deprecated. Please delete this object and use a private layer instead","{0.key}")
                # fixDeleteObject:this
                err.append({'class': 9002001, 'subclass': 1402743016, 'text': mapcss.tr('{0} is deprecated. Please delete this object and use a private layer instead', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[sport=diving]
        # Rule Blacklisted (id: 590643159)

        # *[parking=park_and_ride]
        if ('parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking') == mapcss._value_capture(capture_tags, 0, 'park_and_ride')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + park_ride=yes"
                # fixAdd:"amenity=parking"
                # fixAdd:"park_ride=yes"
                # fixRemove:"parking"
                err.append({'class': 9002001, 'subclass': 1893516041, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','parking'],
                    ['park_ride','yes']]),
                    '-': ([
                    'parking'])
                }})

        # *[parking=yes]
        # *[playground=yes]
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
        # *[landuse=yes]
        # *[shop="*"]
        # *[shop=yes][amenity!=fuel]
        # *[craft=yes]
        # *[service=yes]
        # *[place=yes]
        if ('access' in keys) or ('aerialway' in keys) or ('amenity' in keys) or ('barrier' in keys) or ('craft' in keys) or ('landuse' in keys) or ('leisure' in keys) or ('manhole' in keys) or ('parking' in keys) or ('place' in keys) or ('playground' in keys) or ('police' in keys) or ('service' in keys) or ('shop' in keys) or ('traffic_calming' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'playground') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'plain')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'unknown')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'police') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_calming') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'restricted')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'yes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'public_transport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, '*')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'fuel', 'fuel')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'craft') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Please replace ''{1}'' by a specific value.","{0.key}","{0.value}")
                err.append({'class': 9002007, 'subclass': 1452069773, 'text': mapcss.tr('{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # *[place_name][!name]
        # Rule Blacklisted (id: 1089331760)

        # *[place][place_name=*name]
        # Rule Blacklisted (id: 1116761280)

        # *[waterway=water_point]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'water_point')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=water_point"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 103347605, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'waterway')]]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=waste_disposal]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'waste_disposal')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_disposal"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 1963461348, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'waterway')]]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=mooring]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'mooring')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"mooring=yes"
                # fixAdd:"mooring=yes"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 81358738, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mooring','yes']]),
                    '-': ([
                    'waterway'])
                }})

        # *[building][levels]
        # *[building:part][levels]
        if ('building' in keys and 'levels' in keys) or ('building:part' in keys and 'levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')) and (mapcss._tag_capture(capture_tags, 1, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if match:
                # set levels_building
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.key}")
                # suggestAlternative:"building:levels"
                # fixChangeKey:"levels => building:levels"
                set_levels_building = True
                err.append({'class': 9002001, 'subclass': 869936714, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building:levels', mapcss.tag(tags, 'levels')]]),
                    '-': ([
                    'levels'])
                }})

        # *[levels]!.levels_building
        if ('levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_levels_building) and (mapcss._tag_capture(capture_tags, 0, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unusual key {0}, maybe {1} or {2} is meant","{0.key}","level","building:levels")
                err.append({'class': 9002021, 'subclass': 1172699526, 'text': mapcss.tr('Unusual key {0}, maybe {1} or {2} is meant', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'level', 'building:levels')})

        # *[protected_class]
        if ('protected_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'protected_class')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"protect_class"
                # fixChangeKey:"protected_class => protect_class"
                err.append({'class': 9002001, 'subclass': 716999373, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['protect_class', mapcss.tag(tags, 'protected_class')]]),
                    '-': ([
                    'protected_class'])
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
        # Rule Blacklisted (id: 1052866123)

        # *[sport=skiing]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'skiing')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # suggestAlternative:tr("{0} + {1} + {2}","piste:type=*","piste:difficulty=*","piste:grooming=*")
                err.append({'class': 9002001, 'subclass': 1578959559, 'text': mapcss.tr('Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[waterway=wadi]
        # Rule Blacklisted (id: 719234223)

        # *[drinkable]
        # Rule Blacklisted (id: 1785584789)

        # *[color][!colour]
        # Rule Blacklisted (id: 1850270072)

        # *[color][colour][color=*colour]
        # Rule Blacklisted (id: 1825345743)

        # *[color][colour]!.samecolor
        # Rule Blacklisted (id: 1064658218)

        # *[building:color][building:colour]!.samebuildingcolor
        # Rule Blacklisted (id: 740601387)

        # *[roof:color][roof:colour]!.sameroofcolor
        # Rule Blacklisted (id: 512779280)

        # *[/:color/][!building:color][!roof:color][!gpxd:color]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_554de4c7)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building:color')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'roof:color')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'gpxd:color')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:":colour"
                err.append({'class': 9002001, 'subclass': 1632389707, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/color:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_0c5b5730)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour:"
                err.append({'class': 9002001, 'subclass': 1390370717, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/=|\+|\/|&|<|>|;|'|"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_620f4d52)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("key with uncommon character")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002011, 'subclass': 1752615188, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/^.$/]
        # node[/^..$/][!kp][!pk]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_27210286)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kp')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'pk')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uncommon short key")
                # assertMatch:"node f=b"
                # assertMatch:"node fo=bar"
                # assertNoMatch:"node kp=5"
                # assertNoMatch:"node pk=7"
                err.append({'class': 9002012, 'subclass': 79709106, 'text': mapcss.tr('uncommon short key')})

        # *[sport=hockey]
        # Rule Blacklisted (id: 651933474)

        # *[sport=billard]
        # *[sport=billards]
        # *[sport=billiard]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billard')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billards')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billiard')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=billiards"
                # fixAdd:"sport=billiards"
                err.append({'class': 9002001, 'subclass': 1522897824, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['sport','billiards']])
                }})

        # *[payment:ep_quick]
        # *[payment:ep_cash]
        # *[payment:ep_proton]
        # *[payment:ep_chipknip]
        if ('payment:ep_cash' in keys) or ('payment:ep_chipknip' in keys) or ('payment:ep_proton' in keys) or ('payment:ep_quick' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_quick')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_cash')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_proton')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_chipknip')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 332575437, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[kp][railway!=milestone]
        if ('kp' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kp')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'milestone', 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"kp => distance"
                err.append({'class': 9002001, 'subclass': 1256703107, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['distance', mapcss.tag(tags, 'kp')]]),
                    '-': ([
                    'kp'])
                }})

        # *[pk][railway!=milestone]
        if ('pk' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pk')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'milestone', 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"pk => distance"
                err.append({'class': 9002001, 'subclass': 1339969759, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['distance', mapcss.tag(tags, 'pk')]]),
                    '-': ([
                    'pk'])
                }})

        # *[kp][railway=milestone]
        if ('kp' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kp')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"kp => railway:position"
                err.append({'class': 9002001, 'subclass': 1667272140, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'kp')]]),
                    '-': ([
                    'kp'])
                }})

        # *[pk][railway=milestone]
        if ('pk' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pk')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"pk => railway:position"
                err.append({'class': 9002001, 'subclass': 691355164, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'pk')]]),
                    '-': ([
                    'pk'])
                }})

        # *[distance][railway=milestone]
        if ('distance' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"distance => railway:position"
                err.append({'class': 9002001, 'subclass': 113691181, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'distance')]]),
                    '-': ([
                    'distance'])
                }})

        # *[postcode]
        if ('postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"addr:postcode"
                # suggestAlternative:"postal_code"
                err.append({'class': 9002001, 'subclass': 1942523538, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[water=intermittent]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'intermittent')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"intermittent=yes"
                # fixAdd:"intermittent=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 813530321, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['intermittent','yes']]),
                    '-': ([
                    'water'])
                }})

        # node[type][pipeline=marker]
        # Rule Blacklisted (id: 1878458659)

        # *[landuse=farm]
        # Rule Blacklisted (id: 1968473048)

        # *[seamark=buoy]["seamark:type"=~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if ('seamark' in keys and 'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seamark') == mapcss._value_capture(capture_tags, 0, 'buoy')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_61b0be1b), mapcss._tag_capture(capture_tags, 1, tags, 'seamark:type'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                # fixRemove:"seamark"
                err.append({'class': 9002001, 'subclass': 1224401740, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'seamark'])
                }})

        # *[seamark=buoy]["seamark:type"!~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if ('seamark' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seamark') == mapcss._value_capture(capture_tags, 0, 'buoy')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61b0be1b, '^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$'), mapcss._tag_capture(capture_tags, 1, tags, 'seamark:type'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9002001, 'subclass': 1481035998, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[landuse=conservation]
        if ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'conservation')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"boundary=protected_area"
                # fixAdd:"boundary=protected_area"
                # fixRemove:"landuse"
                err.append({'class': 9002001, 'subclass': 824801072, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['boundary','protected_area']]),
                    '-': ([
                    'landuse'])
                }})

        # *[amenity=kiosk]
        # Rule Blacklisted (id: 1331930630)

        # *[amenity=shop]
        # Rule Blacklisted (id: 1562207150)

        # *[shop=fishmonger]
        # Rule Blacklisted (id: 1376789416)

        # *[shop=fish]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'fish')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=fishing"
                # suggestAlternative:"shop=pet"
                # suggestAlternative:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 47191734, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=betting]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'betting')))
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
                err.append({'class': 9002001, 'subclass': 1035501389, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=perfume]
        # Rule Blacklisted (id: 2075099676)

        # *[amenity=exercise_point]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'exercise_point')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=fitness_station"
                # fixRemove:"amenity"
                # fixAdd:"leisure=fitness_station"
                err.append({'class': 9002001, 'subclass': 1514920202, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leisure','fitness_station']]),
                    '-': ([
                    'amenity'])
                }})

        # *[shop=auto_parts]
        # Rule Blacklisted (id: 1675828779)

        # *[amenity=car_repair]
        # Rule Blacklisted (id: 1681273585)

        # *[amenity=studio][type=audio]
        # *[amenity=studio][type=radio]
        # *[amenity=studio][type=television]
        # *[amenity=studio][type=video]
        if ('amenity' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'audio')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'radio')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'television')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'video')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"studio"
                # fixChangeKey:"type => studio"
                err.append({'class': 9002001, 'subclass': 413401822, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['studio', mapcss.tag(tags, 'type')]]),
                    '-': ([
                    'type'])
                }})

        # *[power=cable_distribution_cabinet]
        # Rule Blacklisted (id: 1007567078)

        # *[power][location=kiosk]
        if ('location' in keys and 'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power')) and (mapcss._tag_capture(capture_tags, 1, tags, 'location') == mapcss._value_capture(capture_tags, 1, 'kiosk')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # fixRemove:"location"
                # fixAdd:"man_made=street_cabinet"
                # fixAdd:"street_cabinet=power"
                err.append({'class': 9002001, 'subclass': 182905067, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['man_made','street_cabinet'],
                    ['street_cabinet','power']]),
                    '-': ([
                    'location'])
                }})

        # *[man_made=well]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'well')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1740864107, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=dog_bin]
        # *[amenity=dog_waste_bin]
        # Rule Blacklisted (id: 2091877281)

        # *[amenity=artwork]
        # Rule Blacklisted (id: 728429076)

        # *[amenity=community_center]
        # Rule Blacklisted (id: 690512681)

        # *[man_made=cut_line]
        # Rule Blacklisted (id: 1008752382)

        # *[amenity=park]
        # Rule Blacklisted (id: 2085280194)

        # *[amenity=hotel]
        # Rule Blacklisted (id: 1341786818)

        # *[shop=window]
        # *[shop=windows]
        # Rule Blacklisted (id: 532391183)

        # *[amenity=education]
        # Rule Blacklisted (id: 796960259)

        # *[shop=gallery]
        # Rule Blacklisted (id: 1319611546)

        # *[shop=gambling]
        # *[leisure=gambling]
        if ('leisure' in keys) or ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'gambling')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'gambling')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1955724853, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[office=real_estate]
        # *[office=real_estate_agent]
        # Rule Blacklisted (id: 2027311706)

        # *[shop=glass]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'glass')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=glaziery"
                # suggestAlternative:"shop=glaziery"
                err.append({'class': 9002001, 'subclass': 712020531, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=proposed]
        # *[amenity=disused]
        # *[shop=disused]
        # *[highway=abandoned]
        # *[historic=abandoned]
        # Rule Blacklisted (id: 847809313)

        # *[amenity=swimming_pool]
        # Rule Blacklisted (id: 2012807801)

        # *[amenity=sauna]
        # Rule Blacklisted (id: 1450116742)

        # *[/^[^t][^i][^g].+_[0-9]$/][!/^note_[0-9]$/][!/^description_[0-9]$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_300dfa36)) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_3185ac6d)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_6d27b157)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable key (ending with a number)")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002014, 'subclass': 2081989305, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[sport=skating]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'skating')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=ice_skating"
                # suggestAlternative:"sport=roller_skating"
                err.append({'class': 9002001, 'subclass': 170699177, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=public_building]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'public_building')))
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
                err.append({'class': 9002001, 'subclass': 1295642010, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[office=administrative]
        # Rule Blacklisted (id: 213844674)

        # *[vending=news_papers]
        if ('vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'news_papers')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=newspapers"
                # fixAdd:"vending=newspapers"
                err.append({'class': 9002001, 'subclass': 1133820292, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['vending','newspapers']])
                }})

        # *[service=drive_through]
        if ('service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service') == mapcss._value_capture(capture_tags, 0, 'drive_through')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"service=drive-through"
                # fixAdd:"service=drive-through"
                err.append({'class': 9002001, 'subclass': 283545650, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['service','drive-through']])
                }})

        # *[noexit][noexit!=yes][noexit!=no]
        if ('noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noexit')) and (mapcss._tag_capture(capture_tags, 1, tags, 'noexit') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noexit') != mapcss._value_const_capture(capture_tags, 2, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The key {0} has an uncommon value.","{1.key}")
                err.append({'class': 9002017, 'subclass': 1357403556, 'text': mapcss.tr('The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[name:botanical]
        # Rule Blacklisted (id: 1061429000)

        # node[pole=air_to_ground]
        # node[pole=transition]
        if ('pole' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole') == mapcss._value_capture(capture_tags, 0, 'air_to_ground')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole') == mapcss._value_capture(capture_tags, 0, 'transition')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"pole"
                err.append({'class': 9002001, 'subclass': 647400518, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location:transition','yes']]),
                    '-': ([
                    'pole'])
                }})

        # node[tower=air_to_ground]
        # node[tower=transition]
        if ('tower' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower') == mapcss._value_capture(capture_tags, 0, 'air_to_ground')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower') == mapcss._value_capture(capture_tags, 0, 'transition')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"tower"
                err.append({'class': 9002001, 'subclass': 1616290060, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location:transition','yes']]),
                    '-': ([
                    'tower'])
                }})

        # *[shop=souvenir]
        # *[shop=souvenirs]
        # *[shop=souveniers]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souvenir')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souvenirs')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souveniers')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=gift"
                # fixAdd:"shop=gift"
                err.append({'class': 9002001, 'subclass': 1794702946, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','gift']])
                }})

        # *[vending=animal_food]
        if ('vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'animal_food')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=animal_feed"
                # fixAdd:"vending=animal_feed"
                err.append({'class': 9002001, 'subclass': 1077411296, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['vending','animal_feed']])
                }})

        # node[vending=photos][amenity=vending_machine]
        # node[vending=photo][amenity=vending_machine]
        if ('amenity' in keys and 'vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'photos')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') == mapcss._value_capture(capture_tags, 1, 'vending_machine')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'photo')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') == mapcss._value_capture(capture_tags, 1, 'vending_machine')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=photo_booth"
                # fixAdd:"amenity=photo_booth"
                # fixRemove:"vending"
                err.append({'class': 9002001, 'subclass': 1387510120, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','photo_booth']]),
                    '-': ([
                    'vending'])
                }})

        # node[vending=photos][amenity!=vending_machine]
        if ('vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'photos')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'vending_machine', 'vending_machine')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=photo_booth"
                err.append({'class': 9002001, 'subclass': 1506790891, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[highway=emergency_access_point][phone][!emergency_telephone_code]
        if ('highway' in keys and 'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'emergency_telephone_code')))
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
                err.append({'class': 9002001, 'subclass': 1339208019, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['emergency_telephone_code', mapcss.tag(tags, 'phone')]]),
                    '-': ([
                    'phone'])
                }})

        # node[highway=emergency_access_point][phone=*emergency_telephone_code]
        if ('highway' in keys and 'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'emergency_telephone_code'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # fixRemove:"phone"
                # assertNoMatch:"node highway=emergency_access_point emergency_telephone_code=123"
                # assertMatch:"node highway=emergency_access_point phone=123 emergency_telephone_code=123"
                # assertNoMatch:"node highway=emergency_access_point phone=123"
                err.append({'class': 9002001, 'subclass': 342466099, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'phone'])
                }})

        # node[highway=emergency_access_point][phone][emergency_telephone_code][phone!=*emergency_telephone_code]
        if ('emergency_telephone_code' in keys and 'highway' in keys and 'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone')) and (mapcss._tag_capture(capture_tags, 2, tags, 'emergency_telephone_code')) and (mapcss._tag_capture(capture_tags, 3, tags, 'phone') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'emergency_telephone_code'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # assertNoMatch:"node highway=emergency_access_point emergency_telephone_code=123"
                # assertNoMatch:"node highway=emergency_access_point phone=123 emergency_telephone_code=123"
                # assertNoMatch:"node highway=emergency_access_point phone=123"
                err.append({'class': 9002001, 'subclass': 663070970, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=hunting_stand][lock=yes]
        # *[amenity=hunting_stand][lock=no]
        if ('amenity' in keys and 'lock' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'hunting_stand')) and (mapcss._tag_capture(capture_tags, 1, tags, 'lock') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'hunting_stand')) and (mapcss._tag_capture(capture_tags, 1, tags, 'lock') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"lockable"
                # fixChangeKey:"lock => lockable"
                err.append({'class': 9002001, 'subclass': 1939599742, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['lockable', mapcss.tag(tags, 'lock')]]),
                    '-': ([
                    'lock'])
                }})

        # *[amenity=advertising][!advertising]
        # Rule Blacklisted (id: 1696784412)

        # *[amenity=advertising][advertising]
        # Rule Blacklisted (id: 1538706366)

        # *[building=true]
        # *[building="*"]
        # *[building=Y]
        # *[building=y]
        # *[building=1]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'true')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, '*')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'Y')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'y')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 1)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"building=yes"
                # fixAdd:"building=yes"
                err.append({'class': 9002018, 'subclass': 596818855, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes']])
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
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'abandoned')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'address')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'bing')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'collapsed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'damaged')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'demolished')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'disused')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'fixme')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'occupied')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'razed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 938825828, 'text': mapcss.tr('{0} is not a building type.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building=other]
        # *[building=unclassified]
        # *[building=undefined]
        # *[building=unknown]
        # *[building=unidentified]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'other')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unclassified')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'undefined')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unknown')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unidentified')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                # fixAdd:"building=yes"
                err.append({'class': 9002001, 'subclass': 48721080, 'text': mapcss.tr('{0} is not a building type.', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes']])
                }})

        # node[power=transformer][location=pole][transformer]
        if ('location' in keys and 'power' in keys and 'transformer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'transformer')) and (mapcss._tag_capture(capture_tags, 1, tags, 'location') == mapcss._value_capture(capture_tags, 1, 'pole')) and (mapcss._tag_capture(capture_tags, 2, tags, 'transformer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # fixChangeKey:"location => power"
                err.append({'class': 9002001, 'subclass': 161456790, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['power', mapcss.tag(tags, 'location')]]),
                    '-': ([
                    'location'])
                }})

        # node[power=transformer][location=pole][!transformer]
        if ('location' in keys and 'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'transformer')) and (mapcss._tag_capture(capture_tags, 1, tags, 'location') == mapcss._value_capture(capture_tags, 1, 'pole')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'transformer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # fixChangeKey:"location => power"
                # fixAdd:"transformer=yes"
                err.append({'class': 9002001, 'subclass': 1830605870, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['power', mapcss.tag(tags, 'location')],
                    ['transformer','yes']]),
                    '-': ([
                    'location'])
                }})

        # node[tourism=picnic_table]
        # node[amenity=picnic_table]
        # node[leisure=picnic]
        # node[leisure=picnic_site]
        if ('amenity' in keys) or ('leisure' in keys) or ('tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tourism') == mapcss._value_capture(capture_tags, 0, 'picnic_table')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'picnic_table')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'picnic')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'picnic_site')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=picnic_table"
                # suggestAlternative:"tourism=picnic_site"
                err.append({'class': 9002001, 'subclass': 480506019, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=toilet]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'toilet')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"amenity=toilets"
                # fixAdd:"amenity=toilets"
                err.append({'class': 9002018, 'subclass': 440018606, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','toilets']])
                }})

        # *[man_made=MDF]
        # *[man_made=telephone_exchange]
        # Rule Blacklisted (id: 634698090)

        # *[building=central_office]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'central_office')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"building=yes"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1091970270, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes'],
                    ['telecom','exchange']])
                }})

        # *[telecom=central_office]
        # Rule Blacklisted (id: 1503278830)

        # node[communication=outdoor_dslam]
        # node[man_made=outdoor_dslam]
        # node[street_cabinet=outdoor_dslam]
        if ('communication' in keys) or ('man_made' in keys) or ('street_cabinet' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'communication') == mapcss._value_capture(capture_tags, 0, 'outdoor_dslam')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'outdoor_dslam')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'street_cabinet') == mapcss._value_capture(capture_tags, 0, 'outdoor_dslam')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=service_device"
                # fixAdd:"telecom=service_device"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1243371306, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['telecom','service_device']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # node[telecom=dslam]
        # node[telecom=outdoor_dslam]
        if ('telecom' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'telecom') == mapcss._value_capture(capture_tags, 0, 'dslam')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'telecom') == mapcss._value_capture(capture_tags, 0, 'outdoor_dslam')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=service_device"
                # fixAdd:"telecom=service_device"
                err.append({'class': 9002001, 'subclass': 781930166, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['telecom','service_device']])
                }})

        # node[amenity=fire_hydrant]
        # Rule Blacklisted (id: 967497433)

        # node[fire_hydrant:type=pond]
        if ('fire_hydrant:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fire_hydrant:type') == mapcss._value_capture(capture_tags, 0, 'pond')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"water_source=pond"
                # fixAdd:"water_source=pond"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1583105855, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['water_source','pond']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # node[fire_hydrant:flow_capacity]
        if ('fire_hydrant:flow_capacity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fire_hydrant:flow_capacity')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"flow_rate"
                err.append({'class': 9002001, 'subclass': 1864683984, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[emergency=fire_hydrant][in_service=no]
        if ('emergency' in keys and 'in_service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'fire_hydrant')) and (mapcss._tag_capture(capture_tags, 1, tags, 'in_service') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"disused:emergency=fire_hydrant"
                # fixAdd:"disused:emergency=fire_hydrant"
                # fixRemove:"{0.key}"
                # fixRemove:"{1.key}"
                err.append({'class': 9002001, 'subclass': 552149777, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['disused:emergency','fire_hydrant']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}'),
                    mapcss._tag_uncapture(capture_tags, '{1.key}')])
                }})

        # node[fire_hydrant:water_source]
        if ('fire_hydrant:water_source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fire_hydrant:water_source')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"water_source"
                # fixChangeKey:"fire_hydrant:water_source => water_source"
                err.append({'class': 9002001, 'subclass': 1207497718, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['water_source', mapcss.tag(tags, 'fire_hydrant:water_source')]]),
                    '-': ([
                    'fire_hydrant:water_source'])
                }})

        # *[natural=waterfall]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'waterfall')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"waterway=waterfall"
                # fixChangeKey:"natural => waterway"
                err.append({'class': 9002001, 'subclass': 764711734, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['waterway', mapcss.tag(tags, 'natural')]]),
                    '-': ([
                    'natural'])
                }})

        # *[religion=unitarian]
        if ('religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'religion') == mapcss._value_capture(capture_tags, 0, 'unitarian')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"religion=unitarian_universalist"
                # fixAdd:"religion=unitarian_universalist"
                err.append({'class': 9002001, 'subclass': 9227331, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['religion','unitarian_universalist']])
                }})

        # *[shop=shopping_centre]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'shopping_centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=mall"
                # fixAdd:"shop=mall"
                err.append({'class': 9002001, 'subclass': 1448390566, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','mall']])
                }})

        # *[is_in]
        # node[/^is_in:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_69ec353a)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1024340790, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[sport=football]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'football')))
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
                err.append({'class': 9002001, 'subclass': 73038577, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[leisure=common]
        if ('leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'common')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"designation=common"
                # suggestAlternative:"landuse=*"
                # suggestAlternative:"leisure=*"
                err.append({'class': 9002001, 'subclass': 157636301, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[cuisine=vegan]
        # *[cuisine=vegetarian]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine') == mapcss._value_capture(capture_tags, 0, 'vegan')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine') == mapcss._value_capture(capture_tags, 0, 'vegetarian')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("diet:","{0.value}","=only")
                # suggestAlternative:concat("diet:","{0.value}","=yes")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 43604574, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[kitchen_hours]
        if ('kitchen_hours' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kitchen_hours')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"opening_hours:kitchen"
                # fixChangeKey:"kitchen_hours => opening_hours:kitchen"
                err.append({'class': 9002001, 'subclass': 1088306802, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours:kitchen', mapcss.tag(tags, 'kitchen_hours')]]),
                    '-': ([
                    'kitchen_hours'])
                }})

        # *[shop=money_transfer]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'money_transfer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=money_transfer"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 1664997936, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'shop')]]),
                    '-': ([
                    'shop'])
                }})

        # *[contact:google_plus]
        if ('contact:google_plus' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'contact:google_plus')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"contact:google_plus"
                err.append({'class': 9002001, 'subclass': 1869461154, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'contact:google_plus'])
                }})

        # *[amenity=garages]
        # *[amenity=garage]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'garages')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'garage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("building=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + parking=garage_boxes"
                # suggestAlternative:"landuse=garages"
                err.append({'class': 9002001, 'subclass': 863228118, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=winery]
        # *[amenity=winery]
        if ('amenity' in keys) or ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'winery')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'winery')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=winery"
                # suggestAlternative:"shop=wine"
                err.append({'class': 9002001, 'subclass': 1773574987, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=youth_centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'youth_centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre + community_centre=youth_centre"
                # fixAdd:"amenity=community_centre"
                # fixAdd:"community_centre=youth_centre"
                err.append({'class': 9002001, 'subclass': 1284929085, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','community_centre'],
                    ['community_centre','youth_centre']])
                }})

        # *[building:type][building=yes]
        # *[building:type][!building]
        if ('building' in keys and 'building:type' in keys) or ('building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # fixChangeKey:"building:type => building"
                err.append({'class': 9002001, 'subclass': 1927794430, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building', mapcss.tag(tags, 'building:type')]]),
                    '-': ([
                    'building:type'])
                }})

        # *[building:type][building][building!=yes]
        if ('building' in keys and 'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (mapcss._tag_capture(capture_tags, 2, tags, 'building') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                err.append({'class': 9002001, 'subclass': 1133239698, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[escalator]
        # Rule Blacklisted (id: 967271828)

        # *[fenced]
        # Rule Blacklisted (id: 1141285220)

        # *[historic_name][!old_name]
        # Rule Blacklisted (id: 1034538127)

        # *[historic_name][old_name]
        # Rule Blacklisted (id: 30762614)

        # *[landuse=field]
        # Rule Blacklisted (id: 426261497)

        # *[leisure=beach]
        if ('leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'beach')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=beach_resort"
                # suggestAlternative:"natural=beach"
                err.append({'class': 9002001, 'subclass': 1767286055, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[leisure=club]
        # Rule Blacklisted (id: 1282397509)

        # *[leisure=video_arcade]
        # Rule Blacklisted (id: 1463909830)

        # *[man_made=jetty]
        # Rule Blacklisted (id: 192707176)

        # *[man_made=village_pump]
        # Rule Blacklisted (id: 423232686)

        # *[man_made=water_tank]
        # Rule Blacklisted (id: 563629665)

        # *[natural=moor]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'moor')))
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
                err.append({'class': 9002001, 'subclass': 374637717, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[noexit=no][!fixme]
        # Rule Blacklisted (id: 647435126)

        # *[noexit=no][fixme]
        # Rule Blacklisted (id: 881828009)

        # *[shop=dive]
        # Rule Blacklisted (id: 1582968978)

        # *[shop=furnace]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'furnace')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=plumber"
                # suggestAlternative:"shop=fireplace"
                err.append({'class': 9002001, 'subclass': 1155821104, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[sport=paragliding]
        # Rule Blacklisted (id: 1531788430)

        # *[tourism=bed_and_breakfast]
        # Rule Blacklisted (id: 954237438)

        # *[diaper=yes]
        # *[diaper=no]
        # Rule Blacklisted (id: 1957125311)

        # *[diaper][diaper=~/^[1-9][0-9]*$/]
        if ('diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0f294fdf), mapcss._tag_capture(capture_tags, 1, tags, 'diaper'))))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=yes + changing_table:count=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixAdd:"changing_table=yes"
                # fixChangeKey:"diaper => changing_table:count"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 2105051472, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table','yes'],
                    ['changing_table:count', mapcss.tag(tags, 'diaper')]]),
                    '-': ([
                    'diaper'])
                }})

        # *[diaper=room]
        if ('diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper') == mapcss._value_capture(capture_tags, 0, 'room')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper_checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table=dedicated_room"
                # suggestAlternative:"changing_table=room"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 883202329, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[diaper]!.diaper_checked
        # Rule Blacklisted (id: 693675339)

        # *[diaper:male=yes]
        if ('diaper:male' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:male') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=male_toilet"
                # fixAdd:"changing_table:location=male_toilet"
                # fixRemove:"diaper:male"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 799035479, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','male_toilet']]),
                    '-': ([
                    'diaper:male'])
                }})

        # *[diaper:female=yes]
        if ('diaper:female' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:female') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=female_toilet"
                # fixAdd:"changing_table:location=female_toilet"
                # fixRemove:"diaper:female"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1450901137, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','female_toilet']]),
                    '-': ([
                    'diaper:female'])
                }})

        # *[diaper:unisex=yes]
        if ('diaper:unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:unisex') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=unisex_toilet"
                # fixAdd:"changing_table:location=unisex_toilet"
                # fixRemove:"diaper:unisex"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1460378712, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','unisex_toilet']]),
                    '-': ([
                    'diaper:unisex'])
                }})

        # *[diaper:wheelchair=yes]
        # *[diaper:wheelchair=no]
        if ('diaper:wheelchair' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:wheelchair=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:wheelchair => changing_table:wheelchair"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1951967281, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:wheelchair', mapcss.tag(tags, 'diaper:wheelchair')]]),
                    '-': ([
                    'diaper:wheelchair'])
                }})

        # *[diaper:fee=yes]
        # *[diaper:fee=no]
        if ('diaper:fee' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:fee') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:fee') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:fee=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:fee => changing_table:fee"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 2008573526, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:fee', mapcss.tag(tags, 'diaper:fee')]]),
                    '-': ([
                    'diaper:fee'])
                }})

        # *[/^diaper:/]!.diaper___checked
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_diaper___checked) and (mapcss._tag_capture(capture_tags, 0, tags, self.re_6029fe03)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","diaper:*")
                # suggestAlternative:"changing_table:*"
                err.append({'class': 9002001, 'subclass': 26578864, 'text': mapcss.tr('{0} is deprecated', 'diaper:*')})

        # *[changing_table][changing_table!~/^(yes|no|limited)$/]
        if ('changing_table' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'changing_table')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_787405b1, '^(yes|no|limited)$'), mapcss._tag_capture(capture_tags, 1, tags, 'changing_table'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"changing_table=limited"
                # suggestAlternative:"changing_table=no"
                # suggestAlternative:"changing_table=yes"
                err.append({'class': 9002019, 'subclass': 1965225408, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[roof:shape=half_hipped]
        if ('roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:shape') == mapcss._value_capture(capture_tags, 0, 'half_hipped')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"roof:shape=half-hipped"
                # fixAdd:"roof:shape=half-hipped"
                err.append({'class': 9002001, 'subclass': 1548347123, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['roof:shape','half-hipped']])
                }})

        # *[bridge_name]
        if ('bridge_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge_name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"bridge:name"
                # fixChangeKey:"bridge_name => bridge:name"
                err.append({'class': 9002001, 'subclass': 80069399, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bridge:name', mapcss.tag(tags, 'bridge_name')]]),
                    '-': ([
                    'bridge_name'])
                }})

        # *[access=public]
        # Rule Blacklisted (id: 1115157097)

        # *[crossing=island]
        if ('crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'crossing') == mapcss._value_capture(capture_tags, 0, 'island')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"crossing:island=yes"
                # fixRemove:"crossing"
                # fixAdd:"crossing:island=yes"
                err.append({'class': 9002001, 'subclass': 1512561318, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['crossing:island','yes']]),
                    '-': ([
                    'crossing'])
                }})

        # *[recycling:metal]
        if ('recycling:metal' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'recycling:metal')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"recycling:scrap_metal"
                # fixChangeKey:"recycling:metal => recycling:scrap_metal"
                err.append({'class': 9002001, 'subclass': 474491272, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:scrap_metal', mapcss.tag(tags, 'recycling:metal')]]),
                    '-': ([
                    'recycling:metal'])
                }})

        # *[shop=dog_grooming]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'dog_grooming')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet_grooming"
                # fixAdd:"shop=pet_grooming"
                err.append({'class': 9002001, 'subclass': 1073412885, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','pet_grooming']])
                }})

        # *[tower:type=anchor]
        # *[tower:type=suspension]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'anchor')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'suspension')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"tower:type => line_attachment"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 180380605, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_attachment', mapcss.tag(tags, 'tower:type')]]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=branch][branch:type=split]
        # *[tower:type=branch][branch:type=loop]
        if ('branch:type' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'split')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'loop')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=split"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=split"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 362350862, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','split']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=branch][!branch:type]
        # *[tower:type=branch][branch:type=tap]
        if ('branch:type' in keys and 'tower:type' in keys) or ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'branch:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'tap')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=branch"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=branch"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 476423517, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','branch']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=branch][branch:type=cross]
        if ('branch:type' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'cross')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=cross"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=cross"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 2103059531, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','cross']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=termination]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'termination')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=termination"
                # fixAdd:"line_management=termination"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 232235847, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','termination']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=transition]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'transition')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1124904944, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location:transition','yes']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=transposing]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'transposing')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=transpose"
                # fixAdd:"line_management=transpose"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1795169098, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','transpose']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=crossing]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"height=* + design=*"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1301565974, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[tower:type][power][power=~/^(tower|pole|insulator|portal|terminal)$/]!.power_tower_type_warning
        if ('power' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_power_tower_type_warning) and (mapcss._tag_capture(capture_tags, 0, tags, 'tower:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_24dfeb95), mapcss._tag_capture(capture_tags, 2, tags, 'power'))))
                except mapcss.RuleAbort: pass
            if match:
                # set generic_power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"design"
                # suggestAlternative:"line_attachment"
                # suggestAlternative:"line_management"
                # suggestAlternative:"structure"
                set_generic_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 2020421267, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[pole:type=anchor]
        # node[pole:type=suspension]
        if ('pole:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'anchor')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'suspension')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_pole_type_warning
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"pole:type => line_attachment"
                set_power_pole_type_warning = True
                err.append({'class': 9002001, 'subclass': 1925507031, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_attachment', mapcss.tag(tags, 'pole:type')]]),
                    '-': ([
                    'pole:type'])
                }})

        # node[pole:type=branch][branch:type=split]
        # node[pole:type=branch][branch:type=loop]
        if ('branch:type' in keys and 'pole:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'split')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'loop')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_pole_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=split"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=split"
                # fixRemove:"pole:type"
                set_power_pole_type_warning = True
                err.append({'class': 9002001, 'subclass': 1645001021, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','split']]),
                    '-': ([
                    'branch:type',
                    'pole:type'])
                }})

        # node[pole:type=branch][!branch:type]
        # node[pole:type=branch][branch:type=tap]
        if ('branch:type' in keys and 'pole:type' in keys) or ('pole:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'branch:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'tap')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_pole_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=branch"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=branch"
                # fixRemove:"pole:type"
                set_power_pole_type_warning = True
                err.append({'class': 9002001, 'subclass': 686268660, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','branch']]),
                    '-': ([
                    'branch:type',
                    'pole:type'])
                }})

        # node[pole:type=branch][branch:type=cross]
        if ('branch:type' in keys and 'pole:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'cross')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_pole_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=cross"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=cross"
                # fixRemove:"pole:type"
                set_power_pole_type_warning = True
                err.append({'class': 9002001, 'subclass': 160459065, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','cross']]),
                    '-': ([
                    'branch:type',
                    'pole:type'])
                }})

        # node[pole:type=termination]
        if ('pole:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'termination')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_pole_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=termination"
                # fixAdd:"line_management=termination"
                # fixRemove:"pole:type"
                set_power_pole_type_warning = True
                err.append({'class': 9002001, 'subclass': 1675908395, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','termination']]),
                    '-': ([
                    'pole:type'])
                }})

        # node[pole:type=transition]
        if ('pole:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pole:type') == mapcss._value_capture(capture_tags, 0, 'transition')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_pole_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"pole:type"
                set_power_pole_type_warning = True
                err.append({'class': 9002001, 'subclass': 1266956723, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location:transition','yes']]),
                    '-': ([
                    'pole:type'])
                }})

        # *[pole:type][power][power=~/^(tower|pole|insulator|portal|terminal)$/]!.power_pole_type_warning!.generic_power_tower_type_warning
        if ('pole:type' in keys and 'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_power_pole_type_warning) and (not set_generic_power_tower_type_warning) and (mapcss._tag_capture(capture_tags, 0, tags, 'pole:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_24dfeb95), mapcss._tag_capture(capture_tags, 2, tags, 'power'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"line_attachment"
                # suggestAlternative:"line_management"
                err.append({'class': 9002001, 'subclass': 1513543887, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[man_made=pipeline_marker]
        # node[pipeline=marker]
        # node[power=marker]
        # node[cable=marker]
        if ('cable' in keys) or ('man_made' in keys) or ('pipeline' in keys) or ('power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pipeline_marker')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pipeline') == mapcss._value_capture(capture_tags, 0, 'marker')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'marker')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cable') == mapcss._value_capture(capture_tags, 0, 'marker')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"marker=* + utility=*"
                err.append({'class': 9002001, 'subclass': 296597752, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[sloped_curb=yes][!kerb]
        # *[sloped_curb=both][!kerb]
        if ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'yes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'both')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=lowered"
                # fixAdd:"kerb=lowered"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 1906002413, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['kerb','lowered']]),
                    '-': ([
                    'sloped_curb'])
                }})

        # *[sloped_curb=no][!kerb]
        if ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'no')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=yes"
                # fixAdd:"kerb=yes"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 893727015, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['kerb','yes']]),
                    '-': ([
                    'sloped_curb'])
                }})

        # *[sloped_curb][sloped_curb!~/^(yes|both|no)$/][!kerb]
        # *[sloped_curb][kerb]
        if ('kerb' in keys and 'sloped_curb' in keys) or ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_01eb1711, '^(yes|both|no)$'), mapcss._tag_capture(capture_tags, 1, tags, 'sloped_curb'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb')) and (mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"kerb=*"
                err.append({'class': 9002001, 'subclass': 1682376745, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[unnamed=yes]
        if ('unnamed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'unnamed') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"noname=yes"
                # fixChangeKey:"unnamed => noname"
                err.append({'class': 9002001, 'subclass': 1901447020, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['noname', mapcss.tag(tags, 'unnamed')]]),
                    '-': ([
                    'unnamed'])
                }})

        # node[segregated][segregated!=yes][segregated!=no]
        if ('segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'segregated')) and (mapcss._tag_capture(capture_tags, 1, tags, 'segregated') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'segregated') != mapcss._value_const_capture(capture_tags, 2, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9002020, 'subclass': 1015641959, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[building:height]
        if ('building:height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:height')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"height"
                # fixChangeKey:"building:height => height"
                err.append({'class': 9002001, 'subclass': 1328174745, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['height', mapcss.tag(tags, 'building:height')]]),
                    '-': ([
                    'building:height'])
                }})

        # *[building:min_height]
        if ('building:min_height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:min_height')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"min_height"
                # fixChangeKey:"building:min_height => min_height"
                err.append({'class': 9002001, 'subclass': 1042683921, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['min_height', mapcss.tag(tags, 'building:min_height')]]),
                    '-': ([
                    'building:min_height'])
                }})

        # *[car][amenity=charging_station]
        # Rule Blacklisted (id: 1165117414)

        # *[navigationaid=approach_light]
        # *[navigationaid="ALS (Approach lighting system)"]
        if ('navigationaid' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'navigationaid') == mapcss._value_capture(capture_tags, 0, 'approach_light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'navigationaid') == mapcss._value_capture(capture_tags, 0, 'ALS (Approach lighting system)')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"navigationaid=als"
                # fixAdd:"navigationaid=als"
                err.append({'class': 9002001, 'subclass': 1577817081, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['navigationaid','als']])
                }})

        # node[exit_to]
        if ('exit_to' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'exit_to')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"destination"
                err.append({'class': 9002001, 'subclass': 2117439762, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[water=riverbank][!natural]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                err.append({'class': 9002001, 'subclass': 186872153, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','water'],
                    ['water','river']])
                }})

        # *[water=riverbank][natural]
        if ('natural' in keys and 'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 630806094, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[waterway=riverbank][!natural][!water]
        # *[waterway=riverbank][natural=water][!water]
        # *[waterway=riverbank][!natural][water=river]
        # *[waterway=riverbank][natural=water][water=river]
        if ('natural' in keys and 'water' in keys and 'waterway' in keys) or ('natural' in keys and 'waterway' in keys) or ('water' in keys and 'waterway' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'river')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'river')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 1604946271, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','water'],
                    ['water','river']]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=riverbank][natural][natural!=water]
        # *[waterway=riverbank][water][water!=river]
        if ('natural' in keys and 'waterway' in keys) or ('water' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (mapcss._tag_capture(capture_tags, 2, tags, 'natural') != mapcss._value_const_capture(capture_tags, 2, 'water', 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'river', 'river')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 301661430, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[amenity=bench][capacity][!seats]
        if ('amenity' in keys and 'capacity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'bench')) and (mapcss._tag_capture(capture_tags, 1, tags, 'capacity')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'seats')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"seats"
                # fixChangeKey:"capacity => seats"
                err.append({'class': 9002001, 'subclass': 417580324, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['seats', mapcss.tag(tags, 'capacity')]]),
                    '-': ([
                    'capacity'])
                }})

        # node[amenity=bench][capacity][seats]
        if ('amenity' in keys and 'capacity' in keys and 'seats' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'bench')) and (mapcss._tag_capture(capture_tags, 1, tags, 'capacity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'seats')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"seats"
                err.append({'class': 9002001, 'subclass': 2124584560, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=lamps]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'lamps')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=lighting"
                # fixAdd:"shop=lighting"
                err.append({'class': 9002001, 'subclass': 746886011, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','lighting']])
                }})

        # *[access=customer]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'customer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"access=customers"
                # fixAdd:"access=customers"
                err.append({'class': 9002001, 'subclass': 1040065637, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['access','customers']])
                }})

        # *[addr:inclusion=estimated]
        if ('addr:inclusion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:inclusion') == mapcss._value_capture(capture_tags, 0, 'estimated')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"addr:inclusion=estimate"
                # fixAdd:"addr:inclusion=estimate"
                err.append({'class': 9002001, 'subclass': 1002643753, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['addr:inclusion','estimate']])
                }})

        # *[building=apartment]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'apartment')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"building=apartments"
                # fixAdd:"building=apartments"
                err.append({'class': 9002001, 'subclass': 1384168519, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','apartments']])
                }})

        # node[lamp_mount="bent mast"]
        if ('lamp_mount' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lamp_mount') == mapcss._value_capture(capture_tags, 0, 'bent mast')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"lamp_mount=bent_mast"
                # fixAdd:"lamp_mount=bent_mast"
                err.append({'class': 9002001, 'subclass': 653926228, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['lamp_mount','bent_mast']])
                }})

        # node[lamp_mount="straight mast"]
        if ('lamp_mount' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lamp_mount') == mapcss._value_capture(capture_tags, 0, 'straight mast')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"lamp_mount=straight_mast"
                # fixAdd:"lamp_mount=straight_mast"
                err.append({'class': 9002001, 'subclass': 2015439082, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['lamp_mount','straight_mast']])
                }})

        # node[lamp_type=electrical]
        if ('lamp_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lamp_type') == mapcss._value_capture(capture_tags, 0, 'electrical')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"lamp_type=electric"
                # fixAdd:"lamp_type=electric"
                err.append({'class': 9002001, 'subclass': 237309553, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['lamp_type','electric']])
                }})

        # *[generator:type=solar_photovoltaic_panels]
        if ('generator:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:type') == mapcss._value_capture(capture_tags, 0, 'solar_photovoltaic_panels')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:type=solar_photovoltaic_panel"
                # fixAdd:"generator:type=solar_photovoltaic_panel"
                err.append({'class': 9002001, 'subclass': 1146719875, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:type','solar_photovoltaic_panel']])
                }})

        # *[building=part]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'part')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"building:part=yes"
                err.append({'class': 9002001, 'subclass': 455695847, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[natural=sink_hole]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'sink_hole')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=sinkhole"
                # fixAdd:"natural=sinkhole"
                err.append({'class': 9002001, 'subclass': 1283355945, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','sinkhole']])
                }})

        # *[climbing:grade:UIAA:min]
        if ('climbing:grade:UIAA:min' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:min')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:min"
                # fixChangeKey:"climbing:grade:UIAA:min => climbing:grade:uiaa:min"
                err.append({'class': 9002001, 'subclass': 1408052420, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:min', mapcss.tag(tags, 'climbing:grade:UIAA:min')]]),
                    '-': ([
                    'climbing:grade:UIAA:min'])
                }})

        # *[climbing:grade:UIAA:max]
        if ('climbing:grade:UIAA:max' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:max')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:max"
                # fixChangeKey:"climbing:grade:UIAA:max => climbing:grade:uiaa:max"
                err.append({'class': 9002001, 'subclass': 1866245426, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:max', mapcss.tag(tags, 'climbing:grade:UIAA:max')]]),
                    '-': ([
                    'climbing:grade:UIAA:max'])
                }})

        # *[climbing:grade:UIAA:mean]
        if ('climbing:grade:UIAA:mean' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:mean')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:mean"
                # fixChangeKey:"climbing:grade:UIAA:mean => climbing:grade:uiaa:mean"
                err.append({'class': 9002001, 'subclass': 1022648087, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:mean', mapcss.tag(tags, 'climbing:grade:UIAA:mean')]]),
                    '-': ([
                    'climbing:grade:UIAA:mean'])
                }})

        # *[climbing:grade:UIAA]
        if ('climbing:grade:UIAA' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa"
                # fixChangeKey:"climbing:grade:UIAA => climbing:grade:uiaa"
                err.append({'class': 9002001, 'subclass': 1007893519, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa', mapcss.tag(tags, 'climbing:grade:UIAA')]]),
                    '-': ([
                    'climbing:grade:UIAA'])
                }})

        # *[cuisine][cuisine=~/^(?i)(bbq)$/]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2f881233), mapcss._tag_capture(capture_tags, 1, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # set bbq_autofix
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"cuisine=barbecue"
                # fixAdd:"cuisine=barbecue"
                set_bbq_autofix = True
                err.append({'class': 9002001, 'subclass': 1943338875, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['cuisine','barbecue']])
                }})

        # *[cuisine=~/(?i)(;bbq|bbq;)/][cuisine!~/(?i)(_bbq)/]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_340a2b31), mapcss._tag_capture(capture_tags, 0, tags, 'cuisine'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7d409ed5, '(?i)(_bbq)'), mapcss._tag_capture(capture_tags, 1, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","cuisine=bbq")
                # suggestAlternative:"cuisine=barbecue"
                err.append({'class': 9002001, 'subclass': 1958782130, 'text': mapcss.tr('{0} is deprecated', 'cuisine=bbq')})

        # *[Fixme]
        if ('Fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'Fixme')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"fixme"
                # fixChangeKey:"Fixme => fixme"
                err.append({'class': 9002001, 'subclass': 592643943, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['fixme', mapcss.tag(tags, 'Fixme')]]),
                    '-': ([
                    'Fixme'])
                }})

        # *[amenity=embassy]
        # Rule Blacklisted (id: 1751915206)

        # *[service:bicycle:chaintool]
        if ('service:bicycle:chaintool' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service:bicycle:chaintool')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"service:bicycle:chain_tool"
                # fixChangeKey:"service:bicycle:chaintool => service:bicycle:chain_tool"
                err.append({'class': 9002001, 'subclass': 1464143873, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['service:bicycle:chain_tool', mapcss.tag(tags, 'service:bicycle:chaintool')]]),
                    '-': ([
                    'service:bicycle:chaintool'])
                }})

        # *[building:roof:shape]
        if ('building:roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:roof:shape')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"roof:shape"
                # fixChangeKey:"building:roof:shape => roof:shape"
                err.append({'class': 9002001, 'subclass': 2106920042, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['roof:shape', mapcss.tag(tags, 'building:roof:shape')]]),
                    '-': ([
                    'building:roof:shape'])
                }})

        # *[man_made=pumping_rig][!pump_mechanism][!mechanical_driver][!mechanical_coupling]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pumping_rig')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'pump_mechanism')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mechanical_coupling')))
                except mapcss.RuleAbort: pass
            if match:
                # set pumping_ring_no_mech
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                # fixAdd:"mechanical_coupling=nodding_donkey"
                # fixAdd:"mechanical_driver=combustion_engine"
                # fixAdd:"pump_mechanism=piston"
                set_pumping_ring_no_mech = True
                err.append({'class': 9002001, 'subclass': 6568074, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mechanical_coupling','nodding_donkey'],
                    ['mechanical_driver','combustion_engine'],
                    ['pump_mechanism','piston']])
                }})

        # *[man_made=pumping_rig]!.pumping_ring_no_mech
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_pumping_ring_no_mech) and (mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pumping_rig')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1031026578, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[pump:type=beam_pump][!pump_mechanism][!mechanical_driver][!mechanical_coupling]
        if ('pump:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pump:type') == mapcss._value_capture(capture_tags, 0, 'beam_pump')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'pump_mechanism')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mechanical_coupling')))
                except mapcss.RuleAbort: pass
            if match:
                # set beam_pump_no_mech
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"pump_mechanism"
                # fixAdd:"mechanical_coupling=nodding_donkey"
                # fixAdd:"mechanical_driver=combustion_engine"
                # fixRemove:"pump:type"
                # fixAdd:"pump_mechanism=piston"
                set_beam_pump_no_mech = True
                err.append({'class': 9002001, 'subclass': 1519103279, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mechanical_coupling','nodding_donkey'],
                    ['mechanical_driver','combustion_engine'],
                    ['pump_mechanism','piston']]),
                    '-': ([
                    'pump:type'])
                }})

        # *[pump:type]!.beam_pump_no_mech
        if ('pump:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_beam_pump_no_mech) and (mapcss._tag_capture(capture_tags, 0, tags, 'pump:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"pump_mechanism"
                err.append({'class': 9002001, 'subclass': 2015679777, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[substance=heat]
        if ('substance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'substance') == mapcss._value_capture(capture_tags, 0, 'heat')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"substance=hot_water"
                # suggestAlternative:"substance=steam"
                err.append({'class': 9002001, 'subclass': 1528467304, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[landuse=school]
        if ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'school')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=college"
                # suggestAlternative:"amenity=school"
                # suggestAlternative:"amenity=university"
                # suggestAlternative:"landuse=education"
                err.append({'class': 9002001, 'subclass': 817812278, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[surface=decoturf]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface') == mapcss._value_capture(capture_tags, 0, 'decoturf')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"surface=acrylic"
                # fixAdd:"surface=acrylic"
                err.append({'class': 9002001, 'subclass': 1995300591, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['surface','acrylic']])
                }})

        # *[role]
        # Rule Blacklisted (id: 2041296832)

        # *[school=entrance]
        if ('school' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'school') == mapcss._value_capture(capture_tags, 0, 'entrance')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"entrance=main"
                # suggestAlternative:"entrance=yes"
                err.append({'class': 9002001, 'subclass': 1398581809, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[voltage-high]
        # *[voltage-low]
        if ('voltage-high' in keys) or ('voltage-low' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage-high')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage-low')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"voltage:primary"
                # suggestAlternative:"voltage:secondary"
                err.append({'class': 9002001, 'subclass': 1379077827, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[toilet][!toilets]
        if ('toilet' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toilet')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'toilets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"toilets"
                # fixChangeKey:"toilet => toilets"
                err.append({'class': 9002001, 'subclass': 466700565, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['toilets', mapcss.tag(tags, 'toilet')]]),
                    '-': ([
                    'toilet'])
                }})

        # *[toilet][toilets]
        if ('toilet' in keys and 'toilets' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toilet')) and (mapcss._tag_capture(capture_tags, 1, tags, 'toilets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"toilets"
                err.append({'class': 9002001, 'subclass': 1092230744, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[type="turnlanes:turns"]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'turnlanes:turns')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"type=connectivity"
                err.append({'class': 9002001, 'subclass': 1789083769, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[image][image=~/^https:\/\/westnordost.de\/p\//]
        if ('image' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'image')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0fbae48f), mapcss._tag_capture(capture_tags, 1, tags, 'image'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} with a temporary URL which may be outdated very soon","{0.key}")
                # fixRemove:"{0.key}"
                # assertNoMatch:"node image=https://commons.wikimedia.org/wiki/File:2015-05-13_Basteibr%C3%BCcke-.jpg"
                # assertNoMatch:"node image=https://web.archive.org/web/20220623215400/https://westnordost.de/p/97331.jpg"
                # assertMatch:"node image=https://westnordost.de/p/17484.jpg"
                err.append({'class': 9002023, 'subclass': 2042174729, 'text': mapcss.tr('{0} with a temporary URL which may be outdated very soon', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[historic=archaeological_site][site_type]
        if ('historic' in keys and 'site_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'historic') == mapcss._value_capture(capture_tags, 0, 'archaeological_site')) and (mapcss._tag_capture(capture_tags, 1, tags, 'site_type')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be replaced with {1}","{1.key}","archaeological_site")
                # fixChangeKey:"site_type => archaeological_site"
                # assertNoMatch:"node historic=archaeological_site site_type2=fortification"
                # assertMatch:"node historic=archaeological_site site_type=fortification"
                err.append({'class': 9002008, 'subclass': 595008939, 'text': mapcss.tr('{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), 'archaeological_site'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['archaeological_site', mapcss.tag(tags, 'site_type')]]),
                    '-': ([
                    'site_type'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_bbq_autofix = set_beam_pump_no_mech = set_diaper___checked = set_diaper_checked = set_generic_power_tower_type_warning = set_levels_building = set_power_pole_type_warning = set_power_tower_type_warning = set_pumping_ring_no_mech = False

        # *[barrier=wire_fence]
        if ('barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wire_fence')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=chain_link"
                # assertNoMatch:"way barrier=fence"
                # assertMatch:"way barrier=wire_fence"
                err.append({'class': 9002001, 'subclass': 1107799632, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['barrier','fence'],
                    ['fence_type','chain_link']])
                }})

        # *[barrier=wood_fence]
        if ('barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wood_fence')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=wood"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=wood"
                err.append({'class': 9002001, 'subclass': 1412230714, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['barrier','fence'],
                    ['fence_type','wood']])
                }})

        # way[highway=ford]
        # Rule Blacklisted (id: 591931361)

        # way[class]
        # Rule Blacklisted (id: 905310794)

        # *[highway=stile]
        # Rule Blacklisted (id: 1435678043)

        # *[highway=incline]
        # Rule Blacklisted (id: 765169083)

        # *[highway=incline_steep]
        # Rule Blacklisted (id: 1966772390)

        # *[highway=unsurfaced]
        # Rule Blacklisted (id: 20631498)

        # *[landuse=wood]
        # Rule Blacklisted (id: 469903103)

        # *[natural=marsh]
        # Rule Blacklisted (id: 1459865523)

        # *[highway=byway]
        # Rule Blacklisted (id: 1844620979)

        # *[power_source]
        # Rule Blacklisted (id: 34751027)

        # *[power_rating]
        # Rule Blacklisted (id: 904750343)

        # *[shop=antique]
        # Rule Blacklisted (id: 596668979)

        # *[shop=bags]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'bags')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=bag"
                # fixAdd:"shop=bag"
                err.append({'class': 9002001, 'subclass': 1709003584, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','bag']])
                }})

        # *[shop=fashion]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'fashion')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=clothes"
                # fixAdd:"shop=clothes"
                err.append({'class': 9002001, 'subclass': 985619804, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','clothes']])
                }})

        # *[shop=organic]
        # Rule Blacklisted (id: 1959365145)

        # *[shop=pets]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'pets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet"
                # fixAdd:"shop=pet"
                err.append({'class': 9002001, 'subclass': 290270098, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','pet']])
                }})

        # *[shop=pharmacy]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'pharmacy')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=pharmacy"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 350722657, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'shop')]]),
                    '-': ([
                    'shop'])
                }})

        # *[bicycle_parking=sheffield]
        if ('bicycle_parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle_parking') == mapcss._value_capture(capture_tags, 0, 'sheffield')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bicycle_parking=stands"
                # fixAdd:"bicycle_parking=stands"
                err.append({'class': 9002001, 'subclass': 718874663, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bicycle_parking','stands']])
                }})

        # *[amenity=emergency_phone]
        # Rule Blacklisted (id: 1108230656)

        # *[sport=gaelic_football]
        # Rule Blacklisted (id: 1768681881)

        # *[power=station]
        # Rule Blacklisted (id: 52025933)

        # *[power=sub_station]
        # Rule Blacklisted (id: 1423074682)

        # *[location=rooftop]
        if ('location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'location') == mapcss._value_capture(capture_tags, 0, 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location=roof"
                # fixAdd:"location=roof"
                err.append({'class': 9002001, 'subclass': 1028577225, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location','roof']])
                }})

        # *[generator:location]
        if ('generator:location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:location')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"location"
                # fixChangeKey:"generator:location => location"
                err.append({'class': 9002001, 'subclass': 900615917, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location', mapcss.tag(tags, 'generator:location')]]),
                    '-': ([
                    'generator:location'])
                }})

        # *[generator:method=dam]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'dam')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-storage"
                # fixAdd:"generator:method=water-storage"
                err.append({'class': 9002001, 'subclass': 248819368, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-storage']])
                }})

        # *[generator:method=pumped-storage]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'pumped-storage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 93454158, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-pumped-storage']])
                }})

        # *[generator:method=pumping]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'pumping')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 2115673716, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-pumped-storage']])
                }})

        # *[fence_type=chain]
        if ('fence_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fence_type') == mapcss._value_capture(capture_tags, 0, 'chain')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=chain"
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 19409288, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building=entrance]
        # Rule Blacklisted (id: 306662985)

        # *[board_type=board]
        if ('board_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'board_type') == mapcss._value_capture(capture_tags, 0, 'board')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"board_type"
                err.append({'class': 9002001, 'subclass': 1150949316, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'board_type'])
                }})

        # *[man_made=measurement_station]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'measurement_station')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=monitoring_station"
                # fixAdd:"man_made=monitoring_station"
                err.append({'class': 9002001, 'subclass': 700465123, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['man_made','monitoring_station']])
                }})

        # *[measurement=water_level]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'water_level')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:water_level=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:water_level=yes"
                err.append({'class': 9002001, 'subclass': 634647702, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:water_level','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[measurement=weather]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'weather')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:weather=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:weather=yes"
                err.append({'class': 9002001, 'subclass': 336627227, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:weather','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[measurement=seismic]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'seismic')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:seismic_activity=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:seismic_activity=yes"
                err.append({'class': 9002001, 'subclass': 1402131289, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:seismic_activity','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[monitoring:river_level]
        if ('monitoring:river_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'monitoring:river_level')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"monitoring:water_level"
                # fixChangeKey:"monitoring:river_level => monitoring:water_level"
                err.append({'class': 9002001, 'subclass': 264907924, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:water_level', mapcss.tag(tags, 'monitoring:river_level')]]),
                    '-': ([
                    'monitoring:river_level'])
                }})

        # *[stay]
        if ('stay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'stay')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"maxstay"
                # fixChangeKey:"stay => maxstay"
                err.append({'class': 9002001, 'subclass': 787370129, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxstay', mapcss.tag(tags, 'stay')]]),
                    '-': ([
                    'stay'])
                }})

        # *[emergency=aed]
        # Rule Blacklisted (id: 707111885)

        # *[day_on][!restriction]
        # *[day_off][!restriction]
        # *[date_on][!restriction]
        # *[date_off][!restriction]
        # *[hour_on][!restriction]
        # *[hour_off][!restriction]
        # Rule Blacklisted (id: 294264920)

        # *[access=designated]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'designated')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' is meaningless, use more specific tags, e.g. ''{1}''","access=designated","bicycle=designated")
                # assertMatch:"way access=designated"
                err.append({'class': 9002002, 'subclass': 2057594338, 'text': mapcss.tr('\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', 'access=designated', 'bicycle=designated')})

        # *[access=official]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'official')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' does not specify the official mode of transportation, use ''{1}'' for example","access=official","bicycle=official")
                # assertMatch:"way access=official"
                err.append({'class': 9002003, 'subclass': 1909133836, 'text': mapcss.tr('\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', 'access=official', 'bicycle=official')})

        # *[fixme=yes]
        # *[FIXME=yes]
        if ('FIXME' in keys) or ('fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fixme') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'FIXME') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Instead of ''{1}'' please give more information about what exactly should be fixed.","{0.key}","{0.value}")
                # assertMatch:"way fixme=yes"
                err.append({'class': 9002004, 'subclass': 136657482, 'text': mapcss.tr('{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # *[name][name=~/^(?i)fixme$/]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.","{0.key}","{0.tag}")
                # fixRemove:"name"
                err.append({'class': 9002005, 'subclass': 642340557, 'text': mapcss.tr('Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'name'])
                }})

        # *[note][note=~/^(?i)fixme$/]
        if ('note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'note')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, 'note'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.","{0.tag}")
                err.append({'class': 9002006, 'subclass': 1243120287, 'text': mapcss.tr('{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[type=broad_leaved]
        # *[type=broad_leafed]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'broad_leaved')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'broad_leafed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=broadleaved"
                # fixAdd:"leaf_type=broadleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 293968062, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','broadleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=coniferous]
        # *[type=coniferous]
        # *[type=conifer]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'coniferous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'coniferous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'conifer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=needleleaved"
                # fixAdd:"leaf_type=needleleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 50517650, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','needleleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=mixed]
        if ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'mixed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=mixed"
                # fixAdd:"leaf_type=mixed"
                # fixRemove:"wood"
                err.append({'class': 9002001, 'subclass': 235914603, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','mixed']]),
                    '-': ([
                    'wood'])
                }})

        # *[wood=evergreen]
        # *[type=evergreen]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'evergreen')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'evergreen')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=evergreen"
                # fixAdd:"leaf_cycle=evergreen"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 747964532, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_cycle','evergreen']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=deciduous]
        # *[type=deciduous]
        # *[type=deciduos]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'deciduous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'deciduous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'deciduos')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=deciduous"
                # fixAdd:"leaf_cycle=deciduous"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1458103800, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_cycle','deciduous']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # way[type=palm]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'palm')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type"
                # suggestAlternative:"species"
                # suggestAlternative:"trees"
                err.append({'class': 9002001, 'subclass': 1757132153, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[natural=land]
        # Rule Blacklisted (id: 94558529)

        # *[bridge=causeway]
        if ('bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge') == mapcss._value_capture(capture_tags, 0, 'causeway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=low_water_crossing"
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"ford=yes"
                err.append({'class': 9002001, 'subclass': 461671124, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[bridge=swing]
        # Rule Blacklisted (id: 1047428067)

        # *[bridge=suspension]
        # Rule Blacklisted (id: 1157046268)

        # *[bridge=pontoon]
        # Rule Blacklisted (id: 1195531951)

        # *[fee=interval]
        # *[lit=interval]
        # *[supervised=interval]
        if ('fee' in keys) or ('lit' in keys) or ('supervised' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fee') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lit') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'supervised') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please specify interval by using opening_hours syntax","{0.tag}")
                err.append({'class': 9002001, 'subclass': 417886592, 'text': mapcss.tr('{0} is deprecated. Please specify interval by using opening_hours syntax', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/josm\/ignore/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_5ee0acf2)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwError:tr("{0} is deprecated. Please delete this object and use a private layer instead","{0.key}")
                # fixDeleteObject:this
                err.append({'class': 9002001, 'subclass': 1402743016, 'text': mapcss.tr('{0} is deprecated. Please delete this object and use a private layer instead', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[sport=diving]
        # Rule Blacklisted (id: 590643159)

        # *[parking=park_and_ride]
        if ('parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking') == mapcss._value_capture(capture_tags, 0, 'park_and_ride')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + park_ride=yes"
                # fixAdd:"amenity=parking"
                # fixAdd:"park_ride=yes"
                # fixRemove:"parking"
                err.append({'class': 9002001, 'subclass': 1893516041, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','parking'],
                    ['park_ride','yes']]),
                    '-': ([
                    'parking'])
                }})

        # *[parking=yes]
        # *[playground=yes]
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
        # *[landuse=yes]
        # *[shop="*"]
        # *[shop=yes][amenity!=fuel]
        # *[craft=yes]
        # *[service=yes]
        # *[place=yes]
        if ('access' in keys) or ('aerialway' in keys) or ('amenity' in keys) or ('barrier' in keys) or ('craft' in keys) or ('landuse' in keys) or ('leisure' in keys) or ('manhole' in keys) or ('parking' in keys) or ('place' in keys) or ('playground' in keys) or ('police' in keys) or ('service' in keys) or ('shop' in keys) or ('traffic_calming' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'playground') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'plain')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'unknown')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'police') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_calming') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'restricted')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'yes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'public_transport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, '*')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'fuel', 'fuel')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'craft') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Please replace ''{1}'' by a specific value.","{0.key}","{0.value}")
                err.append({'class': 9002007, 'subclass': 1452069773, 'text': mapcss.tr('{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # *[place_name][!name]
        # Rule Blacklisted (id: 1089331760)

        # *[place][place_name=*name]
        # Rule Blacklisted (id: 1116761280)

        # way[sidewalk=yes]
        if ('sidewalk' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is unspecific","{0.tag}")
                # suggestAlternative:"sidewalk=both"
                # suggestAlternative:"sidewalk=left"
                # suggestAlternative:"sidewalk=right"
                # suggestAlternative:"sidewalk=separate"
                err.append({'class': 9002024, 'subclass': 36539821, 'text': mapcss.tr('{0} is unspecific', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[waterway=water_point]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'water_point')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=water_point"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 103347605, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'waterway')]]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=waste_disposal]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'waste_disposal')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_disposal"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 1963461348, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'waterway')]]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=mooring]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'mooring')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"mooring=yes"
                # fixAdd:"mooring=yes"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 81358738, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mooring','yes']]),
                    '-': ([
                    'waterway'])
                }})

        # *[building][levels]
        # *[building:part][levels]
        if ('building' in keys and 'levels' in keys) or ('building:part' in keys and 'levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')) and (mapcss._tag_capture(capture_tags, 1, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if match:
                # set levels_building
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.key}")
                # suggestAlternative:"building:levels"
                # fixChangeKey:"levels => building:levels"
                set_levels_building = True
                err.append({'class': 9002001, 'subclass': 869936714, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building:levels', mapcss.tag(tags, 'levels')]]),
                    '-': ([
                    'levels'])
                }})

        # *[levels]!.levels_building
        if ('levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_levels_building) and (mapcss._tag_capture(capture_tags, 0, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unusual key {0}, maybe {1} or {2} is meant","{0.key}","level","building:levels")
                err.append({'class': 9002021, 'subclass': 1172699526, 'text': mapcss.tr('Unusual key {0}, maybe {1} or {2} is meant', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'level', 'building:levels')})

        # *[protected_class]
        if ('protected_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'protected_class')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"protect_class"
                # fixChangeKey:"protected_class => protect_class"
                err.append({'class': 9002001, 'subclass': 716999373, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['protect_class', mapcss.tag(tags, 'protected_class')]]),
                    '-': ([
                    'protected_class'])
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
        # Rule Blacklisted (id: 1052866123)

        # *[sport=skiing]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'skiing')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # suggestAlternative:tr("{0} + {1} + {2}","piste:type=*","piste:difficulty=*","piste:grooming=*")
                err.append({'class': 9002001, 'subclass': 1578959559, 'text': mapcss.tr('Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[waterway=wadi]
        # Rule Blacklisted (id: 719234223)

        # way[oneway=1]
        if ('oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') == mapcss._value_capture(capture_tags, 0, 1)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"oneway=yes"
                # fixAdd:"oneway=yes"
                err.append({'class': 9002001, 'subclass': 1628124317, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['oneway','yes']])
                }})

        # way[oneway=-1]
        if ('oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') == mapcss._value_capture(capture_tags, 0, -1)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is not recommended. Use the Reverse Ways function from the Tools menu.","{0.tag}")
                err.append({'class': 9002016, 'subclass': 579355135, 'text': mapcss.tr('{0} is not recommended. Use the Reverse Ways function from the Tools menu.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[drinkable]
        # Rule Blacklisted (id: 1785584789)

        # *[color][!colour]
        # Rule Blacklisted (id: 1850270072)

        # *[color][colour][color=*colour]
        # Rule Blacklisted (id: 1825345743)

        # *[color][colour]!.samecolor
        # Rule Blacklisted (id: 1064658218)

        # *[building:color][building:colour]!.samebuildingcolor
        # Rule Blacklisted (id: 740601387)

        # *[roof:color][roof:colour]!.sameroofcolor
        # Rule Blacklisted (id: 512779280)

        # *[/:color/][!building:color][!roof:color][!gpxd:color]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_554de4c7)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building:color')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'roof:color')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'gpxd:color')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:":colour"
                # assertNoMatch:"way color=red"
                # assertMatch:"way cycleway:surface:color=grey"
                # assertNoMatch:"way roof:color=grey"
                err.append({'class': 9002001, 'subclass': 1632389707, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/color:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_0c5b5730)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour:"
                # assertMatch:"way color:back=grey"
                # assertNoMatch:"way color=red"
                err.append({'class': 9002001, 'subclass': 1390370717, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/=|\+|\/|&|<|>|;|'|"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_620f4d52)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("key with uncommon character")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002011, 'subclass': 1752615188, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/^.$/]
        # way[/^..$/][route=ferry][!to]
        # way[/^..$/][route!=ferry]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_27210286)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62)) and (mapcss._tag_capture(capture_tags, 1, tags, 'route') == mapcss._value_capture(capture_tags, 1, 'ferry')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'to')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62)) and (mapcss._tag_capture(capture_tags, 1, tags, 'route') != mapcss._value_const_capture(capture_tags, 1, 'ferry', 'ferry')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uncommon short key")
                # assertNoMatch:"way to=Zuidschermer;Akersloot route=ferry"
                # assertMatch:"way to=bar"
                err.append({'class': 9002012, 'subclass': 1765060211, 'text': mapcss.tr('uncommon short key')})

        # *[sport=hockey]
        # Rule Blacklisted (id: 651933474)

        # *[sport=billard]
        # *[sport=billards]
        # *[sport=billiard]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billard')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billards')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billiard')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=billiards"
                # fixAdd:"sport=billiards"
                err.append({'class': 9002001, 'subclass': 1522897824, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['sport','billiards']])
                }})

        # *[payment:ep_quick]
        # *[payment:ep_cash]
        # *[payment:ep_proton]
        # *[payment:ep_chipknip]
        if ('payment:ep_cash' in keys) or ('payment:ep_chipknip' in keys) or ('payment:ep_proton' in keys) or ('payment:ep_quick' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_quick')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_cash')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_proton')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_chipknip')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 332575437, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[kp][railway!=milestone]
        if ('kp' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kp')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'milestone', 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"kp => distance"
                err.append({'class': 9002001, 'subclass': 1256703107, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['distance', mapcss.tag(tags, 'kp')]]),
                    '-': ([
                    'kp'])
                }})

        # *[pk][railway!=milestone]
        if ('pk' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pk')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'milestone', 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"pk => distance"
                err.append({'class': 9002001, 'subclass': 1339969759, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['distance', mapcss.tag(tags, 'pk')]]),
                    '-': ([
                    'pk'])
                }})

        # *[kp][railway=milestone]
        if ('kp' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kp')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"kp => railway:position"
                err.append({'class': 9002001, 'subclass': 1667272140, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'kp')]]),
                    '-': ([
                    'kp'])
                }})

        # *[pk][railway=milestone]
        if ('pk' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pk')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"pk => railway:position"
                err.append({'class': 9002001, 'subclass': 691355164, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'pk')]]),
                    '-': ([
                    'pk'])
                }})

        # *[distance][railway=milestone]
        if ('distance' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"distance => railway:position"
                err.append({'class': 9002001, 'subclass': 113691181, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'distance')]]),
                    '-': ([
                    'distance'])
                }})

        # *[postcode]
        if ('postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"addr:postcode"
                # suggestAlternative:"postal_code"
                err.append({'class': 9002001, 'subclass': 1942523538, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[water=intermittent]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'intermittent')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"intermittent=yes"
                # fixAdd:"intermittent=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 813530321, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['intermittent','yes']]),
                    '-': ([
                    'water'])
                }})

        # way[type][type!=waterway][man_made=pipeline]
        if ('man_made' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') != mapcss._value_const_capture(capture_tags, 1, 'waterway', 'waterway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') == mapcss._value_capture(capture_tags, 2, 'pipeline')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"substance"
                # fixChangeKey:"type => substance"
                err.append({'class': 9002001, 'subclass': 877981524, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['substance', mapcss.tag(tags, 'type')]]),
                    '-': ([
                    'type'])
                }})

        # *[landuse=farm]
        # Rule Blacklisted (id: 1968473048)

        # *[seamark=buoy]["seamark:type"=~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if ('seamark' in keys and 'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seamark') == mapcss._value_capture(capture_tags, 0, 'buoy')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_61b0be1b), mapcss._tag_capture(capture_tags, 1, tags, 'seamark:type'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                # fixRemove:"seamark"
                err.append({'class': 9002001, 'subclass': 1224401740, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'seamark'])
                }})

        # *[seamark=buoy]["seamark:type"!~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if ('seamark' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seamark') == mapcss._value_capture(capture_tags, 0, 'buoy')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61b0be1b, '^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$'), mapcss._tag_capture(capture_tags, 1, tags, 'seamark:type'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9002001, 'subclass': 1481035998, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[landuse=conservation]
        if ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'conservation')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"boundary=protected_area"
                # fixAdd:"boundary=protected_area"
                # fixRemove:"landuse"
                err.append({'class': 9002001, 'subclass': 824801072, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['boundary','protected_area']]),
                    '-': ([
                    'landuse'])
                }})

        # *[amenity=kiosk]
        # Rule Blacklisted (id: 1331930630)

        # *[amenity=shop]
        # Rule Blacklisted (id: 1562207150)

        # *[shop=fishmonger]
        # Rule Blacklisted (id: 1376789416)

        # *[shop=fish]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'fish')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=fishing"
                # suggestAlternative:"shop=pet"
                # suggestAlternative:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 47191734, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=betting]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'betting')))
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
                err.append({'class': 9002001, 'subclass': 1035501389, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=perfume]
        # Rule Blacklisted (id: 2075099676)

        # *[amenity=exercise_point]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'exercise_point')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=fitness_station"
                # fixRemove:"amenity"
                # fixAdd:"leisure=fitness_station"
                err.append({'class': 9002001, 'subclass': 1514920202, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leisure','fitness_station']]),
                    '-': ([
                    'amenity'])
                }})

        # *[shop=auto_parts]
        # Rule Blacklisted (id: 1675828779)

        # *[amenity=car_repair]
        # Rule Blacklisted (id: 1681273585)

        # *[amenity=studio][type=audio]
        # *[amenity=studio][type=radio]
        # *[amenity=studio][type=television]
        # *[amenity=studio][type=video]
        if ('amenity' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'audio')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'radio')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'television')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'video')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"studio"
                # fixChangeKey:"type => studio"
                err.append({'class': 9002001, 'subclass': 413401822, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['studio', mapcss.tag(tags, 'type')]]),
                    '-': ([
                    'type'])
                }})

        # *[power=cable_distribution_cabinet]
        # Rule Blacklisted (id: 1007567078)

        # *[power][location=kiosk]
        if ('location' in keys and 'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power')) and (mapcss._tag_capture(capture_tags, 1, tags, 'location') == mapcss._value_capture(capture_tags, 1, 'kiosk')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # fixRemove:"location"
                # fixAdd:"man_made=street_cabinet"
                # fixAdd:"street_cabinet=power"
                err.append({'class': 9002001, 'subclass': 182905067, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['man_made','street_cabinet'],
                    ['street_cabinet','power']]),
                    '-': ([
                    'location'])
                }})

        # *[man_made=well]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'well')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1740864107, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=dog_bin]
        # *[amenity=dog_waste_bin]
        # Rule Blacklisted (id: 2091877281)

        # *[amenity=artwork]
        # Rule Blacklisted (id: 728429076)

        # *[amenity=community_center]
        # Rule Blacklisted (id: 690512681)

        # *[man_made=cut_line]
        # Rule Blacklisted (id: 1008752382)

        # *[amenity=park]
        # Rule Blacklisted (id: 2085280194)

        # *[amenity=hotel]
        # Rule Blacklisted (id: 1341786818)

        # *[shop=window]
        # *[shop=windows]
        # Rule Blacklisted (id: 532391183)

        # *[amenity=education]
        # Rule Blacklisted (id: 796960259)

        # *[shop=gallery]
        # Rule Blacklisted (id: 1319611546)

        # *[shop=gambling]
        # *[leisure=gambling]
        if ('leisure' in keys) or ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'gambling')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'gambling')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1955724853, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[office=real_estate]
        # *[office=real_estate_agent]
        # Rule Blacklisted (id: 2027311706)

        # *[shop=glass]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'glass')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=glaziery"
                # suggestAlternative:"shop=glaziery"
                err.append({'class': 9002001, 'subclass': 712020531, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=proposed]
        # *[amenity=disused]
        # *[shop=disused]
        # *[highway=abandoned]
        # *[historic=abandoned]
        # Rule Blacklisted (id: 847809313)

        # *[amenity=swimming_pool]
        # Rule Blacklisted (id: 2012807801)

        # *[amenity=sauna]
        # Rule Blacklisted (id: 1450116742)

        # *[/^[^t][^i][^g].+_[0-9]$/][!/^note_[0-9]$/][!/^description_[0-9]$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_300dfa36)) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_3185ac6d)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_6d27b157)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable key (ending with a number)")
                # throwWarning:tr("{0}","{0.key}")
                # assertNoMatch:"way description_3=foo"
                # assertMatch:"way name_1=foo"
                # assertNoMatch:"way note_2=foo"
                # assertNoMatch:"way tiger:name_base_1=bar"
                err.append({'class': 9002014, 'subclass': 2081989305, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[sport=skating]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'skating')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=ice_skating"
                # suggestAlternative:"sport=roller_skating"
                err.append({'class': 9002001, 'subclass': 170699177, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[barrier=wall][type=noise_barrier][!wall]
        # way[barrier=wall][type=noise_barrier][wall=noise_barrier]
        if ('barrier' in keys and 'type' in keys) or ('barrier' in keys and 'type' in keys and 'wall' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wall')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'noise_barrier')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'wall')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wall')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'noise_barrier')) and (mapcss._tag_capture(capture_tags, 2, tags, 'wall') == mapcss._value_capture(capture_tags, 2, 'noise_barrier')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"wall=noise_barrier"
                # fixChangeKey:"type => wall"
                err.append({'class': 9002001, 'subclass': 1513752031, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['wall', mapcss.tag(tags, 'type')]]),
                    '-': ([
                    'type'])
                }})

        # way[barrier=wall][type=noise_barrier][wall][wall!=noise_barrier]
        if ('barrier' in keys and 'type' in keys and 'wall' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wall')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'noise_barrier')) and (mapcss._tag_capture(capture_tags, 2, tags, 'wall')) and (mapcss._tag_capture(capture_tags, 3, tags, 'wall') != mapcss._value_const_capture(capture_tags, 3, 'noise_barrier', 'noise_barrier')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"wall=noise_barrier"
                err.append({'class': 9002001, 'subclass': 2130256462, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[amenity=public_building]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'public_building')))
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
                err.append({'class': 9002001, 'subclass': 1295642010, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[office=administrative]
        # Rule Blacklisted (id: 213844674)

        # *[vending=news_papers]
        if ('vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'news_papers')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=newspapers"
                # fixAdd:"vending=newspapers"
                err.append({'class': 9002001, 'subclass': 1133820292, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['vending','newspapers']])
                }})

        # *[service=drive_through]
        if ('service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service') == mapcss._value_capture(capture_tags, 0, 'drive_through')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"service=drive-through"
                # fixAdd:"service=drive-through"
                err.append({'class': 9002001, 'subclass': 283545650, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['service','drive-through']])
                }})

        # *[noexit][noexit!=yes][noexit!=no]
        # way[highway=service][service][service!~/^(alley|drive-through|drive_through|driveway|emergency_access|parking_aisle|rest_area|slipway|yes)$/]
        # way[railway=rail][service][service!~/^(crossover|siding|spur|yard)$/]
        # way[waterway=canal][service][service!~/^(irrigation|transportation|water_power)$/]
        if ('highway' in keys and 'service' in keys) or ('noexit' in keys) or ('railway' in keys and 'service' in keys) or ('service' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noexit')) and (mapcss._tag_capture(capture_tags, 1, tags, 'noexit') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noexit') != mapcss._value_const_capture(capture_tags, 2, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'service')) and (mapcss._tag_capture(capture_tags, 1, tags, 'service')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_51df498f, '^(alley|drive-through|drive_through|driveway|emergency_access|parking_aisle|rest_area|slipway|yes)$'), mapcss._tag_capture(capture_tags, 2, tags, 'service'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'rail')) and (mapcss._tag_capture(capture_tags, 1, tags, 'service')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2fd4cdcf, '^(crossover|siding|spur|yard)$'), mapcss._tag_capture(capture_tags, 2, tags, 'service'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'canal')) and (mapcss._tag_capture(capture_tags, 1, tags, 'service')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_7a045a17, '^(irrigation|transportation|water_power)$'), mapcss._tag_capture(capture_tags, 2, tags, 'service'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The key {0} has an uncommon value.","{1.key}")
                err.append({'class': 9002017, 'subclass': 806344140, 'text': mapcss.tr('The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[name:botanical]
        # Rule Blacklisted (id: 1061429000)

        # *[shop=souvenir]
        # *[shop=souvenirs]
        # *[shop=souveniers]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souvenir')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souvenirs')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souveniers')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=gift"
                # fixAdd:"shop=gift"
                err.append({'class': 9002001, 'subclass': 1794702946, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','gift']])
                }})

        # *[vending=animal_food]
        if ('vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'animal_food')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=animal_feed"
                # fixAdd:"vending=animal_feed"
                err.append({'class': 9002001, 'subclass': 1077411296, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['vending','animal_feed']])
                }})

        # way[highway=emergency_access_point][phone][!emergency_telephone_code]
        if ('highway' in keys and 'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'emergency_telephone_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # fixChangeKey:"phone => emergency_telephone_code"
                err.append({'class': 9002001, 'subclass': 904792316, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['emergency_telephone_code', mapcss.tag(tags, 'phone')]]),
                    '-': ([
                    'phone'])
                }})

        # way[highway=emergency_access_point][phone=*emergency_telephone_code]
        if ('highway' in keys and 'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'emergency_telephone_code'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                # fixRemove:"phone"
                err.append({'class': 9002001, 'subclass': 3132845, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'phone'])
                }})

        # way[highway=emergency_access_point][phone][emergency_telephone_code][phone!=*emergency_telephone_code]
        if ('emergency_telephone_code' in keys and 'highway' in keys and 'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'emergency_access_point')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone')) and (mapcss._tag_capture(capture_tags, 2, tags, 'emergency_telephone_code')) and (mapcss._tag_capture(capture_tags, 3, tags, 'phone') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'emergency_telephone_code'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"emergency_telephone_code"
                err.append({'class': 9002001, 'subclass': 144379729, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[tracktype=1]
        if ('tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 1)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade1"
                # fixAdd:"tracktype=grade1"
                err.append({'class': 9002018, 'subclass': 823078782, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tracktype','grade1']])
                }})

        # way[tracktype=2]
        if ('tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 2)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade2"
                # fixAdd:"tracktype=grade2"
                err.append({'class': 9002018, 'subclass': 652259155, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tracktype','grade2']])
                }})

        # way[tracktype=3]
        if ('tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 3)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade3"
                # fixAdd:"tracktype=grade3"
                err.append({'class': 9002018, 'subclass': 1624412111, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tracktype','grade3']])
                }})

        # way[tracktype=4]
        if ('tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 4)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade4"
                # fixAdd:"tracktype=grade4"
                err.append({'class': 9002018, 'subclass': 808384986, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tracktype','grade4']])
                }})

        # way[tracktype=5]
        if ('tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 5)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"tracktype=grade5"
                # fixAdd:"tracktype=grade5"
                err.append({'class': 9002018, 'subclass': 1050276122, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tracktype','grade5']])
                }})

        # way[tracktype][tracktype!~/^(1|2|3|4|5|grade1|grade2|grade3|grade4|grade5)$/]
        if ('tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_047d5648, '^(1|2|3|4|5|grade1|grade2|grade3|grade4|grade5)$'), mapcss._tag_capture(capture_tags, 1, tags, 'tracktype'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"tracktype=grade1"
                # suggestAlternative:"tracktype=grade2"
                # suggestAlternative:"tracktype=grade3"
                # suggestAlternative:"tracktype=grade4"
                # suggestAlternative:"tracktype=grade5"
                err.append({'class': 9002019, 'subclass': 1665196665, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=hunting_stand][lock=yes]
        # *[amenity=hunting_stand][lock=no]
        if ('amenity' in keys and 'lock' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'hunting_stand')) and (mapcss._tag_capture(capture_tags, 1, tags, 'lock') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'hunting_stand')) and (mapcss._tag_capture(capture_tags, 1, tags, 'lock') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"lockable"
                # fixChangeKey:"lock => lockable"
                err.append({'class': 9002001, 'subclass': 1939599742, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['lockable', mapcss.tag(tags, 'lock')]]),
                    '-': ([
                    'lock'])
                }})

        # *[amenity=advertising][!advertising]
        # Rule Blacklisted (id: 1696784412)

        # *[amenity=advertising][advertising]
        # Rule Blacklisted (id: 1538706366)

        # way[direction=up][incline=up]
        # way[direction=down][incline=down]
        # way[direction=up][!incline]
        # way[direction=down][!incline]
        if ('direction' in keys) or ('direction' in keys and 'incline' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction') == mapcss._value_capture(capture_tags, 0, 'up')) and (mapcss._tag_capture(capture_tags, 1, tags, 'incline') == mapcss._value_capture(capture_tags, 1, 'up')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction') == mapcss._value_capture(capture_tags, 0, 'down')) and (mapcss._tag_capture(capture_tags, 1, tags, 'incline') == mapcss._value_capture(capture_tags, 1, 'down')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction') == mapcss._value_capture(capture_tags, 0, 'up')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'incline')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction') == mapcss._value_capture(capture_tags, 0, 'down')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'incline')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                # fixChangeKey:"direction => incline"
                err.append({'class': 9002001, 'subclass': 1707030473, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['incline', mapcss.tag(tags, 'direction')]]),
                    '-': ([
                    'direction'])
                }})

        # way[direction=up][incline][incline!=up]
        # way[direction=down][incline][incline!=down]
        if ('direction' in keys and 'incline' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction') == mapcss._value_capture(capture_tags, 0, 'up')) and (mapcss._tag_capture(capture_tags, 1, tags, 'incline')) and (mapcss._tag_capture(capture_tags, 2, tags, 'incline') != mapcss._value_const_capture(capture_tags, 2, 'up', 'up')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'direction') == mapcss._value_capture(capture_tags, 0, 'down')) and (mapcss._tag_capture(capture_tags, 1, tags, 'incline')) and (mapcss._tag_capture(capture_tags, 2, tags, 'incline') != mapcss._value_const_capture(capture_tags, 2, 'down', 'down')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"incline"
                err.append({'class': 9002001, 'subclass': 937812227, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building=true]
        # *[building="*"]
        # *[building=Y]
        # *[building=y]
        # *[building=1]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'true')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, '*')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'Y')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'y')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 1)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"building=yes"
                # fixAdd:"building=yes"
                err.append({'class': 9002018, 'subclass': 596818855, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes']])
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
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'abandoned')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'address')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'bing')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'collapsed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'damaged')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'demolished')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'disused')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'fixme')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'occupied')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'razed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 938825828, 'text': mapcss.tr('{0} is not a building type.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building=other]
        # *[building=unclassified]
        # *[building=undefined]
        # *[building=unknown]
        # *[building=unidentified]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'other')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unclassified')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'undefined')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unknown')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unidentified')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                # fixAdd:"building=yes"
                err.append({'class': 9002001, 'subclass': 48721080, 'text': mapcss.tr('{0} is not a building type.', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes']])
                }})

        # way[water=salt]
        # way[water=salt_pool]
        # way[water=salt_panne]
        # way[water=salt_pond]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'salt')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'salt_pool')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'salt_panne')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'salt_pond')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=salt_pond"
                # suggestAlternative:"salt=yes"
                err.append({'class': 9002001, 'subclass': 403932956, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[water=tidal]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'tidal')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"tidal=yes"
                # fixAdd:"tidal=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 1201030806, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['tidal','yes']]),
                    '-': ([
                    'water'])
                }})

        # *[amenity=toilet]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'toilet')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"amenity=toilets"
                # fixAdd:"amenity=toilets"
                err.append({'class': 9002018, 'subclass': 440018606, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','toilets']])
                }})

        # way[power=busbar]
        if ('power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'busbar')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"power=line + line=busbar"
                # fixAdd:"line=busbar"
                # fixAdd:"power=line"
                err.append({'class': 9002001, 'subclass': 2001565557, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line','busbar'],
                    ['power','line']])
                }})

        # *[man_made=MDF]
        # *[man_made=telephone_exchange]
        # Rule Blacklisted (id: 634698090)

        # *[building=central_office]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'central_office')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"building=yes"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1091970270, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes'],
                    ['telecom','exchange']])
                }})

        # *[telecom=central_office]
        # Rule Blacklisted (id: 1503278830)

        # *[natural=waterfall]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'waterfall')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"waterway=waterfall"
                # fixChangeKey:"natural => waterway"
                err.append({'class': 9002001, 'subclass': 764711734, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['waterway', mapcss.tag(tags, 'natural')]]),
                    '-': ([
                    'natural'])
                }})

        # *[religion=unitarian]
        if ('religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'religion') == mapcss._value_capture(capture_tags, 0, 'unitarian')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"religion=unitarian_universalist"
                # fixAdd:"religion=unitarian_universalist"
                err.append({'class': 9002001, 'subclass': 9227331, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['religion','unitarian_universalist']])
                }})

        # *[shop=shopping_centre]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'shopping_centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=mall"
                # fixAdd:"shop=mall"
                err.append({'class': 9002001, 'subclass': 1448390566, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','mall']])
                }})

        # *[is_in]
        # way[/^is_in:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_69ec353a)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 260361661, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[sport=football]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'football')))
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
                err.append({'class': 9002001, 'subclass': 73038577, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[leisure=common]
        if ('leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'common')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"designation=common"
                # suggestAlternative:"landuse=*"
                # suggestAlternative:"leisure=*"
                err.append({'class': 9002001, 'subclass': 157636301, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[cuisine=vegan]
        # *[cuisine=vegetarian]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine') == mapcss._value_capture(capture_tags, 0, 'vegan')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine') == mapcss._value_capture(capture_tags, 0, 'vegetarian')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("diet:","{0.value}","=only")
                # suggestAlternative:concat("diet:","{0.value}","=yes")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 43604574, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[kitchen_hours]
        if ('kitchen_hours' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kitchen_hours')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"opening_hours:kitchen"
                # fixChangeKey:"kitchen_hours => opening_hours:kitchen"
                err.append({'class': 9002001, 'subclass': 1088306802, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours:kitchen', mapcss.tag(tags, 'kitchen_hours')]]),
                    '-': ([
                    'kitchen_hours'])
                }})

        # *[shop=money_transfer]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'money_transfer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=money_transfer"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 1664997936, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'shop')]]),
                    '-': ([
                    'shop'])
                }})

        # *[contact:google_plus]
        if ('contact:google_plus' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'contact:google_plus')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"contact:google_plus"
                err.append({'class': 9002001, 'subclass': 1869461154, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'contact:google_plus'])
                }})

        # *[amenity=garages]
        # *[amenity=garage]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'garages')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'garage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("building=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + parking=garage_boxes"
                # suggestAlternative:"landuse=garages"
                err.append({'class': 9002001, 'subclass': 863228118, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=winery]
        # *[amenity=winery]
        if ('amenity' in keys) or ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'winery')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'winery')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=winery"
                # suggestAlternative:"shop=wine"
                err.append({'class': 9002001, 'subclass': 1773574987, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=youth_centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'youth_centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre + community_centre=youth_centre"
                # fixAdd:"amenity=community_centre"
                # fixAdd:"community_centre=youth_centre"
                err.append({'class': 9002001, 'subclass': 1284929085, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','community_centre'],
                    ['community_centre','youth_centre']])
                }})

        # *[building:type][building=yes]
        # *[building:type][!building]
        if ('building' in keys and 'building:type' in keys) or ('building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # fixChangeKey:"building:type => building"
                # assertNoMatch:"way building:type=church building=supermarket"
                # assertMatch:"way building:type=church building=yes"
                # assertMatch:"way building:type=church"
                err.append({'class': 9002001, 'subclass': 1927794430, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building', mapcss.tag(tags, 'building:type')]]),
                    '-': ([
                    'building:type'])
                }})

        # *[building:type][building][building!=yes]
        if ('building' in keys and 'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (mapcss._tag_capture(capture_tags, 2, tags, 'building') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # assertMatch:"way building:type=church building=supermarket"
                # assertNoMatch:"way building:type=church building=yes"
                # assertNoMatch:"way building:type=church"
                err.append({'class': 9002001, 'subclass': 1133239698, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[escalator]
        # Rule Blacklisted (id: 967271828)

        # *[fenced]
        # Rule Blacklisted (id: 1141285220)

        # *[historic_name][!old_name]
        # Rule Blacklisted (id: 1034538127)

        # *[historic_name][old_name]
        # Rule Blacklisted (id: 30762614)

        # *[landuse=field]
        # Rule Blacklisted (id: 426261497)

        # *[leisure=beach]
        if ('leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'beach')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=beach_resort"
                # suggestAlternative:"natural=beach"
                err.append({'class': 9002001, 'subclass': 1767286055, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[leisure=club]
        # Rule Blacklisted (id: 1282397509)

        # *[leisure=video_arcade]
        # Rule Blacklisted (id: 1463909830)

        # *[man_made=jetty]
        # Rule Blacklisted (id: 192707176)

        # *[man_made=village_pump]
        # Rule Blacklisted (id: 423232686)

        # *[man_made=water_tank]
        # Rule Blacklisted (id: 563629665)

        # *[natural=moor]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'moor')))
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
                err.append({'class': 9002001, 'subclass': 374637717, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[noexit=no][!fixme]
        # Rule Blacklisted (id: 647435126)

        # *[noexit=no][fixme]
        # Rule Blacklisted (id: 881828009)

        # *[shop=dive]
        # Rule Blacklisted (id: 1582968978)

        # *[shop=furnace]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'furnace')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=plumber"
                # suggestAlternative:"shop=fireplace"
                err.append({'class': 9002001, 'subclass': 1155821104, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[sport=paragliding]
        # Rule Blacklisted (id: 1531788430)

        # *[tourism=bed_and_breakfast]
        # Rule Blacklisted (id: 954237438)

        # *[diaper=yes]
        # *[diaper=no]
        # Rule Blacklisted (id: 1957125311)

        # *[diaper][diaper=~/^[1-9][0-9]*$/]
        if ('diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0f294fdf), mapcss._tag_capture(capture_tags, 1, tags, 'diaper'))))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=yes + changing_table:count=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixAdd:"changing_table=yes"
                # fixChangeKey:"diaper => changing_table:count"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 2105051472, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table','yes'],
                    ['changing_table:count', mapcss.tag(tags, 'diaper')]]),
                    '-': ([
                    'diaper'])
                }})

        # *[diaper=room]
        if ('diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper') == mapcss._value_capture(capture_tags, 0, 'room')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper_checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table=dedicated_room"
                # suggestAlternative:"changing_table=room"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 883202329, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[diaper]!.diaper_checked
        # Rule Blacklisted (id: 693675339)

        # *[diaper:male=yes]
        if ('diaper:male' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:male') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=male_toilet"
                # fixAdd:"changing_table:location=male_toilet"
                # fixRemove:"diaper:male"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 799035479, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','male_toilet']]),
                    '-': ([
                    'diaper:male'])
                }})

        # *[diaper:female=yes]
        if ('diaper:female' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:female') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=female_toilet"
                # fixAdd:"changing_table:location=female_toilet"
                # fixRemove:"diaper:female"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1450901137, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','female_toilet']]),
                    '-': ([
                    'diaper:female'])
                }})

        # *[diaper:unisex=yes]
        if ('diaper:unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:unisex') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=unisex_toilet"
                # fixAdd:"changing_table:location=unisex_toilet"
                # fixRemove:"diaper:unisex"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1460378712, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','unisex_toilet']]),
                    '-': ([
                    'diaper:unisex'])
                }})

        # *[diaper:wheelchair=yes]
        # *[diaper:wheelchair=no]
        if ('diaper:wheelchair' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:wheelchair=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:wheelchair => changing_table:wheelchair"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1951967281, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:wheelchair', mapcss.tag(tags, 'diaper:wheelchair')]]),
                    '-': ([
                    'diaper:wheelchair'])
                }})

        # *[diaper:fee=yes]
        # *[diaper:fee=no]
        if ('diaper:fee' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:fee') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:fee') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:fee=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:fee => changing_table:fee"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 2008573526, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:fee', mapcss.tag(tags, 'diaper:fee')]]),
                    '-': ([
                    'diaper:fee'])
                }})

        # *[/^diaper:/]!.diaper___checked
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_diaper___checked) and (mapcss._tag_capture(capture_tags, 0, tags, self.re_6029fe03)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","diaper:*")
                # suggestAlternative:"changing_table:*"
                err.append({'class': 9002001, 'subclass': 26578864, 'text': mapcss.tr('{0} is deprecated', 'diaper:*')})

        # *[changing_table][changing_table!~/^(yes|no|limited)$/]
        if ('changing_table' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'changing_table')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_787405b1, '^(yes|no|limited)$'), mapcss._tag_capture(capture_tags, 1, tags, 'changing_table'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"changing_table=limited"
                # suggestAlternative:"changing_table=no"
                # suggestAlternative:"changing_table=yes"
                err.append({'class': 9002019, 'subclass': 1965225408, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[roof:shape=half_hipped]
        if ('roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:shape') == mapcss._value_capture(capture_tags, 0, 'half_hipped')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"roof:shape=half-hipped"
                # fixAdd:"roof:shape=half-hipped"
                err.append({'class': 9002001, 'subclass': 1548347123, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['roof:shape','half-hipped']])
                }})

        # *[bridge_name]
        if ('bridge_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge_name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"bridge:name"
                # fixChangeKey:"bridge_name => bridge:name"
                err.append({'class': 9002001, 'subclass': 80069399, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bridge:name', mapcss.tag(tags, 'bridge_name')]]),
                    '-': ([
                    'bridge_name'])
                }})

        # *[access=public]
        # Rule Blacklisted (id: 1115157097)

        # *[crossing=island]
        if ('crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'crossing') == mapcss._value_capture(capture_tags, 0, 'island')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"crossing:island=yes"
                # fixRemove:"crossing"
                # fixAdd:"crossing:island=yes"
                err.append({'class': 9002001, 'subclass': 1512561318, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['crossing:island','yes']]),
                    '-': ([
                    'crossing'])
                }})

        # *[recycling:metal]
        if ('recycling:metal' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'recycling:metal')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"recycling:scrap_metal"
                # fixChangeKey:"recycling:metal => recycling:scrap_metal"
                err.append({'class': 9002001, 'subclass': 474491272, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:scrap_metal', mapcss.tag(tags, 'recycling:metal')]]),
                    '-': ([
                    'recycling:metal'])
                }})

        # *[shop=dog_grooming]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'dog_grooming')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet_grooming"
                # fixAdd:"shop=pet_grooming"
                err.append({'class': 9002001, 'subclass': 1073412885, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','pet_grooming']])
                }})

        # *[tower:type=anchor]
        # *[tower:type=suspension]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'anchor')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'suspension')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"tower:type => line_attachment"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 180380605, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_attachment', mapcss.tag(tags, 'tower:type')]]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=branch][branch:type=split]
        # *[tower:type=branch][branch:type=loop]
        if ('branch:type' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'split')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'loop')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=split"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=split"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 362350862, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','split']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=branch][!branch:type]
        # *[tower:type=branch][branch:type=tap]
        if ('branch:type' in keys and 'tower:type' in keys) or ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'branch:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'tap')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=branch"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=branch"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 476423517, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','branch']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=branch][branch:type=cross]
        if ('branch:type' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'cross')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=cross"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=cross"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 2103059531, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','cross']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=termination]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'termination')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=termination"
                # fixAdd:"line_management=termination"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 232235847, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','termination']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=transition]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'transition')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1124904944, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location:transition','yes']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=transposing]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'transposing')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=transpose"
                # fixAdd:"line_management=transpose"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1795169098, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','transpose']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=crossing]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"height=* + design=*"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1301565974, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[tower:type][power][power=~/^(tower|pole|insulator|portal|terminal)$/]!.power_tower_type_warning
        if ('power' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_power_tower_type_warning) and (mapcss._tag_capture(capture_tags, 0, tags, 'tower:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_24dfeb95), mapcss._tag_capture(capture_tags, 2, tags, 'power'))))
                except mapcss.RuleAbort: pass
            if match:
                # set generic_power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"design"
                # suggestAlternative:"line_attachment"
                # suggestAlternative:"line_management"
                # suggestAlternative:"structure"
                set_generic_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 2020421267, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[pole:type][power][power=~/^(tower|pole|insulator|portal|terminal)$/]!.power_pole_type_warning!.generic_power_tower_type_warning
        if ('pole:type' in keys and 'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_power_pole_type_warning) and (not set_generic_power_tower_type_warning) and (mapcss._tag_capture(capture_tags, 0, tags, 'pole:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_24dfeb95), mapcss._tag_capture(capture_tags, 2, tags, 'power'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"line_attachment"
                # suggestAlternative:"line_management"
                err.append({'class': 9002001, 'subclass': 1513543887, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[barrier=embankment]
        if ('barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'embankment')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"man_made=embankment"
                err.append({'class': 9002001, 'subclass': 2131554464, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[landuse=churchyard]
        if ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'churchyard')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=graveyard"
                # suggestAlternative:"landuse=religious"
                err.append({'class': 9002001, 'subclass': 1973571425, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[sloped_curb=yes][!kerb]
        # *[sloped_curb=both][!kerb]
        if ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'yes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'both')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=lowered"
                # fixAdd:"kerb=lowered"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 1906002413, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['kerb','lowered']]),
                    '-': ([
                    'sloped_curb'])
                }})

        # *[sloped_curb=no][!kerb]
        if ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'no')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=yes"
                # fixAdd:"kerb=yes"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 893727015, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['kerb','yes']]),
                    '-': ([
                    'sloped_curb'])
                }})

        # *[sloped_curb][sloped_curb!~/^(yes|both|no)$/][!kerb]
        # *[sloped_curb][kerb]
        if ('kerb' in keys and 'sloped_curb' in keys) or ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_01eb1711, '^(yes|both|no)$'), mapcss._tag_capture(capture_tags, 1, tags, 'sloped_curb'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb')) and (mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"kerb=*"
                err.append({'class': 9002001, 'subclass': 1682376745, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[unnamed=yes]
        if ('unnamed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'unnamed') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"noname=yes"
                # fixChangeKey:"unnamed => noname"
                err.append({'class': 9002001, 'subclass': 1901447020, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['noname', mapcss.tag(tags, 'unnamed')]]),
                    '-': ([
                    'unnamed'])
                }})

        # way[segregated][segregated!=yes][segregated!=no]
        if ('segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'segregated')) and (mapcss._tag_capture(capture_tags, 1, tags, 'segregated') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'segregated') != mapcss._value_const_capture(capture_tags, 2, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                err.append({'class': 9002020, 'subclass': 1585094150, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[bicycle:oneway]
        if ('bicycle:oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle:oneway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"oneway:bicycle"
                # fixChangeKey:"bicycle:oneway => oneway:bicycle"
                err.append({'class': 9002001, 'subclass': 919622980, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['oneway:bicycle', mapcss.tag(tags, 'bicycle:oneway')]]),
                    '-': ([
                    'bicycle:oneway'])
                }})

        # *[building:height]
        if ('building:height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:height')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"height"
                # fixChangeKey:"building:height => height"
                err.append({'class': 9002001, 'subclass': 1328174745, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['height', mapcss.tag(tags, 'building:height')]]),
                    '-': ([
                    'building:height'])
                }})

        # *[building:min_height]
        if ('building:min_height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:min_height')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"min_height"
                # fixChangeKey:"building:min_height => min_height"
                err.append({'class': 9002001, 'subclass': 1042683921, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['min_height', mapcss.tag(tags, 'building:min_height')]]),
                    '-': ([
                    'building:min_height'])
                }})

        # way[highway][construction=yes][highway!=construction]
        if ('construction' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("highway=construction + construction=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # suggestAlternative:"construction=minor"
                err.append({'class': 9002001, 'subclass': 585996498, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[car][amenity=charging_station]
        # Rule Blacklisted (id: 1165117414)

        # *[navigationaid=approach_light]
        # *[navigationaid="ALS (Approach lighting system)"]
        if ('navigationaid' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'navigationaid') == mapcss._value_capture(capture_tags, 0, 'approach_light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'navigationaid') == mapcss._value_capture(capture_tags, 0, 'ALS (Approach lighting system)')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"navigationaid=als"
                # fixAdd:"navigationaid=als"
                err.append({'class': 9002001, 'subclass': 1577817081, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['navigationaid','als']])
                }})

        # *[water=riverbank][!natural]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                err.append({'class': 9002001, 'subclass': 186872153, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','water'],
                    ['water','river']])
                }})

        # *[water=riverbank][natural]
        if ('natural' in keys and 'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 630806094, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[waterway=riverbank][!natural][!water]
        # *[waterway=riverbank][natural=water][!water]
        # *[waterway=riverbank][!natural][water=river]
        # *[waterway=riverbank][natural=water][water=river]
        if ('natural' in keys and 'water' in keys and 'waterway' in keys) or ('natural' in keys and 'waterway' in keys) or ('water' in keys and 'waterway' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'river')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'river')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                # fixRemove:"waterway"
                # assertNoMatch:"way waterway=riverbank natural=shingle water=river"
                # assertNoMatch:"way waterway=riverbank natural=shingle"
                # assertNoMatch:"way waterway=riverbank natural=water water=lake"
                # assertMatch:"way waterway=riverbank natural=water water=river"
                # assertMatch:"way waterway=riverbank natural=water"
                # assertNoMatch:"way waterway=riverbank water=lake"
                # assertMatch:"way waterway=riverbank water=river"
                # assertMatch:"way waterway=riverbank"
                err.append({'class': 9002001, 'subclass': 1604946271, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','water'],
                    ['water','river']]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=riverbank][natural][natural!=water]
        # *[waterway=riverbank][water][water!=river]
        if ('natural' in keys and 'waterway' in keys) or ('water' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (mapcss._tag_capture(capture_tags, 2, tags, 'natural') != mapcss._value_const_capture(capture_tags, 2, 'water', 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'river', 'river')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # assertMatch:"way waterway=riverbank natural=shingle"
                # assertNoMatch:"way waterway=riverbank natural=water water=river"
                # assertNoMatch:"way waterway=riverbank natural=water"
                # assertMatch:"way waterway=riverbank water=lake"
                # assertNoMatch:"way waterway=riverbank water=river"
                # assertNoMatch:"way waterway=riverbank"
                err.append({'class': 9002001, 'subclass': 301661430, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[amenity=bench][capacity][!seats]
        if ('amenity' in keys and 'capacity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'bench')) and (mapcss._tag_capture(capture_tags, 1, tags, 'capacity')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'seats')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"seats"
                # fixChangeKey:"capacity => seats"
                err.append({'class': 9002001, 'subclass': 1511456494, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['seats', mapcss.tag(tags, 'capacity')]]),
                    '-': ([
                    'capacity'])
                }})

        # way[amenity=bench][capacity][seats]
        if ('amenity' in keys and 'capacity' in keys and 'seats' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'bench')) and (mapcss._tag_capture(capture_tags, 1, tags, 'capacity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'seats')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"seats"
                err.append({'class': 9002001, 'subclass': 1445114632, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[stream=intermittent]
        if ('stream' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'stream') == mapcss._value_capture(capture_tags, 0, 'intermittent')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"intermittent=yes"
                # suggestAlternative:"seasonal=yes"
                err.append({'class': 9002001, 'subclass': 1710194213, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=lamps]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'lamps')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=lighting"
                # fixAdd:"shop=lighting"
                err.append({'class': 9002001, 'subclass': 746886011, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','lighting']])
                }})

        # *[access=customer]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'customer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"access=customers"
                # fixAdd:"access=customers"
                err.append({'class': 9002001, 'subclass': 1040065637, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['access','customers']])
                }})

        # *[addr:inclusion=estimated]
        if ('addr:inclusion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:inclusion') == mapcss._value_capture(capture_tags, 0, 'estimated')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"addr:inclusion=estimate"
                # fixAdd:"addr:inclusion=estimate"
                err.append({'class': 9002001, 'subclass': 1002643753, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['addr:inclusion','estimate']])
                }})

        # *[building=apartment]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'apartment')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"building=apartments"
                # fixAdd:"building=apartments"
                err.append({'class': 9002001, 'subclass': 1384168519, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','apartments']])
                }})

        # *[generator:type=solar_photovoltaic_panels]
        if ('generator:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:type') == mapcss._value_capture(capture_tags, 0, 'solar_photovoltaic_panels')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:type=solar_photovoltaic_panel"
                # fixAdd:"generator:type=solar_photovoltaic_panel"
                err.append({'class': 9002001, 'subclass': 1146719875, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:type','solar_photovoltaic_panel']])
                }})

        # *[building=part]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'part')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"building:part=yes"
                err.append({'class': 9002001, 'subclass': 455695847, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[natural=sink_hole]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'sink_hole')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=sinkhole"
                # fixAdd:"natural=sinkhole"
                err.append({'class': 9002001, 'subclass': 1283355945, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','sinkhole']])
                }})

        # *[climbing:grade:UIAA:min]
        if ('climbing:grade:UIAA:min' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:min')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:min"
                # fixChangeKey:"climbing:grade:UIAA:min => climbing:grade:uiaa:min"
                err.append({'class': 9002001, 'subclass': 1408052420, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:min', mapcss.tag(tags, 'climbing:grade:UIAA:min')]]),
                    '-': ([
                    'climbing:grade:UIAA:min'])
                }})

        # *[climbing:grade:UIAA:max]
        if ('climbing:grade:UIAA:max' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:max')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:max"
                # fixChangeKey:"climbing:grade:UIAA:max => climbing:grade:uiaa:max"
                err.append({'class': 9002001, 'subclass': 1866245426, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:max', mapcss.tag(tags, 'climbing:grade:UIAA:max')]]),
                    '-': ([
                    'climbing:grade:UIAA:max'])
                }})

        # *[climbing:grade:UIAA:mean]
        if ('climbing:grade:UIAA:mean' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:mean')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:mean"
                # fixChangeKey:"climbing:grade:UIAA:mean => climbing:grade:uiaa:mean"
                err.append({'class': 9002001, 'subclass': 1022648087, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:mean', mapcss.tag(tags, 'climbing:grade:UIAA:mean')]]),
                    '-': ([
                    'climbing:grade:UIAA:mean'])
                }})

        # *[climbing:grade:UIAA]
        if ('climbing:grade:UIAA' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa"
                # fixChangeKey:"climbing:grade:UIAA => climbing:grade:uiaa"
                err.append({'class': 9002001, 'subclass': 1007893519, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa', mapcss.tag(tags, 'climbing:grade:UIAA')]]),
                    '-': ([
                    'climbing:grade:UIAA'])
                }})

        # *[cuisine][cuisine=~/^(?i)(bbq)$/]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2f881233), mapcss._tag_capture(capture_tags, 1, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # set bbq_autofix
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"cuisine=barbecue"
                # fixAdd:"cuisine=barbecue"
                # assertMatch:"way cuisine=BBQ"
                # assertMatch:"way cuisine=bbq"
                # assertNoMatch:"way cuisine=bbq;pizza"
                # assertNoMatch:"way cuisine=korean_bbq"
                # assertNoMatch:"way cuisine=korean_bbq;bbq"
                # assertNoMatch:"way cuisine=pasta;bbq;pizza"
                # assertNoMatch:"way cuisine=pizza;Bbq"
                # assertNoMatch:"way cuisine=pizza;bbq"
                set_bbq_autofix = True
                err.append({'class': 9002001, 'subclass': 1943338875, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['cuisine','barbecue']])
                }})

        # *[cuisine=~/(?i)(;bbq|bbq;)/][cuisine!~/(?i)(_bbq)/]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_340a2b31), mapcss._tag_capture(capture_tags, 0, tags, 'cuisine'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7d409ed5, '(?i)(_bbq)'), mapcss._tag_capture(capture_tags, 1, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","cuisine=bbq")
                # suggestAlternative:"cuisine=barbecue"
                # assertNoMatch:"way cuisine=BBQ"
                # assertNoMatch:"way cuisine=bbq"
                # assertMatch:"way cuisine=bbq;pizza"
                # assertNoMatch:"way cuisine=korean_bbq"
                # assertNoMatch:"way cuisine=korean_bbq;bbq"
                # assertMatch:"way cuisine=pasta;bbq;pizza"
                # assertMatch:"way cuisine=pizza;Bbq"
                # assertMatch:"way cuisine=pizza;bbq"
                err.append({'class': 9002001, 'subclass': 1958782130, 'text': mapcss.tr('{0} is deprecated', 'cuisine=bbq')})

        # way[cycleway=none]
        # way[cycleway:left=none]
        # way[cycleway:right=none]
        # way[shoulder=none]
        if ('cycleway' in keys) or ('cycleway:left' in keys) or ('cycleway:right' in keys) or ('shoulder' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway') == mapcss._value_capture(capture_tags, 0, 'none')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left') == mapcss._value_capture(capture_tags, 0, 'none')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:right') == mapcss._value_capture(capture_tags, 0, 'none')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shoulder') == mapcss._value_capture(capture_tags, 0, 'none')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("{0.key}","=no")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixAdd:concat("{0.key}","=no")
                err.append({'class': 9002001, 'subclass': 1752530337, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{0.key}'), '=no')).split('=', 1)])
                }})

        # *[Fixme]
        if ('Fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'Fixme')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"fixme"
                # fixChangeKey:"Fixme => fixme"
                # assertNoMatch:"way FIXME=foo"
                # assertMatch:"way Fixme=foo"
                # assertNoMatch:"way fixme=foo"
                err.append({'class': 9002001, 'subclass': 592643943, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['fixme', mapcss.tag(tags, 'Fixme')]]),
                    '-': ([
                    'Fixme'])
                }})

        # *[amenity=embassy]
        # Rule Blacklisted (id: 1751915206)

        # *[service:bicycle:chaintool]
        if ('service:bicycle:chaintool' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service:bicycle:chaintool')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"service:bicycle:chain_tool"
                # fixChangeKey:"service:bicycle:chaintool => service:bicycle:chain_tool"
                err.append({'class': 9002001, 'subclass': 1464143873, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['service:bicycle:chain_tool', mapcss.tag(tags, 'service:bicycle:chaintool')]]),
                    '-': ([
                    'service:bicycle:chaintool'])
                }})

        # *[building:roof:shape]
        if ('building:roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:roof:shape')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"roof:shape"
                # fixChangeKey:"building:roof:shape => roof:shape"
                err.append({'class': 9002001, 'subclass': 2106920042, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['roof:shape', mapcss.tag(tags, 'building:roof:shape')]]),
                    '-': ([
                    'building:roof:shape'])
                }})

        # *[man_made=pumping_rig][!pump_mechanism][!mechanical_driver][!mechanical_coupling]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pumping_rig')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'pump_mechanism')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mechanical_coupling')))
                except mapcss.RuleAbort: pass
            if match:
                # set pumping_ring_no_mech
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                # fixAdd:"mechanical_coupling=nodding_donkey"
                # fixAdd:"mechanical_driver=combustion_engine"
                # fixAdd:"pump_mechanism=piston"
                set_pumping_ring_no_mech = True
                err.append({'class': 9002001, 'subclass': 6568074, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mechanical_coupling','nodding_donkey'],
                    ['mechanical_driver','combustion_engine'],
                    ['pump_mechanism','piston']])
                }})

        # *[man_made=pumping_rig]!.pumping_ring_no_mech
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_pumping_ring_no_mech) and (mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pumping_rig')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1031026578, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[pump:type=beam_pump][!pump_mechanism][!mechanical_driver][!mechanical_coupling]
        if ('pump:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pump:type') == mapcss._value_capture(capture_tags, 0, 'beam_pump')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'pump_mechanism')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mechanical_coupling')))
                except mapcss.RuleAbort: pass
            if match:
                # set beam_pump_no_mech
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"pump_mechanism"
                # fixAdd:"mechanical_coupling=nodding_donkey"
                # fixAdd:"mechanical_driver=combustion_engine"
                # fixRemove:"pump:type"
                # fixAdd:"pump_mechanism=piston"
                set_beam_pump_no_mech = True
                err.append({'class': 9002001, 'subclass': 1519103279, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mechanical_coupling','nodding_donkey'],
                    ['mechanical_driver','combustion_engine'],
                    ['pump_mechanism','piston']]),
                    '-': ([
                    'pump:type'])
                }})

        # *[pump:type]!.beam_pump_no_mech
        if ('pump:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_beam_pump_no_mech) and (mapcss._tag_capture(capture_tags, 0, tags, 'pump:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"pump_mechanism"
                err.append({'class': 9002001, 'subclass': 2015679777, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[substance=heat]
        if ('substance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'substance') == mapcss._value_capture(capture_tags, 0, 'heat')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"substance=hot_water"
                # suggestAlternative:"substance=steam"
                err.append({'class': 9002001, 'subclass': 1528467304, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[landuse=school]
        if ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'school')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=college"
                # suggestAlternative:"amenity=school"
                # suggestAlternative:"amenity=university"
                # suggestAlternative:"landuse=education"
                err.append({'class': 9002001, 'subclass': 817812278, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[surface=decoturf]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface') == mapcss._value_capture(capture_tags, 0, 'decoturf')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"surface=acrylic"
                # fixAdd:"surface=acrylic"
                err.append({'class': 9002001, 'subclass': 1995300591, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['surface','acrylic']])
                }})

        # *[role]
        # Rule Blacklisted (id: 2041296832)

        # *[school=entrance]
        if ('school' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'school') == mapcss._value_capture(capture_tags, 0, 'entrance')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"entrance=main"
                # suggestAlternative:"entrance=yes"
                err.append({'class': 9002001, 'subclass': 1398581809, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[voltage-high]
        # *[voltage-low]
        if ('voltage-high' in keys) or ('voltage-low' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage-high')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage-low')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"voltage:primary"
                # suggestAlternative:"voltage:secondary"
                err.append({'class': 9002001, 'subclass': 1379077827, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[toilet][!toilets]
        if ('toilet' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toilet')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'toilets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"toilets"
                # fixChangeKey:"toilet => toilets"
                err.append({'class': 9002001, 'subclass': 466700565, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['toilets', mapcss.tag(tags, 'toilet')]]),
                    '-': ([
                    'toilet'])
                }})

        # *[toilet][toilets]
        if ('toilet' in keys and 'toilets' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toilet')) and (mapcss._tag_capture(capture_tags, 1, tags, 'toilets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"toilets"
                err.append({'class': 9002001, 'subclass': 1092230744, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[type="turnlanes:turns"]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'turnlanes:turns')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"type=connectivity"
                err.append({'class': 9002001, 'subclass': 1789083769, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[image][image=~/^https:\/\/westnordost.de\/p\//]
        if ('image' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'image')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0fbae48f), mapcss._tag_capture(capture_tags, 1, tags, 'image'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} with a temporary URL which may be outdated very soon","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002023, 'subclass': 2042174729, 'text': mapcss.tr('{0} with a temporary URL which may be outdated very soon', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[historic=archaeological_site][site_type]
        if ('historic' in keys and 'site_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'historic') == mapcss._value_capture(capture_tags, 0, 'archaeological_site')) and (mapcss._tag_capture(capture_tags, 1, tags, 'site_type')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be replaced with {1}","{1.key}","archaeological_site")
                # fixChangeKey:"site_type => archaeological_site"
                err.append({'class': 9002008, 'subclass': 595008939, 'text': mapcss.tr('{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), 'archaeological_site'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['archaeological_site', mapcss.tag(tags, 'site_type')]]),
                    '-': ([
                    'site_type'])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_bbq_autofix = set_beam_pump_no_mech = set_diaper___checked = set_diaper_checked = set_generic_power_tower_type_warning = set_levels_building = set_power_pole_type_warning = set_power_tower_type_warning = set_pumping_ring_no_mech = False

        # *[barrier=wire_fence]
        if ('barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wire_fence')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 1107799632, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['barrier','fence'],
                    ['fence_type','chain_link']])
                }})

        # *[barrier=wood_fence]
        if ('barrier' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'wood_fence')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=fence + fence_type=wood"
                # fixAdd:"barrier=fence"
                # fixAdd:"fence_type=wood"
                err.append({'class': 9002001, 'subclass': 1412230714, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['barrier','fence'],
                    ['fence_type','wood']])
                }})

        # *[highway=stile]
        # Rule Blacklisted (id: 1435678043)

        # *[highway=incline]
        # Rule Blacklisted (id: 765169083)

        # *[highway=incline_steep]
        # Rule Blacklisted (id: 1966772390)

        # *[highway=unsurfaced]
        # Rule Blacklisted (id: 20631498)

        # *[landuse=wood]
        # Rule Blacklisted (id: 469903103)

        # *[natural=marsh]
        # Rule Blacklisted (id: 1459865523)

        # *[highway=byway]
        # Rule Blacklisted (id: 1844620979)

        # *[power_source]
        # Rule Blacklisted (id: 34751027)

        # *[power_rating]
        # Rule Blacklisted (id: 904750343)

        # *[shop=antique]
        # Rule Blacklisted (id: 596668979)

        # *[shop=bags]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'bags')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=bag"
                # fixAdd:"shop=bag"
                err.append({'class': 9002001, 'subclass': 1709003584, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','bag']])
                }})

        # *[shop=fashion]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'fashion')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=clothes"
                # fixAdd:"shop=clothes"
                err.append({'class': 9002001, 'subclass': 985619804, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','clothes']])
                }})

        # *[shop=organic]
        # Rule Blacklisted (id: 1959365145)

        # *[shop=pets]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'pets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet"
                # fixAdd:"shop=pet"
                err.append({'class': 9002001, 'subclass': 290270098, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','pet']])
                }})

        # *[shop=pharmacy]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'pharmacy')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=pharmacy"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 350722657, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'shop')]]),
                    '-': ([
                    'shop'])
                }})

        # *[bicycle_parking=sheffield]
        if ('bicycle_parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle_parking') == mapcss._value_capture(capture_tags, 0, 'sheffield')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bicycle_parking=stands"
                # fixAdd:"bicycle_parking=stands"
                err.append({'class': 9002001, 'subclass': 718874663, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bicycle_parking','stands']])
                }})

        # *[amenity=emergency_phone]
        # Rule Blacklisted (id: 1108230656)

        # *[sport=gaelic_football]
        # Rule Blacklisted (id: 1768681881)

        # *[power=station]
        # Rule Blacklisted (id: 52025933)

        # *[power=sub_station]
        # Rule Blacklisted (id: 1423074682)

        # *[location=rooftop]
        if ('location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'location') == mapcss._value_capture(capture_tags, 0, 'rooftop')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location=roof"
                # fixAdd:"location=roof"
                err.append({'class': 9002001, 'subclass': 1028577225, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location','roof']])
                }})

        # *[generator:location]
        if ('generator:location' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:location')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"location"
                # fixChangeKey:"generator:location => location"
                err.append({'class': 9002001, 'subclass': 900615917, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location', mapcss.tag(tags, 'generator:location')]]),
                    '-': ([
                    'generator:location'])
                }})

        # *[generator:method=dam]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'dam')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-storage"
                # fixAdd:"generator:method=water-storage"
                err.append({'class': 9002001, 'subclass': 248819368, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-storage']])
                }})

        # *[generator:method=pumped-storage]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'pumped-storage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 93454158, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-pumped-storage']])
                }})

        # *[generator:method=pumping]
        if ('generator:method' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method') == mapcss._value_capture(capture_tags, 0, 'pumping')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:method=water-pumped-storage"
                # fixAdd:"generator:method=water-pumped-storage"
                err.append({'class': 9002001, 'subclass': 2115673716, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:method','water-pumped-storage']])
                }})

        # *[fence_type=chain]
        if ('fence_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fence_type') == mapcss._value_capture(capture_tags, 0, 'chain')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"barrier=chain"
                # suggestAlternative:"barrier=fence + fence_type=chain_link"
                err.append({'class': 9002001, 'subclass': 19409288, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building=entrance]
        # Rule Blacklisted (id: 306662985)

        # *[board_type=board]
        if ('board_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'board_type') == mapcss._value_capture(capture_tags, 0, 'board')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixRemove:"board_type"
                err.append({'class': 9002001, 'subclass': 1150949316, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'board_type'])
                }})

        # *[man_made=measurement_station]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'measurement_station')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=monitoring_station"
                # fixAdd:"man_made=monitoring_station"
                err.append({'class': 9002001, 'subclass': 700465123, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['man_made','monitoring_station']])
                }})

        # *[measurement=water_level]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'water_level')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:water_level=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:water_level=yes"
                err.append({'class': 9002001, 'subclass': 634647702, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:water_level','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[measurement=weather]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'weather')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:weather=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:weather=yes"
                err.append({'class': 9002001, 'subclass': 336627227, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:weather','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[measurement=seismic]
        if ('measurement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'measurement') == mapcss._value_capture(capture_tags, 0, 'seismic')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"monitoring:seismic_activity=yes"
                # fixRemove:"measurement"
                # fixAdd:"monitoring:seismic_activity=yes"
                err.append({'class': 9002001, 'subclass': 1402131289, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:seismic_activity','yes']]),
                    '-': ([
                    'measurement'])
                }})

        # *[monitoring:river_level]
        if ('monitoring:river_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'monitoring:river_level')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"monitoring:water_level"
                # fixChangeKey:"monitoring:river_level => monitoring:water_level"
                err.append({'class': 9002001, 'subclass': 264907924, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['monitoring:water_level', mapcss.tag(tags, 'monitoring:river_level')]]),
                    '-': ([
                    'monitoring:river_level'])
                }})

        # *[stay]
        if ('stay' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'stay')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"maxstay"
                # fixChangeKey:"stay => maxstay"
                err.append({'class': 9002001, 'subclass': 787370129, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxstay', mapcss.tag(tags, 'stay')]]),
                    '-': ([
                    'stay'])
                }})

        # *[emergency=aed]
        # Rule Blacklisted (id: 707111885)

        # *[day_on][!restriction]
        # *[day_off][!restriction]
        # *[date_on][!restriction]
        # *[date_off][!restriction]
        # *[hour_on][!restriction]
        # *[hour_off][!restriction]
        # Rule Blacklisted (id: 294264920)

        # *[access=designated]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'designated')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' is meaningless, use more specific tags, e.g. ''{1}''","access=designated","bicycle=designated")
                err.append({'class': 9002002, 'subclass': 2057594338, 'text': mapcss.tr('\'\'{0}\'\' is meaningless, use more specific tags, e.g. \'\'{1}\'\'', 'access=designated', 'bicycle=designated')})

        # *[access=official]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'official')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' does not specify the official mode of transportation, use ''{1}'' for example","access=official","bicycle=official")
                err.append({'class': 9002003, 'subclass': 1909133836, 'text': mapcss.tr('\'\'{0}\'\' does not specify the official mode of transportation, use \'\'{1}\'\' for example', 'access=official', 'bicycle=official')})

        # *[fixme=yes]
        # *[FIXME=yes]
        if ('FIXME' in keys) or ('fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fixme') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'FIXME') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Instead of ''{1}'' please give more information about what exactly should be fixed.","{0.key}","{0.value}")
                err.append({'class': 9002004, 'subclass': 136657482, 'text': mapcss.tr('{0}={1} is unspecific. Instead of \'\'{1}\'\' please give more information about what exactly should be fixed.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # *[name][name=~/^(?i)fixme$/]
        if ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.","{0.key}","{0.tag}")
                # fixRemove:"name"
                err.append({'class': 9002005, 'subclass': 642340557, 'text': mapcss.tr('Wrong usage of {0} tag. Remove {1}, because it is clear that the name is missing even without an additional tag.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'name'])
                }})

        # *[note][note=~/^(?i)fixme$/]
        if ('note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'note')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1f92073a), mapcss._tag_capture(capture_tags, 1, tags, 'note'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.","{0.tag}")
                err.append({'class': 9002006, 'subclass': 1243120287, 'text': mapcss.tr('{0} is unspecific. Instead use the key fixme with the information what exactly should be fixed in the value of fixme.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[type=broad_leaved]
        # *[type=broad_leafed]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'broad_leaved')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'broad_leafed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=broadleaved"
                # fixAdd:"leaf_type=broadleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 293968062, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','broadleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=coniferous]
        # *[type=coniferous]
        # *[type=conifer]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'coniferous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'coniferous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'conifer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=needleleaved"
                # fixAdd:"leaf_type=needleleaved"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 50517650, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','needleleaved']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=mixed]
        if ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'mixed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_type=mixed"
                # fixAdd:"leaf_type=mixed"
                # fixRemove:"wood"
                err.append({'class': 9002001, 'subclass': 235914603, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_type','mixed']]),
                    '-': ([
                    'wood'])
                }})

        # *[wood=evergreen]
        # *[type=evergreen]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'evergreen')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'evergreen')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=evergreen"
                # fixAdd:"leaf_cycle=evergreen"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 747964532, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_cycle','evergreen']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[wood=deciduous]
        # *[type=deciduous]
        # *[type=deciduos]
        if ('type' in keys) or ('wood' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'wood') == mapcss._value_capture(capture_tags, 0, 'deciduous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'deciduous')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'deciduos')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leaf_cycle=deciduous"
                # fixAdd:"leaf_cycle=deciduous"
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 1458103800, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leaf_cycle','deciduous']]),
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[natural=land]
        # Rule Blacklisted (id: 94558529)

        # *[bridge=causeway]
        if ('bridge' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge') == mapcss._value_capture(capture_tags, 0, 'causeway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"bridge=low_water_crossing"
                # suggestAlternative:"embankment=yes"
                # suggestAlternative:"ford=yes"
                err.append({'class': 9002001, 'subclass': 461671124, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[bridge=swing]
        # Rule Blacklisted (id: 1047428067)

        # *[bridge=suspension]
        # Rule Blacklisted (id: 1157046268)

        # *[bridge=pontoon]
        # Rule Blacklisted (id: 1195531951)

        # *[fee=interval]
        # *[lit=interval]
        # *[supervised=interval]
        if ('fee' in keys) or ('lit' in keys) or ('supervised' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fee') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lit') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'supervised') == mapcss._value_capture(capture_tags, 0, 'interval')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated. Please specify interval by using opening_hours syntax","{0.tag}")
                err.append({'class': 9002001, 'subclass': 417886592, 'text': mapcss.tr('{0} is deprecated. Please specify interval by using opening_hours syntax', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[/josm\/ignore/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_5ee0acf2)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwError:tr("{0} is deprecated. Please delete this object and use a private layer instead","{0.key}")
                # fixDeleteObject:this
                err.append({'class': 9002001, 'subclass': 1402743016, 'text': mapcss.tr('{0} is deprecated. Please delete this object and use a private layer instead', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[sport=diving]
        # Rule Blacklisted (id: 590643159)

        # *[parking=park_and_ride]
        if ('parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking') == mapcss._value_capture(capture_tags, 0, 'park_and_ride')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + park_ride=yes"
                # fixAdd:"amenity=parking"
                # fixAdd:"park_ride=yes"
                # fixRemove:"parking"
                err.append({'class': 9002001, 'subclass': 1893516041, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','parking'],
                    ['park_ride','yes']]),
                    '-': ([
                    'parking'])
                }})

        # *[parking=yes]
        # *[playground=yes]
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
        # *[landuse=yes]
        # *[shop="*"]
        # *[shop=yes][amenity!=fuel]
        # *[craft=yes]
        # *[service=yes]
        # *[place=yes]
        if ('access' in keys) or ('aerialway' in keys) or ('amenity' in keys) or ('barrier' in keys) or ('craft' in keys) or ('landuse' in keys) or ('leisure' in keys) or ('manhole' in keys) or ('parking' in keys) or ('place' in keys) or ('playground' in keys) or ('police' in keys) or ('service' in keys) or ('shop' in keys) or ('traffic_calming' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'playground') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'plain')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'unknown')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'police') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_calming') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'restricted')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'yes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'public_transport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, '*')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'fuel', 'fuel')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'craft') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0}={1} is unspecific. Please replace ''{1}'' by a specific value.","{0.key}","{0.value}")
                err.append({'class': 9002007, 'subclass': 1452069773, 'text': mapcss.tr('{0}={1} is unspecific. Please replace \'\'{1}\'\' by a specific value.', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # *[place_name][!name]
        # Rule Blacklisted (id: 1089331760)

        # *[place][place_name=*name]
        # Rule Blacklisted (id: 1116761280)

        # *[waterway=water_point]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'water_point')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=water_point"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 103347605, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'waterway')]]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=waste_disposal]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'waste_disposal')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=waste_disposal"
                # fixChangeKey:"waterway => amenity"
                err.append({'class': 9002001, 'subclass': 1963461348, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'waterway')]]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=mooring]
        if ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'mooring')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"mooring=yes"
                # fixAdd:"mooring=yes"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 81358738, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mooring','yes']]),
                    '-': ([
                    'waterway'])
                }})

        # *[building][levels]
        # *[building:part][levels]
        if ('building' in keys and 'levels' in keys) or ('building:part' in keys and 'levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')) and (mapcss._tag_capture(capture_tags, 1, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if match:
                # set levels_building
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.key}")
                # suggestAlternative:"building:levels"
                # fixChangeKey:"levels => building:levels"
                set_levels_building = True
                err.append({'class': 9002001, 'subclass': 869936714, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building:levels', mapcss.tag(tags, 'levels')]]),
                    '-': ([
                    'levels'])
                }})

        # *[levels]!.levels_building
        if ('levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_levels_building) and (mapcss._tag_capture(capture_tags, 0, tags, 'levels')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unusual key {0}, maybe {1} or {2} is meant","{0.key}","level","building:levels")
                err.append({'class': 9002021, 'subclass': 1172699526, 'text': mapcss.tr('Unusual key {0}, maybe {1} or {2} is meant', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'level', 'building:levels')})

        # *[protected_class]
        if ('protected_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'protected_class')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"protect_class"
                # fixChangeKey:"protected_class => protect_class"
                err.append({'class': 9002001, 'subclass': 716999373, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['protect_class', mapcss.tag(tags, 'protected_class')]]),
                    '-': ([
                    'protected_class'])
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
        # Rule Blacklisted (id: 1052866123)

        # *[sport=skiing]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'skiing')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("Definition of {0} is unclear","{0.tag}")
                # suggestAlternative:tr("{0} + {1} + {2}","piste:type=*","piste:difficulty=*","piste:grooming=*")
                err.append({'class': 9002001, 'subclass': 1578959559, 'text': mapcss.tr('Definition of {0} is unclear', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[waterway=wadi]
        # Rule Blacklisted (id: 719234223)

        # *[drinkable]
        # Rule Blacklisted (id: 1785584789)

        # *[color][!colour]
        # Rule Blacklisted (id: 1850270072)

        # *[color][colour][color=*colour]
        # Rule Blacklisted (id: 1825345743)

        # *[color][colour]!.samecolor
        # Rule Blacklisted (id: 1064658218)

        # *[building:color][building:colour]!.samebuildingcolor
        # Rule Blacklisted (id: 740601387)

        # *[roof:color][roof:colour]!.sameroofcolor
        # Rule Blacklisted (id: 512779280)

        # *[/:color/][!building:color][!roof:color][!gpxd:color]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_554de4c7)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building:color')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'roof:color')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'gpxd:color')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:":colour"
                err.append({'class': 9002001, 'subclass': 1632389707, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/color:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_0c5b5730)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"colour:"
                err.append({'class': 9002001, 'subclass': 1390370717, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/=|\+|\/|&|<|>|;|'|"|%|#|@|\\|,|\.|\{|\}|\?|\*|\^|\$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_620f4d52)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("key with uncommon character")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002011, 'subclass': 1752615188, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[/^.$/]
        # relation[/^..$/][!to]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_27210286)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_34c15d62)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'to')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uncommon short key")
                # assertMatch:"relation fo=bar"
                # assertNoMatch:"relation to=Berlin"
                err.append({'class': 9002012, 'subclass': 518970721, 'text': mapcss.tr('uncommon short key')})

        # *[sport=hockey]
        # Rule Blacklisted (id: 651933474)

        # *[sport=billard]
        # *[sport=billards]
        # *[sport=billiard]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billard')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billards')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'billiard')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=billiards"
                # fixAdd:"sport=billiards"
                err.append({'class': 9002001, 'subclass': 1522897824, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['sport','billiards']])
                }})

        # *[payment:ep_quick]
        # *[payment:ep_cash]
        # *[payment:ep_proton]
        # *[payment:ep_chipknip]
        if ('payment:ep_cash' in keys) or ('payment:ep_chipknip' in keys) or ('payment:ep_proton' in keys) or ('payment:ep_quick' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_quick')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_cash')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_proton')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'payment:ep_chipknip')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 332575437, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[kp][railway!=milestone]
        if ('kp' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kp')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'milestone', 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"kp => distance"
                err.append({'class': 9002001, 'subclass': 1256703107, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['distance', mapcss.tag(tags, 'kp')]]),
                    '-': ([
                    'kp'])
                }})

        # *[pk][railway!=milestone]
        if ('pk' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pk')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'milestone', 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"distance"
                # fixChangeKey:"pk => distance"
                err.append({'class': 9002001, 'subclass': 1339969759, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['distance', mapcss.tag(tags, 'pk')]]),
                    '-': ([
                    'pk'])
                }})

        # *[kp][railway=milestone]
        if ('kp' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kp')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"kp => railway:position"
                err.append({'class': 9002001, 'subclass': 1667272140, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'kp')]]),
                    '-': ([
                    'kp'])
                }})

        # *[pk][railway=milestone]
        if ('pk' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pk')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"pk => railway:position"
                err.append({'class': 9002001, 'subclass': 691355164, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'pk')]]),
                    '-': ([
                    'pk'])
                }})

        # *[distance][railway=milestone]
        if ('distance' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'distance')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') == mapcss._value_capture(capture_tags, 1, 'milestone')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"railway:position"
                # fixChangeKey:"distance => railway:position"
                err.append({'class': 9002001, 'subclass': 113691181, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway:position', mapcss.tag(tags, 'distance')]]),
                    '-': ([
                    'distance'])
                }})

        # *[postcode]
        if ('postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"addr:postcode"
                # suggestAlternative:"postal_code"
                err.append({'class': 9002001, 'subclass': 1942523538, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[water=intermittent]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'intermittent')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"intermittent=yes"
                # fixAdd:"intermittent=yes"
                # fixRemove:"water"
                err.append({'class': 9002001, 'subclass': 813530321, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['intermittent','yes']]),
                    '-': ([
                    'water'])
                }})

        # *[landuse=farm]
        # Rule Blacklisted (id: 1968473048)

        # *[seamark=buoy]["seamark:type"=~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if ('seamark' in keys and 'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seamark') == mapcss._value_capture(capture_tags, 0, 'buoy')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_61b0be1b), mapcss._tag_capture(capture_tags, 1, tags, 'seamark:type'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                # fixRemove:"seamark"
                err.append({'class': 9002001, 'subclass': 1224401740, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'seamark'])
                }})

        # *[seamark=buoy]["seamark:type"!~/^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$/]
        if ('seamark' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'seamark') == mapcss._value_capture(capture_tags, 0, 'buoy')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_61b0be1b, '^(buoy_cardinal|buoy_installation|buoy_isolated_danger|buoy_lateral|buoy_safe_water|buoy_special_purpose|mooring)$'), mapcss._tag_capture(capture_tags, 1, tags, 'seamark:type'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9002001, 'subclass': 1481035998, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[landuse=conservation]
        if ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'conservation')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"boundary=protected_area"
                # fixAdd:"boundary=protected_area"
                # fixRemove:"landuse"
                err.append({'class': 9002001, 'subclass': 824801072, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['boundary','protected_area']]),
                    '-': ([
                    'landuse'])
                }})

        # *[amenity=kiosk]
        # Rule Blacklisted (id: 1331930630)

        # *[amenity=shop]
        # Rule Blacklisted (id: 1562207150)

        # *[shop=fishmonger]
        # Rule Blacklisted (id: 1376789416)

        # *[shop=fish]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'fish')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=fishing"
                # suggestAlternative:"shop=pet"
                # suggestAlternative:"shop=seafood"
                err.append({'class': 9002001, 'subclass': 47191734, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=betting]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'betting')))
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
                err.append({'class': 9002001, 'subclass': 1035501389, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=perfume]
        # Rule Blacklisted (id: 2075099676)

        # *[amenity=exercise_point]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'exercise_point')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=fitness_station"
                # fixRemove:"amenity"
                # fixAdd:"leisure=fitness_station"
                err.append({'class': 9002001, 'subclass': 1514920202, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['leisure','fitness_station']]),
                    '-': ([
                    'amenity'])
                }})

        # *[shop=auto_parts]
        # Rule Blacklisted (id: 1675828779)

        # *[amenity=car_repair]
        # Rule Blacklisted (id: 1681273585)

        # *[amenity=studio][type=audio]
        # *[amenity=studio][type=radio]
        # *[amenity=studio][type=television]
        # *[amenity=studio][type=video]
        if ('amenity' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'audio')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'radio')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'television')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'studio')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'video')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"studio"
                # fixChangeKey:"type => studio"
                err.append({'class': 9002001, 'subclass': 413401822, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['studio', mapcss.tag(tags, 'type')]]),
                    '-': ([
                    'type'])
                }})

        # *[power=cable_distribution_cabinet]
        # Rule Blacklisted (id: 1007567078)

        # *[power][location=kiosk]
        if ('location' in keys and 'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power')) and (mapcss._tag_capture(capture_tags, 1, tags, 'location') == mapcss._value_capture(capture_tags, 1, 'kiosk')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{1.tag}")
                # fixRemove:"location"
                # fixAdd:"man_made=street_cabinet"
                # fixAdd:"street_cabinet=power"
                err.append({'class': 9002001, 'subclass': 182905067, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['man_made','street_cabinet'],
                    ['street_cabinet','power']]),
                    '-': ([
                    'location'])
                }})

        # *[man_made=well]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'well')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1740864107, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=dog_bin]
        # *[amenity=dog_waste_bin]
        # Rule Blacklisted (id: 2091877281)

        # *[amenity=artwork]
        # Rule Blacklisted (id: 728429076)

        # *[amenity=community_center]
        # Rule Blacklisted (id: 690512681)

        # *[man_made=cut_line]
        # Rule Blacklisted (id: 1008752382)

        # *[amenity=park]
        # Rule Blacklisted (id: 2085280194)

        # *[amenity=hotel]
        # Rule Blacklisted (id: 1341786818)

        # *[shop=window]
        # *[shop=windows]
        # Rule Blacklisted (id: 532391183)

        # *[amenity=education]
        # Rule Blacklisted (id: 796960259)

        # *[shop=gallery]
        # Rule Blacklisted (id: 1319611546)

        # *[shop=gambling]
        # *[leisure=gambling]
        if ('leisure' in keys) or ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'gambling')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'gambling')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=casino"
                # suggestAlternative:"amenity=gambling"
                # suggestAlternative:"leisure=amusement_arcade"
                # suggestAlternative:"shop=bookmaker"
                # suggestAlternative:"shop=lottery"
                err.append({'class': 9002001, 'subclass': 1955724853, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[office=real_estate]
        # *[office=real_estate_agent]
        # Rule Blacklisted (id: 2027311706)

        # *[shop=glass]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'glass')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=glaziery"
                # suggestAlternative:"shop=glaziery"
                err.append({'class': 9002001, 'subclass': 712020531, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=proposed]
        # *[amenity=disused]
        # *[shop=disused]
        # *[highway=abandoned]
        # *[historic=abandoned]
        # Rule Blacklisted (id: 847809313)

        # *[amenity=swimming_pool]
        # Rule Blacklisted (id: 2012807801)

        # *[amenity=sauna]
        # Rule Blacklisted (id: 1450116742)

        # *[/^[^t][^i][^g].+_[0-9]$/][!/^note_[0-9]$/][!/^description_[0-9]$/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_300dfa36)) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_3185ac6d)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_6d27b157)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable key (ending with a number)")
                # throwWarning:tr("{0}","{0.key}")
                err.append({'class': 9002014, 'subclass': 2081989305, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[sport=skating]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'skating')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sport=ice_skating"
                # suggestAlternative:"sport=roller_skating"
                err.append({'class': 9002001, 'subclass': 170699177, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=public_building]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'public_building')))
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
                err.append({'class': 9002001, 'subclass': 1295642010, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[office=administrative]
        # Rule Blacklisted (id: 213844674)

        # *[vending=news_papers]
        if ('vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'news_papers')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=newspapers"
                # fixAdd:"vending=newspapers"
                err.append({'class': 9002001, 'subclass': 1133820292, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['vending','newspapers']])
                }})

        # *[service=drive_through]
        if ('service' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service') == mapcss._value_capture(capture_tags, 0, 'drive_through')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"service=drive-through"
                # fixAdd:"service=drive-through"
                err.append({'class': 9002001, 'subclass': 283545650, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['service','drive-through']])
                }})

        # *[noexit][noexit!=yes][noexit!=no]
        if ('noexit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noexit')) and (mapcss._tag_capture(capture_tags, 1, tags, 'noexit') != mapcss._value_const_capture(capture_tags, 1, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noexit') != mapcss._value_const_capture(capture_tags, 2, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The key {0} has an uncommon value.","{1.key}")
                err.append({'class': 9002017, 'subclass': 1357403556, 'text': mapcss.tr('The key {0} has an uncommon value.', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[name:botanical]
        # Rule Blacklisted (id: 1061429000)

        # *[shop=souvenir]
        # *[shop=souvenirs]
        # *[shop=souveniers]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souvenir')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souvenirs')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'souveniers')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=gift"
                # fixAdd:"shop=gift"
                err.append({'class': 9002001, 'subclass': 1794702946, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','gift']])
                }})

        # *[vending=animal_food]
        if ('vending' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'vending') == mapcss._value_capture(capture_tags, 0, 'animal_food')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"vending=animal_feed"
                # fixAdd:"vending=animal_feed"
                err.append({'class': 9002001, 'subclass': 1077411296, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['vending','animal_feed']])
                }})

        # *[amenity=hunting_stand][lock=yes]
        # *[amenity=hunting_stand][lock=no]
        if ('amenity' in keys and 'lock' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'hunting_stand')) and (mapcss._tag_capture(capture_tags, 1, tags, 'lock') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'hunting_stand')) and (mapcss._tag_capture(capture_tags, 1, tags, 'lock') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{1.key}","{0.tag}")
                # suggestAlternative:"lockable"
                # fixChangeKey:"lock => lockable"
                err.append({'class': 9002001, 'subclass': 1939599742, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['lockable', mapcss.tag(tags, 'lock')]]),
                    '-': ([
                    'lock'])
                }})

        # *[amenity=advertising][!advertising]
        # Rule Blacklisted (id: 1696784412)

        # *[amenity=advertising][advertising]
        # Rule Blacklisted (id: 1538706366)

        # *[building=true]
        # *[building="*"]
        # *[building=Y]
        # *[building=y]
        # *[building=1]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'true')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, '*')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'Y')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'y')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 1)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"building=yes"
                # fixAdd:"building=yes"
                err.append({'class': 9002018, 'subclass': 596818855, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes']])
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
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'abandoned')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'address')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'bing')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'collapsed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'damaged')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'demolished')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'disused')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'fixme')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'occupied')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'razed')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                err.append({'class': 9002001, 'subclass': 938825828, 'text': mapcss.tr('{0} is not a building type.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[building=other]
        # *[building=unclassified]
        # *[building=undefined]
        # *[building=unknown]
        # *[building=unidentified]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'other')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unclassified')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'undefined')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unknown')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'unidentified')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is not a building type.","{0.tag}")
                # fixAdd:"building=yes"
                err.append({'class': 9002001, 'subclass': 48721080, 'text': mapcss.tr('{0} is not a building type.', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes']])
                }})

        # relation[water=salt]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'salt')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"landuse=salt_pond"
                # suggestAlternative:"salt=yes"
                err.append({'class': 9002001, 'subclass': 1845964412, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=toilet]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'toilet')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misspelled value")
                # throwError:tr("{0}","{0.tag}")
                # suggestAlternative:"amenity=toilets"
                # fixAdd:"amenity=toilets"
                err.append({'class': 9002018, 'subclass': 440018606, 'text': mapcss.tr('{0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','toilets']])
                }})

        # *[man_made=MDF]
        # *[man_made=telephone_exchange]
        # Rule Blacklisted (id: 634698090)

        # *[building=central_office]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'central_office')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"telecom=exchange"
                # fixAdd:"building=yes"
                # fixAdd:"telecom=exchange"
                err.append({'class': 9002001, 'subclass': 1091970270, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','yes'],
                    ['telecom','exchange']])
                }})

        # *[telecom=central_office]
        # Rule Blacklisted (id: 1503278830)

        # *[natural=waterfall]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'waterfall')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"waterway=waterfall"
                # fixChangeKey:"natural => waterway"
                err.append({'class': 9002001, 'subclass': 764711734, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['waterway', mapcss.tag(tags, 'natural')]]),
                    '-': ([
                    'natural'])
                }})

        # *[religion=unitarian]
        if ('religion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'religion') == mapcss._value_capture(capture_tags, 0, 'unitarian')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"religion=unitarian_universalist"
                # fixAdd:"religion=unitarian_universalist"
                err.append({'class': 9002001, 'subclass': 9227331, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['religion','unitarian_universalist']])
                }})

        # *[shop=shopping_centre]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'shopping_centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=mall"
                # fixAdd:"shop=mall"
                err.append({'class': 9002001, 'subclass': 1448390566, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','mall']])
                }})

        # *[is_in]
        if ('is_in' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'is_in')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002001, 'subclass': 981454091, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[sport=football]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport') == mapcss._value_capture(capture_tags, 0, 'football')))
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
                err.append({'class': 9002001, 'subclass': 73038577, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[leisure=common]
        if ('leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'common')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"designation=common"
                # suggestAlternative:"landuse=*"
                # suggestAlternative:"leisure=*"
                err.append({'class': 9002001, 'subclass': 157636301, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[cuisine=vegan]
        # *[cuisine=vegetarian]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine') == mapcss._value_capture(capture_tags, 0, 'vegan')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine') == mapcss._value_capture(capture_tags, 0, 'vegetarian')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("diet:","{0.value}","=only")
                # suggestAlternative:concat("diet:","{0.value}","=yes")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                err.append({'class': 9002001, 'subclass': 43604574, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[kitchen_hours]
        if ('kitchen_hours' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kitchen_hours')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"opening_hours:kitchen"
                # fixChangeKey:"kitchen_hours => opening_hours:kitchen"
                err.append({'class': 9002001, 'subclass': 1088306802, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours:kitchen', mapcss.tag(tags, 'kitchen_hours')]]),
                    '-': ([
                    'kitchen_hours'])
                }})

        # *[shop=money_transfer]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'money_transfer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=money_transfer"
                # fixChangeKey:"shop => amenity"
                err.append({'class': 9002001, 'subclass': 1664997936, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity', mapcss.tag(tags, 'shop')]]),
                    '-': ([
                    'shop'])
                }})

        # *[contact:google_plus]
        if ('contact:google_plus' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'contact:google_plus')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # fixRemove:"contact:google_plus"
                err.append({'class': 9002001, 'subclass': 1869461154, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'contact:google_plus'])
                }})

        # *[amenity=garages]
        # *[amenity=garage]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'garages')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'garage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("building=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=parking + parking=garage_boxes"
                # suggestAlternative:"landuse=garages"
                err.append({'class': 9002001, 'subclass': 863228118, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=winery]
        # *[amenity=winery]
        if ('amenity' in keys) or ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'winery')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'winery')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=winery"
                # suggestAlternative:"shop=wine"
                err.append({'class': 9002001, 'subclass': 1773574987, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=youth_centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'youth_centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=community_centre + community_centre=youth_centre"
                # fixAdd:"amenity=community_centre"
                # fixAdd:"community_centre=youth_centre"
                err.append({'class': 9002001, 'subclass': 1284929085, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','community_centre'],
                    ['community_centre','youth_centre']])
                }})

        # *[building:type][building=yes]
        # *[building:type][!building]
        if ('building' in keys and 'building:type' in keys) or ('building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                # fixChangeKey:"building:type => building"
                err.append({'class': 9002001, 'subclass': 1927794430, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building', mapcss.tag(tags, 'building:type')]]),
                    '-': ([
                    'building:type'])
                }})

        # *[building:type][building][building!=yes]
        if ('building' in keys and 'building:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (mapcss._tag_capture(capture_tags, 2, tags, 'building') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"building"
                err.append({'class': 9002001, 'subclass': 1133239698, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[escalator]
        # Rule Blacklisted (id: 967271828)

        # *[fenced]
        # Rule Blacklisted (id: 1141285220)

        # *[historic_name][!old_name]
        # Rule Blacklisted (id: 1034538127)

        # *[historic_name][old_name]
        # Rule Blacklisted (id: 30762614)

        # *[landuse=field]
        # Rule Blacklisted (id: 426261497)

        # *[leisure=beach]
        if ('leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'beach')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"leisure=beach_resort"
                # suggestAlternative:"natural=beach"
                err.append({'class': 9002001, 'subclass': 1767286055, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[leisure=club]
        # Rule Blacklisted (id: 1282397509)

        # *[leisure=video_arcade]
        # Rule Blacklisted (id: 1463909830)

        # *[man_made=jetty]
        # Rule Blacklisted (id: 192707176)

        # *[man_made=village_pump]
        # Rule Blacklisted (id: 423232686)

        # *[man_made=water_tank]
        # Rule Blacklisted (id: 563629665)

        # *[natural=moor]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'moor')))
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
                err.append({'class': 9002001, 'subclass': 374637717, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[noexit=no][!fixme]
        # Rule Blacklisted (id: 647435126)

        # *[noexit=no][fixme]
        # Rule Blacklisted (id: 881828009)

        # *[shop=dive]
        # Rule Blacklisted (id: 1582968978)

        # *[shop=furnace]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'furnace')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"craft=plumber"
                # suggestAlternative:"shop=fireplace"
                err.append({'class': 9002001, 'subclass': 1155821104, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[sport=paragliding]
        # Rule Blacklisted (id: 1531788430)

        # *[tourism=bed_and_breakfast]
        # Rule Blacklisted (id: 954237438)

        # *[diaper=yes]
        # *[diaper=no]
        # Rule Blacklisted (id: 1957125311)

        # *[diaper][diaper=~/^[1-9][0-9]*$/]
        if ('diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0f294fdf), mapcss._tag_capture(capture_tags, 1, tags, 'diaper'))))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper_checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table=yes + changing_table:count=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixAdd:"changing_table=yes"
                # fixChangeKey:"diaper => changing_table:count"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 2105051472, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table','yes'],
                    ['changing_table:count', mapcss.tag(tags, 'diaper')]]),
                    '-': ([
                    'diaper'])
                }})

        # *[diaper=room]
        if ('diaper' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper') == mapcss._value_capture(capture_tags, 0, 'room')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper_checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table=dedicated_room"
                # suggestAlternative:"changing_table=room"
                set_diaper_checked = True
                err.append({'class': 9002001, 'subclass': 883202329, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[diaper]!.diaper_checked
        # Rule Blacklisted (id: 693675339)

        # *[diaper:male=yes]
        if ('diaper:male' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:male') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=male_toilet"
                # fixAdd:"changing_table:location=male_toilet"
                # fixRemove:"diaper:male"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 799035479, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','male_toilet']]),
                    '-': ([
                    'diaper:male'])
                }})

        # *[diaper:female=yes]
        if ('diaper:female' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:female') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=female_toilet"
                # fixAdd:"changing_table:location=female_toilet"
                # fixRemove:"diaper:female"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1450901137, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','female_toilet']]),
                    '-': ([
                    'diaper:female'])
                }})

        # *[diaper:unisex=yes]
        if ('diaper:unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:unisex') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"changing_table:location=unisex_toilet"
                # fixAdd:"changing_table:location=unisex_toilet"
                # fixRemove:"diaper:unisex"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1460378712, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:location','unisex_toilet']]),
                    '-': ([
                    'diaper:unisex'])
                }})

        # *[diaper:wheelchair=yes]
        # *[diaper:wheelchair=no]
        if ('diaper:wheelchair' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:wheelchair') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:wheelchair=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:wheelchair => changing_table:wheelchair"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 1951967281, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:wheelchair', mapcss.tag(tags, 'diaper:wheelchair')]]),
                    '-': ([
                    'diaper:wheelchair'])
                }})

        # *[diaper:fee=yes]
        # *[diaper:fee=no]
        if ('diaper:fee' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:fee') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'diaper:fee') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set diaper___checked
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("changing_table:fee=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"diaper:fee => changing_table:fee"
                set_diaper___checked = True
                err.append({'class': 9002001, 'subclass': 2008573526, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['changing_table:fee', mapcss.tag(tags, 'diaper:fee')]]),
                    '-': ([
                    'diaper:fee'])
                }})

        # *[/^diaper:/]!.diaper___checked
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_diaper___checked) and (mapcss._tag_capture(capture_tags, 0, tags, self.re_6029fe03)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","diaper:*")
                # suggestAlternative:"changing_table:*"
                err.append({'class': 9002001, 'subclass': 26578864, 'text': mapcss.tr('{0} is deprecated', 'diaper:*')})

        # *[changing_table][changing_table!~/^(yes|no|limited)$/]
        if ('changing_table' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'changing_table')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_787405b1, '^(yes|no|limited)$'), mapcss._tag_capture(capture_tags, 1, tags, 'changing_table'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong value: {0}","{0.tag}")
                # suggestAlternative:"changing_table=limited"
                # suggestAlternative:"changing_table=no"
                # suggestAlternative:"changing_table=yes"
                err.append({'class': 9002019, 'subclass': 1965225408, 'text': mapcss.tr('wrong value: {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[roof:shape=half_hipped]
        if ('roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'roof:shape') == mapcss._value_capture(capture_tags, 0, 'half_hipped')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"roof:shape=half-hipped"
                # fixAdd:"roof:shape=half-hipped"
                err.append({'class': 9002001, 'subclass': 1548347123, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['roof:shape','half-hipped']])
                }})

        # *[bridge_name]
        if ('bridge_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge_name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"bridge:name"
                # fixChangeKey:"bridge_name => bridge:name"
                err.append({'class': 9002001, 'subclass': 80069399, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bridge:name', mapcss.tag(tags, 'bridge_name')]]),
                    '-': ([
                    'bridge_name'])
                }})

        # *[access=public]
        # Rule Blacklisted (id: 1115157097)

        # *[crossing=island]
        if ('crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'crossing') == mapcss._value_capture(capture_tags, 0, 'island')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"crossing:island=yes"
                # fixRemove:"crossing"
                # fixAdd:"crossing:island=yes"
                err.append({'class': 9002001, 'subclass': 1512561318, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['crossing:island','yes']]),
                    '-': ([
                    'crossing'])
                }})

        # *[recycling:metal]
        if ('recycling:metal' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'recycling:metal')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"recycling:scrap_metal"
                # fixChangeKey:"recycling:metal => recycling:scrap_metal"
                err.append({'class': 9002001, 'subclass': 474491272, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['recycling:scrap_metal', mapcss.tag(tags, 'recycling:metal')]]),
                    '-': ([
                    'recycling:metal'])
                }})

        # *[shop=dog_grooming]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'dog_grooming')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=pet_grooming"
                # fixAdd:"shop=pet_grooming"
                err.append({'class': 9002001, 'subclass': 1073412885, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','pet_grooming']])
                }})

        # *[tower:type=anchor]
        # *[tower:type=suspension]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'anchor')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'suspension')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # suggestAlternative:concat("line_attachment=","{0.value}")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # fixChangeKey:"tower:type => line_attachment"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 180380605, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_attachment', mapcss.tag(tags, 'tower:type')]]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=branch][branch:type=split]
        # *[tower:type=branch][branch:type=loop]
        if ('branch:type' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'split')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'loop')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=split"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=split"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 362350862, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','split']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=branch][!branch:type]
        # *[tower:type=branch][branch:type=tap]
        if ('branch:type' in keys and 'tower:type' in keys) or ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'branch:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'tap')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=branch"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=branch"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 476423517, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','branch']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=branch][branch:type=cross]
        if ('branch:type' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'branch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'branch:type') == mapcss._value_capture(capture_tags, 1, 'cross')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=cross"
                # fixRemove:"branch:type"
                # fixAdd:"line_management=cross"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 2103059531, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','cross']]),
                    '-': ([
                    'branch:type',
                    'tower:type'])
                }})

        # *[tower:type=termination]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'termination')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=termination"
                # fixAdd:"line_management=termination"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 232235847, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','termination']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=transition]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'transition')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"location:transition=yes"
                # fixAdd:"location:transition=yes"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1124904944, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['location:transition','yes']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=transposing]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'transposing')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"line_management=transpose"
                # fixAdd:"line_management=transpose"
                # fixRemove:"tower:type"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1795169098, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['line_management','transpose']]),
                    '-': ([
                    'tower:type'])
                }})

        # *[tower:type=crossing]
        if ('tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tower:type') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # set power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"height=* + design=*"
                set_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 1301565974, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[tower:type][power][power=~/^(tower|pole|insulator|portal|terminal)$/]!.power_tower_type_warning
        if ('power' in keys and 'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_power_tower_type_warning) and (mapcss._tag_capture(capture_tags, 0, tags, 'tower:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_24dfeb95), mapcss._tag_capture(capture_tags, 2, tags, 'power'))))
                except mapcss.RuleAbort: pass
            if match:
                # set generic_power_tower_type_warning
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"design"
                # suggestAlternative:"line_attachment"
                # suggestAlternative:"line_management"
                # suggestAlternative:"structure"
                set_generic_power_tower_type_warning = True
                err.append({'class': 9002001, 'subclass': 2020421267, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[pole:type][power][power=~/^(tower|pole|insulator|portal|terminal)$/]!.power_pole_type_warning!.generic_power_tower_type_warning
        if ('pole:type' in keys and 'power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_power_pole_type_warning) and (not set_generic_power_tower_type_warning) and (mapcss._tag_capture(capture_tags, 0, tags, 'pole:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_24dfeb95), mapcss._tag_capture(capture_tags, 2, tags, 'power'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated for {1}","{0.key}","{1.tag}")
                # suggestAlternative:"line_attachment"
                # suggestAlternative:"line_management"
                err.append({'class': 9002001, 'subclass': 1513543887, 'text': mapcss.tr('{0} is deprecated for {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[sloped_curb=yes][!kerb]
        # *[sloped_curb=both][!kerb]
        if ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'yes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'both')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=lowered"
                # fixAdd:"kerb=lowered"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 1906002413, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['kerb','lowered']]),
                    '-': ([
                    'sloped_curb'])
                }})

        # *[sloped_curb=no][!kerb]
        if ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb') == mapcss._value_capture(capture_tags, 0, 'no')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"kerb=yes"
                # fixAdd:"kerb=yes"
                # fixRemove:"sloped_curb"
                err.append({'class': 9002001, 'subclass': 893727015, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['kerb','yes']]),
                    '-': ([
                    'sloped_curb'])
                }})

        # *[sloped_curb][sloped_curb!~/^(yes|both|no)$/][!kerb]
        # *[sloped_curb][kerb]
        if ('kerb' in keys and 'sloped_curb' in keys) or ('sloped_curb' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_01eb1711, '^(yes|both|no)$'), mapcss._tag_capture(capture_tags, 1, tags, 'sloped_curb'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sloped_curb')) and (mapcss._tag_capture(capture_tags, 1, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"kerb=*"
                err.append({'class': 9002001, 'subclass': 1682376745, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[unnamed=yes]
        if ('unnamed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'unnamed') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"noname=yes"
                # fixChangeKey:"unnamed => noname"
                err.append({'class': 9002001, 'subclass': 1901447020, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['noname', mapcss.tag(tags, 'unnamed')]]),
                    '-': ([
                    'unnamed'])
                }})

        # *[building:height]
        if ('building:height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:height')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"height"
                # fixChangeKey:"building:height => height"
                err.append({'class': 9002001, 'subclass': 1328174745, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['height', mapcss.tag(tags, 'building:height')]]),
                    '-': ([
                    'building:height'])
                }})

        # *[building:min_height]
        if ('building:min_height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:min_height')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"min_height"
                # fixChangeKey:"building:min_height => min_height"
                err.append({'class': 9002001, 'subclass': 1042683921, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['min_height', mapcss.tag(tags, 'building:min_height')]]),
                    '-': ([
                    'building:min_height'])
                }})

        # *[car][amenity=charging_station]
        # Rule Blacklisted (id: 1165117414)

        # *[navigationaid=approach_light]
        # *[navigationaid="ALS (Approach lighting system)"]
        if ('navigationaid' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'navigationaid') == mapcss._value_capture(capture_tags, 0, 'approach_light')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'navigationaid') == mapcss._value_capture(capture_tags, 0, 'ALS (Approach lighting system)')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"navigationaid=als"
                # fixAdd:"navigationaid=als"
                err.append({'class': 9002001, 'subclass': 1577817081, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['navigationaid','als']])
                }})

        # *[water=riverbank][!natural]
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                err.append({'class': 9002001, 'subclass': 186872153, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','water'],
                    ['water','river']])
                }})

        # *[water=riverbank][natural]
        if ('natural' in keys and 'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 630806094, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[waterway=riverbank][!natural][!water]
        # *[waterway=riverbank][natural=water][!water]
        # *[waterway=riverbank][!natural][water=river]
        # *[waterway=riverbank][natural=water][water=river]
        if ('natural' in keys and 'water' in keys and 'waterway' in keys) or ('natural' in keys and 'waterway' in keys) or ('water' in keys and 'waterway' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'river')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') == mapcss._value_capture(capture_tags, 2, 'river')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                # fixAdd:"natural=water"
                # fixAdd:"water=river"
                # fixRemove:"waterway"
                err.append({'class': 9002001, 'subclass': 1604946271, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','water'],
                    ['water','river']]),
                    '-': ([
                    'waterway'])
                }})

        # *[waterway=riverbank][natural][natural!=water]
        # *[waterway=riverbank][water][water!=river]
        if ('natural' in keys and 'waterway' in keys) or ('water' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (mapcss._tag_capture(capture_tags, 2, tags, 'natural') != mapcss._value_const_capture(capture_tags, 2, 'water', 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')) and (mapcss._tag_capture(capture_tags, 1, tags, 'water')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'river', 'river')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=water + water=river"
                err.append({'class': 9002001, 'subclass': 301661430, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[shop=lamps]
        if ('shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop') == mapcss._value_capture(capture_tags, 0, 'lamps')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"shop=lighting"
                # fixAdd:"shop=lighting"
                err.append({'class': 9002001, 'subclass': 746886011, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['shop','lighting']])
                }})

        # *[access=customer]
        if ('access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access') == mapcss._value_capture(capture_tags, 0, 'customer')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"access=customers"
                # fixAdd:"access=customers"
                err.append({'class': 9002001, 'subclass': 1040065637, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['access','customers']])
                }})

        # *[addr:inclusion=estimated]
        if ('addr:inclusion' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:inclusion') == mapcss._value_capture(capture_tags, 0, 'estimated')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"addr:inclusion=estimate"
                # fixAdd:"addr:inclusion=estimate"
                err.append({'class': 9002001, 'subclass': 1002643753, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['addr:inclusion','estimate']])
                }})

        # *[building=apartment]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'apartment')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"building=apartments"
                # fixAdd:"building=apartments"
                err.append({'class': 9002001, 'subclass': 1384168519, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['building','apartments']])
                }})

        # *[generator:type=solar_photovoltaic_panels]
        if ('generator:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:type') == mapcss._value_capture(capture_tags, 0, 'solar_photovoltaic_panels')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"generator:type=solar_photovoltaic_panel"
                # fixAdd:"generator:type=solar_photovoltaic_panel"
                err.append({'class': 9002001, 'subclass': 1146719875, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['generator:type','solar_photovoltaic_panel']])
                }})

        # *[building=part]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'part')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"building:part=yes"
                err.append({'class': 9002001, 'subclass': 455695847, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[natural=sink_hole]
        if ('natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'sink_hole')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"natural=sinkhole"
                # fixAdd:"natural=sinkhole"
                err.append({'class': 9002001, 'subclass': 1283355945, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['natural','sinkhole']])
                }})

        # *[climbing:grade:UIAA:min]
        if ('climbing:grade:UIAA:min' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:min')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:min"
                # fixChangeKey:"climbing:grade:UIAA:min => climbing:grade:uiaa:min"
                err.append({'class': 9002001, 'subclass': 1408052420, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:min', mapcss.tag(tags, 'climbing:grade:UIAA:min')]]),
                    '-': ([
                    'climbing:grade:UIAA:min'])
                }})

        # *[climbing:grade:UIAA:max]
        if ('climbing:grade:UIAA:max' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:max')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:max"
                # fixChangeKey:"climbing:grade:UIAA:max => climbing:grade:uiaa:max"
                err.append({'class': 9002001, 'subclass': 1866245426, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:max', mapcss.tag(tags, 'climbing:grade:UIAA:max')]]),
                    '-': ([
                    'climbing:grade:UIAA:max'])
                }})

        # *[climbing:grade:UIAA:mean]
        if ('climbing:grade:UIAA:mean' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA:mean')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa:mean"
                # fixChangeKey:"climbing:grade:UIAA:mean => climbing:grade:uiaa:mean"
                err.append({'class': 9002001, 'subclass': 1022648087, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa:mean', mapcss.tag(tags, 'climbing:grade:UIAA:mean')]]),
                    '-': ([
                    'climbing:grade:UIAA:mean'])
                }})

        # *[climbing:grade:UIAA]
        if ('climbing:grade:UIAA' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'climbing:grade:UIAA')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"climbing:grade:uiaa"
                # fixChangeKey:"climbing:grade:UIAA => climbing:grade:uiaa"
                err.append({'class': 9002001, 'subclass': 1007893519, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['climbing:grade:uiaa', mapcss.tag(tags, 'climbing:grade:UIAA')]]),
                    '-': ([
                    'climbing:grade:UIAA'])
                }})

        # *[cuisine][cuisine=~/^(?i)(bbq)$/]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cuisine')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2f881233), mapcss._tag_capture(capture_tags, 1, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # set bbq_autofix
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"cuisine=barbecue"
                # fixAdd:"cuisine=barbecue"
                set_bbq_autofix = True
                err.append({'class': 9002001, 'subclass': 1943338875, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['cuisine','barbecue']])
                }})

        # *[cuisine=~/(?i)(;bbq|bbq;)/][cuisine!~/(?i)(_bbq)/]
        if ('cuisine' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_340a2b31), mapcss._tag_capture(capture_tags, 0, tags, 'cuisine'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_7d409ed5, '(?i)(_bbq)'), mapcss._tag_capture(capture_tags, 1, tags, 'cuisine'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","cuisine=bbq")
                # suggestAlternative:"cuisine=barbecue"
                err.append({'class': 9002001, 'subclass': 1958782130, 'text': mapcss.tr('{0} is deprecated', 'cuisine=bbq')})

        # *[Fixme]
        if ('Fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'Fixme')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"fixme"
                # fixChangeKey:"Fixme => fixme"
                err.append({'class': 9002001, 'subclass': 592643943, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['fixme', mapcss.tag(tags, 'Fixme')]]),
                    '-': ([
                    'Fixme'])
                }})

        # *[amenity=embassy]
        # Rule Blacklisted (id: 1751915206)

        # *[service:bicycle:chaintool]
        if ('service:bicycle:chaintool' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'service:bicycle:chaintool')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"service:bicycle:chain_tool"
                # fixChangeKey:"service:bicycle:chaintool => service:bicycle:chain_tool"
                err.append({'class': 9002001, 'subclass': 1464143873, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['service:bicycle:chain_tool', mapcss.tag(tags, 'service:bicycle:chaintool')]]),
                    '-': ([
                    'service:bicycle:chaintool'])
                }})

        # *[building:roof:shape]
        if ('building:roof:shape' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:roof:shape')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"roof:shape"
                # fixChangeKey:"building:roof:shape => roof:shape"
                err.append({'class': 9002001, 'subclass': 2106920042, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['roof:shape', mapcss.tag(tags, 'building:roof:shape')]]),
                    '-': ([
                    'building:roof:shape'])
                }})

        # *[man_made=pumping_rig][!pump_mechanism][!mechanical_driver][!mechanical_coupling]
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pumping_rig')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'pump_mechanism')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mechanical_coupling')))
                except mapcss.RuleAbort: pass
            if match:
                # set pumping_ring_no_mech
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                # fixAdd:"mechanical_coupling=nodding_donkey"
                # fixAdd:"mechanical_driver=combustion_engine"
                # fixAdd:"pump_mechanism=piston"
                set_pumping_ring_no_mech = True
                err.append({'class': 9002001, 'subclass': 6568074, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mechanical_coupling','nodding_donkey'],
                    ['mechanical_driver','combustion_engine'],
                    ['pump_mechanism','piston']])
                }})

        # *[man_made=pumping_rig]!.pumping_ring_no_mech
        if ('man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_pumping_ring_no_mech) and (mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pumping_rig')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"man_made=petroleum_well"
                # suggestAlternative:"man_made=water_well"
                err.append({'class': 9002001, 'subclass': 1031026578, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[pump:type=beam_pump][!pump_mechanism][!mechanical_driver][!mechanical_coupling]
        if ('pump:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pump:type') == mapcss._value_capture(capture_tags, 0, 'beam_pump')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'pump_mechanism')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'mechanical_coupling')))
                except mapcss.RuleAbort: pass
            if match:
                # set beam_pump_no_mech
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"pump_mechanism"
                # fixAdd:"mechanical_coupling=nodding_donkey"
                # fixAdd:"mechanical_driver=combustion_engine"
                # fixRemove:"pump:type"
                # fixAdd:"pump_mechanism=piston"
                set_beam_pump_no_mech = True
                err.append({'class': 9002001, 'subclass': 1519103279, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['mechanical_coupling','nodding_donkey'],
                    ['mechanical_driver','combustion_engine'],
                    ['pump_mechanism','piston']]),
                    '-': ([
                    'pump:type'])
                }})

        # *[pump:type]!.beam_pump_no_mech
        if ('pump:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_beam_pump_no_mech) and (mapcss._tag_capture(capture_tags, 0, tags, 'pump:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"pump_mechanism"
                err.append({'class': 9002001, 'subclass': 2015679777, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[substance=heat]
        if ('substance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'substance') == mapcss._value_capture(capture_tags, 0, 'heat')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"substance=hot_water"
                # suggestAlternative:"substance=steam"
                err.append({'class': 9002001, 'subclass': 1528467304, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[landuse=school]
        if ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'school')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"amenity=college"
                # suggestAlternative:"amenity=school"
                # suggestAlternative:"amenity=university"
                # suggestAlternative:"landuse=education"
                err.append({'class': 9002001, 'subclass': 817812278, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[surface=decoturf]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface') == mapcss._value_capture(capture_tags, 0, 'decoturf')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"surface=acrylic"
                # fixAdd:"surface=acrylic"
                err.append({'class': 9002001, 'subclass': 1995300591, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['surface','acrylic']])
                }})

        # *[role]
        # Rule Blacklisted (id: 2041296832)

        # *[school=entrance]
        if ('school' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'school') == mapcss._value_capture(capture_tags, 0, 'entrance')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"entrance=main"
                # suggestAlternative:"entrance=yes"
                err.append({'class': 9002001, 'subclass': 1398581809, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[voltage-high]
        # *[voltage-low]
        if ('voltage-high' in keys) or ('voltage-low' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage-high')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage-low')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"voltage:primary"
                # suggestAlternative:"voltage:secondary"
                err.append({'class': 9002001, 'subclass': 1379077827, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[toilet][!toilets]
        if ('toilet' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toilet')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'toilets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"toilets"
                # fixChangeKey:"toilet => toilets"
                err.append({'class': 9002001, 'subclass': 466700565, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['toilets', mapcss.tag(tags, 'toilet')]]),
                    '-': ([
                    'toilet'])
                }})

        # *[toilet][toilets]
        if ('toilet' in keys and 'toilets' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toilet')) and (mapcss._tag_capture(capture_tags, 1, tags, 'toilets')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.key}")
                # suggestAlternative:"toilets"
                err.append({'class': 9002001, 'subclass': 1092230744, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[type="turnlanes:turns"]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'turnlanes:turns')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"type=connectivity"
                err.append({'class': 9002001, 'subclass': 1789083769, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[image][image=~/^https:\/\/westnordost.de\/p\//]
        if ('image' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'image')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_0fbae48f), mapcss._tag_capture(capture_tags, 1, tags, 'image'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} with a temporary URL which may be outdated very soon","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9002023, 'subclass': 2042174729, 'text': mapcss.tr('{0} with a temporary URL which may be outdated very soon', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        # *[historic=archaeological_site][site_type]
        if ('historic' in keys and 'site_type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'historic') == mapcss._value_capture(capture_tags, 0, 'archaeological_site')) and (mapcss._tag_capture(capture_tags, 1, tags, 'site_type')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} should be replaced with {1}","{1.key}","archaeological_site")
                # fixChangeKey:"site_type => archaeological_site"
                err.append({'class': 9002008, 'subclass': 595008939, 'text': mapcss.tr('{0} should be replaced with {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), 'archaeological_site'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['archaeological_site', mapcss.tag(tags, 'site_type')]]),
                    '-': ([
                    'site_type'])
                }})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_deprecated(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'name': 'FIXME'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_err(n.node(data, {'name': 'Fixme'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_err(n.node(data, {'name': 'fixme'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_not_err(n.node(data, {'name': 'valid name'}), expected={'class': 9002005, 'subclass': 642340557})
        self.check_err(n.node(data, {'f': 'b'}), expected={'class': 9002012, 'subclass': 79709106})
        self.check_err(n.node(data, {'fo': 'bar'}), expected={'class': 9002012, 'subclass': 79709106})
        self.check_not_err(n.node(data, {'kp': '5'}), expected={'class': 9002012, 'subclass': 79709106})
        self.check_not_err(n.node(data, {'pk': '7'}), expected={'class': 9002012, 'subclass': 79709106})
        self.check_not_err(n.node(data, {'emergency_telephone_code': '456', 'highway': 'emergency_access_point'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_not_err(n.node(data, {'emergency_telephone_code': '456', 'highway': 'emergency_access_point', 'phone': '123'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_err(n.node(data, {'highway': 'emergency_access_point', 'phone': '123'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_not_err(n.node(data, {'phone': '123'}), expected={'class': 9002001, 'subclass': 1339208019})
        self.check_not_err(n.node(data, {'emergency_telephone_code': '123', 'highway': 'emergency_access_point'}), expected={'class': 9002001, 'subclass': 342466099})
        self.check_err(n.node(data, {'emergency_telephone_code': '123', 'highway': 'emergency_access_point', 'phone': '123'}), expected={'class': 9002001, 'subclass': 342466099})
        self.check_not_err(n.node(data, {'highway': 'emergency_access_point', 'phone': '123'}), expected={'class': 9002001, 'subclass': 342466099})
        self.check_not_err(n.node(data, {'emergency_telephone_code': '123', 'highway': 'emergency_access_point'}), expected={'class': 9002001, 'subclass': 663070970})
        self.check_not_err(n.node(data, {'emergency_telephone_code': '123', 'highway': 'emergency_access_point', 'phone': '123'}), expected={'class': 9002001, 'subclass': 663070970})
        self.check_not_err(n.node(data, {'highway': 'emergency_access_point', 'phone': '123'}), expected={'class': 9002001, 'subclass': 663070970})
        self.check_not_err(n.node(data, {'image': 'https://commons.wikimedia.org/wiki/File:2015-05-13_Basteibr%C3%BCcke-.jpg'}), expected={'class': 9002023, 'subclass': 2042174729})
        self.check_not_err(n.node(data, {'image': 'https://web.archive.org/web/20220623215400/https://westnordost.de/p/97331.jpg'}), expected={'class': 9002023, 'subclass': 2042174729})
        self.check_err(n.node(data, {'image': 'https://westnordost.de/p/17484.jpg'}), expected={'class': 9002023, 'subclass': 2042174729})
        self.check_not_err(n.node(data, {'historic': 'archaeological_site', 'site_type2': 'fortification'}), expected={'class': 9002008, 'subclass': 595008939})
        self.check_err(n.node(data, {'historic': 'archaeological_site', 'site_type': 'fortification'}), expected={'class': 9002008, 'subclass': 595008939})
        self.check_not_err(n.way(data, {'barrier': 'fence'}, [0]), expected={'class': 9002001, 'subclass': 1107799632})
        self.check_err(n.way(data, {'barrier': 'wire_fence'}, [0]), expected={'class': 9002001, 'subclass': 1107799632})
        self.check_err(n.way(data, {'access': 'designated'}, [0]), expected={'class': 9002002, 'subclass': 2057594338})
        self.check_err(n.way(data, {'access': 'official'}, [0]), expected={'class': 9002003, 'subclass': 1909133836})
        self.check_err(n.way(data, {'fixme': 'yes'}, [0]), expected={'class': 9002004, 'subclass': 136657482})
        self.check_not_err(n.way(data, {'color': 'red'}, [0]), expected={'class': 9002001, 'subclass': 1632389707})
        self.check_err(n.way(data, {'cycleway:surface:color': 'grey'}, [0]), expected={'class': 9002001, 'subclass': 1632389707})
        self.check_not_err(n.way(data, {'roof:color': 'grey'}, [0]), expected={'class': 9002001, 'subclass': 1632389707})
        self.check_err(n.way(data, {'color:back': 'grey'}, [0]), expected={'class': 9002001, 'subclass': 1390370717})
        self.check_not_err(n.way(data, {'color': 'red'}, [0]), expected={'class': 9002001, 'subclass': 1390370717})
        self.check_not_err(n.way(data, {'route': 'ferry', 'to': 'Zuidschermer;Akersloot'}, [0]), expected={'class': 9002012, 'subclass': 1765060211})
        self.check_err(n.way(data, {'to': 'bar'}, [0]), expected={'class': 9002012, 'subclass': 1765060211})
        self.check_not_err(n.way(data, {'description_3': 'foo'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_err(n.way(data, {'name_1': 'foo'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_not_err(n.way(data, {'note_2': 'foo'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_not_err(n.way(data, {'tiger:name_base_1': 'bar'}, [0]), expected={'class': 9002014, 'subclass': 2081989305})
        self.check_not_err(n.way(data, {'building': 'supermarket', 'building:type': 'church'}, [0]), expected={'class': 9002001, 'subclass': 1927794430})
        self.check_err(n.way(data, {'building': 'yes', 'building:type': 'church'}, [0]), expected={'class': 9002001, 'subclass': 1927794430})
        self.check_err(n.way(data, {'building:type': 'church'}, [0]), expected={'class': 9002001, 'subclass': 1927794430})
        self.check_err(n.way(data, {'building': 'supermarket', 'building:type': 'church'}, [0]), expected={'class': 9002001, 'subclass': 1133239698})
        self.check_not_err(n.way(data, {'building': 'yes', 'building:type': 'church'}, [0]), expected={'class': 9002001, 'subclass': 1133239698})
        self.check_not_err(n.way(data, {'building:type': 'church'}, [0]), expected={'class': 9002001, 'subclass': 1133239698})
        self.check_not_err(n.way(data, {'natural': 'shingle', 'water': 'river', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_not_err(n.way(data, {'natural': 'shingle', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_not_err(n.way(data, {'natural': 'water', 'water': 'lake', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_err(n.way(data, {'natural': 'water', 'water': 'river', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_err(n.way(data, {'natural': 'water', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_not_err(n.way(data, {'water': 'lake', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_err(n.way(data, {'water': 'river', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_err(n.way(data, {'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 1604946271})
        self.check_err(n.way(data, {'natural': 'shingle', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 301661430})
        self.check_not_err(n.way(data, {'natural': 'water', 'water': 'river', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 301661430})
        self.check_not_err(n.way(data, {'natural': 'water', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 301661430})
        self.check_err(n.way(data, {'water': 'lake', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 301661430})
        self.check_not_err(n.way(data, {'water': 'river', 'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 301661430})
        self.check_not_err(n.way(data, {'waterway': 'riverbank'}, [0]), expected={'class': 9002001, 'subclass': 301661430})
        self.check_err(n.way(data, {'cuisine': 'BBQ'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_err(n.way(data, {'cuisine': 'bbq'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_not_err(n.way(data, {'cuisine': 'bbq;pizza'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_not_err(n.way(data, {'cuisine': 'korean_bbq'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_not_err(n.way(data, {'cuisine': 'korean_bbq;bbq'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_not_err(n.way(data, {'cuisine': 'pasta;bbq;pizza'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_not_err(n.way(data, {'cuisine': 'pizza;Bbq'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_not_err(n.way(data, {'cuisine': 'pizza;bbq'}, [0]), expected={'class': 9002001, 'subclass': 1943338875})
        self.check_not_err(n.way(data, {'cuisine': 'BBQ'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_not_err(n.way(data, {'cuisine': 'bbq'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_err(n.way(data, {'cuisine': 'bbq;pizza'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_not_err(n.way(data, {'cuisine': 'korean_bbq'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_not_err(n.way(data, {'cuisine': 'korean_bbq;bbq'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_err(n.way(data, {'cuisine': 'pasta;bbq;pizza'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_err(n.way(data, {'cuisine': 'pizza;Bbq'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_err(n.way(data, {'cuisine': 'pizza;bbq'}, [0]), expected={'class': 9002001, 'subclass': 1958782130})
        self.check_not_err(n.way(data, {'FIXME': 'foo'}, [0]), expected={'class': 9002001, 'subclass': 592643943})
        self.check_err(n.way(data, {'Fixme': 'foo'}, [0]), expected={'class': 9002001, 'subclass': 592643943})
        self.check_not_err(n.way(data, {'fixme': 'foo'}, [0]), expected={'class': 9002001, 'subclass': 592643943})
        self.check_err(n.relation(data, {'fo': 'bar'}, []), expected={'class': 9002012, 'subclass': 518970721})
        self.check_not_err(n.relation(data, {'to': 'Berlin'}, []), expected={'class': 9002012, 'subclass': 518970721})
