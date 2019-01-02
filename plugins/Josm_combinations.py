#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_combinations(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9001001] = {'item': 9001, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'missing tag')}
        self.errors[9001002] = {'item': 9001, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'suspicious tag combination')}
        self.errors[9001003] = {'item': 9001, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} on a relation without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))}
        self.errors[9001004] = {'item': 9001, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'incomplete usage of {0} on a way without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}

        self.re_050395e0 = re.compile(ur'^maxspeed:?')
        self.re_0737b0c4 = re.compile(ur'^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$')
        self.re_0889a956 = re.compile(ur'^(basin|reservoir)$')
        self.re_088b0835 = re.compile(ur'^addr:')
        self.re_12ce6b85 = re.compile(ur':forward')
        self.re_1dcd648f = re.compile(ur'^(runway|taxiway)$')
        self.re_213d4d09 = re.compile(ur'^parking.*')
        self.re_23888fca = re.compile(ur'^(motorway|motorway_link|trunk|trunk_link)$')
        self.re_25d98c90 = re.compile(ur'_name$')
        self.re_27d9cb1c = re.compile(ur'^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$')
        self.re_29fa4401 = re.compile(ur'^(beach|bare_rock|cliff|peak|water)$')
        self.re_3b4f8f73 = re.compile(ur'^(recreation_ground|piste|farm|farmland)$')
        self.re_46fc3877 = re.compile(ur'^(river|canal|lock)$')
        self.re_4f156c8f = re.compile(ur'^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$')
        self.re_4fbfe59b = re.compile(ur'^(water|spring)$')
        self.re_521b2098 = re.compile(ur'water|bay|strait')
        self.re_5cf0a79f = re.compile(ur'^(parking|parking_space|parking_entrance|motorcycle_parking)$')
        self.re_5ee853b2 = re.compile(ur'^(ferry|road)$')
        self.re_64c931ef = re.compile(ur'^(pub|restaurant|swimming_pool)$')
        self.re_68c05e86 = re.compile(ur'^(wall|retaining_wall)$')
        self.re_7346b495 = re.compile(ur':backward')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_AllSameMaxspeed = False

        # node[ntd_id][!highway]
        # *[border_type][!boundary]
        # *[piste:difficulty][!piste:type]
        # *[source:date][!source]
        # *[source:name][!name]
        # *[source:maxspeed:forward][!maxspeed:forward][!maxspeed]
        # *[source:maxspeed:backward][!maxspeed:backward][!maxspeed]
        # *[source:building][!building]
        # *[source:ref][!ref]
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
        # *[source:addr][!/^addr:/]
        # *[source:maxspeed][!/^maxspeed:?/]
        if (u'border_type' in keys) or (u'ntd_id' in keys) or (u'piste:difficulty' in keys) or (u'source:addr' in keys) or (u'source:addr:housenumber' in keys) or (u'source:addr:postcode' in keys) or (u'source:bicycle' in keys) or (u'source:bridge' in keys) or (u'source:building' in keys) or (u'source:date' in keys) or (u'source:designation' in keys) or (u'source:ele' in keys) or (u'source:height' in keys) or (u'source:hgv' in keys) or (u'source:highway' in keys) or (u'source:housenumber' in keys) or (u'source:lanes' in keys) or (u'source:lit' in keys) or (u'source:maxaxleload' in keys) or (u'source:maxspeed' in keys) or (u'source:maxspeed:backward' in keys) or (u'source:maxspeed:forward' in keys) or (u'source:name' in keys) or (u'source:old_name' in keys) or (u'source:population' in keys) or (u'source:postal_code' in keys) or (u'source:postcode' in keys) or (u'source:ref' in keys) or (u'source:ref:INSEE' in keys) or (u'source:surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ntd_id') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'border_type') and not mapcss._tag_capture(capture_tags, 1, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'piste:difficulty') and not mapcss._tag_capture(capture_tags, 1, tags, u'piste:type'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:date') and not mapcss._tag_capture(capture_tags, 1, tags, u'source'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:name') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed:forward') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:forward') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed:backward') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:backward') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:building') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ref') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:population') and not mapcss._tag_capture(capture_tags, 1, tags, u'population'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:postal_code') and not mapcss._tag_capture(capture_tags, 1, tags, u'postal_code'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ele') and not mapcss._tag_capture(capture_tags, 1, tags, u'ele'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ref:INSEE') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:INSEE'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:lit') and not mapcss._tag_capture(capture_tags, 1, tags, u'lit'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:hgv') and not mapcss._tag_capture(capture_tags, 1, tags, u'hgv'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:highway') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxaxleload') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxaxleload'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:surface') and not mapcss._tag_capture(capture_tags, 1, tags, u'surface'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:bridge') and not mapcss._tag_capture(capture_tags, 1, tags, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:old_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:bicycle') and not mapcss._tag_capture(capture_tags, 1, tags, u'bicycle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:designation') and not mapcss._tag_capture(capture_tags, 1, tags, u'designation'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:height') and not mapcss._tag_capture(capture_tags, 1, tags, u'height'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:lanes') and not mapcss._tag_capture(capture_tags, 1, tags, u'lanes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:postcode') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:housenumber') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr:postcode') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr:housenumber') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr') and not mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, self.re_050395e0))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # assertMatch:"node source:addr:postcode=postman"
                # assertNoMatch:"node source:addr=postman addr:housenumber=42"
                # assertMatch:"node source:addr=postman"
                err.append({'class': 9001001, 'subclass': 1812055539, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[transformer][!power]
        # *[recycling_type][amenity!=recycling]
        # *[information][tourism!=information]
        # node[board_type][information!=board]
        # *[shelter_type][amenity!=shelter]
        # node[lamp_type][highway!=street_lamp]
        # node[map_type][information!=map]
        # *[site_type][historic!=archaeological_site]
        # *[artwork_type][tourism!=artwork][exhibit!=artwork]
        # *[castle_type][historic!=castle]
        # *[parking][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking)$/]
        # *[bunker_type][military!=bunker]
        if (u'artwork_type' in keys) or (u'board_type' in keys) or (u'bunker_type' in keys) or (u'castle_type' in keys) or (u'information' in keys) or (u'lamp_type' in keys) or (u'map_type' in keys) or (u'parking' in keys) or (u'recycling_type' in keys) or (u'shelter_type' in keys) or (u'site_type' in keys) or (u'transformer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'transformer') and not mapcss._tag_capture(capture_tags, 1, tags, u'power'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'recycling_type') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'recycling'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'information') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'information'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'board_type') and mapcss._tag_capture(capture_tags, 1, tags, u'information') != mapcss._value_capture(capture_tags, 1, u'board'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shelter_type') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'shelter'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lamp_type') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') != mapcss._value_capture(capture_tags, 1, u'street_lamp'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'map_type') and mapcss._tag_capture(capture_tags, 1, tags, u'information') != mapcss._value_capture(capture_tags, 1, u'map'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'site_type') and mapcss._tag_capture(capture_tags, 1, tags, u'historic') != mapcss._value_capture(capture_tags, 1, u'archaeological_site'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'artwork_type') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'artwork') and mapcss._tag_capture(capture_tags, 2, tags, u'exhibit') != mapcss._value_capture(capture_tags, 2, u'artwork'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'castle_type') and mapcss._tag_capture(capture_tags, 1, tags, u'historic') != mapcss._value_capture(capture_tags, 1, u'castle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'parking') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5cf0a79f), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bunker_type') and mapcss._tag_capture(capture_tags, 1, tags, u'military') != mapcss._value_capture(capture_tags, 1, u'bunker'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1621799652, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[bridge:movable][bridge!=movable][man_made!=bridge]
        # *[substation][power!=substation][pipeline!=substation]
        # *[reservoir_type][landuse!=reservoir][water!=reservoir]
        if (u'bridge:movable' in keys) or (u'reservoir_type' in keys) or (u'substation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge:movable') and mapcss._tag_capture(capture_tags, 1, tags, u'bridge') != mapcss._value_capture(capture_tags, 1, u'movable') and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') != mapcss._value_capture(capture_tags, 2, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'substation') and mapcss._tag_capture(capture_tags, 1, tags, u'power') != mapcss._value_capture(capture_tags, 1, u'substation') and mapcss._tag_capture(capture_tags, 2, tags, u'pipeline') != mapcss._value_capture(capture_tags, 2, u'substation'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'reservoir_type') and mapcss._tag_capture(capture_tags, 1, tags, u'landuse') != mapcss._value_capture(capture_tags, 1, u'reservoir') and mapcss._tag_capture(capture_tags, 2, tags, u'water') != mapcss._value_capture(capture_tags, 2, u'reservoir'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1195794842, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # *[tourism=information][!information]
        # *[leisure=pitch][!sport]
        # *[aeroway=terminal][!building]
        # *[power=generator][!generator:source]
        # *[amenity=social_facility][!social_facility]
        # *[amenity=place_of_worship][!religion]
        if (u'aeroway' in keys) or (u'amenity' in keys) or (u'leisure' in keys) or (u'power' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'information') and not mapcss._tag_capture(capture_tags, 1, tags, u'information'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and not mapcss._tag_capture(capture_tags, 1, tags, u'sport'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'terminal') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'generator') and not mapcss._tag_capture(capture_tags, 1, tags, u'generator:source'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'social_facility') and not mapcss._tag_capture(capture_tags, 1, tags, u'social_facility'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'place_of_worship') and not mapcss._tag_capture(capture_tags, 1, tags, u'religion'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 9001001, 'subclass': 288794802, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[smoothness][!highway][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$/]
        # *[segregated][!highway][railway!=crossing]
        if (u'segregated' in keys) or (u'smoothness' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'smoothness') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_4f156c8f), mapcss._tag_capture(capture_tags, 2, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'segregated') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != mapcss._value_capture(capture_tags, 2, u'crossing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1366851391, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # *[amenity=recycling][recycling_type!=container][recycling_type!=centre]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'recycling') and mapcss._tag_capture(capture_tags, 1, tags, u'recycling_type') != mapcss._value_capture(capture_tags, 1, u'container') and mapcss._tag_capture(capture_tags, 2, tags, u'recycling_type') != mapcss._value_capture(capture_tags, 2, u'centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 747056792, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # *[intermittent][!waterway][natural!~/^(water|spring)$/][landuse!~/^(basin|reservoir)$/][ford!=yes]
        # *[boat][!waterway][natural!=water][landuse!~/^(basin|reservoir)$/][ford!=yes]
        if (u'boat' in keys) or (u'intermittent' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'intermittent') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_4fbfe59b), mapcss._tag_capture(capture_tags, 2, tags, u'natural')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_0889a956), mapcss._tag_capture(capture_tags, 3, tags, u'landuse')) and mapcss._tag_capture(capture_tags, 4, tags, u'ford') != mapcss._value_capture(capture_tags, 4, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boat') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and mapcss._tag_capture(capture_tags, 2, tags, u'natural') != mapcss._value_capture(capture_tags, 2, u'water') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_0889a956), mapcss._tag_capture(capture_tags, 3, tags, u'landuse')) and mapcss._tag_capture(capture_tags, 4, tags, u'ford') != mapcss._value_capture(capture_tags, 4, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1096267911, 'text': mapcss.tr(u'{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'), mapcss._tag_uncapture(capture_tags, u'{3.tag}'), mapcss._tag_uncapture(capture_tags, u'{4.tag}'))})

        # *[snowplowing][!highway][!amenity][!leisure]
        if (u'snowplowing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'snowplowing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'amenity') and not mapcss._tag_capture(capture_tags, 3, tags, u'leisure'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.key}")
                err.append({'class': 9001001, 'subclass': 585636657, 'text': mapcss.tr(u'{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{3.key}'))})

        # *[toll][!highway][!barrier][route!~/^(ferry|road)$/]
        if (u'toll' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'toll') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'barrier') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_5ee853b2), mapcss._tag_capture(capture_tags, 3, tags, u'route')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1689494174, 'text': mapcss.tr(u'{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{3.tag}'))})

        # *[internet_access=no][internet_access:fee]
        # node[power=transformer][voltage]
        # node[transformer=distribution][voltage][power=pole]
        # *[amenity=vending_machine][shop]
        # *[noname?][name]
        if (u'internet_access' in keys and u'internet_access:fee' in keys) or (u'name' in keys and u'noname' in keys) or (u'power' in keys and u'transformer' in keys and u'voltage' in keys) or (u'power' in keys and u'voltage' in keys) or (u'amenity' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'internet_access') == mapcss._value_capture(capture_tags, 0, u'no') and mapcss._tag_capture(capture_tags, 1, tags, u'internet_access:fee'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer') and mapcss._tag_capture(capture_tags, 1, tags, u'voltage'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'transformer') == mapcss._value_capture(capture_tags, 0, u'distribution') and mapcss._tag_capture(capture_tags, 1, tags, u'voltage') and mapcss._tag_capture(capture_tags, 2, tags, u'power') == mapcss._value_capture(capture_tags, 2, u'pole'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'vending_machine') and mapcss._tag_capture(capture_tags, 1, tags, u'shop'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noname') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1007113564, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[access][eval(number_of_tags())=1]
        # *[area][eval(number_of_tags())=1]!.area_yes_autofix
        # *[name][eval(number_of_tags())=1]
        # *[ref][eval(number_of_tags())=1]
        # *[lit][eval(number_of_tags())=1]
        # Use undeclared class area_yes_autofix

        # *[name][area][eval(number_of_tags())=2]
        # *[name][ref][eval(number_of_tags())=2]
        if (u'area' in keys and u'name' in keys) or (u'name' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'area') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 788702375, 'text': mapcss.tr(u'incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[tourism=attraction][eval(number_of_tags())=1]
        if (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'attraction') and len(tags) == 1)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0}","{0.tag}")
                err.append({'class': 9001001, 'subclass': 463560683, 'text': mapcss.tr(u'incomplete object: only {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name][tourism=attraction][eval(number_of_tags())=2]
        if (u'name' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') == mapcss._value_capture(capture_tags, 1, u'attraction') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 34376505, 'text': mapcss.tr(u'incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[place][place!=farm][/^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$/]
        # *[boundary][/^addr:/]
        # *[highway][/^addr:/][highway!=services][highway!=rest_area][!"addr:postcode"]
        if (u'boundary' in keys) or (u'highway' in keys) or (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') != mapcss._value_capture(capture_tags, 1, u'farm') and mapcss._tag_capture(capture_tags, 2, tags, self.re_0737b0c4))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') and mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835) and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'services') and mapcss._tag_capture(capture_tags, 3, tags, u'highway') != mapcss._value_capture(capture_tags, 3, u'rest_area') and not mapcss._tag_capture(capture_tags, 4, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with addr:*","{0.key}")
                # assertNoMatch:"node place=foo  addr:postcode=12345"
                # assertMatch:"node place=foo addr:housenumber=5 addr:postcode=12345"
                # assertMatch:"node place=foo addr:housenumber=5"
                err.append({'class': 9001002, 'subclass': 2039567622, 'text': mapcss.tr(u'{0} together with addr:*', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][postal_code]["addr:postcode"][postal_code=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 1341956372, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[!highway][postal_code]["addr:postcode"][postal_code!=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 1415856502, 'text': mapcss.tr(u'{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[tunnel][!highway][!railway][!waterway][!piste:type][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor]
        # *[bridge][!highway][!railway][!waterway][!piste:type][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=bridge][building!=bridge]
        # *[psv][!highway][!railway][!waterway][amenity!~/^parking.*/]
        # *[width][!highway][!railway][!waterway][!aeroway][!cycleway][!footway][!barrier][!man_made][!entrance][natural!=stone]
        # *[maxspeed][!highway][!railway][traffic_sign!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][type!=enforcement][waterway!~/^(river|canal|lock)$/][!traffic_calming][aerialway!=zip_line]
        if (u'bridge' in keys) or (u'maxspeed' in keys) or (u'psv' in keys) or (u'tunnel' in keys) or (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tunnel') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 5, tags, u'public_transport') != mapcss._value_capture(capture_tags, 5, u'platform') and mapcss._tag_capture(capture_tags, 6, tags, u'route') != mapcss._value_capture(capture_tags, 6, u'ferry') and mapcss._tag_capture(capture_tags, 7, tags, u'man_made') != mapcss._value_capture(capture_tags, 7, u'pipeline') and mapcss._tag_capture(capture_tags, 8, tags, u'man_made') != mapcss._value_capture(capture_tags, 8, u'goods_conveyor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 5, tags, u'public_transport') != mapcss._value_capture(capture_tags, 5, u'platform') and mapcss._tag_capture(capture_tags, 6, tags, u'route') != mapcss._value_capture(capture_tags, 6, u'ferry') and mapcss._tag_capture(capture_tags, 7, tags, u'man_made') != mapcss._value_capture(capture_tags, 7, u'pipeline') and mapcss._tag_capture(capture_tags, 8, tags, u'man_made') != mapcss._value_capture(capture_tags, 8, u'goods_conveyor') and mapcss._tag_capture(capture_tags, 9, tags, u'man_made') != mapcss._value_capture(capture_tags, 9, u'bridge') and mapcss._tag_capture(capture_tags, 10, tags, u'building') != mapcss._value_capture(capture_tags, 10, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'psv') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 4, self.re_213d4d09), mapcss._tag_capture(capture_tags, 4, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'width') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'aeroway') and not mapcss._tag_capture(capture_tags, 5, tags, u'cycleway') and not mapcss._tag_capture(capture_tags, 6, tags, u'footway') and not mapcss._tag_capture(capture_tags, 7, tags, u'barrier') and not mapcss._tag_capture(capture_tags, 8, tags, u'man_made') and not mapcss._tag_capture(capture_tags, 9, tags, u'entrance') and mapcss._tag_capture(capture_tags, 10, tags, u'natural') != mapcss._value_capture(capture_tags, 10, u'stone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_27d9cb1c), mapcss._tag_capture(capture_tags, 3, tags, u'traffic_sign')) and mapcss._tag_capture(capture_tags, 4, tags, u'type') != mapcss._value_capture(capture_tags, 4, u'enforcement') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 5, self.re_46fc3877), mapcss._tag_capture(capture_tags, 5, tags, u'waterway')) and not mapcss._tag_capture(capture_tags, 6, tags, u'traffic_calming') and mapcss._tag_capture(capture_tags, 7, tags, u'aerialway') != mapcss._value_capture(capture_tags, 7, u'zip_line'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} on suspicious object","{0.key}")
                err.append({'class': 9001002, 'subclass': 755649879, 'text': mapcss.tr(u'{0} on suspicious object', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[highway][waterway][waterway!=dam][waterway!=weir]
        # *[landuse][building][landuse!=retail]
        if (u'building' in keys and u'landuse' in keys) or (u'highway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and mapcss._tag_capture(capture_tags, 2, tags, u'waterway') != mapcss._value_capture(capture_tags, 2, u'dam') and mapcss._tag_capture(capture_tags, 3, tags, u'waterway') != mapcss._value_capture(capture_tags, 3, u'weir'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'landuse') != mapcss._value_capture(capture_tags, 2, u'retail'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                # assertNoMatch:"node highway=street_lamp natural=birds_nest"
                err.append({'class': 9001002, 'subclass': 1750941961, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[natural=water][leisure=swimming_pool]
        if (u'leisure' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'water') and mapcss._tag_capture(capture_tags, 1, tags, u'leisure') == mapcss._value_capture(capture_tags, 1, u'swimming_pool'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("natural water used for swimming pool")
                # fixRemove:"natural"
                err.append({'class': 9001002, 'subclass': 608817213, 'text': mapcss.tr(u'natural water used for swimming pool'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'natural'])
                }})

        # *[sport][sport!=skiing][!building][!club][tourism!=hotel][highway!=raceway][!leisure][natural!~/^(beach|bare_rock|cliff|peak|water)$/][amenity!~/^(pub|restaurant|swimming_pool)$/][landuse!~/^(recreation_ground|piste|farm|farmland)$/][barrier!~/^(wall|retaining_wall)$/][!"piste:type"][shop!=sports]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') != mapcss._value_capture(capture_tags, 1, u'skiing') and not mapcss._tag_capture(capture_tags, 2, tags, u'building') and not mapcss._tag_capture(capture_tags, 3, tags, u'club') and mapcss._tag_capture(capture_tags, 4, tags, u'tourism') != mapcss._value_capture(capture_tags, 4, u'hotel') and mapcss._tag_capture(capture_tags, 5, tags, u'highway') != mapcss._value_capture(capture_tags, 5, u'raceway') and not mapcss._tag_capture(capture_tags, 6, tags, u'leisure') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 7, self.re_29fa4401), mapcss._tag_capture(capture_tags, 7, tags, u'natural')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 8, self.re_64c931ef), mapcss._tag_capture(capture_tags, 8, tags, u'amenity')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 9, self.re_3b4f8f73), mapcss._tag_capture(capture_tags, 9, tags, u'landuse')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 10, self.re_68c05e86), mapcss._tag_capture(capture_tags, 10, tags, u'barrier')) and not mapcss._tag_capture(capture_tags, 11, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 12, tags, u'shop') != mapcss._value_capture(capture_tags, 12, u'sports'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("sport without physical feature")
                # assertNoMatch:"node sport=10pin amenity=restaurant"
                # assertNoMatch:"node sport=beachvolleyball natural=beach"
                # assertNoMatch:"node sport=skiing"
                # assertNoMatch:"node sport=swimming tourism=hotel"
                # assertNoMatch:"node sport=tennis leisure=pitch"
                # assertMatch:"node sport=tennis"
                err.append({'class': 9001001, 'subclass': 1531133249, 'text': mapcss.tr(u'sport without physical feature')})

        # *[building:levels][!building][!building:part]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and not mapcss._tag_capture(capture_tags, 2, tags, u'building:part'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001001, 'subclass': 1821512557, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[/_name$/][!name][!old_name][!loc_name][!uic_name][!artist_name][!lock_name][!"osak:municipality_name"][!"osak:street_name"][noname!=yes]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_25d98c90) and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'old_name') and not mapcss._tag_capture(capture_tags, 3, tags, u'loc_name') and not mapcss._tag_capture(capture_tags, 4, tags, u'uic_name') and not mapcss._tag_capture(capture_tags, 5, tags, u'artist_name') and not mapcss._tag_capture(capture_tags, 6, tags, u'lock_name') and not mapcss._tag_capture(capture_tags, 7, tags, u'osak:municipality_name') and not mapcss._tag_capture(capture_tags, 8, tags, u'osak:street_name') and mapcss._tag_capture(capture_tags, 9, tags, u'noname') != mapcss._value_capture(capture_tags, 9, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("alternative name without {0}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1070694429, 'text': mapcss.tr(u'alternative name without {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[unisex=yes][female=yes][male!=yes][shop=hairdresser]
        # *[unisex=yes][male=yes][female!=yes][shop=hairdresser]
        if (u'male' in keys and u'shop' in keys and u'unisex' in keys) or (u'female' in keys and u'shop' in keys and u'unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'female') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'male') != mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'male') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'female') != mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1043941827, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[unisex=yes][female=yes][male=yes][shop=hairdresser]
        if (u'female' in keys and u'male' in keys and u'shop' in keys and u'unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'female') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'male') == mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {1} and {2}","{0.tag}","{1.tag}","{2.tag}")
                # fixRemove:"female"
                # fixRemove:"male"
                err.append({'class': 9001002, 'subclass': 408307546, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {1} and {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'female',
                    u'male'])
                }})

        # *[female=yes][male=yes][!unisex][shop=hairdresser]
        if (u'female' in keys and u'male' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'female') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'male') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'unisex') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"unisex=yes"
                # fixRemove:"female"
                # fixRemove:"male"
                # fixAdd:"unisex=yes"
                err.append({'class': 9001002, 'subclass': 831595594, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'unisex',u'yes']]),
                    '-': ([
                    u'female',
                    u'male'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_AllSameMaxspeed = False

        # way[junction][!highway][junction!=yes]
        # way[lanes][!highway][leisure!=track][leisure!=swimming_pool]
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
        # way[stream][!waterway]
        # way[length_unit][!waterway]
        # way[canal][!waterway]
        # way[have_riverbank][!waterway]
        # *[border_type][!boundary]
        # *[piste:difficulty][!piste:type]
        # *[source:date][!source]
        # *[source:name][!name]
        # *[source:maxspeed:forward][!maxspeed:forward][!maxspeed]
        # *[source:maxspeed:backward][!maxspeed:backward][!maxspeed]
        # *[source:building][!building]
        # *[source:ref][!ref]
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
        # *[source:addr][!/^addr:/]
        # *[source:maxspeed][!/^maxspeed:?/]
        if (u'border_type' in keys) or (u'canal' in keys) or (u'detail' in keys) or (u'eddy_current_brake' in keys) or (u'electrified' in keys) or (u'etcs' in keys) or (u'gauge' in keys) or (u'grade_of_track' in keys) or (u'have_riverbank' in keys) or (u'junction' in keys) or (u'kursbuchstrecke' in keys) or (u'lanes' in keys) or (u'length_unit' in keys) or (u'living_street' in keys) or (u'lzb' in keys) or (u'maintenance' in keys) or (u'median' in keys) or (u'motorroad' in keys) or (u'old_railway_operator' in keys) or (u'operating_procedure' in keys) or (u'piste:difficulty' in keys) or (u'pzb' in keys) or (u'sac_scale' in keys) or (u'sidewalk' in keys) or (u'source:addr' in keys) or (u'source:addr:housenumber' in keys) or (u'source:addr:postcode' in keys) or (u'source:bicycle' in keys) or (u'source:bridge' in keys) or (u'source:building' in keys) or (u'source:date' in keys) or (u'source:designation' in keys) or (u'source:ele' in keys) or (u'source:height' in keys) or (u'source:hgv' in keys) or (u'source:highway' in keys) or (u'source:housenumber' in keys) or (u'source:lanes' in keys) or (u'source:lit' in keys) or (u'source:maxaxleload' in keys) or (u'source:maxspeed' in keys) or (u'source:maxspeed:backward' in keys) or (u'source:maxspeed:forward' in keys) or (u'source:name' in keys) or (u'source:old_name' in keys) or (u'source:population' in keys) or (u'source:postal_code' in keys) or (u'source:postcode' in keys) or (u'source:ref' in keys) or (u'source:ref:INSEE' in keys) or (u'source:surface' in keys) or (u'step_count' in keys) or (u'stream' in keys) or (u'structure_gauge' in keys) or (u'tilting_technology' in keys) or (u'track_class' in keys) or (u'tracks' in keys) or (u'tracktype' in keys) or (u'traffic_mode' in keys) or (u'trail_visibility' in keys) or (u'trolley_wire' in keys) or (u'workrules' in keys) or (u'zip_left' in keys) or (u'zip_right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'junction') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and mapcss._tag_capture(capture_tags, 2, tags, u'junction') != mapcss._value_capture(capture_tags, 2, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lanes') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') != mapcss._value_capture(capture_tags, 2, u'track') and mapcss._tag_capture(capture_tags, 3, tags, u'leisure') != mapcss._value_capture(capture_tags, 3, u'swimming_pool'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'living_street') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maintenance') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'median') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'motorroad') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sac_scale') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sidewalk') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'step_count') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') != mapcss._value_capture(capture_tags, 2, u'tower'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'trail_visibility') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'trolley_wire') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'zip_left') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'zip_right') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'detail') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'eddy_current_brake') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'electrified') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'etcs') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'gauge') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'grade_of_track') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'kursbuchstrecke') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'lzb') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'old_railway_operator') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'operating_procedure') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'pzb') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'structure_gauge') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tilting_technology') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'track_class') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tracks') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'traffic_mode') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'workrules') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and mapcss._tag_capture(capture_tags, 2, tags, u'route') != mapcss._value_capture(capture_tags, 2, u'railway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'stream') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'length_unit') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'canal') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'have_riverbank') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'border_type') and not mapcss._tag_capture(capture_tags, 1, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'piste:difficulty') and not mapcss._tag_capture(capture_tags, 1, tags, u'piste:type'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:date') and not mapcss._tag_capture(capture_tags, 1, tags, u'source'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:name') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed:forward') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:forward') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed:backward') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:backward') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:building') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ref') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:population') and not mapcss._tag_capture(capture_tags, 1, tags, u'population'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:postal_code') and not mapcss._tag_capture(capture_tags, 1, tags, u'postal_code'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ele') and not mapcss._tag_capture(capture_tags, 1, tags, u'ele'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ref:INSEE') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:INSEE'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:lit') and not mapcss._tag_capture(capture_tags, 1, tags, u'lit'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:hgv') and not mapcss._tag_capture(capture_tags, 1, tags, u'hgv'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:highway') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxaxleload') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxaxleload'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:surface') and not mapcss._tag_capture(capture_tags, 1, tags, u'surface'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:bridge') and not mapcss._tag_capture(capture_tags, 1, tags, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:old_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:bicycle') and not mapcss._tag_capture(capture_tags, 1, tags, u'bicycle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:designation') and not mapcss._tag_capture(capture_tags, 1, tags, u'designation'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:height') and not mapcss._tag_capture(capture_tags, 1, tags, u'height'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:lanes') and not mapcss._tag_capture(capture_tags, 1, tags, u'lanes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:postcode') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:housenumber') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr:postcode') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr:housenumber') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr') and not mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, self.re_050395e0))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                # assertNoMatch:"way lanes=42 highway=unclassified"
                # assertMatch:"way lanes=42"
                err.append({'class': 9001001, 'subclass': 1275753529, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[transformer][!power]
        # way[fence_type][barrier!=fence]
        # *[recycling_type][amenity!=recycling]
        # *[information][tourism!=information]
        # *[shelter_type][amenity!=shelter]
        # *[site_type][historic!=archaeological_site]
        # *[artwork_type][tourism!=artwork][exhibit!=artwork]
        # *[castle_type][historic!=castle]
        # *[parking][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking)$/]
        # way[cutline][man_made!=cutline]
        # *[bunker_type][military!=bunker]
        if (u'artwork_type' in keys) or (u'bunker_type' in keys) or (u'castle_type' in keys) or (u'cutline' in keys) or (u'fence_type' in keys) or (u'information' in keys) or (u'parking' in keys) or (u'recycling_type' in keys) or (u'shelter_type' in keys) or (u'site_type' in keys) or (u'transformer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'transformer') and not mapcss._tag_capture(capture_tags, 1, tags, u'power'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fence_type') and mapcss._tag_capture(capture_tags, 1, tags, u'barrier') != mapcss._value_capture(capture_tags, 1, u'fence'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'recycling_type') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'recycling'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'information') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'information'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shelter_type') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'shelter'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'site_type') and mapcss._tag_capture(capture_tags, 1, tags, u'historic') != mapcss._value_capture(capture_tags, 1, u'archaeological_site'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'artwork_type') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'artwork') and mapcss._tag_capture(capture_tags, 2, tags, u'exhibit') != mapcss._value_capture(capture_tags, 2, u'artwork'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'castle_type') and mapcss._tag_capture(capture_tags, 1, tags, u'historic') != mapcss._value_capture(capture_tags, 1, u'castle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'parking') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5cf0a79f), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cutline') and mapcss._tag_capture(capture_tags, 1, tags, u'man_made') != mapcss._value_capture(capture_tags, 1, u'cutline'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bunker_type') and mapcss._tag_capture(capture_tags, 1, tags, u'military') != mapcss._value_capture(capture_tags, 1, u'bunker'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1572004164, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[bridge:movable][bridge!=movable][man_made!=bridge]
        # *[substation][power!=substation][pipeline!=substation]
        # *[reservoir_type][landuse!=reservoir][water!=reservoir]
        # way[waterway=pressurised][tunnel!=flooded][man_made!=pipeline]
        if (u'bridge:movable' in keys) or (u'reservoir_type' in keys) or (u'substation' in keys) or (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge:movable') and mapcss._tag_capture(capture_tags, 1, tags, u'bridge') != mapcss._value_capture(capture_tags, 1, u'movable') and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') != mapcss._value_capture(capture_tags, 2, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'substation') and mapcss._tag_capture(capture_tags, 1, tags, u'power') != mapcss._value_capture(capture_tags, 1, u'substation') and mapcss._tag_capture(capture_tags, 2, tags, u'pipeline') != mapcss._value_capture(capture_tags, 2, u'substation'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'reservoir_type') and mapcss._tag_capture(capture_tags, 1, tags, u'landuse') != mapcss._value_capture(capture_tags, 1, u'reservoir') and mapcss._tag_capture(capture_tags, 2, tags, u'water') != mapcss._value_capture(capture_tags, 2, u'reservoir'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'pressurised') and mapcss._tag_capture(capture_tags, 1, tags, u'tunnel') != mapcss._value_capture(capture_tags, 1, u'flooded') and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') != mapcss._value_capture(capture_tags, 2, u'pipeline'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 214618643, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # way[boundary=administrative][!admin_level]
        # *[tourism=information][!information]
        # *[leisure=pitch][!sport]
        # *[aeroway=terminal][!building]
        # *[power=generator][!generator:source]
        # *[amenity=social_facility][!social_facility]
        # *[amenity=place_of_worship][!religion]
        if (u'aeroway' in keys) or (u'amenity' in keys) or (u'boundary' in keys) or (u'leisure' in keys) or (u'power' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'administrative') and not mapcss._tag_capture(capture_tags, 1, tags, u'admin_level'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'information') and not mapcss._tag_capture(capture_tags, 1, tags, u'information'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and not mapcss._tag_capture(capture_tags, 1, tags, u'sport'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'terminal') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'generator') and not mapcss._tag_capture(capture_tags, 1, tags, u'generator:source'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'social_facility') and not mapcss._tag_capture(capture_tags, 1, tags, u'social_facility'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'place_of_worship') and not mapcss._tag_capture(capture_tags, 1, tags, u'religion'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 9001001, 'subclass': 2131175041, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[bridge:structure][!bridge][man_made!=bridge]
        # *[smoothness][!highway][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$/]
        # *[segregated][!highway][railway!=crossing]
        if (u'bridge:structure' in keys) or (u'segregated' in keys) or (u'smoothness' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge:structure') and not mapcss._tag_capture(capture_tags, 1, tags, u'bridge') and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') != mapcss._value_capture(capture_tags, 2, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'smoothness') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_4f156c8f), mapcss._tag_capture(capture_tags, 2, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'segregated') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != mapcss._value_capture(capture_tags, 2, u'crossing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1340059227, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # way[usage=penstock][man_made!=pipeline]
        # way[usage=penstock][waterway!=pressurised]
        if (u'usage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'usage') == mapcss._value_capture(capture_tags, 0, u'penstock') and mapcss._tag_capture(capture_tags, 1, tags, u'man_made') != mapcss._value_capture(capture_tags, 1, u'pipeline'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'usage') == mapcss._value_capture(capture_tags, 0, u'penstock') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') != mapcss._value_capture(capture_tags, 1, u'pressurised'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 758205383, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[amenity=recycling][recycling_type!=container][recycling_type!=centre]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'recycling') and mapcss._tag_capture(capture_tags, 1, tags, u'recycling_type') != mapcss._value_capture(capture_tags, 1, u'container') and mapcss._tag_capture(capture_tags, 2, tags, u'recycling_type') != mapcss._value_capture(capture_tags, 2, u'centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 747056792, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # *[intermittent][!waterway][natural!~/^(water|spring)$/][landuse!~/^(basin|reservoir)$/][ford!=yes]
        # *[boat][!waterway][natural!=water][landuse!~/^(basin|reservoir)$/][ford!=yes]
        if (u'boat' in keys) or (u'intermittent' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'intermittent') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_4fbfe59b), mapcss._tag_capture(capture_tags, 2, tags, u'natural')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_0889a956), mapcss._tag_capture(capture_tags, 3, tags, u'landuse')) and mapcss._tag_capture(capture_tags, 4, tags, u'ford') != mapcss._value_capture(capture_tags, 4, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boat') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and mapcss._tag_capture(capture_tags, 2, tags, u'natural') != mapcss._value_capture(capture_tags, 2, u'water') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_0889a956), mapcss._tag_capture(capture_tags, 3, tags, u'landuse')) and mapcss._tag_capture(capture_tags, 4, tags, u'ford') != mapcss._value_capture(capture_tags, 4, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1096267911, 'text': mapcss.tr(u'{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'), mapcss._tag_uncapture(capture_tags, u'{3.tag}'), mapcss._tag_uncapture(capture_tags, u'{4.tag}'))})

        # way[oneway][!highway][!railway][!aerialway]
        # *[snowplowing][!highway][!amenity][!leisure]
        if (u'oneway' in keys) or (u'snowplowing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'aerialway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'snowplowing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'amenity') and not mapcss._tag_capture(capture_tags, 3, tags, u'leisure'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.key}")
                err.append({'class': 9001001, 'subclass': 1335922311, 'text': mapcss.tr(u'{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{3.key}'))})

        # way[incline][!highway][!railway][aeroway!~/^(runway|taxiway)$/]
        # *[toll][!highway][!barrier][route!~/^(ferry|road)$/]
        if (u'incline' in keys) or (u'toll' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'incline') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_1dcd648f), mapcss._tag_capture(capture_tags, 3, tags, u'aeroway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'toll') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'barrier') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_5ee853b2), mapcss._tag_capture(capture_tags, 3, tags, u'route')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 413139586, 'text': mapcss.tr(u'{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{3.tag}'))})

        # *[internet_access=no][internet_access:fee]
        # *[amenity=vending_machine][shop]
        # *[noname?][name]
        # way[oneway=yes][/:backward/][!traffic_sign:backward][bicycle:backward!=use_sidepath][oneway:bicycle!=no][oneway:psv!=no]
        # way[oneway=yes][/:forward/][!traffic_sign:forward][bicycle:forward!=use_sidepath][oneway:bicycle!=no][oneway:psv!=no]
        # way[oneway=-1][/:backward/][!traffic_sign:backward][bicycle:backward!=use_sidepath][oneway:bicycle!=no][oneway:psv!=no]
        # way[oneway=-1][/:forward/][!traffic_sign:forward][bicycle:forward!=use_sidepath][oneway:bicycle!=no][oneway:psv!=no]
        if (u'internet_access' in keys and u'internet_access:fee' in keys) or (u'name' in keys and u'noname' in keys) or (u'oneway' in keys) or (u'amenity' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'internet_access') == mapcss._value_capture(capture_tags, 0, u'no') and mapcss._tag_capture(capture_tags, 1, tags, u'internet_access:fee'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'vending_machine') and mapcss._tag_capture(capture_tags, 1, tags, u'shop'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noname') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, self.re_7346b495) and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign:backward') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle:backward') != mapcss._value_capture(capture_tags, 3, u'use_sidepath') and mapcss._tag_capture(capture_tags, 4, tags, u'oneway:bicycle') != mapcss._value_capture(capture_tags, 4, u'no') and mapcss._tag_capture(capture_tags, 5, tags, u'oneway:psv') != mapcss._value_capture(capture_tags, 5, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, self.re_12ce6b85) and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign:forward') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle:forward') != mapcss._value_capture(capture_tags, 3, u'use_sidepath') and mapcss._tag_capture(capture_tags, 4, tags, u'oneway:bicycle') != mapcss._value_capture(capture_tags, 4, u'no') and mapcss._tag_capture(capture_tags, 5, tags, u'oneway:psv') != mapcss._value_capture(capture_tags, 5, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') == mapcss._value_capture(capture_tags, 0, -1) and mapcss._tag_capture(capture_tags, 1, tags, self.re_7346b495) and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign:backward') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle:backward') != mapcss._value_capture(capture_tags, 3, u'use_sidepath') and mapcss._tag_capture(capture_tags, 4, tags, u'oneway:bicycle') != mapcss._value_capture(capture_tags, 4, u'no') and mapcss._tag_capture(capture_tags, 5, tags, u'oneway:psv') != mapcss._value_capture(capture_tags, 5, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') == mapcss._value_capture(capture_tags, 0, -1) and mapcss._tag_capture(capture_tags, 1, tags, self.re_12ce6b85) and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign:forward') and mapcss._tag_capture(capture_tags, 3, tags, u'bicycle:forward') != mapcss._value_capture(capture_tags, 3, u'use_sidepath') and mapcss._tag_capture(capture_tags, 4, tags, u'oneway:bicycle') != mapcss._value_capture(capture_tags, 4, u'no') and mapcss._tag_capture(capture_tags, 5, tags, u'oneway:psv') != mapcss._value_capture(capture_tags, 5, u'no'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1074257170, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[segregated][bicycle=no]
        # way[segregated][foot=no]
        # way[man_made=pipeline][tunnel=flooded]
        # way[waterway=canal][tunnel=yes]
        # way[highway=footway][bicycle=designated]
        if (u'foot' in keys and u'segregated' in keys) or (u'bicycle' in keys and u'highway' in keys) or (u'bicycle' in keys and u'segregated' in keys) or (u'man_made' in keys and u'tunnel' in keys) or (u'tunnel' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'segregated') and mapcss._tag_capture(capture_tags, 1, tags, u'bicycle') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'segregated') and mapcss._tag_capture(capture_tags, 1, tags, u'foot') == mapcss._value_capture(capture_tags, 1, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'pipeline') and mapcss._tag_capture(capture_tags, 1, tags, u'tunnel') == mapcss._value_capture(capture_tags, 1, u'flooded'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'canal') and mapcss._tag_capture(capture_tags, 1, tags, u'tunnel') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'footway') and mapcss._tag_capture(capture_tags, 1, tags, u'bicycle') == mapcss._value_capture(capture_tags, 1, u'designated'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1606678840, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[waterway][bridge=yes][waterway!=weir]
        if (u'bridge' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'bridge') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'waterway') != mapcss._value_capture(capture_tags, 2, u'weir'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.tag}")
                # suggestAlternative:"bridge=aqueduct"
                # fixAdd:"bridge=aqueduct"
                err.append({'class': 9001002, 'subclass': 1036780075, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'bridge',u'aqueduct']])
                }})

        # way[waterway=weir][bridge=yes][highway]
        if (u'bridge' in keys and u'highway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'weir') and mapcss._tag_capture(capture_tags, 1, tags, u'bridge') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # suggestAlternative:tr("two objects, one with {0} and one with {1} + {2} + {3}","{0.tag}","{2.key}","{1.tag}","layer")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"waterway=dam"
                # suggestAlternative:"waterway=weir + ford=yes"
                err.append({'class': 9001002, 'subclass': 842989092, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[access][eval(number_of_tags())=1]
        # *[area][eval(number_of_tags())=1]!.area_yes_autofix
        # *[name][eval(number_of_tags())=1]
        # *[ref][eval(number_of_tags())=1]
        # *[lit][eval(number_of_tags())=1]
        # Use undeclared class area_yes_autofix

        # *[name][area][eval(number_of_tags())=2]
        # *[name][ref][eval(number_of_tags())=2]
        if (u'area' in keys and u'name' in keys) or (u'name' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'area') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 788702375, 'text': mapcss.tr(u'incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[tourism=attraction][eval(number_of_tags())=1]
        if (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'attraction') and len(tags) == 1)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0}","{0.tag}")
                err.append({'class': 9001001, 'subclass': 463560683, 'text': mapcss.tr(u'incomplete object: only {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name][tourism=attraction][eval(number_of_tags())=2]
        if (u'name' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') == mapcss._value_capture(capture_tags, 1, u'attraction') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 34376505, 'text': mapcss.tr(u'incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[place][place!=farm][/^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$/]
        # *[boundary][/^addr:/]
        # *[highway][/^addr:/][highway!=services][highway!=rest_area][!"addr:postcode"]
        if (u'boundary' in keys) or (u'highway' in keys) or (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') != mapcss._value_capture(capture_tags, 1, u'farm') and mapcss._tag_capture(capture_tags, 2, tags, self.re_0737b0c4))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') and mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835) and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'services') and mapcss._tag_capture(capture_tags, 3, tags, u'highway') != mapcss._value_capture(capture_tags, 3, u'rest_area') and not mapcss._tag_capture(capture_tags, 4, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with addr:*","{0.key}")
                err.append({'class': 9001002, 'subclass': 2039567622, 'text': mapcss.tr(u'{0} together with addr:*', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][postal_code]["addr:postcode"][postal_code=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 1341956372, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[!highway][postal_code]["addr:postcode"][postal_code!=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 1415856502, 'text': mapcss.tr(u'{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # way[highway][postal_code]["addr:postcode"][postal_code=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'highway' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{1.key}","{2.key}")
                # fixRemove:"addr:postcode"
                err.append({'class': 9001002, 'subclass': 1035459161, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'addr:postcode'])
                }})

        # way[highway][postal_code]["addr:postcode"][postal_code!=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'highway' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 902503316, 'text': mapcss.tr(u'{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # way[highway][highway!=services][highway!=rest_area][!postal_code]["addr:postcode"]
        if (u'addr:postcode' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') != mapcss._value_capture(capture_tags, 1, u'services') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'rest_area') and not mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 4, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{4.key}")
                # suggestAlternative:"postal_code"
                # fixChangeKey:"addr:postcode=>postal_code"
                err.append({'class': 9001002, 'subclass': 1784225201, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{4.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'postal_code', mapcss.tag(tags, u'addr:postcode')]]),
                    '-': ([
                    u'addr:postcode'])
                }})

        # way[highway=footway][cycleway=lane]
        if (u'cycleway' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'footway') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway') == mapcss._value_capture(capture_tags, 1, u'lane'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"highway=path + foot=designated + bicycle=designated + segregated=yes"
                err.append({'class': 9001002, 'subclass': 393240150, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[tunnel][!highway][!railway][!waterway][!piste:type][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor]
        # *[bridge][!highway][!railway][!waterway][!piste:type][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=bridge][building!=bridge]
        # *[psv][!highway][!railway][!waterway][amenity!~/^parking.*/]
        # *[width][!highway][!railway][!waterway][!aeroway][!cycleway][!footway][!barrier][!man_made][!entrance][natural!=stone]
        # *[maxspeed][!highway][!railway][traffic_sign!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][type!=enforcement][waterway!~/^(river|canal|lock)$/][!traffic_calming][aerialway!=zip_line]
        if (u'bridge' in keys) or (u'maxspeed' in keys) or (u'psv' in keys) or (u'tunnel' in keys) or (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tunnel') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 5, tags, u'public_transport') != mapcss._value_capture(capture_tags, 5, u'platform') and mapcss._tag_capture(capture_tags, 6, tags, u'route') != mapcss._value_capture(capture_tags, 6, u'ferry') and mapcss._tag_capture(capture_tags, 7, tags, u'man_made') != mapcss._value_capture(capture_tags, 7, u'pipeline') and mapcss._tag_capture(capture_tags, 8, tags, u'man_made') != mapcss._value_capture(capture_tags, 8, u'goods_conveyor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 5, tags, u'public_transport') != mapcss._value_capture(capture_tags, 5, u'platform') and mapcss._tag_capture(capture_tags, 6, tags, u'route') != mapcss._value_capture(capture_tags, 6, u'ferry') and mapcss._tag_capture(capture_tags, 7, tags, u'man_made') != mapcss._value_capture(capture_tags, 7, u'pipeline') and mapcss._tag_capture(capture_tags, 8, tags, u'man_made') != mapcss._value_capture(capture_tags, 8, u'goods_conveyor') and mapcss._tag_capture(capture_tags, 9, tags, u'man_made') != mapcss._value_capture(capture_tags, 9, u'bridge') and mapcss._tag_capture(capture_tags, 10, tags, u'building') != mapcss._value_capture(capture_tags, 10, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'psv') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 4, self.re_213d4d09), mapcss._tag_capture(capture_tags, 4, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'width') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'aeroway') and not mapcss._tag_capture(capture_tags, 5, tags, u'cycleway') and not mapcss._tag_capture(capture_tags, 6, tags, u'footway') and not mapcss._tag_capture(capture_tags, 7, tags, u'barrier') and not mapcss._tag_capture(capture_tags, 8, tags, u'man_made') and not mapcss._tag_capture(capture_tags, 9, tags, u'entrance') and mapcss._tag_capture(capture_tags, 10, tags, u'natural') != mapcss._value_capture(capture_tags, 10, u'stone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_27d9cb1c), mapcss._tag_capture(capture_tags, 3, tags, u'traffic_sign')) and mapcss._tag_capture(capture_tags, 4, tags, u'type') != mapcss._value_capture(capture_tags, 4, u'enforcement') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 5, self.re_46fc3877), mapcss._tag_capture(capture_tags, 5, tags, u'waterway')) and not mapcss._tag_capture(capture_tags, 6, tags, u'traffic_calming') and mapcss._tag_capture(capture_tags, 7, tags, u'aerialway') != mapcss._value_capture(capture_tags, 7, u'zip_line'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} on suspicious object","{0.key}")
                err.append({'class': 9001002, 'subclass': 755649879, 'text': mapcss.tr(u'{0} on suspicious object', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway][barrier]
        # *[highway][waterway][waterway!=dam][waterway!=weir]
        # way[highway][natural][natural!=ridge]
        # *[landuse][building][landuse!=retail]
        if (u'building' in keys and u'landuse' in keys) or (u'barrier' in keys and u'highway' in keys) or (u'highway' in keys and u'natural' in keys) or (u'highway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'barrier'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and mapcss._tag_capture(capture_tags, 2, tags, u'waterway') != mapcss._value_capture(capture_tags, 2, u'dam') and mapcss._tag_capture(capture_tags, 3, tags, u'waterway') != mapcss._value_capture(capture_tags, 3, u'weir'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'natural') and mapcss._tag_capture(capture_tags, 2, tags, u'natural') != mapcss._value_capture(capture_tags, 2, u'ridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'landuse') != mapcss._value_capture(capture_tags, 2, u'retail'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 636059786, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[natural=water][leisure=swimming_pool]
        if (u'leisure' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'water') and mapcss._tag_capture(capture_tags, 1, tags, u'leisure') == mapcss._value_capture(capture_tags, 1, u'swimming_pool'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("natural water used for swimming pool")
                # fixRemove:"natural"
                err.append({'class': 9001002, 'subclass': 608817213, 'text': mapcss.tr(u'natural water used for swimming pool'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'natural'])
                }})

        # *[sport][sport!=skiing][!building][!club][tourism!=hotel][highway!=raceway][!leisure][natural!~/^(beach|bare_rock|cliff|peak|water)$/][amenity!~/^(pub|restaurant|swimming_pool)$/][landuse!~/^(recreation_ground|piste|farm|farmland)$/][barrier!~/^(wall|retaining_wall)$/][!"piste:type"][shop!=sports]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') != mapcss._value_capture(capture_tags, 1, u'skiing') and not mapcss._tag_capture(capture_tags, 2, tags, u'building') and not mapcss._tag_capture(capture_tags, 3, tags, u'club') and mapcss._tag_capture(capture_tags, 4, tags, u'tourism') != mapcss._value_capture(capture_tags, 4, u'hotel') and mapcss._tag_capture(capture_tags, 5, tags, u'highway') != mapcss._value_capture(capture_tags, 5, u'raceway') and not mapcss._tag_capture(capture_tags, 6, tags, u'leisure') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 7, self.re_29fa4401), mapcss._tag_capture(capture_tags, 7, tags, u'natural')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 8, self.re_64c931ef), mapcss._tag_capture(capture_tags, 8, tags, u'amenity')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 9, self.re_3b4f8f73), mapcss._tag_capture(capture_tags, 9, tags, u'landuse')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 10, self.re_68c05e86), mapcss._tag_capture(capture_tags, 10, tags, u'barrier')) and not mapcss._tag_capture(capture_tags, 11, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 12, tags, u'shop') != mapcss._value_capture(capture_tags, 12, u'sports'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("sport without physical feature")
                err.append({'class': 9001001, 'subclass': 1531133249, 'text': mapcss.tr(u'sport without physical feature')})

        # *[building:levels][!building][!building:part]
        # way[usage][!railway][!waterway][route!=railway][man_made!=pipeline]
        if (u'building:levels' in keys) or (u'usage' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and not mapcss._tag_capture(capture_tags, 2, tags, u'building:part'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'usage') and not mapcss._tag_capture(capture_tags, 1, tags, u'railway') and not mapcss._tag_capture(capture_tags, 2, tags, u'waterway') and mapcss._tag_capture(capture_tags, 3, tags, u'route') != mapcss._value_capture(capture_tags, 3, u'railway') and mapcss._tag_capture(capture_tags, 4, tags, u'man_made') != mapcss._value_capture(capture_tags, 4, u'pipeline'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001001, 'subclass': 1032721815, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[/_name$/][!name][!old_name][!loc_name][!uic_name][!artist_name][!lock_name][!"osak:municipality_name"][!"osak:street_name"][noname!=yes]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_25d98c90) and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'old_name') and not mapcss._tag_capture(capture_tags, 3, tags, u'loc_name') and not mapcss._tag_capture(capture_tags, 4, tags, u'uic_name') and not mapcss._tag_capture(capture_tags, 5, tags, u'artist_name') and not mapcss._tag_capture(capture_tags, 6, tags, u'lock_name') and not mapcss._tag_capture(capture_tags, 7, tags, u'osak:municipality_name') and not mapcss._tag_capture(capture_tags, 8, tags, u'osak:street_name') and mapcss._tag_capture(capture_tags, 9, tags, u'noname') != mapcss._value_capture(capture_tags, 9, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("alternative name without {0}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1070694429, 'text': mapcss.tr(u'alternative name without {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[destination][!oneway?][junction!=roundabout][highway]
        if (u'destination' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'destination') and not mapcss._tag_capture(capture_tags, 1, tags, u'oneway') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 2, tags, u'junction') != mapcss._value_capture(capture_tags, 2, u'roundabout') and mapcss._tag_capture(capture_tags, 3, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("incomplete usage of {0} on a way without {1}","{0.key}","{1.key}")
                # suggestAlternative:"destination:backward"
                # suggestAlternative:"destination:forward"
                err.append({'class': 9001004, 'subclass': 915799973, 'text': mapcss.tr(u'incomplete usage of {0} on a way without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way["maxspeed:forward"=*"maxspeed:backward"][!maxspeed]
        if (u'maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:forward') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'maxspeed:backward')) and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
                # suggestAlternative:"maxspeed"
                # fixRemove:"maxspeed:backward"
                # fixChangeKey:"maxspeed:forward=>maxspeed"
                err.append({'class': 9001002, 'subclass': 1534863867, 'text': mapcss.tr(u'Same value of {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'maxspeed', mapcss.tag(tags, u'maxspeed:forward')]]),
                    '-': ([
                    u'maxspeed:backward',
                    u'maxspeed:forward'])
                }})

        # way["maxspeed:forward"=*maxspeed]["maxspeed:backward"=*maxspeed][maxspeed]
        if (u'maxspeed' in keys and u'maxspeed:backward' in keys and u'maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:forward') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'maxspeed')) and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:backward') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'maxspeed')) and mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if match:
                # setAllSameMaxspeed
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Same value of {0}, {1} and {2}","{0.key}","{1.key}","{2.key}")
                # suggestAlternative:"maxspeed"
                # fixRemove:"maxspeed:backward"
                # fixRemove:"maxspeed:forward"
                set_AllSameMaxspeed = True
                err.append({'class': 9001002, 'subclass': 734184728, 'text': mapcss.tr(u'Same value of {0}, {1} and {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'maxspeed:backward',
                    u'maxspeed:forward'])
                }})

        # way["maxspeed:forward"]["maxspeed:backward"][maxspeed]!.AllSameMaxspeed
        if (u'maxspeed' in keys and u'maxspeed:backward' in keys and u'maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not set_AllSameMaxspeed and mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:forward') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:backward') and mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} and {1} together with {2} and conflicting values","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 1753674842, 'text': mapcss.tr(u'{0} and {1} together with {2} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # way["maxspeed:forward"][maxspeed][!"maxspeed:backward"]
        # way["maxspeed:backward"][maxspeed][!"maxspeed:forward"]
        if (u'maxspeed' in keys and u'maxspeed:backward' in keys) or (u'maxspeed' in keys and u'maxspeed:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:forward') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed:backward'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed:backward') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed:forward'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 174535527, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[layer][layer<0][bridge][bridge!=no][location!=underground][indoor!=yes][!tunnel]
        # way[layer][layer>0][tunnel][tunnel!=no][location!=overground][indoor!=yes][!bridge]
        if (u'bridge' in keys and u'layer' in keys) or (u'layer' in keys and u'tunnel' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < mapcss._value_capture(capture_tags, 1, 0) and mapcss._tag_capture(capture_tags, 2, tags, u'bridge') and mapcss._tag_capture(capture_tags, 3, tags, u'bridge') != mapcss._value_capture(capture_tags, 3, u'no') and mapcss._tag_capture(capture_tags, 4, tags, u'location') != mapcss._value_capture(capture_tags, 4, u'underground') and mapcss._tag_capture(capture_tags, 5, tags, u'indoor') != mapcss._value_capture(capture_tags, 5, u'yes') and not mapcss._tag_capture(capture_tags, 6, tags, u'tunnel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'layer') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > mapcss._value_capture(capture_tags, 1, 0) and mapcss._tag_capture(capture_tags, 2, tags, u'tunnel') and mapcss._tag_capture(capture_tags, 3, tags, u'tunnel') != mapcss._value_capture(capture_tags, 3, u'no') and mapcss._tag_capture(capture_tags, 4, tags, u'location') != mapcss._value_capture(capture_tags, 4, u'overground') and mapcss._tag_capture(capture_tags, 5, tags, u'indoor') != mapcss._value_capture(capture_tags, 5, u'yes') and not mapcss._tag_capture(capture_tags, 6, tags, u'bridge'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{2.tag}","{0.tag}")
                err.append({'class': 9001002, 'subclass': 1563148874, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{2.tag}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[waterway][layer][layer=~/^(-1|-2|-3|-4|-5)$/][!tunnel][culvert!=yes][covered!=yes][pipeline!=yes][location!=underground][eval(waylength())>400]
        # Part of rule not implemented

        # *[unisex=yes][female=yes][male!=yes][shop=hairdresser]
        # *[unisex=yes][male=yes][female!=yes][shop=hairdresser]
        if (u'male' in keys and u'shop' in keys and u'unisex' in keys) or (u'female' in keys and u'shop' in keys and u'unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'female') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'male') != mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'male') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'female') != mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1043941827, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[unisex=yes][female=yes][male=yes][shop=hairdresser]
        if (u'female' in keys and u'male' in keys and u'shop' in keys and u'unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'female') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'male') == mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {1} and {2}","{0.tag}","{1.tag}","{2.tag}")
                # fixRemove:"female"
                # fixRemove:"male"
                err.append({'class': 9001002, 'subclass': 408307546, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {1} and {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'female',
                    u'male'])
                }})

        # *[female=yes][male=yes][!unisex][shop=hairdresser]
        if (u'female' in keys and u'male' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'female') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'male') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'unisex') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"unisex=yes"
                # fixRemove:"female"
                # fixRemove:"male"
                # fixAdd:"unisex=yes"
                err.append({'class': 9001002, 'subclass': 831595594, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'unisex',u'yes']]),
                    '-': ([
                    u'female',
                    u'male'])
                }})

        # way!:closed[water][natural!~/water|bay|strait/][water!=intermittent]
        if (u'water' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'water') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_521b2098), mapcss._tag_capture(capture_tags, 1, tags, u'natural')) and mapcss._tag_capture(capture_tags, 2, tags, u'water') != mapcss._value_capture(capture_tags, 2, u'intermittent') and nds[0] == nds[-1])
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{1.key}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 2074767689, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/][lanes][turn:lanes][tag(lanes)!=eval(count(split("|",tag("turn:lanes"))))]
        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/][lanes][change:lanes][tag(lanes)!=eval(count(split("|",tag("change:lanes"))))]
        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/][lanes][maxspeed:lanes][tag(lanes)!=eval(count(split("|",tag("maxspeed:lanes"))))]
        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/][lanes][minspeed:lanes][tag(lanes)!=eval(count(split("|",tag("minspeed:lanes"))))]
        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/][lanes][destination:lanes][tag(lanes)!=eval(count(split("|",tag("destination:lanes"))))]
        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/][lanes][destination:ref:lanes][tag(lanes)!=eval(count(split("|",tag("destination:ref:lanes"))))]
        # way[highway=~/^(motorway|motorway_link|trunk|trunk_link)$/][lanes][destination:symbol:lanes][tag(lanes)!=eval(count(split("|",tag("destination:symbol:lanes"))))]
        if (u'destination:lanes' in keys and u'highway' in keys and u'lanes' in keys) or (u'destination:symbol:lanes' in keys and u'highway' in keys and u'lanes' in keys) or (u'change:lanes' in keys and u'highway' in keys and u'lanes' in keys) or (u'destination:ref:lanes' in keys and u'highway' in keys and u'lanes' in keys) or (u'highway' in keys and u'lanes' in keys and u'maxspeed:lanes' in keys) or (u'highway' in keys and u'lanes' in keys and u'minspeed:lanes' in keys) or (u'highway' in keys and u'lanes' in keys and u'turn:lanes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and mapcss._tag_capture(capture_tags, 2, tags, u'turn:lanes') and mapcss._tag_capture(capture_tags, 3, tags, u'lanes') != mapcss._value_capture(capture_tags, 3, mapcss.count(mapcss.split(u'|', mapcss.tag(tags, u'turn:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and mapcss._tag_capture(capture_tags, 2, tags, u'change:lanes') and mapcss._tag_capture(capture_tags, 3, tags, u'lanes') != mapcss._value_capture(capture_tags, 3, mapcss.count(mapcss.split(u'|', mapcss.tag(tags, u'change:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed:lanes') and mapcss._tag_capture(capture_tags, 3, tags, u'lanes') != mapcss._value_capture(capture_tags, 3, mapcss.count(mapcss.split(u'|', mapcss.tag(tags, u'maxspeed:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and mapcss._tag_capture(capture_tags, 2, tags, u'minspeed:lanes') and mapcss._tag_capture(capture_tags, 3, tags, u'lanes') != mapcss._value_capture(capture_tags, 3, mapcss.count(mapcss.split(u'|', mapcss.tag(tags, u'minspeed:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and mapcss._tag_capture(capture_tags, 2, tags, u'destination:lanes') and mapcss._tag_capture(capture_tags, 3, tags, u'lanes') != mapcss._value_capture(capture_tags, 3, mapcss.count(mapcss.split(u'|', mapcss.tag(tags, u'destination:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and mapcss._tag_capture(capture_tags, 2, tags, u'destination:ref:lanes') and mapcss._tag_capture(capture_tags, 3, tags, u'lanes') != mapcss._value_capture(capture_tags, 3, mapcss.count(mapcss.split(u'|', mapcss.tag(tags, u'destination:ref:lanes')))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_23888fca), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and mapcss._tag_capture(capture_tags, 2, tags, u'destination:symbol:lanes') and mapcss._tag_capture(capture_tags, 3, tags, u'lanes') != mapcss._value_capture(capture_tags, 3, mapcss.count(mapcss.split(u'|', mapcss.tag(tags, u'destination:symbol:lanes')))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("Different number of lanes in the keys {0} and {1}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 267306393, 'text': mapcss.tr(u'Different number of lanes in the keys {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # way[highway][lanes][!lanes:forward][!lanes:backward][oneway!=yes][oneway!=-1][junction!=roundabout][lanes>2][get(split(".",tag(lanes)/2),1)=5]
        if (u'highway' in keys and u'lanes' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') and not mapcss._tag_capture(capture_tags, 2, tags, u'lanes:forward') and not mapcss._tag_capture(capture_tags, 3, tags, u'lanes:backward') and mapcss._tag_capture(capture_tags, 4, tags, u'oneway') != mapcss._value_capture(capture_tags, 4, u'yes') and mapcss._tag_capture(capture_tags, 5, tags, u'oneway') != mapcss._value_capture(capture_tags, 5, -1) and mapcss._tag_capture(capture_tags, 6, tags, u'junction') != mapcss._value_capture(capture_tags, 6, u'roundabout') and mapcss._tag_capture(capture_tags, 7, tags, u'lanes') > mapcss._value_capture(capture_tags, 7, 2) and mapcss.get(mapcss.split(u'.', mapcss.tag(tags, u'lanes')/2), 1) == 5)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("street with odd number of {0}, but without {1} and {2} or {3}","{1.key}","{2.key}","{3.key}","{4.key}")
                # assertNoMatch:"way highway=primary lanes=2"
                # assertNoMatch:"way highway=primary lanes=3 lanes:backward=2"
                # assertNoMatch:"way highway=primary lanes=3 oneway=-1"
                # assertMatch:"way highway=primary lanes=3"
                # assertNoMatch:"way highway=primary lanes=4"
                err.append({'class': 9001001, 'subclass': 841292752, 'text': mapcss.tr(u'street with odd number of {0}, but without {1} and {2} or {3}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{3.key}'), mapcss._tag_uncapture(capture_tags, u'{4.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_AllSameMaxspeed = False

        # *[border_type][!boundary]
        # *[piste:difficulty][!piste:type]
        # *[source:date][!source]
        # *[source:name][!name]
        # *[source:maxspeed:forward][!maxspeed:forward][!maxspeed]
        # *[source:maxspeed:backward][!maxspeed:backward][!maxspeed]
        # *[source:building][!building]
        # *[source:ref][!ref]
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
        # *[source:addr][!/^addr:/]
        # *[source:maxspeed][!/^maxspeed:?/]
        if (u'border_type' in keys) or (u'piste:difficulty' in keys) or (u'source:addr' in keys) or (u'source:addr:housenumber' in keys) or (u'source:addr:postcode' in keys) or (u'source:bicycle' in keys) or (u'source:bridge' in keys) or (u'source:building' in keys) or (u'source:date' in keys) or (u'source:designation' in keys) or (u'source:ele' in keys) or (u'source:height' in keys) or (u'source:hgv' in keys) or (u'source:highway' in keys) or (u'source:housenumber' in keys) or (u'source:lanes' in keys) or (u'source:lit' in keys) or (u'source:maxaxleload' in keys) or (u'source:maxspeed' in keys) or (u'source:maxspeed:backward' in keys) or (u'source:maxspeed:forward' in keys) or (u'source:name' in keys) or (u'source:old_name' in keys) or (u'source:population' in keys) or (u'source:postal_code' in keys) or (u'source:postcode' in keys) or (u'source:ref' in keys) or (u'source:ref:INSEE' in keys) or (u'source:surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'border_type') and not mapcss._tag_capture(capture_tags, 1, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'piste:difficulty') and not mapcss._tag_capture(capture_tags, 1, tags, u'piste:type'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:date') and not mapcss._tag_capture(capture_tags, 1, tags, u'source'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:name') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed:forward') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:forward') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed:backward') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed:backward') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:building') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ref') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:population') and not mapcss._tag_capture(capture_tags, 1, tags, u'population'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:postal_code') and not mapcss._tag_capture(capture_tags, 1, tags, u'postal_code'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ele') and not mapcss._tag_capture(capture_tags, 1, tags, u'ele'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:ref:INSEE') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref:INSEE'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:lit') and not mapcss._tag_capture(capture_tags, 1, tags, u'lit'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:hgv') and not mapcss._tag_capture(capture_tags, 1, tags, u'hgv'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:highway') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxaxleload') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxaxleload'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:surface') and not mapcss._tag_capture(capture_tags, 1, tags, u'surface'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:bridge') and not mapcss._tag_capture(capture_tags, 1, tags, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:old_name') and not mapcss._tag_capture(capture_tags, 1, tags, u'old_name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:bicycle') and not mapcss._tag_capture(capture_tags, 1, tags, u'bicycle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:designation') and not mapcss._tag_capture(capture_tags, 1, tags, u'designation'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:height') and not mapcss._tag_capture(capture_tags, 1, tags, u'height'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:lanes') and not mapcss._tag_capture(capture_tags, 1, tags, u'lanes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:postcode') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:housenumber') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr:postcode') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr:housenumber') and not mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:addr') and not mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, self.re_050395e0))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 583462851, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[transformer][!power]
        # *[recycling_type][amenity!=recycling]
        # *[information][tourism!=information]
        # *[shelter_type][amenity!=shelter]
        # *[site_type][historic!=archaeological_site]
        # *[artwork_type][tourism!=artwork][exhibit!=artwork]
        # *[castle_type][historic!=castle]
        # *[parking][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking)$/]
        # *[bunker_type][military!=bunker]
        if (u'artwork_type' in keys) or (u'bunker_type' in keys) or (u'castle_type' in keys) or (u'information' in keys) or (u'parking' in keys) or (u'recycling_type' in keys) or (u'shelter_type' in keys) or (u'site_type' in keys) or (u'transformer' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'transformer') and not mapcss._tag_capture(capture_tags, 1, tags, u'power'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'recycling_type') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'recycling'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'information') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'information'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shelter_type') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'shelter'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'site_type') and mapcss._tag_capture(capture_tags, 1, tags, u'historic') != mapcss._value_capture(capture_tags, 1, u'archaeological_site'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'artwork_type') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'artwork') and mapcss._tag_capture(capture_tags, 2, tags, u'exhibit') != mapcss._value_capture(capture_tags, 2, u'artwork'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'castle_type') and mapcss._tag_capture(capture_tags, 1, tags, u'historic') != mapcss._value_capture(capture_tags, 1, u'castle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'parking') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5cf0a79f), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bunker_type') and mapcss._tag_capture(capture_tags, 1, tags, u'military') != mapcss._value_capture(capture_tags, 1, u'bunker'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 1270651182, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[bridge:movable][bridge!=movable][man_made!=bridge]
        # *[substation][power!=substation][pipeline!=substation]
        # *[reservoir_type][landuse!=reservoir][water!=reservoir]
        if (u'bridge:movable' in keys) or (u'reservoir_type' in keys) or (u'substation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge:movable') and mapcss._tag_capture(capture_tags, 1, tags, u'bridge') != mapcss._value_capture(capture_tags, 1, u'movable') and mapcss._tag_capture(capture_tags, 2, tags, u'man_made') != mapcss._value_capture(capture_tags, 2, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'substation') and mapcss._tag_capture(capture_tags, 1, tags, u'power') != mapcss._value_capture(capture_tags, 1, u'substation') and mapcss._tag_capture(capture_tags, 2, tags, u'pipeline') != mapcss._value_capture(capture_tags, 2, u'substation'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'reservoir_type') and mapcss._tag_capture(capture_tags, 1, tags, u'landuse') != mapcss._value_capture(capture_tags, 1, u'reservoir') and mapcss._tag_capture(capture_tags, 2, tags, u'water') != mapcss._value_capture(capture_tags, 2, u'reservoir'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1195794842, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

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
        # *[power=generator][!generator:source]
        # *[amenity=social_facility][!social_facility]
        # *[amenity=place_of_worship][!religion]
        if (u'aeroway' in keys) or (u'amenity' in keys) or (u'boundary' in keys) or (u'leisure' in keys) or (u'power' in keys) or (u'route' in keys and u'type' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'administrative') and not mapcss._tag_capture(capture_tags, 1, tags, u'admin_level'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'bicycle') and not mapcss._tag_capture(capture_tags, 1, tags, u'network') and mapcss._tag_capture(capture_tags, 2, tags, u'type') == mapcss._value_capture(capture_tags, 2, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'hiking') and not mapcss._tag_capture(capture_tags, 1, tags, u'network') and mapcss._tag_capture(capture_tags, 2, tags, u'type') == mapcss._value_capture(capture_tags, 2, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'foot') and not mapcss._tag_capture(capture_tags, 1, tags, u'network') and mapcss._tag_capture(capture_tags, 2, tags, u'type') == mapcss._value_capture(capture_tags, 2, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'horse') and not mapcss._tag_capture(capture_tags, 1, tags, u'network') and mapcss._tag_capture(capture_tags, 2, tags, u'type') == mapcss._value_capture(capture_tags, 2, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'piste') and not mapcss._tag_capture(capture_tags, 1, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 2, tags, u'type') == mapcss._value_capture(capture_tags, 2, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'ski') and not mapcss._tag_capture(capture_tags, 1, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 2, tags, u'type') == mapcss._value_capture(capture_tags, 2, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'information') and not mapcss._tag_capture(capture_tags, 1, tags, u'information'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and not mapcss._tag_capture(capture_tags, 1, tags, u'sport'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'terminal') and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'generator') and not mapcss._tag_capture(capture_tags, 1, tags, u'generator:source'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'social_facility') and not mapcss._tag_capture(capture_tags, 1, tags, u'social_facility'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'place_of_worship') and not mapcss._tag_capture(capture_tags, 1, tags, u'religion'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 9001001, 'subclass': 43540141, 'text': mapcss.tr(u'{0} without {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[smoothness][!highway][amenity!~/^(parking|parking_space|parking_entrance|motorcycle_parking|bicycle_parking)$/]
        # *[segregated][!highway][railway!=crossing]
        if (u'segregated' in keys) or (u'smoothness' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'smoothness') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_4f156c8f), mapcss._tag_capture(capture_tags, 2, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'segregated') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and mapcss._tag_capture(capture_tags, 2, tags, u'railway') != mapcss._value_capture(capture_tags, 2, u'crossing'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 1366851391, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # *[amenity=recycling][recycling_type!=container][recycling_type!=centre]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'recycling') and mapcss._tag_capture(capture_tags, 1, tags, u'recycling_type') != mapcss._value_capture(capture_tags, 1, u'container') and mapcss._tag_capture(capture_tags, 2, tags, u'recycling_type') != mapcss._value_capture(capture_tags, 2, u'centre'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.tag}","{1.tag}","{2.tag}")
                err.append({'class': 9001001, 'subclass': 747056792, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'))})

        # *[intermittent][!waterway][natural!~/^(water|spring)$/][landuse!~/^(basin|reservoir)$/][ford!=yes]
        # *[boat][!waterway][natural!=water][landuse!~/^(basin|reservoir)$/][ford!=yes]
        if (u'boat' in keys) or (u'intermittent' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'intermittent') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_4fbfe59b), mapcss._tag_capture(capture_tags, 2, tags, u'natural')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_0889a956), mapcss._tag_capture(capture_tags, 3, tags, u'landuse')) and mapcss._tag_capture(capture_tags, 4, tags, u'ford') != mapcss._value_capture(capture_tags, 4, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boat') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and mapcss._tag_capture(capture_tags, 2, tags, u'natural') != mapcss._value_capture(capture_tags, 2, u'water') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_0889a956), mapcss._tag_capture(capture_tags, 3, tags, u'landuse')) and mapcss._tag_capture(capture_tags, 4, tags, u'ford') != mapcss._value_capture(capture_tags, 4, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2}, {3} or {4}","{0.key}","{1.key}","{2.tag}","{3.tag}","{4.tag}")
                err.append({'class': 9001001, 'subclass': 1096267911, 'text': mapcss.tr(u'{0} without {1}, {2}, {3} or {4}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}'), mapcss._tag_uncapture(capture_tags, u'{3.tag}'), mapcss._tag_uncapture(capture_tags, u'{4.tag}'))})

        # *[snowplowing][!highway][!amenity][!leisure]
        if (u'snowplowing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'snowplowing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'amenity') and not mapcss._tag_capture(capture_tags, 3, tags, u'leisure'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.key}")
                err.append({'class': 9001001, 'subclass': 585636657, 'text': mapcss.tr(u'{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{3.key}'))})

        # *[toll][!highway][!barrier][route!~/^(ferry|road)$/]
        if (u'toll' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'toll') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'barrier') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_5ee853b2), mapcss._tag_capture(capture_tags, 3, tags, u'route')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}, {2} or {3}","{0.key}","{1.key}","{2.key}","{3.tag}")
                err.append({'class': 9001001, 'subclass': 1689494174, 'text': mapcss.tr(u'{0} without {1}, {2} or {3}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{3.tag}'))})

        # *[internet_access=no][internet_access:fee]
        # *[amenity=vending_machine][shop]
        # *[noname?][name]
        if (u'internet_access' in keys and u'internet_access:fee' in keys) or (u'name' in keys and u'noname' in keys) or (u'amenity' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'internet_access') == mapcss._value_capture(capture_tags, 0, u'no') and mapcss._tag_capture(capture_tags, 1, tags, u'internet_access:fee'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'vending_machine') and mapcss._tag_capture(capture_tags, 1, tags, u'shop'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noname') in ('yes', 'true', '1') and mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1004083393, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[access][eval(number_of_tags())=1]
        # *[area][eval(number_of_tags())=1]!.area_yes_autofix
        # *[name][eval(number_of_tags())=1]
        # *[ref][eval(number_of_tags())=1]
        # *[lit][eval(number_of_tags())=1]
        # Use undeclared class area_yes_autofix

        # *[name][area][eval(number_of_tags())=2]
        # *[name][ref][eval(number_of_tags())=2]
        if (u'area' in keys and u'name' in keys) or (u'name' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'area') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.key}")
                err.append({'class': 9001001, 'subclass': 788702375, 'text': mapcss.tr(u'incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[tourism=attraction][eval(number_of_tags())=1]
        if (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'attraction') and len(tags) == 1)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0}","{0.tag}")
                err.append({'class': 9001001, 'subclass': 463560683, 'text': mapcss.tr(u'incomplete object: only {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name][tourism=attraction][eval(number_of_tags())=2]
        if (u'name' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') == mapcss._value_capture(capture_tags, 1, u'attraction') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("incomplete object: only {0} and {1}","{0.key}","{1.tag}")
                err.append({'class': 9001001, 'subclass': 34376505, 'text': mapcss.tr(u'incomplete object: only {0} and {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[place][place!=farm][/^(addr:housenumber|addr:housename|addr:flats|addr:conscriptionnumber|addr:street|addr:place|addr:city|addr:country|addr:full|addr:hamlet|addr:suburb|addr:subdistrict|addr:district|addr:province|addr:state|addr:interpolation|addr:interpolation|addr:inclusion)$/]
        # *[boundary][/^addr:/]
        # *[highway][/^addr:/][highway!=services][highway!=rest_area][!"addr:postcode"]
        if (u'boundary' in keys) or (u'highway' in keys) or (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss._tag_capture(capture_tags, 1, tags, u'place') != mapcss._value_capture(capture_tags, 1, u'farm') and mapcss._tag_capture(capture_tags, 2, tags, self.re_0737b0c4))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') and mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, self.re_088b0835) and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'services') and mapcss._tag_capture(capture_tags, 3, tags, u'highway') != mapcss._value_capture(capture_tags, 3, u'rest_area') and not mapcss._tag_capture(capture_tags, 4, tags, u'addr:postcode'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with addr:*","{0.key}")
                err.append({'class': 9001002, 'subclass': 2039567622, 'text': mapcss.tr(u'{0} together with addr:*', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][postal_code]["addr:postcode"][postal_code=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') == mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 1341956372, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[!highway][postal_code]["addr:postcode"][postal_code!=*"addr:postcode"]
        if (u'addr:postcode' in keys and u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'postal_code') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 3, tags, u'postal_code') != mapcss._value_capture(capture_tags, 3, mapcss.tag(tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and conflicting values","{1.key}","{2.key}")
                err.append({'class': 9001002, 'subclass': 1415856502, 'text': mapcss.tr(u'{0} together with {1} and conflicting values', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[tunnel][!highway][!railway][!waterway][!piste:type][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor]
        # *[bridge][!highway][!railway][!waterway][!piste:type][public_transport!=platform][route!=ferry][man_made!=pipeline][man_made!=goods_conveyor][man_made!=bridge][building!=bridge]
        # *[psv][!highway][!railway][!waterway][amenity!~/^parking.*/]
        # *[width][!highway][!railway][!waterway][!aeroway][!cycleway][!footway][!barrier][!man_made][!entrance][natural!=stone]
        # *[maxspeed][!highway][!railway][traffic_sign!~/^((.*;)?maxspeed(;.*)?|[A-Z][A-Z]:.+)$/][type!=enforcement][waterway!~/^(river|canal|lock)$/][!traffic_calming][aerialway!=zip_line]
        if (u'bridge' in keys) or (u'maxspeed' in keys) or (u'psv' in keys) or (u'tunnel' in keys) or (u'width' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tunnel') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 5, tags, u'public_transport') != mapcss._value_capture(capture_tags, 5, u'platform') and mapcss._tag_capture(capture_tags, 6, tags, u'route') != mapcss._value_capture(capture_tags, 6, u'ferry') and mapcss._tag_capture(capture_tags, 7, tags, u'man_made') != mapcss._value_capture(capture_tags, 7, u'pipeline') and mapcss._tag_capture(capture_tags, 8, tags, u'man_made') != mapcss._value_capture(capture_tags, 8, u'goods_conveyor'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 5, tags, u'public_transport') != mapcss._value_capture(capture_tags, 5, u'platform') and mapcss._tag_capture(capture_tags, 6, tags, u'route') != mapcss._value_capture(capture_tags, 6, u'ferry') and mapcss._tag_capture(capture_tags, 7, tags, u'man_made') != mapcss._value_capture(capture_tags, 7, u'pipeline') and mapcss._tag_capture(capture_tags, 8, tags, u'man_made') != mapcss._value_capture(capture_tags, 8, u'goods_conveyor') and mapcss._tag_capture(capture_tags, 9, tags, u'man_made') != mapcss._value_capture(capture_tags, 9, u'bridge') and mapcss._tag_capture(capture_tags, 10, tags, u'building') != mapcss._value_capture(capture_tags, 10, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'psv') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 4, self.re_213d4d09), mapcss._tag_capture(capture_tags, 4, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'width') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'waterway') and not mapcss._tag_capture(capture_tags, 4, tags, u'aeroway') and not mapcss._tag_capture(capture_tags, 5, tags, u'cycleway') and not mapcss._tag_capture(capture_tags, 6, tags, u'footway') and not mapcss._tag_capture(capture_tags, 7, tags, u'barrier') and not mapcss._tag_capture(capture_tags, 8, tags, u'man_made') and not mapcss._tag_capture(capture_tags, 9, tags, u'entrance') and mapcss._tag_capture(capture_tags, 10, tags, u'natural') != mapcss._value_capture(capture_tags, 10, u'stone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_27d9cb1c), mapcss._tag_capture(capture_tags, 3, tags, u'traffic_sign')) and mapcss._tag_capture(capture_tags, 4, tags, u'type') != mapcss._value_capture(capture_tags, 4, u'enforcement') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 5, self.re_46fc3877), mapcss._tag_capture(capture_tags, 5, tags, u'waterway')) and not mapcss._tag_capture(capture_tags, 6, tags, u'traffic_calming') and mapcss._tag_capture(capture_tags, 7, tags, u'aerialway') != mapcss._value_capture(capture_tags, 7, u'zip_line'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} on suspicious object","{0.key}")
                err.append({'class': 9001002, 'subclass': 755649879, 'text': mapcss.tr(u'{0} on suspicious object', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[highway][waterway][waterway!=dam][waterway!=weir]
        # *[landuse][building][landuse!=retail]
        if (u'building' in keys and u'landuse' in keys) or (u'highway' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'waterway') and mapcss._tag_capture(capture_tags, 2, tags, u'waterway') != mapcss._value_capture(capture_tags, 2, u'dam') and mapcss._tag_capture(capture_tags, 3, tags, u'waterway') != mapcss._value_capture(capture_tags, 3, u'weir'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'landuse') != mapcss._value_capture(capture_tags, 2, u'retail'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.key}","{1.key}")
                err.append({'class': 9001002, 'subclass': 1750941961, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[natural=water][leisure=swimming_pool]
        if (u'leisure' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'water') and mapcss._tag_capture(capture_tags, 1, tags, u'leisure') == mapcss._value_capture(capture_tags, 1, u'swimming_pool'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("natural water used for swimming pool")
                # fixRemove:"natural"
                err.append({'class': 9001002, 'subclass': 608817213, 'text': mapcss.tr(u'natural water used for swimming pool'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'natural'])
                }})

        # *[sport][sport!=skiing][!building][!club][tourism!=hotel][highway!=raceway][!leisure][natural!~/^(beach|bare_rock|cliff|peak|water)$/][amenity!~/^(pub|restaurant|swimming_pool)$/][landuse!~/^(recreation_ground|piste|farm|farmland)$/][barrier!~/^(wall|retaining_wall)$/][!"piste:type"][shop!=sports]
        if (u'sport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sport') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') != mapcss._value_capture(capture_tags, 1, u'skiing') and not mapcss._tag_capture(capture_tags, 2, tags, u'building') and not mapcss._tag_capture(capture_tags, 3, tags, u'club') and mapcss._tag_capture(capture_tags, 4, tags, u'tourism') != mapcss._value_capture(capture_tags, 4, u'hotel') and mapcss._tag_capture(capture_tags, 5, tags, u'highway') != mapcss._value_capture(capture_tags, 5, u'raceway') and not mapcss._tag_capture(capture_tags, 6, tags, u'leisure') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 7, self.re_29fa4401), mapcss._tag_capture(capture_tags, 7, tags, u'natural')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 8, self.re_64c931ef), mapcss._tag_capture(capture_tags, 8, tags, u'amenity')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 9, self.re_3b4f8f73), mapcss._tag_capture(capture_tags, 9, tags, u'landuse')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 10, self.re_68c05e86), mapcss._tag_capture(capture_tags, 10, tags, u'barrier')) and not mapcss._tag_capture(capture_tags, 11, tags, u'piste:type') and mapcss._tag_capture(capture_tags, 12, tags, u'shop') != mapcss._value_capture(capture_tags, 12, u'sports'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("sport without physical feature")
                err.append({'class': 9001001, 'subclass': 1531133249, 'text': mapcss.tr(u'sport without physical feature')})

        # *[building:levels][!building][!building:part]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and not mapcss._tag_capture(capture_tags, 2, tags, u'building:part'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1} or {2}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9001001, 'subclass': 1821512557, 'text': mapcss.tr(u'{0} without {1} or {2}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[/_name$/][!name][!old_name][!loc_name][!uic_name][!artist_name][!lock_name][!"osak:municipality_name"][!"osak:street_name"][noname!=yes]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_25d98c90) and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'old_name') and not mapcss._tag_capture(capture_tags, 3, tags, u'loc_name') and not mapcss._tag_capture(capture_tags, 4, tags, u'uic_name') and not mapcss._tag_capture(capture_tags, 5, tags, u'artist_name') and not mapcss._tag_capture(capture_tags, 6, tags, u'lock_name') and not mapcss._tag_capture(capture_tags, 7, tags, u'osak:municipality_name') and not mapcss._tag_capture(capture_tags, 8, tags, u'osak:street_name') and mapcss._tag_capture(capture_tags, 9, tags, u'noname') != mapcss._value_capture(capture_tags, 9, u'yes'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("alternative name without {0}","{1.key}")
                err.append({'class': 9001001, 'subclass': 1070694429, 'text': mapcss.tr(u'alternative name without {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # relation[oneway][type!=route]
        if (u'oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != mapcss._value_capture(capture_tags, 1, u'route'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a relation without {1}","{0.key}","{1.tag}")
                err.append({'class': 9001003, 'subclass': 1921058011, 'text': mapcss.tr(u'{0} on a relation without {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[unisex=yes][female=yes][male!=yes][shop=hairdresser]
        # *[unisex=yes][male=yes][female!=yes][shop=hairdresser]
        if (u'male' in keys and u'shop' in keys and u'unisex' in keys) or (u'female' in keys and u'shop' in keys and u'unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'female') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'male') != mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'male') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'female') != mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                err.append({'class': 9001002, 'subclass': 1043941827, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[unisex=yes][female=yes][male=yes][shop=hairdresser]
        if (u'female' in keys and u'male' in keys and u'shop' in keys and u'unisex' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'unisex') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'female') == mapcss._value_capture(capture_tags, 1, u'yes') and mapcss._tag_capture(capture_tags, 2, tags, u'male') == mapcss._value_capture(capture_tags, 2, u'yes') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} and {2}. Remove {1} and {2}","{0.tag}","{1.tag}","{2.tag}")
                # fixRemove:"female"
                # fixRemove:"male"
                err.append({'class': 9001002, 'subclass': 408307546, 'text': mapcss.tr(u'{0} together with {1} and {2}. Remove {1} and {2}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'), mapcss._tag_uncapture(capture_tags, u'{2.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'female',
                    u'male'])
                }})

        # *[female=yes][male=yes][!unisex][shop=hairdresser]
        if (u'female' in keys and u'male' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'female') == mapcss._value_capture(capture_tags, 0, u'yes') and mapcss._tag_capture(capture_tags, 1, tags, u'male') == mapcss._value_capture(capture_tags, 1, u'yes') and not mapcss._tag_capture(capture_tags, 2, tags, u'unisex') and mapcss._tag_capture(capture_tags, 3, tags, u'shop') == mapcss._value_capture(capture_tags, 3, u'hairdresser'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"unisex=yes"
                # fixRemove:"female"
                # fixRemove:"male"
                # fixAdd:"unisex=yes"
                err.append({'class': 9001002, 'subclass': 831595594, 'text': mapcss.tr(u'{0} together with {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'unisex',u'yes']]),
                    '-': ([
                    u'female',
                    u'male'])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_combinations(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'source:addr:postcode': u'postman'}), expected={'class': 9001001, 'subclass': 1812055539})
        self.check_not_err(n.node(data, {u'addr:housenumber': u'42', u'source:addr': u'postman'}), expected={'class': 9001001, 'subclass': 1812055539})
        self.check_err(n.node(data, {u'source:addr': u'postman'}), expected={'class': 9001001, 'subclass': 1812055539})
        self.check_not_err(n.node(data, {u'addr:postcode': u'12345', u'place': u'foo'}), expected={'class': 9001002, 'subclass': 2039567622})
        self.check_err(n.node(data, {u'addr:housenumber': u'5', u'addr:postcode': u'12345', u'place': u'foo'}), expected={'class': 9001002, 'subclass': 2039567622})
        self.check_err(n.node(data, {u'addr:housenumber': u'5', u'place': u'foo'}), expected={'class': 9001002, 'subclass': 2039567622})
        self.check_not_err(n.node(data, {u'highway': u'street_lamp', u'natural': u'birds_nest'}), expected={'class': 9001002, 'subclass': 1750941961})
        self.check_not_err(n.node(data, {u'amenity': u'restaurant', u'sport': u'10pin'}), expected={'class': 9001001, 'subclass': 1531133249})
        self.check_not_err(n.node(data, {u'natural': u'beach', u'sport': u'beachvolleyball'}), expected={'class': 9001001, 'subclass': 1531133249})
        self.check_not_err(n.node(data, {u'sport': u'skiing'}), expected={'class': 9001001, 'subclass': 1531133249})
        self.check_not_err(n.node(data, {u'sport': u'swimming', u'tourism': u'hotel'}), expected={'class': 9001001, 'subclass': 1531133249})
        self.check_not_err(n.node(data, {u'leisure': u'pitch', u'sport': u'tennis'}), expected={'class': 9001001, 'subclass': 1531133249})
        self.check_err(n.node(data, {u'sport': u'tennis'}), expected={'class': 9001001, 'subclass': 1531133249})
        self.check_not_err(n.way(data, {u'highway': u'unclassified', u'lanes': u'42'}, [0]), expected={'class': 9001001, 'subclass': 1275753529})
        self.check_err(n.way(data, {u'lanes': u'42'}, [0]), expected={'class': 9001001, 'subclass': 1275753529})
        self.check_not_err(n.way(data, {u'highway': u'primary', u'lanes': u'2'}, [0]), expected={'class': 9001001, 'subclass': 841292752})
        self.check_not_err(n.way(data, {u'highway': u'primary', u'lanes': u'3', u'lanes:backward': u'2'}, [0]), expected={'class': 9001001, 'subclass': 841292752})
        self.check_not_err(n.way(data, {u'highway': u'primary', u'lanes': u'3', u'oneway': u'-1'}, [0]), expected={'class': 9001001, 'subclass': 841292752})
        self.check_err(n.way(data, {u'highway': u'primary', u'lanes': u'3'}, [0]), expected={'class': 9001001, 'subclass': 841292752})
        self.check_not_err(n.way(data, {u'highway': u'primary', u'lanes': u'4'}, [0]), expected={'class': 9001001, 'subclass': 841292752})
