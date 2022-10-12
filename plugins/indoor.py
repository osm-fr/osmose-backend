#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class indoor(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[50] = self.def_class(item = 1300, level = 3, tags = mapcss.list_('indoor', 'geom') + mapcss.list_('fix:survey'), title = mapcss.tr('This indoor feature should be a closed and valid polygon'))
        self.errors[51] = self.def_class(item = 1300, level = 3, tags = mapcss.list_('indoor', 'geom') + mapcss.list_('fix:survey'), title = mapcss.tr('This indoor feature should have a level'))
        self.errors[52] = self.def_class(item = 1300, level = 3, tags = mapcss.list_('indoor', 'geom') + mapcss.list_('fix:survey', 'shop'), title = mapcss.tr('This indoor shop should probably be inside a room'))

        self.re_2a047336 = re.compile(r'room|corridor|area|level')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # node[indoor=~/room|corridor|area|level/][inside("DE,CH,FR")]
        # node[room][inside("DE,CH,FR")]
        if ('indoor' in keys) or ('room' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2a047336), mapcss._tag_capture(capture_tags, 0, tags, 'indoor'))) and (mapcss.inside(self.father.config.options, 'DE,CH,FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'room')) and (mapcss.inside(self.father.config.options, 'DE,CH,FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:survey")
                # -osmoseItemClassLevel:"1300/50/3"
                # throwError:tr("This indoor feature should be a closed and valid polygon")
                # -osmoseAssertMatchWithContext:list("node indoor=room","inside=FR")
                # -osmoseAssertMatchWithContext:list("node room=shop","inside=DE")
                err.append({'class': 50, 'subclass': 0, 'text': mapcss.tr('This indoor feature should be a closed and valid polygon')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way!:closed[indoor=~/room|corridor|area|level/][inside("DE,CH,FR")]
        # way!:closed[room][inside("DE,CH,FR")]
        if ('indoor' in keys) or ('room' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2a047336), mapcss._tag_capture(capture_tags, 1, tags, 'indoor'))) and (mapcss.inside(self.father.config.options, 'DE,CH,FR')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 1, tags, 'room')) and (mapcss.inside(self.father.config.options, 'DE,CH,FR')) and (nds[0] != nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:survey")
                # -osmoseItemClassLevel:"1300/50/3"
                # throwError:tr("This indoor feature should be a closed and valid polygon")
                err.append({'class': 50, 'subclass': 0, 'text': mapcss.tr('This indoor feature should be a closed and valid polygon')})

        # way:closed[indoor=~/room|corridor|area|level/][!level][inside("DE,CH,FR")]
        if ('indoor' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2a047336), mapcss._tag_capture(capture_tags, 1, tags, 'indoor'))) and (not mapcss._tag_capture(capture_tags, 2, tags, 'level')) and (mapcss.inside(self.father.config.options, 'DE,CH,FR')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:survey")
                # -osmoseItemClassLevel:"1300/51/3"
                # throwWarning:tr("This indoor feature should have a level")
                # -osmoseAssertNoMatchWithContext:list("way indoor=room level=-0.5","inside=DE")
                # -osmoseAssertMatchWithContext:list("way indoor=room room=shop","inside=FR")
                err.append({'class': 51, 'subclass': 0, 'text': mapcss.tr('This indoor feature should have a level')})

        # way:closed[indoor=area][shop][inside("DE,CH,FR")]
        # way:closed[indoor=corridor][shop][inside("DE,CH,FR")]
        if ('indoor' in keys and 'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 1, tags, 'indoor') == mapcss._value_capture(capture_tags, 1, 'area')) and (mapcss._tag_capture(capture_tags, 2, tags, 'shop')) and (mapcss.inside(self.father.config.options, 'DE,CH,FR')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 1, tags, 'indoor') == mapcss._value_capture(capture_tags, 1, 'corridor')) and (mapcss._tag_capture(capture_tags, 2, tags, 'shop')) and (mapcss.inside(self.father.config.options, 'DE,CH,FR')) and (nds[0] == nds[-1]))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("fix:survey","shop")
                # -osmoseItemClassLevel:"1300/52/3"
                # throwWarning:tr("This indoor shop should probably be inside a room")
                # fixAdd:"indoor=room"
                # -osmoseAssertMatchWithContext:list("way indoor=area shop=florist level=3","inside=DE")
                # -osmoseAssertMatchWithContext:list("way indoor=corridor shop=tickets","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way indoor=room room=shop shop=florist","inside=DE")
                err.append({'class': 52, 'subclass': 0, 'text': mapcss.tr('This indoor shop should probably be inside a room'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['indoor','room']])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = indoor(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'indoor': 'room'}), expected={'class': 50, 'subclass': 0})
        with with_options(n, {'country': 'DE'}):
            self.check_err(n.node(data, {'room': 'shop'}), expected={'class': 50, 'subclass': 0})
        with with_options(n, {'country': 'DE'}):
            self.check_not_err(n.way(data, {'indoor': 'room', 'level': '-0.5'}, [0]), expected={'class': 51, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'indoor': 'room', 'room': 'shop'}, [0]), expected={'class': 51, 'subclass': 0})
        with with_options(n, {'country': 'DE'}):
            self.check_err(n.way(data, {'indoor': 'area', 'level': '3', 'shop': 'florist'}, [0]), expected={'class': 52, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'indoor': 'corridor', 'shop': 'tickets'}, [0]), expected={'class': 52, 'subclass': 0})
        with with_options(n, {'country': 'DE'}):
            self.check_not_err(n.way(data, {'indoor': 'room', 'room': 'shop', 'shop': 'florist'}, [0]), expected={'class': 52, 'subclass': 0})
