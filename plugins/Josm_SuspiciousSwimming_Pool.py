#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_SuspiciousSwimming_Pool(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[30811] = {'item': 3081, 'level': 3, 'tag': ["tag"] + mapcss.list_(u'tag', u'fix:chair', u'leisure', u'public equipment'), 'desc': mapcss.tr(u'Suspicious tag association - possible confusion between swimming_pool and sports_centre')}



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[leisure=swimming_pool][name]
        # *[leisure=swimming_pool][building=yes]
        # *[leisure=swimming_pool][website]
        # *[leisure=swimming_pool][url]
        # *[leisure=swimming_pool][contact:website]
        # *[leisure=swimming_pool][contact:url]
        # *[leisure=swimming_pool][phone]
        # *[leisure=swimming_pool][contact:phone]
        # *[leisure=swimming_pool][wikipedia]
        if (u'building' in keys and u'leisure' in keys) or (u'contact:phone' in keys and u'leisure' in keys) or (u'contact:url' in keys and u'leisure' in keys) or (u'contact:website' in keys and u'leisure' in keys) or (u'leisure' in keys and u'name' in keys) or (u'leisure' in keys and u'phone' in keys) or (u'leisure' in keys and u'url' in keys) or (u'leisure' in keys and u'website' in keys) or (u'leisure' in keys and u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'building') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'website'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'url'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:website'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:url'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'phone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Suspicious tag association - possible confusion between swimming_pool and sports_centre")
                # -osmoseTags:list("tag","fix:chair","leisure","public equipment")
                # -osmoseItemClassLevel:"3081/30811/3"
                # throwWarning:tr("If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.")
                # assertMatch:"node leisure=swimming_pool building=yes"
                err.append({'class': 30811, 'subclass': 0, 'text': mapcss.tr(u'If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[leisure=swimming_pool][building=yes]
        # *[leisure=swimming_pool][website]
        # *[leisure=swimming_pool][url]
        # *[leisure=swimming_pool][contact:website]
        # *[leisure=swimming_pool][contact:url]
        # *[leisure=swimming_pool][phone]
        # *[leisure=swimming_pool][contact:phone]
        # *[leisure=swimming_pool][wikipedia]
        if (u'building' in keys and u'leisure' in keys) or (u'contact:phone' in keys and u'leisure' in keys) or (u'contact:url' in keys and u'leisure' in keys) or (u'contact:website' in keys and u'leisure' in keys) or (u'leisure' in keys and u'phone' in keys) or (u'leisure' in keys and u'url' in keys) or (u'leisure' in keys and u'website' in keys) or (u'leisure' in keys and u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'building') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'website'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'url'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:website'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:url'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'phone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Suspicious tag association - possible confusion between swimming_pool and sports_centre")
                # -osmoseTags:list("tag","fix:chair","leisure","public equipment")
                # -osmoseItemClassLevel:"3081/30811/3"
                # throwWarning:tr("If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.")
                # assertMatch:"way leisure=swimming_pool url=A"
                # assertNoMatch:"way leisure=swimming_pool"
                err.append({'class': 30811, 'subclass': 0, 'text': mapcss.tr(u'If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[leisure=swimming_pool][building=yes]
        # *[leisure=swimming_pool][website]
        # *[leisure=swimming_pool][url]
        # *[leisure=swimming_pool][contact:website]
        # *[leisure=swimming_pool][contact:url]
        # *[leisure=swimming_pool][phone]
        # *[leisure=swimming_pool][contact:phone]
        # *[leisure=swimming_pool][wikipedia]
        if (u'building' in keys and u'leisure' in keys) or (u'contact:phone' in keys and u'leisure' in keys) or (u'contact:url' in keys and u'leisure' in keys) or (u'contact:website' in keys and u'leisure' in keys) or (u'leisure' in keys and u'phone' in keys) or (u'leisure' in keys and u'url' in keys) or (u'leisure' in keys and u'website' in keys) or (u'leisure' in keys and u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'building') == mapcss._value_capture(capture_tags, 1, u'yes'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'website'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'url'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:website'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:url'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'phone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'swimming_pool') and mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Suspicious tag association - possible confusion between swimming_pool and sports_centre")
                # -osmoseTags:list("tag","fix:chair","leisure","public equipment")
                # -osmoseItemClassLevel:"3081/30811/3"
                # throwWarning:tr("If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.")
                # assertMatch:"relation leisure=swimming_pool phone=+3334656565"
                err.append({'class': 30811, 'subclass': 0, 'text': mapcss.tr(u'If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_SuspiciousSwimming_Pool(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'building': u'yes', u'leisure': u'swimming_pool'}), expected={'class': 30811, 'subclass': 0})
        self.check_err(n.way(data, {u'leisure': u'swimming_pool', u'url': u'A'}, [0]), expected={'class': 30811, 'subclass': 0})
        self.check_not_err(n.way(data, {u'leisure': u'swimming_pool'}, [0]), expected={'class': 30811, 'subclass': 0})
        self.check_err(n.relation(data, {u'leisure': u'swimming_pool', u'phone': u'+3334656565'}, []), expected={'class': 30811, 'subclass': 0})
