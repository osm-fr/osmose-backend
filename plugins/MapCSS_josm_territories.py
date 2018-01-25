#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_territories(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9009001] = {'item': 9009, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'deprecated tagging', capture_tags)}
        self.errors[9009002] = {'item': 9009, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'street name contains ss', capture_tags)}
        self.errors[9009003] = {'item': 9009, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'street name contains ß', capture_tags)}

        self.re_3d3faeb5 = re.compile(ur'(?i).*Straße.*')
        self.re_559797c8 = re.compile(ur'(?i).*Strasser.*')
        self.re_5b84a257 = re.compile(ur'(?i).*Strasse.*')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'operator') == u'ERDF' and mapcss.inside(self.father.config.options, u'FR'))):
            # group:tr("deprecated tagging")
            # throwWarning:tr("{0} is deprecated","{0.tag}")
            # suggestAlternative:"operator=Enedis"
            # fixAdd:"operator=Enedis"
            err.append({'class': 9009001, 'subclass': 262422756, 'text': mapcss.tr(u'{0} is deprecated', capture_tags, u'{0.tag}'), 'fix': {
                '+': dict([
                    [u'operator',u'Enedis']])
            }})

        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][inside("DE,AT")]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_5b84a257, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and not mapcss.regexp_test_(self.re_559797c8, mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'DE,AT')) or \
            (mapcss.regexp_test_(self.re_5b84a257, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss.regexp_test_(self.re_559797c8, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'DE,AT'))):
            # throwError:tr("street name contains ss")
            err.append({'class': 9009002, 'subclass': 821908491, 'text': mapcss.tr(u'street name contains ss', capture_tags)})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_3d3faeb5, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'LI,CH')) or \
            (mapcss.regexp_test_(self.re_3d3faeb5, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'LI,CH'))):
            # throwError:tr("street name contains ß")
            err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr(u'street name contains ß', capture_tags)})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'operator') == u'ERDF' and mapcss.inside(self.father.config.options, u'FR'))):
            # group:tr("deprecated tagging")
            # throwWarning:tr("{0} is deprecated","{0.tag}")
            # suggestAlternative:"operator=Enedis"
            # fixAdd:"operator=Enedis"
            err.append({'class': 9009001, 'subclass': 262422756, 'text': mapcss.tr(u'{0} is deprecated', capture_tags, u'{0.tag}'), 'fix': {
                '+': dict([
                    [u'operator',u'Enedis']])
            }})

        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][inside("DE,AT")]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_5b84a257, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and not mapcss.regexp_test_(self.re_559797c8, mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'DE,AT')) or \
            (mapcss.regexp_test_(self.re_5b84a257, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss.regexp_test_(self.re_559797c8, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'DE,AT'))):
            # throwError:tr("street name contains ss")
            err.append({'class': 9009002, 'subclass': 821908491, 'text': mapcss.tr(u'street name contains ss', capture_tags)})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_3d3faeb5, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'LI,CH')) or \
            (mapcss.regexp_test_(self.re_3d3faeb5, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'LI,CH'))):
            # throwError:tr("street name contains ß")
            err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr(u'street name contains ß', capture_tags)})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[operator=ERDF][inside("FR")]
        if (u'operator' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'operator') == u'ERDF' and mapcss.inside(self.father.config.options, u'FR'))):
            # group:tr("deprecated tagging")
            # throwWarning:tr("{0} is deprecated","{0.tag}")
            # suggestAlternative:"operator=Enedis"
            # fixAdd:"operator=Enedis"
            err.append({'class': 9009001, 'subclass': 262422756, 'text': mapcss.tr(u'{0} is deprecated', capture_tags, u'{0.tag}'), 'fix': {
                '+': dict([
                    [u'operator',u'Enedis']])
            }})

        # *[addr:street=~/(?i).*Strasse.*/][addr:street!~/(?i).*Strasser.*/][inside("DE,AT")]
        # *[name=~/(?i).*Strasse.*/][name!~/(?i).*Strasser.*/][inside("DE,AT")]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_5b84a257, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and not mapcss.regexp_test_(self.re_559797c8, mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'DE,AT')) or \
            (mapcss.regexp_test_(self.re_5b84a257, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss.regexp_test_(self.re_559797c8, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'DE,AT'))):
            # throwError:tr("street name contains ss")
            err.append({'class': 9009002, 'subclass': 821908491, 'text': mapcss.tr(u'street name contains ss', capture_tags)})

        # *[addr:street=~/(?i).*Straße.*/][inside("LI,CH")]
        # *[name=~/(?i).*Straße.*/][inside("LI,CH")]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_3d3faeb5, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'LI,CH')) or \
            (mapcss.regexp_test_(self.re_3d3faeb5, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'LI,CH'))):
            # throwError:tr("street name contains ß")
            err.append({'class': 9009003, 'subclass': 610086334, 'text': mapcss.tr(u'street name contains ß', capture_tags)})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_territories(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


