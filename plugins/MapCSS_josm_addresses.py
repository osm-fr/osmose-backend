#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_addresses(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9000001] = {'item': 9000, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'Way with {0}. Tag each housenumber separately if possible.', capture_tags, u'{0.key}')}
        self.errors[9000002] = {'item': 9000, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'Object has no {0}, however, it has {1} and {2} whose value looks like a housenumber.', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')}
        self.errors[9000003] = {'item': 9000, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Same value of {0} and {1}', capture_tags, u'{0.key}', u'{1.key}')}

        self.re_429c332e = re.compile(ur'^[0-9]+[a-zA-Z]?$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[!addr:housenumber][addr:street][addr:housename=~/^[0-9]+[a-zA-Z]?$/]
        if (u'addr:street' in keys) and \
            ((not mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:street') and mapcss.regexp_test_(self.re_429c332e, mapcss._tag_capture(capture_tags, 2, tags, u'addr:housename')))):
            # throwOther:tr("Object has no {0}, however, it has {1} and {2} whose value looks like a housenumber.","{0.key}","{1.key}","{2.key}")
            # assertNoMatch:"node addr:housename=1"
            # assertNoMatch:"node addr:street=foo addr:housename=1 addr:housenumber=1"
            # assertMatch:"node addr:street=foo addr:housename=1"
            # assertMatch:"node addr:street=foo addr:housename=1a"
            # assertMatch:"node addr:street=foo addr:housename=221B"
            # assertNoMatch:"node addr:street=foo addr:housename=bar"
            err.append({'class': 9000002, 'subclass': 1929266742, 'text': mapcss.tr(u'Object has no {0}, however, it has {1} and {2} whose value looks like a housenumber.', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')})

        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housenumber' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss.tag(tags, u'addr:housename'))):
            # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
            # assertMatch:"node addr:housename=1 addr:housenumber=1"
            # assertNoMatch:"node addr:housename=1 addr:housenumber=2"
            err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', capture_tags, u'{0.key}', u'{1.key}')})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[addr:interpolation]
        if (u'addr:interpolation' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:interpolation'))):
            # throwOther:tr("Way with {0}. Tag each housenumber separately if possible.","{0.key}")
            err.append({'class': 9000001, 'subclass': 1264784897, 'text': mapcss.tr(u'Way with {0}. Tag each housenumber separately if possible.', capture_tags, u'{0.key}')})

        # *[!addr:housenumber][addr:street][addr:housename=~/^[0-9]+[a-zA-Z]?$/]
        if (u'addr:street' in keys) and \
            ((not mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:street') and mapcss.regexp_test_(self.re_429c332e, mapcss._tag_capture(capture_tags, 2, tags, u'addr:housename')))):
            # throwOther:tr("Object has no {0}, however, it has {1} and {2} whose value looks like a housenumber.","{0.key}","{1.key}","{2.key}")
            err.append({'class': 9000002, 'subclass': 1929266742, 'text': mapcss.tr(u'Object has no {0}, however, it has {1} and {2} whose value looks like a housenumber.', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')})

        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housenumber' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss.tag(tags, u'addr:housename'))):
            # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
            err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', capture_tags, u'{0.key}', u'{1.key}')})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[!addr:housenumber][addr:street][addr:housename=~/^[0-9]+[a-zA-Z]?$/]
        if (u'addr:street' in keys) and \
            ((not mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:street') and mapcss.regexp_test_(self.re_429c332e, mapcss._tag_capture(capture_tags, 2, tags, u'addr:housename')))):
            # throwOther:tr("Object has no {0}, however, it has {1} and {2} whose value looks like a housenumber.","{0.key}","{1.key}","{2.key}")
            err.append({'class': 9000002, 'subclass': 1929266742, 'text': mapcss.tr(u'Object has no {0}, however, it has {1} and {2} whose value looks like a housenumber.', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')})

        # *[addr:housenumber][addr:housename]["addr:housenumber"=*"addr:housename"]
        if (u'addr:housenumber' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:housename') and mapcss._tag_capture(capture_tags, 2, tags, u'addr:housenumber') == mapcss.tag(tags, u'addr:housename'))):
            # throwWarning:tr("Same value of {0} and {1}","{0.key}","{1.key}")
            err.append({'class': 9000003, 'subclass': 1820984183, 'text': mapcss.tr(u'Same value of {0} and {1}', capture_tags, u'{0.key}', u'{1.key}')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_addresses(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {u'addr:housename': u'1'}), expected={'class': 9000002, 'subclass': 1929266742})
        self.check_not_err(n.node(data, {u'addr:housename': u'1', u'addr:housenumber': u'1', u'addr:street': u'foo'}), expected={'class': 9000002, 'subclass': 1929266742})
        self.check_err(n.node(data, {u'addr:housename': u'1', u'addr:street': u'foo'}), expected={'class': 9000002, 'subclass': 1929266742})
        self.check_err(n.node(data, {u'addr:housename': u'1a', u'addr:street': u'foo'}), expected={'class': 9000002, 'subclass': 1929266742})
        self.check_err(n.node(data, {u'addr:housename': u'221B', u'addr:street': u'foo'}), expected={'class': 9000002, 'subclass': 1929266742})
        self.check_not_err(n.node(data, {u'addr:housename': u'bar', u'addr:street': u'foo'}), expected={'class': 9000002, 'subclass': 1929266742})
        self.check_err(n.node(data, {u'addr:housename': u'1', u'addr:housenumber': u'1'}), expected={'class': 9000003, 'subclass': 1820984183})
        self.check_not_err(n.node(data, {u'addr:housename': u'1', u'addr:housenumber': u'2'}), expected={'class': 9000003, 'subclass': 1820984183})
