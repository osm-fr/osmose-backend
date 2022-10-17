#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class TagFix_Destination(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[316010] = self.def_class(item = 3160, level = 3, tags = mapcss.list_('tag', 'highway', 'waterway'), title = mapcss.tr('Pipe characters should not be used in destination tag, only in destination:lanes'))

        self.re_262d3d80 = re.compile(r'\|')
        self.re_49b44b3d = re.compile(r'^destination:lanes')
        self.re_53d7e349 = re.compile(r'^destination:')
        self.re_60b51c01 = re.compile(r'^destination:.*:lanes')


    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[highway][destination][destination*="|"]
        # way[highway][/^destination:/][!/^destination:lanes/][!/^destination:.*:lanes/][/^destination:/=~/\|/]
        # way[waterway][destination][destination*="|"]
        # way[waterway][/^destination:/][!/^destination:lanes/][!/^destination:.*:lanes/][/^destination:/=~/\|/]
        if ('destination' in keys and 'highway' in keys) or ('destination' in keys and 'waterway' in keys) or ('highway' in keys) or ('waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'destination')) and (mapcss.string_contains(mapcss._tag_capture(capture_tags, 2, tags, 'destination'), mapcss._value_capture(capture_tags, 2, '|'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_53d7e349)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_49b44b3d)) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_60b51c01)) and (mapcss.regexp_test(self.re_262d3d80, mapcss._match_regex(tags, self.re_53d7e349))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 1, tags, 'destination')) and (mapcss.string_contains(mapcss._tag_capture(capture_tags, 2, tags, 'destination'), mapcss._value_capture(capture_tags, 2, '|'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'waterway')) and (mapcss._tag_capture(capture_tags, 1, tags, self.re_53d7e349)) and (not mapcss._tag_capture(capture_tags, 2, tags, self.re_49b44b3d)) and (not mapcss._tag_capture(capture_tags, 3, tags, self.re_60b51c01)) and (mapcss.regexp_test(self.re_262d3d80, mapcss._match_regex(tags, self.re_53d7e349))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Pipe characters should not be used in destination tag, only in destination:lanes")
                # -osmoseItemClassLevel:"3160/316010:0/3"
                # suggestAlternative:tr("In case of multiple values, use instead a semicolon to separate values")
                # throwError:tr("{0} contains a pipe character","{1.tag}")
                # fixAdd:concat("{1.key}=",replace("{1.value}","|",";"))
                # assertNoMatch:"way highway=primary destination:colour=Red"
                # assertMatch:"way highway=primary destination:colour=Red|Yellow"
                # assertNoMatch:"way highway=primary destination:lanes:backward=A8|Centre|Plage"
                # assertNoMatch:"way highway=primary destination:lanes=A8|Centre|Plage"
                # assertNoMatch:"way highway=primary destination:ref:lanes=A8|A10|A23"
                # assertNoMatch:"way highway=primary destination=A8"
                # assertMatch:"way highway=primary destination=A8|Centre|Plage"
                # assertNoMatch:"way highway=tertiary destination:ref:lanes:backward=B 3|B 3"
                # assertNoMatch:"way highway=tertiary destination:ref:to:lanes=A 7|"
                # assertNoMatch:"way waterway=river destination=East"
                # assertMatch:"way waterway=river destination=East|West"
                err.append({'class': 316010, 'subclass': 0, 'text': mapcss.tr('{0} contains a pipe character', mapcss._tag_uncapture(capture_tags, '{1.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(mapcss._tag_uncapture(capture_tags, '{1.key}='), mapcss.replace(mapcss._tag_uncapture(capture_tags, '{1.value}'), '|', ';'))).split('=', 1)])
                }})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = TagFix_Destination(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.way(data, {'destination:colour': 'Red', 'highway': 'primary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_err(n.way(data, {'destination:colour': 'Red|Yellow', 'highway': 'primary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_not_err(n.way(data, {'destination:lanes:backward': 'A8|Centre|Plage', 'highway': 'primary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_not_err(n.way(data, {'destination:lanes': 'A8|Centre|Plage', 'highway': 'primary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_not_err(n.way(data, {'destination:ref:lanes': 'A8|A10|A23', 'highway': 'primary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_not_err(n.way(data, {'destination': 'A8', 'highway': 'primary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_err(n.way(data, {'destination': 'A8|Centre|Plage', 'highway': 'primary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_not_err(n.way(data, {'destination:ref:lanes:backward': 'B 3|B 3', 'highway': 'tertiary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_not_err(n.way(data, {'destination:ref:to:lanes': 'A 7|', 'highway': 'tertiary'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_not_err(n.way(data, {'destination': 'East', 'waterway': 'river'}, [0]), expected={'class': 316010, 'subclass': 0})
        self.check_err(n.way(data, {'destination': 'East|West', 'waterway': 'river'}, [0]), expected={'class': 316010, 'subclass': 0})
