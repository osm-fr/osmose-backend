#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_highway(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/highway.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9004001] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('abbreviated street name'))
        self.errors[9004002] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('wrong crossing tag on a way'))
        self.errors[9004004] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('Unspecific highway type'))
        self.errors[9004006] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('deprecated tagging'))
        self.errors[9004008] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('wrong highway tag on a node'))
        self.errors[9004009] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('missing tag'))
        self.errors[9004010] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('{0} on a node', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9004011] = self.def_class(item = 9004, level = 2, tags = ["tag", "highway"], title = mapcss.tr('suspicious tag combination'))
        self.errors[9004012] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('questionable value (ending with a number)'))
        self.errors[9004013] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[9004014] = self.def_class(item = 9004, level = 3, tags = ["tag", "highway"], title = mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}')))

        self.re_015aabd5 = re.compile(r'^(unclassified|residential|living_street|service)$')
        self.re_23c50386 = re.compile(r'^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$')
        self.re_3092b7ac = re.compile(r'^.*_link$')
        self.re_33052a50 = re.compile(r'^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$')
        self.re_4186cb68 = re.compile(r'(?i).* (Ave|Blvd|Bnd|Br|Brg|Cct|Cir|Cl|Cr|Crct|Cres|Crt|Ct|Cv|Dr|Drv|Esp|Espl|Hwy|Ln|Mw|Mwy|Pky|Pkwy|Pl|Rd|Qy|Qys|Sq|St|Str|Ter|Tce|Tr|Trl|Vw|Wy|Xing)[.]?$')
        self.re_447f4d65 = re.compile(r'motorway|trunk|primary|secondary|tertiary|unclassified|residential|service|living_street|pedestrian|track|path|footway|cycleway|busway|bus_guideway|bridleway')
        self.re_4dcdb354 = re.compile(r'^footway:')
        self.re_55b03910 = re.compile(r'^paving_stones:(\d+)$')
        self.re_55ee32ac = re.compile(r'^(motorway|trunk|primary|secondary|tertiary)$')
        self.re_5757d731 = re.compile(r'^((motorway|trunk|primary|secondary|tertiary)(_link)?|residential|unclassified)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_fixable_footway = set_link_road = set_major_road = set_minor_road = set_not_fixable_footway = False

        # node[highway=~/motorway|trunk|primary|secondary|tertiary|unclassified|residential|service|living_street|pedestrian|track|path|footway|cycleway|busway|bus_guideway|bridleway/][highway!=motorway_junction][highway!=services]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_447f4d65), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway') != mapcss._value_const_capture(capture_tags, 1, 'motorway_junction', 'motorway_junction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'services', 'services')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong highway tag on a node")
                # assertNoMatch:"node highway=bus_stop"
                # assertNoMatch:"node highway=crossing"
                # assertNoMatch:"node highway=emergency_access_point"
                # assertNoMatch:"node highway=give_way"
                # assertNoMatch:"node highway=mini_roundabout"
                # assertNoMatch:"node highway=motorway_junction"
                # assertNoMatch:"node highway=passing_place"
                # assertMatch:"node highway=primary"
                # assertMatch:"node highway=primary_link"
                # assertNoMatch:"node highway=rest_area"
                # assertNoMatch:"node highway=services"
                # assertNoMatch:"node highway=speed_camera"
                # assertNoMatch:"node highway=stop"
                # assertNoMatch:"node highway=street_lamp"
                # assertNoMatch:"node highway=traffic_calming"
                # assertNoMatch:"node highway=traffic_signals"
                # assertNoMatch:"node highway=turning_circle"
                err.append({'class': 9004008, 'subclass': 224371448, 'text': mapcss.tr('wrong highway tag on a node')})

        # node[footway=crossing]
        if ('footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node","{0.tag}")
                # suggestAlternative:"highway=crossing"
                # suggestAlternative:"railway=crossing"
                err.append({'class': 9004010, 'subclass': 1262520638, 'text': mapcss.tr('{0} on a node', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[cycleway=crossing]
        if ('cycleway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node","{0.tag}")
                # suggestAlternative:"highway=crossing + bicycle=yes"
                # suggestAlternative:"railway=crossing + bicycle=yes"
                err.append({'class': 9004010, 'subclass': 1385847744, 'text': mapcss.tr('{0} on a node', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[railway!=crossing][crossing!=no].is_in_railway.is_in_minor_road!.is_in_major_road
        if True:
            match = False
            # Skip selector using undeclared class is_in_major_road, is_in_minor_road, is_in_railway
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("pedestrian railway crossing without {0}","{0.tag}")
                # fixAdd:"railway=crossing"
                err.append({'class': 9004009, 'subclass': 18813378, 'text': mapcss.tr('pedestrian railway crossing without {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway','crossing']])
                }})

        # node[railway!=level_crossing].is_in_railway.is_in_major_road!.is_in_minor_road
        if True:
            match = False
            # Skip selector using undeclared class is_in_major_road, is_in_minor_road, is_in_railway
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("railway crossing without {0}","{0.tag}")
                # fixAdd:"railway=level_crossing"
                err.append({'class': 9004009, 'subclass': 1127761651, 'text': mapcss.tr('railway crossing without {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['railway','level_crossing']])
                }})

        # node[highway=crossing][barrier=kerb].is_in_major_road
        if ('barrier' in keys and 'highway' in keys):
            match = False
            # Skip selector using undeclared class is_in_major_road
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"kerb=*"
                err.append({'class': 9004011, 'subclass': 440952770, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[surface=~/^paving_stones:(\d+)$/]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55b03910), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable value (ending with a number)")
                # throwWarning:tr("{0} with trailing number","paving_stones")
                # suggestAlternative:"paving_stones:length"
                # suggestAlternative:"paving_stones:width"
                err.append({'class': 9004012, 'subclass': 291757414, 'text': mapcss.tr('{0} with trailing number', 'paving_stones')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_fixable_footway = set_link_road = set_major_road = set_minor_road = set_not_fixable_footway = False

        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # set major_road
                set_major_road = True

        # way[highway=~/^.*_link$/]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3092b7ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # set link_road
                set_link_road = True

        # way[highway=~/^(unclassified|residential|living_street|service)$/]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_015aabd5), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # set minor_road
                set_minor_road = True

        # way[highway][name=~/(?i).* (Ave|Blvd|Bnd|Br|Brg|Cct|Cir|Cl|Cr|Crct|Cres|Crt|Ct|Cv|Dr|Drv|Esp|Espl|Hwy|Ln|Mw|Mwy|Pky|Pkwy|Pl|Rd|Qy|Qys|Sq|St|Str|Ter|Tce|Tr|Trl|Vw|Wy|Xing)[.]?$/]
        if ('highway' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4186cb68), mapcss._tag_capture(capture_tags, 1, tags, 'name'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("abbreviated street name")
                # assertMatch:"way highway=unclassified name=\"Bou Blvd.\""
                # assertMatch:"way highway=unclassified name=\"Bou blvd.\""
                # assertMatch:"way highway=unclassified name=\"Foo Ave\""
                # assertMatch:"way highway=unclassified name=\"Foo Ave.\""
                err.append({'class': 9004001, 'subclass': 1120623403, 'text': mapcss.tr('abbreviated street name')})

        # way[highway=crossing]
        # way[railway=crossing]
        # way[railway=level_crossing]
        if ('highway' in keys) or ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'crossing')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'level_crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong crossing tag on a way")
                # assertMatch:"way highway=crossing"
                err.append({'class': 9004002, 'subclass': 1549110307, 'text': mapcss.tr('wrong crossing tag on a way')})

        # way[highway=yes]
        # way[highway=road]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'road')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unspecific highway type")
                # assertNoMatch:"way highway=residential"
                # assertMatch:"way highway=road"
                err.append({'class': 9004004, 'subclass': 1729022478, 'text': mapcss.tr('Unspecific highway type')})

        # way[highway=footway][maxspeed]
        # way[highway=steps][maxspeed]
        # way[highway=cycleway][bicycle=no]
        # way[highway=footway][foot=no]
        # way[highway=cycleway][cycleway=lane]
        if ('bicycle' in keys and 'highway' in keys) or ('cycleway' in keys and 'highway' in keys) or ('foot' in keys and 'highway' in keys) or ('highway' in keys and 'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'steps')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bicycle') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'foot') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway') == mapcss._value_capture(capture_tags, 1, 'lane')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way highway=cycleway bicycle=yes"
                # assertMatch:"way highway=cycleway cycleway=lane"
                # assertNoMatch:"way highway=cycleway"
                # assertNoMatch:"way highway=cycleway"
                # assertNoMatch:"way highway=footway foot=yes"
                # assertMatch:"way highway=footway maxspeed=20"
                # assertNoMatch:"way highway=footway"
                # assertNoMatch:"way highway=footway"
                # assertNoMatch:"way highway=residential cycleway=lane"
                # assertNoMatch:"way highway=residential maxspeed=20"
                err.append({'class': 9004013, 'subclass': 469607562, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[footway=left][/^footway:/]
        # way[footway=right][/^footway:/]
        # way[footway=both][/^footway:/]
        # way[footway=separate][/^footway:/]
        # way[footway=no][/^footway:/]
        if ('footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'left')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'right')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'both')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'separate')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'no')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354)))
                except mapcss.RuleAbort: pass
            if match:
                # set not_fixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated, use {1} instead. Also check similar tags like {2}","{0.tag}","sidewalk","{1.key}")
                # assertMatch:"way footway=both footway:surface=asphalt"
                # assertMatch:"way footway=separate footway:surface=asphalt"
                set_not_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 1255595246, 'text': mapcss.tr('{0} is deprecated, use {1} instead. Also check similar tags like {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'sidewalk', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[footway=none][/^footway:/]
        if ('footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'none')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354)))
                except mapcss.RuleAbort: pass
            if match:
                # set not_fixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated, use {1} instead. Also check similar tags like {2}","{0.tag}","sidewalk=no","{1.key}")
                # assertNoMatch:"way footway=no footway:surface=asphalt"
                # assertMatch:"way footway=none footway:surface=asphalt"
                set_not_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 2016837729, 'text': mapcss.tr('{0} is deprecated, use {1} instead. Also check similar tags like {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'sidewalk=no', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[footway=left]!.not_fixable_footway
        # way[footway=right]!.not_fixable_footway
        # way[footway=both]!.not_fixable_footway
        # way[footway=separate]!.not_fixable_footway
        # way[footway=no]!.not_fixable_footway
        if ('footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_not_fixable_footway) and (mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'left')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_not_fixable_footway) and (mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'right')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_not_fixable_footway) and (mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'both')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_not_fixable_footway) and (mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'separate')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_not_fixable_footway) and (mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # set fixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sidewalk"
                # fixChangeKey:"footway => sidewalk"
                set_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 1136570919, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['sidewalk', mapcss.tag(tags, 'footway')]]),
                    '-': ([
                    'footway'])
                }})

        # way[footway=none]!.not_fixable_footway
        if ('footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_not_fixable_footway) and (mapcss._tag_capture(capture_tags, 0, tags, 'footway') == mapcss._value_capture(capture_tags, 0, 'none')))
                except mapcss.RuleAbort: pass
            if match:
                # set fixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sidewalk=no"
                # fixRemove:"footway"
                # fixAdd:"sidewalk=no"
                set_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 430589555, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['sidewalk','no']]),
                    '-': ([
                    'footway'])
                }})

        # way[turn][turn!~/^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$/]
        # way[turn:forward][turn:forward!~/^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$/]
        # way[turn:backward][turn:backward!~/^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$/]
        # way[turn:both_ways][turn:both_ways!~/^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$/]
        # way[turn:both_ways:forward][turn:both_ways:forward!~/^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$/]
        # way[turn:both_ways:backward][turn:both_ways:backward!~/^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$/]
        # way[turn:lanes][turn:lanes!~/^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$/]
        # way[turn:lanes:forward][turn:lanes:forward!~/^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$/]
        # way[turn:lanes:backward][turn:lanes:backward!~/^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$/]
        # way[turn:lanes:both_ways][turn:lanes:both_ways!~/^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$/]
        # way[turn:lanes:both_ways:forward][turn:lanes:both_ways:forward!~/^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$/]
        # way[turn:lanes:both_ways:backward][turn:lanes:both_ways:backward!~/^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$/]
        if ('turn' in keys) or ('turn:backward' in keys) or ('turn:both_ways' in keys) or ('turn:both_ways:backward' in keys) or ('turn:both_ways:forward' in keys) or ('turn:forward' in keys) or ('turn:lanes' in keys) or ('turn:lanes:backward' in keys) or ('turn:lanes:both_ways' in keys) or ('turn:lanes:both_ways:backward' in keys) or ('turn:lanes:both_ways:forward' in keys) or ('turn:lanes:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_33052a50, '^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:forward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_33052a50, '^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:forward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:backward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_33052a50, '^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:backward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:both_ways')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_33052a50, '^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:both_ways'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:both_ways:forward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_33052a50, '^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:both_ways:forward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:both_ways:backward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_33052a50, '^(none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:both_ways:backward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:lanes')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23c50386, '^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:lanes'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:lanes:forward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23c50386, '^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:lanes:forward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:lanes:backward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23c50386, '^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:lanes:backward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:lanes:both_ways')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23c50386, '^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:lanes:both_ways'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:lanes:both_ways:forward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23c50386, '^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:lanes:both_ways:forward'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'turn:lanes:both_ways:backward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23c50386, '^(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*)(\|(|none|((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through)(;((sharp_|slight_|merge_to_|slide_)?(left|right)|reverse|through))*))*$'), mapcss._tag_capture(capture_tags, 1, tags, 'turn:lanes:both_ways:backward'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("unusual value of {0}","{0.key}")
                # assertNoMatch:"way turn:lanes:forward=sharp_left;left||left;through;slight_right|slight_right;right|"
                # assertMatch:"way turn:lanes:forward=slight_reverse|right"
                # assertMatch:"way turn:lanes:forward=straight|right"
                # assertMatch:"way turn:lanes=left;none|right"
                # assertMatch:"way turn=slight_reverse"
                # assertMatch:"way turn=straight"
                # assertNoMatch:"way turn=through;right"
                # assertMatch:"way turn=through|right"
                err.append({'class': 9004014, 'subclass': 1634496690, 'text': mapcss.tr('unusual value of {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[highway=~/^((motorway|trunk|primary|secondary|tertiary)(_link)?|residential|unclassified)$/][area=yes]
        if ('area' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5757d731), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'area') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwError:tr("Area with {0} above {1} is invalid","highway=*","highway=service")
                # suggestAlternative:"area:highway=*"
                # assertNoMatch:"way highway=service area=yes"
                # assertMatch:"way highway=trunk area=yes"
                # assertNoMatch:"way highway=trunk"
                err.append({'class': 9004011, 'subclass': 610375152, 'text': mapcss.tr('Area with {0} above {1} is invalid', 'highway=*', 'highway=service')})

        # *[surface=~/^paving_stones:(\d+)$/]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55b03910), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable value (ending with a number)")
                # throwWarning:tr("{0} with trailing number","paving_stones")
                # suggestAlternative:"paving_stones:length"
                # suggestAlternative:"paving_stones:width"
                err.append({'class': 9004012, 'subclass': 291757414, 'text': mapcss.tr('{0} with trailing number', 'paving_stones')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_fixable_footway = set_link_road = set_major_road = set_minor_road = set_not_fixable_footway = False

        # relation[highway=~/^((motorway|trunk|primary|secondary|tertiary)(_link)?|residential|unclassified)$/][type=multipolygon]
        if ('highway' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5757d731), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') == mapcss._value_capture(capture_tags, 1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwError:tr("Area with {0} above {1} is invalid","highway=*","highway=service")
                # suggestAlternative:"area:highway=*"
                # assertMatch:"relation highway=trunk type=multipolygon"
                err.append({'class': 9004011, 'subclass': 2126629809, 'text': mapcss.tr('Area with {0} above {1} is invalid', 'highway=*', 'highway=service')})

        # *[surface=~/^paving_stones:(\d+)$/]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55b03910), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("questionable value (ending with a number)")
                # throwWarning:tr("{0} with trailing number","paving_stones")
                # suggestAlternative:"paving_stones:length"
                # suggestAlternative:"paving_stones:width"
                err.append({'class': 9004012, 'subclass': 291757414, 'text': mapcss.tr('{0} with trailing number', 'paving_stones')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_highway(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {'highway': 'bus_stop'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'crossing'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'emergency_access_point'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'give_way'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'mini_roundabout'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'motorway_junction'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'passing_place'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.node(data, {'highway': 'primary'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.node(data, {'highway': 'primary_link'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'rest_area'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'services'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'speed_camera'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'stop'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'street_lamp'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'traffic_calming'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'traffic_signals'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.node(data, {'highway': 'turning_circle'}), expected={'class': 9004008, 'subclass': 224371448}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'highway': 'unclassified', 'name': 'Bou Blvd.'}, [0]), expected={'class': 9004001, 'subclass': 1120623403}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'highway': 'unclassified', 'name': 'Bou blvd.'}, [0]), expected={'class': 9004001, 'subclass': 1120623403}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'highway': 'unclassified', 'name': 'Foo Ave'}, [0]), expected={'class': 9004001, 'subclass': 1120623403}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'highway': 'unclassified', 'name': 'Foo Ave.'}, [0]), expected={'class': 9004001, 'subclass': 1120623403}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'highway': 'crossing'}, [0]), expected={'class': 9004002, 'subclass': 1549110307}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'highway': 'residential'}, [0]), expected={'class': 9004004, 'subclass': 1729022478}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'highway': 'road'}, [0]), expected={'class': 9004004, 'subclass': 1729022478}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'bicycle': 'yes', 'highway': 'cycleway'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'cycleway': 'lane', 'highway': 'cycleway'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'highway': 'cycleway'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'highway': 'cycleway'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'foot': 'yes', 'highway': 'footway'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'highway': 'footway', 'maxspeed': '20'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'highway': 'footway'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'highway': 'footway'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'cycleway': 'lane', 'highway': 'residential'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'highway': 'residential', 'maxspeed': '20'}, [0]), expected={'class': 9004013, 'subclass': 469607562}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'footway': 'both', 'footway:surface': 'asphalt'}, [0]), expected={'class': 9004006, 'subclass': 1255595246}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'footway': 'separate', 'footway:surface': 'asphalt'}, [0]), expected={'class': 9004006, 'subclass': 1255595246}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'footway': 'no', 'footway:surface': 'asphalt'}, [0]), expected={'class': 9004006, 'subclass': 2016837729}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'footway': 'none', 'footway:surface': 'asphalt'}, [0]), expected={'class': 9004006, 'subclass': 2016837729}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'turn:lanes:forward': 'sharp_left;left||left;through;slight_right|slight_right;right|'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'turn:lanes:forward': 'slight_reverse|right'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'turn:lanes:forward': 'straight|right'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'turn:lanes': 'left;none|right'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'turn': 'slight_reverse'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'turn': 'straight'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'turn': 'through;right'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'turn': 'through|right'}, [0]), expected={'class': 9004014, 'subclass': 1634496690}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'area': 'yes', 'highway': 'service'}, [0]), expected={'class': 9004011, 'subclass': 610375152}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.way(data, {'area': 'yes', 'highway': 'trunk'}, [0]), expected={'class': 9004011, 'subclass': 610375152}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.way(data, {'highway': 'trunk'}, [0]), expected={'class': 9004011, 'subclass': 610375152}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.relation(data, {'highway': 'trunk', 'type': 'multipolygon'}, []), expected={'class': 9004011, 'subclass': 2126629809}, disallowed_str_in_text = ['{', '}'])
