#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Phone2(PluginMapCSS):



    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[3097] = self.def_class(item = 3092, level = 2, tags = mapcss.list_('tag'), title = mapcss.tr('Different value of tag contact:* and *'))



    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[phone][contact:phone][replace(replace(tag("contact:phone"),"-","")," ","")!=replace(replace(tag("phone"),"-","")," ","")]
        # *[fax][contact:fax][replace(replace(tag("contact:fax"),"-","")," ","")!=replace(replace(tag("fax"),"-","")," ","")]
        # *[mobile][contact:mobile][replace(replace(tag("contact:mobile"),"-","")," ","")!=replace(replace(tag("mobile"),"-","")," ","")]
        # *[instagram][contact:instagram][contact:instagram!=*instagram]
        # *[facebook][contact:facebook][contact:facebook!=*facebook]
        # *[email][contact:email][contact:email!=*email]
        # *[website][contact:website][contact:website!=*website]
        if ('contact:email' in keys and 'email' in keys) or ('contact:facebook' in keys and 'facebook' in keys) or ('contact:fax' in keys and 'fax' in keys) or ('contact:instagram' in keys and 'instagram' in keys) or ('contact:mobile' in keys and 'mobile' in keys) or ('contact:phone' in keys and 'phone' in keys) or ('contact:website' in keys and 'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'phone')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:phone')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:phone'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'phone'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fax')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:fax')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:fax'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'fax'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mobile')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:mobile')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:mobile'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'mobile'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'instagram')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:instagram')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:instagram') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'instagram'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'facebook')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:facebook')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:facebook') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'facebook'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'email')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:email')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:email') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'email'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'website')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:website')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:website') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'website'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Different value of tag contact:* and *")
                # -osmoseItemClassLevel:"3092/3097/2"
                # throwWarning:tr("Different values of {0} and of {1}","{0.key}","{1.key}")
                # assertNoMatch:"node phone=\"+31 123-456 789\" contact:phone=\"+31123456789\""
                # assertMatch:"node phone=1 contact:phone=2"
                # assertNoMatch:"node website=1 contact:website=1"
                err.append({'class': 3097, 'subclass': 0, 'text': mapcss.tr('Different values of {0} and of {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[phone][contact:phone][replace(replace(tag("contact:phone"),"-","")," ","")!=replace(replace(tag("phone"),"-","")," ","")]
        # *[fax][contact:fax][replace(replace(tag("contact:fax"),"-","")," ","")!=replace(replace(tag("fax"),"-","")," ","")]
        # *[mobile][contact:mobile][replace(replace(tag("contact:mobile"),"-","")," ","")!=replace(replace(tag("mobile"),"-","")," ","")]
        # *[instagram][contact:instagram][contact:instagram!=*instagram]
        # *[facebook][contact:facebook][contact:facebook!=*facebook]
        # *[email][contact:email][contact:email!=*email]
        # *[website][contact:website][contact:website!=*website]
        if ('contact:email' in keys and 'email' in keys) or ('contact:facebook' in keys and 'facebook' in keys) or ('contact:fax' in keys and 'fax' in keys) or ('contact:instagram' in keys and 'instagram' in keys) or ('contact:mobile' in keys and 'mobile' in keys) or ('contact:phone' in keys and 'phone' in keys) or ('contact:website' in keys and 'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'phone')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:phone')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:phone'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'phone'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fax')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:fax')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:fax'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'fax'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mobile')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:mobile')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:mobile'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'mobile'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'instagram')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:instagram')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:instagram') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'instagram'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'facebook')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:facebook')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:facebook') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'facebook'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'email')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:email')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:email') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'email'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'website')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:website')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:website') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'website'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Different value of tag contact:* and *")
                # -osmoseItemClassLevel:"3092/3097/2"
                # throwWarning:tr("Different values of {0} and of {1}","{0.key}","{1.key}")
                err.append({'class': 3097, 'subclass': 0, 'text': mapcss.tr('Different values of {0} and of {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[phone][contact:phone][replace(replace(tag("contact:phone"),"-","")," ","")!=replace(replace(tag("phone"),"-","")," ","")]
        # *[fax][contact:fax][replace(replace(tag("contact:fax"),"-","")," ","")!=replace(replace(tag("fax"),"-","")," ","")]
        # *[mobile][contact:mobile][replace(replace(tag("contact:mobile"),"-","")," ","")!=replace(replace(tag("mobile"),"-","")," ","")]
        # *[instagram][contact:instagram][contact:instagram!=*instagram]
        # *[facebook][contact:facebook][contact:facebook!=*facebook]
        # *[email][contact:email][contact:email!=*email]
        # *[website][contact:website][contact:website!=*website]
        if ('contact:email' in keys and 'email' in keys) or ('contact:facebook' in keys and 'facebook' in keys) or ('contact:fax' in keys and 'fax' in keys) or ('contact:instagram' in keys and 'instagram' in keys) or ('contact:mobile' in keys and 'mobile' in keys) or ('contact:phone' in keys and 'phone' in keys) or ('contact:website' in keys and 'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'phone')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:phone')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:phone'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'phone'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'fax')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:fax')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:fax'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'fax'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'mobile')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:mobile')) and (mapcss.replace(mapcss.replace(mapcss.tag(tags, 'contact:mobile'), '-', ''), ' ', '') != mapcss.replace(mapcss.replace(mapcss.tag(tags, 'mobile'), '-', ''), ' ', '')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'instagram')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:instagram')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:instagram') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'instagram'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'facebook')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:facebook')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:facebook') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'facebook'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'email')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:email')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:email') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'email'))))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'website')) and (mapcss._tag_capture(capture_tags, 1, tags, 'contact:website')) and (mapcss._tag_capture(capture_tags, 2, tags, 'contact:website') != mapcss._value_capture(capture_tags, 2, mapcss.tag(tags, 'website'))))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Different value of tag contact:* and *")
                # -osmoseItemClassLevel:"3092/3097/2"
                # throwWarning:tr("Different values of {0} and of {1}","{0.key}","{1.key}")
                err.append({'class': 3097, 'subclass': 0, 'text': mapcss.tr('Different values of {0} and of {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        return err


from plugins.PluginMapCSS import TestPluginMapcss


class Test(TestPluginMapcss):
    def test(self):
        n = Phone2(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_not_err(n.node(data, {'contact:phone': '+31123456789', 'phone': '+31 123-456 789'}), expected={'class': 3097, 'subclass': 0})
        self.check_err(n.node(data, {'contact:phone': '2', 'phone': '1'}), expected={'class': 3097, 'subclass': 0})
        self.check_not_err(n.node(data, {'contact:website': '1', 'website': '1'}), expected={'class': 3097, 'subclass': 0})
