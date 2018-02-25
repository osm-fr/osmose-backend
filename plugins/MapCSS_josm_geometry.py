#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_geometry(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9003001] = {'item': 9003, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} on a node. Should be used on a way.', capture_tags, u'{0.tag}')}
        self.errors[9003002] = {'item': 9003, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} on a node. Should be used on a way or relation.', capture_tags, u'{0.tag}')}
        self.errors[9003003] = {'item': 9003, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} on a node. Should be drawn as an area.', capture_tags, u'{0.tag}')}
        self.errors[9003004] = {'item': 9003, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} on a node. Should be used in a relation', capture_tags, u'{0.tag}')}
        self.errors[9003005] = {'item': 9003, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'suspicious tag combination', capture_tags)}
        self.errors[9003006] = {'item': 9003, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} on a node', capture_tags, u'{0.key}')}
        self.errors[9003007] = {'item': 9003, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} on a way. Should be used on a node.', capture_tags, u'{0.tag}')}
        self.errors[9003008] = {'item': 9003, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} on a way. Should be used in a relation', capture_tags, u'{0.tag}')}
        self.errors[9003009] = {'item': 9003, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.', capture_tags)}



    def node(self, data, tags, *args):
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
        if u'aerialway' in keys or u'aeroway' in keys or u'area' in keys or u'bridge' in keys or u'cutline' in keys or u'footway' in keys or u'man_made' in keys or u'natural' in keys or u'oneway' in keys or u'power' in keys or u'railway' in keys or u'sidewalk' in keys or u'waterway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'area') == u'no'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'oneway')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'bridge')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'sidewalk')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'footway')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == u'embankment'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == u'groyne'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == u'cutline'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'power') == u'line'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'cutline')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'cable_car'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'gondola'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'chair_lift'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'mixed_lift'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'drag_lift'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u't-bar'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'j-bar'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'platter'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'magic_carpet'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'rope_tow'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aerialway') == u'goods'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'taxiway'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'runway'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'rail'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'narrow_gauge'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'monorail'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'preserved'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'light_rail'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'subway'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'tram'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'disused'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'abandoned'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == u'river'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == u'canal'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == u'stream'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == u'ditch'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == u'drain'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'coastline'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'ridge'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'valley'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'tree_row'))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be used on a way.","{0.tag}")
            # assertMatch:"node bridge=viaduct"
            # assertMatch:"node bridge=yes"
            # assertMatch:"node oneway=-1"
                err.append({'class': 9003001, 'subclass': 2132549655, 'text': mapcss.tr(u'{0} on a node. Should be used on a way.', capture_tags, u'{0.tag}')})

        # node[boundary=administrative]
        if u'boundary' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'administrative'))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be used on a way or relation.","{0.tag}")
                err.append({'class': 9003002, 'subclass': 1005532536, 'text': mapcss.tr(u'{0} on a node. Should be used on a way or relation.', capture_tags, u'{0.tag}')})

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
        # node[building:part]
        # node[source:outline]
        if u'aeroway' in keys or u'area' in keys or u'building:part' in keys or u'landuse' in keys or u'man_made' in keys or u'natural' in keys or u'power' in keys or u'source:outline' in keys or u'waterway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'area') == u'yes'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'landuse')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'scree'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'scrub'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'fell'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'heath'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'wood'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'grassland'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'wetland'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'water'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'mud'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'beach'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'sand'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'wood'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'bare_rock'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'glacier'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') == u'riverbank'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == u'bridge'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == u'breakwater'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'apron'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'power') == u'plant'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'building:part')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'source:outline')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be drawn as an area.","{0.tag}")
                err.append({'class': 9003003, 'subclass': 990395761, 'text': mapcss.tr(u'{0} on a node. Should be drawn as an area.', capture_tags, u'{0.tag}')})

        # node[type=multipolygon]
        # node[route]
        # node[restriction]
        if u'restriction' in keys or u'route' in keys or u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'multipolygon'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'route')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'restriction')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} on a node. Should be used in a relation","{0.tag}")
                err.append({'class': 9003004, 'subclass': 1669293716, 'text': mapcss.tr(u'{0} on a node. Should be used in a relation', capture_tags, u'{0.tag}')})

        # node[man_made!=monitoring_station][at(0.0,0.0)]
        if True:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') != u'monitoring_station' and (data['lat'] == 0.0 and data['lon'] == 0.0)))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.")
            # fixDeleteObject:this
                err.append({'class': 9003009, 'subclass': 829325630, 'text': mapcss.tr(u'Object at Position 0.00E 0.00N. There is nothing at this position except an already mapped weather buoy.', capture_tags)})

        # node[leisure=park][natural=tree]
        if u'leisure' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'park' and mapcss._tag_capture(capture_tags, 1, tags, u'natural') == u'tree'))
            except mapcss.RuleAbort: pass
            if match:
                # group:tr("suspicious tag combination")
            # throwWarning:tr("{0} together with {1} on a node. Remove {0}.","{0.tag}","{1.tag}")
            # fixRemove:"leisure"
                err.append({'class': 9003005, 'subclass': 1715941543, 'text': mapcss.tr(u'{0} together with {1} on a node. Remove {0}.', capture_tags, u'{0.tag}', u'{1.tag}'), 'fix': {
                    '-': ([
                    u'leisure'])
                }})

        # node[leisure=park][natural!=tree]
        if u'leisure' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'park' and mapcss._tag_capture(capture_tags, 1, tags, u'natural') != u'tree'))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node. Should be drawn as an area.","{0.tag}")
                err.append({'class': 9003003, 'subclass': 317377122, 'text': mapcss.tr(u'{0} on a node. Should be drawn as an area.', capture_tags, u'{0.tag}')})

        # node[source:geometry]
        if u'source:geometry' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'source:geometry')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a node","{0.key}")
            # fixChangeKey:"source:geometry => source:position"
                err.append({'class': 9003006, 'subclass': 1287904360, 'text': mapcss.tr(u'{0} on a node', capture_tags, u'{0.key}'), 'fix': {
                    '+': dict([
                    [u'source:position', mapcss.tag(tags, u'source:geometry')]]),
                    '-': ([
                    u'source:geometry'])
                }})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[entrance]
        # way[railway=subway_entrance]
        # way[man_made=survey_point]
        # way[aeroway=holding_position]
        # way[power=transformer]
        # way[power=pole]
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
        if u'aeroway' in keys or u'amenity' in keys or u'entrance' in keys or u'highway' in keys or u'man_made' in keys or u'natural' in keys or u'power' in keys or u'railway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'entrance')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'railway') == u'subway_entrance'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == u'survey_point'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'holding_position'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'power') == u'transformer'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'power') == u'pole'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'vending_machine'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'peak'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'saddle'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'volcano'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'natural') == u'tree'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'give_way'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'milestone'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'mini_roundabout'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'stop'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'street_lamp'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'traffic_signals'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'turning_loop'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'turning_circle'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'motorway_junction'))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} on a way. Should be used on a node.","{0.tag}")
                err.append({'class': 9003007, 'subclass': 520876934, 'text': mapcss.tr(u'{0} on a way. Should be used on a node.', capture_tags, u'{0.tag}')})

        # way[type=multipolygon]
        # way[route=bus]
        if u'route' in keys or u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'multipolygon'))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'route') == u'bus'))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} on a way. Should be used in a relation","{0.tag}")
                err.append({'class': 9003008, 'subclass': 173468051, 'text': mapcss.tr(u'{0} on a way. Should be used in a relation', capture_tags, u'{0.tag}')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_geometry(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'bridge': u'viaduct'}), expected={'class': 9003001, 'subclass': 2132549655})
        self.check_err(n.node(data, {u'bridge': u'yes'}), expected={'class': 9003001, 'subclass': 2132549655})
        self.check_err(n.node(data, {u'oneway': u'-1'}), expected={'class': 9003001, 'subclass': 2132549655})
