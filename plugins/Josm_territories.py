#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_territories(Plugin):


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9009001] = {'item': 9009, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'deprecated tagging')}
        self.errors[9009002] = {'item': 9009, 'level': 2, 'tag': ["tag"], 'desc': mapcss.tr(u'street name contains ss')}
        self.errors[9009003] = {'item': 9009, 'level': 2, 'tag': ["tag"], 'desc': mapcss.tr(u'street name contains ß')}

        self.re_3d3faeb5 = re.compile(ur'(?i).*Straße.*')
        self.re_559797c8 = re.compile(ur'(?i).*Strasser.*')
        self.re_5b84a257 = re.compile(ur'(?i).*Strasse.*')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'operator') == mapcss._value_capture(capture_tags, 0, u'ERDF') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 9009001, 'subclass': 262422756, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'operator',u'Enedis']])
                }})

        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][inside("DE,AT")]
        if (u'addr:street' in keys) or (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_559797c8), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'DE,AT'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_559797c8), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'DE,AT'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ss")
                err.append({'class': 9009002, 'subclass': 821908491, 'text': mapcss.tr(u'street name contains ss')})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if (u'addr:street' in keys) or (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'LI,CH'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'LI,CH'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ß")
                err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr(u'street name contains ß')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'operator') == mapcss._value_capture(capture_tags, 0, u'ERDF') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 9009001, 'subclass': 262422756, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'operator',u'Enedis']])
                }})

        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][inside("DE,AT")]
        if (u'addr:street' in keys) or (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_559797c8), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'DE,AT'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_559797c8), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'DE,AT'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ss")
                err.append({'class': 9009002, 'subclass': 821908491, 'text': mapcss.tr(u'street name contains ss')})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if (u'addr:street' in keys) or (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'LI,CH'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'LI,CH'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ß")
                err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr(u'street name contains ß')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'operator') == mapcss._value_capture(capture_tags, 0, u'ERDF') and mapcss.inside(self.father.config.options, u'FR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 9009001, 'subclass': 262422756, 'text': mapcss.tr(u'{0} is deprecated', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'operator',u'Enedis']])
                }})

        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][inside("DE,AT")]
        if (u'addr:street' in keys) or (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_559797c8), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'DE,AT'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5b84a257), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_559797c8), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'DE,AT'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ss")
                err.append({'class': 9009002, 'subclass': 821908491, 'text': mapcss.tr(u'street name contains ss')})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if (u'addr:street' in keys) or (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'LI,CH'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_3d3faeb5), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'LI,CH'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("street name contains ß")
                err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr(u'street name contains ß')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_territories(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


