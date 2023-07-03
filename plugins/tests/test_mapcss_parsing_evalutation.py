#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class test_mapcss_parsing_evalutation(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[1] = self.def_class(item = 0, level = 3, tags = [], title = {'en': 'test #1740'})
        self.errors[2] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test #994 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[3] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test #328 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}')))
        self.errors[4] = self.def_class(item = 0, level = 3, tags = [], title = {'en': 'test commit 373d1ff9bacf8126508bbf3e37467df2bdf17fbd'})
        self.errors[5] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test #327'))
        self.errors[6] = self.def_class(item = 0, level = 2, tags = [], title = {'en': 'test'})
        self.errors[7] = self.def_class(item = 0, level = 2, tags = [], title = mapcss.tr('test #1882 - {0}-{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[8] = self.def_class(item = 0, level = 2, tags = [], title = mapcss.tr('test #1882 - {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[9] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[10] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test closed rewrite {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[11] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test any {0} {1}', mapcss.any_(mapcss.tag(tags, 'b'), ''), mapcss.any_(mapcss.tag(tags, 'c'), mapcss.tag(tags, 'd'), '')))
        self.errors[12] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test concat {0}', mapcss.concat(mapcss.tag(tags, 'b'), mapcss.tag(tags, 'c'))))
        self.errors[13] = self.def_class(item = 0, level = 3, tags = [], title = {'en': 'test #1610'})
        self.errors[14] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test #1603 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[15] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test righthandtraffic'))
        self.errors[16] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test lefthandtraffic'))
        self.errors[17] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[18] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test #1303, #1742 {0}', mapcss._tag_uncapture(capture_tags, '{2.key}')))
        self.errors[19] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test #1303 {0}', mapcss._tag_uncapture(capture_tags, '{2.key}')))
        self.errors[20] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test #1742 - {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}')))
        self.errors[21] = self.def_class(item = 0, level = 3, tags = [], title = mapcss.tr('test {0}{1}', 'text', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[97] = self.def_class(item = 4, level = 1, tags = mapcss.list_('osmose_rules'), title = mapcss.tr('test'), trap = mapcss.tr('Don\'t do this!'), detail = mapcss.tr('More {0}.', '`info`'), example = {"en": 'Look at me, I haven\'t lost my apostrophe'}, fix = {"en": 'This may fix it.'}, resource = 'https://wiki.openstreetmap.org/wiki/Useful_Page')
        self.errors[98] = self.def_class(item = 4030, level = 2, tags = mapcss.list_('fix:survey'), title = {'en': 'test #1740'})
        self.errors[99] = self.def_class(item = 4, level = 1, tags = mapcss.list_('osmose_rules'), title = mapcss.tr('test'), trap = mapcss.tr('Don\'t do this!'), detail = mapcss.tr('More {0}.', '`info`'), example = {"en": 'Look at me, I haven\'t lost my apostrophe'}, fix = {"en": 'This may fix it.'}, resource = 'https://wiki.openstreetmap.org/wiki/Useful_Page')

        self.re_3d3faeb5 = re.compile(r'(?i).*Straße.*')
        self.re_49048f80 = re.compile(r'd')
        self.re_4961c1fa = re.compile(r'abc')
        self.re_75974701 = re.compile(r'^(parking|motorcycle_parking)$')
        self.re_7f42aaa6 = re.compile(r'def')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_a = set_b = False

        # node[x=0]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x') == mapcss._value_capture(capture_tags, 0, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:survey")
                # -osmoseItemClassLevel:"4030/98:0/2"
                # throwWarning:"test #1740"
                # assertMatch:"node x=0"
                # assertNoMatch:"node x=1"
                # assertNoMatch:"node x=1.0"
                # assertNoMatch:"node x=Osmose"
                err.append({'class': 98, 'subclass': 0, 'text': {'en': 'test #1740'}})

        # node[x!=0]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x') != mapcss._value_capture(capture_tags, 0, 0)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test #1740"
                # assertNoMatch:"node x=0"
                # assertMatch:"node x=1"
                # assertMatch:"node x=1.0"
                # assertMatch:"node x=Osmose"
                err.append({'class': 1, 'subclass': 659546685, 'text': {'en': 'test #1740'}})

        # *[parking][amenity!~/^(parking|motorcycle_parking)$/]
        if ('parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_75974701, '^(parking|motorcycle_parking)$'), mapcss._tag_capture(capture_tags, 1, tags, 'amenity'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #994 - {0}{1}","{0.key}","{1.tag}")
                # assertMatch:"node parking=yes amenity=osmose"
                # assertNoMatch:"node parking=yes amenity=parking"
                err.append({'class': 2, 'subclass': 650362898, 'text': mapcss.tr('test #994 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[a][!c]
        # *[b][!/d/]
        if ('a' in keys) or ('b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'c')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'b')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49048f80)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #328 - {0}{1}","{0.key}","{1.key}")
                err.append({'class': 3, 'subclass': 1004069731, 'text': mapcss.tr('test #328 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[/abc/=~/def/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(self.re_7f42aaa6, mapcss._match_regex(tags, self.re_4961c1fa))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test commit 373d1ff9bacf8126508bbf3e37467df2bdf17fbd"
                err.append({'class': 4, 'subclass': 1371556921, 'text': {'en': 'test commit 373d1ff9bacf8126508bbf3e37467df2bdf17fbd'}})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        if ('addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #327")
                # -osmoseAssertNoMatchWithContext:list("node addr:street=Neuestraßebahn","inside=FR")
                # -osmoseAssertMatchWithContext:list("node addr:street=Neuestraßebahn","inside=LI")
                err.append({'class': 5, 'subclass': 43561107, 'text': mapcss.tr('test #327')})

        # *[a][a=*b]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'a') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'b'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"test"
                # assertMatch:"node a=x b=x"
                # assertNoMatch:"node a=x b=y"
                # assertNoMatch:"node a=x"
                err.append({'class': 6, 'subclass': 1343056298, 'text': {'en': 'test'}})

        # node[lit][eval(number_of_tags())=1]
        if ('lit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lit')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test"
                # assertNoMatch:"node abc=def lit=yes"
                # assertMatch:"node lit=yes"
                err.append({'class': 6, 'subclass': 130427469, 'text': {'en': 'test'}})

        # node[lit][number_of_tags()==1]
        if ('lit' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'lit')) and (len(tags) == 1))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test"
                # assertNoMatch:"node abc=def lit=yes"
                # assertMatch:"node lit=yes"
                err.append({'class': 6, 'subclass': 612979508, 'text': {'en': 'test'}})

        # node[a][b][tag("a")>tag("b")]
        if ('a' in keys and 'b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'b')) and (mapcss.tag(tags, 'a') > mapcss.tag(tags, 'b')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}-{1}","{0.tag}","{1.tag}")
                # assertNoMatch:"node a=3  b=6"
                # assertNoMatch:"node a=3  b=6a"
                # assertNoMatch:"node a=3.0  b=6a"
                # assertNoMatch:"node a=3a b=6"
                # assertNoMatch:"node a=3a b=6a"
                # assertNoMatch:"node a=X  b=Y"
                # assertMatch:"node b=-5 a=6"
                # assertMatch:"node b=3  a=12"
                # assertMatch:"node b=3  a=12.0"
                # assertMatch:"node b=3  a=6"
                # assertNoMatch:"node b=3  a=6a"
                # assertMatch:"node b=3.0  a=12"
                # assertMatch:"node b=3.0  a=6.0"
                # assertNoMatch:"node b=3a a=6"
                # assertNoMatch:"node b=3a a=6a"
                # assertNoMatch:"node b=X  a=Y"
                err.append({'class': 7, 'subclass': 766520351, 'text': mapcss.tr('test #1882 - {0}-{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[a][b][tag("a")>=tag("b")]
        if ('a' in keys and 'b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'b')) and (mapcss.tag(tags, 'a') >= mapcss.tag(tags, 'b')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}-{1}","{0.tag}","{1.tag}")
                # assertNoMatch:"node a=3  b=6"
                # assertNoMatch:"node a=3  b=6a"
                # assertNoMatch:"node a=3.0  b=6a"
                # assertNoMatch:"node a=3a b=6"
                # assertNoMatch:"node a=3a b=6a"
                # assertNoMatch:"node a=X  b=Y"
                # assertMatch:"node b=-5 a=6"
                # assertMatch:"node b=3  a=12"
                # assertMatch:"node b=3  a=12.0"
                # assertMatch:"node b=3  a=6"
                # assertNoMatch:"node b=3  a=6a"
                # assertMatch:"node b=3.0  a=12"
                # assertMatch:"node b=3.0  a=6.0"
                # assertNoMatch:"node b=3a a=6"
                # assertNoMatch:"node b=3a a=6a"
                # assertNoMatch:"node b=X  a=Y"
                err.append({'class': 7, 'subclass': 1296744085, 'text': mapcss.tr('test #1882 - {0}-{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[a][b][tag("b")<tag("a")]
        if ('a' in keys and 'b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'b')) and (mapcss.tag(tags, 'b') < mapcss.tag(tags, 'a')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}-{1}","{0.tag}","{1.tag}")
                # assertNoMatch:"node a=3  b=6"
                # assertNoMatch:"node a=3  b=6a"
                # assertNoMatch:"node a=3.0  b=6a"
                # assertNoMatch:"node a=3a b=6"
                # assertNoMatch:"node a=3a b=6a"
                # assertNoMatch:"node a=X  b=Y"
                # assertMatch:"node b=-5 a=6"
                # assertMatch:"node b=3  a=12"
                # assertMatch:"node b=3  a=12.0"
                # assertMatch:"node b=3  a=6"
                # assertNoMatch:"node b=3  a=6a"
                # assertMatch:"node b=3.0  a=12"
                # assertMatch:"node b=3.0  a=6.0"
                # assertNoMatch:"node b=3a a=6"
                # assertNoMatch:"node b=3a a=6a"
                # assertNoMatch:"node b=X  a=Y"
                err.append({'class': 7, 'subclass': 660577118, 'text': mapcss.tr('test #1882 - {0}-{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[a][b][tag("b")<=tag("a")]
        if ('a' in keys and 'b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'b')) and (mapcss.tag(tags, 'b') <= mapcss.tag(tags, 'a')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}-{1}","{0.tag}","{1.tag}")
                # assertNoMatch:"node a=3  b=6"
                # assertNoMatch:"node a=3  b=6a"
                # assertNoMatch:"node a=3.0  b=6a"
                # assertNoMatch:"node a=3a b=6"
                # assertNoMatch:"node a=3a b=6a"
                # assertNoMatch:"node a=X  b=Y"
                # assertMatch:"node b=-5 a=6"
                # assertMatch:"node b=3  a=12"
                # assertMatch:"node b=3  a=12.0"
                # assertMatch:"node b=3  a=6"
                # assertNoMatch:"node b=3  a=6a"
                # assertMatch:"node b=3.0  a=12"
                # assertMatch:"node b=3.0  a=6.0"
                # assertNoMatch:"node b=3a a=6"
                # assertNoMatch:"node b=3a a=6a"
                # assertNoMatch:"node b=X  a=Y"
                err.append({'class': 7, 'subclass': 1302849761, 'text': mapcss.tr('test #1882 - {0}-{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[a>2]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a') > mapcss._value_capture(capture_tags, 0, 2)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}","{0.tag}")
                # assertNoMatch:"node a=-5"
                # assertNoMatch:"node a=1"
                # assertNoMatch:"node a=1.0"
                # assertMatch:"node a=3"
                # assertMatch:"node a=3.0"
                # assertNoMatch:"node a=X"
                err.append({'class': 8, 'subclass': 1910232765, 'text': mapcss.tr('test #1882 - {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[a>2.0]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a') > mapcss._value_capture(capture_tags, 0, 2.0)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}","{0.tag}")
                # assertNoMatch:"node a=-5"
                # assertNoMatch:"node a=1"
                # assertNoMatch:"node a=1.0"
                # assertMatch:"node a=3"
                # assertMatch:"node a=3.0"
                # assertNoMatch:"node a=X"
                err.append({'class': 8, 'subclass': 1369591651, 'text': mapcss.tr('test #1882 - {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[a][count(split("n",tag("a")))>2]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss.count(mapcss.split('n', mapcss.tag(tags, 'a'))) > 2))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}","{0.tag}")
                # assertNoMatch:"node a=X"
                # assertMatch:"node a=ananas"
                err.append({'class': 8, 'subclass': 130115842, 'text': mapcss.tr('test #1882 - {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[a][count(split("n",tag("a")))>2.0]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss.count(mapcss.split('n', mapcss.tag(tags, 'a'))) > 2.0))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}","{0.tag}")
                # assertNoMatch:"node a=X"
                # assertMatch:"node a=ananas"
                err.append({'class': 8, 'subclass': 935120167, 'text': mapcss.tr('test #1882 - {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[a][b][count(split("n",tag("a")))>tag(b)]
        if ('a' in keys and 'b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'b')) and (mapcss.count(mapcss.split('n', mapcss.tag(tags, 'a'))) > mapcss.tag(tags, 'b')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("test #1882 - {0}-{1}","{0.tag}","{1.tag}")
                # assertNoMatch:"node a=X b=2"
                # assertNoMatch:"node a=X b=2.0"
                # assertMatch:"node a=ananas b=2"
                # assertMatch:"node a=ananas b=2.0"
                err.append({'class': 7, 'subclass': 1734018842, 'text': mapcss.tr('test #1882 - {0}-{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # node[x]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"node building=yes"
                # assertMatch:"node x=z"
                err.append({'class': 9, 'subclass': 555657026, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[x]!:closed
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test closed rewrite {0}","{0.tag}")
                # assertMatch:"node x=yes"
                err.append({'class': 10, 'subclass': 2047373107, 'text': mapcss.tr('test closed rewrite {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[any(tag("x"),"")==any(tag("y"),"hello")]
        # node[a]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.any_(mapcss.tag(tags, 'x'), '') == mapcss.any_(mapcss.tag(tags, 'y'), 'hello')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test any {0} {1}",any(tag("b"),""),any(tag("c"),tag("d"),""))
                # assertMatch:"node a=1 b=2 c=3 d=four"
                # assertMatch:"node a=1 b=2 d=four"
                # assertMatch:"node a=1"
                # assertNoMatch:"node unknownkey=yes"
                # assertNoMatch:"node x=bye y=world"
                # assertMatch:"node x=hello y=hello"
                # assertNoMatch:"node x=hello y=world"
                # assertMatch:"node x=hello"
                # assertNoMatch:"node y=world"
                err.append({'class': 11, 'subclass': 1778220616, 'text': mapcss.tr('test any {0} {1}', mapcss.any_(mapcss.tag(tags, 'b'), ''), mapcss.any_(mapcss.tag(tags, 'c'), mapcss.tag(tags, 'd'), ''))})

        # node[any(tag("x"),tag("y"))]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.any_(mapcss.tag(tags, 'x'), mapcss.tag(tags, 'y'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test"
                # assertMatch:"node x=yes"
                # assertMatch:"node y=yes"
                # assertNoMatch:"node z=yes"
                err.append({'class': 6, 'subclass': 519126950, 'text': {'en': 'test'}})

        # node[x][substring(tag(x),1)=="bcde"][substring(tag(x),1,3)="bc"]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x')) and (mapcss.substring(mapcss.tag(tags, 'x'), 1) == 'bcde') and (mapcss.substring(mapcss.tag(tags, 'x'), 1, 3) == 'bc'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test"
                # assertMatch:"node x=abcde"
                err.append({'class': 6, 'subclass': 770828321, 'text': {'en': 'test'}})

        # node[a][concat(tag("a"),"bc",tag("d"))=="1bc"]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss.concat(mapcss.tag(tags, 'a'), 'bc', mapcss.tag(tags, 'd')) == '1bc'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test concat {0}",concat(tag("b"),tag("c")))
                # assertNoMatch:"node a=1 b=2 c=c d=d"
                # assertMatch:"node a=1 b=2 c=c"
                # assertMatch:"node a=1 b=2"
                # assertMatch:"node a=1"
                err.append({'class': 12, 'subclass': 2101484523, 'text': mapcss.tr('test concat {0}', mapcss.concat(mapcss.tag(tags, 'b'), mapcss.tag(tags, 'c')))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_a = set_b = False

        # way[x~=C1]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.list_contains(mapcss._tag_capture(capture_tags, 0, tags, 'x'), mapcss._value_capture(capture_tags, 0, 'C1'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test #1610"
                # assertMatch:"way x=C00;C1;C22"
                # assertMatch:"way x=C1"
                # assertNoMatch:"way x=C12"
                err.append({'class': 13, 'subclass': 1785050832, 'text': {'en': 'test #1610'}})

        # way:righthandtraffic[x=y][z?]
        if ('x' in keys and 'z' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 1, tags, 'x') == mapcss._value_capture(capture_tags, 1, 'y')) and (mapcss._tag_capture(capture_tags, 2, tags, 'z') in ('yes', 'true', '1')) and (mapcss.setting(self.father.config.options, 'driving_side') != 'left'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #1603 - {0}{1}","{1.tag}","{2.tag}")
                # -osmoseAssertMatchWithContext:list("way x=y z=yes","inside=NL")
                err.append({'class': 14, 'subclass': 169712264, 'text': mapcss.tr('test #1603 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{1.tag}'), mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[x=y][z?]:righthandtraffic
        if ('x' in keys and 'z' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x') == mapcss._value_capture(capture_tags, 0, 'y')) and (mapcss._tag_capture(capture_tags, 1, tags, 'z') in ('yes', 'true', '1')) and (mapcss.setting(self.father.config.options, 'driving_side') != 'left'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #1603 - {0}{1}","{0.tag}","{1.tag}")
                # -osmoseAssertMatchWithContext:list("way x=y z=yes","inside=NL")
                err.append({'class': 14, 'subclass': 2074848923, 'text': mapcss.tr('test #1603 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[parking][amenity!~/^(parking|motorcycle_parking)$/]
        if ('parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_75974701, '^(parking|motorcycle_parking)$'), mapcss._tag_capture(capture_tags, 1, tags, 'amenity'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #994 - {0}{1}","{0.key}","{1.tag}")
                err.append({'class': 2, 'subclass': 650362898, 'text': mapcss.tr('test #994 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[a][!c]
        # *[b][!/d/]
        if ('a' in keys) or ('b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'c')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'b')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49048f80)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #328 - {0}{1}","{0.key}","{1.key}")
                # assertNoMatch:"way a=b c=d"
                # assertMatch:"way a=b"
                # assertNoMatch:"way b=a d=c"
                # assertMatch:"way b=c"
                err.append({'class': 3, 'subclass': 1004069731, 'text': mapcss.tr('test #328 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[/abc/=~/def/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(self.re_7f42aaa6, mapcss._match_regex(tags, self.re_4961c1fa))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test commit 373d1ff9bacf8126508bbf3e37467df2bdf17fbd"
                err.append({'class': 4, 'subclass': 1371556921, 'text': {'en': 'test commit 373d1ff9bacf8126508bbf3e37467df2bdf17fbd'}})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        if ('addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #327")
                err.append({'class': 5, 'subclass': 43561107, 'text': mapcss.tr('test #327')})

        # way:righthandtraffic
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.setting(self.father.config.options, 'driving_side') != 'left'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test righthandtraffic")
                # -osmoseAssertNoMatchWithContext:list("way","driving_side=left")
                # -osmoseAssertMatchWithContext:list("way","driving_side=right")
                err.append({'class': 15, 'subclass': 529680562, 'text': mapcss.tr('test righthandtraffic')})

        # way!:righthandtraffic
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.setting(self.father.config.options, 'driving_side') == 'left'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test lefthandtraffic")
                # -osmoseAssertMatchWithContext:list("way","driving_side=left")
                # -osmoseAssertNoMatchWithContext:list("way","driving_side=right")
                err.append({'class': 16, 'subclass': 877255184, 'text': mapcss.tr('test lefthandtraffic')})

        # way[count(uniq_list(tag_regex("abc")))==2]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.count(mapcss.uniq_list(mapcss.tag_regex(tags, self.re_4961c1fa))) == 2))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test"
                # assertNoMatch:"way abc=def abcdef=def"
                # assertMatch:"way abc=def abcdef=ghi abcd=ghi"
                # assertMatch:"way abc=def abcdef=ghi"
                # assertNoMatch:"way abc=def def=def"
                err.append({'class': 6, 'subclass': 346020981, 'text': {'en': 'test'}})

        # way[count(uniq_list(tag_regex("abc")))==2.0]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.count(mapcss.uniq_list(mapcss.tag_regex(tags, self.re_4961c1fa))) == 2.0))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test"
                # assertNoMatch:"way abc=def abcdef=def"
                # assertMatch:"way abc=def abcdef=ghi abcd=ghi"
                # assertMatch:"way abc=def abcdef=ghi"
                # assertNoMatch:"way abc=def def=def"
                err.append({'class': 6, 'subclass': 57938147, 'text': {'en': 'test'}})

        # way[oneway?]
        if ('oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') in ('yes', 'true', '1')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test {0}","{0.tag}")
                # assertMatch:"way oneway=1"
                # assertNoMatch:"way oneway=4.0"
                # assertNoMatch:"way oneway=no"
                # assertMatch:"way oneway=yes"
                # assertNoMatch:"way x=y"
                err.append({'class': 17, 'subclass': 1489464739, 'text': mapcss.tr('test {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[oneway?!]
        if ('oneway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'oneway') not in ('yes', 'true', '1')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test {0}","{0.tag}")
                # assertMatch:"way oneway=0"
                # assertMatch:"way oneway=no"
                # assertNoMatch:"way oneway=yes"
                # assertNoMatch:"way x=y"
                err.append({'class': 17, 'subclass': 722694187, 'text': mapcss.tr('test {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[name*=Trigger][tag("building")=="chapel"||tag("amenity")=="place_of_worship"][x]
        if ('name' in keys and 'x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.string_contains(mapcss._tag_capture(capture_tags, 0, tags, 'name'), mapcss._value_capture(capture_tags, 0, 'Trigger'))) and (mapcss.tag(tags, 'building') == 'chapel' or mapcss.tag(tags, 'amenity') == 'place_of_worship') and (mapcss._tag_capture(capture_tags, 2, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #1303, #1742 {0}","{2.key}")
                # assertMatch:"way amenity=place_of_worship building=chapel name=OsmoseRuleTrigger x=yes"
                # assertMatch:"way amenity=place_of_worship name=OsmoseRuleTrigger x=yes"
                # assertNoMatch:"way amenity=place_of_worship name=Westminster x=yes"
                # assertMatch:"way building=chapel name=OsmoseRuleTrigger x=yes"
                err.append({'class': 18, 'subclass': 1095325051, 'text': mapcss.tr('test #1303, #1742 {0}', mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[name*=Trigger][tag("building")=="chapel"&&tag("amenity")=="place_of_worship"][x]
        if ('name' in keys and 'x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.string_contains(mapcss._tag_capture(capture_tags, 0, tags, 'name'), mapcss._value_capture(capture_tags, 0, 'Trigger'))) and (mapcss.tag(tags, 'building') == 'chapel' and mapcss.tag(tags, 'amenity') == 'place_of_worship') and (mapcss._tag_capture(capture_tags, 2, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #1303 {0}","{2.key}")
                # assertMatch:"way amenity=place_of_worship building=chapel name=OsmoseRuleTrigger x=yes"
                # assertNoMatch:"way amenity=place_of_worship building=chapel name=Westminster x=yes"
                # assertNoMatch:"way amenity=place_of_worship name=OsmoseRuleTrigger x=yes"
                # assertNoMatch:"way building=chapel name=OsmoseRuleTrigger x=yes"
                err.append({'class': 19, 'subclass': 1140742172, 'text': mapcss.tr('test #1303 {0}', mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # way[inside(FR)][x]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.inside(self.father.config.options, 'FR')) and (mapcss._tag_capture(capture_tags, 1, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #1742 - {0}","{1.tag}")
                # -osmoseAssertMatchWithContext:list("way x=y","inside=FR")
                err.append({'class': 20, 'subclass': 1132689531, 'text': mapcss.tr('test #1742 - {0}', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[a][a=*b]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'a') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'b'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"test"
                err.append({'class': 6, 'subclass': 1343056298, 'text': {'en': 'test'}})

        # way[x]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("test")
                # -osmoseTags:list("osmose_rules")
                # -osmoseTrap:tr("Don't do this!")
                # -osmoseDetail:tr("More {0}.","`info`")
                # -osmoseExample:"Look at me, I haven't lost my apostrophe"
                # -osmoseItemClassLevel:"4/97:2/1"
                # -osmoseFix:"This may fix it."
                # -osmoseResource:"https://wiki.openstreetmap.org/wiki/Useful_Page"
                # throwOther:tr("test")
                # fixRemove:"x"
                # fixAdd:"y=z"
                # assertMatch:"way x=yes"
                # assertNoMatch:"way y=yes"
                err.append({'class': 97, 'subclass': 2, 'text': mapcss.tr('test'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['y','z']]),
                    '-': ([
                    'x'])
                }})

        # way[x]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("test")
                # -osmoseTags:list("osmose_rules")
                # -osmoseTrap:tr("Don't do this!")
                # -osmoseDetail:tr("More {0}.","`info`")
                # -osmoseExample:"Look at me, I haven't lost my apostrophe"
                # -osmoseItemClassLevel:"4/99:2/1"
                # -osmoseFix:"This may fix it."
                # -osmoseResource:"https://wiki.openstreetmap.org/wiki/Useful_Page"
                # throwOther:tr("test")
                # fixRemove:"x"
                # fixAdd:"y=z"
                # assertMatch:"way x=yes"
                # assertNoMatch:"way y=yes"
                err.append({'class': 99, 'subclass': 2, 'text': mapcss.tr('test'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['y','z']]),
                    '-': ([
                    'x'])
                }})

        # way[maxspeed>5000]
        if ('maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'maxspeed') > mapcss._value_capture(capture_tags, 0, 5000)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test {0}{1}","text","{0.key}")
                # assertMatch:"way maxspeed=10000"
                # assertNoMatch:"way maxspeed=5000"
                # assertNoMatch:"way maxspeed=default"
                # assertNoMatch:"way"
                err.append({'class': 21, 'subclass': 2063115534, 'text': mapcss.tr('test {0}{1}', 'text', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # way[tag(a)>tag(b)]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.tag(tags, 'a') > mapcss.tag(tags, 'b')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test"
                # assertNoMatch:"way a=0 b=1"
                # assertNoMatch:"way a=0 b=yes"
                # assertMatch:"way a=1 b=0"
                err.append({'class': 6, 'subclass': 384294833, 'text': {'en': 'test'}})

        # way[x]
        if ('x' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'x')))
                except mapcss.RuleAbort: pass
            if match:
                # set a
                # set b
                # throwWarning:"test"
                # assertMatch:"way x=y"
                set_a = True
                set_b = True
                err.append({'class': 6, 'subclass': 1961315435, 'text': {'en': 'test'}})

        # area[building]
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"way area=no building=yes"
                # assertMatch:"way area=yes building=yes"
                # assertMatch:"way building=yes"
                # assertNoMatch:"way x=yes"
                err.append({'class': 9, 'subclass': 1099901647, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # area[building]:closed:closed2
        # area[landuse]:closed2
        if ('building' in keys) or ('landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')) and (nds[0] == nds[-1]) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"way area=no building=yes"
                # assertNoMatch:"way area=no landuse=yes"
                err.append({'class': 9, 'subclass': 2006953473, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # area[building]!:closed
        if ('building' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                err.append({'class': 9, 'subclass': 1591435356, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[y]
        # area[building=yes]
        if ('building' in keys) or ('y' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'y')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, -1, tags, 'area') != mapcss._value_const_capture(capture_tags, -1, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"way area=no building=yes"
                # assertMatch:"way building=yes"
                # assertMatch:"way y=z"
                err.append({'class': 9, 'subclass': 2128563767, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []
        set_a = set_b = False

        # *[parking][amenity!~/^(parking|motorcycle_parking)$/]
        if ('parking' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'parking')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_75974701, '^(parking|motorcycle_parking)$'), mapcss._tag_capture(capture_tags, 1, tags, 'amenity'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #994 - {0}{1}","{0.key}","{1.tag}")
                err.append({'class': 2, 'subclass': 650362898, 'text': mapcss.tr('test #994 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *[a][!c]
        # *[b][!/d/]
        if ('a' in keys) or ('b' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'c')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'b')) and (not mapcss._tag_capture(capture_tags, 1, tags, self.re_49048f80)))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #328 - {0}{1}","{0.key}","{1.key}")
                err.append({'class': 3, 'subclass': 1004069731, 'text': mapcss.tr('test #328 - {0}{1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *[/abc/=~/def/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(self.re_7f42aaa6, mapcss._match_regex(tags, self.re_4961c1fa))))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:"test commit 373d1ff9bacf8126508bbf3e37467df2bdf17fbd"
                # assertNoMatch:"relation ABC=DEF"
                # assertMatch:"relation abc=def"
                # assertNoMatch:"relation abc=ghi"
                # assertMatch:"relation xabcx=xdefx"
                err.append({'class': 4, 'subclass': 1371556921, 'text': {'en': 'test commit 373d1ff9bacf8126508bbf3e37467df2bdf17fbd'}})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        if ('addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test #327")
                err.append({'class': 5, 'subclass': 43561107, 'text': mapcss.tr('test #327')})

        # *[a][a=*b]
        if ('a' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'a')) and (mapcss._tag_capture(capture_tags, 1, tags, 'a') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, 'b'))))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:"test"
                err.append({'class': 6, 'subclass': 1343056298, 'text': {'en': 'test'}})

        # area[building]
        if ('building' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"relation building=yes"
                # assertMatch:"relation type=multipolygon building=yes"
                # assertNoMatch:"relation type=multipolygon x=yes"
                err.append({'class': 9, 'subclass': 1099901647, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # area[building]:closed:closed2
        # area[landuse]:closed2
        if ('building' in keys and 'type' in keys) or ('landuse' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')) and (mapcss._tag_capture(capture_tags, -2, tags, 'type') == mapcss._value_capture(capture_tags, -2, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'landuse')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')) and (mapcss._tag_capture(capture_tags, -2, tags, 'type') == mapcss._value_capture(capture_tags, -2, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"relation building=yes"
                # assertNoMatch:"relation landuse=yes"
                # assertMatch:"relation type=multipolygon building=yes"
                # assertMatch:"relation type=multipolygon landuse=yes"
                # assertNoMatch:"relation type=multipolygon x=yes"
                err.append({'class': 9, 'subclass': 2006953473, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # area[building]!:closed
        if ('building' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')) and (mapcss._tag_capture(capture_tags, -2, tags, 'type') != mapcss._value_const_capture(capture_tags, -2, 'multipolygon', 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"relation type=multipolygon building=yes"
                # assertNoMatch:"relation type=other building=yes"
                err.append({'class': 9, 'subclass': 1591435356, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # area[building=yes]
        if ('building' in keys and 'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'building') == mapcss._value_capture(capture_tags, 0, 'yes')) and (mapcss._tag_capture(capture_tags, -1, tags, 'type') == mapcss._value_capture(capture_tags, -1, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test area rule {0}","{0.tag}")
                # assertNoMatch:"relation building=yes"
                # assertMatch:"relation type=multipolygon building=yes"
                # assertNoMatch:"relation x=z y=z"
                err.append({'class': 9, 'subclass': 434545653, 'text': mapcss.tr('test area rule {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # relation[y]:closed
        # relation[z]!:closed2
        if ('type' in keys and 'y' in keys) or ('z' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'y')) and (mapcss._tag_capture(capture_tags, -2, tags, 'type') == mapcss._value_capture(capture_tags, -2, 'multipolygon')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'z')) and (mapcss._tag_capture(capture_tags, -2, tags, 'type') != mapcss._value_const_capture(capture_tags, -2, 'multipolygon', 'multipolygon')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("test closed rewrite {0}","{0.tag}")
                # assertMatch:"relation type=multipolygon y=yes"
                # assertNoMatch:"relation type=multipolygon z=yes"
                # assertNoMatch:"relation type=other y=yes"
                # assertMatch:"relation type=other z=yes"
                err.append({'class': 10, 'subclass': 758090756, 'text': mapcss.tr('test closed rewrite {0}', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # relation[tag(x)==parent_tag(x)]
        # Part of rule not implemented

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = test_mapcss_parsing_evalutation(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'x': '0'}), expected={'class': 98, 'subclass': 0})
        self.check_not_err(n.node(data, {'x': '1'}), expected={'class': 98, 'subclass': 0})
        self.check_not_err(n.node(data, {'x': '1.0'}), expected={'class': 98, 'subclass': 0})
        self.check_not_err(n.node(data, {'x': 'Osmose'}), expected={'class': 98, 'subclass': 0})
        self.check_not_err(n.node(data, {'x': '0'}), expected={'class': 1, 'subclass': 659546685})
        self.check_err(n.node(data, {'x': '1'}), expected={'class': 1, 'subclass': 659546685})
        self.check_err(n.node(data, {'x': '1.0'}), expected={'class': 1, 'subclass': 659546685})
        self.check_err(n.node(data, {'x': 'Osmose'}), expected={'class': 1, 'subclass': 659546685})
        self.check_err(n.node(data, {'amenity': 'osmose', 'parking': 'yes'}), expected={'class': 2, 'subclass': 650362898})
        self.check_not_err(n.node(data, {'amenity': 'parking', 'parking': 'yes'}), expected={'class': 2, 'subclass': 650362898})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.node(data, {'addr:street': 'Neuestraßebahn'}), expected={'class': 5, 'subclass': 43561107})
        with with_options(n, {'country': 'LI'}):
            self.check_err(n.node(data, {'addr:street': 'Neuestraßebahn'}), expected={'class': 5, 'subclass': 43561107})
        self.check_err(n.node(data, {'a': 'x', 'b': 'x'}), expected={'class': 6, 'subclass': 1343056298})
        self.check_not_err(n.node(data, {'a': 'x', 'b': 'y'}), expected={'class': 6, 'subclass': 1343056298})
        self.check_not_err(n.node(data, {'a': 'x'}), expected={'class': 6, 'subclass': 1343056298})
        self.check_not_err(n.node(data, {'abc': 'def', 'lit': 'yes'}), expected={'class': 6, 'subclass': 130427469})
        self.check_err(n.node(data, {'lit': 'yes'}), expected={'class': 6, 'subclass': 130427469})
        self.check_not_err(n.node(data, {'abc': 'def', 'lit': 'yes'}), expected={'class': 6, 'subclass': 612979508})
        self.check_err(n.node(data, {'lit': 'yes'}), expected={'class': 6, 'subclass': 612979508})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6a'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '3.0', 'b': '6a'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6a'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': 'X', 'b': 'Y'}), expected={'class': 7, 'subclass': 766520351})
        self.check_err(n.node(data, {'a': '6', 'b': '-5'}), expected={'class': 7, 'subclass': 766520351})
        self.check_err(n.node(data, {'a': '12', 'b': '3'}), expected={'class': 7, 'subclass': 766520351})
        self.check_err(n.node(data, {'a': '12.0', 'b': '3'}), expected={'class': 7, 'subclass': 766520351})
        self.check_err(n.node(data, {'a': '6', 'b': '3'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3'}), expected={'class': 7, 'subclass': 766520351})
        self.check_err(n.node(data, {'a': '12', 'b': '3.0'}), expected={'class': 7, 'subclass': 766520351})
        self.check_err(n.node(data, {'a': '6.0', 'b': '3.0'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '6', 'b': '3a'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3a'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': 'Y', 'b': 'X'}), expected={'class': 7, 'subclass': 766520351})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6a'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '3.0', 'b': '6a'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6a'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': 'X', 'b': 'Y'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_err(n.node(data, {'a': '6', 'b': '-5'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_err(n.node(data, {'a': '12', 'b': '3'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_err(n.node(data, {'a': '12.0', 'b': '3'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_err(n.node(data, {'a': '6', 'b': '3'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_err(n.node(data, {'a': '12', 'b': '3.0'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_err(n.node(data, {'a': '6.0', 'b': '3.0'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '6', 'b': '3a'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3a'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': 'Y', 'b': 'X'}), expected={'class': 7, 'subclass': 1296744085})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6a'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '3.0', 'b': '6a'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6a'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': 'X', 'b': 'Y'}), expected={'class': 7, 'subclass': 660577118})
        self.check_err(n.node(data, {'a': '6', 'b': '-5'}), expected={'class': 7, 'subclass': 660577118})
        self.check_err(n.node(data, {'a': '12', 'b': '3'}), expected={'class': 7, 'subclass': 660577118})
        self.check_err(n.node(data, {'a': '12.0', 'b': '3'}), expected={'class': 7, 'subclass': 660577118})
        self.check_err(n.node(data, {'a': '6', 'b': '3'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3'}), expected={'class': 7, 'subclass': 660577118})
        self.check_err(n.node(data, {'a': '12', 'b': '3.0'}), expected={'class': 7, 'subclass': 660577118})
        self.check_err(n.node(data, {'a': '6.0', 'b': '3.0'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '6', 'b': '3a'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3a'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': 'Y', 'b': 'X'}), expected={'class': 7, 'subclass': 660577118})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '3', 'b': '6a'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '3.0', 'b': '6a'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '3a', 'b': '6a'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': 'X', 'b': 'Y'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_err(n.node(data, {'a': '6', 'b': '-5'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_err(n.node(data, {'a': '12', 'b': '3'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_err(n.node(data, {'a': '12.0', 'b': '3'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_err(n.node(data, {'a': '6', 'b': '3'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_err(n.node(data, {'a': '12', 'b': '3.0'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_err(n.node(data, {'a': '6.0', 'b': '3.0'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '6', 'b': '3a'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '6a', 'b': '3a'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': 'Y', 'b': 'X'}), expected={'class': 7, 'subclass': 1302849761})
        self.check_not_err(n.node(data, {'a': '-5'}), expected={'class': 8, 'subclass': 1910232765})
        self.check_not_err(n.node(data, {'a': '1'}), expected={'class': 8, 'subclass': 1910232765})
        self.check_not_err(n.node(data, {'a': '1.0'}), expected={'class': 8, 'subclass': 1910232765})
        self.check_err(n.node(data, {'a': '3'}), expected={'class': 8, 'subclass': 1910232765})
        self.check_err(n.node(data, {'a': '3.0'}), expected={'class': 8, 'subclass': 1910232765})
        self.check_not_err(n.node(data, {'a': 'X'}), expected={'class': 8, 'subclass': 1910232765})
        self.check_not_err(n.node(data, {'a': '-5'}), expected={'class': 8, 'subclass': 1369591651})
        self.check_not_err(n.node(data, {'a': '1'}), expected={'class': 8, 'subclass': 1369591651})
        self.check_not_err(n.node(data, {'a': '1.0'}), expected={'class': 8, 'subclass': 1369591651})
        self.check_err(n.node(data, {'a': '3'}), expected={'class': 8, 'subclass': 1369591651})
        self.check_err(n.node(data, {'a': '3.0'}), expected={'class': 8, 'subclass': 1369591651})
        self.check_not_err(n.node(data, {'a': 'X'}), expected={'class': 8, 'subclass': 1369591651})
        self.check_not_err(n.node(data, {'a': 'X'}), expected={'class': 8, 'subclass': 130115842})
        self.check_err(n.node(data, {'a': 'ananas'}), expected={'class': 8, 'subclass': 130115842})
        self.check_not_err(n.node(data, {'a': 'X'}), expected={'class': 8, 'subclass': 935120167})
        self.check_err(n.node(data, {'a': 'ananas'}), expected={'class': 8, 'subclass': 935120167})
        self.check_not_err(n.node(data, {'a': 'X', 'b': '2'}), expected={'class': 7, 'subclass': 1734018842})
        self.check_not_err(n.node(data, {'a': 'X', 'b': '2.0'}), expected={'class': 7, 'subclass': 1734018842})
        self.check_err(n.node(data, {'a': 'ananas', 'b': '2'}), expected={'class': 7, 'subclass': 1734018842})
        self.check_err(n.node(data, {'a': 'ananas', 'b': '2.0'}), expected={'class': 7, 'subclass': 1734018842})
        self.check_not_err(n.node(data, {'building': 'yes'}), expected={'class': 9, 'subclass': 555657026})
        self.check_err(n.node(data, {'x': 'z'}), expected={'class': 9, 'subclass': 555657026})
        self.check_err(n.node(data, {'x': 'yes'}), expected={'class': 10, 'subclass': 2047373107})
        self.check_err(n.node(data, {'a': '1', 'b': '2', 'c': '3', 'd': 'four'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_err(n.node(data, {'a': '1', 'b': '2', 'd': 'four'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_err(n.node(data, {'a': '1'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_not_err(n.node(data, {'unknownkey': 'yes'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_not_err(n.node(data, {'x': 'bye', 'y': 'world'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_err(n.node(data, {'x': 'hello', 'y': 'hello'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_not_err(n.node(data, {'x': 'hello', 'y': 'world'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_err(n.node(data, {'x': 'hello'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_not_err(n.node(data, {'y': 'world'}), expected={'class': 11, 'subclass': 1778220616})
        self.check_err(n.node(data, {'x': 'yes'}), expected={'class': 6, 'subclass': 519126950})
        self.check_err(n.node(data, {'y': 'yes'}), expected={'class': 6, 'subclass': 519126950})
        self.check_not_err(n.node(data, {'z': 'yes'}), expected={'class': 6, 'subclass': 519126950})
        self.check_err(n.node(data, {'x': 'abcde'}), expected={'class': 6, 'subclass': 770828321})
        self.check_not_err(n.node(data, {'a': '1', 'b': '2', 'c': 'c', 'd': 'd'}), expected={'class': 12, 'subclass': 2101484523})
        self.check_err(n.node(data, {'a': '1', 'b': '2', 'c': 'c'}), expected={'class': 12, 'subclass': 2101484523})
        self.check_err(n.node(data, {'a': '1', 'b': '2'}), expected={'class': 12, 'subclass': 2101484523})
        self.check_err(n.node(data, {'a': '1'}), expected={'class': 12, 'subclass': 2101484523})
        self.check_err(n.way(data, {'x': 'C00;C1;C22'}, [0]), expected={'class': 13, 'subclass': 1785050832})
        self.check_err(n.way(data, {'x': 'C1'}, [0]), expected={'class': 13, 'subclass': 1785050832})
        self.check_not_err(n.way(data, {'x': 'C12'}, [0]), expected={'class': 13, 'subclass': 1785050832})
        with with_options(n, {'country': 'NL'}):
            self.check_err(n.way(data, {'x': 'y', 'z': 'yes'}, [0]), expected={'class': 14, 'subclass': 169712264})
        with with_options(n, {'country': 'NL'}):
            self.check_err(n.way(data, {'x': 'y', 'z': 'yes'}, [0]), expected={'class': 14, 'subclass': 2074848923})
        self.check_not_err(n.way(data, {'a': 'b', 'c': 'd'}, [0]), expected={'class': 3, 'subclass': 1004069731})
        self.check_err(n.way(data, {'a': 'b'}, [0]), expected={'class': 3, 'subclass': 1004069731})
        self.check_not_err(n.way(data, {'b': 'a', 'd': 'c'}, [0]), expected={'class': 3, 'subclass': 1004069731})
        self.check_err(n.way(data, {'b': 'c'}, [0]), expected={'class': 3, 'subclass': 1004069731})
        with with_options(n, {'driving_side': 'left'}):
            self.check_not_err(n.way(data, {}, [0]), expected={'class': 15, 'subclass': 529680562})
        with with_options(n, {'driving_side': 'right'}):
            self.check_err(n.way(data, {}, [0]), expected={'class': 15, 'subclass': 529680562})
        with with_options(n, {'driving_side': 'left'}):
            self.check_err(n.way(data, {}, [0]), expected={'class': 16, 'subclass': 877255184})
        with with_options(n, {'driving_side': 'right'}):
            self.check_not_err(n.way(data, {}, [0]), expected={'class': 16, 'subclass': 877255184})
        self.check_not_err(n.way(data, {'abc': 'def', 'abcdef': 'def'}, [0]), expected={'class': 6, 'subclass': 346020981})
        self.check_err(n.way(data, {'abc': 'def', 'abcd': 'ghi', 'abcdef': 'ghi'}, [0]), expected={'class': 6, 'subclass': 346020981})
        self.check_err(n.way(data, {'abc': 'def', 'abcdef': 'ghi'}, [0]), expected={'class': 6, 'subclass': 346020981})
        self.check_not_err(n.way(data, {'abc': 'def', 'def': 'def'}, [0]), expected={'class': 6, 'subclass': 346020981})
        self.check_not_err(n.way(data, {'abc': 'def', 'abcdef': 'def'}, [0]), expected={'class': 6, 'subclass': 57938147})
        self.check_err(n.way(data, {'abc': 'def', 'abcd': 'ghi', 'abcdef': 'ghi'}, [0]), expected={'class': 6, 'subclass': 57938147})
        self.check_err(n.way(data, {'abc': 'def', 'abcdef': 'ghi'}, [0]), expected={'class': 6, 'subclass': 57938147})
        self.check_not_err(n.way(data, {'abc': 'def', 'def': 'def'}, [0]), expected={'class': 6, 'subclass': 57938147})
        self.check_err(n.way(data, {'oneway': '1'}, [0]), expected={'class': 17, 'subclass': 1489464739})
        self.check_not_err(n.way(data, {'oneway': '4.0'}, [0]), expected={'class': 17, 'subclass': 1489464739})
        self.check_not_err(n.way(data, {'oneway': 'no'}, [0]), expected={'class': 17, 'subclass': 1489464739})
        self.check_err(n.way(data, {'oneway': 'yes'}, [0]), expected={'class': 17, 'subclass': 1489464739})
        self.check_not_err(n.way(data, {'x': 'y'}, [0]), expected={'class': 17, 'subclass': 1489464739})
        self.check_err(n.way(data, {'oneway': '0'}, [0]), expected={'class': 17, 'subclass': 722694187})
        self.check_err(n.way(data, {'oneway': 'no'}, [0]), expected={'class': 17, 'subclass': 722694187})
        self.check_not_err(n.way(data, {'oneway': 'yes'}, [0]), expected={'class': 17, 'subclass': 722694187})
        self.check_not_err(n.way(data, {'x': 'y'}, [0]), expected={'class': 17, 'subclass': 722694187})
        self.check_err(n.way(data, {'amenity': 'place_of_worship', 'building': 'chapel', 'name': 'OsmoseRuleTrigger', 'x': 'yes'}, [0]), expected={'class': 18, 'subclass': 1095325051})
        self.check_err(n.way(data, {'amenity': 'place_of_worship', 'name': 'OsmoseRuleTrigger', 'x': 'yes'}, [0]), expected={'class': 18, 'subclass': 1095325051})
        self.check_not_err(n.way(data, {'amenity': 'place_of_worship', 'name': 'Westminster', 'x': 'yes'}, [0]), expected={'class': 18, 'subclass': 1095325051})
        self.check_err(n.way(data, {'building': 'chapel', 'name': 'OsmoseRuleTrigger', 'x': 'yes'}, [0]), expected={'class': 18, 'subclass': 1095325051})
        self.check_err(n.way(data, {'amenity': 'place_of_worship', 'building': 'chapel', 'name': 'OsmoseRuleTrigger', 'x': 'yes'}, [0]), expected={'class': 19, 'subclass': 1140742172})
        self.check_not_err(n.way(data, {'amenity': 'place_of_worship', 'building': 'chapel', 'name': 'Westminster', 'x': 'yes'}, [0]), expected={'class': 19, 'subclass': 1140742172})
        self.check_not_err(n.way(data, {'amenity': 'place_of_worship', 'name': 'OsmoseRuleTrigger', 'x': 'yes'}, [0]), expected={'class': 19, 'subclass': 1140742172})
        self.check_not_err(n.way(data, {'building': 'chapel', 'name': 'OsmoseRuleTrigger', 'x': 'yes'}, [0]), expected={'class': 19, 'subclass': 1140742172})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'x': 'y'}, [0]), expected={'class': 20, 'subclass': 1132689531})
        self.check_err(n.way(data, {'x': 'yes'}, [0]), expected={'class': 97, 'subclass': 2})
        self.check_not_err(n.way(data, {'y': 'yes'}, [0]), expected={'class': 97, 'subclass': 2})
        self.check_err(n.way(data, {'x': 'yes'}, [0]), expected={'class': 99, 'subclass': 2})
        self.check_not_err(n.way(data, {'y': 'yes'}, [0]), expected={'class': 99, 'subclass': 2})
        self.check_err(n.way(data, {'maxspeed': '10000'}, [0]), expected={'class': 21, 'subclass': 2063115534})
        self.check_not_err(n.way(data, {'maxspeed': '5000'}, [0]), expected={'class': 21, 'subclass': 2063115534})
        self.check_not_err(n.way(data, {'maxspeed': 'default'}, [0]), expected={'class': 21, 'subclass': 2063115534})
        self.check_not_err(n.way(data, {}, [0]), expected={'class': 21, 'subclass': 2063115534})
        self.check_not_err(n.way(data, {'a': '0', 'b': '1'}, [0]), expected={'class': 6, 'subclass': 384294833})
        self.check_not_err(n.way(data, {'a': '0', 'b': 'yes'}, [0]), expected={'class': 6, 'subclass': 384294833})
        self.check_err(n.way(data, {'a': '1', 'b': '0'}, [0]), expected={'class': 6, 'subclass': 384294833})
        self.check_err(n.way(data, {'x': 'y'}, [0]), expected={'class': 6, 'subclass': 1961315435})
        self.check_not_err(n.way(data, {'area': 'no', 'building': 'yes'}, [0]), expected={'class': 9, 'subclass': 1099901647})
        self.check_err(n.way(data, {'area': 'yes', 'building': 'yes'}, [0]), expected={'class': 9, 'subclass': 1099901647})
        self.check_err(n.way(data, {'building': 'yes'}, [0]), expected={'class': 9, 'subclass': 1099901647})
        self.check_not_err(n.way(data, {'x': 'yes'}, [0]), expected={'class': 9, 'subclass': 1099901647})
        self.check_not_err(n.way(data, {'area': 'no', 'building': 'yes'}, [0]), expected={'class': 9, 'subclass': 2006953473})
        self.check_not_err(n.way(data, {'area': 'no', 'landuse': 'yes'}, [0]), expected={'class': 9, 'subclass': 2006953473})
        self.check_not_err(n.way(data, {'area': 'no', 'building': 'yes'}, [0]), expected={'class': 9, 'subclass': 2128563767})
        self.check_err(n.way(data, {'building': 'yes'}, [0]), expected={'class': 9, 'subclass': 2128563767})
        self.check_err(n.way(data, {'y': 'z'}, [0]), expected={'class': 9, 'subclass': 2128563767})
        self.check_not_err(n.relation(data, {'ABC': 'DEF'}, []), expected={'class': 4, 'subclass': 1371556921})
        self.check_err(n.relation(data, {'abc': 'def'}, []), expected={'class': 4, 'subclass': 1371556921})
        self.check_not_err(n.relation(data, {'abc': 'ghi'}, []), expected={'class': 4, 'subclass': 1371556921})
        self.check_err(n.relation(data, {'xabcx': 'xdefx'}, []), expected={'class': 4, 'subclass': 1371556921})
        self.check_not_err(n.relation(data, {'building': 'yes'}, []), expected={'class': 9, 'subclass': 1099901647})
        self.check_err(n.relation(data, {'building': 'yes', 'type': 'multipolygon'}, []), expected={'class': 9, 'subclass': 1099901647})
        self.check_not_err(n.relation(data, {'type': 'multipolygon', 'x': 'yes'}, []), expected={'class': 9, 'subclass': 1099901647})
        self.check_not_err(n.relation(data, {'building': 'yes'}, []), expected={'class': 9, 'subclass': 2006953473})
        self.check_not_err(n.relation(data, {'landuse': 'yes'}, []), expected={'class': 9, 'subclass': 2006953473})
        self.check_err(n.relation(data, {'building': 'yes', 'type': 'multipolygon'}, []), expected={'class': 9, 'subclass': 2006953473})
        self.check_err(n.relation(data, {'landuse': 'yes', 'type': 'multipolygon'}, []), expected={'class': 9, 'subclass': 2006953473})
        self.check_not_err(n.relation(data, {'type': 'multipolygon', 'x': 'yes'}, []), expected={'class': 9, 'subclass': 2006953473})
        self.check_not_err(n.relation(data, {'building': 'yes', 'type': 'multipolygon'}, []), expected={'class': 9, 'subclass': 1591435356})
        self.check_not_err(n.relation(data, {'building': 'yes', 'type': 'other'}, []), expected={'class': 9, 'subclass': 1591435356})
        self.check_not_err(n.relation(data, {'building': 'yes'}, []), expected={'class': 9, 'subclass': 434545653})
        self.check_err(n.relation(data, {'building': 'yes', 'type': 'multipolygon'}, []), expected={'class': 9, 'subclass': 434545653})
        self.check_not_err(n.relation(data, {'x': 'z', 'y': 'z'}, []), expected={'class': 9, 'subclass': 434545653})
        self.check_err(n.relation(data, {'type': 'multipolygon', 'y': 'yes'}, []), expected={'class': 10, 'subclass': 758090756})
        self.check_not_err(n.relation(data, {'type': 'multipolygon', 'z': 'yes'}, []), expected={'class': 10, 'subclass': 758090756})
        self.check_not_err(n.relation(data, {'type': 'other', 'y': 'yes'}, []), expected={'class': 10, 'subclass': 758090756})
        self.check_err(n.relation(data, {'type': 'other', 'z': 'yes'}, []), expected={'class': 10, 'subclass': 758090756})
