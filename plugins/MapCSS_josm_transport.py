#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_transport(Plugin):

    only_for = ['FR']

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9014001] = {'item': 9014, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'Stop without name', capture_tags)}
        self.errors[9014002] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Is it a bus stop or a bus station?', capture_tags)}
        self.errors[9014003] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Specify if it is a stop (platform) or a location on the road (stop_position)', capture_tags)}
        self.errors[9014004] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'The legacy tag is missing, add the tag highway=bus_stop / railway=tram_stop', capture_tags)}
        self.errors[9014005] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Is this a bus stop? add the tag highway=bus_stop', capture_tags)}
        self.errors[9014006] = {'item': 9014, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'Check if the note can be deleted', capture_tags)}
        self.errors[9014007] = {'item': 9014, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'The network should be on the transport lines and not on the stops', capture_tags)}
        self.errors[9014008] = {'item': 9014, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'The operator should be on the transport lines and not on the stops', capture_tags)}
        self.errors[9014009] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Missing transportation mode, add a tag route = bus/coach/tram/etc', capture_tags)}
        self.errors[9014010] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Missing transportation mode, chnage tag route to route_master', capture_tags)}
        self.errors[9014011] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Missing public_transport:version tag on a public_transport route relation', capture_tags)}
        self.errors[9014012] = {'item': 9014, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'The stops may not be in the right order', capture_tags)}
        self.errors[9014013] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Check the operator tag', capture_tags)}
        self.errors[9014014] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Check the network tag', capture_tags)}
        self.errors[9014015] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Missing network tag on a public_transport relation', capture_tags)}
        self.errors[9014016] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Missing operator tag on a public_transport relation', capture_tags)}
        self.errors[9014017] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Missing ref tag for line number on a public_transport relation', capture_tags)}
        self.errors[9014018] = {'item': 9014, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Missing from/to tag on a public_transport route relation', capture_tags)}

        self.re_25554804 = re.compile(ur'STIF|Kéolis|Véolia')
        self.re_37f81db8 = re.compile(ur'^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus)$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_pt_route = set_pt_route_master = False

        # node[highway=bus_stop][!name]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Stop without name")
                err.append({'class': 9014001, 'subclass': 1368699603, 'text': mapcss.tr(u'Stop without name', capture_tags)})

        # node[highway=bus_stop][amenity=bus_station]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == u'bus_station'))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Is it a bus stop or a bus station?")
            # fixRemove:"amenity"
                err.append({'class': 9014002, 'subclass': 1676203359, 'text': mapcss.tr(u'Is it a bus stop or a bus station?', capture_tags), 'fix': {
                    '-': ([
                    u'amenity'])
                }})

        # node[highway=bus_stop][!public_transport]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Specify if it is a stop (platform) or a location on the road (stop_position)")
            # fixAdd:"public_transport=platform"
                err.append({'class': 9014003, 'subclass': 364316040, 'text': mapcss.tr(u'Specify if it is a stop (platform) or a location on the road (stop_position)', capture_tags), 'fix': {
                    '+': dict([
                    [u'public_transport',u'platform']])
                }})

        # node["public_transport"="platform"][!highway][!railway]
        if u'public_transport' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'public_transport') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("The legacy tag is missing, add the tag highway=bus_stop / railway=tram_stop")
                err.append({'class': 9014004, 'subclass': 1713888967, 'text': mapcss.tr(u'The legacy tag is missing, add the tag highway=bus_stop / railway=tram_stop', capture_tags)})

        # node["public_transport"="platform"][bus=yes][!highway]
        if u'public_transport' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'public_transport') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'bus') == u'yes' and not mapcss._tag_capture(capture_tags, 2, tags, u'highway')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Is this a bus stop? add the tag highway=bus_stop")
            # fixAdd:"highway=bus_stop"
                err.append({'class': 9014005, 'subclass': 569497609, 'text': mapcss.tr(u'Is this a bus stop? add the tag highway=bus_stop', capture_tags), 'fix': {
                    '+': dict([
                    [u'highway',u'bus_stop']])
                }})

        # node[highway=bus_stop][note]
        # node[highway=bus_stop][note:fr][inside("FR")]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'note')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'note:fr') and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Check if the note can be deleted")
                err.append({'class': 9014006, 'subclass': 673170504, 'text': mapcss.tr(u'Check if the note can be deleted', capture_tags)})

        # node[highway=bus_stop][network][inside("FR")]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'network') and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The network should be on the transport lines and not on the stops")
            # fixRemove:"network"
                err.append({'class': 9014007, 'subclass': 1428913922, 'text': mapcss.tr(u'The network should be on the transport lines and not on the stops', capture_tags), 'fix': {
                    '-': ([
                    u'network'])
                }})

        # node[highway=bus_stop][operator][inside("FR")]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The operator should be on the transport lines and not on the stops")
            # fixRemove:"operator"
                err.append({'class': 9014008, 'subclass': 210603856, 'text': mapcss.tr(u'The operator should be on the transport lines and not on the stops', capture_tags), 'fix': {
                    '-': ([
                    u'operator'])
                }})

        # node[public_transport=platform]!.platform_ok
        # Use undeclared class platform_ok

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_pt_route = set_pt_route_master = False

        # relation[type=route][!route]
        if u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route' and not mapcss._tag_capture(capture_tags, 1, tags, u'route')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, add a tag route = bus/coach/tram/etc")
                err.append({'class': 9014009, 'subclass': 828849115, 'text': mapcss.tr(u'Missing transportation mode, add a tag route = bus/coach/tram/etc', capture_tags)})

        # relation[type=route_master][!route_master][!route]
        if u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route_master' and not mapcss._tag_capture(capture_tags, 1, tags, u'route_master') and not mapcss._tag_capture(capture_tags, 2, tags, u'route')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, add a tag route = bus/coach/tram/etc")
                err.append({'class': 9014009, 'subclass': 607011337, 'text': mapcss.tr(u'Missing transportation mode, add a tag route = bus/coach/tram/etc', capture_tags)})

        # relation[type=route_master][!route_master][route]
        if u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route_master' and not mapcss._tag_capture(capture_tags, 1, tags, u'route_master') and mapcss._tag_capture(capture_tags, 2, tags, u'route')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, chnage tag route to route_master")
            # fixChangeKey:"route=>route_master"
                err.append({'class': 9014010, 'subclass': 3385524, 'text': mapcss.tr(u'Missing transportation mode, chnage tag route to route_master', capture_tags), 'fix': {
                    '+': dict([
                    [u'route_master', mapcss.tag(tags, u'route')]]),
                    '-': ([
                    u'route'])
                }})

        # relation[type=route][route=~/^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus)$/]
        if u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route' and mapcss.regexp_test_(self.re_37f81db8, mapcss._tag_capture(capture_tags, 1, tags, u'route'))))
            except mapcss.RuleAbort: pass
            if match:
                # setpt_route
                set_pt_route = True

        # relation[type=route_master][route_master=~/^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus)$/]
        if u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route_master' and mapcss.regexp_test_(self.re_37f81db8, mapcss._tag_capture(capture_tags, 1, tags, u'route_master'))))
            except mapcss.RuleAbort: pass
            if match:
                # setpt_route_master
                set_pt_route_master = True

        # relation.pt_route[!public_transport:version]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'public_transport:version')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing public_transport:version tag on a public_transport route relation")
            # assertNoMatch:"relation type=route route=bus public_transport:version=1"
            # assertMatch:"relation type=route route=bus"
                err.append({'class': 9014011, 'subclass': 527371968, 'text': mapcss.tr(u'Missing public_transport:version tag on a public_transport route relation', capture_tags)})

        # relation.pt_route[!network]
        # relation.pt_route_master[!network]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'network')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'network')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing network tag on a public_transport relation")
            # assertNoMatch:"relation type=route route=bus network=BiBiBus"
            # assertMatch:"relation type=route route=bus"
                err.append({'class': 9014015, 'subclass': 253478598, 'text': mapcss.tr(u'Missing network tag on a public_transport relation', capture_tags)})

        # relation.pt_route[!operator]
        # relation.pt_route_master[!operator]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'operator')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'operator')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing operator tag on a public_transport relation")
            # assertNoMatch:"relation type=route route=bus operator=BiBiBus"
            # assertMatch:"relation type=route route=bus"
                err.append({'class': 9014016, 'subclass': 1639261067, 'text': mapcss.tr(u'Missing operator tag on a public_transport relation', capture_tags)})

        # relation.pt_route[!ref]
        # relation.pt_route_master[!ref]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'ref')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'ref')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing ref tag for line number on a public_transport relation")
            # assertNoMatch:"relation type=route route=bus ref=3"
            # assertMatch:"relation type=route route=bus"
                err.append({'class': 9014017, 'subclass': 1396643784, 'text': mapcss.tr(u'Missing ref tag for line number on a public_transport relation', capture_tags)})

        # relation.pt_route[!from]
        # relation.pt_route[!to]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'from')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'to')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing from/to tag on a public_transport route relation")
            # assertNoMatch:"relation type=route route=bus from=A to=B"
            # assertMatch:"relation type=route route=bus from=A"
            # assertMatch:"relation type=route route=bus to=B"
            # assertMatch:"relation type=route route=bus"
                err.append({'class': 9014018, 'subclass': 1016437930, 'text': mapcss.tr(u'Missing from/to tag on a public_transport route relation', capture_tags)})

        # relation.pt_route["fixme:relation"="order members"]
        if u'fixme:relation' in keys:
            match = False
            try: match = match or ((set_pt_route and mapcss._tag_capture(capture_tags, 0, tags, u'fixme:relation') == u'order members'))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The stops may not be in the right order")
                err.append({'class': 9014012, 'subclass': 1681682692, 'text': mapcss.tr(u'The stops may not be in the right order', capture_tags)})

        # relation.pt_route["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if u'operator' in keys:
            match = False
            try: match = match or ((set_pt_route and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Check the operator tag")
                err.append({'class': 9014013, 'subclass': 286137008, 'text': mapcss.tr(u'Check the operator tag', capture_tags)})

        # relation.pt_route["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if u'network' in keys:
            match = False
            try: match = match or ((set_pt_route and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'network')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'network')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Check the network tag")
                err.append({'class': 9014014, 'subclass': 735027962, 'text': mapcss.tr(u'Check the network tag', capture_tags)})

        # relation.pt_route!.route_ok
        # Use undeclared class route_ok, pt_route

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_transport(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.relation(data, {u'public_transport:version': u'1', u'route': u'bus', u'type': u'route'}), expected={'class': 9014011, 'subclass': 527371968})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}), expected={'class': 9014011, 'subclass': 527371968})
        self.check_not_err(n.relation(data, {u'network': u'BiBiBus', u'route': u'bus', u'type': u'route'}), expected={'class': 9014015, 'subclass': 253478598})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}), expected={'class': 9014015, 'subclass': 253478598})
        self.check_not_err(n.relation(data, {u'operator': u'BiBiBus', u'route': u'bus', u'type': u'route'}), expected={'class': 9014016, 'subclass': 1639261067})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}), expected={'class': 9014016, 'subclass': 1639261067})
        self.check_not_err(n.relation(data, {u'ref': u'3', u'route': u'bus', u'type': u'route'}), expected={'class': 9014017, 'subclass': 1396643784})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}), expected={'class': 9014017, 'subclass': 1396643784})
        self.check_not_err(n.relation(data, {u'from': u'A', u'route': u'bus', u'to': u'B', u'type': u'route'}), expected={'class': 9014018, 'subclass': 1016437930})
        self.check_err(n.relation(data, {u'from': u'A', u'route': u'bus', u'type': u'route'}), expected={'class': 9014018, 'subclass': 1016437930})
        self.check_err(n.relation(data, {u'route': u'bus', u'to': u'B', u'type': u'route'}), expected={'class': 9014018, 'subclass': 1016437930})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}), expected={'class': 9014018, 'subclass': 1016437930})
