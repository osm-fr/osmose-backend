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
        self.errors[53] = self.def_class(item = 1300, level = 2, tags = mapcss.list_('indoor', 'geom'), title = mapcss.tr('This indoor room should have a door'))
        self.errors[21201] = self.def_class(item = 2120, level = 3, tags = mapcss.list_('indoor', 'geom'), title = mapcss.tr('`{0}` without `{1}` or `{2}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}')))
        self.errors[21202] = self.def_class(item = 2120, level = 3, tags = mapcss.list_('indoor', 'geom'), title = mapcss.tr('`{0}` without `{1}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), trap = mapcss.tr('For the number of rooms in a facility, use `{0}` instead.', 'rooms=*'))

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

        # *[indoor][!level][!repeat_on][indoor!=yes][indoor!=no]
        if ('indoor' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'indoor')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'level')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'repeat_on')) and (mapcss._tag_capture(capture_tags, 3, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 3, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 4, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2120/21201:1/3"
                # throwWarning:tr("`{0}` without `{1}` or `{2}`","{0.tag}","{1.key}","{2.key}")
                # assertMatch:"node indoor=room"
                err.append({'class': 21201, 'subclass': 1, 'text': mapcss.tr('`{0}` without `{1}` or `{2}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *[room][!indoor][!buildingpart]
        if ('room' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'room')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'indoor')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'buildingpart')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTrap:tr("For the number of rooms in a facility, use `{0}` instead.","rooms=*")
                # -osmoseItemClassLevel:"2120/21202:2/3"
                # throwWarning:tr("`{0}` without `{1}`","{0.tag}","{1.key}")
                # fixAdd:"indoor=room"
                # assertMatch:"node room=office"
                err.append({'class': 21202, 'subclass': 2, 'text': mapcss.tr('`{0}` without `{1}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['indoor','room']])
                }})

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

        # area[indoor=room][access!~/no|private/]!.room_with_door
        if ('indoor' in keys):
            match = False
            # Skip selector using undeclared class room_with_door
            if match:
                # -osmoseItemClassLevel:"1300/53/2"
                # throwError:tr("This indoor room should have a door")
                err.append({'class': 53, 'subclass': 0, 'text': mapcss.tr('This indoor room should have a door')})

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

        # *[indoor][!level][!repeat_on][indoor!=yes][indoor!=no]
        if ('indoor' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'indoor')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'level')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'repeat_on')) and (mapcss._tag_capture(capture_tags, 3, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 3, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 4, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2120/21201:1/3"
                # throwWarning:tr("`{0}` without `{1}` or `{2}`","{0.tag}","{1.key}","{2.key}")
                err.append({'class': 21201, 'subclass': 1, 'text': mapcss.tr('`{0}` without `{1}` or `{2}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *[room][!indoor][!buildingpart]
        if ('room' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'room')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'indoor')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'buildingpart')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTrap:tr("For the number of rooms in a facility, use `{0}` instead.","rooms=*")
                # -osmoseItemClassLevel:"2120/21202:2/3"
                # throwWarning:tr("`{0}` without `{1}`","{0.tag}","{1.key}")
                # fixAdd:"indoor=room"
                err.append({'class': 21202, 'subclass': 2, 'text': mapcss.tr('`{0}` without `{1}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['indoor','room']])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # area[indoor=room][access!~/no|private/]!.room_with_door
        if ('indoor' in keys and 'type' in keys):
            match = False
            # Skip selector using undeclared class room_with_door
            if match:
                # -osmoseItemClassLevel:"1300/53/2"
                # throwError:tr("This indoor room should have a door")
                err.append({'class': 53, 'subclass': 0, 'text': mapcss.tr('This indoor room should have a door')})

        # *[indoor][!level][!repeat_on][indoor!=yes][indoor!=no]
        if ('indoor' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'indoor')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'level')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'repeat_on')) and (mapcss._tag_capture(capture_tags, 3, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 3, 'yes', 'yes')) and (mapcss._tag_capture(capture_tags, 4, tags, 'indoor') != mapcss._value_const_capture(capture_tags, 4, 'no', 'no')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseItemClassLevel:"2120/21201:1/3"
                # throwWarning:tr("`{0}` without `{1}` or `{2}`","{0.tag}","{1.key}","{2.key}")
                err.append({'class': 21201, 'subclass': 1, 'text': mapcss.tr('`{0}` without `{1}` or `{2}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{2.key}'))})

        # *[room][!indoor][!buildingpart]
        if ('room' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'room')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'indoor')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'buildingpart')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTrap:tr("For the number of rooms in a facility, use `{0}` instead.","rooms=*")
                # -osmoseItemClassLevel:"2120/21202:2/3"
                # throwWarning:tr("`{0}` without `{1}`","{0.tag}","{1.key}")
                # fixAdd:"indoor=room"
                err.append({'class': 21202, 'subclass': 2, 'text': mapcss.tr('`{0}` without `{1}`', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['indoor','room']])
                }})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
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
        self.check_err(n.node(data, {'indoor': 'room'}), expected={'class': 21201, 'subclass': 1})
        self.check_err(n.node(data, {'room': 'office'}), expected={'class': 21202, 'subclass': 2})
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
