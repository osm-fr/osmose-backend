#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Name_Cadastre_FR(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[50801] = self.def_class(item = 5080, level = 1, tags = mapcss.list_('name', 'fix:chair'), title = mapcss.tr('Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.'))

        self.re_5d724bf1 = re.compile(r'.+([- ]([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre))$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[place=locality][name=~/.+([- ]([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre))$/][inside("FR")]
        # node[place=hamlet][name=~/.+([- ]([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre))$/][inside("FR")]
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place') == mapcss._value_capture(capture_tags, 0, 'locality')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5d724bf1), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place') == mapcss._value_capture(capture_tags, 0, 'hamlet')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5d724bf1), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"5080/50801/1"
                # throwError:tr("Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.")
                # -osmoseAssertNoMatchWithContext:list('node place=hamlet name="Kerbrest"',"inside=FR")
                # -osmoseAssertNoMatchWithContext:list('node place=hamlet name="ZA Sud Loire"',"inside=FR")
                # -osmoseAssertMatchWithContext:list('node place=hamlet name=Montdésert-Sud',"inside=FR")
                err.append({'class': 50801, 'subclass': 0, 'text': mapcss.tr('Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[place=locality][name=~/.+([- ]([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre))$/][inside("FR")]
        # way[place=hamlet][name=~/.+([- ]([Nn]ord|[Ss]ud$|[Ee]st|[Oo]uest|[Cc]entre))$/][inside("FR")]
        if ('name' in keys and 'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place') == mapcss._value_capture(capture_tags, 0, 'locality')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5d724bf1), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'place') == mapcss._value_capture(capture_tags, 0, 'hamlet')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_5d724bf1), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"5080/50801/1"
                # throwError:tr("Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.")
                err.append({'class': 50801, 'subclass': 0, 'text': mapcss.tr('Hamlet or Locality name suffix Nord, Sud, Est, Ouest, Centre should be removed from Cadastre name. Place should be integrated only once.')})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
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
            self.check_not_err(n.node(data, {'name': 'Kerbrest', 'place': 'hamlet'}), expected={'class': 50801, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.node(data, {'name': 'ZA Sud Loire', 'place': 'hamlet'}), expected={'class': 50801, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'name': 'Montdésert-Sud', 'place': 'hamlet'}), expected={'class': 50801, 'subclass': 0})
