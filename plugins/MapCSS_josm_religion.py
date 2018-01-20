#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_religion(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9008001] = {'item': 9008, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'missing tag', capture_tags)}
        self.errors[9008002] = {'item': 9008, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'unknown christian denomination', capture_tags)}
        self.errors[9008003] = {'item': 9008, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'unknown muslim denomination', capture_tags)}
        self.errors[9008004] = {'item': 9008, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'unknown jewish denomination', capture_tags)}

        self.re_3937f042 = re.compile(ur'^(alaouite|druze|ibadi|ismaili|nondenominational|shia|sunni)$')
        self.re_45d9ca87 = re.compile(ur'^(anglican|apostolic|baptist|catholic|christian_community|christian_scientist|coptic_orthodox|czechoslovak_hussite|dutch_reformed|evangelical|foursquare|greek_catholic|greek_orthodox|jehovahs_witness|kabbalah|karaite|living_waters_church|lutheran|maronite|mennonite|methodist|mormon|new_apostolic|nondenominational|old_catholic|orthodox|pentecostal|presbyterian|protestant|quaker|roman_catholic|russian_orthodox|salvation_army|serbian_orthodox|seventh_day_adventist|spiritist|united|united_reformed|uniting)$')
        self.re_735596a1 = re.compile(ur'^(christian|jewish|muslim)$')
        self.re_7dfe4b2d = re.compile(ur'^(alternative|ashkenazi|conservative|hasidic|humanistic|liberal|modern_orthodox|neo_orthodox|nondenominational|orthodox|progressive|reconstructionist|reform|renewal|samaritan|ultra_orthodox)$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=~/^(christian|jewish|muslim)$/][!denomination][type!=route]
        if (u'religion' in keys) and \
            ((mapcss.regexp_test_(self.re_735596a1, mapcss._tag_capture(capture_tags, 0, tags, u'religion')) and not mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and mapcss._tag_capture(capture_tags, 2, tags, u'type') != u'route')):
            # group:tr("missing tag")
            # throwOther:tr("religion without denomination")
            # assertNoMatch:"node religion=christian denomination=catholic"
            # assertMatch:"node religion=christian"
            # assertNoMatch:"node religion=foobar"
            err.append({'class': 9008001, 'subclass': 126464904, 'text': mapcss.tr(u'religion without denomination', capture_tags)})

        # *[religion=christian][denomination][denomination!~/^(anglican|apostolic|baptist|catholic|christian_community|christian_scientist|coptic_orthodox|czechoslovak_hussite|dutch_reformed|evangelical|foursquare|greek_catholic|greek_orthodox|jehovahs_witness|kabbalah|karaite|living_waters_church|lutheran|maronite|mennonite|methodist|mormon|new_apostolic|nondenominational|old_catholic|orthodox|pentecostal|presbyterian|protestant|quaker|roman_catholic|russian_orthodox|salvation_army|serbian_orthodox|seventh_day_adventist|spiritist|united|united_reformed|uniting)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'christian' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_45d9ca87, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown christian denomination")
            # assertNoMatch:"node religion=christian denomination=catholic"
            # assertMatch:"node religion=christian denomination=foobar"
            # assertNoMatch:"node religion=christian"
            err.append({'class': 9008002, 'subclass': 136607579, 'text': mapcss.tr(u'unknown christian denomination', capture_tags)})

        # *[religion=muslim][denomination][denomination!~/^(alaouite|druze|ibadi|ismaili|nondenominational|shia|sunni)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'muslim' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_3937f042, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown muslim denomination")
            # assertNoMatch:"node religion=muslim denomination=alaouite"
            # assertMatch:"node religion=muslim denomination=foobar"
            # assertNoMatch:"node religion=muslim"
            err.append({'class': 9008003, 'subclass': 1080497449, 'text': mapcss.tr(u'unknown muslim denomination', capture_tags)})

        # *[religion=jewish][denomination][denomination!~/^(alternative|ashkenazi|conservative|hasidic|humanistic|liberal|modern_orthodox|neo_orthodox|nondenominational|orthodox|progressive|reconstructionist|reform|renewal|samaritan|ultra_orthodox)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'jewish' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_7dfe4b2d, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown jewish denomination")
            # assertNoMatch:"node religion=jewish denomination=alternative"
            # assertMatch:"node religion=jewish denomination=foobar"
            # assertNoMatch:"node religion=jewish"
            err.append({'class': 9008004, 'subclass': 1543128846, 'text': mapcss.tr(u'unknown jewish denomination', capture_tags)})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=~/^(christian|jewish|muslim)$/][!denomination][type!=route]
        if (u'religion' in keys) and \
            ((mapcss.regexp_test_(self.re_735596a1, mapcss._tag_capture(capture_tags, 0, tags, u'religion')) and not mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and mapcss._tag_capture(capture_tags, 2, tags, u'type') != u'route')):
            # group:tr("missing tag")
            # throwOther:tr("religion without denomination")
            err.append({'class': 9008001, 'subclass': 126464904, 'text': mapcss.tr(u'religion without denomination', capture_tags)})

        # *[religion=christian][denomination][denomination!~/^(anglican|apostolic|baptist|catholic|christian_community|christian_scientist|coptic_orthodox|czechoslovak_hussite|dutch_reformed|evangelical|foursquare|greek_catholic|greek_orthodox|jehovahs_witness|kabbalah|karaite|living_waters_church|lutheran|maronite|mennonite|methodist|mormon|new_apostolic|nondenominational|old_catholic|orthodox|pentecostal|presbyterian|protestant|quaker|roman_catholic|russian_orthodox|salvation_army|serbian_orthodox|seventh_day_adventist|spiritist|united|united_reformed|uniting)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'christian' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_45d9ca87, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown christian denomination")
            err.append({'class': 9008002, 'subclass': 136607579, 'text': mapcss.tr(u'unknown christian denomination', capture_tags)})

        # *[religion=muslim][denomination][denomination!~/^(alaouite|druze|ibadi|ismaili|nondenominational|shia|sunni)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'muslim' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_3937f042, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown muslim denomination")
            err.append({'class': 9008003, 'subclass': 1080497449, 'text': mapcss.tr(u'unknown muslim denomination', capture_tags)})

        # *[religion=jewish][denomination][denomination!~/^(alternative|ashkenazi|conservative|hasidic|humanistic|liberal|modern_orthodox|neo_orthodox|nondenominational|orthodox|progressive|reconstructionist|reform|renewal|samaritan|ultra_orthodox)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'jewish' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_7dfe4b2d, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown jewish denomination")
            err.append({'class': 9008004, 'subclass': 1543128846, 'text': mapcss.tr(u'unknown jewish denomination', capture_tags)})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[religion=~/^(christian|jewish|muslim)$/][!denomination][type!=route]
        if (u'religion' in keys) and \
            ((mapcss.regexp_test_(self.re_735596a1, mapcss._tag_capture(capture_tags, 0, tags, u'religion')) and not mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and mapcss._tag_capture(capture_tags, 2, tags, u'type') != u'route')):
            # group:tr("missing tag")
            # throwOther:tr("religion without denomination")
            err.append({'class': 9008001, 'subclass': 126464904, 'text': mapcss.tr(u'religion without denomination', capture_tags)})

        # *[religion=christian][denomination][denomination!~/^(anglican|apostolic|baptist|catholic|christian_community|christian_scientist|coptic_orthodox|czechoslovak_hussite|dutch_reformed|evangelical|foursquare|greek_catholic|greek_orthodox|jehovahs_witness|kabbalah|karaite|living_waters_church|lutheran|maronite|mennonite|methodist|mormon|new_apostolic|nondenominational|old_catholic|orthodox|pentecostal|presbyterian|protestant|quaker|roman_catholic|russian_orthodox|salvation_army|serbian_orthodox|seventh_day_adventist|spiritist|united|united_reformed|uniting)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'christian' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_45d9ca87, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown christian denomination")
            err.append({'class': 9008002, 'subclass': 136607579, 'text': mapcss.tr(u'unknown christian denomination', capture_tags)})

        # *[religion=muslim][denomination][denomination!~/^(alaouite|druze|ibadi|ismaili|nondenominational|shia|sunni)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'muslim' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_3937f042, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown muslim denomination")
            err.append({'class': 9008003, 'subclass': 1080497449, 'text': mapcss.tr(u'unknown muslim denomination', capture_tags)})

        # *[religion=jewish][denomination][denomination!~/^(alternative|ashkenazi|conservative|hasidic|humanistic|liberal|modern_orthodox|neo_orthodox|nondenominational|orthodox|progressive|reconstructionist|reform|renewal|samaritan|ultra_orthodox)$/]
        if (u'religion' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'religion') == u'jewish' and mapcss._tag_capture(capture_tags, 1, tags, u'denomination') and not mapcss.regexp_test_(self.re_7dfe4b2d, mapcss._tag_capture(capture_tags, 2, tags, u'denomination')))):
            # throwOther:tr("unknown jewish denomination")
            err.append({'class': 9008004, 'subclass': 1543128846, 'text': mapcss.tr(u'unknown jewish denomination', capture_tags)})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_religion(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {u'denomination': u'catholic', u'religion': u'christian'}), expected={'class': 9008001, 'subclass': 126464904})
        self.check_err(n.node(data, {u'religion': u'christian'}), expected={'class': 9008001, 'subclass': 126464904})
        self.check_not_err(n.node(data, {u'religion': u'foobar'}), expected={'class': 9008001, 'subclass': 126464904})
        self.check_not_err(n.node(data, {u'denomination': u'catholic', u'religion': u'christian'}), expected={'class': 9008002, 'subclass': 136607579})
        self.check_err(n.node(data, {u'denomination': u'foobar', u'religion': u'christian'}), expected={'class': 9008002, 'subclass': 136607579})
        self.check_not_err(n.node(data, {u'religion': u'christian'}), expected={'class': 9008002, 'subclass': 136607579})
        self.check_not_err(n.node(data, {u'denomination': u'alaouite', u'religion': u'muslim'}), expected={'class': 9008003, 'subclass': 1080497449})
        self.check_err(n.node(data, {u'denomination': u'foobar', u'religion': u'muslim'}), expected={'class': 9008003, 'subclass': 1080497449})
        self.check_not_err(n.node(data, {u'religion': u'muslim'}), expected={'class': 9008003, 'subclass': 1080497449})
        self.check_not_err(n.node(data, {u'denomination': u'alternative', u'religion': u'jewish'}), expected={'class': 9008004, 'subclass': 1543128846})
        self.check_err(n.node(data, {u'denomination': u'foobar', u'religion': u'jewish'}), expected={'class': 9008004, 'subclass': 1543128846})
        self.check_not_err(n.node(data, {u'religion': u'jewish'}), expected={'class': 9008004, 'subclass': 1543128846})
