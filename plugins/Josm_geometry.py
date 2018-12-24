#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_geometry(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9003001] = {'item': 9003, 'level': 3, 'tag': ["geom"], 'desc': mapcss.tr(u'{0} on a node. Should be used on a way.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9003002] = {'item': 9003, 'level': 3, 'tag': ["geom"], 'desc': mapcss.tr(u'{0} on a node. Should be used on a way or relation.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9003003] = {'item': 9003, 'level': 3, 'tag': ["geom"], 'desc': mapcss.tr(u'{0} on a node. Should be drawn as an area.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9003004] = {'item': 9003, 'level': 2, 'tag': ["geom"], 'desc': mapcss.tr(u'{0} on a node. Should be used in a relation', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9003005] = {'item': 9003, 'level': 3, 'tag': ["geom"], 'desc': mapcss.tr(u'suspicious tag combination')}
        self.errors[9003006] = {'item': 9003, 'level': 3, 'tag': ["geom"], 'desc': mapcss.tr(u'{0} on a node', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9003007] = {'item': 9003, 'level': 3, 'tag': ["geom"], 'desc': mapcss.tr(u'{0} on a way. Should be used on a node.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9003008] = {'item': 9003, 'level': 2, 'tag': ["geom"], 'desc': mapcss.tr(u'{0} on a way. Should be used in a relation', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9003009] = {'item': 9003, 'level': 2, 'tag': ["geom"], 'desc': mapcss.tr(u'Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.')}
        self.errors[9003010] = {'item': 9003, 'level': 2, 'tag': ["geom"], 'desc': mapcss.tr(u'Way with {0} not closed.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}

        self.re_22f56734 = re.compile(ur'^(no_right_turn|no_left_turn|no_u_turn|no_straight_on|only_right_turn|only_left_turn|only_straight_on|no_entry|no_exit)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[area=no]
        # node[oneway]
        # node[bridge]
        # node[sidewalk]
        # node[footway]
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
        if (u'aerialway' in keys) or (u'aeroway' in keys) or (u'area' in keys) or (u'bridge' in keys) or (u'cutline' in keys) or (u'footway' in keys) or (u'man_made' in keys) or (u'natural' in keys) or (u'oneway' in keys) or (u'power' in keys) or (u'railway' in keys) or (u'sidewalk' in keys) or (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'area') == mapcss._value_capture(capture_tags, 0, u'no'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'oneway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'sidewalk'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'footway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'embankment'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'groyne'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'cutline'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'line'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cutline'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'cable_car'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'gondola'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'chair_lift'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'mixed_lift'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'drag_lift'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u't-bar'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'j-bar'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'platter'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'magic_carpet'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'rope_tow'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == mapcss._value_capture(capture_tags, 0, u'goods'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'taxiway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'runway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'rail'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'narrow_gauge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'monorail'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'preserved'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'light_rail'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'subway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'tram'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'disused'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'abandoned'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'river'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'canal'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'stream'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'ditch'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'drain'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'coastline'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'ridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'valley'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'tree_row'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be used on a way.","{0.tag}")
                # assertMatch:"node bridge=viaduct"
                # assertMatch:"node bridge=yes"
                # assertMatch:"node oneway=-1"
                err.append({'class': 9003001, 'subclass': 2132549655, 'text': mapcss.tr(u'{0} on a node. Should be used on a way.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[boundary=administrative]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'administrative'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be used on a way or relation.","{0.tag}")
                err.append({'class': 9003002, 'subclass': 1005532536, 'text': mapcss.tr(u'{0} on a node. Should be used on a way or relation.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[golf=green]
        # node[golf=bunker]
        # node[golf=fairway]
        # node[area=yes]
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
        # node[waterway=riverbank]
        # node[man_made=bridge]
        # node[man_made=breakwater]
        # node[aeroway=apron]
        # node[power=plant]
        # node[power=switchgear]
        # node[building:part]
        # node[source:outline]
        if (u'aeroway' in keys) or (u'area' in keys) or (u'building:part' in keys) or (u'golf' in keys) or (u'landuse' in keys) or (u'man_made' in keys) or (u'natural' in keys) or (u'power' in keys) or (u'source:outline' in keys) or (u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'golf') == mapcss._value_capture(capture_tags, 0, u'green'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'golf') == mapcss._value_capture(capture_tags, 0, u'bunker'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'golf') == mapcss._value_capture(capture_tags, 0, u'fairway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'area') == mapcss._value_capture(capture_tags, 0, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'scree'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'scrub'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'fell'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'heath'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'wood'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'grassland'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'wetland'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'water'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'mud'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'beach'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'sand'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'wood'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'bare_rock'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'glacier'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == mapcss._value_capture(capture_tags, 0, u'riverbank'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'bridge'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'breakwater'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'apron'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'plant'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'switchgear'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:part'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:outline'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be drawn as an area.","{0.tag}")
                err.append({'class': 9003003, 'subclass': 913295728, 'text': mapcss.tr(u'{0} on a node. Should be drawn as an area.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[type=multipolygon]
        # node[route]
        # node[restriction]
        if (u'restriction' in keys) or (u'route' in keys) or (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'multipolygon'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'restriction'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} on a node. Should be used in a relation","{0.tag}")
                err.append({'class': 9003004, 'subclass': 1669293716, 'text': mapcss.tr(u'{0} on a node. Should be used in a relation', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[man_made!=monitoring_station][at(0.0,0.0)]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') != mapcss._value_capture(capture_tags, 0, u'monitoring_station') and mapcss.at(data['lat'], data['lon'], 0.0, 0.0))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.")
                # fixDeleteObject:this
                err.append({'class': 9003009, 'subclass': 829325630, 'text': mapcss.tr(u'Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.')})

        # node[leisure=park][natural=tree]
        if (u'leisure' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'park') and mapcss._tag_capture(capture_tags, 1, tags, u'natural') == mapcss._value_capture(capture_tags, 1, u'tree'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
                # throwWarning:tr("{0} together with {1} on a node. Remove {0}.","{0.tag}","{1.tag}")
                # fixRemove:"leisure"
                err.append({'class': 9003005, 'subclass': 1715941543, 'text': mapcss.tr(u'{0} together with {1} on a node. Remove {0}.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'leisure'])
                }})

        # node[leisure=park][natural!=tree]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'park') and mapcss._tag_capture(capture_tags, 1, tags, u'natural') != mapcss._value_capture(capture_tags, 1, u'tree'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be drawn as an area.","{0.tag}")
                err.append({'class': 9003003, 'subclass': 317377122, 'text': mapcss.tr(u'{0} on a node. Should be drawn as an area.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[source:geometry]
        if (u'source:geometry' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source:geometry'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node","{0.key}")
                # fixChangeKey:"source:geometry => source:position"
                err.append({'class': 9003006, 'subclass': 1287904360, 'text': mapcss.tr(u'{0} on a node', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'source:position', mapcss.tag(tags, u'source:geometry')]]),
                    '-': ([
                    u'source:geometry'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[entrance]
        # way[railway=subway_entrance]
        # way[man_made=survey_point]
        # way[aeroway=holding_position]
        # way[power=transformer]
        # way[power=pole]
        # way[power=catenary_mast]
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
        if (u'aeroway' in keys) or (u'amenity' in keys) or (u'entrance' in keys) or (u'highway' in keys) or (u'man_made' in keys) or (u'natural' in keys) or (u'power' in keys) or (u'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'entrance'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'subway_entrance'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'survey_point'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'holding_position'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'transformer'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'pole'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'catenary_mast'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'terminal'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'power') == mapcss._value_capture(capture_tags, 0, u'tower') and nds[0] == nds[-1])
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'vending_machine'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'peak'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'saddle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'volcano'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'tree'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'give_way'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'milestone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'mini_roundabout'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stop'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'street_lamp'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'traffic_signals'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'turning_loop'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'turning_circle'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a way. Should be used on a node.","{0.tag}")
                err.append({'class': 9003007, 'subclass': 1466799427, 'text': mapcss.tr(u'{0} on a way. Should be used on a node.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[restriction][restriction=~/^(no_right_turn|no_left_turn|no_u_turn|no_straight_on|only_right_turn|only_left_turn|only_straight_on|no_entry|no_exit)$/]
        # way[type=multipolygon]
        # way[route=bus]
        if (u'restriction' in keys) or (u'route' in keys) or (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'restriction') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_22f56734), mapcss._tag_capture(capture_tags, 1, tags, u'restriction')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'multipolygon'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'bus'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} on a way. Should be used in a relation","{0.tag}")
                err.append({'class': 9003008, 'subclass': 1728608057, 'text': mapcss.tr(u'{0} on a way. Should be used in a relation', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[place=island]!:closed
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'island') and nds[0] == nds[-1])
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Way with {0} not closed.","{0.tag}")
                err.append({'class': 9003010, 'subclass': 167228643, 'text': mapcss.tr(u'Way with {0} not closed.', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

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

        self.check_err(n.node(data, {u'bridge': u'viaduct'}), expected={'class': 9003001, 'subclass': 2132549655})
        self.check_err(n.node(data, {u'bridge': u'yes'}), expected={'class': 9003001, 'subclass': 2132549655})
        self.check_err(n.node(data, {u'oneway': u'-1'}), expected={'class': 9003001, 'subclass': 2132549655})
