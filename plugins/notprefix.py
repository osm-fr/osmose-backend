#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class notprefix(PluginMapCSS):
    # ------------------------------- IMPORTANT -------------------------------
    # This file is generated automatically and should not be modified directly.
    # Instead, modify the source mapcss file and regenerate this Python script.
    # -------------------------------------------------------------------------



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[40302] = self.def_class(item = 4030, level = 2, tags = [], title = mapcss.tr('`{0}` together with `{1}` and equal values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[not:name][name]["not:name"=*"name"]
        # *[not:addr:postcode][addr:postcode]["not:addr:postcode"=*"addr:postcode"]
        # *[not:network][network]["not:network"=*"network"]
        # *[not:designation][designation]["not:designation"=*"designation"]
        # *[not:brand:wikidata][brand:wikidata]["not:brand:wikidata"=*"brand:wikidata"]
        # *[not:network:wikidata][network:wikidata]["not:network:wikidata"=*"network:wikidata"]
        # *[not:operator:wikidata][operator:wikidata]["not:operator:wikidata"=*"operator:wikidata"]
        # *[not:highway][highway]["not:highway"=*"highway"]
        if ('addr:postcode' in keys and 'not:addr:postcode' in keys) or ('brand:wikidata' in keys and 'not:brand:wikidata' in keys) or ('designation' in keys and 'not:designation' in keys) or ('highway' in keys and 'not:highway' in keys) or ('name' in keys and 'not:name' in keys) or ('network' in keys and 'not:network' in keys) or ('network:wikidata' in keys and 'not:network:wikidata' in keys) or ('not:operator:wikidata' in keys and 'operator:wikidata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:name') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:addr:postcode')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:addr:postcode') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:network')) and (mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:network') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'network'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:designation')) and (mapcss._tag_capture(capture_tags, 1, tags, 'designation')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:designation') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'designation'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:brand:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'brand:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:brand:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'brand:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:network:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'network:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:network:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'network:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:operator:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'operator:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:operator:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'operator:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:highway') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4030/40302/2"
                # throwWarning:tr("`{0}` together with `{1}` and equal values","{0.key}","{1.key}")
                err.append({'class': 40302, 'subclass': 0, 'text': mapcss.tr('`{0}` together with `{1}` and equal values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[not:name][name]["not:name"=*"name"]
        # *[not:addr:postcode][addr:postcode]["not:addr:postcode"=*"addr:postcode"]
        # *[not:network][network]["not:network"=*"network"]
        # *[not:designation][designation]["not:designation"=*"designation"]
        # *[not:brand:wikidata][brand:wikidata]["not:brand:wikidata"=*"brand:wikidata"]
        # *[not:network:wikidata][network:wikidata]["not:network:wikidata"=*"network:wikidata"]
        # *[not:operator:wikidata][operator:wikidata]["not:operator:wikidata"=*"operator:wikidata"]
        # *[not:highway][highway]["not:highway"=*"highway"]
        if ('addr:postcode' in keys and 'not:addr:postcode' in keys) or ('brand:wikidata' in keys and 'not:brand:wikidata' in keys) or ('designation' in keys and 'not:designation' in keys) or ('highway' in keys and 'not:highway' in keys) or ('name' in keys and 'not:name' in keys) or ('network' in keys and 'not:network' in keys) or ('network:wikidata' in keys and 'not:network:wikidata' in keys) or ('not:operator:wikidata' in keys and 'operator:wikidata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:name') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:addr:postcode')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:addr:postcode') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:network')) and (mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:network') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'network'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:designation')) and (mapcss._tag_capture(capture_tags, 1, tags, 'designation')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:designation') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'designation'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:brand:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'brand:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:brand:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'brand:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:network:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'network:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:network:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'network:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:operator:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'operator:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:operator:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'operator:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:highway') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4030/40302/2"
                # throwWarning:tr("`{0}` together with `{1}` and equal values","{0.key}","{1.key}")
                # assertMatch:"way name=Osmoseroad not:name=Osmoseroad"
                # assertNoMatch:"way name=Osmosestreet not:name=Osmoseroad"
                err.append({'class': 40302, 'subclass': 0, 'text': mapcss.tr('`{0}` together with `{1}` and equal values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[not:name][name]["not:name"=*"name"]
        # *[not:addr:postcode][addr:postcode]["not:addr:postcode"=*"addr:postcode"]
        # *[not:network][network]["not:network"=*"network"]
        # *[not:designation][designation]["not:designation"=*"designation"]
        # *[not:brand:wikidata][brand:wikidata]["not:brand:wikidata"=*"brand:wikidata"]
        # *[not:network:wikidata][network:wikidata]["not:network:wikidata"=*"network:wikidata"]
        # *[not:operator:wikidata][operator:wikidata]["not:operator:wikidata"=*"operator:wikidata"]
        # *[not:highway][highway]["not:highway"=*"highway"]
        if ('addr:postcode' in keys and 'not:addr:postcode' in keys) or ('brand:wikidata' in keys and 'not:brand:wikidata' in keys) or ('designation' in keys and 'not:designation' in keys) or ('highway' in keys and 'not:highway' in keys) or ('name' in keys and 'not:name' in keys) or ('network' in keys and 'not:network' in keys) or ('network:wikidata' in keys and 'not:network:wikidata' in keys) or ('not:operator:wikidata' in keys and 'operator:wikidata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:name')) and (mapcss._tag_capture(capture_tags, 1, tags, 'name')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:name') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'name'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:addr:postcode')) and (mapcss._tag_capture(capture_tags, 1, tags, 'addr:postcode')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:addr:postcode') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'addr:postcode'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:network')) and (mapcss._tag_capture(capture_tags, 1, tags, 'network')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:network') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'network'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:designation')) and (mapcss._tag_capture(capture_tags, 1, tags, 'designation')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:designation') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'designation'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:brand:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'brand:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:brand:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'brand:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:network:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'network:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:network:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'network:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:operator:wikidata')) and (mapcss._tag_capture(capture_tags, 1, tags, 'operator:wikidata')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:operator:wikidata') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'operator:wikidata'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'not:highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 2, tags, 'not:highway') == mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'highway'))))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"4030/40302/2"
                # throwWarning:tr("`{0}` together with `{1}` and equal values","{0.key}","{1.key}")
                err.append({'class': 40302, 'subclass': 0, 'text': mapcss.tr('`{0}` together with `{1}` and equal values', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = notprefix(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {'name': 'Osmoseroad', 'not:name': 'Osmoseroad'}, [0]), expected={'class': 40302, 'subclass': 0})
        self.check_not_err(n.way(data, {'name': 'Osmosestreet', 'not:name': 'Osmoseroad'}, [0]), expected={'class': 40302, 'subclass': 0})
