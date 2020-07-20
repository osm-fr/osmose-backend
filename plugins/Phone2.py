#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Phone2(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[3097] = self.def_class(item = 3092, level = 2, tags = mapcss.list_(u'tag'), title = mapcss.tr(u'Different value of tag contact:* and *'))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[phone][contact:phone][contact:phone!=tag(phone)]
        # *[fax][contact:fax][contact:fax!=tag(fax)]
        # *[email][contact:email][contact:email!=tag(email)]
        # *[website][contact:website][contact:website!=tag(website)]
        if (u'contact:email' in keys and u'email' in keys) or (u'contact:fax' in keys and u'fax' in keys) or (u'contact:phone' in keys and u'phone' in keys) or (u'contact:website' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'phone') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:phone') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fax') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:fax') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:fax') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'fax')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'email') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:email') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:email') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'email')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'website') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:website') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:website') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'website')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Different value of tag contact:* and *")
                # -osmoseItemClassLevel:"3092/3097/2"
                # throwWarning:tr("Different values of {0} and of {1}","0.key","1.key")
                # assertMatch:"node phone=1 contact:phone=2"
                # assertNoMatch:"node website=1 contact:website=1"
                err.append({'class': 3097, 'subclass': 0, 'text': mapcss.tr(u'Different values of {0} and of {1}', u'0.key', u'1.key')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[phone][contact:phone][contact:phone!=tag(phone)]
        # *[fax][contact:fax][contact:fax!=tag(fax)]
        # *[email][contact:email][contact:email!=tag(email)]
        # *[website][contact:website][contact:website!=tag(website)]
        if (u'contact:email' in keys and u'email' in keys) or (u'contact:fax' in keys and u'fax' in keys) or (u'contact:phone' in keys and u'phone' in keys) or (u'contact:website' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'phone') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:phone') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fax') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:fax') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:fax') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'fax')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'email') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:email') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:email') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'email')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'website') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:website') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:website') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'website')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Different value of tag contact:* and *")
                # -osmoseItemClassLevel:"3092/3097/2"
                # throwWarning:tr("Different values of {0} and of {1}","0.key","1.key")
                err.append({'class': 3097, 'subclass': 0, 'text': mapcss.tr(u'Different values of {0} and of {1}', u'0.key', u'1.key')})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[phone][contact:phone][contact:phone!=tag(phone)]
        # *[fax][contact:fax][contact:fax!=tag(fax)]
        # *[email][contact:email][contact:email!=tag(email)]
        # *[website][contact:website][contact:website!=tag(website)]
        if (u'contact:email' in keys and u'email' in keys) or (u'contact:fax' in keys and u'fax' in keys) or (u'contact:phone' in keys and u'phone' in keys) or (u'contact:website' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'phone') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:phone') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'phone')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'fax') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:fax') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:fax') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'fax')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'email') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:email') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:email') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'email')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'website') and mapcss._tag_capture(capture_tags, 1, tags, u'contact:website') and mapcss._tag_capture(capture_tags, 2, tags, u'contact:website') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, u'website')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Different value of tag contact:* and *")
                # -osmoseItemClassLevel:"3092/3097/2"
                # throwWarning:tr("Different values of {0} and of {1}","0.key","1.key")
                err.append({'class': 3097, 'subclass': 0, 'text': mapcss.tr(u'Different values of {0} and of {1}', u'0.key', u'1.key')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Phone2(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'contact:phone': u'2', u'phone': u'1'}), expected={'class': 3097, 'subclass': 0})
        self.check_not_err(n.node(data, {u'contact:website': u'1', u'website': u'1'}), expected={'class': 3097, 'subclass': 0})
