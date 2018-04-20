#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class Josm_ru_housenumber(Plugin):

    only_for = ['RU']


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9017001] = {'item': 9017, 'level': 3, 'tag': ["tag", "addr"], 'desc': mapcss.tr(u'Номера домов не соответствующие принятому соглашению', capture_tags)}

        self.re_62d22c1b = re.compile(ur'^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housenumber!~/^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$/]
        if u'addr:housenumber' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_62d22c1b), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Номера домов не соответствующие принятому соглашению")
                err.append({'class': 9017001, 'subclass': 774061168, 'text': mapcss.tr(u'Номера домов не соответствующие принятому соглашению', capture_tags)})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housenumber!~/^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$/]
        if u'addr:housenumber' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_62d22c1b), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Номера домов не соответствующие принятому соглашению")
                err.append({'class': 9017001, 'subclass': 774061168, 'text': mapcss.tr(u'Номера домов не соответствующие принятому соглашению', capture_tags)})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[addr:housenumber][addr:housenumber!~/^((?:вл)?[0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?(?: к[0-9А-Я]+)?(?: с[0-9А-Я]+)?(?: соор[0-9А-Я]+)?(?: лит[0-9А-Я]+)?(?: фл[0-9А-Я]+)?|[0-9]+-[0-9]+|[0-9]+[А-Я]?[\/-][0-9]+[А-Я]?[\/-][0-9]+[А-Я]?|(([0-9]+[А-Я]?[IXV]*)|[IXV]*)[\/-]([0-9]+[А-Я]?|[IXV]*)|ЗЯБ-[0-9]+|С-([0-9]+[А-Я]?(?:\/[0-9]+[А-Я]?)?|[IXV]*)|к[0-9А-Я]+)$/]
        if u'addr:housenumber' in keys:
            match = False
            try: match = match or ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_62d22c1b), mapcss._tag_capture(capture_tags, 1, tags, u'addr:housenumber'))))
            except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("Номера домов не соответствующие принятому соглашению")
                err.append({'class': 9017001, 'subclass': 774061168, 'text': mapcss.tr(u'Номера домов не соответствующие принятому соглашению', capture_tags)})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_ru_housenumber(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


