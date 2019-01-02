#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_transport(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[21401] = {'item': 2140, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing public_transport:version tag on a public_transport route relation')}
        self.errors[21402] = {'item': 2140, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing network tag on a public_transport relation')}
        self.errors[21403] = {'item': 2140, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing operator tag on a public_transport relation')}
        self.errors[21404] = {'item': 2140, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing ref tag for line number on a public_transport relation')}
        self.errors[21405] = {'item': 2140, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing from/to tag on a public_transport route relation')}
        self.errors[21411] = {'item': 2140, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing public_transport tag on a public transport stop')}
        self.errors[21412] = {'item': 2140, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing legacy tag on a public transport stop')}
        self.errors[9014002] = {'item': 9014, 'level': 2, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Is it a bus stop or a bus station?')}
        self.errors[9014006] = {'item': 9014, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Check if the note can be deleted')}
        self.errors[9014007] = {'item': 9014, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'The network should be on the transport lines and not on the stops')}
        self.errors[9014008] = {'item': 9014, 'level': 3, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'The operator should be on the transport lines and not on the stops')}
        self.errors[9014009] = {'item': 9014, 'level': 2, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing transportation mode, add a tag route = bus/coach/tram/etc')}
        self.errors[9014010] = {'item': 9014, 'level': 2, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Missing transportation mode, change tag route to route_master')}
        self.errors[9014013] = {'item': 9014, 'level': 2, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Check the operator tag')}
        self.errors[9014014] = {'item': 9014, 'level': 2, 'tag': mapcss.list_(u'tag', u'public_transport'), 'desc': mapcss.tr(u'Check the network tag')}

        self.re_25554804 = re.compile(ur'STIF|Kéolis|Véolia')
        self.re_37f81db8 = re.compile(ur'^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_pt_route = set_pt_route_master = False

        # node[highway=bus_stop][amenity=bus_station]
        if (u'amenity' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'bus_stop') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'bus_station'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Is it a bus stop or a bus station?")
                # fixRemove:"amenity"
                err.append({'class': 9014002, 'subclass': 1676203359, 'text': mapcss.tr(u'Is it a bus stop or a bus station?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'amenity'])
                }})

        # node[highway=bus_stop][!public_transport]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'bus_stop') and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing public_transport tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21411:0/3"
                # throwError:tr("Specify if it is a stop (platform) or a location on the road (stop_position)")
                # fixAdd:"public_transport=platform"
                # assertNoMatch:"node highway=bus_stop public_transport=platform"
                # assertNoMatch:"node highway=bus_stop public_transport=stop_position"
                # assertMatch:"node highway=bus_stop"
                err.append({'class': 21411, 'subclass': 0, 'text': mapcss.tr(u'Specify if it is a stop (platform) or a location on the road (stop_position)'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'public_transport',u'platform']])
                }})

        # node[railway=tram_stop][!public_transport]
        if (u'railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'railway') == mapcss._value_capture(capture_tags, 0, u'tram_stop') and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing public_transport tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21411:1/3"
                # throwError:tr("Specify if it is a stop (platform) or a location on the rails (stop_position)")
                # fixAdd:"public_transport=stop_position"
                # assertNoMatch:"node railway=tram_stop public_transport=platform"
                # assertNoMatch:"node railway=tram_stop public_transport=stop_position"
                # assertMatch:"node railway=tram_stop"
                err.append({'class': 21411, 'subclass': 1, 'text': mapcss.tr(u'Specify if it is a stop (platform) or a location on the rails (stop_position)'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'public_transport',u'stop_position']])
                }})

        # node[public_transport=platform][!highway][!railway][!bus][!shelter]
        if (u'public_transport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'public_transport') == mapcss._value_capture(capture_tags, 0, u'platform') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and not mapcss._tag_capture(capture_tags, 3, tags, u'bus') and not mapcss._tag_capture(capture_tags, 4, tags, u'shelter'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing legacy tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21412:1/3"
                # throwError:tr("The legacy tag is missing, add the tag highway=bus_stop / railway=tram_stop")
                err.append({'class': 21412, 'subclass': 1, 'text': mapcss.tr(u'The legacy tag is missing, add the tag highway=bus_stop / railway=tram_stop')})

        # node[public_transport=platform][!highway][!railway][bus=yes]
        # node[public_transport=platform][!highway][!railway][shelter]
        if (u'bus' in keys and u'public_transport' in keys) or (u'public_transport' in keys and u'shelter' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'public_transport') == mapcss._value_capture(capture_tags, 0, u'platform') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and mapcss._tag_capture(capture_tags, 3, tags, u'bus') == mapcss._value_capture(capture_tags, 3, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'public_transport') == mapcss._value_capture(capture_tags, 0, u'platform') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and mapcss._tag_capture(capture_tags, 3, tags, u'shelter'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing legacy tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21412:0/3"
                # throwError:tr("Is this a bus stop? add the tag highway=bus_stop")
                # fixAdd:"highway=bus_stop"
                # assertMatch:"node public_transport=platform shelter=yes"
                err.append({'class': 21412, 'subclass': 0, 'text': mapcss.tr(u'Is this a bus stop? add the tag highway=bus_stop'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'highway',u'bus_stop']])
                }})

        # node[highway=bus_stop][note]
        # node[highway=bus_stop][note:fr][inside("FR")]
        if (u'highway' in keys and u'note' in keys) or (u'highway' in keys and u'note:fr' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'bus_stop') and mapcss._tag_capture(capture_tags, 1, tags, u'note'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'bus_stop') and mapcss._tag_capture(capture_tags, 1, tags, u'note:fr') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Check if the note can be deleted")
                err.append({'class': 9014006, 'subclass': 673170504, 'text': mapcss.tr(u'Check if the note can be deleted')})

        # node[highway=bus_stop][network][inside("FR")]
        if (u'highway' in keys and u'network' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'bus_stop') and mapcss._tag_capture(capture_tags, 1, tags, u'network') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The network should be on the transport lines and not on the stops")
                # fixRemove:"network"
                err.append({'class': 9014007, 'subclass': 1428913922, 'text': mapcss.tr(u'The network should be on the transport lines and not on the stops'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'network'])
                }})

        # node[highway=bus_stop][operator][inside("FR")]
        if (u'highway' in keys and u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'bus_stop') and mapcss._tag_capture(capture_tags, 1, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The operator should be on the transport lines and not on the stops")
                # fixRemove:"operator"
                err.append({'class': 9014008, 'subclass': 210603856, 'text': mapcss.tr(u'The operator should be on the transport lines and not on the stops'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'operator'])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_pt_route = set_pt_route_master = False

        # relation[type=route][!route]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route') and not mapcss._tag_capture(capture_tags, 1, tags, u'route'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, add a tag route = bus/coach/tram/etc")
                err.append({'class': 9014009, 'subclass': 828849115, 'text': mapcss.tr(u'Missing transportation mode, add a tag route = bus/coach/tram/etc')})

        # relation[type=route_master][!route_master][!route]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route_master') and not mapcss._tag_capture(capture_tags, 1, tags, u'route_master') and not mapcss._tag_capture(capture_tags, 2, tags, u'route'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, add a tag route = bus/coach/tram/etc")
                err.append({'class': 9014009, 'subclass': 607011337, 'text': mapcss.tr(u'Missing transportation mode, add a tag route = bus/coach/tram/etc')})

        # relation[type=route_master][!route_master][route]
        if (u'route' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route_master') and not mapcss._tag_capture(capture_tags, 1, tags, u'route_master') and mapcss._tag_capture(capture_tags, 2, tags, u'route'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, change tag route to route_master")
                # fixChangeKey:"route=>route_master"
                err.append({'class': 9014010, 'subclass': 3385524, 'text': mapcss.tr(u'Missing transportation mode, change tag route to route_master'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'route_master', mapcss.tag(tags, u'route')]]),
                    '-': ([
                    u'route'])
                }})

        # relation[type=route][route=~/^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus)$/]
        if (u'route' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_37f81db8), mapcss._tag_capture(capture_tags, 1, tags, u'route')))
                except mapcss.RuleAbort: pass
            if match:
                # setpt_route
                set_pt_route = True

        # relation[type=route_master][route_master=~/^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus)$/]
        if (u'route_master' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route_master') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_37f81db8), mapcss._tag_capture(capture_tags, 1, tags, u'route_master')))
                except mapcss.RuleAbort: pass
            if match:
                # setpt_route_master
                set_pt_route_master = True

        # relation.pt_route[!public_transport:version]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'public_transport:version'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21401/3"
                # throwError:tr("Missing public_transport:version tag on a public_transport route relation")
                # assertNoMatch:"relation type=route route=bus public_transport:version=1"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21401, 'subclass': 0, 'text': mapcss.tr(u'Missing public_transport:version tag on a public_transport route relation')})

        # relation.pt_route[!network]
        # relation.pt_route_master[!network]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'network'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'network'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21402/3"
                # throwError:tr("Missing network tag on a public_transport relation")
                # assertNoMatch:"relation type=route route=bus network=BiBiBus"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21402, 'subclass': 0, 'text': mapcss.tr(u'Missing network tag on a public_transport relation')})

        # relation.pt_route[!operator]
        # relation.pt_route_master[!operator]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'operator'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'operator'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21403/3"
                # throwError:tr("Missing operator tag on a public_transport relation")
                # assertNoMatch:"relation type=route route=bus operator=BiBiBus"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21403, 'subclass': 0, 'text': mapcss.tr(u'Missing operator tag on a public_transport relation')})

        # relation.pt_route[!ref]
        # relation.pt_route_master[!ref]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21404/3"
                # throwError:tr("Missing ref tag for line number on a public_transport relation")
                # assertNoMatch:"relation type=route route=bus ref=3"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21404, 'subclass': 0, 'text': mapcss.tr(u'Missing ref tag for line number on a public_transport relation')})

        # relation.pt_route[!from]
        # relation.pt_route[!to]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'from'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'to'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21405/3"
                # throwError:tr("Missing from/to tag on a public_transport route relation")
                # assertNoMatch:"relation type=route route=bus from=A to=B"
                # assertMatch:"relation type=route route=bus from=A"
                # assertMatch:"relation type=route route=bus to=B"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21405, 'subclass': 0, 'text': mapcss.tr(u'Missing from/to tag on a public_transport route relation')})

        # relation.pt_route["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if (u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_25554804), mapcss._tag_capture(capture_tags, 0, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (set_pt_route_master and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_25554804), mapcss._tag_capture(capture_tags, 0, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Check the operator tag")
                err.append({'class': 9014013, 'subclass': 286137008, 'text': mapcss.tr(u'Check the operator tag')})

        # relation.pt_route["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if (u'network' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (set_pt_route and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_25554804), mapcss._tag_capture(capture_tags, 0, tags, u'network')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (set_pt_route_master and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_25554804), mapcss._tag_capture(capture_tags, 0, tags, u'network')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Check the network tag")
                err.append({'class': 9014014, 'subclass': 735027962, 'text': mapcss.tr(u'Check the network tag')})

        # relation.pt_route!.route_ok
        # Use undeclared class pt_route, route_ok

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_transport(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {u'highway': u'bus_stop', u'public_transport': u'platform'}), expected={'class': 21411, 'subclass': 0})
        self.check_not_err(n.node(data, {u'highway': u'bus_stop', u'public_transport': u'stop_position'}), expected={'class': 21411, 'subclass': 0})
        self.check_err(n.node(data, {u'highway': u'bus_stop'}), expected={'class': 21411, 'subclass': 0})
        self.check_not_err(n.node(data, {u'public_transport': u'platform', u'railway': u'tram_stop'}), expected={'class': 21411, 'subclass': 1})
        self.check_not_err(n.node(data, {u'public_transport': u'stop_position', u'railway': u'tram_stop'}), expected={'class': 21411, 'subclass': 1})
        self.check_err(n.node(data, {u'railway': u'tram_stop'}), expected={'class': 21411, 'subclass': 1})
        self.check_err(n.node(data, {u'public_transport': u'platform', u'shelter': u'yes'}), expected={'class': 21412, 'subclass': 0})
        self.check_not_err(n.relation(data, {u'public_transport:version': u'1', u'route': u'bus', u'type': u'route'}, []), expected={'class': 21401, 'subclass': 0})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}, []), expected={'class': 21401, 'subclass': 0})
        self.check_not_err(n.relation(data, {u'network': u'BiBiBus', u'route': u'bus', u'type': u'route'}, []), expected={'class': 21402, 'subclass': 0})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}, []), expected={'class': 21402, 'subclass': 0})
        self.check_not_err(n.relation(data, {u'operator': u'BiBiBus', u'route': u'bus', u'type': u'route'}, []), expected={'class': 21403, 'subclass': 0})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}, []), expected={'class': 21403, 'subclass': 0})
        self.check_not_err(n.relation(data, {u'ref': u'3', u'route': u'bus', u'type': u'route'}, []), expected={'class': 21404, 'subclass': 0})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}, []), expected={'class': 21404, 'subclass': 0})
        self.check_not_err(n.relation(data, {u'from': u'A', u'route': u'bus', u'to': u'B', u'type': u'route'}, []), expected={'class': 21405, 'subclass': 0})
        self.check_err(n.relation(data, {u'from': u'A', u'route': u'bus', u'type': u'route'}, []), expected={'class': 21405, 'subclass': 0})
        self.check_err(n.relation(data, {u'route': u'bus', u'to': u'B', u'type': u'route'}, []), expected={'class': 21405, 'subclass': 0})
        self.check_err(n.relation(data, {u'route': u'bus', u'type': u'route'}, []), expected={'class': 21405, 'subclass': 0})
