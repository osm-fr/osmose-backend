#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_relation(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9007001] = {'item': 9007, 'level': 3, 'tag': ["tag", "relation"], 'desc': mapcss.tr(u'missing tag')}
        self.errors[9007002] = {'item': 9007, 'level': 2, 'tag': ["tag", "relation"], 'desc': mapcss.tr(u'relation without type')}

        self.re_67b11051 = re.compile(ur'^restriction')


    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[!type]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'type'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("relation without type")
                # assertMatch:"relation name=Foo"
                # assertNoMatch:"relation type=route name=Foo"
                err.append({'class': 9007002, 'subclass': 1457279320, 'text': mapcss.tr(u'relation without type')})

        # relation[type=route][!route]
        # relation[type=route_master][!route_master]
        # relation[type=restriction][!/^restriction/]
        # relation[type=boundary][!boundary]
        # relation[type=public_transport][!public_transport]
        # relation[type=waterway][!waterway]
        # relation[type=enforcement][!enforcement]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route') and not mapcss._tag_capture(capture_tags, 1, tags, u'route'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route_master') and not mapcss._tag_capture(capture_tags, 1, tags, u'route_master'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'restriction') and not mapcss._tag_capture(capture_tags, 1, tags, self.re_67b11051))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'boundary') and not mapcss._tag_capture(capture_tags, 1, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'public_transport') and not mapcss._tag_capture(capture_tags, 1, tags, u'public_transport'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'waterway') and not mapcss._tag_capture(capture_tags, 1, tags, u'waterway'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'enforcement') and not mapcss._tag_capture(capture_tags, 1, tags, u'enforcement'))
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
                # assertNoMatch:"relation type=restriction restriction=no_left_turn"
                # assertMatch:"relation type=restriction"
                # assertNoMatch:"relation type=route route=train"
                # assertMatch:"relation type=route"
                # assertNoMatch:"relation type=route_master route_master=train"
                # assertMatch:"relation type=route_master"
                # assertNoMatch:"relation type=site site=administrative"
                # assertNoMatch:"relation type=waterway waterway=river"
                # assertMatch:"relation type=waterway"
                err.append({'class': 9007001, 'subclass': 881372982, 'text': mapcss.tr(u'{0} relation without {0} tag', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

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

        self.check_err(n.relation(data, {u'name': u'Foo'}, []), expected={'class': 9007002, 'subclass': 1457279320})
        self.check_not_err(n.relation(data, {u'name': u'Foo', u'type': u'route'}, []), expected={'class': 9007002, 'subclass': 1457279320})
        self.check_not_err(n.relation(data, {u'boundary': u'administrative', u'type': u'boundary'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_err(n.relation(data, {u'type': u'boundary'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_not_err(n.relation(data, {u'enforcement': u'maxspeed', u'type': u'enforcement'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_err(n.relation(data, {u'type': u'enforcement'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_not_err(n.relation(data, {u'public_transport': u'stop_area', u'type': u'public_transport'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_err(n.relation(data, {u'type': u'public_transport'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_not_err(n.relation(data, {u'restriction': u'no_left_turn', u'type': u'restriction'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_err(n.relation(data, {u'type': u'restriction'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_not_err(n.relation(data, {u'route': u'train', u'type': u'route'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_err(n.relation(data, {u'type': u'route'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_not_err(n.relation(data, {u'route_master': u'train', u'type': u'route_master'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_err(n.relation(data, {u'type': u'route_master'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_not_err(n.relation(data, {u'site': u'administrative', u'type': u'site'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_not_err(n.relation(data, {u'type': u'waterway', u'waterway': u'river'}, []), expected={'class': 9007001, 'subclass': 881372982})
        self.check_err(n.relation(data, {u'type': u'waterway'}, []), expected={'class': 9007001, 'subclass': 881372982})
