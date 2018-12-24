#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_ru_housenumber(Plugin):

    only_for = ['RU']


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9017001] = {'item': 9017, 'level': 3, 'tag': ["tag", "addr"], 'desc': mapcss.tr(u'Номера домов не соответствующие принятому соглашению')}

        self.re_62d22c1b = re.compile(ur'^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housenumber!~/^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$/]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_62d22c1b), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Номера домов не соответствующие принятому соглашению")
                err.append({'class': 9017001, 'subclass': 774061168, 'text': mapcss.tr(u'Номера домов не соответствующие принятому соглашению')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housenumber!~/^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$/]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_62d22c1b), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Номера домов не соответствующие принятому соглашению")
                err.append({'class': 9017001, 'subclass': 774061168, 'text': mapcss.tr(u'Номера домов не соответствующие принятому соглашению')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housenumber!~/^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$/]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_62d22c1b), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Номера домов не соответствующие принятому соглашению")
                err.append({'class': 9017001, 'subclass': 774061168, 'text': mapcss.tr(u'Номера домов не соответствующие принятому соглашению')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_ru_housenumber(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


