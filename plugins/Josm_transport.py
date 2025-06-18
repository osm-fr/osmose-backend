#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_transport(PluginMapCSS):
    # ------------------------------- IMPORTANT -------------------------------
    # This file is generated automatically and should not be modified directly.
    # Instead, modify the source mapcss file and regenerate this Python script.
    # -------------------------------------------------------------------------

    MAPCSS_URL = 'https://github.com/Jungle-Bus/transport_mapcss/blob/master/transport.validator.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[21401] = self.def_class(item = 2140, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing public_transport:version tag on a public_transport route relation'))
        self.errors[21402] = self.def_class(item = 2140, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing network tag on a public_transport relation'))
        self.errors[21403] = self.def_class(item = 2140, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing operator tag on a public_transport relation'))
        self.errors[21405] = self.def_class(item = 2140, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing from/to tag on a public_transport route relation'))
        self.errors[21411] = self.def_class(item = 2140, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing public_transport tag on a public transport stop'))
        self.errors[21412] = self.def_class(item = 2140, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing legacy tag on a public transport stop'))
        self.errors[9014002] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Is it a bus stop or a bus station?'))
        self.errors[9014006] = self.def_class(item = 9014, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Check if the note can be deleted'))
        self.errors[9014007] = self.def_class(item = 9014, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('The network should be on the transport lines and not on the stops'))
        self.errors[9014008] = self.def_class(item = 9014, level = 3, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('The operator should be on the transport lines and not on the stops'))
        self.errors[9014009] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing transportation mode, add a tag route = bus/coach/tram/etc'))
        self.errors[9014010] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing transportation mode, change tag route to route_master'))
        self.errors[9014019] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('A bus stop is supposed to be a node'))
        self.errors[9014020] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('The color of the public transport line should be in a colour tag'))
        self.errors[9014021] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('The interval is invalid (try a number of minutes)'))
        self.errors[9014022] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('The duration is invalid (try a number of minutes)'))
        self.errors[9014023] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing interval tag to specify the main interval'))
        self.errors[9014024] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Missing opening_hours tag'))
        self.errors[9014025] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Check the operator tag : this operator does not exist, it may be a typo'))
        self.errors[9014026] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Check the network tag : this network does not exist, it may be a typo'))
        self.errors[9014027] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('Subway entrances should be mapped as nodes'))
        self.errors[9014028] = self.def_class(item = 9014, level = 2, tags = mapcss.list_('tag', 'public_transport'), title = mapcss.tr('The line variant does not belong to any line, add it to the route_master relation'))

        self.re_25554804 = re.compile(r'STIF|Kéolis|Véolia')
        self.re_2fe0817d = re.compile(r'^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$')
        self.re_6194d2a4 = re.compile(r'^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus|walking_bus)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_pt_route = set_pt_route_master = set_pt_route_probably_v2 = False

        # node[highway=bus_stop][amenity=bus_station]
        if ('amenity' in keys and 'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity') == mapcss._value_capture(capture_tags, 1, 'bus_station')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Is it a bus stop or a bus station?")
                # fixRemove:"amenity"
                err.append({'class': 9014002, 'subclass': 1676203359, 'text': mapcss.tr('Is it a bus stop or a bus station?'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'amenity'])
                }})

        # node[highway=bus_stop][!public_transport]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'public_transport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing public_transport tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21411:0/3"
                # throwError:tr("Specify if it is a stop (platform) or a location on the road (stop_position)")
                # fixAdd:"public_transport=platform"
                # assertNoMatch:"node highway=bus_stop public_transport=platform"
                # assertNoMatch:"node highway=bus_stop public_transport=stop_position"
                # assertMatch:"node highway=bus_stop"
                err.append({'class': 21411, 'subclass': 0, 'text': mapcss.tr('Specify if it is a stop (platform) or a location on the road (stop_position)'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['public_transport','platform']])
                }})

        # node[railway=tram_stop][!public_transport]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'tram_stop')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'public_transport')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing public_transport tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21411:1/3"
                # throwError:tr("Specify if it is a stop (platform) or a location on the rails (stop_position)")
                # fixAdd:"public_transport=stop_position"
                # assertNoMatch:"node railway=tram_stop public_transport=platform"
                # assertNoMatch:"node railway=tram_stop public_transport=stop_position"
                # assertMatch:"node railway=tram_stop"
                err.append({'class': 21411, 'subclass': 1, 'text': mapcss.tr('Specify if it is a stop (platform) or a location on the rails (stop_position)'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['public_transport','stop_position']])
                }})

        # node[public_transport=platform][!highway][!railway][!bus][!tram][!ferry][!walking_bus]
        if ('public_transport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'public_transport') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'railway')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'bus')) and (not mapcss._tag_capture(capture_tags, 4, tags, 'tram')) and (not mapcss._tag_capture(capture_tags, 5, tags, 'ferry')) and (not mapcss._tag_capture(capture_tags, 6, tags, 'walking_bus')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing legacy tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21412:1/3"
                # throwError:tr("Is this a bus or tram stop ? Add a tag to precise the kind of platform")
                err.append({'class': 21412, 'subclass': 1, 'text': mapcss.tr('Is this a bus or tram stop ? Add a tag to precise the kind of platform')})

        # node[public_transport=platform][!highway][!railway][bus=yes]
        if ('bus' in keys and 'public_transport' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'public_transport') == mapcss._value_capture(capture_tags, 0, 'platform')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'railway')) and (mapcss._tag_capture(capture_tags, 3, tags, 'bus') == mapcss._value_capture(capture_tags, 3, 'yes')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Missing legacy tag on a public transport stop")
                # -osmoseItemClassLevel:"2140/21412:0/3"
                # throwError:tr("Is this a bus stop? add the tag highway=bus_stop")
                # fixAdd:"highway=bus_stop"
                # assertMatch:"node public_transport=platform bus=yes"
                err.append({'class': 21412, 'subclass': 0, 'text': mapcss.tr('Is this a bus stop? add the tag highway=bus_stop'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['highway','bus_stop']])
                }})

        # node[highway=bus_stop][note]
        # node[highway=bus_stop][note:fr][inside("FR")]
        if ('highway' in keys and 'note' in keys) or ('highway' in keys and 'note:fr' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')) and (mapcss._tag_capture(capture_tags, 1, tags, 'note')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')) and (mapcss._tag_capture(capture_tags, 1, tags, 'note:fr')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Check if the note can be deleted")
                err.append({'class': 9014006, 'subclass': 673170504, 'text': mapcss.tr('Check if the note can be deleted')})

        # node[highway=bus_stop][network][inside("FR")]
        if ('highway' in keys and 'network' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')) and (mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The network should be on the transport lines and not on the stops")
                # fixRemove:"network"
                err.append({'class': 9014007, 'subclass': 1428913922, 'text': mapcss.tr('The network should be on the transport lines and not on the stops'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'network'])
                }})

        # node[highway=bus_stop][operator][inside("FR")]
        if ('highway' in keys and 'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')) and (mapcss._tag_capture(capture_tags, 1, tags, 'operator')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("The operator should be on the transport lines and not on the stops")
                # fixRemove:"operator"
                err.append({'class': 9014008, 'subclass': 210603856, 'text': mapcss.tr('The operator should be on the transport lines and not on the stops'), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'operator'])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_pt_route = set_pt_route_master = set_pt_route_probably_v2 = False

        # way[highway=bus_stop]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("A bus stop is supposed to be a node")
                err.append({'class': 9014019, 'subclass': 1153984743, 'text': mapcss.tr('A bus stop is supposed to be a node')})

        # way[railway=subway_entrance]
        # way[railway=train_station_entrance]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'subway_entrance')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'train_station_entrance')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Subway entrances should be mapped as nodes")
                # assertMatch:"way railway=subway_entrance"
                err.append({'class': 9014027, 'subclass': 514884813, 'text': mapcss.tr('Subway entrances should be mapped as nodes')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_pt_route = set_pt_route_master = set_pt_route_probably_v2 = False

        # relation[type=route][!route][!disused:route]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'route')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'route')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'disused:route')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, add a tag route = bus/coach/tram/etc")
                err.append({'class': 9014009, 'subclass': 1678105256, 'text': mapcss.tr('Missing transportation mode, add a tag route = bus/coach/tram/etc')})

        # relation[type=route_master][!route_master][!route][!disused:route_master]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'route_master')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'route_master')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'route')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'disused:route_master')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, add a tag route = bus/coach/tram/etc")
                err.append({'class': 9014009, 'subclass': 1165025485, 'text': mapcss.tr('Missing transportation mode, add a tag route = bus/coach/tram/etc')})

        # relation[type=route_master][!route_master][route]
        if ('route' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'route_master')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'route_master')) and (mapcss._tag_capture(capture_tags, 2, tags, 'route')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing transportation mode, change tag route to route_master")
                # fixChangeKey:"route=>route_master"
                err.append({'class': 9014010, 'subclass': 3385524, 'text': mapcss.tr('Missing transportation mode, change tag route to route_master'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['route_master', mapcss.tag(tags, 'route')]]),
                    '-': ([
                    'route'])
                }})

        # relation[type=route][route=~/^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus|walking_bus)$/]
        if ('route' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'route')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6194d2a4), mapcss._tag_capture(capture_tags, 1, tags, 'route'))))
                except mapcss.RuleAbort: pass
            if match:
                # set pt_route
                set_pt_route = True

        # relation[type=route_master][route_master=~/^(bus|coach|train|subway|monorail|trolleybus|aerialway|funicular|ferry|tram|share_taxi|light_rail|school_bus|walking_bus)$/]
        if ('route_master' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'route_master')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6194d2a4), mapcss._tag_capture(capture_tags, 1, tags, 'route_master'))))
                except mapcss.RuleAbort: pass
            if match:
                # set pt_route_master
                set_pt_route_master = True

        # relation.route_in_master.pt_route
        if True:
            match = False
            # Skip selector using undeclared class pt_route, route_in_master
            if match:
                # set pt_route_probably_v2
                set_pt_route_probably_v2 = True

        # relation.pt_route[!public_transport:version]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (not mapcss._tag_capture(capture_tags, 1, tags, 'public_transport:version')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21401/3"
                # throwError:tr("Missing public_transport:version tag on a public_transport route relation")
                # assertNoMatch:"relation type=route route=bus public_transport:version=1"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21401, 'subclass': 0, 'text': mapcss.tr('Missing public_transport:version tag on a public_transport route relation')})

        # relation.pt_route[!network]
        # relation.pt_route_master[!network]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (not mapcss._tag_capture(capture_tags, 1, tags, 'network')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (not mapcss._tag_capture(capture_tags, 1, tags, 'network')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21402/3"
                # throwError:tr("Missing network tag on a public_transport relation")
                # assertNoMatch:"relation type=route route=bus network=BiBiBus"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21402, 'subclass': 0, 'text': mapcss.tr('Missing network tag on a public_transport relation')})

        # relation.pt_route[!operator]
        # relation.pt_route_master[!operator]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (not mapcss._tag_capture(capture_tags, 1, tags, 'operator')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (not mapcss._tag_capture(capture_tags, 1, tags, 'operator')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21403/3"
                # throwError:tr("Missing operator tag on a public_transport relation")
                # assertNoMatch:"relation type=route route=bus operator=BiBiBus"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21403, 'subclass': 0, 'text': mapcss.tr('Missing operator tag on a public_transport relation')})

        # relation.pt_route[!from]
        # relation.pt_route[!to]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (not mapcss._tag_capture(capture_tags, 1, tags, 'from')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (not mapcss._tag_capture(capture_tags, 1, tags, 'to')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2140/21405/3"
                # throwError:tr("Missing from/to tag on a public_transport route relation")
                # assertNoMatch:"relation type=route route=bus from=A to=B"
                # assertMatch:"relation type=route route=bus from=A"
                # assertMatch:"relation type=route route=bus to=B"
                # assertMatch:"relation type=route route=bus"
                err.append({'class': 21405, 'subclass': 0, 'text': mapcss.tr('Missing from/to tag on a public_transport route relation')})

        # relation.pt_route[tag(network)!=parent_tag(network)]
        # Part of rule not implemented

        # relation.pt_route[tag(operator)!=parent_tag(operator)]
        # Part of rule not implemented

        # relation.pt_route[tag(ref)!=parent_tag(ref)]
        # Part of rule not implemented

        # relation.pt_route[tag(colour)!=parent_tag(colour)]
        # Part of rule not implemented

        # relation.pt_route[tag(route)!=parent_tag(route_master)]
        # Part of rule not implemented

        # relation.pt_route[!colour][color]
        # relation.pt_route_master[!colour][color]
        if ('color' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (not mapcss._tag_capture(capture_tags, 1, tags, 'colour')) and (mapcss._tag_capture(capture_tags, 2, tags, 'color')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (not mapcss._tag_capture(capture_tags, 1, tags, 'colour')) and (mapcss._tag_capture(capture_tags, 2, tags, 'color')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("The color of the public transport line should be in a colour tag")
                # fixChangeKey:"color=>colour"
                err.append({'class': 9014020, 'subclass': 218794881, 'text': mapcss.tr('The color of the public transport line should be in a colour tag'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['colour', mapcss.tag(tags, 'color')]]),
                    '-': ([
                    'color'])
                }})

        # relation.pt_route["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if ('operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_25554804), mapcss._tag_capture(capture_tags, 1, tags, 'operator'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_25554804), mapcss._tag_capture(capture_tags, 1, tags, 'operator'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Check the operator tag : this operator does not exist, it may be a typo")
                err.append({'class': 9014025, 'subclass': 286137008, 'text': mapcss.tr('Check the operator tag : this operator does not exist, it may be a typo')})

        # relation.pt_route["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if ('network' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_25554804), mapcss._tag_capture(capture_tags, 1, tags, 'network'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_25554804), mapcss._tag_capture(capture_tags, 1, tags, 'network'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Check the network tag : this network does not exist, it may be a typo")
                err.append({'class': 9014026, 'subclass': 735027962, 'text': mapcss.tr('Check the network tag : this network does not exist, it may be a typo')})

        # relation[highway=bus_stop]
        if ('highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'bus_stop')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("A bus stop is supposed to be a node")
                err.append({'class': 9014019, 'subclass': 1590282811, 'text': mapcss.tr('A bus stop is supposed to be a node')})

        # relation.pt_route!.route_ok
        if True:
            match = False
            # Skip selector using undeclared class pt_route, route_ok
            if match:
                # throwError:tr("The line variant does not belong to any line, add it to the route_master relation")
                err.append({'class': 9014028, 'subclass': 1286525207, 'text': mapcss.tr('The line variant does not belong to any line, add it to the route_master relation')})

        # relation.pt_route[interval][interval!~/^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$/]
        # relation.pt_route_master[interval][interval!~/^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$/]
        if ('interval' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (mapcss._tag_capture(capture_tags, 1, tags, 'interval')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2fe0817d, '^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$'), mapcss._tag_capture(capture_tags, 2, tags, 'interval'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (mapcss._tag_capture(capture_tags, 1, tags, 'interval')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2fe0817d, '^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$'), mapcss._tag_capture(capture_tags, 2, tags, 'interval'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("The interval is invalid (try a number of minutes)")
                # assertNoMatch:"relation type=route route=bus interval=00:05"
                # assertNoMatch:"relation type=route route=bus interval=00:10:00"
                # assertMatch:"relation type=route route=bus interval=00:70:00"
                # assertNoMatch:"relation type=route route=bus interval=02:00:00"
                # assertNoMatch:"relation type=route route=bus interval=10"
                # assertNoMatch:"relation type=route route=bus interval=120"
                # assertNoMatch:"relation type=route route=bus interval=5"
                # assertMatch:"relation type=route route=bus interval=irregular"
                # assertMatch:"relation type=route route=ferry interval=2heures"
                # assertMatch:"relation type=route_master route_master=bus interval=1240"
                err.append({'class': 9014021, 'subclass': 170114261, 'text': mapcss.tr('The interval is invalid (try a number of minutes)')})

        # relation.pt_route[duration][duration!~/^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$/]
        # relation.pt_route_master[duration][duration!~/^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$/]
        if ('duration' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (mapcss._tag_capture(capture_tags, 1, tags, 'duration')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2fe0817d, '^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$'), mapcss._tag_capture(capture_tags, 2, tags, 'duration'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (mapcss._tag_capture(capture_tags, 1, tags, 'duration')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2fe0817d, '^([0-9][0-9]?[0-9]?|[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?)$'), mapcss._tag_capture(capture_tags, 2, tags, 'duration'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("The duration is invalid (try a number of minutes)")
                # assertMatch:"relation type=route route=bus duration=20minutes"
                # assertNoMatch:"relation type=route route=bus duration=25:00"
                # assertNoMatch:"relation type=route route=ferry duration=120"
                # assertMatch:"relation type=route route=ferry duration=1240"
                # assertNoMatch:"relation type=route route=ferry duration=20"
                # assertNoMatch:"relation type=route_master route=bus duration=02:00:00"
                # assertNoMatch:"relation type=route_master route_master=bus duration=5"
                err.append({'class': 9014022, 'subclass': 317647061, 'text': mapcss.tr('The duration is invalid (try a number of minutes)')})

        # relation.pt_route["interval:conditional"][!interval]
        # relation.pt_route_master["interval:conditional"][!interval]
        if ('interval:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (mapcss._tag_capture(capture_tags, 1, tags, 'interval:conditional')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'interval')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (mapcss._tag_capture(capture_tags, 1, tags, 'interval:conditional')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'interval')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing interval tag to specify the main interval")
                err.append({'class': 9014023, 'subclass': 1710360237, 'text': mapcss.tr('Missing interval tag to specify the main interval')})

        # relation.pt_route["interval:conditional"][!opening_hours]
        # relation.pt_route_master["interval:conditional"][!opening_hours]
        if ('interval:conditional' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route) and (mapcss._tag_capture(capture_tags, 1, tags, 'interval:conditional')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((set_pt_route_master) and (mapcss._tag_capture(capture_tags, 1, tags, 'interval:conditional')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'opening_hours')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Missing opening_hours tag")
                err.append({'class': 9014024, 'subclass': 210081506, 'text': mapcss.tr('Missing opening_hours tag')})

        # relation[railway=subway_entrance]
        # relation[railway=train_station_entrance]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'subway_entrance')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'train_station_entrance')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("Subway entrances should be mapped as nodes")
                err.append({'class': 9014027, 'subclass': 569512108, 'text': mapcss.tr('Subway entrances should be mapped as nodes')})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_transport(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {'highway': 'bus_stop', 'public_transport': 'platform'}), expected={'class': 21411, 'subclass': 0})
        self.check_not_err(n.node(data, {'highway': 'bus_stop', 'public_transport': 'stop_position'}), expected={'class': 21411, 'subclass': 0})
        self.check_err(n.node(data, {'highway': 'bus_stop'}), expected={'class': 21411, 'subclass': 0})
        self.check_not_err(n.node(data, {'public_transport': 'platform', 'railway': 'tram_stop'}), expected={'class': 21411, 'subclass': 1})
        self.check_not_err(n.node(data, {'public_transport': 'stop_position', 'railway': 'tram_stop'}), expected={'class': 21411, 'subclass': 1})
        self.check_err(n.node(data, {'railway': 'tram_stop'}), expected={'class': 21411, 'subclass': 1})
        self.check_err(n.node(data, {'bus': 'yes', 'public_transport': 'platform'}), expected={'class': 21412, 'subclass': 0})
        self.check_err(n.way(data, {'railway': 'subway_entrance'}, [0]), expected={'class': 9014027, 'subclass': 514884813})
        self.check_not_err(n.relation(data, {'public_transport:version': '1', 'route': 'bus', 'type': 'route'}, []), expected={'class': 21401, 'subclass': 0})
        self.check_err(n.relation(data, {'route': 'bus', 'type': 'route'}, []), expected={'class': 21401, 'subclass': 0})
        self.check_not_err(n.relation(data, {'network': 'BiBiBus', 'route': 'bus', 'type': 'route'}, []), expected={'class': 21402, 'subclass': 0})
        self.check_err(n.relation(data, {'route': 'bus', 'type': 'route'}, []), expected={'class': 21402, 'subclass': 0})
        self.check_not_err(n.relation(data, {'operator': 'BiBiBus', 'route': 'bus', 'type': 'route'}, []), expected={'class': 21403, 'subclass': 0})
        self.check_err(n.relation(data, {'route': 'bus', 'type': 'route'}, []), expected={'class': 21403, 'subclass': 0})
        self.check_not_err(n.relation(data, {'from': 'A', 'route': 'bus', 'to': 'B', 'type': 'route'}, []), expected={'class': 21405, 'subclass': 0})
        self.check_err(n.relation(data, {'from': 'A', 'route': 'bus', 'type': 'route'}, []), expected={'class': 21405, 'subclass': 0})
        self.check_err(n.relation(data, {'route': 'bus', 'to': 'B', 'type': 'route'}, []), expected={'class': 21405, 'subclass': 0})
        self.check_err(n.relation(data, {'route': 'bus', 'type': 'route'}, []), expected={'class': 21405, 'subclass': 0})
        self.check_not_err(n.relation(data, {'interval': '00:05', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_not_err(n.relation(data, {'interval': '00:10:00', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_err(n.relation(data, {'interval': '00:70:00', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_not_err(n.relation(data, {'interval': '02:00:00', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_not_err(n.relation(data, {'interval': '10', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_not_err(n.relation(data, {'interval': '120', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_not_err(n.relation(data, {'interval': '5', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_err(n.relation(data, {'interval': 'irregular', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_err(n.relation(data, {'interval': '2heures', 'route': 'ferry', 'type': 'route'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_err(n.relation(data, {'interval': '1240', 'route_master': 'bus', 'type': 'route_master'}, []), expected={'class': 9014021, 'subclass': 170114261})
        self.check_err(n.relation(data, {'duration': '20minutes', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014022, 'subclass': 317647061})
        self.check_not_err(n.relation(data, {'duration': '25:00', 'route': 'bus', 'type': 'route'}, []), expected={'class': 9014022, 'subclass': 317647061})
        self.check_not_err(n.relation(data, {'duration': '120', 'route': 'ferry', 'type': 'route'}, []), expected={'class': 9014022, 'subclass': 317647061})
        self.check_err(n.relation(data, {'duration': '1240', 'route': 'ferry', 'type': 'route'}, []), expected={'class': 9014022, 'subclass': 317647061})
        self.check_not_err(n.relation(data, {'duration': '20', 'route': 'ferry', 'type': 'route'}, []), expected={'class': 9014022, 'subclass': 317647061})
        self.check_not_err(n.relation(data, {'duration': '02:00:00', 'route': 'bus', 'type': 'route_master'}, []), expected={'class': 9014022, 'subclass': 317647061})
        self.check_not_err(n.relation(data, {'duration': '5', 'route_master': 'bus', 'type': 'route_master'}, []), expected={'class': 9014022, 'subclass': 317647061})
