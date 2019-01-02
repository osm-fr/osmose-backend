#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_highway(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9004001] = {'item': 9004, 'level': 3, 'tag': ["tag", "highway"], 'desc': mapcss.tr(u'abbreviated street name')}
        self.errors[9004002] = {'item': 9004, 'level': 3, 'tag': ["tag", "highway"], 'desc': mapcss.tr(u'wrong crossing tag on a way')}
        self.errors[9004004] = {'item': 9004, 'level': 3, 'tag': ["tag", "highway"], 'desc': mapcss.tr(u'Unspecific highway type')}
        self.errors[9004005] = {'item': 9004, 'level': 3, 'tag': ["tag", "highway"], 'desc': mapcss.tr(u'{0} used with {1}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))}
        self.errors[9004006] = {'item': 9004, 'level': 3, 'tag': ["tag", "highway"], 'desc': mapcss.tr(u'deprecated tagging')}
        self.errors[9004007] = {'item': 9004, 'level': 3, 'tag': ["tag", "highway"], 'desc': mapcss.tr(u'Value of \'\'{0}\'\' should either be \'\'{1}\'\' or \'\'{2}\'\'. For sidewalks use \'\'{3}\'\' instead.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'), u'sidewalk=left|right|both|no')}
        self.errors[9004008] = {'item': 9004, 'level': 3, 'tag': ["tag", "highway"], 'desc': mapcss.tr(u'wrong highway tag on a node')}

        self.re_015aabd5 = re.compile(ur'^(unclassified|residential|living_street|service)$')
        self.re_3092b7ac = re.compile(ur'^.*_link$')
        self.re_3dc5dd7c = re.compile(ur'motorway|trunk|primary|secondary|tertiary|unclassified|residential|service|living_street|pedestrian|track|path|footway|cycleway|bus_guideway|bridleway')
        self.re_4dcdb354 = re.compile(ur'^footway:')
        self.re_55ee32ac = re.compile(ur'^(motorway|trunk|primary|secondary|tertiary)$')
        self.re_61bbe299 = re.compile(ur'footway:')
        self.re_776f2c1a = re.compile(ur'(?i).* (Ave|Blvd|Br|Brg|Cct|Cir|Cl|Cr|Crct|Cres|Crt|Ct|Dr|Drv|Esp|Espl|Hwy|Ln|Mw|Mwy|Pky|Pkwy|Pl|Rd|Qy|Qys|Sq|St|Str|Ter|Tce|Tr|Wy)[.]?$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_fixable_footway = set_link_road = set_major_road = set_minor_road = set_not_fixable_footway = False

        # node[highway=~/motorway|trunk|primary|secondary|tertiary|unclassified|residential|service|living_street|pedestrian|track|path|footway|cycleway|bus_guideway|bridleway/][highway!=motorway_junction][highway!=services]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3dc5dd7c), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'highway') != mapcss._value_capture(capture_tags, 1, u'motorway_junction') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'services'))
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
                err.append({'class': 9004008, 'subclass': 325492196, 'text': mapcss.tr(u'wrong highway tag on a node')})

        # node[railway!=crossing][crossing!=no].is_in_railway.is_in_minor_road!.is_in_major_road
        # Use undeclared class is_in_major_road, is_in_minor_road, is_in_railway

        # node[railway!=level_crossing].is_in_railway.is_in_major_road!.is_in_minor_road
        # Use undeclared class is_in_major_road, is_in_minor_road, is_in_railway

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_fixable_footway = set_link_road = set_major_road = set_minor_road = set_not_fixable_footway = False

        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # setmajor_road
                set_major_road = True

        # way[highway=~/^.*_link$/]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3092b7ac), mapcss._tag_capture(capture_tags, 0, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # setlink_road
                set_link_road = True

        # way[highway=~/^(unclassified|residential|living_street|service)$/]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_015aabd5), mapcss._tag_capture(capture_tags, 0, tags, u'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # setminor_road
                set_minor_road = True

        # way[highway][name=~/(?i).* (Ave|Blvd|Br|Brg|Cct|Cir|Cl|Cr|Crct|Cres|Crt|Ct|Dr|Drv|Esp|Espl|Hwy|Ln|Mw|Mwy|Pky|Pkwy|Pl|Rd|Qy|Qys|Sq|St|Str|Ter|Tce|Tr|Wy)[.]?$/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_776f2c1a), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("abbreviated street name")
                # assertMatch:"way highway=unclassified name=\"Bou Blvd.\""
                # assertMatch:"way highway=unclassified name=\"Bou blvd.\""
                # assertMatch:"way highway=unclassified name=\"Foo Ave\""
                # assertMatch:"way highway=unclassified name=\"Foo Ave.\""
                err.append({'class': 9004001, 'subclass': 544432044, 'text': mapcss.tr(u'abbreviated street name')})

        # way[highway=crossing]
        # way[railway=crossing]
        # way[railway=level_crossing]
        if (u'highway' in keys) or (u'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'crossing'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'crossing'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'level_crossing'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wrong crossing tag on a way")
                # assertMatch:"way highway=crossing"
                err.append({'class': 9004002, 'subclass': 1549110307, 'text': mapcss.tr(u'wrong crossing tag on a way')})

        # way[highway=yes]
        # way[highway=road]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'road'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unspecific highway type")
                # assertNoMatch:"way highway=residential"
                # assertMatch:"way highway=road"
                err.append({'class': 9004004, 'subclass': 1729022478, 'text': mapcss.tr(u'Unspecific highway type')})

        # way[highway=footway][maxspeed]
        # way[highway=steps][maxspeed]
        # way[highway=cycleway][bicycle=no]
        # way[highway=footway][foot=no]
        # way[highway=cycleway][cycleway=lane]
        if (u'bicycle' in keys and u'highway' in keys) or (u'cycleway' in keys and u'highway' in keys) or (u'foot' in keys and u'highway' in keys) or (u'highway' in keys and u'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'footway') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'steps') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'bicycle') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'footway') and mapcss._tag_capture(capture_tags, 1, tags, u'foot') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway') == mapcss._value_capture(capture_tags, 1, u'lane'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} used with {1}","{0.value}","{1.tag}")
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
                err.append({'class': 9004005, 'subclass': 469607562, 'text': mapcss.tr(u'{0} used with {1}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[footway=left][/^footway:/]
        # way[footway=right][/^footway:/]
        # way[footway=both][/^footway:/]
        # way[footway=no][/^footway:/]
        if (u'footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'left') and mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'right') and mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'both') and mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'no') and mapcss._tag_capture(capture_tags, 1, tags, self.re_4dcdb354))
                except mapcss.RuleAbort: pass
            if match:
                # setnot_fixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated, use {1} instead. Also check similar tags like {2}","{0.tag}","sidewalk","{1.key}")
                # assertMatch:"way footway=both footway:surface=asphalt"
                set_not_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 141262069, 'text': mapcss.tr(u'{0} is deprecated, use {1} instead. Also check similar tags like {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'sidewalk', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[footway=none][/footway:/]
        if (u'footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'none') and mapcss._tag_capture(capture_tags, 1, tags, self.re_61bbe299))
                except mapcss.RuleAbort: pass
            if match:
                # setnot_fixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated, use {1} instead. Also check similar tags like {2}","{0.tag}","sidewalk=no","{1.key}")
                set_not_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 1570348899, 'text': mapcss.tr(u'{0} is deprecated, use {1} instead. Also check similar tags like {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), u'sidewalk=no', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[footway=left]!.not_fixable_footway
        # way[footway=right]!.not_fixable_footway
        # way[footway=both]!.not_fixable_footway
        # way[footway=no]!.not_fixable_footway
        if (u'footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_not_fixable_footway and mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (not set_not_fixable_footway and mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (not set_not_fixable_footway and mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'both'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (not set_not_fixable_footway and mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # setfixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sidewalk"
                # fixChangeKey:"footway => sidewalk"
                set_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 2076937761, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sidewalk', mapcss.tag(tags, u'footway')]]),
                    '-': ([
                    u'footway'])
                }})

        # way[footway=none]!.not_fixable_footway
        if (u'footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_not_fixable_footway and mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'none'))
                except mapcss.RuleAbort: pass
            if match:
                # setfixable_footway
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"sidewalk=no"
                # fixRemove:"footway"
                # fixAdd:"sidewalk=no"
                set_fixable_footway = True
                err.append({'class': 9004006, 'subclass': 430589555, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'sidewalk',u'no']]),
                    '-': ([
                    u'footway'])
                }})

        # way[footway][footway!=sidewalk][footway!=crossing]!.fixable_footway!.not_fixable_footway
        if (u'footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_fixable_footway and not set_not_fixable_footway and mapcss._tag_capture(capture_tags, 0, tags, u'footway') and mapcss._tag_capture(capture_tags, 1, tags, u'footway') != mapcss._value_capture(capture_tags, 1, u'sidewalk') and mapcss._tag_capture(capture_tags, 2, tags, u'footway') != mapcss._value_capture(capture_tags, 2, u'crossing'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Value of ''{0}'' should either be ''{1}'' or ''{2}''. For sidewalks use ''{3}'' instead.","{0.key}","{1.value}","{2.value}","sidewalk=left|right|both|no")
                # assertMatch:"way footway=bar"
                # assertNoMatch:"way footway=left footway:left:surface=asphalt"
                # assertNoMatch:"way footway=left"
                # assertNoMatch:"way footway=none"
                err.append({'class': 9004007, 'subclass': 156640320, 'text': mapcss.tr(u'Value of \'\'{0}\'\' should either be \'\'{1}\'\' or \'\'{2}\'\'. For sidewalks use \'\'{3}\'\' instead.', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'), u'sidewalk=left|right|both|no')})

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

        self.check_not_err(n.node(data, {u'highway': u'bus_stop'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'crossing'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'emergency_access_point'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'give_way'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'mini_roundabout'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'motorway_junction'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'passing_place'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_err(n.node(data, {u'highway': u'primary'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_err(n.node(data, {u'highway': u'primary_link'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'rest_area'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'services'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'speed_camera'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'stop'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'street_lamp'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'traffic_calming'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'traffic_signals'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_not_err(n.node(data, {u'highway': u'turning_circle'}), expected={'class': 9004008, 'subclass': 325492196})
        self.check_err(n.way(data, {u'highway': u'unclassified', u'name': u'Bou Blvd.'}, [0]), expected={'class': 9004001, 'subclass': 544432044})
        self.check_err(n.way(data, {u'highway': u'unclassified', u'name': u'Bou blvd.'}, [0]), expected={'class': 9004001, 'subclass': 544432044})
        self.check_err(n.way(data, {u'highway': u'unclassified', u'name': u'Foo Ave'}, [0]), expected={'class': 9004001, 'subclass': 544432044})
        self.check_err(n.way(data, {u'highway': u'unclassified', u'name': u'Foo Ave.'}, [0]), expected={'class': 9004001, 'subclass': 544432044})
        self.check_err(n.way(data, {u'highway': u'crossing'}, [0]), expected={'class': 9004002, 'subclass': 1549110307})
        self.check_not_err(n.way(data, {u'highway': u'residential'}, [0]), expected={'class': 9004004, 'subclass': 1729022478})
        self.check_err(n.way(data, {u'highway': u'road'}, [0]), expected={'class': 9004004, 'subclass': 1729022478})
        self.check_not_err(n.way(data, {u'bicycle': u'yes', u'highway': u'cycleway'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_err(n.way(data, {u'cycleway': u'lane', u'highway': u'cycleway'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_not_err(n.way(data, {u'highway': u'cycleway'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_not_err(n.way(data, {u'highway': u'cycleway'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_not_err(n.way(data, {u'foot': u'yes', u'highway': u'footway'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_err(n.way(data, {u'highway': u'footway', u'maxspeed': u'20'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_not_err(n.way(data, {u'highway': u'footway'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_not_err(n.way(data, {u'highway': u'footway'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_not_err(n.way(data, {u'cycleway': u'lane', u'highway': u'residential'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_not_err(n.way(data, {u'highway': u'residential', u'maxspeed': u'20'}, [0]), expected={'class': 9004005, 'subclass': 469607562})
        self.check_err(n.way(data, {u'footway': u'both', u'footway:surface': u'asphalt'}, [0]), expected={'class': 9004006, 'subclass': 141262069})
        self.check_err(n.way(data, {u'footway': u'bar'}, [0]), expected={'class': 9004007, 'subclass': 156640320})
        self.check_not_err(n.way(data, {u'footway': u'left', u'footway:left:surface': u'asphalt'}, [0]), expected={'class': 9004007, 'subclass': 156640320})
        self.check_not_err(n.way(data, {u'footway': u'left'}, [0]), expected={'class': 9004007, 'subclass': 156640320})
        self.check_not_err(n.way(data, {u'footway': u'none'}, [0]), expected={'class': 9004007, 'subclass': 156640320})
