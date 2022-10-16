#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_geometry(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/geometry.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9003001] = self.def_class(item = 9003, level = 3, tags = ["geom"], title = mapcss.tr('{0} on a node. Should be used on a way.', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9003002] = self.def_class(item = 9003, level = 3, tags = ["geom"], title = mapcss.tr('{0} on a node. Should be used on a way or relation.', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9003003] = self.def_class(item = 9003, level = 3, tags = ["geom"], title = mapcss.tr('{0} on a node. Should be drawn as an area.', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9003004] = self.def_class(item = 9003, level = 2, tags = ["geom"], title = mapcss.tr('{0} on a node. Should be used in a relation', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9003006] = self.def_class(item = 9003, level = 3, tags = ["geom"], title = mapcss.tr('{0} on a node', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9003007] = self.def_class(item = 9003, level = 3, tags = ["geom"], title = mapcss.tr('{0} on a way. Should be used on a node.', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9003008] = self.def_class(item = 9003, level = 2, tags = ["geom"], title = mapcss.tr('{0} on a way. Should be used in a relation', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9003009] = self.def_class(item = 9003, level = 2, tags = ["geom"], title = mapcss.tr('Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.'))
        self.errors[9003011] = self.def_class(item = 9003, level = 3, tags = ["geom"], title = mapcss.tr('{0} on a closed way. Should be used on an unclosed way.', mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[9003012] = self.def_class(item = 9003, level = 3, tags = ["geom"], title = mapcss.tr('{0} on a relation', mapcss._tag_uncapture(capture_tags, '{0.key}')))

        self.re_22f56734 = re.compile(r'^(no_right_turn|no_left_turn|no_u_turn|no_straight_on|only_right_turn|only_left_turn|only_straight_on|no_entry|no_exit)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[area=no]
        # node[oneway]
        # node[bridge]
        # node[sidewalk]
        # node[footway][footway!=crossing]
        # node[man_made=embankment]
        # node[man_made=groyne]
        # node[man_made=cutline]
        # node[power=line]
        # node[cutline]
        # node[aerialway=cable_car]
        # node[aerialway=gondola]
        # node[aerialway=chair_lift]
        # node[aerialway=mixed_lift]
        # node[aerialway=drag_lift]
        # node[aerialway=t-bar]
        # node[aerialway=j-bar]
        # node[aerialway=platter]
        # node[aerialway=magic_carpet]
        # node[aerialway=rope_tow]
        # node[aerialway=goods]
        # node[aeroway=taxiway]
        # node[aeroway=runway]
        # node[railway=rail]
        # node[railway=narrow_gauge]
        # node[railway=monorail]
        # node[railway=preserved]
        # node[railway=light_rail]
        # node[railway=subway]
        # node[railway=tram]
        # node[railway=disused]
        # node[railway=abandoned]
        # node[waterway=river]
        # node[waterway=canal]
        # node[waterway=stream]
        # node[waterway=ditch]
        # node[waterway=drain]
        # node[natural=coastline]
        # node[natural=ridge]
        # node[natural=valley]
        # node[natural=tree_row]
        if ('aerialway' in keys) or ('aeroway' in keys) or ('area' in keys) or ('bridge' in keys) or ('cutline' in keys) or ('footway' in keys) or ('man_made' in keys) or ('natural' in keys) or ('oneway' in keys) or ('power' in keys) or ('railway' in keys) or ('sidewalk' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'area') == mapcss._value_capture(capture_tags, 0, 'no')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'sidewalk')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'footway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'footway') != mapcss._value_const_capture(capture_tags, 1, 'crossing', 'crossing')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'embankment')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'groyne')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'cutline')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'line')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'cutline')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'cable_car')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'gondola')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'chair_lift')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'mixed_lift')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'drag_lift')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 't-bar')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'j-bar')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'platter')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'magic_carpet')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'rope_tow')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aerialway') == mapcss._value_capture(capture_tags, 0, 'goods')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'taxiway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'runway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'rail')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'narrow_gauge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'monorail')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'preserved')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'light_rail')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'subway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'tram')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'disused')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'abandoned')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'river')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'canal')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'stream')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'ditch')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'drain')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'coastline')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'ridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'valley')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'tree_row')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be used on a way.","{0.tag}")
                # assertMatch:"node bridge=viaduct"
                # assertMatch:"node bridge=yes"
                # assertMatch:"node oneway=-1"
                err.append({'class': 9003001, 'subclass': 431750003, 'text': mapcss.tr('{0} on a node. Should be used on a way.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[boundary=administrative]
        if ('boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'boundary') == mapcss._value_capture(capture_tags, 0, 'administrative')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be used on a way or relation.","{0.tag}")
                err.append({'class': 9003002, 'subclass': 1005532536, 'text': mapcss.tr('{0} on a node. Should be used on a way or relation.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[golf=green]
        # node[golf=bunker]
        # node[golf=fairway]
        # node[area=yes]
        # node[area:highway]
        # node[landuse]
        # node[natural=scree]
        # node[natural=scrub]
        # node[natural=fell]
        # node[natural=heath]
        # node[natural=wood]
        # node[natural=grassland]
        # node[natural=wetland]
        # node[natural=water]
        # node[natural=mud]
        # node[natural=beach]
        # node[natural=sand]
        # node[natural=wood]
        # node[natural=bare_rock]
        # node[natural=glacier]
        # node[leisure=park][natural!=tree]
        # node[leisure=nature_reserve]
        # node[waterway=riverbank]
        # node[man_made=bridge]
        # node[man_made=breakwater]
        # node[aeroway=apron]
        # node[power=plant]
        # node[power=switchgear]
        # node[building:part]
        # node[source:outline]
        if ('aeroway' in keys) or ('area' in keys) or ('area:highway' in keys) or ('building:part' in keys) or ('golf' in keys) or ('landuse' in keys) or ('leisure' in keys) or ('man_made' in keys) or ('natural' in keys) or ('power' in keys) or ('source:outline' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'golf') == mapcss._value_capture(capture_tags, 0, 'green')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'golf') == mapcss._value_capture(capture_tags, 0, 'bunker')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'golf') == mapcss._value_capture(capture_tags, 0, 'fairway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'area') == mapcss._value_capture(capture_tags, 0, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'area:highway')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'scree')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'scrub')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'fell')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'heath')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'wood')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'grassland')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'wetland')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'water')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'mud')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'beach')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'sand')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'wood')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'bare_rock')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'glacier')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'park')) and (mapcss._tag_capture(capture_tags, 1, tags, 'natural') != mapcss._value_const_capture(capture_tags, 1, 'tree', 'tree')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'nature_reserve')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway') == mapcss._value_capture(capture_tags, 0, 'riverbank')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'bridge')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'breakwater')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'aeroway') == mapcss._value_capture(capture_tags, 0, 'apron')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'plant')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'switchgear')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building:part')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:outline')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be drawn as an area.","{0.tag}")
                err.append({'class': 9003003, 'subclass': 1633038746, 'text': mapcss.tr('{0} on a node. Should be drawn as an area.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[type=multipolygon]
        # node[interval]
        # node[route]
        # node[restriction]
        if ('interval' in keys) or ('restriction' in keys) or ('route' in keys) or ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'restriction')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} on a node. Should be used in a relation","{0.tag}")
                err.append({'class': 9003004, 'subclass': 104835602, 'text': mapcss.tr('{0} on a node. Should be used in a relation', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[man_made!=monitoring_station][at(0.0,0.0)]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') != mapcss._value_const_capture(capture_tags, 0, 'monitoring_station', 'monitoring_station')) and (mapcss.at(data['lat'], data['lon'], 0.0, 0.0)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.")
                # fixDeleteObject:this
                err.append({'class': 9003009, 'subclass': 829325630, 'text': mapcss.tr('Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.')})

        # node[source:geometry]
        if ('source:geometry' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'source:geometry')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node","{0.key}")
                # fixChangeKey:"source:geometry => source:position"
                err.append({'class': 9003006, 'subclass': 1287904360, 'text': mapcss.tr('{0} on a node', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['source:position', mapcss.tag(tags, 'source:geometry')]]),
                    '-': ([
                    'source:geometry'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[emergency=fire_hydrant]
        # way[emergency=defibrillator]
        # way[railway=subway_entrance]
        # way[man_made=survey_point]
        # way[power=transformer]
        # way[power=pole]
        # way[power=catenary_mast]
        # way[power=connection]
        # way[power=terminal]
        # way[power=tower]!:closed
        # way[amenity=vending_machine]
        # way[natural=peak]
        # way[natural=saddle]
        # way[natural=volcano]
        # way[natural=tree]
        # way[highway=give_way]
        # way[highway=milestone]
        # way[highway=mini_roundabout]
        # way[highway=stop]
        # way[highway=street_lamp]
        # way[highway=traffic_signals]
        # way[highway=turning_loop]
        # way[highway=turning_circle]
        # way[highway=motorway_junction]
        if ('amenity' in keys) or ('emergency' in keys) or ('highway' in keys) or ('man_made' in keys) or ('natural' in keys) or ('power' in keys) or ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'fire_hydrant')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'emergency') == mapcss._value_capture(capture_tags, 0, 'defibrillator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'subway_entrance')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'man_made') == mapcss._value_capture(capture_tags, 0, 'survey_point')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'transformer')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'pole')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'catenary_mast')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'connection')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'terminal')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'tower')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'vending_machine')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'peak')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'saddle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'volcano')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'natural') == mapcss._value_capture(capture_tags, 0, 'tree')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'give_way')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'milestone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'mini_roundabout')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'stop')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'street_lamp')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'traffic_signals')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'turning_loop')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'turning_circle')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'motorway_junction')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a way. Should be used on a node.","{0.tag}")
                err.append({'class': 9003007, 'subclass': 1619711985, 'text': mapcss.tr('{0} on a way. Should be used on a node.', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[voltage:primary]
        # way[voltage:secondary]
        # way[voltage:tertiary]
        # way[transformer]
        # way[line_attachment]
        # way[line_management]
        # way[entrance]
        # way[door]
        if ('door' in keys) or ('entrance' in keys) or ('line_attachment' in keys) or ('line_management' in keys) or ('transformer' in keys) or ('voltage:primary' in keys) or ('voltage:secondary' in keys) or ('voltage:tertiary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:primary')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:secondary')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'voltage:tertiary')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'transformer')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'line_attachment')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'line_management')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'entrance')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'door')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a way. Should be used on a node.","{0.key}")
                err.append({'class': 9003007, 'subclass': 685282689, 'text': mapcss.tr('{0} on a way. Should be used on a node.', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[restriction][restriction=~/^(no_right_turn|no_left_turn|no_u_turn|no_straight_on|only_right_turn|only_left_turn|only_straight_on|no_entry|no_exit)$/]
        # way[type=multipolygon]
        # way[interval][route!=ferry]
        # way[route=bus]
        if ('interval' in keys) or ('restriction' in keys) or ('route' in keys) or ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'restriction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_22f56734), mapcss._tag_capture(capture_tags, 1, tags, 'restriction'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'interval')) and (mapcss._tag_capture(capture_tags, 1, tags, 'route') != mapcss._value_const_capture(capture_tags, 1, 'ferry', 'ferry')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'route') == mapcss._value_capture(capture_tags, 0, 'bus')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} on a way. Should be used in a relation","{0.tag}")
                err.append({'class': 9003008, 'subclass': 665916193, 'text': mapcss.tr('{0} on a way. Should be used in a relation', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way:closed[power=line]
        if ('power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 1, tags, 'power') == mapcss._value_capture(capture_tags, 1, 'line')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a closed way. Should be used on an unclosed way.","{1.tag}")
                err.append({'class': 9003011, 'subclass': 2100265426, 'text': mapcss.tr('{0} on a closed way. Should be used on an unclosed way.', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[area?]
        if ('area' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'area') in ('yes', 'true', '1')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a relation","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9003012, 'subclass': 922972473, 'text': mapcss.tr('{0} on a relation', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, '{0.key}')])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_geometry(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'bridge': 'viaduct'}), expected={'class': 9003001, 'subclass': 431750003}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.node(data, {'bridge': 'yes'}), expected={'class': 9003001, 'subclass': 431750003}, disallowed_str_in_text = ['{', '}'])
        self.check_err(n.node(data, {'oneway': '-1'}), expected={'class': 9003001, 'subclass': 431750003}, disallowed_str_in_text = ['{', '}'])
