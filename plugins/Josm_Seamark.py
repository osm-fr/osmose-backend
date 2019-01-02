#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_Seamark(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9012001] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'Multi-colour {0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))}
        self.errors[9012002] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'Unrecognized {0}: {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))}
        self.errors[9012003] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'{0} have no IALA or system defind ({1})', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9012004] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'Probably wrong category on {0}, {1} colour mean {2} in {3}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'), mapcss._tag_uncapture(capture_tags, u'{3.value}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'))}
        self.errors[9012005] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'Probably wrong category on {0}, the colour combination {1} usually mean {2}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))}
        self.errors[9012006] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'{0} have no {1}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9012007] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'{0} set without {1}={2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'))}
        self.errors[9012008] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9012009] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'In {0} {1}={2} require {3}={4}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'))}
        self.errors[9012010] = {'item': 9012, 'level': 3, 'tag': ["tag", "seamark"], 'desc': mapcss.tr(u'{0} sign require {1} set to left or right', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}

        self.re_01dd9715 = re.compile(ur'right|left')
        self.re_09200db5 = re.compile(ur'keep_to_port_margin|keep_to_starboard_margin|keep_to_mid|cross_river_to_port|cross_river_to_starboard|reduce_speed')
        self.re_09c0bae9 = re.compile(ur'opening_to_right|opening_to_left')
        self.re_0b7ab6fc = re.compile(ur'keep_to_port_margin|keep_to_starboard_margin|keep_to_mid-river|cross_river_to_port|cross_river_to_starboard')
        self.re_0e114cad = re.compile(ur'bniwr2|ppwbc')
        self.re_0e3e01fc = re.compile(ur'no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes')
        self.re_1389a933 = re.compile(ur'move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact')
        self.re_141d4d2f = re.compile(ur'horizontal|vertical|diagonal|squared|stripes|border|cross|saltire')
        self.re_253b0e7a = re.compile(ur'channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right')
        self.re_281803e9 = re.compile(ur'preferred_channel_starboard|turnoff_right')
        self.re_288a42ac = re.compile(ur'port|waterway_right|channel_right')
        self.re_2a269778 = re.compile(ur'main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right')
        self.re_2e10f0c7 = re.compile(ur'entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted')
        self.re_32e3abb7 = re.compile(ur'starboard|waterway_left|channel_left')
        self.re_336a6c28 = re.compile(ur'limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right')
        self.re_39084725 = re.compile(ur'limited_headroom')
        self.re_430e795b = re.compile(ur'main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|traffic_between_margins')
        self.re_61629c48 = re.compile(ur'preferred_channel_starboard|preferred_channel_port|waterway_separation|channel_separation')
        self.re_637abe26 = re.compile(ur'preferred_channel_port|turnoff_left')
        self.re_7c5430c7 = re.compile(ur'no_anchoring')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:color"*=";"][!"seamark:buoy_lateral:colour_pattern"]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:color"*=";"][!"seamark:beacon_lateral:colour_pattern"]
        # node["seamark:type"=buoy_cardinal]["seamark:buoy_cardinal:color"*=";"][!"seamark:buoy_cardinal:colour_pattern"]
        # node["seamark:type"=beacon_cardinal]["seamark:beacon_cardinal:color"*=";"][!"seamark:beacon_cardinal:colour_pattern"]
        # node["seamark:type"=buoy_isolated_danger]["seamark:buoy_isolated_danger:color"*=";"][!"seamark:buoy_isolated_danger:colour_pattern"]
        # node["seamark:type"=beacon_isolated_danger]["seamark:beacon_isolated_danger:color"*=";"][!"seamark:beacon_isolated_danger:colour_pattern"]
        # node["seamark:type"=buoy_safe_water]["seamark:buoy_safe_water:color"*=";"][!"seamark:buoy_safe_water:colour_pattern"]
        # node["seamark:type"=beacon_special_purpose]["seamark:beacon_special_purpose:color"*=";"][!"seamark:beacon_special_purpose:colour_pattern"]
        if (u'seamark:beacon_cardinal:color' in keys and u'seamark:type' in keys) or (u'seamark:buoy_cardinal:color' in keys and u'seamark:type' in keys) or (u'seamark:buoy_safe_water:color' in keys and u'seamark:type' in keys) or (u'seamark:beacon_isolated_danger:color' in keys and u'seamark:type' in keys) or (u'seamark:beacon_lateral:color' in keys and u'seamark:type' in keys) or (u'seamark:beacon_special_purpose:color' in keys and u'seamark:type' in keys) or (u'seamark:buoy_isolated_danger:color' in keys and u'seamark:type' in keys) or (u'seamark:buoy_lateral:color' in keys and u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour_pattern'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour_pattern'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_cardinal') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_cardinal:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_cardinal:colour_pattern'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_cardinal') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_cardinal:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_cardinal:colour_pattern'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_isolated_danger') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_isolated_danger:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_isolated_danger:colour_pattern'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_isolated_danger') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_isolated_danger:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_isolated_danger:colour_pattern'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_safe_water') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_safe_water:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_safe_water:colour_pattern'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_special_purpose') and mapcss.string_contains(mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_special_purpose:color'), mapcss._value_capture(capture_tags, 1, u';')) and not mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_special_purpose:colour_pattern'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Multi-colour {0} without {1}","{0.value}","{2.key}")
                err.append({'class': 9012001, 'subclass': 349882546, 'text': mapcss.tr(u'Multi-colour {0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # node["seamark:buoy_lateral:colour_pattern"]["seamark:buoy_lateral:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:beacon_lateral:colour_pattern"]["seamark:beacon_lateral:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:buoy_cardinal:colour_pattern"]["seamark:buoy_cardinal:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:beacon_cardinal:colour_pattern"]["seamark:beacon_cardinal:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:buoy_isolated_danger:colour_pattern"]["seamark:buoy_isolated_danger:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:beacon_isolated_danger:colour_pattern"]["seamark:beacon_isolated_danger:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:buoy_installation:colour_pattern"]["seamark:buoy_installation:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:buoy_safe_water:colour_pattern"]["seamark:buoy_safe_water:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:beacon_safe_water:colour_pattern"]["seamark:beacon_safe_water:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:buoy_special_purpose:colour_pattern"]["seamark:buoy_special_purpose:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:beacon_special_purpose:colour_pattern"]["seamark:beacon_special_purpose:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:topmark:colour_pattern"]["seamark:topmark:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:daymark:colour_pattern"]["seamark:daymark:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:bridge:colour_pattern"]["seamark:bridge:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:building:colour_pattern"]["seamark:building:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:landmark:colour_pattern"]["seamark:landmark:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:light_float:colour_pattern"]["seamark:light_float:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:light_vessel:colour_pattern"]["seamark:light_vessel:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:notice:colour_pattern"]["seamark:notice:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:pile:colour_pattern"]["seamark:pile:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:platform:colour_pattern"]["seamark:platform:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        # node["seamark:mooring:colour_pattern"]["seamark:mooring:colour_pattern"!~/horizontal|vertical|diagonal|squared|stripes|border|cross|saltire/]
        if (u'seamark:beacon_cardinal:colour_pattern' in keys) or (u'seamark:beacon_isolated_danger:colour_pattern' in keys) or (u'seamark:beacon_lateral:colour_pattern' in keys) or (u'seamark:beacon_safe_water:colour_pattern' in keys) or (u'seamark:beacon_special_purpose:colour_pattern' in keys) or (u'seamark:bridge:colour_pattern' in keys) or (u'seamark:building:colour_pattern' in keys) or (u'seamark:buoy_cardinal:colour_pattern' in keys) or (u'seamark:buoy_installation:colour_pattern' in keys) or (u'seamark:buoy_isolated_danger:colour_pattern' in keys) or (u'seamark:buoy_lateral:colour_pattern' in keys) or (u'seamark:buoy_safe_water:colour_pattern' in keys) or (u'seamark:buoy_special_purpose:colour_pattern' in keys) or (u'seamark:daymark:colour_pattern' in keys) or (u'seamark:landmark:colour_pattern' in keys) or (u'seamark:light_float:colour_pattern' in keys) or (u'seamark:light_vessel:colour_pattern' in keys) or (u'seamark:mooring:colour_pattern' in keys) or (u'seamark:notice:colour_pattern' in keys) or (u'seamark:pile:colour_pattern' in keys) or (u'seamark:platform:colour_pattern' in keys) or (u'seamark:topmark:colour_pattern' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:buoy_lateral:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:beacon_lateral:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:buoy_cardinal:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_cardinal:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:beacon_cardinal:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_cardinal:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:buoy_isolated_danger:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_isolated_danger:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:beacon_isolated_danger:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_isolated_danger:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:buoy_installation:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_installation:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:buoy_safe_water:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_safe_water:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:beacon_safe_water:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_safe_water:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:buoy_special_purpose:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_special_purpose:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:beacon_special_purpose:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_special_purpose:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:topmark:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:topmark:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:daymark:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:daymark:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:bridge:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:bridge:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:building:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:building:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:landmark:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:landmark:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:light_float:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:light_float:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:light_vessel:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:light_vessel:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:pile:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:pile:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:platform:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:platform:colour_pattern')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:mooring:colour_pattern') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_141d4d2f), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:mooring:colour_pattern')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Unrecognized {0}: {1}","{0.key}","{0.value}")
                err.append({'class': 9012002, 'subclass': 2001970681, 'text': mapcss.tr(u'Unrecognized {0}: {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # node["seamark:type"=buoy_lateral][!"seamark:buoy_lateral:system"]
        # node["seamark:type"=beacon_lateral][!"seamark:beacon_lateral:system"]
        if (u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} have no IALA or system defind ({1})","{0.value}","{1.key}")
                err.append({'class': 9012003, 'subclass': 1924932803, 'text': mapcss.tr(u'{0} have no IALA or system defind ({1})', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-a]["seamark:buoy_lateral:colour"=red]["seamark:buoy_lateral:category"!=port]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-a]["seamark:beacon_lateral:colour"=red]["seamark:beacon_lateral:category"!=port]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-a]["seamark:buoy_lateral:colour"=green]["seamark:buoy_lateral:category"!=starboard]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-a]["seamark:buoy_lateral:colour"=green]["seamark:beacon_lateral:category"!=starboard]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-a]["seamark:buoy_lateral:colour"="green;red;green"]["seamark:buoy_lateral:category"!=preferred_channel_port]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-a]["seamark:beacon_lateral:colour"="green;red;green"]["seamark:beacon_lateral:category"!=preferred_channel_port]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-b]["seamark:buoy_lateral:colour"="green;red;green"]["seamark:buoy_lateral:category"!=preferred_channel_starboard]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-b]["seamark:beacon_lateral:colour"="green;red;green"]["seamark:beacon_lateral:category"!=preferred_channel_starbord]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-b]["seamark:buoy_lateral:colour"="red;green;red"]["seamark:buoy_lateral:category"!=preferred_channel_port]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-b]["seamark:beacon_lateral:colour"="red;green;red"]["seamark:beacon_lateral:category"!=preferred_channel_port]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-a]["seamark:buoy_lateral:colour"="red;green;red"]["seamark:buoy_lateral:category"!=preferred_channel_starboard]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-a]["seamark:beacon_lateral:colour"="red;green;red"]["seamark:beacon_lateral:category"!=preferred_channel_starboard]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-b]["seamark:buoy_lateral:colour"=green]["seamark:buoy_lateral:category"!=port]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-b]["seamark:beacon_lateral:colour"=green]["seamark:beacon_lateral:category"!=port]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=iala-b]["seamark:buoy_lateral:colour"=red]["seamark:buoy_lateral:category"!=starboard]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=iala-b]["seamark:buoy_lateral:colour"=red]["seamark:beacon_lateral:category"!=starboard]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"=green]["seamark:buoy_lateral:category"!~/starboard|waterway_left|channel_left/]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"=red]["seamark:buoy_lateral:category"!~/port|waterway_right|channel_right/]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="red;green;red;green"]["seamark:buoy_lateral:category"!~/preferred_channel_starboard|preferred_channel_port|waterway_separation|channel_separation/]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="red;green;red"]["seamark:buoy_lateral:category"!~/preferred_channel_starboard|turnoff_right/]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="green;red;green"]["seamark:buoy_lateral:category"!~/preferred_channel_port|turnoff_left/]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="red;white;red;white"]["seamark:buoy_lateral:category"!=danger_right]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="green;white;green;white"]["seamark:buoy_lateral:category"!=danger_left]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="white;red"]["seamark:buoy_lateral:category"!=turnoff_right]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="white;green"]["seamark:buoy_lateral:category"!=turnoff_left]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="red;white;red"]["seamark:buoy_lateral:category"!=junction_right]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="green;white;green"]["seamark:buoy_lateral:category"!=junction_left]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="red;white"]["seamark:buoy_lateral:category"!=harbour_right]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"="green;white"]["seamark:buoy_lateral:category"!=harbour_left]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"=yellow]["seamark:buoy_lateral:category"!=harbour_right]["seamark:topmark:colour"=red]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"=yellow]["seamark:buoy_lateral:category"!=harbour_left]["seamark:topmark:colour"=green]
        # node["seamark:type"=buoy_lateral]["seamark:buoy_lateral:system"=cevni]["seamark:buoy_lateral:colour"=yellow]["seamark:buoy_lateral:category"!=bridge_pier][!"seamark:topmark:colour"]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"=green]["seamark:beacon_lateral:category"!~/starboard|waterway_left|channel_left/]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"=red]["seamark:beacon_lateral:category"!~/port|waterway_right|channel_right/]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="red;green;red;green"]["seamark:beacon_lateral:category"!~/preferred_channel_starboard|preferred_channel_port|waterway_separation|channel_separation/]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="red;green;red"]["seamark:beacon_lateral:category"!~/preferred_channel_starboard|turnoff_right/]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="green;red;green"]["seamark:beacon_lateral:category"!~/preferred_channel_port|turnoff_left/]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="red;white;red;white"]["seamark:beacon_lateral:category"!=danger_right]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="green;white;green;white"]["seamark:beacon_lateral:category"!=danger_left]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="white;red"]["seamark:beacon_lateral:category"!=turnoff_right]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="white;green"]["seamark:beacon_lateral:category"!=turnoff_left]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="red;white;red"]["seamark:beacon_lateral:category"!=junction_right]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="green;white;green"]["seamark:beacon_lateral:category"!=junction_left]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="red;white"]["seamark:beacon_lateral:category"!=harbour_right]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"="green;white"]["seamark:beacon_lateral:category"!=harbour_left]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"=yellow]["seamark:beacon_lateral:category"!=harbour_right]["seamark:topmark:colour"=red]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"=yellow]["seamark:beacon_lateral:category"!=harbour_left]["seamark:topmark:colour"=green]
        # node["seamark:type"=beacon_lateral]["seamark:beacon_lateral:system"=cevni]["seamark:beacon_lateral:colour"=yellow]["seamark:beacon_lateral:category"!=bridge_pier][!"seamark:topmark:colour"]
        if (u'seamark:beacon_lateral:colour' in keys and u'seamark:beacon_lateral:system' in keys and u'seamark:type' in keys) or (u'seamark:beacon_lateral:colour' in keys and u'seamark:beacon_lateral:system' in keys and u'seamark:topmark:colour' in keys and u'seamark:type' in keys) or (u'seamark:beacon_lateral:system' in keys and u'seamark:buoy_lateral:colour' in keys and u'seamark:type' in keys) or (u'seamark:buoy_lateral:colour' in keys and u'seamark:buoy_lateral:system' in keys and u'seamark:type' in keys) or (u'seamark:buoy_lateral:colour' in keys and u'seamark:buoy_lateral:system' in keys and u'seamark:topmark:colour' in keys and u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'starboard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'starboard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;red;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;red;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;red;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_starboard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;red;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_starbord'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_starboard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-a') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'preferred_channel_starboard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'port'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'starboard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'iala-b') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'starboard'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_32e3abb7), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_288a42ac), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red;green') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_61629c48), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_281803e9), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;red;green') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_637abe26), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;white;red;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'danger_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;white;green;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'danger_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'white;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'turnoff_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'white;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'turnoff_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;white;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'junction_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;white;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'junction_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'yellow') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_right') and mapcss._tag_capture(capture_tags, 4, tags, u'seamark:topmark:colour') == mapcss._value_capture(capture_tags, 4, u'red'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'yellow') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_left') and mapcss._tag_capture(capture_tags, 4, tags, u'seamark:topmark:colour') == mapcss._value_capture(capture_tags, 4, u'green'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'yellow') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:buoy_lateral:category') != mapcss._value_capture(capture_tags, 3, u'bridge_pier') and not mapcss._tag_capture(capture_tags, 4, tags, u'seamark:topmark:colour'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_32e3abb7), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_288a42ac), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red;green') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_61629c48), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;green;red') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_281803e9), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;red;green') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_637abe26), mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;white;red;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'danger_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;white;green;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'danger_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'white;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'turnoff_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'white;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'turnoff_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;white;red') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'junction_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;white;green') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'junction_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'red;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_right'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'green;white') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_left'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'yellow') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_right') and mapcss._tag_capture(capture_tags, 4, tags, u'seamark:topmark:colour') == mapcss._value_capture(capture_tags, 4, u'red'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'yellow') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'harbour_left') and mapcss._tag_capture(capture_tags, 4, tags, u'seamark:topmark:colour') == mapcss._value_capture(capture_tags, 4, u'green'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_lateral') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon_lateral:system') == mapcss._value_capture(capture_tags, 1, u'cevni') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_lateral:colour') == mapcss._value_capture(capture_tags, 2, u'yellow') and mapcss._tag_capture(capture_tags, 3, tags, u'seamark:beacon_lateral:category') != mapcss._value_capture(capture_tags, 3, u'bridge_pier') and not mapcss._tag_capture(capture_tags, 4, tags, u'seamark:topmark:colour'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Probably wrong category on {0}, {1} colour mean {2} in {3}","{0.value}","{2.value}","{3.value}","{1.value}")
                err.append({'class': 9012004, 'subclass': 1696218961, 'text': mapcss.tr(u'Probably wrong category on {0}, {1} colour mean {2} in {3}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'), mapcss._tag_uncapture(capture_tags, u'{3.value}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'))})

        # node["seamark:type"=buoy_cardinal]["seamark:buoy_cardinal:colour"="black;yellow"]["seamark:buoy_cardinal:category"!=north]
        # node["seamark:type"=beacon_cardinal]["seamark:beacon:cardinal:colour"="black;yellow"]["seamark:beacon_cardinal:category"!=north]
        # node["seamark:type"=buoy_cardinal]["seamark:buoy_cardinal:colour"="black;yellow;black"]["seamark:buoy_cardinal:category"!=east]
        # node["seamark:type"=beacon_cardinal]["seamark:beacon:cardinal:colour"="black;yellow;black"]["seamark:beacon_cardinal:category"!=east]
        # node["seamark:type"=buoy_cardinal]["seamark:buoy_cardinal:colour"="yellow;black"]["seamark:buoy_cardinal:category"!=south]
        # node["seamark:type"=beacon_cardinal]["seamark:beacon:cardinal:colour"="yellow;black"]["seamark:beacon_cardinal:category"!=south]
        # node["seamark:type"=buoy_cardinal]["seamark:buoy_cardinal:colour"="yellow;black;yellow"]["seamark:buoy_cardinal:category"!=west]
        # node["seamark:type"=beacon_cardinal]["seamark:beacon:cardinal:colour"="yellow;black;yellow"]["seamark:beacon_cardinal:category"!=west]
        if (u'seamark:beacon:cardinal:colour' in keys and u'seamark:type' in keys) or (u'seamark:buoy_cardinal:colour' in keys and u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'black;yellow') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'north'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon:cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'black;yellow') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'north'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'black;yellow;black') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'east'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon:cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'black;yellow;black') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'east'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'yellow;black') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'south'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon:cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'yellow;black') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'south'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'buoy_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:buoy_cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'yellow;black;yellow') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:buoy_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'west'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'beacon_cardinal') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:beacon:cardinal:colour') == mapcss._value_capture(capture_tags, 1, u'yellow;black;yellow') and mapcss._tag_capture(capture_tags, 2, tags, u'seamark:beacon_cardinal:category') != mapcss._value_capture(capture_tags, 2, u'west'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Probably wrong category on {0}, the colour combination {1} usually mean {2}","{0.value}","{1.value}","{2.value}")
                err.append({'class': 9012005, 'subclass': 1608037739, 'text': mapcss.tr(u'Probably wrong category on {0}, the colour combination {1} usually mean {2}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))})

        # node["seamark:type"=wreck][!"seamark:wreck:category"]
        if (u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'wreck') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:wreck:category'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} have no {1}","{0.value}","{1.key}")
                err.append({'class': 9012006, 'subclass': 408021642, 'text': mapcss.tr(u'{0} have no {1}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node["seamark:wreck:category"]["seamark:type"!=wreck]
        if (u'seamark:wreck:category' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:wreck:category') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:type') != mapcss._value_capture(capture_tags, 1, u'wreck'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} set without {1}={2}","{0.key}","{1.key}","{1.value}")
                err.append({'class': 9012007, 'subclass': 1137370881, 'text': mapcss.tr(u'{0} set without {1}={2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'))})

        # node["seamark:type"=rock][!"seamark:rock:water_level"]
        if (u'seamark:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:type') == mapcss._value_capture(capture_tags, 0, u'rock') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:rock:water_level'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} without {1}","{0.value}","{1.key}")
                err.append({'class': 9012008, 'subclass': 806216043, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node["seamark:notice:category"][!"seamark:notice:system"]
        # node["seamark:notice:1:category"][!"seamark:notice:1:system"]
        # node["seamark:notice:2:category"][!"seamark:notice:2:system"]
        # node["seamark:notice:3:category"][!"seamark:notice:3:system"]
        # node["seamark:notice:4:category"][!"seamark:notice:4:system"]
        # node["seamark:notice:5:category"][!"seamark:notice:5:system"]
        # node["seamark:notice:6:category"][!"seamark:notice:6:system"]
        # node["seamark:notice:7:category"][!"seamark:notice:7:system"]
        # node["seamark:notice:8:category"][!"seamark:notice:8:system"]
        # node["seamark:notice:9:category"][!"seamark:notice:9:system"]
        if (u'seamark:notice:1:category' in keys) or (u'seamark:notice:2:category' in keys) or (u'seamark:notice:3:category' in keys) or (u'seamark:notice:4:category' in keys) or (u'seamark:notice:5:category' in keys) or (u'seamark:notice:6:category' in keys) or (u'seamark:notice:7:category' in keys) or (u'seamark:notice:8:category' in keys) or (u'seamark:notice:9:category' in keys) or (u'seamark:notice:category' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:3:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:3:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:4:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:4:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:5:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:5:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:6:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:6:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:7:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:7:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:8:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:8:system'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:9:category') and not mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:9:system'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                err.append({'class': 9012008, 'subclass': 1495790025, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node["seamark:notice:system"=cevni]["seamark:notice:function"!=prohibition]["seamark:notice:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:1:system"=cevni]["seamark:notice:1:function"!=prohibition]["seamark:notice:1:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:2:system"=cevni]["seamark:notice:2:function"!=prohibition]["seamark:notice:2:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:3:system"=cevni]["seamark:notice:3:function"!=prohibition]["seamark:notice:3:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:4:system"=cevni]["seamark:notice:4:function"!=prohibition]["seamark:notice:4:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:5:system"=cevni]["seamark:notice:5:function"!=prohibition]["seamark:notice:5:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:6:system"=cevni]["seamark:notice:6:function"!=prohibition]["seamark:notice:6:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:7:system"=cevni]["seamark:notice:7:function"!=prohibition]["seamark:notice:7:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:8:system"=cevni]["seamark:notice:8:function"!=prohibition]["seamark:notice:8:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:9:system"=cevni]["seamark:notice:9:function"!=prohibition]["seamark:notice:9:category"=~/no_entry|closed_area|no_overtaking|no_convoy_overtaking|no_passing|no_convoy_passing|no_berthing|no_berthing_lateral_limit|no_anchoring|no_mooring|no_turning|no_wash|no_passage_left|no_passage_right|no_motor_craft|no_sport_craft|no_waterskiing|no_sailing_craft|no_unpowered_craft|no_sailboards|no_high_speeds|no_launching_beaching|no_waterbikes/]
        # node["seamark:notice:system"=cevni]["seamark:notice:function"!=regulation]["seamark:notice:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:1:system"=cevni]["seamark:notice:1:function"!=regulation]["seamark:notice:1:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:2:system"=cevni]["seamark:notice:2:function"!=regulation]["seamark:notice:2:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:3:system"=cevni]["seamark:notice:3:function"!=regulation]["seamark:notice:3:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:4:system"=cevni]["seamark:notice:4:function"!=regulation]["seamark:notice:4:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:5:system"=cevni]["seamark:notice:5:function"!=regulation]["seamark:notice:5:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:6:system"=cevni]["seamark:notice:6:function"!=regulation]["seamark:notice:6:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:7:system"=cevni]["seamark:notice:7:function"!=regulation]["seamark:notice:7:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:8:system"=cevni]["seamark:notice:8:function"!=regulation]["seamark:notice:8:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:9:system"=cevni]["seamark:notice:9:function"!=regulation]["seamark:notice:9:category"=~/move_to_left|move_to_right|move_to_port|move_to_starboard|keep_to_port|keep_to_starboard|cross_to_port|cross_to_starboard|stop|speed_limit|sound_horn|keep_lookout|give_way_junction|give_way_crossing|make_radio_contact/]
        # node["seamark:notice:system"=cevni]["seamark:notice:function"!=restriction]["seamark:notice:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:1:system"=cevni]["seamark:notice:1:function"!=restriction]["seamark:notice:1:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:2:system"=cevni]["seamark:notice:2:function"!=restriction]["seamark:notice:2:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:3:system"=cevni]["seamark:notice:3:function"!=restriction]["seamark:notice:3:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:4:system"=cevni]["seamark:notice:4:function"!=restriction]["seamark:notice:4:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:5:system"=cevni]["seamark:notice:5:function"!=restriction]["seamark:notice:5:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:6:system"=cevni]["seamark:notice:6:function"!=restriction]["seamark:notice:6:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:7:system"=cevni]["seamark:notice:7:function"!=restriction]["seamark:notice:7:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:8:system"=cevni]["seamark:notice:8:function"!=restriction]["seamark:notice:8:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:9:system"=cevni]["seamark:notice:9:function"!=restriction]["seamark:notice:9:category"=~/limited_depth|limited_headroom|limited_width|navigation_restrictions|channel_distance_left|channel_distance_right/]
        # node["seamark:notice:system"=cevni]["seamark:notice:function"!=recommendation]["seamark:notice:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:1:system"=cevni]["seamark:notice:1:function"!=recommendation]["seamark:notice:1:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:2:system"=cevni]["seamark:notice:2:function"!=recommendation]["seamark:notice:2:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:3:system"=cevni]["seamark:notice:3:function"!=recommendation]["seamark:notice:3:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:4:system"=cevni]["seamark:notice:4:function"!=recommendation]["seamark:notice:4:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:5:system"=cevni]["seamark:notice:5:function"!=recommendation]["seamark:notice:5:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:6:system"=cevni]["seamark:notice:6:function"!=recommendation]["seamark:notice:6:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:7:system"=cevni]["seamark:notice:7:function"!=recommendation]["seamark:notice:7:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:8:system"=cevni]["seamark:notice:8:function"!=recommendation]["seamark:notice:8:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:9:system"=cevni]["seamark:notice:9:function"!=recommendation]["seamark:notice:9:category"=~/channel_two_way|channel_one_way|opening_to_right|opening_to_left|proceed_to_left|proceed_to_right/]
        # node["seamark:notice:system"=cevni]["seamark:notice:function"!=information]["seamark:notice:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:1:system"=cevni]["seamark:notice:1:function"!=information]["seamark:notice:1:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:2:system"=cevni]["seamark:notice:2:function"!=information]["seamark:notice:2:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:3:system"=cevni]["seamark:notice:3:function"!=information]["seamark:notice:3:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:4:system"=cevni]["seamark:notice:4:function"!=information]["seamark:notice:4:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:5:system"=cevni]["seamark:notice:5:function"!=information]["seamark:notice:5:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:6:system"=cevni]["seamark:notice:6:function"!=information]["seamark:notice:6:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:7:system"=cevni]["seamark:notice:7:function"!=information]["seamark:notice:7:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:8:system"=cevni]["seamark:notice:8:function"!=information]["seamark:notice:8:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:9:system"=cevni]["seamark:notice:9:function"!=information]["seamark:notice:9:category"=~/entry_permitted|overhead_cable|weir|ferry_non_independent|ferry_independent|berthing_permitted|berthing_lateral_limit|berthing_lateral_limits|berthing_rafting_limit|berthing_unmarked_pushing|berthing_marked_pushing_1|berthing_marked_pushing_2|berthing_marked_pushing_3|berthing_unmarked_non_pushing|berthing_marked_non_pushing_1|berthing_marked_non_pushing_2|berthing_marked_non_pushing_3|berthing_unmarked|berthing_marked_1|berthing_marked_2|berthing_marked_3|anchoring_permitted|mooring_permitted|vehicle_loading_berth|turning_area|secondary_waterway_crossing|secondary_waterway_right|secondary_waterway_left|main_waterway_right_secondary_ahead|main_waterway_left_secondary_ahead|main_waterway_right_secondary_left|main_waterway_left_secondary_right|main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|main_waterway_crossing|main_waterway_junction|main_waterway_ahead_right|main_waterway_ahead_left|main_waterway_ahead_right_secondary_left|main_waterway_ahead_left_secondary_right|prohibition_ends|drinking_water|telephone|motor_craft_permitted|sport_craft_permitted|waterskiing_permitted|sailing_craft_permitted|unpowered_craft_permitted|sailboards_permitted|high_speeds_permitted|launching_beaching_permitted|radio_information|waterbikes_permitted/]
        # node["seamark:notice:system"=bniwr]["seamark:notice:system"!=prohibition]["seamark:notice:category"=~/no_anchoring/]
        # node["seamark:notice:system"=bniwr2]["seamark:notice:system"!=prohibition]["seamark:notice:category"=~/no_anchoring/]
        # node["seamark:notice:1:system"=bniwr]["seamark:notice:1:system"!=prohibition]["seamark:notice:1:category"=~/no_anchoring/]
        # node["seamark:notice:1:system"=bniwr2]["seamark:notice:1:system"!=prohibition]["seamark:notice:1:category"=~/no_anchoring/]
        # node["seamark:notice:2:system"=bniwr]["seamark:notice:2:system"!=prohibition]["seamark:notice:2:category"=~/no_anchoring/]
        # node["seamark:notice:2:system"=bniwr2]["seamark:notice:2:system"!=prohibition]["seamark:notice:2:category"=~/no_anchoring/]
        # node["seamark:notice:system"=bniwr]["seamark:notice:system"!=regulation]["seamark:notice:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid|cross_river_to_port|cross_river_to_starboard|reduce_speed/]
        # node["seamark:notice:system"=bniwr2]["seamark:notice:system"!=regulation]["seamark:notice:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid|cross_river_to_port|cross_river_to_starboard|reduce_speed/]
        # node["seamark:notice:1:system"=bniwr]["seamark:notice:1:system"!=regulation]["seamark:notice:1:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid|cross_river_to_port|cross_river_to_starboard|reduce_speed/]
        # node["seamark:notice:1:system"=bniwr2]["seamark:notice:1:system"!=regulation]["seamark:notice:1:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid|cross_river_to_port|cross_river_to_starboard|reduce_speed/]
        # node["seamark:notice:2:system"=bniwr]["seamark:notice:2:system"!=regulation]["seamark:notice:2:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid|cross_river_to_port|cross_river_to_starboard|reduce_speed/]
        # node["seamark:notice:2:system"=bniwr2]["seamark:notice:2:system"!=regulation]["seamark:notice:2:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid|cross_river_to_port|cross_river_to_starboard|reduce_speed/]
        # node["seamark:notice:system"=bniwr]["seamark:notice:system"!=restriction]["seamark:notice:category"=~/limited_headroom/]
        # node["seamark:notice:system"=bniwr2]["seamark:notice:system"!=restriction]["seamark:notice:category"=~/limited_headroom/]
        # node["seamark:notice:1:system"=bniwr]["seamark:notice:1:system"!=restriction]["seamark:notice:1:category"=~/limited_headroom/]
        # node["seamark:notice:1:system"=bniwr2]["seamark:notice:1:system"!=restriction]["seamark:notice:1:category"=~/limited_headroom/]
        # node["seamark:notice:2:system"=bniwr]["seamark:notice:2:system"!=restriction]["seamark:notice:2:category"=~/limited_headroom/]
        # node["seamark:notice:2:system"=bniwr2]["seamark:notice:2:system"!=restriction]["seamark:notice:2:category"=~/limited_headroom/]
        # node["seamark:notice:system"=bniwr]["seamark:notice:system"!=recommendation]["seamark:notice:category"=~/opening_to_right|opening_to_left/]
        # node["seamark:notice:system"=bniwr2]["seamark:notice:system"!=recommendation]["seamark:notice:category"=~/opening_to_right|opening_to_left/]
        # node["seamark:notice:1:system"=bniwr]["seamark:notice:1:system"!=recommendation]["seamark:notice:1:category"=~/opening_to_right|opening_to_left/]
        # node["seamark:notice:1:system"=bniwr2]["seamark:notice:1:system"!=recommendation]["seamark:notice:1:category"=~/opening_to_right|opening_to_left/]
        # node["seamark:notice:2:system"=bniwr]["seamark:notice:2:system"!=recommendation]["seamark:notice:2:category"=~/opening_to_right|opening_to_left/]
        # node["seamark:notice:2:system"=bniwr2]["seamark:notice:2:system"!=recommendation]["seamark:notice:2:category"=~/opening_to_right|opening_to_left/]
        # node["seamark:notice:system"=bniwr]["seamark:notice:system"!=information]["seamark:notice:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|traffic_between_margins/]
        # node["seamark:notice:system"=bniwr2]["seamark:notice:system"!=information]["seamark:notice:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|traffic_between_margins/]
        # node["seamark:notice:1:system"=bniwr]["seamark:notice:1:system"!=information]["seamark:notice:1:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|traffic_between_margins/]
        # node["seamark:notice:1:system"=bniwr2]["seamark:notice:1:system"!=information]["seamark:notice:1:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|traffic_between_margins/]
        # node["seamark:notice:2:system"=bniwr]["seamark:notice:2:system"!=information]["seamark:notice:2:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|traffic_between_margins/]
        # node["seamark:notice:2:system"=bniwr2]["seamark:notice:2:system"!=information]["seamark:notice:2:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right|traffic_between_margins/]
        # node["seamark:notice:system"=ppwbc]["seamark:notice:system"!=regulation]["seamark:notice:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid-river|cross_river_to_port|cross_river_to_starboard/]
        # node["seamark:notice:1:system"=ppwbc]["seamark:notice:1:system"!=regulation]["seamark:notice:1:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid-river|cross_river_to_port|cross_river_to_starboard/]
        # node["seamark:notice:2:system"=ppwbc]["seamark:notice:2:system"!=regulation]["seamark:notice:2:category"=~/keep_to_port_margin|keep_to_starboard_margin|keep_to_mid-river|cross_river_to_port|cross_river_to_starboard/]
        # node["seamark:notice:system"=ppwbc]["seamark:notice:system"!=information]["seamark:notice:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right/]
        # node["seamark:notice:1:system"=ppwbc]["seamark:notice:1:system"!=information]["seamark:notice:1:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right/]
        # node["seamark:notice:2:system"=ppwbc]["seamark:notice:2:system"!=information]["seamark:notice:2:category"=~/main_waterway_right_secondary_ahead_left|main_waterway_left_secondary_ahead_right/]
        if (u'seamark:notice:1:category' in keys and u'seamark:notice:1:system' in keys) or (u'seamark:notice:2:category' in keys and u'seamark:notice:2:system' in keys) or (u'seamark:notice:3:category' in keys and u'seamark:notice:3:system' in keys) or (u'seamark:notice:4:category' in keys and u'seamark:notice:4:system' in keys) or (u'seamark:notice:5:category' in keys and u'seamark:notice:5:system' in keys) or (u'seamark:notice:6:category' in keys and u'seamark:notice:6:system' in keys) or (u'seamark:notice:7:category' in keys and u'seamark:notice:7:system' in keys) or (u'seamark:notice:8:category' in keys and u'seamark:notice:8:system' in keys) or (u'seamark:notice:9:category' in keys and u'seamark:notice:9:system' in keys) or (u'seamark:notice:category' in keys and u'seamark:notice:system' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:3:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:3:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:3:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:4:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:4:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:4:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:5:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:5:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:5:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:6:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:6:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:6:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:7:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:7:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:7:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:8:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:8:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:8:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:9:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:9:function') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0e3e01fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:9:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:3:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:3:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:3:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:4:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:4:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:4:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:5:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:5:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:5:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:6:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:6:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:6:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:7:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:7:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:7:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:8:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:8:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:8:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:9:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:9:function') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_1389a933), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:9:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:3:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:3:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:3:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:4:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:4:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:4:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:5:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:5:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:5:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:6:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:6:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:6:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:7:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:7:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:7:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:8:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:8:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:8:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:9:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:9:function') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_336a6c28), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:9:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:3:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:3:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:3:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:4:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:4:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:4:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:5:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:5:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:5:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:6:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:6:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:6:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:7:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:7:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:7:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:8:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:8:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:8:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:9:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:9:function') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_253b0e7a), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:9:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:3:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:3:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:3:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:4:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:4:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:4:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:5:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:5:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:5:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:6:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:6:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:6:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:7:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:7:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:7:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:8:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:8:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:8:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:9:system') == mapcss._value_capture(capture_tags, 0, u'cevni') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:9:function') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2e10f0c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:9:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_7c5430c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_7c5430c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_7c5430c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_7c5430c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_7c5430c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'prohibition') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_7c5430c7), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09200db5), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09200db5), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09200db5), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09200db5), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09200db5), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09200db5), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_39084725), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_39084725), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_39084725), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_39084725), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_39084725), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_39084725), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09c0bae9), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09c0bae9), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09c0bae9), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09c0bae9), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09c0bae9), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'recommendation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_09c0bae9), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_430e795b), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_430e795b), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_430e795b), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_430e795b), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_430e795b), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'bniwr2') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_430e795b), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'ppwbc') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0b7ab6fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'ppwbc') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0b7ab6fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'ppwbc') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'regulation') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_0b7ab6fc), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system') == mapcss._value_capture(capture_tags, 0, u'ppwbc') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2a269778), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system') == mapcss._value_capture(capture_tags, 0, u'ppwbc') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2a269778), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:1:category')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system') == mapcss._value_capture(capture_tags, 0, u'ppwbc') and mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:system') != mapcss._value_capture(capture_tags, 1, u'information') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2a269778), mapcss._tag_capture(capture_tags, 2, tags, u'seamark:notice:2:category')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("In {0} {1}={2} require {3}={4}","{0.value}","{2.key}","{2.value}","{1.key}","{1.value}")
                err.append({'class': 9012009, 'subclass': 838520301, 'text': mapcss.tr(u'In {0} {1}={2} require {3}={4}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{1.value}'))})

        # node["seamark:notice:system"=~/bniwr2|ppwbc/]["seamark:notice:bank"!~/right|left/]
        # node["seamark:notice:1:system"=~/bniwr2|ppwbc/]["seamark:notice:1:bank"!~/right|left/]
        # node["seamark:notice:2:system"=~/bniwr2|ppwbc/]["seamark:notice:2:bank"!~/right|left/]
        if (u'seamark:notice:1:system' in keys) or (u'seamark:notice:2:system' in keys) or (u'seamark:notice:system' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0e114cad), mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:system')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_01dd9715), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:bank')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0e114cad), mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:1:system')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_01dd9715), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:1:bank')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0e114cad), mapcss._tag_capture(capture_tags, 0, tags, u'seamark:notice:2:system')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_01dd9715), mapcss._tag_capture(capture_tags, 1, tags, u'seamark:notice:2:bank')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sign require {1} set to left or right","{0.value}","{1.key}")
                err.append({'class': 9012010, 'subclass': 1214402030, 'text': mapcss.tr(u'{0} sign require {1} set to left or right', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_Seamark(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


