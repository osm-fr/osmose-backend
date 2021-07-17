#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_SuspiciousSwimming_Pool(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/wiki/Rules/SuspiciousSwimming_Pool'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[30801] = self.def_class(item = 3080, level = 3, tags = ["tag"] + mapcss.list_('tag', 'fix:chair', 'leisure', 'public equipment'), title = mapcss.tr('Suspicious tag association - possible confusion between swimming_pool and sports_centre'))



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
        if ('building' in keys and 'leisure' in keys) or ('contact:phone' in keys and 'leisure' in keys) or ('contact:url' in keys and 'leisure' in keys) or ('contact:website' in keys and 'leisure' in keys) or ('leisure' in keys and 'name' in keys) or ('leisure' in keys and 'phone' in keys) or ('leisure' in keys and 'url' in keys) or ('leisure' in keys and 'website' in keys) or ('leisure' in keys and 'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'website')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'url')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:website')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:url')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Suspicious tag association - possible confusion between swimming_pool and sports_centre")
                # -osmoseTags:list("tag","fix:chair","leisure","public equipment")
                # -osmoseItemClassLevel:"3080/30801/3"
                # throwWarning:tr("If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.")
                # assertMatch:"node leisure=swimming_pool building=yes"
                err.append({'class': 30801, 'subclass': 0, 'text': mapcss.tr('If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.')})

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
        if ('building' in keys and 'leisure' in keys) or ('contact:phone' in keys and 'leisure' in keys) or ('contact:url' in keys and 'leisure' in keys) or ('contact:website' in keys and 'leisure' in keys) or ('leisure' in keys and 'phone' in keys) or ('leisure' in keys and 'url' in keys) or ('leisure' in keys and 'website' in keys) or ('leisure' in keys and 'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'website')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'url')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:website')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:url')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Suspicious tag association - possible confusion between swimming_pool and sports_centre")
                # -osmoseTags:list("tag","fix:chair","leisure","public equipment")
                # -osmoseItemClassLevel:"3080/30801/3"
                # throwWarning:tr("If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.")
                # assertMatch:"way leisure=swimming_pool url=A"
                # assertNoMatch:"way leisure=swimming_pool"
                err.append({'class': 30801, 'subclass': 0, 'text': mapcss.tr('If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.')})

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
        if ('building' in keys and 'leisure' in keys) or ('contact:phone' in keys and 'leisure' in keys) or ('contact:url' in keys and 'leisure' in keys) or ('contact:website' in keys and 'leisure' in keys) or ('leisure' in keys and 'phone' in keys) or ('leisure' in keys and 'url' in keys) or ('leisure' in keys and 'website' in keys) or ('leisure' in keys and 'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'building') == mapcss._value_capture(capture_tags, 1, 'yes')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'website')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'url')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:website')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:url')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'leisure') == mapcss._value_capture(capture_tags, 0, 'swimming_pool')) and (mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Suspicious tag association - possible confusion between swimming_pool and sports_centre")
                # -osmoseTags:list("tag","fix:chair","leisure","public equipment")
                # -osmoseItemClassLevel:"3080/30801/3"
                # throwWarning:tr("If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.")
                # assertMatch:"relation leisure=swimming_pool phone=+3334656565"
                err.append({'class': 30801, 'subclass': 0, 'text': mapcss.tr('If this is a facility containing one or more swimming pools it should be tagged leisure=sports_centre + sport=swimming.')})

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

        self.check_err(n.node(data, {'building': 'yes', 'leisure': 'swimming_pool'}), expected={'class': 30801, 'subclass': 0})
        self.check_err(n.way(data, {'leisure': 'swimming_pool', 'url': 'A'}, [0]), expected={'class': 30801, 'subclass': 0})
        self.check_not_err(n.way(data, {'leisure': 'swimming_pool'}, [0]), expected={'class': 30801, 'subclass': 0})
        self.check_err(n.relation(data, {'leisure': 'swimming_pool', 'phone': '+3334656565'}, []), expected={'class': 30801, 'subclass': 0})
