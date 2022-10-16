#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_relation(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/relation.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9007001] = self.def_class(item = 9007, level = 3, tags = ["tag", "relation"], title = mapcss.tr('missing tag'))
        self.errors[9007002] = self.def_class(item = 9007, level = 2, tags = ["tag", "relation"], title = mapcss.tr('relation without type'))

        self.re_67b11051 = re.compile(r'^restriction')


    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[!type]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((not mapcss._tag_capture(capture_tags, 0, tags, 'type')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("relation without type")
                # assertMatch:"relation name=Foo"
                # assertNoMatch:"relation type=route name=Foo"
                err.append({'class': 9007002, 'subclass': 1457279320, 'text': mapcss.tr('relation without type')})

        # relation[type=boundary][!boundary][!disused:boundary]
        # relation[type=destination_sign][!destination]
        # relation[type=enforcement][!enforcement]
        # relation[type=public_transport][!public_transport]
        # relation[type=route][!route]
        # relation[type=route_master][!route_master]
        # relation[type=waterway][!waterway]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'boundary')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'boundary')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'disused:boundary')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'destination_sign')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'destination')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'enforcement')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'enforcement')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'public_transport')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'public_transport')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'route')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'route')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'route_master')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'route_master')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'waterway')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'waterway')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} relation without {0} tag","{1.key}")
                # assertNoMatch:"relation type=boundary boundary=administrative"
                # assertMatch:"relation type=boundary"
                # assertNoMatch:"relation type=enforcement enforcement=maxspeed"
                # assertMatch:"relation type=enforcement"
                # assertNoMatch:"relation type=public_transport public_transport=stop_area"
                # assertMatch:"relation type=public_transport"
                # assertNoMatch:"relation type=route route=train"
                # assertMatch:"relation type=route"
                # assertNoMatch:"relation type=route_master route_master=train"
                # assertMatch:"relation type=route_master"
                # assertNoMatch:"relation type=site site=administrative"
                # assertNoMatch:"relation type=waterway waterway=river"
                # assertMatch:"relation type=waterway"
                err.append({'class': 9007001, 'subclass': 93004660, 'text': mapcss.tr('{0} relation without {0} tag', mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # relation[type=restriction][!/^restriction/]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'restriction')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_67b11051)))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} relation without {0} tag","restriction")
                # assertNoMatch:"relation type=restriction restriction:hgv=no_left_turn"
                # assertNoMatch:"relation type=restriction restriction=no_left_turn"
                # assertMatch:"relation type=restriction"
                err.append({'class': 9007001, 'subclass': 1097316614, 'text': mapcss.tr('{0} relation without {0} tag', 'restriction')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_relation(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.relation(data, {'name': 'Foo'}, []), expected={'class': 9007002, 'subclass': 1457279320}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.relation(data, {'name': 'Foo', 'type': 'route'}, []), expected={'class': 9007002, 'subclass': 1457279320})
        self.check_not_err(n.relation(data, {'boundary': 'administrative', 'type': 'boundary'}, []), expected={'class': 9007001, 'subclass': 93004660})
        self.check_err(n.relation(data, {'type': 'boundary'}, []), expected={'class': 9007001, 'subclass': 93004660}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.relation(data, {'enforcement': 'maxspeed', 'type': 'enforcement'}, []), expected={'class': 9007001, 'subclass': 93004660})
        self.check_err(n.relation(data, {'type': 'enforcement'}, []), expected={'class': 9007001, 'subclass': 93004660}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.relation(data, {'public_transport': 'stop_area', 'type': 'public_transport'}, []), expected={'class': 9007001, 'subclass': 93004660})
        self.check_err(n.relation(data, {'type': 'public_transport'}, []), expected={'class': 9007001, 'subclass': 93004660}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.relation(data, {'route': 'train', 'type': 'route'}, []), expected={'class': 9007001, 'subclass': 93004660})
        self.check_err(n.relation(data, {'type': 'route'}, []), expected={'class': 9007001, 'subclass': 93004660}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.relation(data, {'route_master': 'train', 'type': 'route_master'}, []), expected={'class': 9007001, 'subclass': 93004660})
        self.check_err(n.relation(data, {'type': 'route_master'}, []), expected={'class': 9007001, 'subclass': 93004660}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.relation(data, {'site': 'administrative', 'type': 'site'}, []), expected={'class': 9007001, 'subclass': 93004660})
        self.check_not_err(n.relation(data, {'type': 'waterway', 'waterway': 'river'}, []), expected={'class': 9007001, 'subclass': 93004660})
        self.check_err(n.relation(data, {'type': 'waterway'}, []), expected={'class': 9007001, 'subclass': 93004660}, disallowed_str_in_text = ['{', '}'])
        self.check_not_err(n.relation(data, {'restriction:hgv': 'no_left_turn', 'type': 'restriction'}, []), expected={'class': 9007001, 'subclass': 1097316614})
        self.check_not_err(n.relation(data, {'restriction': 'no_left_turn', 'type': 'restriction'}, []), expected={'class': 9007001, 'subclass': 1097316614})
        self.check_err(n.relation(data, {'type': 'restriction'}, []), expected={'class': 9007001, 'subclass': 1097316614}, disallowed_str_in_text = ['{', '}'])
