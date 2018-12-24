#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Name_Cadastre_FR(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[50801] = {'item': 5080, 'level': 1, 'tag': mapcss.list_(u'name', u'fix:chair'), 'desc': mapcss.tr(u'Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.')}

        self.re_422a87ff = re.compile(ur'.+([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[place=locality][name=~/.+([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre)$/][inside("FR")]
        # node[place=hamlet][name=~/.+([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre)$/][inside("FR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'locality') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_422a87ff), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'hamlet') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_422a87ff), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"5080/50801/1"
                # throwError:tr("Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.")
                # assertNoMatchWithContext:list('node place=hamlet name="ZA Sud Loire"',"inside=FR")
                # assertMatchWithContext:list('node place=hamlet name=Montdésert-Sud',"inside=FR")
                err.append({'class': 50801, 'subclass': 0, 'text': mapcss.tr(u'Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[place=locality][name=~/.+([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre)$/][inside("FR")]
        # way[place=hamlet][name=~/.+([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre)$/][inside("FR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'locality') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_422a87ff), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'hamlet') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_422a87ff), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"5080/50801/1"
                # throwError:tr("Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.")
                err.append({'class': 50801, 'subclass': 0, 'text': mapcss.tr(u'Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Name_Cadastre_FR(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.node(data, {u'name': u'ZA Sud Loire', u'place': u'hamlet'}), expected={'class': 50801, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {u'name': u'Montdésert-Sud', u'place': u'hamlet'}), expected={'class': 50801, 'subclass': 0})
