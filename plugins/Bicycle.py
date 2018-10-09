#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Bicycle(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[20301] = {'item': 2030, 'level': 1, 'tag': mapcss.list_(u'tag', u'highway', u'cycleway', u'fix:survey'), 'desc': mapcss.tr(u'Opposite cycleway without oneway', capture_tags)}
        self.errors[20302] = {'item': 2030, 'level': 1, 'tag': mapcss.list_(u'tag', u'highway', u'cycleway', u'fix:survey'), 'desc': mapcss.tr(u'Opposite or opposite lane in the same way of the oneway', capture_tags)}
        self.errors[20805] = {'item': 2080, 'level': 3, 'tag': mapcss.list_(u'tag', u'highway', u'footway'), 'desc': mapcss.tr(u'{0} without {1}', capture_tags, u'{0.tag}', u'{1.tag}')}
        self.errors[30328] = {'item': 3032, 'level': 2, 'tag': mapcss.list_(u'tag', u'highway', u'cycleway'), 'desc': mapcss.tr(u'{0} with {1}', capture_tags, u'{0.tag}', u'{1.tag}')}
        self.errors[30329] = {'item': 3032, 'level': 3, 'tag': mapcss.list_(u'tag', u'highway', u'fix:survey'), 'desc': mapcss.tr(u'{0} doesn\'t match with {1}', capture_tags, u'{0.tag}', u'{1.tag}')}
        self.errors[40101] = {'item': 4010, 'level': 2, 'tag': mapcss.list_(u'tag', u'highway'), 'desc': mapcss.tr(u'{0} is preferred to {1}', capture_tags, u'{2.tag}', u'{1.tag}')}
        self.errors[40301] = {'item': 4030, 'level': 2, 'tag': mapcss.list_(u'tag', u'highway', u'cycleway'), 'desc': mapcss.tr(u'{0} with {1} and {2}', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')}

        self.re_67b51e41 = re.compile(ur'opposite|opposite_lane')


    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[cycleway][cycleway:right][cycleway:left]
        if u'cycleway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:right') and mapcss._tag_capture(capture_tags, 2, tags, u'cycleway:left')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway","cycleway")
                # osmoseItemClassLevel:"4030/40301/2"
                # throwWarning:tr("{0} with {1} and {2}","{0.key}","{1.key}","{2.key}")
                # assertMatch:"way cycleway=a cycleway:right=b cycleway:left=c"
                err.append({'class': 40301, 'subclass': 0, 'text': mapcss.tr(u'{0} with {1} and {2}', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')})

        # way[footway=sidewalk][highway!=footway]
        if u'footway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'footway') == mapcss._value_capture(capture_tags, 0, u'sidewalk') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') != mapcss._value_capture(capture_tags, 1, u'footway')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway","footway")
                # osmoseItemClassLevel:"2080/20805/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.tag}")
                # assertNoMatch:"way footway=sidewalk highway=footway"
                # assertMatch:"way footway=sidewalk highway=path"
                err.append({'class': 20805, 'subclass': 0, 'text': mapcss.tr(u'{0} without {1}', capture_tags, u'{0.tag}', u'{1.tag}')})

        # way[highway=service][service=psv][psv!=yes]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'service') and mapcss._tag_capture(capture_tags, 1, tags, u'service') == mapcss._value_capture(capture_tags, 1, u'psv') and mapcss._tag_capture(capture_tags, 2, tags, u'psv') != mapcss._value_capture(capture_tags, 2, u'yes')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway")
                # osmoseItemClassLevel:"4010/40101/2"
                # throwWarning:tr("{0} is preferred to {1}","{2.tag}","{1.tag}")
                # fixAdd:"psv=yes"
                # fixRemove:"service"
                # assertMatch:"way highway=service service=psv psv=no"
                # assertNoMatch:"way highway=service service=psv psv=yes"
                err.append({'class': 40101, 'subclass': 0, 'text': mapcss.tr(u'{0} is preferred to {1}', capture_tags, u'{2.tag}', u'{1.tag}'), 'fix': {
                    '+': dict([
                    [u'psv',u'yes']]),
                    '-': ([
                    u'service'])
                }})

        # way[highway=cycleway][cycleway=track]
        if u'highway' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway') == mapcss._value_capture(capture_tags, 1, u'track')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway","cycleway")
                # osmoseItemClassLevel:"3032/30328/2"
                # throwWarning:tr("{0} with {1}","{0.tag}","{1.tag}")
                # fixRemove:"cycleway"
                err.append({'class': 30328, 'subclass': 0, 'text': mapcss.tr(u'{0} with {1}', capture_tags, u'{0.tag}', u'{1.tag}'), 'fix': {
                    '-': ([
                    u'cycleway'])
                }})

        # way[tracktype>=2][surface=asphalt]
        if u'tracktype' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'tracktype') >= mapcss._value_capture(capture_tags, 0, 2) and mapcss._tag_capture(capture_tags, 1, tags, u'surface') == mapcss._value_capture(capture_tags, 1, u'asphalt')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway","fix:survey")
                # osmoseItemClassLevel:"3032/30329/3"
                # throwWarning:tr("{0} doesn't match with {1}","{0.tag}","{1.tag}")
                # assertMatch:"way tracktype=3 surface=asphalt"
                err.append({'class': 30329, 'subclass': 0, 'text': mapcss.tr(u'{0} doesn\'t match with {1}', capture_tags, u'{0.tag}', u'{1.tag}')})

        # way[cycleway=~/opposite|opposite_lane/][!oneway]
        # way[cycleway=~/opposite|opposite_lane/][oneway=no]
        if u'cycleway' in keys:
            match = False
            try: match = match or ((mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway')) and not mapcss._tag_capture(capture_tags, 1, tags, u'oneway')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'no')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway","cycleway","fix:survey")
                # osmoseItemClassLevel:"2030/20301/1"
                # throwError:tr("Opposite cycleway without oneway")
                # assertNoMatch:"way cycleway=lane oneway=yes"
                # assertNoMatch:"way cycleway=opposite oneway=yes"
                # assertMatch:"way cycleway=opposite"
                err.append({'class': 20301, 'subclass': 0, 'text': mapcss.tr(u'Opposite cycleway without oneway', capture_tags)})

        # way["cycleway:right"=~/opposite|opposite_lane/][oneway=yes]
        # way["cycleway:left"=~/opposite|opposite_lane/][oneway="-1"]
        if u'cycleway:left' in keys or u'cycleway:right' in keys:
            match = False
            try: match = match or ((mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway:right')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'yes')))
            except mapcss.RuleAbort: pass
            try: match = match or ((mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_67b51e41), mapcss._tag_capture(capture_tags, 0, tags, u'cycleway:left')) and mapcss._tag_capture(capture_tags, 1, tags, u'oneway') == mapcss._value_capture(capture_tags, 1, u'-1')))
            except mapcss.RuleAbort: pass
            if match:
                # osmoseTags:list("tag","highway","cycleway","fix:survey")
                # osmoseItemClassLevel:"2030/20302/1"
                # throwError:tr("Opposite or opposite lane in the same way of the oneway")
                # assertMatch:"way cycleway:right=opposite oneway=yes"
                # assertNoMatch:"way cycleway=opposite oneway=yes"
                err.append({'class': 20302, 'subclass': 0, 'text': mapcss.tr(u'Opposite or opposite lane in the same way of the oneway', capture_tags)})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Bicycle(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {u'cycleway': u'a', u'cycleway:left': u'c', u'cycleway:right': u'b'}), expected={'class': 40301, 'subclass': 0})
        self.check_not_err(n.way(data, {u'footway': u'sidewalk', u'highway': u'footway'}), expected={'class': 20805, 'subclass': 0})
        self.check_err(n.way(data, {u'footway': u'sidewalk', u'highway': u'path'}), expected={'class': 20805, 'subclass': 0})
        self.check_err(n.way(data, {u'highway': u'service', u'psv': u'no', u'service': u'psv'}), expected={'class': 40101, 'subclass': 0})
        self.check_not_err(n.way(data, {u'highway': u'service', u'psv': u'yes', u'service': u'psv'}), expected={'class': 40101, 'subclass': 0})
        self.check_err(n.way(data, {u'surface': u'asphalt', u'tracktype': u'3'}), expected={'class': 30329, 'subclass': 0})
        self.check_not_err(n.way(data, {u'cycleway': u'lane', u'oneway': u'yes'}), expected={'class': 20301, 'subclass': 0})
        self.check_not_err(n.way(data, {u'cycleway': u'opposite', u'oneway': u'yes'}), expected={'class': 20301, 'subclass': 0})
        self.check_err(n.way(data, {u'cycleway': u'opposite'}), expected={'class': 20301, 'subclass': 0})
        self.check_err(n.way(data, {u'cycleway:right': u'opposite', u'oneway': u'yes'}), expected={'class': 20302, 'subclass': 0})
        self.check_not_err(n.way(data, {u'cycleway': u'opposite', u'oneway': u'yes'}), expected={'class': 20302, 'subclass': 0})
