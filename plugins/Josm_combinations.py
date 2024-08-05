#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_combinations(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/combinations.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9001001] = self.def_class(item = 9001, level = 3, tags = ["tag"], title = mapcss.tr('missing tag'))
        self.errors[9001002] = self.def_class(item = 9001, level = 3, tags = ["tag"], title = mapcss.tr('suspicious tag combination'))
        self.errors[9001003] = self.def_class(item = 9001, level = 3, tags = ["tag"], title = mapcss.tr('{0} on a relation without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[9001004] = self.def_class(item = 9001, level = 3, tags = ["tag"], title = mapcss.tr('incomplete usage of {0} on a way without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')))
        self.errors[9001005] = self.def_class(item = 9001, level = 3, tags = ["tag"], title = mapcss.tr('Use {0} only as value of {1}', 'transition', 'placement'))

        self.re_01d4d495 = re.compile(r'^(paved|asphalt|cobblestone|cobblestone:flattened|sett|concrete|concrete:plates|paving_stones|metal|wood|unhewn_cobblestone)$')
        self.re_050395e0 = re.compile(r'^maxspeed:?')
        self.re_06b82725 = re.compile(r'^(yes|minor|no)$')
        self.re_0737b0c4 = re.compile(r'^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$')
        self.re_0889a956 = re.compile(r'^(basin|reservoir)$')
        self.re_088b0835 = re.compile(r'^addr:')
        self.re_0aef1f28 = re.compile(r'^cycleway(:|$)')
        self.re_12ce6b85 = re.compile(r':forward')
        self.re_143f11c5 = re.compile(r'^(no|use_sidepath)$')
        self.re_19e33301 = re.compile(r'^no$')
        self.re_1bc43c40 = re.compile(r'^(left|right|both)$')
        self.re_1dcd648f = re.compile(r'^(runway|taxiway)$')
        self.re_209d461d = re.compile(r'^(path|footway|cycleway|construction|proposed)$')
        self.re_213d4d09 = re.compile(r'^parking.*')
        self.re_22985ce9 = re.compile(r'^oneway:(bicycle|bus|mofa|moped|psv)$')
        self.re_22ceec1b = re.compile(r'^.*:lanes$')
        self.re_23888fca = re.compile(r'^(motorway|motorway_link|trunk|trunk_link)$')
        self.re_25d98c90 = re.compile(r'_name$')
        self.re_27d9cb1c = re.compile(r'^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$')
        self.re_29fa4401 = re.compile(r'^(beach|bare_rock|cliff|peak|water)$')
        self.re_2d1850d1 = re.compile(r'^recycling:')
        self.re_2fb1110d = re.compile(r':highway$')
        self.re_2fc1bb0a = re.compile(r'^(canal|fairway|lock|river|tidal_channel)$')
        self.re_333281f7 = re.compile(r'^oneway:(.+:)?conditional$')
        self.re_33560b51 = re.compile(r'^(bollard|bump_gate|bus_trap|cattle_grid|chain|coupure|entrance|gate|height_restrictor|jersey_barrier|kerb|lift_gate|rope|sally_port|sliding_beam|sliding_gate|spikes|swing_gate|toll_booth|yes)$')
        self.re_337d9a77 = re.compile(r'^maxspeed:.+')
        self.re_382feae2 = re.compile(r'^(sand|mud|ground|earth|dirt|grass|ice|salt|snow|woodchips)$')
        self.re_390b8c0f = re.compile(r'^(building|building:part)$')
        self.re_3a43a33d = re.compile(r'[a-z]-[A-Z].*[0-9]-[0-9]')
        self.re_3ad9e1f5 = re.compile(r'^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$')
        self.re_3b1153a4 = re.compile(r'^plant:')
        self.re_3b4f8f73 = re.compile(r'^(recreation_ground|piste|farm|farmland)$')
        self.re_3baad59c = re.compile(r'^.*:lanes:both_ways$')
        self.re_3e28f822 = re.compile(r'^.*:lanes:(forward|backward|both_ways)$')
        self.re_41650b2e = re.compile(r'^(bar|dojo|pub|restaurant|swimming_pool)$')
        self.re_43e7f95e = re.compile(r'mph')
        self.re_49fc2c26 = re.compile(r'^(bowling_alley|slipway|swimming_pool|track)$')
        self.re_4f156c8f = re.compile(r'^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$')
        self.re_4fbfe59b = re.compile(r'^(water|spring)$')
        self.re_503776bb = re.compile(r'^generator:')
        self.re_5111b0b1 = re.compile(r'^(no|none|separate)$')
        self.re_51b15093 = re.compile(r'^(Des Moines Headwaters|Upper Des Moines|East Fork Des Moines)$')
        self.re_521b2098 = re.compile(r'water|bay|strait')
        self.re_53cf0b2e = re.compile(r'^(cycleway|footway|path)$')
        self.re_57c5150b = re.compile(r'^placement:.*$')
        self.re_5cf0a79f = re.compile(r'^(parking|parking_space|parking_entrance|motorcycle_parking)$')
        self.re_5dd46ebe = re.compile(r'^(pedestrian|raceway)$')
        self.re_5ee853b2 = re.compile(r'^(ferry|road)$')
        self.re_60ec5bd8 = re.compile(r'^bicycle:')
        self.re_68c05e86 = re.compile(r'^(wall|retaining_wall)$')
        self.re_6f957488 = re.compile(r'^(unpaved|compacted|gravel|fine_gravel|pebblestone|ground|earth|dirt|grass|sand|mud|ice|salt|snow|woodchips)$')
        self.re_7346b495 = re.compile(r':backward')
        self.re_734e4397 = re.compile(r'^(yes|stepping_stones)$')
        self.re_78efbab0 = re.compile(r'(^|;)manual(;|$)')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_AllSameCycleway = set_AllSameMaxspeed = set_AllSameSidewalk = set_MotorwayTrunk = set_PlacementTransitionWarning = set_TunnelCulvertWithoutWaterway = set_fully_paved_surface = set_only_one_tag = set_unpaved_surface = False

        # node[voltage:primary][!transformer]
        # node[voltage:secondary][!transformer]
        # node[voltage:tertiary][!transformer]
        # node[ntd_id][!highway]
        # *[border_type][!boundary]
        # *[piste:difficulty][!piste:type]
        # *[place][!name][place!=islet][place!=plot][noname!=yes]
        # *[transformer][!power]
        # *[source:date][!source]
        # *[source:name][!name][noname!=yes]
        # *[source:maxspeed:forward][!maxspeed:forward][!maxspeed]
        # *[source:maxspeed:backward][!maxspeed:backward][!maxspeed]
        # *[source:building][!building]
        # *[source:ref][!ref][noref!=yes]
        # *[source:population][!population]
        # *[source:postal_code][!postal_code]
        # *[source:ele][!ele]
        # *[source:ref:INSEE][!ref:INSEE]
        # *[source:lit][!lit]
        # *[source:hgv][!hgv]
        # *[source:highway][!highway]
        # *[source:maxaxleload][!maxaxleload]
        # *[source:surface][!surface]
        # *[source:bridge][!bridge]
        # *[source:old_name][!old_name]
        # *[source:bicycle][!bicycle]
        # *[source:designation][!designation]
        # *[source:height][!height]
        # *[source:lanes][!lanes]
        # *[source:postcode][!addr:postcode]
        # *[source:housenumber][!addr:housenumber]
        # *[source:addr:postcode][!addr:postcode]
        # *[source:addr:housenumber][!addr:housenumber]
        if ('border_type' in keys) or ('ntd_id' in keys) or ('piste:difficulty' in keys) or ('place' in keys) or ('source:addr:housenumber' in keys) or ('source:addr:postcode' in keys) or ('source:bicycle' in keys) or ('source:bridge' in keys) or ('source:building' in keys) or ('source:date' in keys) or ('source:designation' in keys) or ('source:ele' in keys) or ('source:height' in keys) or ('source:hgv' in keys) or ('source:highway' in keys) or ('source:housenumber' in keys) or ('source:lanes' in keys) or ('source:lit' in keys) or ('source:maxaxleload' in keys) or ('source:maxspeed:backward' in keys) or ('source:maxspeed:forward' in keys) or ('source:name' in keys) or ('source:old_name' in keys) or ('source:population' in keys) or ('source:postal_code' in keys) or ('source:postcode' in keys) or ('source:ref' in keys) or ('source:ref:INSEE' in keys) or ('source:surface' in keys) or ('transformer' in keys) or ('voltage:primary' in keys) or ('voltage:secondary' in keys) or ('voltage:tertiary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:primary')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'transformer')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:secondary')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'transformer')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:tertiary')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'transformer')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ntd_id')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'border_type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'boundary')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'piste:difficulty')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'piste:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'place') != mapcss._value_const_capture(capture_tags, 2, 'islet', 'islet')) and (mapcss._tag_capture(capture_tags, 3, tags, 'place') != mapcss._value_const_capture(capture_tags, 3, 'plot', 'plot')) and (mapcss._tag_capture(capture_tags, 4, tags, 'noname') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'transformer')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'power')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:date')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'source')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:name')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noname') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed:forward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:forward')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed:backward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:building')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ref')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noref') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:population')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'population')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:postal_code')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'postal_code')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ele')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ele')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ref:INSEE')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:INSEE')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:lit')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lit')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:hgv')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'hgv')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:highway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxaxleload')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:surface')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'surface')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:bridge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:old_name')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'old_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:bicycle')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'bicycle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:designation')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'designation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:height')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'height')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:lanes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lanes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:postcode')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:housenumber')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr:postcode')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr:housenumber')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # assertMatch:"node source:addr:postcode=postman"
                err.append({'class': 9001001, 'subclass': 31231113, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # node[railway:switch][railway!=switch]
        # *[generator:source][power!=generator]
        # *[generator:method][power!=generator]
        # *[generator:type][power!=generator]
        # node[fire_hydrant:type][emergency!=fire_hydrant][disused:emergency!=fire_hydrant]
        # node[manhole][man_made!=manhole]
        # *[recycling_type][amenity!=recycling]
        # *[information][tourism!=information]
        # node[board_type][information!=board]
        # *[shelter_type][amenity!=shelter]
        # node[lamp_type][highway!=street_lamp]
        # node[map_type][information!=map]
        # *[archaeological_site][historic!=archaeological_site]
        # *[artwork_type][tourism!=artwork][exhibit!=artwork]
        # *[castle_type][historic!=castle]
        # *[parking][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking)$/][parking!=yes][parking!=no]
        # *[zoo][tourism!=zoo]
        # *[bunker_type][military!=bunker]
        if ('archaeological_site' in keys) or ('artwork_type' in keys) or ('board_type' in keys) or ('bunker_type' in keys) or ('castle_type' in keys) or ('fire_hydrant:type' in keys) or ('generator:method' in keys) or ('generator:source' in keys) or ('generator:type' in keys) or ('information' in keys) or ('lamp_type' in keys) or ('manhole' in keys) or ('map_type' in keys) or ('parking' in keys) or ('railway:switch' in keys) or ('recycling_type' in keys) or ('shelter_type' in keys) or ('zoo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway:switch')) and (mapcss._tag_capture(capture_tags, 1, tags, 'railway') != mapcss._value_const_capture(capture_tags, 1, 'switch', 'switch')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:source')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fire_hydrant:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'emergency') != mapcss._value_const_capture(capture_tags, 1, 'fire_hydrant', 'fire_hydrant')) and (mapcss._tag_capture(capture_tags, 2, tags, 'disused:emergency') != mapcss._value_const_capture(capture_tags, 2, 'fire_hydrant', 'fire_hydrant')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'manhole')) and (mapcss._tag_capture(capture_tags, 1, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 1, 'manhole', 'manhole')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'recycling_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'recycling', 'recycling')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'information')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'information', 'information')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'board_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'information') != mapcss._value_const_capture(capture_tags, 1, 'board', 'board')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shelter_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'shelter', 'shelter')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lamp_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway') != mapcss._value_const_capture(capture_tags, 1, 'street_lamp', 'street_lamp')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'map_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'information') != mapcss._value_const_capture(capture_tags, 1, 'map', 'map')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'archaeological_site')) and (mapcss._tag_capture(capture_tags, 1, tags, 'historic') != mapcss._value_const_capture(capture_tags, 1, 'archaeological_site', 'archaeological_site')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'artwork_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'artwork', 'artwork')) and (mapcss._tag_capture(capture_tags, 2, tags, 'exhibit') != mapcss._value_const_capture(capture_tags, 2, 'artwork', 'artwork')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'castle_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'historic') != mapcss._value_const_capture(capture_tags, 1, 'castle', 'castle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5cf0a79f, '^(parking|parking_space|parking_entrance|motorcycle_parking)$'), mapcss._tag_capture(capture_tags, 1, tags, 'amenity'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'parking') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'zoo')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'zoo', 'zoo')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bunker_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'military') != mapcss._value_const_capture(capture_tags, 1, 'bunker', 'bunker')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1864412486, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[bridge:movable][bridge!=movable][man_made!=bridge]
        # *[substation][power!=substation][pipeline!=substation]
        # *[reservoir_type][landuse!=reservoir][water!=reservoir]
        if ('bridge:movable' in keys) or ('reservoir_type' in keys) or ('substation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge:movable')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') != mapcss._value_const_capture(capture_tags, 1, 'movable', 'movable')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'bridge', 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'substation')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'substation', 'substation')) and (mapcss._tag_capture(capture_tags, 2, tags, 'pipeline') != mapcss._value_const_capture(capture_tags, 2, 'substation', 'substation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'reservoir_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 1, 'reservoir', 'reservoir')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'reservoir', 'reservoir')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1195794842, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[iata][aeroway!=aerodrome][aeroway!=heliport][aeroway!=helipad]
        # *[icao][aeroway!=aerodrome][aeroway!=heliport][aeroway!=helipad]
        if ('iata' in keys) or ('icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'iata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 1, 'aerodrome', 'aerodrome')) and (mapcss._tag_capture(capture_tags, 2, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 2, 'heliport', 'heliport')) and (mapcss._tag_capture(capture_tags, 3, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 3, 'helipad', 'helipad')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'icao')) and (mapcss._tag_capture(capture_tags, 1, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 1, 'aerodrome', 'aerodrome')) and (mapcss._tag_capture(capture_tags, 2, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 2, 'heliport', 'heliport')) and (mapcss._tag_capture(capture_tags, 3, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 3, 'helipad', 'helipad')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.tag}","{2.tag}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1908755652, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

        # *[pump_mechanism][man_made!=pump][man_made!=windpump][man_made!=water_well][man_made!=petroleum_well]
        if ('pump_mechanism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pump_mechanism')) and (mapcss._tag_capture(capture_tags, 1, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 1, 'pump', 'pump')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'windpump', 'windpump')) and (mapcss._tag_capture(capture_tags, 3, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 3, 'water_well', 'water_well')) and (mapcss._tag_capture(capture_tags, 4, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 4, 'petroleum_well', 'petroleum_well')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.tag}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1271875329, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.tag}'))})

        # node[traffic_sign=maxspeed][!maxspeed][!/^maxspeed:.+/]
        # *[actuator=manual][!handle]
        # *[mechanical_driver=manual][!handle]
        # node[emergency=fire_hydrant][!fire_hydrant:type]
        # *[tourism=information][!information]
        # *[leisure=pitch][!sport]
        # *[aeroway=terminal][!building]
        # *[office=government][!government]
        # *[power=generator][!generator:source]
        # *[amenity=social_facility][!social_facility]
        # *[amenity=place_of_worship][!religion]
        # *[man_made=tower][!tower:type]
        if ('actuator' in keys) or ('aeroway' in keys) or ('amenity' in keys) or ('emergency' in keys) or ('leisure' in keys) or ('man_made' in keys) or ('mechanical_driver' in keys) or ('office' in keys) or ('power' in keys) or ('tourism' in keys) or ('traffic_sign' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_sign') == mapcss._value_capture(capture_tags, 0, 'maxspeed')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_337d9a77)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'actuator') == mapcss._value_capture(capture_tags, 0, 'manual')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'handle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mechanical_driver') == mapcss._value_capture(capture_tags, 0, 'manual')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'handle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'fire_hydrant')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'fire_hydrant:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tourism') == mapcss._value_capture(capture_tags, 0, 'information')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'information')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'pitch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'terminal')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'office') == mapcss._value_capture(capture_tags, 0, 'government')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'government')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'generator')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'generator:source')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'social_facility')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'social_facility')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'place_of_worship')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'religion')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'tower')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'tower:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                # assertNoMatch:"node traffic_sign=maxspeed maxspeed:hgv:conditional=\"80 @ (weight>7.5 AND 22:00-05:00)\""
                err.append({'class': 9001001, 'subclass': 2095780217, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[segregated][!highway][railway!=crossing]
        if ('segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'segregated')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway') != mapcss._value_const_capture(capture_tags, 2, 'crossing', 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 413539177, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[amenity=recycling][recycling_type!=container][recycling_type!=centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'container', 'container')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 2, 'centre', 'centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 747056792, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[smoothness][!highway][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$/][barrier!=kerb][!kerb]
        if ('smoothness' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'smoothness')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_4f156c8f, '^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$'), mapcss._tag_capture(capture_tags, 2, tags, 'amenity'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'barrier') != mapcss._value_const_capture(capture_tags, 3, 'kerb', 'kerb')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.key}")
                err.append({'class': 9001001, 'subclass': 1922079652, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.key}'))})

        # *[intermittent][!waterway][natural!~/^(water|spring)$/][landuse!~/^(basin|reservoir)$/][ford!~/^(yes|stepping_stones)$/]
        # *[boat][!waterway][natural!=water][landuse!~/^(basin|reservoir)$/][ford!=yes]
        if ('boat' in keys) or ('intermittent' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'intermittent')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_4fbfe59b, '^(water|spring)$'), mapcss._tag_capture(capture_tags, 2, tags, 'natural'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_0889a956, '^(basin|reservoir)$'), mapcss._tag_capture(capture_tags, 3, tags, 'landuse'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_734e4397, '^(yes|stepping_stones)$'), mapcss._tag_capture(capture_tags, 4, tags, 'ford'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boat')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'natural') != mapcss._value_const_capture(capture_tags, 2, 'water', 'water')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_0889a956, '^(basin|reservoir)$'), mapcss._tag_capture(capture_tags, 3, tags, 'landuse'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'ford') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1547975047, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.tag}'))})

        # *[snowplowing][!highway][!amenity][!leisure]
        if ('snowplowing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'snowplowing')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'amenity')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'leisure')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.key}")
                err.append({'class': 9001001, 'subclass': 585636657, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{3.key}'))})

        # *[toll][!highway][!barrier][route!~/^(ferry|road)$/]
        if ('toll' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toll')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'barrier')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_5ee853b2, '^(ferry|road)$'), mapcss._tag_capture(capture_tags, 3, tags, 'route'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1689494174, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

        # *[amenity=marketplace][highway]
        # *[power=plant][/^generator:/]
        # *[power=generator][/^plant:/]
        # *[power=plant][voltage]
        # *[power=plant][frequency]
        # *[internet_access=no][internet_access:fee]
        # node[power=transformer][voltage]
        # node[transformer=distribution][voltage][power=pole]
        # *[amenity=vending_machine][shop]
        # *[noname?][name]
        # *[noref?][ref]
        # *[nohousenumber?][addr:housenumber]
        # *[actuator][handle][actuator!~/(^|;)manual(;|$)/]
        # *[mechanical_driver][handle][mechanical_driver!~/(^|;)manual(;|$)/]
        if ('actuator' in keys and 'handle' in keys) or ('addr:housenumber' in keys and 'nohousenumber' in keys) or ('amenity' in keys and 'highway' in keys) or ('amenity' in keys and 'shop' in keys) or ('frequency' in keys and 'power' in keys) or ('handle' in keys and 'mechanical_driver' in keys) or ('internet_access' in keys and 'internet_access:fee' in keys) or ('name' in keys and 'noname' in keys) or ('noref' in keys and 'ref' in keys) or ('power' in keys) or ('power' in keys and 'transformer' in keys and 'voltage' in keys) or ('power' in keys and 'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'marketplace')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_503776bb)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'generator')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_3b1153a4)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, 'frequency')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'internet_access') == mapcss._value_capture(capture_tags, 0, 'no')) and (mapcss._tag_capture(capture_tags, 1, tags, 'internet_access:fee')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'transformer')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'transformer') == mapcss._value_capture(capture_tags, 0, 'distribution')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')) and (mapcss._tag_capture(capture_tags, 2, tags, 'power') == mapcss._value_capture(capture_tags, 2, 'pole')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'vending_machine')) and (mapcss._tag_capture(capture_tags, 1, tags, 'shop')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noname') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noref') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'nohousenumber') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'actuator')) and (mapcss._tag_capture(capture_tags, 1, tags, 'handle')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_78efbab0, '(^|;)manual(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'actuator'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mechanical_driver')) and (mapcss._tag_capture(capture_tags, 1, tags, 'handle')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_78efbab0, '(^|;)manual(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.key}")
                err.append({'class': 9001002, 'subclass': 778725600, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[barrier=kerb][kerb=no]
        # *[man_made=bridge][bridge=yes]
        # *[man_made=tunnel][tunnel=yes]
        # *[amenity=police][police]
        # node[highway=crossing][crossing=no]
        # node[railway=crossing][crossing=no]
        if ('amenity' in keys and 'police' in keys) or ('barrier' in keys and 'kerb' in keys) or ('bridge' in keys and 'man_made' in keys) or ('crossing' in keys and 'highway' in keys) or ('crossing' in keys and 'railway' in keys) or ('man_made' in keys and 'tunnel' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'kerb')) and (mapcss._tag_capture(capture_tags, 1, tags, 'kerb') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'bridge')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'tunnel')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tunnel') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'police')) and (mapcss._tag_capture(capture_tags, 1, tags, 'police')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'crossing')) and (mapcss._tag_capture(capture_tags, 1, tags, 'crossing') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'crossing')) and (mapcss._tag_capture(capture_tags, 1, tags, 'crossing') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 2109026588, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[transformer][voltage]
        # node[marker][cover]
        # node[marker][voltage]
        # node[marker][pressure]
        # node[marker][diameter]
        # node[marker][substance]
        # *[building:part][building]
        # *[addr:street][addr:place][outside("CZ,DK")]
        if ('addr:place' in keys and 'addr:street' in keys) or ('building' in keys and 'building:part' in keys) or ('cover' in keys and 'marker' in keys) or ('diameter' in keys and 'marker' in keys) or ('marker' in keys and 'pressure' in keys) or ('marker' in keys and 'substance' in keys) or ('marker' in keys and 'voltage' in keys) or ('transformer' in keys and 'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'transformer')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'marker')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cover')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'marker')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'marker')) and (mapcss._tag_capture(capture_tags, 1, tags, 'pressure')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'marker')) and (mapcss._tag_capture(capture_tags, 1, tags, 'diameter')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'marker')) and (mapcss._tag_capture(capture_tags, 1, tags, 'substance')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:place')) and (mapcss.outside(self.father.config.options, 'CZ,DK')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1424906562, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # node[access][eval(number_of_tags())=1]
        # node[area][eval(number_of_tags())=1]!.area_yes_autofix
        # node[lanes][eval(number_of_tags())=1]
        # node[layer][eval(number_of_tags())=1]
        # node[lit][eval(number_of_tags())=1]
        # node[name][eval(number_of_tags())=1]
        # node[ref][eval(number_of_tags())=1]
        # node[surface][eval(number_of_tags())=1]
        if ('access' in keys) or ('area' in keys) or ('lanes' in keys) or ('layer' in keys) or ('lit' in keys) or ('name' in keys) or ('ref' in keys) or ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            # Skip selector using undeclared class area_yes_autofix
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lanes')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'layer')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lit')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if match:
                # set only_one_tag
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0}","{0.key}")
                set_only_one_tag = True
                err.append({'class': 9001001, 'subclass': 729897947, 'text': mapcss.tr('incomplete object: only {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # node[name][area][eval(number_of_tags())=2]
        # node[name][ref][eval(number_of_tags())=2]
        if ('area' in keys and 'name' in keys) or ('name' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'area')) and (len(tags) == 2))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'ref')) and (len(tags) == 2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1930775280, 'text': mapcss.tr('incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # node[tourism=attraction][eval(number_of_tags())=1]
        if ('tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tourism') == mapcss._value_capture(capture_tags, 0, 'attraction')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0}","{0.tag}")
                err.append({'class': 9001001, 'subclass': 413890824, 'text': mapcss.tr('incomplete object: only {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[name][tourism=attraction][eval(number_of_tags())=2]
        if ('name' in keys and 'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') == mapcss._value_capture(capture_tags, 1, 'attraction')) and (len(tags) == 2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 13522860, 'text': mapcss.tr('incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[place][place!=farm][place!=plot][/^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$/]
        # *[boundary][/^addr:/]
        # *[highway][/^addr:/][highway!=services][highway!=rest_area][!"addr:postcode"]
        if ('boundary' in keys) or ('highway' in keys) or ('place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place') != mapcss._value_const_capture(capture_tags, 1, 'farm', 'farm')) and (mapcss._tag_capture(capture_tags, 2, tags, 'place') != mapcss._value_const_capture(capture_tags, 2, 'plot', 'plot')) and (mapcss._tag_capture(capture_tags, 3, tags, self.re_0737b0c4)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'services', 'services')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'rest_area', 'rest_area')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","addr:*")
                # assertNoMatch:"node place=foo  addr:postcode=12345"
                # assertMatch:"node place=foo addr:housenumber=5 addr:postcode=12345"
                # assertMatch:"node place=foo addr:housenumber=5"
                err.append({'class': 9001002, 'subclass': 1053814004, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'addr:*')})

        # *[postal_code]["addr:postcode"][!highway][postal_code=*"addr:postcode"]
        if ('addr:postcode' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 731431309, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[postal_code]["addr:postcode"][!highway][postal_code!=*"addr:postcode"]
        if ('addr:postcode' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 433558919, 'text': mapcss.tr('{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # node[lanes][!barrier][!ford][highway!=mini_roundabout][!junction][leisure!~/^(bowling_alley|slipway|swimming_pool|track)$/][!traffic_calming]!.only_one_tag
        # *[tunnel][!highway][!area:highway][!railway][!waterway][!piste:type][type!=tunnel][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=wildlife_crossing][man_made!=tunnel][power!=cable]!.TunnelCulvertWithoutWaterway
        # *[bridge][!highway][!area:highway][!railway][!waterway][!piste:type][type!=bridge][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=wildlife_crossing][man_made!=bridge][building!=bridge]
        # *[psv][!highway][!area:highway][!railway][!waterway][barrier!~/^(bollard|bump_gate|bus_trap|cattle_grid|chain|coupure|entrance|gate|height_restrictor|jersey_barrier|kerb|lift_gate|rope|sally_port|sliding_beam|sliding_gate|spikes|swing_gate|toll_booth|yes)$/][amenity!~/^parking.*/]
        # *[width][!highway][!area:highway][!railway][!waterway][!aeroway][!cycleway][!footway][!barrier][!man_made][!entrance][natural!=stone][leisure!=track]
        # *[maxspeed][!highway][!area:highway][!railway][traffic_sign!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][traffic_sign:forward!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][traffic_sign:backward!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][type!=enforcement][waterway!~/^(canal|fairway|lock|river|tidal_channel)$/][!traffic_calming][aerialway!=zip_line]
        if ('bridge' in keys) or ('lanes' in keys) or ('maxspeed' in keys) or ('psv' in keys) or ('tunnel' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_only_one_tag) and (mapcss._tag_capture(capture_tags, 0, tags, 'lanes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'barrier')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'ford')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'mini_roundabout', 'mini_roundabout')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'junction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_49fc2c26, '^(bowling_alley|slipway|swimming_pool|track)$'), mapcss._tag_capture(capture_tags, 5, tags, 'leisure'))) and (not mapcss._tag_capture(capture_tags, 6, tags, 'traffic_calming')))
                except mapcss.RuleAbort: pass
            # Skip selector using undeclared class TunnelCulvertWithoutWaterway
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 6, tags, 'type') != mapcss._value_const_capture(capture_tags, 6, 'bridge', 'bridge')) and (mapcss._tag_capture(capture_tags, 7, tags, 'public_transport') != mapcss._value_const_capture(capture_tags, 7, 'platform', 'platform')) and (mapcss._tag_capture(capture_tags, 8, tags, 'route') != mapcss._value_const_capture(capture_tags, 8, 'ferry', 'ferry')) and (mapcss._tag_capture(capture_tags, 9, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 9, 'pipeline', 'pipeline')) and (mapcss._tag_capture(capture_tags, 10, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 10, 'goods_conveyor', 'goods_conveyor')) and (mapcss._tag_capture(capture_tags, 11, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 11, 'wildlife_crossing', 'wildlife_crossing')) and (mapcss._tag_capture(capture_tags, 12, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 12, 'bridge', 'bridge')) and (mapcss._tag_capture(capture_tags, 13, tags, 'building') != mapcss._value_const_capture(capture_tags, 13, 'bridge', 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'psv')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_33560b51, '^(bollard|bump_gate|bus_trap|cattle_grid|chain|coupure|entrance|gate|height_restrictor|jersey_barrier|kerb|lift_gate|rope|sally_port|sliding_beam|sliding_gate|spikes|swing_gate|toll_booth|yes)$'), mapcss._tag_capture(capture_tags, 5, tags, 'barrier'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_213d4d09, '^parking.*'), mapcss._tag_capture(capture_tags, 6, tags, 'amenity'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'aeroway')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'footway')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'barrier')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'man_made')) and (not mapcss._tag_capture(capture_tags, 10, tags, 'entrance')) and (mapcss._tag_capture(capture_tags, 11, tags, 'natural') != mapcss._value_const_capture(capture_tags, 11, 'stone', 'stone')) and (mapcss._tag_capture(capture_tags, 12, tags, 'leisure') != mapcss._value_const_capture(capture_tags, 12, 'track', 'track')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 4, tags, 'traffic_sign'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 5, tags, 'traffic_sign:forward'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 6, tags, 'traffic_sign:backward'))) and (mapcss._tag_capture(capture_tags, 7, tags, 'type') != mapcss._value_const_capture(capture_tags, 7, 'enforcement', 'enforcement')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 8, self.re_2fc1bb0a, '^(canal|fairway|lock|river|tidal_channel)$'), mapcss._tag_capture(capture_tags, 8, tags, 'waterway'))) and (not mapcss._tag_capture(capture_tags, 9, tags, 'traffic_calming')) and (mapcss._tag_capture(capture_tags, 10, tags, 'aerialway') != mapcss._value_const_capture(capture_tags, 10, 'zip_line', 'zip_line')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} on suspicious object","{0.key}")
                err.append({'class': 9001002, 'subclass': 1211215386, 'text': mapcss.tr('{0} on suspicious object', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[highway][waterway][waterway!=dam][waterway!=weir]
        # *[landuse][building][landuse!=retail]
        if ('building' in keys and 'landuse' in keys) or ('highway' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 2, 'dam', 'dam')) and (mapcss._tag_capture(capture_tags, 3, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 3, 'weir', 'weir')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (mapcss._tag_capture(capture_tags, 2, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 2, 'retail', 'retail')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # assertNoMatch:"node highway=street_lamp natural=birds_nest"
                err.append({'class': 9001002, 'subclass': 1750941961, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[natural=water][leisure=swimming_pool]
        if ('leisure' in keys and 'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'water')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'swimming_pool')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("natural water used for swimming pool")
                # fixRemove:"natural"
                err.append({'class': 9001002, 'subclass': 608817213, 'text': mapcss.tr('natural water used for swimming pool'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'natural'])
                }})

        # *[sport][sport!=skiing][!building][!"building:part"][!club][tourism!=hotel][highway!~/^(pedestrian|raceway)$/][!leisure][natural!~/^(beach|bare_rock|cliff|peak|water)$/][amenity!~/^(bar|dojo|pub|restaurant|swimming_pool)$/][landuse!~/^(recreation_ground|piste|farm|farmland)$/][barrier!~/^(wall|retaining_wall)$/][!"piste:type"][shop!=sports][attraction!=summer_toboggan]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sport') != mapcss._value_const_capture(capture_tags, 1, 'skiing', 'skiing')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'building:part')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'club')) and (mapcss._tag_capture(capture_tags, 5, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 5, 'hotel', 'hotel')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_5dd46ebe, '^(pedestrian|raceway)$'), mapcss._tag_capture(capture_tags, 6, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 7, tags, 'leisure')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 8, self.re_29fa4401, '^(beach|bare_rock|cliff|peak|water)$'), mapcss._tag_capture(capture_tags, 8, tags, 'natural'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 9, self.re_41650b2e, '^(bar|dojo|pub|restaurant|swimming_pool)$'), mapcss._tag_capture(capture_tags, 9, tags, 'amenity'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 10, self.re_3b4f8f73, '^(recreation_ground|piste|farm|farmland)$'), mapcss._tag_capture(capture_tags, 10, tags, 'landuse'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 11, self.re_68c05e86, '^(wall|retaining_wall)$'), mapcss._tag_capture(capture_tags, 11, tags, 'barrier'))) and (not mapcss._tag_capture(capture_tags, 12, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 13, tags, 'shop') != mapcss._value_const_capture(capture_tags, 13, 'sports', 'sports')) and (mapcss._tag_capture(capture_tags, 14, tags, 'attraction') != mapcss._value_const_capture(capture_tags, 14, 'summer_toboggan', 'summer_toboggan')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("sport without physical feature")
                # assertNoMatch:"node sport=10pin amenity=restaurant"
                # assertNoMatch:"node sport=beachvolleyball natural=beach"
                # assertNoMatch:"node sport=boxing building:part=yes"
                # assertNoMatch:"node sport=skiing"
                # assertNoMatch:"node sport=swimming tourism=hotel"
                # assertNoMatch:"node sport=tennis leisure=pitch"
                # assertMatch:"node sport=tennis"
                err.append({'class': 9001001, 'subclass': 1738767711, 'text': mapcss.tr('sport without physical feature')})

        # *[building:levels][!building][!building:part]
        if ('building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:levels')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'building:part')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001001, 'subclass': 1821512557, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *[/_name$/][!name][!old_name][!loc_name][!reg_name][!uic_name][!artist_name][!lock_name][!"osak:municipality_name"][!"osak:street_name"][NHD:subbasin_name!~/^(Des Moines Headwaters|Upper Des Moines|East Fork Des Moines)$/][noname!=yes]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_25d98c90)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'old_name')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'loc_name')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'reg_name')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'uic_name')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'artist_name')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'lock_name')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'osak:municipality_name')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'osak:street_name')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 10, self.re_51b15093, '^(Des Moines Headwaters|Upper Des Moines|East Fork Des Moines)$'), mapcss._tag_capture(capture_tags, 10, tags, 'NHD:subbasin_name'))) and (mapcss._tag_capture(capture_tags, 11, tags, 'noname') != mapcss._value_const_capture(capture_tags, 11, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("alternative name without {0}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1822630838, 'text': mapcss.tr('alternative name without {0}', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # node[leisure=park][natural=tree]
        if ('leisure' in keys and 'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'park')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'tree')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} on a node. Remove {0}.","{0.tag}","{1.tag}")
                # fixRemove:"leisure"
                err.append({'class': 9001002, 'subclass': 1715941543, 'text': mapcss.tr('{0} together with {1} on a node. Remove {0}.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'leisure'])
                }})

        # *[highway=cycleway][cycleway=track]
        if ('cycleway' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway') == mapcss._value_capture(capture_tags, 1, 'track')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Remove {1}.","{0.tag}","{1.tag}")
                # fixRemove:"cycleway"
                err.append({'class': 9001002, 'subclass': 563138279, 'text': mapcss.tr('{0} together with {1}. Remove {1}.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'cycleway'])
                }})

        # node[emergency_ward_entrance][emergency!=emergency_ward_entrance]
        if ('emergency_ward_entrance' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'emergency_ward_entrance')) and (mapcss._tag_capture(capture_tags, 1, tags, 'emergency') != mapcss._value_const_capture(capture_tags, 1, 'emergency_ward_entrance', 'emergency_ward_entrance')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # fixAdd:"emergency=emergency_ward_entrance"
                err.append({'class': 9001001, 'subclass': 1567634001, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['emergency','emergency_ward_entrance']])
                }})

        # *[construction:building][!building][!construction]
        # *[construction:highway][!highway][!construction]
        # *[construction:railway][!railway][!construction]
        # *[construction:landuse][!landuse][!construction]
        if ('construction:building' in keys) or ('construction:highway' in keys) or ('construction:landuse' in keys) or ('construction:railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} and {2}","{0.key}","{1.key}","{2.key}")
                # fixAdd:"construction={0.value}"
                # fixAdd:"{1.key}=construction"
                err.append({'class': 9001001, 'subclass': 1239539337, 'text': mapcss.tr('{0} without {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, 'construction={0.value}')).split('=', 1),
                    (mapcss._tag_uncapture(capture_tags, '{1.key}=construction')).split('=', 1)])
                }})

        # *[building=construction]["construction:building"][!construction]
        # *[highway=construction]["construction:highway"][!construction]
        # *[railway=construction]["construction:railway"][!construction]
        # *[landuse=construction]["construction:landuse"][!construction]
        if ('building' in keys and 'construction:building' in keys) or ('construction:highway' in keys and 'highway' in keys) or ('construction:landuse' in keys and 'landuse' in keys) or ('construction:railway' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} together with {1} but without {2}","{0.key}","{1.key}","{2.key}")
                # fixAdd:"construction={1.value}"
                err.append({'class': 9001001, 'subclass': 855187849, 'text': mapcss.tr('{0} together with {1} but without {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, 'construction={1.value}')).split('=', 1)])
                }})

        # *[building]["construction:building"][!construction][building!=construction]
        # *[highway]["construction:highway"][!construction][highway!=construction]
        # *[railway]["construction:railway"][!construction][railway!=construction]
        # *[landuse]["construction:landuse"][!construction][landuse!=construction]
        if ('building' in keys and 'construction:building' in keys) or ('construction:highway' in keys and 'highway' in keys) or ('construction:landuse' in keys and 'landuse' in keys) or ('construction:railway' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values plus no {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 164864338, 'text': mapcss.tr('{0} together with {1} and conflicting values plus no {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *["construction:building"][construction][construction:building!=*construction]
        # *["construction:highway"][construction][construction:highway!=*construction]
        # *["construction:railway"][construction][construction:railway!=*construction]
        # *["construction:landuse"][construction][construction:landuse!=*construction]
        if ('construction' in keys and 'construction:building' in keys) or ('construction' in keys and 'construction:highway' in keys) or ('construction' in keys and 'construction:landuse' in keys) or ('construction' in keys and 'construction:railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:building') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:highway') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:railway') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:landuse') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1971600459, 'text': mapcss.tr('{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[amenity=recycling][collection_times="24/7"][!opening_hours]
        # *[amenity=recycling][collection_times][!opening_hours][collection_times=~/[a-z]-[A-Z].*[0-9]-[0-9]/]
        if ('amenity' in keys and 'collection_times' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'collection_times') == mapcss._value_capture(capture_tags, 1, '24/7')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'collection_times')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_3a43a33d), mapcss._tag_capture(capture_tags, 3, tags, 'collection_times'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Probably {2} is meant.","{1.key}","{0.tag}","{2.key}")
                # fixChangeKey:"collection_times => opening_hours"
                # assertNoMatch:"node amenity=recycling collection_times=\"Mo 08:00-11:00\""
                # assertMatch:"node amenity=recycling collection_times=\"Mo-Fr 06:00-20:00\""
                # assertNoMatch:"node amenity=recycling collection_times=\"Mo-Fr 15:00\""
                # assertNoMatch:"node amenity=recycling collection_times=\"Sa[2,4] 8:00-11:00\""
                err.append({'class': 9001002, 'subclass': 1009884322, 'text': mapcss.tr('{0} together with {1}. Probably {2} is meant.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours', mapcss.tag(tags, 'collection_times')]]),
                    '-': ([
                    'collection_times'])
                }})

        # *[amenity=recycling][!/^recycling:/][recycling_type!=centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_2d1850d1)) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 2, 'centre', 'centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","recycling:*")
                err.append({'class': 9001001, 'subclass': 321354601, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'recycling:*')})

        # *[source:addr][!/^addr:/]
        if ('source:addr' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","addr:*")
                # assertNoMatch:"node source:addr=postman addr:housenumber=42"
                # assertMatch:"node source:addr=postman"
                err.append({'class': 9001001, 'subclass': 886065920, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'addr:*')})

        # *[source:maxspeed][!/^maxspeed:?/]
        if ('source:maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_050395e0)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","maxspeed","maxspeed:*")
                err.append({'class': 9001001, 'subclass': 480030366, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'maxspeed', 'maxspeed:*')})

        # *[man_made=communications_tower][height][siunit_length(tag(height))<75]
        if ('height' in keys and 'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'communications_tower')) and (mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss.siunit_length(mapcss.tag(tags, 'height')) < 75))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"man_made=tower + tower:type=communication + height"
                # assertNoMatch:"node height=4358'"
                # assertMatch:"node man_made=communications_tower height=245'"
                # assertMatch:"node man_made=communications_tower height=\"224.22 ft\""
                # assertNoMatch:"node man_made=communications_tower height=\"328.22 ft\""
                # assertMatch:"node man_made=communications_tower height=\"74 m\""
                # assertNoMatch:"node man_made=communications_tower height=\"75 m\""
                # assertMatch:"node man_made=communications_tower height=0.8"
                # assertMatch:"node man_made=communications_tower height=231'10.22\""
                # assertNoMatch:"node man_made=communications_tower height=4358'8\""
                # assertMatch:"node man_made=communications_tower height=58"
                # assertNoMatch:"node man_made=communications_tower height=75.72"
                err.append({'class': 9001002, 'subclass': 1533608671, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[fixme][count(split(" ",tag("fixme")))==1][has_tag_key(tag("fixme"))]
        # *[FIXME][count(split(" ",tag("FIXME")))==1][has_tag_key(tag("FIXME"))]
        if ('FIXME' in keys) or ('fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fixme')) and (mapcss.count(mapcss.split(' ', mapcss.tag(tags, 'fixme'))) == 1) and (keys.__contains__(mapcss.tag(tags, 'fixme'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'FIXME')) and (mapcss.count(mapcss.split(' ', mapcss.tag(tags, 'FIXME'))) == 1) and (keys.__contains__(mapcss.tag(tags, 'FIXME'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Is the fixme fixed?","{0.tag}","{0.value}")
                err.append({'class': 9001002, 'subclass': 2092275873, 'text': mapcss.tr('{0} together with {1}. Is the fixme fixed?', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # node:righthandtraffic[highway=mini_roundabout][direction=clockwise]
        # Rule Blacklisted (id: 643796350)

        # node!:righthandtraffic[highway=mini_roundabout][direction=anticlockwise]
        # Rule Blacklisted (id: 317760248)

        # *[voltage:primary][voltage:secondary][transformer=generator][tag("voltage:secondary")<tag("voltage:primary")]
        if ('transformer' in keys and 'voltage:primary' in keys and 'voltage:secondary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:primary')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage:secondary')) and (mapcss._tag_capture(capture_tags, 2, tags, 'transformer') == mapcss._value_capture(capture_tags, 2, 'generator')) and (mapcss.tag(tags, 'voltage:secondary') < mapcss.tag(tags, 'voltage:primary')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} is lower than {1} on {2}.","{1.key}","{0.key}","{2.tag}")
                err.append({'class': 9001002, 'subclass': 1175862429, 'text': mapcss.tr('{0} is lower than {1} on {2}.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_AllSameCycleway = set_AllSameMaxspeed = set_AllSameSidewalk = set_MotorwayTrunk = set_PlacementTransitionWarning = set_TunnelCulvertWithoutWaterway = set_fully_paved_surface = set_only_one_tag = set_unpaved_surface = False

        # way[surface=~/^(unpaved|compacted|gravel|fine_gravel|pebblestone|ground|earth|dirt|grass|sand|mud|ice|salt|snow|woodchips)$/]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6f957488), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if match:
                # set unpaved_surface
                set_unpaved_surface = True

        # way[surface=~/^(paved|asphalt|cobblestone|cobblestone:flattened|sett|concrete|concrete:plates|paving_stones|metal|wood|unhewn_cobblestone)$/]
        if ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_01d4d495), mapcss._tag_capture(capture_tags, 0, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if match:
                # set fully_paved_surface
                set_fully_paved_surface = True

        # way[junction][!highway][junction!=yes][!area:highway]
        # way[living_street][!highway]
        # way[maintenance][!highway]
        # way[median][!highway]
        # way[motorroad][!highway]
        # way[sac_scale][!highway]
        # way[sidewalk][!highway]
        # way[step_count][!highway][man_made!=tower]
        # way[tracktype][!highway]
        # way[trail_visibility][!highway]
        # way[trolley_wire][!highway]
        # way[zip_left][!highway]
        # way[zip_right][!highway]
        # way[detail][!railway][route!=railway]
        # way[eddy_current_brake][!railway][route!=railway]
        # way[electrified][!railway][route!=railway][!highway]
        # way[etcs][!railway][route!=railway]
        # way[gauge][!railway][route!=railway]
        # way[grade_of_track][!railway][route!=railway]
        # way[kursbuchstrecke][!railway][route!=railway]
        # way[lzb][!railway][route!=railway]
        # way[old_railway_operator][!railway][route!=railway]
        # way[operating_procedure][!railway][route!=railway]
        # way[pzb][!railway][route!=railway]
        # way[structure_gauge][!railway][route!=railway]
        # way[tilting_technology][!railway][route!=railway]
        # way[track_class][!railway][route!=railway]
        # way[tracks][!railway][route!=railway]
        # way[traffic_mode][!railway][route!=railway]
        # way[workrules][!railway][route!=railway]
        # way[length_unit][!waterway]
        # way[canal][!waterway]
        # way[have_riverbank][!waterway]
        # area[min_height][!height][/^(building|building:part)$/]
        # area[building:min_level][!building:levels][/^(building|building:part)$/]
        # *[border_type][!boundary]
        # *[piste:difficulty][!piste:type]
        # *[place][!name][place!=islet][place!=plot][noname!=yes]
        # *[transformer][!power]
        # *[source:date][!source]
        # *[source:name][!name][noname!=yes]
        # *[source:maxspeed:forward][!maxspeed:forward][!maxspeed]
        # *[source:maxspeed:backward][!maxspeed:backward][!maxspeed]
        # *[source:building][!building]
        # *[source:ref][!ref][noref!=yes]
        # *[source:population][!population]
        # *[source:postal_code][!postal_code]
        # *[source:ele][!ele]
        # *[source:ref:INSEE][!ref:INSEE]
        # *[source:lit][!lit]
        # *[source:hgv][!hgv]
        # *[source:highway][!highway]
        # *[source:maxaxleload][!maxaxleload]
        # *[source:surface][!surface]
        # *[source:bridge][!bridge]
        # *[source:old_name][!old_name]
        # *[source:bicycle][!bicycle]
        # *[source:designation][!designation]
        # *[source:height][!height]
        # *[source:lanes][!lanes]
        # *[source:postcode][!addr:postcode]
        # *[source:housenumber][!addr:housenumber]
        # *[source:addr:postcode][!addr:postcode]
        # *[source:addr:housenumber][!addr:housenumber]
        if ('border_type' in keys) or ('building:min_level' in keys) or ('canal' in keys) or ('detail' in keys) or ('eddy_current_brake' in keys) or ('electrified' in keys) or ('etcs' in keys) or ('gauge' in keys) or ('grade_of_track' in keys) or ('have_riverbank' in keys) or ('junction' in keys) or ('kursbuchstrecke' in keys) or ('length_unit' in keys) or ('living_street' in keys) or ('lzb' in keys) or ('maintenance' in keys) or ('median' in keys) or ('min_height' in keys) or ('motorroad' in keys) or ('old_railway_operator' in keys) or ('operating_procedure' in keys) or ('piste:difficulty' in keys) or ('place' in keys) or ('pzb' in keys) or ('sac_scale' in keys) or ('sidewalk' in keys) or ('source:addr:housenumber' in keys) or ('source:addr:postcode' in keys) or ('source:bicycle' in keys) or ('source:bridge' in keys) or ('source:building' in keys) or ('source:date' in keys) or ('source:designation' in keys) or ('source:ele' in keys) or ('source:height' in keys) or ('source:hgv' in keys) or ('source:highway' in keys) or ('source:housenumber' in keys) or ('source:lanes' in keys) or ('source:lit' in keys) or ('source:maxaxleload' in keys) or ('source:maxspeed:backward' in keys) or ('source:maxspeed:forward' in keys) or ('source:name' in keys) or ('source:old_name' in keys) or ('source:population' in keys) or ('source:postal_code' in keys) or ('source:postcode' in keys) or ('source:ref' in keys) or ('source:ref:INSEE' in keys) or ('source:surface' in keys) or ('step_count' in keys) or ('structure_gauge' in keys) or ('tilting_technology' in keys) or ('track_class' in keys) or ('tracks' in keys) or ('tracktype' in keys) or ('traffic_mode' in keys) or ('trail_visibility' in keys) or ('transformer' in keys) or ('trolley_wire' in keys) or ('workrules' in keys) or ('zip_left' in keys) or ('zip_right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'junction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'junction') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'area:highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'living_street')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maintenance')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'median')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'motorroad')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sac_scale')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'step_count')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'tower', 'tower')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'trail_visibility')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'trolley_wire')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'zip_left')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'zip_right')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'detail')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'eddy_current_brake')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'electrified')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'etcs')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'gauge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'grade_of_track')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'kursbuchstrecke')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lzb')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'old_railway_operator')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'operating_procedure')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pzb')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'structure_gauge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tilting_technology')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'track_class')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracks')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'traffic_mode')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'workrules')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route') != mapcss._value_const_capture(capture_tags, 2, 'railway', 'railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'length_unit')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'canal')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'have_riverbank')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss._tag_capture(capture_tags, 2, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:min_level')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building:levels')) and (mapcss._tag_capture(capture_tags, 2, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'border_type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'boundary')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'piste:difficulty')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'piste:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'place') != mapcss._value_const_capture(capture_tags, 2, 'islet', 'islet')) and (mapcss._tag_capture(capture_tags, 3, tags, 'place') != mapcss._value_const_capture(capture_tags, 3, 'plot', 'plot')) and (mapcss._tag_capture(capture_tags, 4, tags, 'noname') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'transformer')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'power')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:date')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'source')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:name')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noname') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed:forward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:forward')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed:backward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:building')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ref')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noref') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:population')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'population')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:postal_code')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'postal_code')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ele')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ele')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ref:INSEE')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:INSEE')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:lit')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lit')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:hgv')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'hgv')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:highway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxaxleload')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:surface')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'surface')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:bridge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:old_name')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'old_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:bicycle')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'bicycle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:designation')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'designation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:height')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'height')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:lanes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lanes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:postcode')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:housenumber')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr:postcode')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr:housenumber')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1598649795, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[generator:source][power!=generator]
        # *[generator:method][power!=generator]
        # *[generator:type][power!=generator]
        # way[fence_type][barrier!=fence]
        # *[recycling_type][amenity!=recycling]
        # *[information][tourism!=information]
        # *[shelter_type][amenity!=shelter]
        # *[archaeological_site][historic!=archaeological_site]
        # *[artwork_type][tourism!=artwork][exhibit!=artwork]
        # *[castle_type][historic!=castle]
        # *[parking][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking)$/][parking!=yes][parking!=no]
        # way[cutline][man_made!=cutline]
        # *[zoo][tourism!=zoo]
        # *[bunker_type][military!=bunker]
        if ('archaeological_site' in keys) or ('artwork_type' in keys) or ('bunker_type' in keys) or ('castle_type' in keys) or ('cutline' in keys) or ('fence_type' in keys) or ('generator:method' in keys) or ('generator:source' in keys) or ('generator:type' in keys) or ('information' in keys) or ('parking' in keys) or ('recycling_type' in keys) or ('shelter_type' in keys) or ('zoo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:source')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fence_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'barrier') != mapcss._value_const_capture(capture_tags, 1, 'fence', 'fence')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'recycling_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'recycling', 'recycling')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'information')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'information', 'information')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shelter_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'shelter', 'shelter')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'archaeological_site')) and (mapcss._tag_capture(capture_tags, 1, tags, 'historic') != mapcss._value_const_capture(capture_tags, 1, 'archaeological_site', 'archaeological_site')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'artwork_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'artwork', 'artwork')) and (mapcss._tag_capture(capture_tags, 2, tags, 'exhibit') != mapcss._value_const_capture(capture_tags, 2, 'artwork', 'artwork')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'castle_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'historic') != mapcss._value_const_capture(capture_tags, 1, 'castle', 'castle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5cf0a79f, '^(parking|parking_space|parking_entrance|motorcycle_parking)$'), mapcss._tag_capture(capture_tags, 1, tags, 'amenity'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'parking') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cutline')) and (mapcss._tag_capture(capture_tags, 1, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 1, 'cutline', 'cutline')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'zoo')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'zoo', 'zoo')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bunker_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'military') != mapcss._value_const_capture(capture_tags, 1, 'bunker', 'bunker')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1261817376, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[bridge:movable][bridge!=movable][man_made!=bridge]
        # *[substation][power!=substation][pipeline!=substation]
        # *[reservoir_type][landuse!=reservoir][water!=reservoir]
        # way[waterway=pressurised][tunnel!=flooded][man_made!=pipeline]
        if ('bridge:movable' in keys) or ('reservoir_type' in keys) or ('substation' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge:movable')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') != mapcss._value_const_capture(capture_tags, 1, 'movable', 'movable')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'bridge', 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'substation')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'substation', 'substation')) and (mapcss._tag_capture(capture_tags, 2, tags, 'pipeline') != mapcss._value_const_capture(capture_tags, 2, 'substation', 'substation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'reservoir_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 1, 'reservoir', 'reservoir')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'reservoir', 'reservoir')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'pressurised')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tunnel') != mapcss._value_const_capture(capture_tags, 1, 'flooded', 'flooded')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'pipeline', 'pipeline')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 214618643, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[iata][aeroway!=aerodrome][aeroway!=heliport][aeroway!=helipad]
        # *[icao][aeroway!=aerodrome][aeroway!=heliport][aeroway!=helipad]
        if ('iata' in keys) or ('icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'iata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 1, 'aerodrome', 'aerodrome')) and (mapcss._tag_capture(capture_tags, 2, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 2, 'heliport', 'heliport')) and (mapcss._tag_capture(capture_tags, 3, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 3, 'helipad', 'helipad')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'icao')) and (mapcss._tag_capture(capture_tags, 1, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 1, 'aerodrome', 'aerodrome')) and (mapcss._tag_capture(capture_tags, 2, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 2, 'heliport', 'heliport')) and (mapcss._tag_capture(capture_tags, 3, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 3, 'helipad', 'helipad')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.tag}","{2.tag}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1908755652, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

        # *[pump_mechanism][man_made!=pump][man_made!=windpump][man_made!=water_well][man_made!=petroleum_well]
        if ('pump_mechanism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pump_mechanism')) and (mapcss._tag_capture(capture_tags, 1, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 1, 'pump', 'pump')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'windpump', 'windpump')) and (mapcss._tag_capture(capture_tags, 3, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 3, 'water_well', 'water_well')) and (mapcss._tag_capture(capture_tags, 4, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 4, 'petroleum_well', 'petroleum_well')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.tag}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1271875329, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.tag}'))})

        # way[railway=construction][!construction][!construction:railway]
        # way[highway=construction][!construction][!construction:highway]
        # area[building=construction][!construction][!construction:building]
        # area[landuse=construction][!construction][!construction:landuse]
        # *[actuator=manual][!handle]
        # *[mechanical_driver=manual][!handle]
        # way[boundary=administrative][!admin_level]
        # *[tourism=information][!information]
        # *[leisure=pitch][!sport]
        # *[aeroway=terminal][!building]
        # *[office=government][!government]
        # *[power=generator][!generator:source]
        # *[amenity=social_facility][!social_facility]
        # *[amenity=place_of_worship][!religion]
        # *[man_made=tower][!tower:type]
        if ('actuator' in keys) or ('aeroway' in keys) or ('amenity' in keys) or ('boundary' in keys) or ('building' in keys) or ('highway' in keys) or ('landuse' in keys) or ('leisure' in keys) or ('man_made' in keys) or ('mechanical_driver' in keys) or ('office' in keys) or ('power' in keys) or ('railway' in keys) or ('tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction:railway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction:highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'construction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction:building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'construction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction:landuse')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'actuator') == mapcss._value_capture(capture_tags, 0, 'manual')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'handle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mechanical_driver') == mapcss._value_capture(capture_tags, 0, 'manual')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'handle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary') == mapcss._value_capture(capture_tags, 0, 'administrative')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'admin_level')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tourism') == mapcss._value_capture(capture_tags, 0, 'information')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'information')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'pitch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'terminal')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'office') == mapcss._value_capture(capture_tags, 0, 'government')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'government')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'generator')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'generator:source')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'social_facility')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'social_facility')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'place_of_worship')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'religion')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'tower')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'tower:type')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1166107880, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[bridge:structure][!bridge][man_made!=bridge]
        # *[segregated][!highway][railway!=crossing]
        if ('bridge:structure' in keys) or ('segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge:structure')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'bridge')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'bridge', 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'segregated')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway') != mapcss._value_const_capture(capture_tags, 2, 'crossing', 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1408612243, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[tunnel=culvert][man_made!=tunnel][!waterway]
        if ('tunnel' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tunnel') == mapcss._value_capture(capture_tags, 0, 'culvert')) and (mapcss._tag_capture(capture_tags, 1, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 1, 'tunnel', 'tunnel')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if match:
                # set TunnelCulvertWithoutWaterway
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","{1.tag}","{2.key}")
                set_TunnelCulvertWithoutWaterway = True
                err.append({'class': 9001002, 'subclass': 633859539, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[usage=penstock][man_made!=pipeline]
        # way[usage=penstock][waterway!=pressurised]
        if ('usage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'usage') == mapcss._value_capture(capture_tags, 0, 'penstock')) and (mapcss._tag_capture(capture_tags, 1, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 1, 'pipeline', 'pipeline')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'usage') == mapcss._value_capture(capture_tags, 0, 'penstock')) and (mapcss._tag_capture(capture_tags, 1, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 1, 'pressurised', 'pressurised')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 758205383, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[amenity=recycling][recycling_type!=container][recycling_type!=centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'container', 'container')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 2, 'centre', 'centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 747056792, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[smoothness][!highway][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$/][barrier!=kerb][!kerb]
        if ('smoothness' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'smoothness')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_4f156c8f, '^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$'), mapcss._tag_capture(capture_tags, 2, tags, 'amenity'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'barrier') != mapcss._value_const_capture(capture_tags, 3, 'kerb', 'kerb')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.key}")
                err.append({'class': 9001001, 'subclass': 1922079652, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.key}'))})

        # *[intermittent][!waterway][natural!~/^(water|spring)$/][landuse!~/^(basin|reservoir)$/][ford!~/^(yes|stepping_stones)$/]
        # *[boat][!waterway][natural!=water][landuse!~/^(basin|reservoir)$/][ford!=yes]
        if ('boat' in keys) or ('intermittent' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'intermittent')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_4fbfe59b, '^(water|spring)$'), mapcss._tag_capture(capture_tags, 2, tags, 'natural'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_0889a956, '^(basin|reservoir)$'), mapcss._tag_capture(capture_tags, 3, tags, 'landuse'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_734e4397, '^(yes|stepping_stones)$'), mapcss._tag_capture(capture_tags, 4, tags, 'ford'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boat')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'natural') != mapcss._value_const_capture(capture_tags, 2, 'water', 'water')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_0889a956, '^(basin|reservoir)$'), mapcss._tag_capture(capture_tags, 3, tags, 'landuse'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'ford') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1547975047, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.tag}'))})

        # *[snowplowing][!highway][!amenity][!leisure]
        if ('snowplowing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'snowplowing')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'amenity')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'leisure')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.key}")
                err.append({'class': 9001001, 'subclass': 585636657, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{3.key}'))})

        # *[toll][!highway][!barrier][route!~/^(ferry|road)$/]
        if ('toll' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toll')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'barrier')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_5ee853b2, '^(ferry|road)$'), mapcss._tag_capture(capture_tags, 3, tags, 'route'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1689494174, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

        # *[amenity=marketplace][highway]
        # *[power=plant][/^generator:/]
        # *[power=generator][/^plant:/]
        # *[power=plant][voltage]
        # *[power=plant][frequency]
        # *[internet_access=no][internet_access:fee]
        # *[amenity=vending_machine][shop]
        # *[noname?][name]
        # *[noref?][ref]
        # *[nohousenumber?][addr:housenumber]
        # *[actuator][handle][actuator!~/(^|;)manual(;|$)/]
        # *[mechanical_driver][handle][mechanical_driver!~/(^|;)manual(;|$)/]
        # way[oneway?][/:backward/][!traffic_sign:backward][bicycle:backward!=use_sidepath][/^oneway:(bicycle|bus|mofa|moped|psv)$/!~/^no$/][!/^oneway:(.+:)?conditional$/]
        # way[oneway?][/:forward/][!traffic_sign:forward][bicycle:forward!=use_sidepath][/^oneway:(bicycle|bus|mofa|moped|psv)$/!~/^no$/][!/^oneway:(.+:)?conditional$/]
        # way[oneway=-1][/:backward/][!traffic_sign:backward][bicycle:backward!=use_sidepath][/^oneway:(bicycle|bus|mofa|moped|psv)$/!~/^no$/][!/^oneway:(.+:)?conditional$/]
        # way[oneway=-1][/:forward/][!traffic_sign:forward][bicycle:forward!=use_sidepath][/^oneway:(bicycle|bus|mofa|moped|psv)$/!~/^no$/][!/^oneway:(.+:)?conditional$/]
        if ('actuator' in keys and 'handle' in keys) or ('addr:housenumber' in keys and 'nohousenumber' in keys) or ('amenity' in keys and 'highway' in keys) or ('amenity' in keys and 'shop' in keys) or ('frequency' in keys and 'power' in keys) or ('handle' in keys and 'mechanical_driver' in keys) or ('internet_access' in keys and 'internet_access:fee' in keys) or ('name' in keys and 'noname' in keys) or ('noref' in keys and 'ref' in keys) or ('oneway' in keys) or ('power' in keys) or ('power' in keys and 'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'marketplace')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_503776bb)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'generator')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_3b1153a4)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, 'frequency')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'internet_access') == mapcss._value_capture(capture_tags, 0, 'no')) and (mapcss._tag_capture(capture_tags, 1, tags, 'internet_access:fee')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'vending_machine')) and (mapcss._tag_capture(capture_tags, 1, tags, 'shop')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noname') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noref') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'nohousenumber') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'actuator')) and (mapcss._tag_capture(capture_tags, 1, tags, 'handle')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_78efbab0, '(^|;)manual(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'actuator'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mechanical_driver')) and (mapcss._tag_capture(capture_tags, 1, tags, 'handle')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_78efbab0, '(^|;)manual(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_7346b495)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:backward')) and (mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:backward') != mapcss._value_const_capture(capture_tags, 3, 'use_sidepath', 'use_sidepath')) and (not mapcss.regexp_test(self.re_19e33301, mapcss._match_regex(tags, self.re_22985ce9))) and (not mapcss._tag_capture(capture_tags, 5, tags, self.re_333281f7)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_12ce6b85)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:forward')) and (mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:forward') != mapcss._value_const_capture(capture_tags, 3, 'use_sidepath', 'use_sidepath')) and (not mapcss.regexp_test(self.re_19e33301, mapcss._match_regex(tags, self.re_22985ce9))) and (not mapcss._tag_capture(capture_tags, 5, tags, self.re_333281f7)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') == mapcss._value_capture(capture_tags, 0, -1)) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_7346b495)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:backward')) and (mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:backward') != mapcss._value_const_capture(capture_tags, 3, 'use_sidepath', 'use_sidepath')) and (not mapcss.regexp_test(self.re_19e33301, mapcss._match_regex(tags, self.re_22985ce9))) and (not mapcss._tag_capture(capture_tags, 5, tags, self.re_333281f7)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') == mapcss._value_capture(capture_tags, 0, -1)) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_12ce6b85)) and (not mapcss._tag_capture(capture_tags, 2, tags, 'traffic_sign:forward')) and (mapcss._tag_capture(capture_tags, 3, tags, 'bicycle:forward') != mapcss._value_const_capture(capture_tags, 3, 'use_sidepath', 'use_sidepath')) and (not mapcss.regexp_test(self.re_19e33301, mapcss._match_regex(tags, self.re_22985ce9))) and (not mapcss._tag_capture(capture_tags, 5, tags, self.re_333281f7)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.key}")
                # assertNoMatch:"way oneway=-1 bicycle:forward=destination oneway:bicycle=no"
                # assertNoMatch:"way oneway=yes bicycle:backward:conditional=\"yes @ (Mo-Fr)\" oneway:bicycle:conditional=\"no @ (Mo-Fr)\""
                # assertNoMatch:"way oneway=yes bicycle:backward=destination oneway:bicycle=no"
                # assertMatch:"way oneway=yes bicycle:backward=destination"
                # assertMatch:"way power=generator plant:source=combustion"
                # assertMatch:"way power=plant generator:source=wind"
                err.append({'class': 9001002, 'subclass': 1751419774, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[barrier=kerb][kerb=no]
        # way[highway=construction][construction][construction=~/^(yes|minor|no)$/]
        # way[railway=construction][construction][construction=~/^(yes|minor|no)$/]
        # area[building=construction][construction][construction=~/^(yes|minor|no)$/]
        # area[landuse=construction][construction][construction=~/^(yes|minor|no)$/]
        # *[man_made=bridge][bridge=yes]
        # *[man_made=tunnel][tunnel=yes]
        # *[amenity=police][police]
        # way[junction=yes][highway]
        # way[tracktype=grade1][surface].unpaved_surface
        # way[tracktype=grade2][surface][surface=~/^(sand|mud|ground|earth|dirt|grass|ice|salt|snow|woodchips)$/]
        # way[tracktype=grade4][surface].fully_paved_surface
        # way[tracktype=grade5][surface].fully_paved_surface
        # way[segregated][bicycle=no]
        # way[segregated][foot=no]
        # way[man_made=pipeline][tunnel=flooded]
        if ('amenity' in keys and 'police' in keys) or ('barrier' in keys and 'kerb' in keys) or ('bicycle' in keys and 'segregated' in keys) or ('bridge' in keys and 'man_made' in keys) or ('building' in keys and 'construction' in keys) or ('construction' in keys and 'highway' in keys) or ('construction' in keys and 'landuse' in keys) or ('construction' in keys and 'railway' in keys) or ('foot' in keys and 'segregated' in keys) or ('highway' in keys and 'junction' in keys) or ('man_made' in keys and 'tunnel' in keys) or ('surface' in keys and 'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'kerb')) and (mapcss._tag_capture(capture_tags, 1, tags, 'kerb') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_06b82725), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_06b82725), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_06b82725), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_06b82725), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'bridge')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'tunnel')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tunnel') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'police')) and (mapcss._tag_capture(capture_tags, 1, tags, 'police')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'junction') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_unpaved_surface) and (mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 'grade1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 'grade2')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_382feae2), mapcss._tag_capture(capture_tags, 2, tags, 'surface'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_fully_paved_surface) and (mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 'grade4')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_fully_paved_surface) and (mapcss._tag_capture(capture_tags, 0, tags, 'tracktype') == mapcss._value_capture(capture_tags, 0, 'grade5')) and (mapcss._tag_capture(capture_tags, 1, tags, 'surface')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'segregated')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bicycle') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'segregated')) and (mapcss._tag_capture(capture_tags, 1, tags, 'foot') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'pipeline')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tunnel') == mapcss._value_capture(capture_tags, 1, 'flooded')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1936513938, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[building:part][building]
        # *[addr:street][addr:place][outside("CZ,DK")]
        if ('addr:place' in keys and 'addr:street' in keys) or ('building' in keys and 'building:part' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:place')) and (mapcss.outside(self.father.config.options, 'CZ,DK')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1590654104, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[highway=~/^(cycleway|footway|path)$/][segregated=no][sidewalk=~/^(left|right|both)$/]
        if ('highway' in keys and 'segregated' in keys and 'sidewalk' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53cf0b2e), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'segregated') == mapcss._value_capture(capture_tags, 1, 'no')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_1bc43c40), mapcss._tag_capture(capture_tags, 2, tags, 'sidewalk'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and {2}","{0.tag}","{1.tag}","{2.key}")
                err.append({'class': 9001002, 'subclass': 340416718, 'text': mapcss.tr('{0} together with {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[railway][electrified=no][frequency]
        # way[railway][electrified=no][voltage]
        if ('electrified' in keys and 'frequency' in keys and 'railway' in keys) or ('electrified' in keys and 'railway' in keys and 'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'electrified') == mapcss._value_capture(capture_tags, 1, 'no')) and (mapcss._tag_capture(capture_tags, 2, tags, 'frequency')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'electrified') == mapcss._value_capture(capture_tags, 1, 'no')) and (mapcss._tag_capture(capture_tags, 2, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and {2}","{0.key}","{1.tag}","{2.key}")
                err.append({'class': 9001002, 'subclass': 154935939, 'text': mapcss.tr('{0} together with {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[waterway][bridge=yes][waterway!=weir]
        if ('bridge' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 2, 'weir', 'weir')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.tag}")
                # suggestAlternative:"bridge=aqueduct"
                # fixAdd:"bridge=aqueduct"
                err.append({'class': 9001002, 'subclass': 1036780075, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['bridge','aqueduct']])
                }})

        # way[waterway=weir][bridge=yes][highway]
        if ('bridge' in keys and 'highway' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'weir')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') == mapcss._value_capture(capture_tags, 1, 'yes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # suggestAlternative:tr("two objects, one with {0} and one with {1} + {2} + {3}","{0.tag}","{2.key}","{1.tag}","layer")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"waterway=dam"
                # suggestAlternative:"waterway=weir + ford=yes"
                err.append({'class': 9001002, 'subclass': 842989092, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[access][eval(number_of_tags())=1]
        # way[area][eval(number_of_tags())=1]!.area_yes_autofix
        # way[lanes][eval(number_of_tags())=1]
        # way[layer][eval(number_of_tags())=1]
        # way[level][eval(number_of_tags())=1]
        # way[lit][eval(number_of_tags())=1]
        # way[name][eval(number_of_tags())=1]
        # way[ref][eval(number_of_tags())=1]
        # way[surface][eval(number_of_tags())=1]
        if ('access' in keys) or ('area' in keys) or ('lanes' in keys) or ('layer' in keys) or ('level' in keys) or ('lit' in keys) or ('name' in keys) or ('ref' in keys) or ('surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'access')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            # Skip selector using undeclared class area_yes_autofix
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lanes')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'layer')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'level')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lit')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'surface')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if match:
                # set only_one_tag
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0}","{0.key}")
                set_only_one_tag = True
                err.append({'class': 9001001, 'subclass': 396232069, 'text': mapcss.tr('incomplete object: only {0}', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[name][area][eval(number_of_tags())=2]
        # way[name][ref][eval(number_of_tags())=2]
        if ('area' in keys and 'name' in keys) or ('name' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'area')) and (len(tags) == 2))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'ref')) and (len(tags) == 2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 24958270, 'text': mapcss.tr('incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[tourism=attraction][eval(number_of_tags())=1]
        if ('tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tourism') == mapcss._value_capture(capture_tags, 0, 'attraction')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0}","{0.tag}")
                err.append({'class': 9001001, 'subclass': 557203641, 'text': mapcss.tr('incomplete object: only {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[name][tourism=attraction][eval(number_of_tags())=2]
        if ('name' in keys and 'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') == mapcss._value_capture(capture_tags, 1, 'attraction')) and (len(tags) == 2))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1755320367, 'text': mapcss.tr('incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[place][place!=farm][place!=plot][/^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$/]
        # *[boundary][/^addr:/]
        # *[highway][/^addr:/][highway!=services][highway!=rest_area][!"addr:postcode"]
        if ('boundary' in keys) or ('highway' in keys) or ('place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place') != mapcss._value_const_capture(capture_tags, 1, 'farm', 'farm')) and (mapcss._tag_capture(capture_tags, 2, tags, 'place') != mapcss._value_const_capture(capture_tags, 2, 'plot', 'plot')) and (mapcss._tag_capture(capture_tags, 3, tags, self.re_0737b0c4)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'services', 'services')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'rest_area', 'rest_area')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","addr:*")
                err.append({'class': 9001002, 'subclass': 1053814004, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'addr:*')})

        # *[postal_code]["addr:postcode"][!highway][postal_code=*"addr:postcode"]
        if ('addr:postcode' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 731431309, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[postal_code]["addr:postcode"][!highway][postal_code!=*"addr:postcode"]
        if ('addr:postcode' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 433558919, 'text': mapcss.tr('{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[postal_code]["addr:postcode"][highway][postal_code=*"addr:postcode"]
        if ('addr:postcode' in keys and 'highway' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # fixRemove:"addr:postcode"
                err.append({'class': 9001002, 'subclass': 1131045488, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'addr:postcode'])
                }})

        # way[postal_code]["addr:postcode"][highway][postal_code!=*"addr:postcode"]
        if ('addr:postcode' in keys and 'highway' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 724652011, 'text': mapcss.tr('{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[highway]["addr:postcode"][highway!=services][highway!=rest_area][!postal_code]
        if ('addr:postcode' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'services', 'services')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'rest_area', 'rest_area')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'postal_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # suggestAlternative:"postal_code"
                # fixChangeKey:"addr:postcode=>postal_code"
                err.append({'class': 9001002, 'subclass': 1339665321, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['postal_code', mapcss.tag(tags, 'addr:postcode')]]),
                    '-': ([
                    'addr:postcode'])
                }})

        # way[highway=footway][cycleway=lane]
        if ('cycleway' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway') == mapcss._value_capture(capture_tags, 1, 'lane')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"highway=path + foot=designated + bicycle=designated + segregated=yes"
                err.append({'class': 9001002, 'subclass': 393240150, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[oneway][!highway][!area:highway][!railway][!aerialway][attraction!=summer_toboggan][aeroway!~/^(runway|taxiway)$/][leisure!=track][waterway!~/^(canal|fairway|lock|river|tidal_channel)$/]
        # way[lanes][!barrier][!ford][!highway][!area:highway][!junction][leisure!~/^(bowling_alley|slipway|swimming_pool|track)$/][!traffic_calming]!.only_one_tag
        # *[tunnel][!highway][!area:highway][!railway][!waterway][!piste:type][type!=tunnel][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=wildlife_crossing][man_made!=tunnel][power!=cable]!.TunnelCulvertWithoutWaterway
        # *[bridge][!highway][!area:highway][!railway][!waterway][!piste:type][type!=bridge][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=wildlife_crossing][man_made!=bridge][building!=bridge]
        # *[psv][!highway][!area:highway][!railway][!waterway][barrier!~/^(bollard|bump_gate|bus_trap|cattle_grid|chain|coupure|entrance|gate|height_restrictor|jersey_barrier|kerb|lift_gate|rope|sally_port|sliding_beam|sliding_gate|spikes|swing_gate|toll_booth|yes)$/][amenity!~/^parking.*/]
        # *[width][!highway][!area:highway][!railway][!waterway][!aeroway][!cycleway][!footway][!barrier][!man_made][!entrance][natural!=stone][leisure!=track]
        # *[maxspeed][!highway][!area:highway][!railway][traffic_sign!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][traffic_sign:forward!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][traffic_sign:backward!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][type!=enforcement][waterway!~/^(canal|fairway|lock|river|tidal_channel)$/][!traffic_calming][aerialway!=zip_line]
        # way[incline][!highway][!area:highway][!railway][aeroway!~/^(runway|taxiway)$/][attraction!=summer_toboggan][leisure!=slipway]
        if ('bridge' in keys) or ('incline' in keys) or ('lanes' in keys) or ('maxspeed' in keys) or ('oneway' in keys) or ('psv' in keys) or ('tunnel' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'aerialway')) and (mapcss._tag_capture(capture_tags, 5, tags, 'attraction') != mapcss._value_const_capture(capture_tags, 5, 'summer_toboggan', 'summer_toboggan')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_1dcd648f, '^(runway|taxiway)$'), mapcss._tag_capture(capture_tags, 6, tags, 'aeroway'))) and (mapcss._tag_capture(capture_tags, 7, tags, 'leisure') != mapcss._value_const_capture(capture_tags, 7, 'track', 'track')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 8, self.re_2fc1bb0a, '^(canal|fairway|lock|river|tidal_channel)$'), mapcss._tag_capture(capture_tags, 8, tags, 'waterway'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_only_one_tag) and (mapcss._tag_capture(capture_tags, 0, tags, 'lanes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'barrier')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'ford')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'junction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_49fc2c26, '^(bowling_alley|slipway|swimming_pool|track)$'), mapcss._tag_capture(capture_tags, 6, tags, 'leisure'))) and (not mapcss._tag_capture(capture_tags, 7, tags, 'traffic_calming')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_TunnelCulvertWithoutWaterway) and (mapcss._tag_capture(capture_tags, 0, tags, 'tunnel')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 6, tags, 'type') != mapcss._value_const_capture(capture_tags, 6, 'tunnel', 'tunnel')) and (mapcss._tag_capture(capture_tags, 7, tags, 'public_transport') != mapcss._value_const_capture(capture_tags, 7, 'platform', 'platform')) and (mapcss._tag_capture(capture_tags, 8, tags, 'route') != mapcss._value_const_capture(capture_tags, 8, 'ferry', 'ferry')) and (mapcss._tag_capture(capture_tags, 9, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 9, 'pipeline', 'pipeline')) and (mapcss._tag_capture(capture_tags, 10, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 10, 'goods_conveyor', 'goods_conveyor')) and (mapcss._tag_capture(capture_tags, 11, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 11, 'wildlife_crossing', 'wildlife_crossing')) and (mapcss._tag_capture(capture_tags, 12, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 12, 'tunnel', 'tunnel')) and (mapcss._tag_capture(capture_tags, 13, tags, 'power') != mapcss._value_const_capture(capture_tags, 13, 'cable', 'cable')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 6, tags, 'type') != mapcss._value_const_capture(capture_tags, 6, 'bridge', 'bridge')) and (mapcss._tag_capture(capture_tags, 7, tags, 'public_transport') != mapcss._value_const_capture(capture_tags, 7, 'platform', 'platform')) and (mapcss._tag_capture(capture_tags, 8, tags, 'route') != mapcss._value_const_capture(capture_tags, 8, 'ferry', 'ferry')) and (mapcss._tag_capture(capture_tags, 9, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 9, 'pipeline', 'pipeline')) and (mapcss._tag_capture(capture_tags, 10, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 10, 'goods_conveyor', 'goods_conveyor')) and (mapcss._tag_capture(capture_tags, 11, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 11, 'wildlife_crossing', 'wildlife_crossing')) and (mapcss._tag_capture(capture_tags, 12, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 12, 'bridge', 'bridge')) and (mapcss._tag_capture(capture_tags, 13, tags, 'building') != mapcss._value_const_capture(capture_tags, 13, 'bridge', 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'psv')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_33560b51, '^(bollard|bump_gate|bus_trap|cattle_grid|chain|coupure|entrance|gate|height_restrictor|jersey_barrier|kerb|lift_gate|rope|sally_port|sliding_beam|sliding_gate|spikes|swing_gate|toll_booth|yes)$'), mapcss._tag_capture(capture_tags, 5, tags, 'barrier'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_213d4d09, '^parking.*'), mapcss._tag_capture(capture_tags, 6, tags, 'amenity'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'aeroway')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'footway')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'barrier')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'man_made')) and (not mapcss._tag_capture(capture_tags, 10, tags, 'entrance')) and (mapcss._tag_capture(capture_tags, 11, tags, 'natural') != mapcss._value_const_capture(capture_tags, 11, 'stone', 'stone')) and (mapcss._tag_capture(capture_tags, 12, tags, 'leisure') != mapcss._value_const_capture(capture_tags, 12, 'track', 'track')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 4, tags, 'traffic_sign'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 5, tags, 'traffic_sign:forward'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 6, tags, 'traffic_sign:backward'))) and (mapcss._tag_capture(capture_tags, 7, tags, 'type') != mapcss._value_const_capture(capture_tags, 7, 'enforcement', 'enforcement')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 8, self.re_2fc1bb0a, '^(canal|fairway|lock|river|tidal_channel)$'), mapcss._tag_capture(capture_tags, 8, tags, 'waterway'))) and (not mapcss._tag_capture(capture_tags, 9, tags, 'traffic_calming')) and (mapcss._tag_capture(capture_tags, 10, tags, 'aerialway') != mapcss._value_const_capture(capture_tags, 10, 'zip_line', 'zip_line')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'incline')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_1dcd648f, '^(runway|taxiway)$'), mapcss._tag_capture(capture_tags, 4, tags, 'aeroway'))) and (mapcss._tag_capture(capture_tags, 5, tags, 'attraction') != mapcss._value_const_capture(capture_tags, 5, 'summer_toboggan', 'summer_toboggan')) and (mapcss._tag_capture(capture_tags, 6, tags, 'leisure') != mapcss._value_const_capture(capture_tags, 6, 'slipway', 'slipway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} on suspicious object","{0.key}")
                err.append({'class': 9001002, 'subclass': 1496920948, 'text': mapcss.tr('{0} on suspicious object', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[highway][barrier]
        # *[highway][waterway][waterway!=dam][waterway!=weir]
        # way[highway][natural][natural!=ridge]
        # *[landuse][building][landuse!=retail]
        if ('barrier' in keys and 'highway' in keys) or ('building' in keys and 'landuse' in keys) or ('highway' in keys and 'natural' in keys) or ('highway' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'barrier')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 2, 'dam', 'dam')) and (mapcss._tag_capture(capture_tags, 3, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 3, 'weir', 'weir')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural')) and (mapcss._tag_capture(capture_tags, 2, tags, 'natural') != mapcss._value_const_capture(capture_tags, 2, 'ridge', 'ridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (mapcss._tag_capture(capture_tags, 2, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 2, 'retail', 'retail')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 636059786, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[natural=water][leisure=swimming_pool]
        if ('leisure' in keys and 'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'water')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'swimming_pool')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("natural water used for swimming pool")
                # fixRemove:"natural"
                err.append({'class': 9001002, 'subclass': 608817213, 'text': mapcss.tr('natural water used for swimming pool'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'natural'])
                }})

        # *[sport][sport!=skiing][!building][!"building:part"][!club][tourism!=hotel][highway!~/^(pedestrian|raceway)$/][!leisure][natural!~/^(beach|bare_rock|cliff|peak|water)$/][amenity!~/^(bar|dojo|pub|restaurant|swimming_pool)$/][landuse!~/^(recreation_ground|piste|farm|farmland)$/][barrier!~/^(wall|retaining_wall)$/][!"piste:type"][shop!=sports][attraction!=summer_toboggan]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sport') != mapcss._value_const_capture(capture_tags, 1, 'skiing', 'skiing')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'building:part')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'club')) and (mapcss._tag_capture(capture_tags, 5, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 5, 'hotel', 'hotel')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_5dd46ebe, '^(pedestrian|raceway)$'), mapcss._tag_capture(capture_tags, 6, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 7, tags, 'leisure')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 8, self.re_29fa4401, '^(beach|bare_rock|cliff|peak|water)$'), mapcss._tag_capture(capture_tags, 8, tags, 'natural'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 9, self.re_41650b2e, '^(bar|dojo|pub|restaurant|swimming_pool)$'), mapcss._tag_capture(capture_tags, 9, tags, 'amenity'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 10, self.re_3b4f8f73, '^(recreation_ground|piste|farm|farmland)$'), mapcss._tag_capture(capture_tags, 10, tags, 'landuse'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 11, self.re_68c05e86, '^(wall|retaining_wall)$'), mapcss._tag_capture(capture_tags, 11, tags, 'barrier'))) and (not mapcss._tag_capture(capture_tags, 12, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 13, tags, 'shop') != mapcss._value_const_capture(capture_tags, 13, 'sports', 'sports')) and (mapcss._tag_capture(capture_tags, 14, tags, 'attraction') != mapcss._value_const_capture(capture_tags, 14, 'summer_toboggan', 'summer_toboggan')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("sport without physical feature")
                err.append({'class': 9001001, 'subclass': 1738767711, 'text': mapcss.tr('sport without physical feature')})

        # *[building:levels][!building][!building:part]
        # way[usage][!railway][!waterway][route!=railway][man_made!=pipeline][!aerialway]
        if ('building:levels' in keys) or ('usage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:levels')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'building:part')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'usage')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'route') != mapcss._value_const_capture(capture_tags, 3, 'railway', 'railway')) and (mapcss._tag_capture(capture_tags, 4, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 4, 'pipeline', 'pipeline')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'aerialway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001001, 'subclass': 1552380544, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *[/_name$/][!name][!old_name][!loc_name][!reg_name][!uic_name][!artist_name][!lock_name][!"osak:municipality_name"][!"osak:street_name"][NHD:subbasin_name!~/^(Des Moines Headwaters|Upper Des Moines|East Fork Des Moines)$/][noname!=yes]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_25d98c90)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'old_name')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'loc_name')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'reg_name')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'uic_name')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'artist_name')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'lock_name')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'osak:municipality_name')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'osak:street_name')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 10, self.re_51b15093, '^(Des Moines Headwaters|Upper Des Moines|East Fork Des Moines)$'), mapcss._tag_capture(capture_tags, 10, tags, 'NHD:subbasin_name'))) and (mapcss._tag_capture(capture_tags, 11, tags, 'noname') != mapcss._value_const_capture(capture_tags, 11, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("alternative name without {0}","{1.key}")
                # assertNoMatch:"way alt_name=Foo name=Bar"
                # assertMatch:"way alt_name=Foo"
                err.append({'class': 9001001, 'subclass': 1822630838, 'text': mapcss.tr('alternative name without {0}', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[name][alt_name][name=*alt_name]
        if ('alt_name' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'alt_name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'name') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'alt_name'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                # fixRemove:"alt_name"
                err.append({'class': 9001002, 'subclass': 1996350593, 'text': mapcss.tr('Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'alt_name'])
                }})

        # way[destination][!oneway?][junction!=roundabout][highway]
        if ('destination' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'destination')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'oneway') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 2, tags, 'junction') != mapcss._value_const_capture(capture_tags, 2, 'roundabout', 'roundabout')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("incomplete usage of {0} on a way without {1}","{0.key}","{1.key}")
                # suggestAlternative:"destination:backward"
                # suggestAlternative:"destination:forward"
                err.append({'class': 9001004, 'subclass': 915799973, 'text': mapcss.tr('incomplete usage of {0} on a way without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[maxspeed:forward][maxspeed:backward][!maxspeed]["maxspeed:forward"=*"maxspeed:backward"]
        if ('maxspeed:backward' in keys and 'maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:forward') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'maxspeed:backward'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                # suggestAlternative:"maxspeed"
                # fixRemove:"maxspeed:backward"
                # fixChangeKey:"maxspeed:forward=>maxspeed"
                err.append({'class': 9001002, 'subclass': 191340446, 'text': mapcss.tr('Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['maxspeed', mapcss.tag(tags, 'maxspeed:forward')]]),
                    '-': ([
                    'maxspeed:backward',
                    'maxspeed:forward'])
                }})

        # way[maxspeed:forward][maxspeed:backward][maxspeed]["maxspeed:forward"=*maxspeed]["maxspeed:backward"=*maxspeed]
        if ('maxspeed' in keys and 'maxspeed:backward' in keys and 'maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')) and (mapcss._tag_capture(capture_tags, 3, tags, 'maxspeed:forward') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'maxspeed'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'maxspeed:backward') == mapcss._value_capture(capture_tags, 4, mapcss.tag(tags, 'maxspeed'))))
                except mapcss.RuleAbort: pass
            if match:
                # set AllSameMaxspeed
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0}, {1} and {2}","{0.key}","{1.key}","{2.key}")
                # suggestAlternative:"maxspeed"
                # fixRemove:"maxspeed:backward"
                # fixRemove:"maxspeed:forward"
                set_AllSameMaxspeed = True
                err.append({'class': 9001002, 'subclass': 1144434553, 'text': mapcss.tr('Same value of {0}, {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'maxspeed:backward',
                    'maxspeed:forward'])
                }})

        # way[cycleway:left][cycleway:right][!cycleway]["cycleway:left"=*"cycleway:right"]
        if ('cycleway:left' in keys and 'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:right')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'cycleway:left') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'cycleway:right'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                # suggestAlternative:"cycleway"
                # fixChangeKey:"cycleway:left=>cycleway"
                # fixRemove:"cycleway:right"
                err.append({'class': 9001002, 'subclass': 268388923, 'text': mapcss.tr('Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['cycleway', mapcss.tag(tags, 'cycleway:left')]]),
                    '-': ([
                    'cycleway:left',
                    'cycleway:right'])
                }})

        # way[cycleway:left][cycleway:right][cycleway]["cycleway:left"=*cycleway]["cycleway:right"=*cycleway]
        if ('cycleway' in keys and 'cycleway:left' in keys and 'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:right')) and (mapcss._tag_capture(capture_tags, 2, tags, 'cycleway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'cycleway:left') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'cycleway'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'cycleway:right') == mapcss._value_capture(capture_tags, 4, mapcss.tag(tags, 'cycleway'))))
                except mapcss.RuleAbort: pass
            if match:
                # set AllSameCycleway
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0}, {1} and {2}","{0.key}","{1.key}","{2.key}")
                # suggestAlternative:"cycleway"
                # fixRemove:"cycleway:left"
                # fixRemove:"cycleway:right"
                set_AllSameCycleway = True
                err.append({'class': 9001002, 'subclass': 746971984, 'text': mapcss.tr('Same value of {0}, {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'cycleway:left',
                    'cycleway:right'])
                }})

        # way[sidewalk:left][sidewalk:right][!sidewalk]["sidewalk:left"=*"sidewalk:right"]
        if ('sidewalk:left' in keys and 'sidewalk:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sidewalk:right')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'sidewalk')) and (mapcss._tag_capture(capture_tags, 3, tags, 'sidewalk:left') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'sidewalk:right'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                # suggestAlternative:"sidewalk"
                # fixChangeKey:"sidewalk:left=>sidewalk"
                # fixRemove:"sidewalk:right"
                err.append({'class': 9001002, 'subclass': 951427711, 'text': mapcss.tr('Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['sidewalk', mapcss.tag(tags, 'sidewalk:left')]]),
                    '-': ([
                    'sidewalk:left',
                    'sidewalk:right'])
                }})

        # way[sidewalk:left][sidewalk:right][sidewalk]["sidewalk:left"=*sidewalk]["sidewalk:right"=*sidewalk]
        if ('sidewalk' in keys and 'sidewalk:left' in keys and 'sidewalk:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sidewalk:right')) and (mapcss._tag_capture(capture_tags, 2, tags, 'sidewalk')) and (mapcss._tag_capture(capture_tags, 3, tags, 'sidewalk:left') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'sidewalk'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'sidewalk:right') == mapcss._value_capture(capture_tags, 4, mapcss.tag(tags, 'sidewalk'))))
                except mapcss.RuleAbort: pass
            if match:
                # set AllSameSidewalk
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0}, {1} and {2}","{0.key}","{1.key}","{2.key}")
                # suggestAlternative:"sidewalk"
                # fixRemove:"sidewalk:left"
                # fixRemove:"sidewalk:right"
                set_AllSameSidewalk = True
                err.append({'class': 9001002, 'subclass': 1539830684, 'text': mapcss.tr('Same value of {0}, {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'sidewalk:left',
                    'sidewalk:right'])
                }})

        # way["maxspeed:forward"]["maxspeed:backward"][maxspeed]!.AllSameMaxspeed
        # way["cycleway:left"]["cycleway:right"][cycleway]!.AllSameCycleway
        # way["sidewalk:left"]["sidewalk:right"][sidewalk]!.AllSameSidewalk
        if ('cycleway' in keys and 'cycleway:left' in keys and 'cycleway:right' in keys) or ('maxspeed' in keys and 'maxspeed:backward' in keys and 'maxspeed:forward' in keys) or ('sidewalk' in keys and 'sidewalk:left' in keys and 'sidewalk:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_AllSameMaxspeed) and (mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_AllSameCycleway) and (mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway:right')) and (mapcss._tag_capture(capture_tags, 2, tags, 'cycleway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_AllSameSidewalk) and (mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sidewalk:right')) and (mapcss._tag_capture(capture_tags, 2, tags, 'sidewalk')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} and {1} together with {2} and conflicting values","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 321600037, 'text': mapcss.tr('{0} and {1} together with {2} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way["maxspeed:forward"][maxspeed][!"maxspeed:backward"]
        # way["maxspeed:backward"][maxspeed][!"maxspeed:forward"]
        # way["cycleway:left"][cycleway][!"cycleway:right"]
        # way["cycleway:right"][cycleway][!"cycleway:left"]
        # way["sidewalk:left"][sidewalk][!"sidewalk:right"]
        # way["sidewalk:right"][sidewalk][!"sidewalk:left"]
        if ('cycleway' in keys and 'cycleway:left' in keys) or ('cycleway' in keys and 'cycleway:right' in keys) or ('maxspeed' in keys and 'maxspeed:backward' in keys) or ('maxspeed' in keys and 'maxspeed:forward' in keys) or ('sidewalk' in keys and 'sidewalk:left' in keys) or ('sidewalk' in keys and 'sidewalk:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:backward')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed:backward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:forward')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'cycleway:right')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway:right')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'cycleway:left')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk:left')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sidewalk')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'sidewalk:right')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk:right')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sidewalk')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'sidewalk:left')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1987260958, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[bridge][layer][layer<0][bridge!=no][location!=underground][indoor!=yes][!tunnel]
        # way[tunnel][layer][layer>0][tunnel!=no][location!=overground][indoor!=yes][!bridge]
        if ('bridge' in keys and 'layer' in keys) or ('layer' in keys and 'tunnel' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge')) and (mapcss._tag_capture(capture_tags, 1, tags, 'layer')) and (mapcss._tag_capture(capture_tags, 2, tags, 'layer') < mapcss._value_capture(capture_tags, 2, 0)) and (mapcss._tag_capture(capture_tags, 3, tags, 'bridge') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'location') != mapcss._value_const_capture(capture_tags, 4, 'underground', 'underground')) and (mapcss._tag_capture(capture_tags, 5, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'tunnel')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tunnel')) and (mapcss._tag_capture(capture_tags, 1, tags, 'layer')) and (mapcss._tag_capture(capture_tags, 2, tags, 'layer') > mapcss._value_capture(capture_tags, 2, 0)) and (mapcss._tag_capture(capture_tags, 3, tags, 'tunnel') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no')) and (mapcss._tag_capture(capture_tags, 4, tags, 'location') != mapcss._value_const_capture(capture_tags, 4, 'overground', 'overground')) and (mapcss._tag_capture(capture_tags, 5, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 5, 'yes', 'yes')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'bridge')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1336318030, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[waterway][layer][layer=~/^(-1|-2|-3|-4|-5)$/][!tunnel][culvert!=yes][covered!=yes][pipeline!=yes][location!=underground][eval(waylength())>400]
        # Part of rule not implemented

        # way[water][natural!~/water|bay|strait/][water!=intermittent][amenity!=lavoir]!:closed
        # area[water][natural!~/water|bay|strait/][water!=intermittent][amenity!=lavoir]:closed
        if ('water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_521b2098, 'water|bay|strait'), mapcss._tag_capture(capture_tags, 1, tags, 'natural'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'intermittent', 'intermittent')) and (mapcss._tag_capture(capture_tags, 3, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 3, 'lavoir', 'lavoir')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_521b2098, 'water|bay|strait'), mapcss._tag_capture(capture_tags, 1, tags, 'natural'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'intermittent', 'intermittent')) and (mapcss._tag_capture(capture_tags, 3, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 3, 'lavoir', 'lavoir')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1901340680, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # area[golf=bunker][natural=beach]
        if ('golf' in keys and 'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'golf') == mapcss._value_capture(capture_tags, 0, 'bunker')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'beach')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"natural=sand"
                # suggestAlternative:"surface=sand"
                err.append({'class': 9001002, 'subclass': 253392874, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # set MotorwayTrunk
                set_MotorwayTrunk = True

        # way.MotorwayTrunk[lanes][turn:lanes][tag(lanes)!=eval(count(split("|",tag("turn:lanes"))))]
        # way.MotorwayTrunk[lanes][change:lanes][tag(lanes)!=eval(count(split("|",tag("change:lanes"))))]
        # way.MotorwayTrunk[lanes][maxspeed:lanes][tag(lanes)!=eval(count(split("|",tag("maxspeed:lanes"))))]
        # way.MotorwayTrunk[lanes][minspeed:lanes][tag(lanes)!=eval(count(split("|",tag("minspeed:lanes"))))]
        # way.MotorwayTrunk[lanes][destination:lanes][tag(lanes)!=eval(count(split("|",tag("destination:lanes"))))]
        # way.MotorwayTrunk[lanes][destination:ref:lanes][tag(lanes)!=eval(count(split("|",tag("destination:ref:lanes"))))]
        # way.MotorwayTrunk[lanes][destination:symbol:lanes][tag(lanes)!=eval(count(split("|",tag("destination:symbol:lanes"))))]
        if ('change:lanes' in keys and 'lanes' in keys) or ('destination:lanes' in keys and 'lanes' in keys) or ('destination:ref:lanes' in keys and 'lanes' in keys) or ('destination:symbol:lanes' in keys and 'lanes' in keys) or ('lanes' in keys and 'maxspeed:lanes' in keys) or ('lanes' in keys and 'minspeed:lanes' in keys) or ('lanes' in keys and 'turn:lanes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_MotorwayTrunk) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'turn:lanes')) and (mapcss.tag(tags, 'lanes') != mapcss.count(mapcss.split('|', mapcss.tag(tags, 'turn:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_MotorwayTrunk) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'change:lanes')) and (mapcss.tag(tags, 'lanes') != mapcss.count(mapcss.split('|', mapcss.tag(tags, 'change:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_MotorwayTrunk) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed:lanes')) and (mapcss.tag(tags, 'lanes') != mapcss.count(mapcss.split('|', mapcss.tag(tags, 'maxspeed:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_MotorwayTrunk) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'minspeed:lanes')) and (mapcss.tag(tags, 'lanes') != mapcss.count(mapcss.split('|', mapcss.tag(tags, 'minspeed:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_MotorwayTrunk) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'destination:lanes')) and (mapcss.tag(tags, 'lanes') != mapcss.count(mapcss.split('|', mapcss.tag(tags, 'destination:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_MotorwayTrunk) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'destination:ref:lanes')) and (mapcss.tag(tags, 'lanes') != mapcss.count(mapcss.split('|', mapcss.tag(tags, 'destination:ref:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_MotorwayTrunk) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'destination:symbol:lanes')) and (mapcss.tag(tags, 'lanes') != mapcss.count(mapcss.split('|', mapcss.tag(tags, 'destination:symbol:lanes')))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Different number of lanes in the keys {0} and {1}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 32264269, 'text': mapcss.tr('Different number of lanes in the keys {0} and {1}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[highway][lanes][!lanes:forward][!lanes:backward][oneway!=yes][oneway!=-1][oneway!=reversible][highway!=motorway][junction!=roundabout][lanes>2][mod(tag(lanes),2)=1]
        if ('highway' in keys and 'lanes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'lanes:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'lanes:backward')) and (mapcss._tag_capture(capture_tags, 4, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 5, tags, 'oneway') != mapcss._value_capture(capture_tags, 5, -1)) and (mapcss._tag_capture(capture_tags, 6, tags, 'oneway') != mapcss._value_const_capture(capture_tags, 6, 'reversible', 'reversible')) and (mapcss._tag_capture(capture_tags, 7, tags, 'highway') != mapcss._value_const_capture(capture_tags, 7, 'motorway', 'motorway')) and (mapcss._tag_capture(capture_tags, 8, tags, 'junction') != mapcss._value_const_capture(capture_tags, 8, 'roundabout', 'roundabout')) and (mapcss._tag_capture(capture_tags, 9, tags, 'lanes') > mapcss._value_capture(capture_tags, 9, 2)) and (mapcss.mod(mapcss.tag(tags, 'lanes'), 2) == 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("street with odd number of {0}, but without {1} and {2} or {3}","{1.key}","{2.key}","{3.key}","{4.key}")
                # assertNoMatch:"way highway=primary lanes=2"
                # assertNoMatch:"way highway=primary lanes=3 lanes:backward=2"
                # assertNoMatch:"way highway=primary lanes=3 oneway=-1"
                # assertMatch:"way highway=primary lanes=3"
                # assertNoMatch:"way highway=primary lanes=4"
                err.append({'class': 9001001, 'subclass': 1503842400, 'text': mapcss.tr('street with odd number of {0}, but without {1} and {2} or {3}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{3.key}'), mapcss._tag_uncapture(capture_tags, '{4.key}'))})

        # way[/^.*:lanes$/][!lanes][highway][!source:lanes]
        # way[/^.*:lanes:(forward|backward|both_ways)$/][!lanes][highway]
        # way[/^.*:lanes:both_ways$/][!lanes:both_ways][highway]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_22ceec1b)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'source:lanes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_3e28f822)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lanes')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_3baad59c)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lanes:both_ways')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # assertMatch:"way highway=primary turn:lanes:forward=left|right"
                # assertNoMatch:"way highway=primary turn:lanes=left|right lanes=2"
                # assertMatch:"way highway=primary turn:lanes=left|right"
                err.append({'class': 9001001, 'subclass': 1407445006, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # area[boundary=administrative][landuse=residential]
        if ('boundary' in keys and 'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary') == mapcss._value_capture(capture_tags, 0, 'administrative')) and (mapcss._tag_capture(capture_tags, 1, tags, 'landuse') == mapcss._value_capture(capture_tags, 1, 'residential')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1711273436, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[highway=pedestrian][width][siunit_length(tag(width))<3]
        if ('highway' in keys and 'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'pedestrian')) and (mapcss._tag_capture(capture_tags, 1, tags, 'width')) and (mapcss.siunit_length(mapcss.tag(tags, 'width')) < 3))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"highway=footway"
                # fixAdd:"highway=footway"
                # assertMatch:"way highway=pedestrian width=0.8"
                # assertMatch:"way highway=pedestrian width=1"
                # assertNoMatch:"way highway=pedestrian width=3"
                # assertNoMatch:"way highway=pedestrian width=5.5"
                err.append({'class': 9001002, 'subclass': 1277186295, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['highway','footway']])
                }})

        # area[cemetery=sector][landuse=cemetery]
        if ('cemetery' in keys and 'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cemetery') == mapcss._value_capture(capture_tags, 0, 'sector')) and (mapcss._tag_capture(capture_tags, 1, tags, 'landuse') == mapcss._value_capture(capture_tags, 1, 'cemetery')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1139622431, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[highway=cycleway][cycleway=track]
        if ('cycleway' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway') == mapcss._value_capture(capture_tags, 1, 'track')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Remove {1}.","{0.tag}","{1.tag}")
                # fixRemove:"cycleway"
                err.append({'class': 9001002, 'subclass': 563138279, 'text': mapcss.tr('{0} together with {1}. Remove {1}.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'cycleway'])
                }})

        # way[highway=path][!segregated][foot=designated][bicycle=designated]
        # way[highway=footway][!segregated][bicycle=designated]
        # way[highway=cycleway][!segregated][foot=designated]
        if ('bicycle' in keys and 'foot' in keys and 'highway' in keys) or ('bicycle' in keys and 'highway' in keys) or ('foot' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'path')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'segregated')) and (mapcss._tag_capture(capture_tags, 2, tags, 'foot') == mapcss._value_capture(capture_tags, 2, 'designated')) and (mapcss._tag_capture(capture_tags, 3, tags, 'bicycle') == mapcss._value_capture(capture_tags, 3, 'designated')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'footway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'segregated')) and (mapcss._tag_capture(capture_tags, 2, tags, 'bicycle') == mapcss._value_capture(capture_tags, 2, 'designated')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'segregated')) and (mapcss._tag_capture(capture_tags, 2, tags, 'foot') == mapcss._value_capture(capture_tags, 2, 'designated')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("Combined foot- and cycleway without {0}.","{1.key}")
                err.append({'class': 9001001, 'subclass': 130310293, 'text': mapcss.tr('Combined foot- and cycleway without {0}.', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[construction:building][!building][!construction]
        # *[construction:highway][!highway][!construction]
        # *[construction:railway][!railway][!construction]
        # *[construction:landuse][!landuse][!construction]
        if ('construction:building' in keys) or ('construction:highway' in keys) or ('construction:landuse' in keys) or ('construction:railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} and {2}","{0.key}","{1.key}","{2.key}")
                # fixAdd:"construction={0.value}"
                # fixAdd:"{1.key}=construction"
                # assertNoMatch:"way construction:building=house building=house "
                # assertNoMatch:"way construction:building=house construction=house"
                # assertMatch:"way construction:building=house"
                err.append({'class': 9001001, 'subclass': 1239539337, 'text': mapcss.tr('{0} without {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, 'construction={0.value}')).split('=', 1),
                    (mapcss._tag_uncapture(capture_tags, '{1.key}=construction')).split('=', 1)])
                }})

        # *[building=construction]["construction:building"][!construction]
        # *[highway=construction]["construction:highway"][!construction]
        # *[railway=construction]["construction:railway"][!construction]
        # *[landuse=construction]["construction:landuse"][!construction]
        if ('building' in keys and 'construction:building' in keys) or ('construction:highway' in keys and 'highway' in keys) or ('construction:landuse' in keys and 'landuse' in keys) or ('construction:railway' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} together with {1} but without {2}","{0.key}","{1.key}","{2.key}")
                # fixAdd:"construction={1.value}"
                # assertMatch:"way construction:building=house building=construction"
                # assertNoMatch:"way construction:building=house building=house "
                # assertNoMatch:"way construction:building=house construction=house"
                err.append({'class': 9001001, 'subclass': 855187849, 'text': mapcss.tr('{0} together with {1} but without {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, 'construction={1.value}')).split('=', 1)])
                }})

        # *[building]["construction:building"][!construction][building!=construction]
        # *[highway]["construction:highway"][!construction][highway!=construction]
        # *[railway]["construction:railway"][!construction][railway!=construction]
        # *[landuse]["construction:landuse"][!construction][landuse!=construction]
        if ('building' in keys and 'construction:building' in keys) or ('construction:highway' in keys and 'highway' in keys) or ('construction:landuse' in keys and 'landuse' in keys) or ('construction:railway' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values plus no {2}","{0.key}","{1.key}","{2.key}")
                # assertNoMatch:"way construction:building=house building=construction"
                # assertMatch:"way construction:building=house building=office"
                # assertNoMatch:"way construction:building=house construction=house"
                err.append({'class': 9001002, 'subclass': 164864338, 'text': mapcss.tr('{0} together with {1} and conflicting values plus no {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *["construction:building"][construction][construction:building!=*construction]
        # *["construction:highway"][construction][construction:highway!=*construction]
        # *["construction:railway"][construction][construction:railway!=*construction]
        # *["construction:landuse"][construction][construction:landuse!=*construction]
        if ('construction' in keys and 'construction:building' in keys) or ('construction' in keys and 'construction:highway' in keys) or ('construction' in keys and 'construction:landuse' in keys) or ('construction' in keys and 'construction:railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:building') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:highway') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:railway') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:landuse') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                # assertNoMatch:"way construction:building=house construction=house"
                # assertMatch:"way construction:building=house construction=office"
                err.append({'class': 9001002, 'subclass': 1971600459, 'text': mapcss.tr('{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[highway][construction][construction!~/^(yes|minor|no)$/][highway!=construction]
        # way[railway][construction][construction!~/^(yes|minor|no)$/][railway!=construction]
        # area[building][construction][construction!~/^(yes|minor|no)$/][building!=construction]
        # area[landuse][construction][construction!~/^(yes|minor|no)$/][landuse!=construction]
        if ('building' in keys and 'construction' in keys) or ('construction' in keys and 'highway' in keys) or ('construction' in keys and 'landuse' in keys) or ('construction' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_06b82725, '^(yes|minor|no)$'), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_06b82725, '^(yes|minor|no)$'), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_06b82725, '^(yes|minor|no)$'), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_06b82725, '^(yes|minor|no)$'), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 864644489, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[amenity=recycling][collection_times="24/7"][!opening_hours]
        # *[amenity=recycling][collection_times][!opening_hours][collection_times=~/[a-z]-[A-Z].*[0-9]-[0-9]/]
        if ('amenity' in keys and 'collection_times' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'collection_times') == mapcss._value_capture(capture_tags, 1, '24/7')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'collection_times')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_3a43a33d), mapcss._tag_capture(capture_tags, 3, tags, 'collection_times'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Probably {2} is meant.","{1.key}","{0.tag}","{2.key}")
                # fixChangeKey:"collection_times => opening_hours"
                err.append({'class': 9001002, 'subclass': 1009884322, 'text': mapcss.tr('{0} together with {1}. Probably {2} is meant.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours', mapcss.tag(tags, 'collection_times')]]),
                    '-': ([
                    'collection_times'])
                }})

        # way[highway][crossing][highway=~/^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|unclassified|residential|service|living_street)$/]
        if ('crossing' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'crossing')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_3ad9e1f5), mapcss._tag_capture(capture_tags, 2, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Should be used on a minor highway type or a node","{1.key}","{0.tag}")
                # fixRemove:"crossing"
                # assertNoMatch:"way highway=construction construction=footway crossing=unmarked"
                # assertMatch:"way highway=trunk crossing=unmarked"
                err.append({'class': 9001002, 'subclass': 1696418751, 'text': mapcss.tr('{0} together with {1}. Should be used on a minor highway type or a node', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'crossing'])
                }})

        # *[amenity=recycling][!/^recycling:/][recycling_type!=centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_2d1850d1)) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 2, 'centre', 'centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","recycling:*")
                err.append({'class': 9001001, 'subclass': 321354601, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'recycling:*')})

        # *[source:addr][!/^addr:/]
        if ('source:addr' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","addr:*")
                err.append({'class': 9001001, 'subclass': 886065920, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'addr:*')})

        # *[source:maxspeed][!/^maxspeed:?/]
        if ('source:maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_050395e0)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","maxspeed","maxspeed:*")
                err.append({'class': 9001001, 'subclass': 480030366, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'maxspeed', 'maxspeed:*')})

        # *[man_made=communications_tower][height][siunit_length(tag(height))<75]
        if ('height' in keys and 'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'communications_tower')) and (mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss.siunit_length(mapcss.tag(tags, 'height')) < 75))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"man_made=tower + tower:type=communication + height"
                err.append({'class': 9001002, 'subclass': 1533608671, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[fixme][count(split(" ",tag("fixme")))==1][has_tag_key(tag("fixme"))]
        # *[FIXME][count(split(" ",tag("FIXME")))==1][has_tag_key(tag("FIXME"))]
        if ('FIXME' in keys) or ('fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fixme')) and (mapcss.count(mapcss.split(' ', mapcss.tag(tags, 'fixme'))) == 1) and (keys.__contains__(mapcss.tag(tags, 'fixme'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'FIXME')) and (mapcss.count(mapcss.split(' ', mapcss.tag(tags, 'FIXME'))) == 1) and (keys.__contains__(mapcss.tag(tags, 'FIXME'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Is the fixme fixed?","{0.tag}","{0.value}")
                # assertNoMatch:"way fixme=name"
                # assertMatch:"way name=\"Florist Gump\" FIXME=name"
                # assertNoMatch:"way name=\"Florist Gump\" fixme=\"the name might have changed\""
                # assertMatch:"way name=\"Florist Gump\" fixme=name"
                # assertNoMatch:"way name=\"Florist Gump\""
                err.append({'class': 9001002, 'subclass': 2092275873, 'text': mapcss.tr('{0} together with {1}. Is the fixme fixed?', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # way[highway][placement=transition][join_list("",uniq_list(tag_regex("^placement:.*$")))==transition]
        # way[highway][!placement][/^placement:.*$/][join_list("",uniq_list(tag_regex("^placement:.*$")))==transition]
        if ('highway' in keys) or ('highway' in keys and 'placement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'placement') == mapcss._value_capture(capture_tags, 1, 'transition')) and (mapcss.join_list('', mapcss.uniq_list(mapcss.tag_regex(tags, self.re_57c5150b))) == 'transition'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'placement')) and (mapcss._tag_capture(capture_tags, 2, tags, self.re_57c5150b)) and (mapcss.join_list('', mapcss.uniq_list(mapcss.tag_regex(tags, self.re_57c5150b))) == 'transition'))
                except mapcss.RuleAbort: pass
            if match:
                # set PlacementTransitionWarning
                # throwWarning:tr("Use {0} only as value of {1}","transition","placement")
                # fixRemove:"placement:backward"
                # fixRemove:"placement:both_ways"
                # fixRemove:"placement:forward"
                # fixAdd:"placement=transition"
                # assertNoMatch:"way highway=primary placement:backward=middle_of:1 placement:forward=transition"
                # assertMatch:"way highway=primary placement:backward=transition placement:forward=transition"
                # assertNoMatch:"way highway=primary placement=middle_of:1 placement:backward=transition placement:forward=transition"
                # assertMatch:"way highway=primary placement=transition placement:both_ways=transition"
                set_PlacementTransitionWarning = True
                err.append({'class': 9001005, 'subclass': 942326561, 'text': mapcss.tr('Use {0} only as value of {1}', 'transition', 'placement'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['placement','transition']]),
                    '-': ([
                    'placement:backward',
                    'placement:both_ways',
                    'placement:forward'])
                }})

        # way[placement][/^placement:.*$/][highway]!.PlacementTransitionWarning
        # way["placement:forward"]["placement:backward"][highway]!.PlacementTransitionWarning
        # way["placement:forward"]["placement:both_ways"][highway]!.PlacementTransitionWarning
        # way["placement:backward"]["placement:both_ways"][highway]!.PlacementTransitionWarning
        if ('highway' in keys and 'placement' in keys) or ('highway' in keys and 'placement:backward' in keys and 'placement:both_ways' in keys) or ('highway' in keys and 'placement:backward' in keys and 'placement:forward' in keys) or ('highway' in keys and 'placement:both_ways' in keys and 'placement:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_PlacementTransitionWarning) and (mapcss._tag_capture(capture_tags, 0, tags, 'placement')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_57c5150b)) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_PlacementTransitionWarning) and (mapcss._tag_capture(capture_tags, 0, tags, 'placement:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'placement:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_PlacementTransitionWarning) and (mapcss._tag_capture(capture_tags, 0, tags, 'placement:forward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'placement:both_ways')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((not set_PlacementTransitionWarning) and (mapcss._tag_capture(capture_tags, 0, tags, 'placement:backward')) and (mapcss._tag_capture(capture_tags, 1, tags, 'placement:both_ways')) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwError:tr("{0} together with {1}","{0.key}","{1.key}")
                # assertNoMatch:"way highway=primary placement:forward=right_of:1"
                # assertNoMatch:"way highway=primary placement:forward=transition placement:both_ways=transition"
                # assertMatch:"way highway=primary placement=left_of:2 placement:forward=right_of:1"
                err.append({'class': 9001002, 'subclass': 2100246844, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[footway][highway][footway=sidewalk][highway!~/^(path|footway|cycleway|construction|proposed)$/]
        if ('footway' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'footway') == mapcss._value_capture(capture_tags, 2, 'sidewalk')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_209d461d, '^(path|footway|cycleway|construction|proposed)$'), mapcss._tag_capture(capture_tags, 3, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"sidewalk=both"
                # suggestAlternative:"sidewalk=left"
                # suggestAlternative:"sidewalk=right"
                # suggestAlternative:"sidewalk=separate"
                err.append({'class': 9001002, 'subclass': 1490104380, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[footway][highway][footway!=sidewalk][highway!~/^(path|footway|cycleway|construction|proposed)$/]
        if ('footway' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'footway') != mapcss._value_const_capture(capture_tags, 2, 'sidewalk', 'sidewalk')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_209d461d, '^(path|footway|cycleway|construction|proposed)$'), mapcss._tag_capture(capture_tags, 3, tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1488812195, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[footway][!highway][!/:highway$/]
        # way[cycleway][!highway][!/:highway$/]
        if ('cycleway' in keys) or ('footway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_2fb1110d)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_2fb1110d)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # assertNoMatch:"way footway=sidewalk abandoned:highway=unclassified"
                err.append({'class': 9001001, 'subclass': 1698700242, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # way[bicycle][/^cycleway(:|$)/][!/^bicycle:/][bicycle=~/^(no|use_sidepath)$/][/^cycleway(:|$)/!~/^(no|none|separate)$/]
        if ('bicycle' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bicycle')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_0aef1f28)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_60ec5bd8)) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_143f11c5), mapcss._tag_capture(capture_tags, 3, tags, 'bicycle'))) and (not mapcss.regexp_test(self.re_5111b0b1, mapcss._match_regex(tags, self.re_0aef1f28))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way bicycle=no cycleway:right=no"
                # assertMatch:"way bicycle=no cycleway=track"
                # assertNoMatch:"way bicycle=use_sidepath bicycle:backward=yes cycleway:left=lane"
                # assertMatch:"way bicycle=use_sidepath cycleway:left=lane"
                # assertNoMatch:"way bicycle=use_sidepath cycleway:left=none"
                # assertMatch:"way bicycle=use_sidepath cycleway=lane"
                # assertNoMatch:"way bicycle=use_sidepath cycleway=no"
                # assertNoMatch:"way highway=cycleway cycleway=separate"
                # assertNoMatch:"way highway=residential bicycle=use_sidepath"
                err.append({'class': 9001002, 'subclass': 340613033, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[highway=living_street][maxspeed][maxspeed=~/mph/][get(split(" ",tag(maxspeed)),0)>15]
        # way[highway=living_street][maxspeed][maxspeed!~/mph/][get(split(" ",tag(maxspeed)),0)>20]
        if ('highway' in keys and 'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'living_street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_43e7f95e), mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed'))) and (mapcss.get(mapcss.split(' ', mapcss.tag(tags, 'maxspeed')), 0) > 15))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'living_street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_43e7f95e, 'mph'), mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed'))) and (mapcss.get(mapcss.split(' ', mapcss.tag(tags, 'maxspeed')), 0) > 20))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way highway=living_street maxspeed=\"15 mph\""
                # assertMatch:"way highway=living_street maxspeed=\"20 mph\""
                # assertNoMatch:"way highway=living_street maxspeed=20"
                # assertMatch:"way highway=living_street maxspeed=30"
                # assertNoMatch:"way highway=living_street maxspeed=walk"
                # assertNoMatch:"way highway=living_street"
                err.append({'class': 9001002, 'subclass': 1040857321, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[piste:type=nordic][!piste:grooming]
        if ('piste:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'piste:type') == mapcss._value_capture(capture_tags, 0, 'nordic')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'piste:grooming')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("No grooming defined for {0} skiing, add {1}","nordic","piste:grooming=")
                # assertNoMatch:"way piste:type=nordic piste:grooming=classic"
                # assertMatch:"way piste:type=nordic"
                err.append({'class': 9001001, 'subclass': 716854348, 'text': mapcss.tr('No grooming defined for {0} skiing, add {1}', 'nordic', 'piste:grooming=')})

        # way[piste:type=~/^downhill|nordic|skitour$/][!piste:difficulty][count(parent_tags("piste:difficulty"))==0]
        # Part of rule not implemented

        # *[voltage:primary][voltage:secondary][transformer=generator][tag("voltage:secondary")<tag("voltage:primary")]
        if ('transformer' in keys and 'voltage:primary' in keys and 'voltage:secondary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:primary')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage:secondary')) and (mapcss._tag_capture(capture_tags, 2, tags, 'transformer') == mapcss._value_capture(capture_tags, 2, 'generator')) and (mapcss.tag(tags, 'voltage:secondary') < mapcss.tag(tags, 'voltage:primary')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} is lower than {1} on {2}.","{1.key}","{0.key}","{2.tag}")
                err.append({'class': 9001002, 'subclass': 1175862429, 'text': mapcss.tr('{0} is lower than {1} on {2}.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # area[/^(building|building:part)$/][height][min_height][siunit_length(tag(height))<=siunit_length(tag(min_height))]
        # area[/^(building|building:part)$/][building:levels][building:min_level][tag("building:levels")<=tag("building:min_level")]
        if ('building:levels' in keys and 'building:min_level' in keys) or ('height' in keys and 'min_height' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss._tag_capture(capture_tags, 2, tags, 'min_height')) and (mapcss.siunit_length(mapcss.tag(tags, 'height')) <= mapcss.siunit_length(mapcss.tag(tags, 'min_height'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, 1, tags, 'building:levels')) and (mapcss._tag_capture(capture_tags, 2, tags, 'building:min_level')) and (mapcss.tag(tags, 'building:levels') <= mapcss.tag(tags, 'building:min_level')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} is lower or equal to {1} on {2}","{1.key}","{2.key}","{0.key}")
                err.append({'class': 9001002, 'subclass': 1399744513, 'text': mapcss.tr('{0} is lower or equal to {1} on {2}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_AllSameCycleway = set_AllSameMaxspeed = set_AllSameSidewalk = set_MotorwayTrunk = set_PlacementTransitionWarning = set_TunnelCulvertWithoutWaterway = set_fully_paved_surface = set_only_one_tag = set_unpaved_surface = False

        # *[border_type][!boundary]
        # *[piste:difficulty][!piste:type]
        # *[place][!name][place!=islet][place!=plot][noname!=yes]
        # *[transformer][!power]
        # *[source:date][!source]
        # *[source:name][!name][noname!=yes]
        # *[source:maxspeed:forward][!maxspeed:forward][!maxspeed]
        # *[source:maxspeed:backward][!maxspeed:backward][!maxspeed]
        # *[source:building][!building]
        # *[source:ref][!ref][noref!=yes]
        # *[source:population][!population]
        # *[source:postal_code][!postal_code]
        # *[source:ele][!ele]
        # *[source:ref:INSEE][!ref:INSEE]
        # *[source:lit][!lit]
        # *[source:hgv][!hgv]
        # *[source:highway][!highway]
        # *[source:maxaxleload][!maxaxleload]
        # *[source:surface][!surface]
        # *[source:bridge][!bridge]
        # *[source:old_name][!old_name]
        # *[source:bicycle][!bicycle]
        # *[source:designation][!designation]
        # *[source:height][!height]
        # *[source:lanes][!lanes]
        # *[source:postcode][!addr:postcode]
        # *[source:housenumber][!addr:housenumber]
        # *[source:addr:postcode][!addr:postcode]
        # *[source:addr:housenumber][!addr:housenumber]
        # area[min_height][!height][/^(building|building:part)$/]
        # area[building:min_level][!building:levels][/^(building|building:part)$/]
        if ('border_type' in keys) or ('building:min_level' in keys and 'type' in keys) or ('min_height' in keys and 'type' in keys) or ('piste:difficulty' in keys) or ('place' in keys) or ('source:addr:housenumber' in keys) or ('source:addr:postcode' in keys) or ('source:bicycle' in keys) or ('source:bridge' in keys) or ('source:building' in keys) or ('source:date' in keys) or ('source:designation' in keys) or ('source:ele' in keys) or ('source:height' in keys) or ('source:hgv' in keys) or ('source:highway' in keys) or ('source:housenumber' in keys) or ('source:lanes' in keys) or ('source:lit' in keys) or ('source:maxaxleload' in keys) or ('source:maxspeed:backward' in keys) or ('source:maxspeed:forward' in keys) or ('source:name' in keys) or ('source:old_name' in keys) or ('source:population' in keys) or ('source:postal_code' in keys) or ('source:postcode' in keys) or ('source:ref' in keys) or ('source:ref:INSEE' in keys) or ('source:surface' in keys) or ('transformer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'border_type')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'boundary')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'piste:difficulty')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'piste:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'place') != mapcss._value_const_capture(capture_tags, 2, 'islet', 'islet')) and (mapcss._tag_capture(capture_tags, 3, tags, 'place') != mapcss._value_const_capture(capture_tags, 3, 'plot', 'plot')) and (mapcss._tag_capture(capture_tags, 4, tags, 'noname') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'transformer')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'power')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:date')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'source')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:name')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noname') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed:forward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:forward')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed:backward')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxspeed:backward')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'maxspeed')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:building')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ref')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref')) and (mapcss._tag_capture(capture_tags, 2, tags, 'noref') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:population')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'population')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:postal_code')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'postal_code')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ele')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ele')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:ref:INSEE')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:INSEE')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:lit')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lit')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:hgv')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'hgv')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:highway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxaxleload')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'maxaxleload')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:surface')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'surface')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:bridge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:old_name')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'old_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:bicycle')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'bicycle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:designation')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'designation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:height')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'height')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:lanes')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'lanes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:postcode')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:housenumber')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr:postcode')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr:housenumber')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'min_height')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss._tag_capture(capture_tags, 2, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:min_level')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building:levels')) and (mapcss._tag_capture(capture_tags, 2, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 845575979, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[generator:source][power!=generator]
        # *[generator:method][power!=generator]
        # *[generator:type][power!=generator]
        # *[recycling_type][amenity!=recycling]
        # *[information][tourism!=information]
        # *[shelter_type][amenity!=shelter]
        # *[archaeological_site][historic!=archaeological_site]
        # *[artwork_type][tourism!=artwork][exhibit!=artwork]
        # *[castle_type][historic!=castle]
        # *[parking][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking)$/][parking!=yes][parking!=no]
        # *[zoo][tourism!=zoo]
        # *[bunker_type][military!=bunker]
        if ('archaeological_site' in keys) or ('artwork_type' in keys) or ('bunker_type' in keys) or ('castle_type' in keys) or ('generator:method' in keys) or ('generator:source' in keys) or ('generator:type' in keys) or ('information' in keys) or ('parking' in keys) or ('recycling_type' in keys) or ('shelter_type' in keys) or ('zoo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:source')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:method')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'generator:type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'generator', 'generator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'recycling_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'recycling', 'recycling')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'information')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'information', 'information')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shelter_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 1, 'shelter', 'shelter')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'archaeological_site')) and (mapcss._tag_capture(capture_tags, 1, tags, 'historic') != mapcss._value_const_capture(capture_tags, 1, 'archaeological_site', 'archaeological_site')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'artwork_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'artwork', 'artwork')) and (mapcss._tag_capture(capture_tags, 2, tags, 'exhibit') != mapcss._value_const_capture(capture_tags, 2, 'artwork', 'artwork')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'castle_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'historic') != mapcss._value_const_capture(capture_tags, 1, 'castle', 'castle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5cf0a79f, '^(parking|parking_space|parking_entrance|motorcycle_parking)$'), mapcss._tag_capture(capture_tags, 1, tags, 'amenity'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'parking') != mapcss._value_const_capture(capture_tags, 2, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 3, tags, 'parking') != mapcss._value_const_capture(capture_tags, 3, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'zoo')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 1, 'zoo', 'zoo')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bunker_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'military') != mapcss._value_const_capture(capture_tags, 1, 'bunker', 'bunker')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1921138977, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[bridge:movable][bridge!=movable][man_made!=bridge]
        # *[substation][power!=substation][pipeline!=substation]
        # *[reservoir_type][landuse!=reservoir][water!=reservoir]
        if ('bridge:movable' in keys) or ('reservoir_type' in keys) or ('substation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge:movable')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') != mapcss._value_const_capture(capture_tags, 1, 'movable', 'movable')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'bridge', 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'substation')) and (mapcss._tag_capture(capture_tags, 1, tags, 'power') != mapcss._value_const_capture(capture_tags, 1, 'substation', 'substation')) and (mapcss._tag_capture(capture_tags, 2, tags, 'pipeline') != mapcss._value_const_capture(capture_tags, 2, 'substation', 'substation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'reservoir_type')) and (mapcss._tag_capture(capture_tags, 1, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 1, 'reservoir', 'reservoir')) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'reservoir', 'reservoir')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1195794842, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[iata][aeroway!=aerodrome][aeroway!=heliport][aeroway!=helipad]
        # *[icao][aeroway!=aerodrome][aeroway!=heliport][aeroway!=helipad]
        if ('iata' in keys) or ('icao' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'iata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 1, 'aerodrome', 'aerodrome')) and (mapcss._tag_capture(capture_tags, 2, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 2, 'heliport', 'heliport')) and (mapcss._tag_capture(capture_tags, 3, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 3, 'helipad', 'helipad')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'icao')) and (mapcss._tag_capture(capture_tags, 1, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 1, 'aerodrome', 'aerodrome')) and (mapcss._tag_capture(capture_tags, 2, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 2, 'heliport', 'heliport')) and (mapcss._tag_capture(capture_tags, 3, tags, 'aeroway') != mapcss._value_const_capture(capture_tags, 3, 'helipad', 'helipad')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.tag}","{2.tag}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1908755652, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

        # *[pump_mechanism][man_made!=pump][man_made!=windpump][man_made!=water_well][man_made!=petroleum_well]
        if ('pump_mechanism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'pump_mechanism')) and (mapcss._tag_capture(capture_tags, 1, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 1, 'pump', 'pump')) and (mapcss._tag_capture(capture_tags, 2, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 2, 'windpump', 'windpump')) and (mapcss._tag_capture(capture_tags, 3, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 3, 'water_well', 'water_well')) and (mapcss._tag_capture(capture_tags, 4, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 4, 'petroleum_well', 'petroleum_well')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.tag}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1271875329, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.tag}'))})

        # *[actuator=manual][!handle]
        # *[mechanical_driver=manual][!handle]
        # relation[boundary=administrative][!admin_level]
        # relation[route=bicycle][!network][type=route]
        # relation[route=hiking][!network][type=route]
        # relation[route=foot][!network][type=route]
        # relation[route=horse][!network][type=route]
        # relation[route=piste][!piste:type][type=route]
        # relation[route=ski][!piste:type][type=route]
        # *[tourism=information][!information]
        # *[leisure=pitch][!sport]
        # *[aeroway=terminal][!building]
        # *[office=government][!government]
        # *[power=generator][!generator:source]
        # *[amenity=social_facility][!social_facility]
        # *[amenity=place_of_worship][!religion]
        # *[man_made=tower][!tower:type]
        # area[building=construction][!construction][!construction:building]
        # area[landuse=construction][!construction][!construction:landuse]
        if ('actuator' in keys) or ('aeroway' in keys) or ('amenity' in keys) or ('boundary' in keys) or ('building' in keys and 'type' in keys) or ('landuse' in keys and 'type' in keys) or ('leisure' in keys) or ('man_made' in keys) or ('mechanical_driver' in keys) or ('office' in keys) or ('power' in keys) or ('route' in keys and 'type' in keys) or ('tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'actuator') == mapcss._value_capture(capture_tags, 0, 'manual')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'handle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mechanical_driver') == mapcss._value_capture(capture_tags, 0, 'manual')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'handle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary') == mapcss._value_capture(capture_tags, 0, 'administrative')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'admin_level')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route') == mapcss._value_capture(capture_tags, 0, 'bicycle')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') == mapcss._value_capture(capture_tags, 2, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route') == mapcss._value_capture(capture_tags, 0, 'hiking')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') == mapcss._value_capture(capture_tags, 2, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route') == mapcss._value_capture(capture_tags, 0, 'foot')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') == mapcss._value_capture(capture_tags, 2, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route') == mapcss._value_capture(capture_tags, 0, 'horse')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') == mapcss._value_capture(capture_tags, 2, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route') == mapcss._value_capture(capture_tags, 0, 'piste')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') == mapcss._value_capture(capture_tags, 2, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route') == mapcss._value_capture(capture_tags, 0, 'ski')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 2, tags, 'type') == mapcss._value_capture(capture_tags, 2, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tourism') == mapcss._value_capture(capture_tags, 0, 'information')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'information')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'pitch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'sport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'terminal')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'office') == mapcss._value_capture(capture_tags, 0, 'government')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'government')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'generator')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'generator:source')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'social_facility')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'social_facility')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'place_of_worship')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'religion')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'tower')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'tower:type')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'construction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction:building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'construction')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction:landuse')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1165316570, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[segregated][!highway][railway!=crossing]
        if ('segregated' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'segregated')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'railway') != mapcss._value_const_capture(capture_tags, 2, 'crossing', 'crossing')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 413539177, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[amenity=recycling][recycling_type!=container][recycling_type!=centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 1, 'container', 'container')) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 2, 'centre', 'centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 747056792, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[smoothness][!highway][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$/][barrier!=kerb][!kerb]
        if ('smoothness' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'smoothness')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_4f156c8f, '^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$'), mapcss._tag_capture(capture_tags, 2, tags, 'amenity'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'barrier') != mapcss._value_const_capture(capture_tags, 3, 'kerb', 'kerb')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'kerb')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.key}")
                err.append({'class': 9001001, 'subclass': 1922079652, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.key}'))})

        # *[intermittent][!waterway][natural!~/^(water|spring)$/][landuse!~/^(basin|reservoir)$/][ford!~/^(yes|stepping_stones)$/]
        # *[boat][!waterway][natural!=water][landuse!~/^(basin|reservoir)$/][ford!=yes]
        if ('boat' in keys) or ('intermittent' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'intermittent')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_4fbfe59b, '^(water|spring)$'), mapcss._tag_capture(capture_tags, 2, tags, 'natural'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_0889a956, '^(basin|reservoir)$'), mapcss._tag_capture(capture_tags, 3, tags, 'landuse'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_734e4397, '^(yes|stepping_stones)$'), mapcss._tag_capture(capture_tags, 4, tags, 'ford'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boat')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'natural') != mapcss._value_const_capture(capture_tags, 2, 'water', 'water')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_0889a956, '^(basin|reservoir)$'), mapcss._tag_capture(capture_tags, 3, tags, 'landuse'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'ford') != mapcss._value_const_capture(capture_tags, 4, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1547975047, 'text': mapcss.tr('{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'), mapcss._tag_uncapture(capture_tags, '{4.tag}'))})

        # *[snowplowing][!highway][!amenity][!leisure]
        if ('snowplowing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'snowplowing')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'amenity')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'leisure')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.key}")
                err.append({'class': 9001001, 'subclass': 585636657, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{3.key}'))})

        # *[toll][!highway][!barrier][route!~/^(ferry|road)$/]
        if ('toll' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'toll')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'barrier')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_5ee853b2, '^(ferry|road)$'), mapcss._tag_capture(capture_tags, 3, tags, 'route'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1689494174, 'text': mapcss.tr('{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{3.tag}'))})

        # *[amenity=marketplace][highway]
        # *[power=plant][/^generator:/]
        # *[power=generator][/^plant:/]
        # *[power=plant][voltage]
        # *[power=plant][frequency]
        # *[internet_access=no][internet_access:fee]
        # *[amenity=vending_machine][shop]
        # *[noname?][name]
        # *[noref?][ref]
        # *[nohousenumber?][addr:housenumber]
        # *[actuator][handle][actuator!~/(^|;)manual(;|$)/]
        # *[mechanical_driver][handle][mechanical_driver!~/(^|;)manual(;|$)/]
        if ('actuator' in keys and 'handle' in keys) or ('addr:housenumber' in keys and 'nohousenumber' in keys) or ('amenity' in keys and 'highway' in keys) or ('amenity' in keys and 'shop' in keys) or ('frequency' in keys and 'power' in keys) or ('handle' in keys and 'mechanical_driver' in keys) or ('internet_access' in keys and 'internet_access:fee' in keys) or ('name' in keys and 'noname' in keys) or ('noref' in keys and 'ref' in keys) or ('power' in keys) or ('power' in keys and 'voltage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'marketplace')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_503776bb)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'generator')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_3b1153a4)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')) and (mapcss._tag_capture(capture_tags, 1, tags, 'frequency')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'internet_access') == mapcss._value_capture(capture_tags, 0, 'no')) and (mapcss._tag_capture(capture_tags, 1, tags, 'internet_access:fee')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'vending_machine')) and (mapcss._tag_capture(capture_tags, 1, tags, 'shop')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noname') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'noref') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'nohousenumber') in ('yes', 'true', '1')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'actuator')) and (mapcss._tag_capture(capture_tags, 1, tags, 'handle')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_78efbab0, '(^|;)manual(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'actuator'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mechanical_driver')) and (mapcss._tag_capture(capture_tags, 1, tags, 'handle')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_78efbab0, '(^|;)manual(;|$)'), mapcss._tag_capture(capture_tags, 2, tags, 'mechanical_driver'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1052450987, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[barrier=kerb][kerb=no]
        # *[man_made=bridge][bridge=yes]
        # *[man_made=tunnel][tunnel=yes]
        # *[amenity=police][police]
        # area[building=construction][construction][construction=~/^(yes|minor|no)$/]
        # area[landuse=construction][construction][construction=~/^(yes|minor|no)$/]
        if ('amenity' in keys and 'police' in keys) or ('barrier' in keys and 'kerb' in keys) or ('bridge' in keys and 'man_made' in keys) or ('building' in keys and 'construction' in keys and 'type' in keys) or ('construction' in keys and 'landuse' in keys and 'type' in keys) or ('man_made' in keys and 'tunnel' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'barrier') == mapcss._value_capture(capture_tags, 0, 'kerb')) and (mapcss._tag_capture(capture_tags, 1, tags, 'kerb') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'bridge')) and (mapcss._tag_capture(capture_tags, 1, tags, 'bridge') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'tunnel')) and (mapcss._tag_capture(capture_tags, 1, tags, 'tunnel') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'police')) and (mapcss._tag_capture(capture_tags, 1, tags, 'police')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_06b82725), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_06b82725), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1975860553, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # relation[type=multipolygon][area=no]
        if ('area' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'multipolygon')) and (mapcss._tag_capture(capture_tags, 1, tags, 'area') == mapcss._value_capture(capture_tags, 1, 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwError:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1091177792, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[building:part][building]
        # *[addr:street][addr:place][outside("CZ,DK")]
        if ('addr:place' in keys and 'addr:street' in keys) or ('building' in keys and 'building:part' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'addr:street')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:place')) and (mapcss.outside(self.father.config.options, 'CZ,DK')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1590654104, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[place][place!=farm][place!=plot][/^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$/]
        # *[boundary][/^addr:/]
        # *[highway][/^addr:/][highway!=services][highway!=rest_area][!"addr:postcode"]
        if ('boundary' in keys) or ('highway' in keys) or ('place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place')) and (mapcss._tag_capture(capture_tags, 1, tags, 'place') != mapcss._value_const_capture(capture_tags, 1, 'farm', 'farm')) and (mapcss._tag_capture(capture_tags, 2, tags, 'place') != mapcss._value_const_capture(capture_tags, 2, 'plot', 'plot')) and (mapcss._tag_capture(capture_tags, 3, tags, self.re_0737b0c4)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)) and (mapcss._tag_capture(capture_tags, 2, tags, 'highway') != mapcss._value_const_capture(capture_tags, 2, 'services', 'services')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'rest_area', 'rest_area')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","addr:*")
                err.append({'class': 9001002, 'subclass': 1053814004, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'addr:*')})

        # *[postal_code]["addr:postcode"][!highway][postal_code=*"addr:postcode"]
        if ('addr:postcode' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 731431309, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[postal_code]["addr:postcode"][!highway][postal_code!=*"addr:postcode"]
        if ('addr:postcode' in keys and 'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'postal_code')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 433558919, 'text': mapcss.tr('{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[tunnel][!highway][!area:highway][!railway][!waterway][!piste:type][type!=tunnel][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=wildlife_crossing][man_made!=tunnel][power!=cable]!.TunnelCulvertWithoutWaterway
        # *[bridge][!highway][!area:highway][!railway][!waterway][!piste:type][type!=bridge][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=wildlife_crossing][man_made!=bridge][building!=bridge]
        # *[psv][!highway][!area:highway][!railway][!waterway][barrier!~/^(bollard|bump_gate|bus_trap|cattle_grid|chain|coupure|entrance|gate|height_restrictor|jersey_barrier|kerb|lift_gate|rope|sally_port|sliding_beam|sliding_gate|spikes|swing_gate|toll_booth|yes)$/][amenity!~/^parking.*/]
        # *[width][!highway][!area:highway][!railway][!waterway][!aeroway][!cycleway][!footway][!barrier][!man_made][!entrance][natural!=stone][leisure!=track]
        # *[maxspeed][!highway][!area:highway][!railway][traffic_sign!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][traffic_sign:forward!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][traffic_sign:backward!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][type!=enforcement][waterway!~/^(canal|fairway|lock|river|tidal_channel)$/][!traffic_calming][aerialway!=zip_line]
        if ('bridge' in keys) or ('maxspeed' in keys) or ('psv' in keys) or ('tunnel' in keys) or ('width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not set_TunnelCulvertWithoutWaterway) and (mapcss._tag_capture(capture_tags, 0, tags, 'tunnel')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 6, tags, 'type') != mapcss._value_const_capture(capture_tags, 6, 'tunnel', 'tunnel')) and (mapcss._tag_capture(capture_tags, 7, tags, 'public_transport') != mapcss._value_const_capture(capture_tags, 7, 'platform', 'platform')) and (mapcss._tag_capture(capture_tags, 8, tags, 'route') != mapcss._value_const_capture(capture_tags, 8, 'ferry', 'ferry')) and (mapcss._tag_capture(capture_tags, 9, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 9, 'pipeline', 'pipeline')) and (mapcss._tag_capture(capture_tags, 10, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 10, 'goods_conveyor', 'goods_conveyor')) and (mapcss._tag_capture(capture_tags, 11, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 11, 'wildlife_crossing', 'wildlife_crossing')) and (mapcss._tag_capture(capture_tags, 12, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 12, 'tunnel', 'tunnel')) and (mapcss._tag_capture(capture_tags, 13, tags, 'power') != mapcss._value_const_capture(capture_tags, 13, 'cable', 'cable')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 6, tags, 'type') != mapcss._value_const_capture(capture_tags, 6, 'bridge', 'bridge')) and (mapcss._tag_capture(capture_tags, 7, tags, 'public_transport') != mapcss._value_const_capture(capture_tags, 7, 'platform', 'platform')) and (mapcss._tag_capture(capture_tags, 8, tags, 'route') != mapcss._value_const_capture(capture_tags, 8, 'ferry', 'ferry')) and (mapcss._tag_capture(capture_tags, 9, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 9, 'pipeline', 'pipeline')) and (mapcss._tag_capture(capture_tags, 10, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 10, 'goods_conveyor', 'goods_conveyor')) and (mapcss._tag_capture(capture_tags, 11, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 11, 'wildlife_crossing', 'wildlife_crossing')) and (mapcss._tag_capture(capture_tags, 12, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 12, 'bridge', 'bridge')) and (mapcss._tag_capture(capture_tags, 13, tags, 'building') != mapcss._value_const_capture(capture_tags, 13, 'bridge', 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'psv')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_33560b51, '^(bollard|bump_gate|bus_trap|cattle_grid|chain|coupure|entrance|gate|height_restrictor|jersey_barrier|kerb|lift_gate|rope|sally_port|sliding_beam|sliding_gate|spikes|swing_gate|toll_booth|yes)$'), mapcss._tag_capture(capture_tags, 5, tags, 'barrier'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_213d4d09, '^parking.*'), mapcss._tag_capture(capture_tags, 6, tags, 'amenity'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'width')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'aeroway')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'cycleway')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'footway')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'barrier')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'man_made')) and (not mapcss._tag_capture(capture_tags, 10, tags, 'entrance')) and (mapcss._tag_capture(capture_tags, 11, tags, 'natural') != mapcss._value_const_capture(capture_tags, 11, 'stone', 'stone')) and (mapcss._tag_capture(capture_tags, 12, tags, 'leisure') != mapcss._value_const_capture(capture_tags, 12, 'track', 'track')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area:highway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'railway')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 4, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 4, tags, 'traffic_sign'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 5, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 5, tags, 'traffic_sign:forward'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_27d9cb1c, '^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$'), mapcss._tag_capture(capture_tags, 6, tags, 'traffic_sign:backward'))) and (mapcss._tag_capture(capture_tags, 7, tags, 'type') != mapcss._value_const_capture(capture_tags, 7, 'enforcement', 'enforcement')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 8, self.re_2fc1bb0a, '^(canal|fairway|lock|river|tidal_channel)$'), mapcss._tag_capture(capture_tags, 8, tags, 'waterway'))) and (not mapcss._tag_capture(capture_tags, 9, tags, 'traffic_calming')) and (mapcss._tag_capture(capture_tags, 10, tags, 'aerialway') != mapcss._value_const_capture(capture_tags, 10, 'zip_line', 'zip_line')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} on suspicious object","{0.key}")
                err.append({'class': 9001002, 'subclass': 808700716, 'text': mapcss.tr('{0} on suspicious object', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[highway][waterway][waterway!=dam][waterway!=weir]
        # *[landuse][building][landuse!=retail]
        if ('building' in keys and 'landuse' in keys) or ('highway' in keys and 'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 2, 'dam', 'dam')) and (mapcss._tag_capture(capture_tags, 3, tags, 'waterway') != mapcss._value_const_capture(capture_tags, 3, 'weir', 'weir')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (mapcss._tag_capture(capture_tags, 2, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 2, 'retail', 'retail')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1750941961, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[natural=water][leisure=swimming_pool]
        if ('leisure' in keys and 'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'water')) and (mapcss._tag_capture(capture_tags, 1, tags, 'leisure') == mapcss._value_capture(capture_tags, 1, 'swimming_pool')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("natural water used for swimming pool")
                # fixRemove:"natural"
                err.append({'class': 9001002, 'subclass': 608817213, 'text': mapcss.tr('natural water used for swimming pool'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'natural'])
                }})

        # *[sport][sport!=skiing][!building][!"building:part"][!club][tourism!=hotel][highway!~/^(pedestrian|raceway)$/][!leisure][natural!~/^(beach|bare_rock|cliff|peak|water)$/][amenity!~/^(bar|dojo|pub|restaurant|swimming_pool)$/][landuse!~/^(recreation_ground|piste|farm|farmland)$/][barrier!~/^(wall|retaining_wall)$/][!"piste:type"][shop!=sports][attraction!=summer_toboggan]
        if ('sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sport')) and (mapcss._tag_capture(capture_tags, 1, tags, 'sport') != mapcss._value_const_capture(capture_tags, 1, 'skiing', 'skiing')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'building:part')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'club')) and (mapcss._tag_capture(capture_tags, 5, tags, 'tourism') != mapcss._value_const_capture(capture_tags, 5, 'hotel', 'hotel')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_5dd46ebe, '^(pedestrian|raceway)$'), mapcss._tag_capture(capture_tags, 6, tags, 'highway'))) and (not mapcss._tag_capture(capture_tags, 7, tags, 'leisure')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 8, self.re_29fa4401, '^(beach|bare_rock|cliff|peak|water)$'), mapcss._tag_capture(capture_tags, 8, tags, 'natural'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 9, self.re_41650b2e, '^(bar|dojo|pub|restaurant|swimming_pool)$'), mapcss._tag_capture(capture_tags, 9, tags, 'amenity'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 10, self.re_3b4f8f73, '^(recreation_ground|piste|farm|farmland)$'), mapcss._tag_capture(capture_tags, 10, tags, 'landuse'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 11, self.re_68c05e86, '^(wall|retaining_wall)$'), mapcss._tag_capture(capture_tags, 11, tags, 'barrier'))) and (not mapcss._tag_capture(capture_tags, 12, tags, 'piste:type')) and (mapcss._tag_capture(capture_tags, 13, tags, 'shop') != mapcss._value_const_capture(capture_tags, 13, 'sports', 'sports')) and (mapcss._tag_capture(capture_tags, 14, tags, 'attraction') != mapcss._value_const_capture(capture_tags, 14, 'summer_toboggan', 'summer_toboggan')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("sport without physical feature")
                err.append({'class': 9001001, 'subclass': 1738767711, 'text': mapcss.tr('sport without physical feature')})

        # *[building:levels][!building][!building:part]
        if ('building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:levels')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'building:part')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001001, 'subclass': 1821512557, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *[/_name$/][!name][!old_name][!loc_name][!reg_name][!uic_name][!artist_name][!lock_name][!"osak:municipality_name"][!"osak:street_name"][NHD:subbasin_name!~/^(Des Moines Headwaters|Upper Des Moines|East Fork Des Moines)$/][noname!=yes]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_25d98c90)) and (not mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'old_name')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'loc_name')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'reg_name')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'uic_name')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'artist_name')) and (not mapcss._tag_capture(capture_tags, 7, tags, 'lock_name')) and (not mapcss._tag_capture(capture_tags, 8, tags, 'osak:municipality_name')) and (not mapcss._tag_capture(capture_tags, 9, tags, 'osak:street_name')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 10, self.re_51b15093, '^(Des Moines Headwaters|Upper Des Moines|East Fork Des Moines)$'), mapcss._tag_capture(capture_tags, 10, tags, 'NHD:subbasin_name'))) and (mapcss._tag_capture(capture_tags, 11, tags, 'noname') != mapcss._value_const_capture(capture_tags, 11, 'yes', 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("alternative name without {0}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1822630838, 'text': mapcss.tr('alternative name without {0}', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # relation[oneway][type!=route]
        if ('oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'type') != mapcss._value_const_capture(capture_tags, 1, 'route', 'route')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a relation without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001003, 'subclass': 1921058011, 'text': mapcss.tr('{0} on a relation without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # area[water][natural!~/water|bay|strait/][water!=intermittent][amenity!=lavoir]:closed
        if ('type' in keys and 'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'water')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_521b2098, 'water|bay|strait'), mapcss._tag_capture(capture_tags, 1, tags, 'natural'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'water') != mapcss._value_const_capture(capture_tags, 2, 'intermittent', 'intermittent')) and (mapcss._tag_capture(capture_tags, 3, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 3, 'lavoir', 'lavoir')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')) and (mapcss._tag_capture(capture_tags, -2, tags, 'type') == mapcss._value_capture(capture_tags, -2, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 712980290, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # area[golf=bunker][natural=beach]
        if ('golf' in keys and 'natural' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'golf') == mapcss._value_capture(capture_tags, 0, 'bunker')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') == mapcss._value_capture(capture_tags, 1, 'beach')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"natural=sand"
                # suggestAlternative:"surface=sand"
                err.append({'class': 9001002, 'subclass': 253392874, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # area[boundary=administrative][landuse=residential]
        if ('boundary' in keys and 'landuse' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary') == mapcss._value_capture(capture_tags, 0, 'administrative')) and (mapcss._tag_capture(capture_tags, 1, tags, 'landuse') == mapcss._value_capture(capture_tags, 1, 'residential')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1711273436, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # area[cemetery=sector][landuse=cemetery]
        if ('cemetery' in keys and 'landuse' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cemetery') == mapcss._value_capture(capture_tags, 0, 'sector')) and (mapcss._tag_capture(capture_tags, 1, tags, 'landuse') == mapcss._value_capture(capture_tags, 1, 'cemetery')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1139622431, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[highway=cycleway][cycleway=track]
        if ('cycleway' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'cycleway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'cycleway') == mapcss._value_capture(capture_tags, 1, 'track')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Remove {1}.","{0.tag}","{1.tag}")
                # fixRemove:"cycleway"
                err.append({'class': 9001002, 'subclass': 563138279, 'text': mapcss.tr('{0} together with {1}. Remove {1}.', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'cycleway'])
                }})

        # *[construction:building][!building][!construction]
        # *[construction:highway][!highway][!construction]
        # *[construction:railway][!railway][!construction]
        # *[construction:landuse][!landuse][!construction]
        if ('construction:building' in keys) or ('construction:highway' in keys) or ('construction:landuse' in keys) or ('construction:railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} and {2}","{0.key}","{1.key}","{2.key}")
                # fixAdd:"construction={0.value}"
                # fixAdd:"{1.key}=construction"
                err.append({'class': 9001001, 'subclass': 1239539337, 'text': mapcss.tr('{0} without {1} and {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, 'construction={0.value}')).split('=', 1),
                    (mapcss._tag_uncapture(capture_tags, '{1.key}=construction')).split('=', 1)])
                }})

        # *[building=construction]["construction:building"][!construction]
        # *[highway=construction]["construction:highway"][!construction]
        # *[railway=construction]["construction:railway"][!construction]
        # *[landuse=construction]["construction:landuse"][!construction]
        if ('building' in keys and 'construction:building' in keys) or ('construction:highway' in keys and 'highway' in keys) or ('construction:landuse' in keys and 'landuse' in keys) or ('construction:railway' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse') == mapcss._value_capture(capture_tags, 0, 'construction')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} together with {1} but without {2}","{0.key}","{1.key}","{2.key}")
                # fixAdd:"construction={1.value}"
                err.append({'class': 9001001, 'subclass': 855187849, 'text': mapcss.tr('{0} together with {1} but without {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, 'construction={1.value}')).split('=', 1)])
                }})

        # *[building]["construction:building"][!construction][building!=construction]
        # *[highway]["construction:highway"][!construction][highway!=construction]
        # *[railway]["construction:railway"][!construction][railway!=construction]
        # *[landuse]["construction:landuse"][!construction][landuse!=construction]
        if ('building' in keys and 'construction:building' in keys) or ('construction:highway' in keys and 'highway' in keys) or ('construction:landuse' in keys and 'landuse' in keys) or ('construction:railway' in keys and 'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:building')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'highway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:railway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'railway') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction:landuse')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 3, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values plus no {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 164864338, 'text': mapcss.tr('{0} together with {1} and conflicting values plus no {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *["construction:building"][construction][construction:building!=*construction]
        # *["construction:highway"][construction][construction:highway!=*construction]
        # *["construction:railway"][construction][construction:railway!=*construction]
        # *["construction:landuse"][construction][construction:landuse!=*construction]
        if ('construction' in keys and 'construction:building' in keys) or ('construction' in keys and 'construction:highway' in keys) or ('construction' in keys and 'construction:landuse' in keys) or ('construction' in keys and 'construction:railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:building') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:highway') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:railway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:railway') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'construction:landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (mapcss._tag_capture(capture_tags, 2, tags, 'construction:landuse') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'construction'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1971600459, 'text': mapcss.tr('{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # area[building][construction][construction!~/^(yes|minor|no)$/][building!=construction]
        # area[landuse][construction][construction!~/^(yes|minor|no)$/][landuse!=construction]
        if ('building' in keys and 'construction' in keys and 'type' in keys) or ('construction' in keys and 'landuse' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_06b82725, '^(yes|minor|no)$'), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'building') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, 1, tags, 'construction')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_06b82725, '^(yes|minor|no)$'), mapcss._tag_capture(capture_tags, 2, tags, 'construction'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'landuse') != mapcss._value_const_capture(capture_tags, 3, 'construction', 'construction')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1489908627, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[amenity=recycling][collection_times="24/7"][!opening_hours]
        # *[amenity=recycling][collection_times][!opening_hours][collection_times=~/[a-z]-[A-Z].*[0-9]-[0-9]/]
        if ('amenity' in keys and 'collection_times' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'collection_times') == mapcss._value_capture(capture_tags, 1, '24/7')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (mapcss._tag_capture(capture_tags, 1, tags, 'collection_times')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_3a43a33d), mapcss._tag_capture(capture_tags, 3, tags, 'collection_times'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Probably {2} is meant.","{1.key}","{0.tag}","{2.key}")
                # fixChangeKey:"collection_times => opening_hours"
                err.append({'class': 9001002, 'subclass': 1009884322, 'text': mapcss.tr('{0} together with {1}. Probably {2} is meant.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['opening_hours', mapcss.tag(tags, 'collection_times')]]),
                    '-': ([
                    'collection_times'])
                }})

        # *[amenity=recycling][!/^recycling:/][recycling_type!=centre]
        if ('amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'recycling')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_2d1850d1)) and (mapcss._tag_capture(capture_tags, 2, tags, 'recycling_type') != mapcss._value_const_capture(capture_tags, 2, 'centre', 'centre')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","recycling:*")
                err.append({'class': 9001001, 'subclass': 321354601, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'recycling:*')})

        # *[source:addr][!/^addr:/]
        if ('source:addr' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:addr')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","addr:*")
                err.append({'class': 9001001, 'subclass': 886065920, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'addr:*')})

        # *[source:maxspeed][!/^maxspeed:?/]
        if ('source:maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:maxspeed')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_050395e0)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","maxspeed","maxspeed:*")
                err.append({'class': 9001001, 'subclass': 480030366, 'text': mapcss.tr('{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'maxspeed', 'maxspeed:*')})

        # *[man_made=communications_tower][height][siunit_length(tag(height))<75]
        if ('height' in keys and 'man_made' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'communications_tower')) and (mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss.siunit_length(mapcss.tag(tags, 'height')) < 75))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"man_made=tower + tower:type=communication + height"
                err.append({'class': 9001002, 'subclass': 1533608671, 'text': mapcss.tr('{0} together with {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[fixme][count(split(" ",tag("fixme")))==1][has_tag_key(tag("fixme"))]
        # *[FIXME][count(split(" ",tag("FIXME")))==1][has_tag_key(tag("FIXME"))]
        if ('FIXME' in keys) or ('fixme' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fixme')) and (mapcss.count(mapcss.split(' ', mapcss.tag(tags, 'fixme'))) == 1) and (keys.__contains__(mapcss.tag(tags, 'fixme'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'FIXME')) and (mapcss.count(mapcss.split(' ', mapcss.tag(tags, 'FIXME'))) == 1) and (keys.__contains__(mapcss.tag(tags, 'FIXME'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}. Is the fixme fixed?","{0.tag}","{0.value}")
                err.append({'class': 9001002, 'subclass': 2092275873, 'text': mapcss.tr('{0} together with {1}. Is the fixme fixed?', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{0.value}'))})

        # *[voltage:primary][voltage:secondary][transformer=generator][tag("voltage:secondary")<tag("voltage:primary")]
        if ('transformer' in keys and 'voltage:primary' in keys and 'voltage:secondary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:primary')) and (mapcss._tag_capture(capture_tags, 1, tags, 'voltage:secondary')) and (mapcss._tag_capture(capture_tags, 2, tags, 'transformer') == mapcss._value_capture(capture_tags, 2, 'generator')) and (mapcss.tag(tags, 'voltage:secondary') < mapcss.tag(tags, 'voltage:primary')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} is lower than {1} on {2}.","{1.key}","{0.key}","{2.tag}")
                err.append({'class': 9001002, 'subclass': 1175862429, 'text': mapcss.tr('{0} is lower than {1} on {2}.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # area[/^(building|building:part)$/][height][min_height][siunit_length(tag(height))<=siunit_length(tag(min_height))]
        # area[/^(building|building:part)$/][building:levels][building:min_level][tag("building:levels")<=tag("building:min_level")]
        if ('building:levels' in keys and 'building:min_level' in keys and 'type' in keys) or ('height' in keys and 'min_height' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, 1, tags, 'height')) and (mapcss._tag_capture(capture_tags, 2, tags, 'min_height')) and (mapcss.siunit_length(mapcss.tag(tags, 'height')) <= mapcss.siunit_length(mapcss.tag(tags, 'min_height'))) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, self.re_390b8c0f)) and (mapcss._tag_capture(capture_tags, 1, tags, 'building:levels')) and (mapcss._tag_capture(capture_tags, 2, tags, 'building:min_level')) and (mapcss.tag(tags, 'building:levels') <= mapcss.tag(tags, 'building:min_level')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} is lower or equal to {1} on {2}","{1.key}","{2.key}","{0.key}")
                err.append({'class': 9001002, 'subclass': 1399744513, 'text': mapcss.tr('{0} is lower or equal to {1} on {2}', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_combinations(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'source:addr:postcode': 'postman'}), expected={'class': 9001001, 'subclass': 31231113})
        self.check_not_err(n.node(data, {'maxspeed:hgv:conditional': '80 @ (weight>7.5 AND 22:00-05:00)', 'traffic_sign': 'maxspeed'}), expected={'class': 9001001, 'subclass': 2095780217})
        self.check_not_err(n.node(data, {'addr:postcode': '12345', 'place': 'foo'}), expected={'class': 9001002, 'subclass': 1053814004})
        self.check_err(n.node(data, {'addr:housenumber': '5', 'addr:postcode': '12345', 'place': 'foo'}), expected={'class': 9001002, 'subclass': 1053814004})
        self.check_err(n.node(data, {'addr:housenumber': '5', 'place': 'foo'}), expected={'class': 9001002, 'subclass': 1053814004})
        self.check_not_err(n.node(data, {'highway': 'street_lamp', 'natural': 'birds_nest'}), expected={'class': 9001002, 'subclass': 1750941961})
        self.check_not_err(n.node(data, {'amenity': 'restaurant', 'sport': '10pin'}), expected={'class': 9001001, 'subclass': 1738767711})
        self.check_not_err(n.node(data, {'natural': 'beach', 'sport': 'beachvolleyball'}), expected={'class': 9001001, 'subclass': 1738767711})
        self.check_not_err(n.node(data, {'building:part': 'yes', 'sport': 'boxing'}), expected={'class': 9001001, 'subclass': 1738767711})
        self.check_not_err(n.node(data, {'sport': 'skiing'}), expected={'class': 9001001, 'subclass': 1738767711})
        self.check_not_err(n.node(data, {'sport': 'swimming', 'tourism': 'hotel'}), expected={'class': 9001001, 'subclass': 1738767711})
        self.check_not_err(n.node(data, {'leisure': 'pitch', 'sport': 'tennis'}), expected={'class': 9001001, 'subclass': 1738767711})
        self.check_err(n.node(data, {'sport': 'tennis'}), expected={'class': 9001001, 'subclass': 1738767711})
        self.check_not_err(n.node(data, {'amenity': 'recycling', 'collection_times': 'Mo 08:00-11:00'}), expected={'class': 9001002, 'subclass': 1009884322})
        self.check_err(n.node(data, {'amenity': 'recycling', 'collection_times': 'Mo-Fr 06:00-20:00'}), expected={'class': 9001002, 'subclass': 1009884322})
        self.check_not_err(n.node(data, {'amenity': 'recycling', 'collection_times': 'Mo-Fr 15:00'}), expected={'class': 9001002, 'subclass': 1009884322})
        self.check_not_err(n.node(data, {'amenity': 'recycling', 'collection_times': 'Sa[2,4] 8:00-11:00'}), expected={'class': 9001002, 'subclass': 1009884322})
        self.check_not_err(n.node(data, {'addr:housenumber': '42', 'source:addr': 'postman'}), expected={'class': 9001001, 'subclass': 886065920})
        self.check_err(n.node(data, {'source:addr': 'postman'}), expected={'class': 9001001, 'subclass': 886065920})
        self.check_not_err(n.node(data, {'height': '4358\''}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_err(n.node(data, {'height': '245\'', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_err(n.node(data, {'height': '224.22 ft', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_not_err(n.node(data, {'height': '328.22 ft', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_err(n.node(data, {'height': '74 m', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_not_err(n.node(data, {'height': '75 m', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_err(n.node(data, {'height': '0.8', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_err(n.node(data, {'height': '231\'10.22"', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_not_err(n.node(data, {'height': '4358\'8"', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_err(n.node(data, {'height': '58', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_not_err(n.node(data, {'height': '75.72', 'man_made': 'communications_tower'}), expected={'class': 9001002, 'subclass': 1533608671})
        self.check_not_err(n.way(data, {'bicycle:forward': 'destination', 'oneway': '-1', 'oneway:bicycle': 'no'}, [0]), expected={'class': 9001002, 'subclass': 1751419774})
        self.check_not_err(n.way(data, {'bicycle:backward:conditional': 'yes @ (Mo-Fr)', 'oneway': 'yes', 'oneway:bicycle:conditional': 'no @ (Mo-Fr)'}, [0]), expected={'class': 9001002, 'subclass': 1751419774})
        self.check_not_err(n.way(data, {'bicycle:backward': 'destination', 'oneway': 'yes', 'oneway:bicycle': 'no'}, [0]), expected={'class': 9001002, 'subclass': 1751419774})
        self.check_err(n.way(data, {'bicycle:backward': 'destination', 'oneway': 'yes'}, [0]), expected={'class': 9001002, 'subclass': 1751419774})
        self.check_err(n.way(data, {'plant:source': 'combustion', 'power': 'generator'}, [0]), expected={'class': 9001002, 'subclass': 1751419774})
        self.check_err(n.way(data, {'generator:source': 'wind', 'power': 'plant'}, [0]), expected={'class': 9001002, 'subclass': 1751419774})
        self.check_not_err(n.way(data, {'alt_name': 'Foo', 'name': 'Bar'}, [0]), expected={'class': 9001001, 'subclass': 1822630838})
        self.check_err(n.way(data, {'alt_name': 'Foo'}, [0]), expected={'class': 9001001, 'subclass': 1822630838})
        self.check_not_err(n.way(data, {'highway': 'primary', 'lanes': '2'}, [0]), expected={'class': 9001001, 'subclass': 1503842400})
        self.check_not_err(n.way(data, {'highway': 'primary', 'lanes': '3', 'lanes:backward': '2'}, [0]), expected={'class': 9001001, 'subclass': 1503842400})
        self.check_not_err(n.way(data, {'highway': 'primary', 'lanes': '3', 'oneway': '-1'}, [0]), expected={'class': 9001001, 'subclass': 1503842400})
        self.check_err(n.way(data, {'highway': 'primary', 'lanes': '3'}, [0]), expected={'class': 9001001, 'subclass': 1503842400})
        self.check_not_err(n.way(data, {'highway': 'primary', 'lanes': '4'}, [0]), expected={'class': 9001001, 'subclass': 1503842400})
        self.check_err(n.way(data, {'highway': 'primary', 'turn:lanes:forward': 'left|right'}, [0]), expected={'class': 9001001, 'subclass': 1407445006})
        self.check_not_err(n.way(data, {'highway': 'primary', 'lanes': '2', 'turn:lanes': 'left|right'}, [0]), expected={'class': 9001001, 'subclass': 1407445006})
        self.check_err(n.way(data, {'highway': 'primary', 'turn:lanes': 'left|right'}, [0]), expected={'class': 9001001, 'subclass': 1407445006})
        self.check_err(n.way(data, {'highway': 'pedestrian', 'width': '0.8'}, [0]), expected={'class': 9001002, 'subclass': 1277186295})
        self.check_err(n.way(data, {'highway': 'pedestrian', 'width': '1'}, [0]), expected={'class': 9001002, 'subclass': 1277186295})
        self.check_not_err(n.way(data, {'highway': 'pedestrian', 'width': '3'}, [0]), expected={'class': 9001002, 'subclass': 1277186295})
        self.check_not_err(n.way(data, {'highway': 'pedestrian', 'width': '5.5'}, [0]), expected={'class': 9001002, 'subclass': 1277186295})
        self.check_not_err(n.way(data, {'building': 'house', 'construction:building': 'house'}, [0]), expected={'class': 9001001, 'subclass': 1239539337})
        self.check_not_err(n.way(data, {'construction': 'house', 'construction:building': 'house'}, [0]), expected={'class': 9001001, 'subclass': 1239539337})
        self.check_err(n.way(data, {'construction:building': 'house'}, [0]), expected={'class': 9001001, 'subclass': 1239539337})
        self.check_err(n.way(data, {'building': 'construction', 'construction:building': 'house'}, [0]), expected={'class': 9001001, 'subclass': 855187849})
        self.check_not_err(n.way(data, {'building': 'house', 'construction:building': 'house'}, [0]), expected={'class': 9001001, 'subclass': 855187849})
        self.check_not_err(n.way(data, {'construction': 'house', 'construction:building': 'house'}, [0]), expected={'class': 9001001, 'subclass': 855187849})
        self.check_not_err(n.way(data, {'building': 'construction', 'construction:building': 'house'}, [0]), expected={'class': 9001002, 'subclass': 164864338})
        self.check_err(n.way(data, {'building': 'office', 'construction:building': 'house'}, [0]), expected={'class': 9001002, 'subclass': 164864338})
        self.check_not_err(n.way(data, {'construction': 'house', 'construction:building': 'house'}, [0]), expected={'class': 9001002, 'subclass': 164864338})
        self.check_not_err(n.way(data, {'construction': 'house', 'construction:building': 'house'}, [0]), expected={'class': 9001002, 'subclass': 1971600459})
        self.check_err(n.way(data, {'construction': 'office', 'construction:building': 'house'}, [0]), expected={'class': 9001002, 'subclass': 1971600459})
        self.check_not_err(n.way(data, {'construction': 'footway', 'crossing': 'unmarked', 'highway': 'construction'}, [0]), expected={'class': 9001002, 'subclass': 1696418751})
        self.check_err(n.way(data, {'crossing': 'unmarked', 'highway': 'trunk'}, [0]), expected={'class': 9001002, 'subclass': 1696418751})
        self.check_not_err(n.way(data, {'fixme': 'name'}, [0]), expected={'class': 9001002, 'subclass': 2092275873})
        self.check_err(n.way(data, {'FIXME': 'name', 'name': 'Florist Gump'}, [0]), expected={'class': 9001002, 'subclass': 2092275873})
        self.check_not_err(n.way(data, {'fixme': 'the name might have changed', 'name': 'Florist Gump'}, [0]), expected={'class': 9001002, 'subclass': 2092275873})
        self.check_err(n.way(data, {'fixme': 'name', 'name': 'Florist Gump'}, [0]), expected={'class': 9001002, 'subclass': 2092275873})
        self.check_not_err(n.way(data, {'name': 'Florist Gump'}, [0]), expected={'class': 9001002, 'subclass': 2092275873})
        self.check_not_err(n.way(data, {'highway': 'primary', 'placement:backward': 'middle_of:1', 'placement:forward': 'transition'}, [0]), expected={'class': 9001005, 'subclass': 942326561})
        self.check_err(n.way(data, {'highway': 'primary', 'placement:backward': 'transition', 'placement:forward': 'transition'}, [0]), expected={'class': 9001005, 'subclass': 942326561})
        self.check_not_err(n.way(data, {'highway': 'primary', 'placement': 'middle_of:1', 'placement:backward': 'transition', 'placement:forward': 'transition'}, [0]), expected={'class': 9001005, 'subclass': 942326561})
        self.check_err(n.way(data, {'highway': 'primary', 'placement': 'transition', 'placement:both_ways': 'transition'}, [0]), expected={'class': 9001005, 'subclass': 942326561})
        self.check_not_err(n.way(data, {'highway': 'primary', 'placement:forward': 'right_of:1'}, [0]), expected={'class': 9001002, 'subclass': 2100246844})
        self.check_not_err(n.way(data, {'highway': 'primary', 'placement:both_ways': 'transition', 'placement:forward': 'transition'}, [0]), expected={'class': 9001002, 'subclass': 2100246844})
        self.check_err(n.way(data, {'highway': 'primary', 'placement': 'left_of:2', 'placement:forward': 'right_of:1'}, [0]), expected={'class': 9001002, 'subclass': 2100246844})
        self.check_not_err(n.way(data, {'abandoned:highway': 'unclassified', 'footway': 'sidewalk'}, [0]), expected={'class': 9001001, 'subclass': 1698700242})
        self.check_not_err(n.way(data, {'bicycle': 'no', 'cycleway:right': 'no'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_err(n.way(data, {'bicycle': 'no', 'cycleway': 'track'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_not_err(n.way(data, {'bicycle': 'use_sidepath', 'bicycle:backward': 'yes', 'cycleway:left': 'lane'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_err(n.way(data, {'bicycle': 'use_sidepath', 'cycleway:left': 'lane'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_not_err(n.way(data, {'bicycle': 'use_sidepath', 'cycleway:left': 'none'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_err(n.way(data, {'bicycle': 'use_sidepath', 'cycleway': 'lane'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_not_err(n.way(data, {'bicycle': 'use_sidepath', 'cycleway': 'no'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_not_err(n.way(data, {'cycleway': 'separate', 'highway': 'cycleway'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_not_err(n.way(data, {'bicycle': 'use_sidepath', 'highway': 'residential'}, [0]), expected={'class': 9001002, 'subclass': 340613033})
        self.check_not_err(n.way(data, {'highway': 'living_street', 'maxspeed': '15 mph'}, [0]), expected={'class': 9001002, 'subclass': 1040857321})
        self.check_err(n.way(data, {'highway': 'living_street', 'maxspeed': '20 mph'}, [0]), expected={'class': 9001002, 'subclass': 1040857321})
        self.check_not_err(n.way(data, {'highway': 'living_street', 'maxspeed': '20'}, [0]), expected={'class': 9001002, 'subclass': 1040857321})
        self.check_err(n.way(data, {'highway': 'living_street', 'maxspeed': '30'}, [0]), expected={'class': 9001002, 'subclass': 1040857321})
        self.check_not_err(n.way(data, {'highway': 'living_street', 'maxspeed': 'walk'}, [0]), expected={'class': 9001002, 'subclass': 1040857321})
        self.check_not_err(n.way(data, {'highway': 'living_street'}, [0]), expected={'class': 9001002, 'subclass': 1040857321})
        self.check_not_err(n.way(data, {'piste:grooming': 'classic', 'piste:type': 'nordic'}, [0]), expected={'class': 9001001, 'subclass': 716854348})
        self.check_err(n.way(data, {'piste:type': 'nordic'}, [0]), expected={'class': 9001001, 'subclass': 716854348})
