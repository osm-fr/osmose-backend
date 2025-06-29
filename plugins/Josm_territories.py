#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_territories(PluginMapCSS):
    # ------------------------------- IMPORTANT -------------------------------
    # This file is generated automatically and should not be modified directly.
    # Instead, modify the source mapcss file and regenerate this Python script.
    # -------------------------------------------------------------------------

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/territories.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9009001] = self.def_class(item = 9009, level = 3, tags = ["tag"], title = mapcss.tr('deprecated tagging'))
        self.errors[9009002] = self.def_class(item = 9009, level = 2, tags = ["tag"], title = mapcss.tr('street name contains ss'))
        self.errors[9009003] = self.def_class(item = 9009, level = 2, tags = ["tag"], title = mapcss.tr('street name contains ß'))

        self.re_1596ad87 = re.compile(r'(?i).*spannungstrasse.*')
        self.re_3d3faeb5 = re.compile(r'(?i).*Straße.*')
        self.re_559797c8 = re.compile(r'(?i).*Strasser.*')
        self.re_5b84a257 = re.compile(r'(?i).*Strasse.*')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][name!~/(?i).*spannungstrasse.*/][inside("DE,AT")]
        if ('addr:street' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_559797c8, '(?i).*Strasser.*'), mapcss._tag_capture(capture_tags, 1, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'DE,AT')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_559797c8, '(?i).*Strasser.*'), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1596ad87, '(?i).*spannungstrasse.*'), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'DE,AT')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ss")
                err.append({'class': 9009002, 'subclass': 1817721249, 'text': mapcss.tr('street name contains ss')})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if ('addr:street' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ß")
                err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr('street name contains ß')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][name!~/(?i).*spannungstrasse.*/][inside("DE,AT")]
        if ('addr:street' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_559797c8, '(?i).*Strasser.*'), mapcss._tag_capture(capture_tags, 1, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'DE,AT')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_559797c8, '(?i).*Strasser.*'), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1596ad87, '(?i).*spannungstrasse.*'), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'DE,AT')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ss")
                # assertMatch:"way name=Hauptstrasse"
                # assertNoMatch:"way name=Hauptstraße"
                # assertNoMatch:"way name=Hochspannungstrasse"
                # assertNoMatch:"way name=Kapitän-Strasser-Straße"
                # assertNoMatch:"way name=Peter-Strasser-Platz"
                err.append({'class': 9009002, 'subclass': 1817721249, 'text': mapcss.tr('street name contains ss')})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if ('addr:street' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ß")
                # assertNoMatch:"way name=Hauptstrasse"
                # assertMatch:"way name=Hauptstraße"
                err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr('street name contains ß')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][name!~/(?i).*spannungstrasse.*/][inside("DE,AT")]
        if ('addr:street' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_559797c8, '(?i).*Strasser.*'), mapcss._tag_capture(capture_tags, 1, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'DE,AT')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_559797c8, '(?i).*Strasser.*'), mapcss._tag_capture(capture_tags, 1, tags, 'name'))) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_1596ad87, '(?i).*spannungstrasse.*'), mapcss._tag_capture(capture_tags, 2, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'DE,AT')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ss")
                err.append({'class': 9009002, 'subclass': 1817721249, 'text': mapcss.tr('street name contains ss')})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if ('addr:street' in keys) or ('name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'addr:street'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss.inside(self.father.config.options, 'LI,CH')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ß")
                err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr('street name contains ß')})

        # relation[type=associatedStreet][inside("DE")]
        if ('type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'type') == mapcss._value_capture(capture_tags, 0, 'associatedStreet')) and (mapcss.inside(self.father.config.options, 'DE')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated in {1}","{0.tag}","Deutschland")
                # suggestAlternative:"addr:street"
                err.append({'class': 9009001, 'subclass': 746730328, 'text': mapcss.tr('{0} is deprecated in {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), 'Deutschland')})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Josm_territories(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.way(data, {'name': 'Hauptstrasse'}, [0]), expected={'class': 9009002, 'subclass': 1817721249})
        self.check_not_err(n.way(data, {'name': 'Hauptstraße'}, [0]), expected={'class': 9009002, 'subclass': 1817721249})
        self.check_not_err(n.way(data, {'name': 'Hochspannungstrasse'}, [0]), expected={'class': 9009002, 'subclass': 1817721249})
        self.check_not_err(n.way(data, {'name': 'Kapitän-Strasser-Straße'}, [0]), expected={'class': 9009002, 'subclass': 1817721249})
        self.check_not_err(n.way(data, {'name': 'Peter-Strasser-Platz'}, [0]), expected={'class': 9009002, 'subclass': 1817721249})
        self.check_not_err(n.way(data, {'name': 'Hauptstrasse'}, [0]), expected={'class': 9009003, 'subclass': 610086334})
        self.check_err(n.way(data, {'name': 'Hauptstraße'}, [0]), expected={'class': 9009003, 'subclass': 610086334})
