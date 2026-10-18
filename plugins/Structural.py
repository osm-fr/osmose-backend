import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Structural(PluginMapCSS):
    # ------------------------------- IMPORTANT -------------------------------
    # This file is generated automatically and should not be modified directly.
    # Instead, modify the source mapcss file and regenerate this Python script.
    # -------------------------------------------------------------------------



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[4] = self.def_class(item = 1170, level = 1, tags = mapcss.list_('geom', 'fix:imagery', 'fix:chair'), title = mapcss.tr('Should be polygon, part of multipolygon or not having area tag'), detail = mapcss.tr('A way has a tag that suggests it is an area, but the way is not closed.'), fix = mapcss.tr('Make sure the first and last node of the way are connected, such that it forms a closed way. If the way is not an area, add `area=no` or correct the tags.'), trap = mapcss.tr('Use a multipolygon relation instead of a way if a closed way cannot be formed to represent the area. In this case, remove the area-related tags from the way.'), example = {"en": '![](https://wiki.openstreetmap.org/w/images/c/cc/Osmose-eg-error-1100.png)'})

        self.re_2d687399 = re.compile(r'^(barefoot|bathing_place|slipway|track)$')
        self.re_342e1a01 = re.compile(r'^(yes|designated|permissive)$')
        self.re_3977796a = re.compile(r'^(bench|bicycle_parking|hitching_post|ticket_validator|weighbridge)$')
        self.re_3ad8d56a = re.compile(r'^(bare_rock|bay|beach|fell|glacier|grassland|heath|hot_spring|moor|mud|rock|sand|scree|scrub|shingle|sinkhole|stone|water|wetland|wood)$')
        self.re_3dd10aca = re.compile(r'^(obstacle_course|road|trench)$')
        self.re_50f04966 = re.compile(r'^(artwork|attraction|yes)$')
        self.re_7d3259ea = re.compile(r'^(boatyard|dock|fuel|riverbank)$')


    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[amenity]!:closed[!area][amenity!~/^(bench|bicycle_parking|hitching_post|ticket_validator|weighbridge)$/]
        # way[area]!:closed[area!=no]
        # way[area:highway]!:closed
        # way[building:part]!:closed[!area]
        # way[building]!:closed
        # way[club]!:closed[!area]
        # way[craft]!:closed[!area]
        # way[emergency]!:closed[!area][emergency!~/^(yes|designated|permissive)$/][!highway]
        # way[healthcare]!:closed[!area]
        # way[landcover]!:closed
        # way[landuse]!:closed
        # way[leisure]!:closed[!area][leisure!~/^(barefoot|bathing_place|slipway|track)$/]
        # way[military]!:closed[!area][military!~/^(obstacle_course|road|trench)$/][!highway]
        # way[natural]!:closed[!area][natural=~/^(bare_rock|bay|beach|fell|glacier|grassland|heath|hot_spring|moor|mud|rock|sand|scree|scrub|shingle|sinkhole|stone|water|wetland|wood)$/][bay!=fjord]
        # way[office]!:closed[!area]
        # way[place]!:closed
        # way[shop]!:closed[!area]
        # way[tourism]!:closed[!area][tourism!~/^(artwork|attraction|yes)$/]
        # way[waterway]!:closed[!area][waterway=~/^(boatyard|dock|fuel|riverbank)$/]
        if ('amenity' in keys) or ('area' in keys) or ('area:highway' in keys) or ('building' in keys) or ('building:part' in keys) or ('club' in keys) or ('craft' in keys) or ('emergency' in keys) or ('healthcare' in keys) or ('landcover' in keys) or ('landuse' in keys) or ('leisure' in keys) or ('military' in keys) or ('natural' in keys) or ('office' in keys) or ('place' in keys) or ('shop' in keys) or ('tourism' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_3977796a, '^(bench|bicycle_parking|hitching_post|ticket_validator|weighbridge)$'), mapcss._tag_capture(capture_tags, 3, tags, 'amenity'))) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'area')) and (mapcss._tag_capture(capture_tags, 2, tags, 'area') != mapcss._value_const_capture(capture_tags, 2, 'no', 'no')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'area:highway')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'club')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'craft')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'emergency')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_342e1a01, '^(yes|designated|permissive)$'), mapcss._tag_capture(capture_tags, 3, tags, 'emergency'))) and (not mapcss._tag_capture(capture_tags, 4, tags, 'highway')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'healthcare')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landcover')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_2d687399, '^(barefoot|bathing_place|slipway|track)$'), mapcss._tag_capture(capture_tags, 3, tags, 'leisure'))) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'military')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_3dd10aca, '^(obstacle_course|road|trench)$'), mapcss._tag_capture(capture_tags, 3, tags, 'military'))) and (not mapcss._tag_capture(capture_tags, 4, tags, 'highway')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_3ad8d56a), mapcss._tag_capture(capture_tags, 3, tags, 'natural'))) and (mapcss._tag_capture(capture_tags, 4, tags, 'bay') != mapcss._value_const_capture(capture_tags, 4, 'fjord', 'fjord')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'office')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'shop')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'tourism')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_50f04966, '^(artwork|attraction|yes)$'), mapcss._tag_capture(capture_tags, 3, tags, 'tourism'))) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'area')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_7d3259ea), mapcss._tag_capture(capture_tags, 3, tags, 'waterway'))) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Should be polygon, part of multipolygon or not having area tag")
                # -osmoseTags:list("geom","fix:imagery","fix:chair")
                # -osmoseDetail:tr("A way has a tag that suggests it is an area, but the way is not closed.")
                # -osmoseFix:tr("Make sure the first and last node of the way are connected, such that it forms a closed way. If the way is not an area, add `area=no` or correct the tags.")
                # -osmoseTrap:tr("Use a multipolygon relation instead of a way if a closed way cannot be formed to represent the area. In this case, remove the area-related tags from the way.")
                # -osmoseExample:"![](https://wiki.openstreetmap.org/w/images/c/cc/Osmose-eg-error-1100.png)"
                # -osmoseItemClassLevel:"1170/4/1"
                # throwError:tr("Unclosed way with {0}","{0.tag}")
                # assertNoMatch:"way emergency=designated"
                # assertNoMatch:"way oneway=no"
                # assertNoMatch:"way tourism=xyz area=no"
                err.append({'class': 4, 'subclass': 0, 'text': mapcss.tr('Unclosed way with {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Structural(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.way(data, {'emergency': 'designated'}, [0]), expected={'class': 4, 'subclass': 0})
        self.check_not_err(n.way(data, {'oneway': 'no'}, [0]), expected={'class': 4, 'subclass': 0})
        self.check_not_err(n.way(data, {'area': 'no', 'tourism': 'xyz'}, [0]), expected={'class': 4, 'subclass': 0})
