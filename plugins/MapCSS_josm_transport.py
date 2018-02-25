#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_transport(Plugin):

    only_for = ['FR']

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9014001] = {'item': 9014, 'level': 3, 'tag': [], 'desc': {'en': u'Jungle : L\'arrêt n\'a pas de nom'}}
        self.errors[9014002] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Est-ce un arrêt de bus ou une gare routière ?'}}
        self.errors[9014003] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Préciser s\'il s\'agit d\'un arrêt (platform) ou d\'un emplacement sur la route (stop_position)'}}
        self.errors[9014004] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Le tag historique est manquant (ajouter le tag highway=bus_stop/railway=tram_stop)'}}
        self.errors[9014005] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Est-ce un arrêt de bus ? (ajouter le tag highway=bus_stop)'}}
        self.errors[9014006] = {'item': 9014, 'level': 3, 'tag': [], 'desc': {'en': u'Jungle : Vérifier si la note peut être supprimée'}}
        self.errors[9014007] = {'item': 9014, 'level': 3, 'tag': [], 'desc': {'en': u'Jungle : Le réseau devrait être porté par les lignes de transport et non par les arrêts'}}
        self.errors[9014008] = {'item': 9014, 'level': 3, 'tag': [], 'desc': {'en': u'Jungle : L\'opérateur devrait être porté par les lignes de transport et non par les arrêts'}}
        self.errors[9014009] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Le mode est manquant (ajouter un tag route = bus/coach/tram/etc)'}}
        self.errors[9014010] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Le mode est manquant (ajouter un tag route_master = bus/coach/tram/etc)'}}
        self.errors[9014011] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Le mode est manquant (transformer le tag route en route_master)'}}
        self.errors[9014012] = {'item': 9014, 'level': 3, 'tag': [], 'desc': {'en': u'Jungle : Les arrêts ne sont peut-être pas dans le bon ordre'}}
        self.errors[9014013] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Vérifier l\'opérateur'}}
        self.errors[9014014] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Vérifier le réseau'}}
        self.errors[9014015] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Le réseau est manquant (ajouter un tag network)'}}
        self.errors[9014016] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : L\'opérateur est manquant (ajouter un tag operator)'}}
        self.errors[9014017] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : Le numéro de ligne est manquant (ajouter un tag ref)'}}
        self.errors[9014018] = {'item': 9014, 'level': 2, 'tag': [], 'desc': {'en': u'Jungle : L\'origine/destination est manquante (ajouter les tags from/to)'}}

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
                # throwWarning:"Jungle : L'arrêt n'a pas de nom"
                err.append({'class': 9014001, 'subclass': 1368699603, 'text': {'en': u'Jungle : L\'arrêt n\'a pas de nom'}})

        # node[highway=bus_stop][amenity=bus_station]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == u'bus_station'))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Est-ce un arrêt de bus ou une gare routière ?"
            # fixRemove:"amenity"
                err.append({'class': 9014002, 'subclass': 1676203359, 'text': {'en': u'Jungle : Est-ce un arrêt de bus ou une gare routière ?'}, 'fix': {
                    '-': ([
                    u'amenity'])
                }})

        # node[highway=bus_stop][!public_transport]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Préciser s'il s'agit d'un arrêt (platform) ou d'un emplacement sur la route (stop_position)"
            # fixAdd:"public_transport=platform"
                err.append({'class': 9014003, 'subclass': 364316040, 'text': {'en': u'Jungle : Préciser s\'il s\'agit d\'un arrêt (platform) ou d\'un emplacement sur la route (stop_position)'}, 'fix': {
                    '+': dict([
                    [u'public_transport',u'platform']])
                }})

        # node["public_transport"="platform"][!highway][!railway]
        if u'public_transport' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'public_transport') == u'platform' and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Le tag historique est manquant (ajouter le tag highway=bus_stop/railway=tram_stop)"
                err.append({'class': 9014004, 'subclass': 1713888967, 'text': {'en': u'Jungle : Le tag historique est manquant (ajouter le tag highway=bus_stop/railway=tram_stop)'}})

        # node["public_transport"="platform"][bus=yes][!highway]
        if u'public_transport' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'public_transport') == u'platform' and mapcss._tag_capture(capture_tags, 1, tags, u'bus') == u'yes' and not mapcss._tag_capture(capture_tags, 2, tags, u'highway')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Est-ce un arrêt de bus ? (ajouter le tag highway=bus_stop)"
            # fixAdd:"highway=bus_stop"
                err.append({'class': 9014005, 'subclass': 569497609, 'text': {'en': u'Jungle : Est-ce un arrêt de bus ? (ajouter le tag highway=bus_stop)'}, 'fix': {
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
                # throwWarning:"Jungle : Vérifier si la note peut être supprimée"
                err.append({'class': 9014006, 'subclass': 673170504, 'text': {'en': u'Jungle : Vérifier si la note peut être supprimée'}})

        # node[highway=bus_stop][network][inside("FR")]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'network') and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"Jungle : Le réseau devrait être porté par les lignes de transport et non par les arrêts"
            # fixRemove:"network"
                err.append({'class': 9014007, 'subclass': 1428913922, 'text': {'en': u'Jungle : Le réseau devrait être porté par les lignes de transport et non par les arrêts'}, 'fix': {
                    '-': ([
                    u'network'])
                }})

        # node[highway=bus_stop][operator][inside("FR")]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'bus_stop' and mapcss._tag_capture(capture_tags, 1, tags, u'operator') and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"Jungle : L'opérateur devrait être porté par les lignes de transport et non par les arrêts"
            # fixRemove:"operator"
                err.append({'class': 9014008, 'subclass': 210603856, 'text': {'en': u'Jungle : L\'opérateur devrait être porté par les lignes de transport et non par les arrêts'}, 'fix': {
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
                # throwError:"Jungle : Le mode est manquant (ajouter un tag route = bus/coach/tram/etc)"
                err.append({'class': 9014009, 'subclass': 828849115, 'text': {'en': u'Jungle : Le mode est manquant (ajouter un tag route = bus/coach/tram/etc)'}})

        # relation[type=route_master][!route_master][!route]
        if u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route_master' and not mapcss._tag_capture(capture_tags, 1, tags, u'route_master') and not mapcss._tag_capture(capture_tags, 2, tags, u'route')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Le mode est manquant (ajouter un tag route_master = bus/coach/tram/etc)"
                err.append({'class': 9014010, 'subclass': 607011337, 'text': {'en': u'Jungle : Le mode est manquant (ajouter un tag route_master = bus/coach/tram/etc)'}})

        # relation[type=route_master][!route_master][route]
        if u'type' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route_master' and not mapcss._tag_capture(capture_tags, 1, tags, u'route_master') and mapcss._tag_capture(capture_tags, 2, tags, u'route')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Le mode est manquant (transformer le tag route en route_master)"
            # fixChangeKey:"route=>route_master"
                err.append({'class': 9014011, 'subclass': 3385524, 'text': {'en': u'Jungle : Le mode est manquant (transformer le tag route en route_master)'}, 'fix': {
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

        # relation.pt_route[!network]
        # relation.pt_route_master[!network]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'network')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'network')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Le réseau est manquant (ajouter un tag network)"
                err.append({'class': 9014015, 'subclass': 253478598, 'text': {'en': u'Jungle : Le réseau est manquant (ajouter un tag network)'}})

        # relation.pt_route[!operator]
        # relation.pt_route_master[!operator]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'operator')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'operator')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : L'opérateur est manquant (ajouter un tag operator)"
                err.append({'class': 9014016, 'subclass': 1639261067, 'text': {'en': u'Jungle : L\'opérateur est manquant (ajouter un tag operator)'}})

        # relation.pt_route[!ref]
        # relation.pt_route_master[!ref]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'ref')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and not mapcss._tag_capture(capture_tags, 0, tags, u'ref')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Le numéro de ligne est manquant (ajouter un tag ref)"
                err.append({'class': 9014017, 'subclass': 1396643784, 'text': {'en': u'Jungle : Le numéro de ligne est manquant (ajouter un tag ref)'}})

        # relation.pt_route[!from]
        # relation.pt_route[!to]
        if True:
            match = False
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'from')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route and not mapcss._tag_capture(capture_tags, 0, tags, u'to')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : L'origine/destination est manquante (ajouter les tags from/to)"
                err.append({'class': 9014018, 'subclass': 1016437930, 'text': {'en': u'Jungle : L\'origine/destination est manquante (ajouter les tags from/to)'}})

        # relation.pt_route["fixme:relation"="order members"]
        if u'fixme:relation' in keys:
            match = False
            try: match = match or ((set_pt_route and mapcss._tag_capture(capture_tags, 0, tags, u'fixme:relation') == u'order members'))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"Jungle : Les arrêts ne sont peut-être pas dans le bon ordre"
                err.append({'class': 9014012, 'subclass': 1681682692, 'text': {'en': u'Jungle : Les arrêts ne sont peut-être pas dans le bon ordre'}})

        # relation.pt_route["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["operator"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if u'operator' in keys:
            match = False
            try: match = match or ((set_pt_route and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'operator')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Vérifier l'opérateur"
                err.append({'class': 9014013, 'subclass': 286137008, 'text': {'en': u'Jungle : Vérifier l\'opérateur'}})

        # relation.pt_route["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        # relation.pt_route_master["network"=~/STIF|Kéolis|Véolia/][inside("FR")]
        if u'network' in keys:
            match = False
            try: match = match or ((set_pt_route and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'network')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            try: match = match or ((set_pt_route_master and mapcss.regexp_test_(self.re_25554804, mapcss._tag_capture(capture_tags, 0, tags, u'network')) and mapcss.inside(self.father.config.options, u'FR')))
            except mapcss.RuleAbort: pass
            if match:
                # throwError:"Jungle : Vérifier le réseau"
                err.append({'class': 9014014, 'subclass': 735027962, 'text': {'en': u'Jungle : Vérifier le réseau'}})

        # relation.pt_route!.route_ok
        # Use undeclared class route_ok, pt_route

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_transport(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


