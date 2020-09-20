#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_wikipedia(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/browser/josm/trunk/resources/data/validator/wikipedia.mapcss'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[9011001] = self.def_class(item = 9011, level = 2, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\''))
        self.errors[9011002] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia tag has an unknown language prefix'))
        self.errors[9011003] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('deprecated tagging'))
        self.errors[9011004] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', 'be-x-old', 'be-tarask'))
        self.errors[9011005] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', 'cz', 'cs'))
        self.errors[9011006] = self.def_class(item = 9011, level = 2, tags = ["tag", "wikipedia"], title = mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9011007] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia title should not start with a space after language code'))
        self.errors[9011008] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia title should not have \'\'{0}\'\' prefix', 'wiki/'))
        self.errors[9011009] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia page title should have first letter capitalized'))
        self.errors[9011010] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')'))
        self.errors[9011011] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('wikipedia language seems to be duplicated, e.g. en:en:Foo'))
        self.errors[9011012] = self.def_class(item = 9011, level = 2, tags = ["tag", "wikipedia"], title = mapcss.tr('wikidata tag must be in Qnnnn format, where n is a digit'))
        self.errors[9011015] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('\'\'{0}\'\' tag is set, but no \'\'{1}\'\' tag. Make sure to set \'\'wikipedia=language:value\'\' for the main article and optional \'\'wikipedia:language=value\'\' only for additional articles that are not just other language variants of the main article.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}')))
        self.errors[9011016] = self.def_class(item = 9011, level = 3, tags = ["tag", "wikipedia"], title = mapcss.tr('{0} value looks like a {1} value', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'wikidata'))

        self.re_034ab801 = re.compile(r'^cz:')
        self.re_04adb5d2 = re.compile(r'(?i).*%[0-9A-F][0-9A-F]')
        self.re_07f8e639 = re.compile(r'(?i)^[-a-z]{2,12}:')
        self.re_08b52119 = re.compile(r'(?i)^[-a-z]{2,12}:.*_')
        self.re_091c4afa = re.compile(r'(?i)^[-a-z]{2,12}:https?:\/\/')
        self.re_1559839b = re.compile(r'(?i)^([-a-z]+:)(.+)$')
        self.re_19995c46 = re.compile(r'(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]')
        self.re_1ac7f364 = re.compile(r'^jbo:')
        self.re_1f90813f = re.compile(r'^https?:\/\/')
        self.re_210c6ccc = re.compile(r'%[0-9A-F][0-9A-F]')
        self.re_294645af = re.compile(r'^(ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|atj|av|ay|az|azb|ba|ban|bar|bat-smg|bcl|be|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|din|diq|dsb|dty|dv|dz|ee|el|eml|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gcr|gd|gl|glk|gn|gom|gor|got|gu|gv|ha|hak|haw|he|hi|hif|hr|hsb|ht|hu|hy|hyw|ia|id|ie|ig|ik|ilo|inh|io|is|it|iu|ja|jam|jbo|jv|ka|kaa|kab|kbd|kbp|kg|ki|kk|kl|km|kn|ko|koi|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|mai|map-bms|mdf|mg|mhr|mi|min|mk|ml|mn|mnw|mr|mrj|ms|mt|mwl|my|myv|mzn|na|nah|nap|nds|nds-nl|ne|new|nl|nn|no|nov|nqo|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rw|sa|sah|sat|sc|scn|sco|sd|se|sg|sh|shn|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|szy|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|wa|war|wo|wuu|xal|xh|xmf|yi|yo|za|zea|zh|zh-classical|zh-min-nan|zh-yue|zu):')
        self.re_2a71e33b = re.compile(r'(?i)^([-a-z]+:)wiki/(.*)$')
        self.re_2d3d5d3d = re.compile(r'(?i)^[-a-z]{2,12}:https?:')
        self.re_2dd1bee3 = re.compile(r'^[-a-zA-Z]{2,12}:Q[1-9][0-9]{0,8}$')
        self.re_4b567f18 = re.compile(r'^Q[1-9][0-9]{0,8}$')
        self.re_536e5b67 = re.compile(r'(?i)^[-a-z]{2,12}: ')
        self.re_53b6f173 = re.compile(r'^be-x-old:')
        self.re_577ca7fb = re.compile(r'^cz:(.+)$')
        self.re_5940ff7c = re.compile(r'^[-a-zA-Z]{2,12}:\p{Ll}')
        self.re_62d51e93 = re.compile(r'(?i)^([-a-z]+:)([-a-z]+:)(.*)$')
        self.re_676bdf5d = re.compile(r'(?i)^([-a-z]+:)(.*)$')
        self.re_67c3b565 = re.compile(r'(?i)^[-a-z]{2,12}:wiki\/')
        self.re_6a4abd53 = re.compile(r'^be-x-old:(.+)$')
        self.re_6a7e1973 = re.compile(r'(?i)^([-a-z]+:)(.)(.*)$')
        self.re_79319bf9 = re.compile(r'^wikipedia:')
        self.re_79a96753 = re.compile(r'^wikipedia:[-a-z]{2,12}$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[wikipedia][wikipedia!~/(?i)^[-a-z]{2,12}:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_07f8e639, '(?i)^[-a-z]{2,12}:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wikipedia tag has no language given, use ''wikipedia''=''language:page title''")
                # assertMatch:"node wikipedia=Foobar"
                # assertNoMatch:"node wikipedia=en-GB:Foobar"
                # assertNoMatch:"node wikipedia=en:Foobar"
                err.append({'class': 9011001, 'subclass': 1517450396, 'text': mapcss.tr('wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\'')})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:/][wikipedia!~/^https?:\/\//][wikipedia!~/^(ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|atj|av|ay|az|azb|ba|ban|bar|bat-smg|bcl|be|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|din|diq|dsb|dty|dv|dz|ee|el|eml|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gcr|gd|gl|glk|gn|gom|gor|got|gu|gv|ha|hak|haw|he|hi|hif|hr|hsb|ht|hu|hy|hyw|ia|id|ie|ig|ik|ilo|inh|io|is|it|iu|ja|jam|jbo|jv|ka|kaa|kab|kbd|kbp|kg|ki|kk|kl|km|kn|ko|koi|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|mai|map-bms|mdf|mg|mhr|mi|min|mk|ml|mn|mnw|mr|mrj|ms|mt|mwl|my|myv|mzn|na|nah|nap|nds|nds-nl|ne|new|nl|nn|no|nov|nqo|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rw|sa|sah|sat|sc|scn|sco|sd|se|sg|sh|shn|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|szy|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|wa|war|wo|wuu|xal|xh|xmf|yi|yo|za|zea|zh|zh-classical|zh-min-nan|zh-yue|zu):/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_07f8e639), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1f90813f, '^https?:\/\/'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_294645af, '^(ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|atj|av|ay|az|azb|ba|ban|bar|bat-smg|bcl|be|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|din|diq|dsb|dty|dv|dz|ee|el|eml|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gcr|gd|gl|glk|gn|gom|gor|got|gu|gv|ha|hak|haw|he|hi|hif|hr|hsb|ht|hu|hy|hyw|ia|id|ie|ig|ik|ilo|inh|io|is|it|iu|ja|jam|jbo|jv|ka|kaa|kab|kbd|kbp|kg|ki|kk|kl|km|kn|ko|koi|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|mai|map-bms|mdf|mg|mhr|mi|min|mk|ml|mn|mnw|mr|mrj|ms|mt|mwl|my|myv|mzn|na|nah|nap|nds|nds-nl|ne|new|nl|nn|no|nov|nqo|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rw|sa|sah|sat|sc|scn|sco|sd|se|sg|sh|shn|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|szy|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|wa|war|wo|wuu|xal|xh|xmf|yi|yo|za|zea|zh|zh-classical|zh-min-nan|zh-yue|zu):'), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia tag has an unknown language prefix")
                # assertMatch:"node wikipedia=X-Y-Z:Foobar"
                # assertNoMatch:"node wikipedia=en:Foobar"
                err.append({'class': 9011002, 'subclass': 1358433348, 'text': mapcss.tr('wikipedia tag has an unknown language prefix')})

        # *[wikipedia=~/^https?:\/\//]
        # *[wikipedia=~/(?i)^[-a-z]{2,12}:https?:\/\//]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_1f90813f), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_091c4afa), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:tr("''wikipedia''=''language:page title''")
                # throwWarning:tr("wikipedia tag format is deprecated")
                # assertNoMatch:"node wikipedia=en:OpenStreetMap"
                # assertMatch:"node wikipedia=http://en.wikipedia.org/wiki/OpenStreetMap"
                err.append({'class': 9011003, 'subclass': 75691825, 'text': mapcss.tr('wikipedia tag format is deprecated')})

        # *[wikipedia=~/^be-x-old:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53b6f173), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia ''{0}'' language is obsolete, use ''{1}'' instead","be-x-old","be-tarask")
                # fixAdd:concat("wikipedia=be-tarask:",get(regexp_match("^be-x-old:(.+)$",tag("wikipedia")),1))
                # assertNoMatch:"node wikipedia=abe-x-old:foo"
                # assertMatch:"node wikipedia=be-x-old:foo"
                err.append({'class': 9011004, 'subclass': 616152609, 'text': mapcss.tr('wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', 'be-x-old', 'be-tarask'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=be-tarask:', mapcss.get(mapcss.regexp_match(self.re_6a4abd53, mapcss.tag(tags, 'wikipedia')), 1))).split('=', 1)])
                }})

        # *[wikipedia=~/^cz:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_034ab801), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia ''{0}'' language is invalid, use ''{1}'' instead","cz","cs")
                # fixAdd:concat("wikipedia=cs:",get(regexp_match("^cz:(.+)$",tag("wikipedia")),1))
                # assertMatch:"node wikipedia=cz:foo"
                # assertNoMatch:"node wikipedia=en:cz:foo"
                err.append({'class': 9011005, 'subclass': 243392039, 'text': mapcss.tr('wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', 'cz', 'cs'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=cs:', mapcss.get(mapcss.regexp_match(self.re_577ca7fb, mapcss.tag(tags, 'wikipedia')), 1))).split('=', 1)])
                }})

        # *[wikimedia_commons=~/%[0-9A-F][0-9A-F]/]
        if ('wikimedia_commons' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_210c6ccc), mapcss._tag_capture(capture_tags, 0, tags, 'wikimedia_commons')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                # fixAdd:concat("wikimedia_commons=",trim(replace(URL_decode(tag("wikimedia_commons")),"_"," ")))
                # assertMatch:"node wikimedia_commons=File:Foo%27s"
                # assertNoMatch:"node wikimedia_commons=File:Foo"
                err.append({'class': 9011006, 'subclass': 1999051286, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikimedia_commons=', mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.tag(tags, 'wikimedia_commons')), '_', ' ')))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_19995c46), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(replace(URL_decode(get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),2)),"_"," ")))
                # assertMatch:"node wikipedia=en:Foo%27s"
                # assertNoMatch:"node wikipedia=en:Foo"
                err.append({'class': 9011006, 'subclass': 83644825, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 2)), '_', ' ')))).split('=', 1)])
                }})

        # *[/^wikipedia:[-a-z]{2,12}$/][/^wikipedia:[-a-z]{2,12}$/=~/(?i).*%[0-9A-F][0-9A-F]/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_79a96753) and mapcss.regexp_test(self.re_04adb5d2, mapcss._match_regex(tags, self.re_79a96753)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                # assertMatch:"node wikipedia:de=Foo%27s"
                # assertNoMatch:"node wikipedia:de=Foo"
                err.append({'class': 9011006, 'subclass': 556604422, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}: /]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_536e5b67), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia title should not start with a space after language code")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),2)))
                # assertMatch:"node wikipedia=en: foo"
                # assertNoMatch:"node wikipedia=en:foo"
                err.append({'class': 9011007, 'subclass': 1273458928, 'text': mapcss.tr('wikipedia title should not start with a space after language code'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 2)))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:wiki\//]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67c3b565), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia title should not have ''{0}'' prefix","wiki/")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),1),trim(get(regexp_match("(?i)^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),2)))
                # assertNoMatch:"node wikipedia=en:foo"
                # assertMatch:"node wikipedia=en:wiki/foo"
                err.append({'class': 9011008, 'subclass': 696665203, 'text': mapcss.tr('wikipedia title should not have \'\'{0}\'\' prefix', 'wiki/'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_2a71e33b, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_2a71e33b, mapcss.tag(tags, 'wikipedia')), 2)))).split('=', 1)])
                }})

        # *[wikipedia=~/^[-a-zA-Z]{2,12}:\p{Ll}/][wikipedia!~/^jbo:/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5940ff7c), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1ac7f364, '^jbo:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2d3d5d3d, '(?i)^[-a-z]{2,12}:https?:'), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia page title should have first letter capitalized")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),1),upper(get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),2)),get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),3))
                # assertNoMatch:"node wikipedia=en:Foo"
                # assertMatch:"node wikipedia=en:foo"
                # assertNoMatch:"node wikipedia=ru:Абв"
                # assertMatch:"node wikipedia=ru:абв"
                err.append({'class': 9011009, 'subclass': 1824269684, 'text': mapcss.tr('wikipedia page title should have first letter capitalized'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 1), mapcss.upper(mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 2)), mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 3))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*_/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_08b52119), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2d3d5d3d, '(?i)^[-a-z]{2,12}:https?:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia page title should have spaces instead of underscores (''_''→'' '')")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),1),trim(replace(get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),2),"_"," ")))
                # assertNoMatch:"node wikipedia=en:foo bar"
                # assertMatch:"node wikipedia=en:foo_bar"
                err.append({'class': 9011010, 'subclass': 2024856824, 'text': mapcss.tr('wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 2), '_', ' ')))).split('=', 1)])
                }})

        # *[wikipedia^="da:da:"]
        # *[wikipedia^="da:dk:"]
        # *[wikipedia^="de:de:"]
        # *[wikipedia^="dk:dk:"]
        # *[wikipedia^="en:de:"]
        # *[wikipedia^="en:en:"]
        # *[wikipedia^="en:es:"]
        # *[wikipedia^="en:eu:"]
        # *[wikipedia^="en:fr:"]
        # *[wikipedia^="en:ja:"]
        # *[wikipedia^="en:pl:"]
        # *[wikipedia^="en:pt:"]
        # *[wikipedia^="en:zh:"]
        # *[wikipedia^="es:es:"]
        # *[wikipedia^="eu:eu:"]
        # *[wikipedia^="fr:fr:"]
        # *[wikipedia^="ja:ja:"]
        # *[wikipedia^="pl:en:"]
        # *[wikipedia^="pl:pl:"]
        # *[wikipedia^="pt:pt:"]
        # *[wikipedia^="ru:fr:"]
        # *[wikipedia^="ru:ru:"]
        # *[wikipedia^="zh:zh:"]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'da:da:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'da:dk:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'de:de:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'dk:dk:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:de:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:en:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:es:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:eu:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:ja:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:pl:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:pt:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:zh:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'es:es:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'eu:eu:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'fr:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ja:ja:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pl:en:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pl:pl:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pt:pt:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ru:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ru:ru:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'zh:zh:')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia language seems to be duplicated, e.g. en:en:Foo")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),2),trim(get(regexp_match("(?i)^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),3)))
                # assertNoMatch:"node wikipedia=en:Bar"
                # assertMatch:"node wikipedia=en:en:Foo"
                # assertMatch:"node wikipedia=en:fr:Foo"
                err.append({'class': 9011011, 'subclass': 124114060, 'text': mapcss.tr('wikipedia language seems to be duplicated, e.g. en:en:Foo'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_62d51e93, mapcss.tag(tags, 'wikipedia')), 2), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_62d51e93, mapcss.tag(tags, 'wikipedia')), 3)))).split('=', 1)])
                }})

        # *[wikidata][wikidata!~/^Q[1-9][0-9]{0,8}$/]
        if ('wikidata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikidata') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4b567f18, '^Q[1-9][0-9]{0,8}$'), mapcss._tag_capture(capture_tags, 1, tags, 'wikidata')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wikidata tag must be in Qnnnn format, where n is a digit")
                # assertMatch:"node wikidata=Q"
                # assertMatch:"node wikidata=Q0"
                # assertMatch:"node wikidata=Q0123"
                # assertNoMatch:"node wikidata=Q1"
                # assertNoMatch:"node wikidata=Q123"
                # assertMatch:"node wikidata=a"
                err.append({'class': 9011012, 'subclass': 1398622919, 'text': mapcss.tr('wikidata tag must be in Qnnnn format, where n is a digit')})

        # *[wikipedia][wikipedia=~/^[-a-zA-Z]{2,12}:Q[1-9][0-9]{0,8}$/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2dd1bee3), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value looks like a {1} value","{0.key}","wikidata")
                # assertNoMatch:"node wikipedia=a"
                # assertNoMatch:"node wikipedia=de:Q"
                # assertNoMatch:"node wikipedia=de:Q0"
                # assertNoMatch:"node wikipedia=de:Q0123"
                # assertMatch:"node wikipedia=de:Q1"
                # assertMatch:"node wikipedia=de:Q123"
                # assertNoMatch:"node wikipedia=de:a"
                # assertNoMatch:"node wikipedia=en-GB:Q0123"
                # assertMatch:"node wikipedia=en-GB:Q1"
                # assertMatch:"node wikipedia=en-GB:Q123"
                err.append({'class': 9011016, 'subclass': 346570414, 'text': mapcss.tr('{0} value looks like a {1} value', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'wikidata')})

        # *[!wikipedia][/^wikipedia:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and mapcss._tag_capture(capture_tags, 1, tags, self.re_79319bf9))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' tag is set, but no ''{1}'' tag. Make sure to set ''wikipedia=language:value'' for the main article and optional ''wikipedia:language=value'' only for additional articles that are not just other language variants of the main article.","{1.key}","{0.key}")
                # assertMatch:"node wikipedia:en=a"
                # assertNoMatch:"node wikipedia=Foo"
                # assertNoMatch:"node wikipedia=a wikipedia:en=b"
                err.append({'class': 9011015, 'subclass': 153018468, 'text': mapcss.tr('\'\'{0}\'\' tag is set, but no \'\'{1}\'\' tag. Make sure to set \'\'wikipedia=language:value\'\' for the main article and optional \'\'wikipedia:language=value\'\' only for additional articles that are not just other language variants of the main article.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[wikipedia][wikipedia!~/(?i)^[-a-z]{2,12}:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_07f8e639, '(?i)^[-a-z]{2,12}:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wikipedia tag has no language given, use ''wikipedia''=''language:page title''")
                err.append({'class': 9011001, 'subclass': 1517450396, 'text': mapcss.tr('wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\'')})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:/][wikipedia!~/^https?:\/\//][wikipedia!~/^(ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|atj|av|ay|az|azb|ba|ban|bar|bat-smg|bcl|be|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|din|diq|dsb|dty|dv|dz|ee|el|eml|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gcr|gd|gl|glk|gn|gom|gor|got|gu|gv|ha|hak|haw|he|hi|hif|hr|hsb|ht|hu|hy|hyw|ia|id|ie|ig|ik|ilo|inh|io|is|it|iu|ja|jam|jbo|jv|ka|kaa|kab|kbd|kbp|kg|ki|kk|kl|km|kn|ko|koi|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|mai|map-bms|mdf|mg|mhr|mi|min|mk|ml|mn|mnw|mr|mrj|ms|mt|mwl|my|myv|mzn|na|nah|nap|nds|nds-nl|ne|new|nl|nn|no|nov|nqo|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rw|sa|sah|sat|sc|scn|sco|sd|se|sg|sh|shn|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|szy|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|wa|war|wo|wuu|xal|xh|xmf|yi|yo|za|zea|zh|zh-classical|zh-min-nan|zh-yue|zu):/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_07f8e639), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1f90813f, '^https?:\/\/'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_294645af, '^(ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|atj|av|ay|az|azb|ba|ban|bar|bat-smg|bcl|be|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|din|diq|dsb|dty|dv|dz|ee|el|eml|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gcr|gd|gl|glk|gn|gom|gor|got|gu|gv|ha|hak|haw|he|hi|hif|hr|hsb|ht|hu|hy|hyw|ia|id|ie|ig|ik|ilo|inh|io|is|it|iu|ja|jam|jbo|jv|ka|kaa|kab|kbd|kbp|kg|ki|kk|kl|km|kn|ko|koi|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|mai|map-bms|mdf|mg|mhr|mi|min|mk|ml|mn|mnw|mr|mrj|ms|mt|mwl|my|myv|mzn|na|nah|nap|nds|nds-nl|ne|new|nl|nn|no|nov|nqo|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rw|sa|sah|sat|sc|scn|sco|sd|se|sg|sh|shn|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|szy|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|wa|war|wo|wuu|xal|xh|xmf|yi|yo|za|zea|zh|zh-classical|zh-min-nan|zh-yue|zu):'), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia tag has an unknown language prefix")
                err.append({'class': 9011002, 'subclass': 1358433348, 'text': mapcss.tr('wikipedia tag has an unknown language prefix')})

        # *[wikipedia=~/^https?:\/\//]
        # *[wikipedia=~/(?i)^[-a-z]{2,12}:https?:\/\//]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_1f90813f), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_091c4afa), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:tr("''wikipedia''=''language:page title''")
                # throwWarning:tr("wikipedia tag format is deprecated")
                err.append({'class': 9011003, 'subclass': 75691825, 'text': mapcss.tr('wikipedia tag format is deprecated')})

        # *[wikipedia=~/^be-x-old:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53b6f173), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia ''{0}'' language is obsolete, use ''{1}'' instead","be-x-old","be-tarask")
                # fixAdd:concat("wikipedia=be-tarask:",get(regexp_match("^be-x-old:(.+)$",tag("wikipedia")),1))
                err.append({'class': 9011004, 'subclass': 616152609, 'text': mapcss.tr('wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', 'be-x-old', 'be-tarask'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=be-tarask:', mapcss.get(mapcss.regexp_match(self.re_6a4abd53, mapcss.tag(tags, 'wikipedia')), 1))).split('=', 1)])
                }})

        # *[wikipedia=~/^cz:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_034ab801), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia ''{0}'' language is invalid, use ''{1}'' instead","cz","cs")
                # fixAdd:concat("wikipedia=cs:",get(regexp_match("^cz:(.+)$",tag("wikipedia")),1))
                err.append({'class': 9011005, 'subclass': 243392039, 'text': mapcss.tr('wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', 'cz', 'cs'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=cs:', mapcss.get(mapcss.regexp_match(self.re_577ca7fb, mapcss.tag(tags, 'wikipedia')), 1))).split('=', 1)])
                }})

        # *[wikimedia_commons=~/%[0-9A-F][0-9A-F]/]
        if ('wikimedia_commons' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_210c6ccc), mapcss._tag_capture(capture_tags, 0, tags, 'wikimedia_commons')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                # fixAdd:concat("wikimedia_commons=",trim(replace(URL_decode(tag("wikimedia_commons")),"_"," ")))
                err.append({'class': 9011006, 'subclass': 1999051286, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikimedia_commons=', mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.tag(tags, 'wikimedia_commons')), '_', ' ')))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_19995c46), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(replace(URL_decode(get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),2)),"_"," ")))
                err.append({'class': 9011006, 'subclass': 83644825, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 2)), '_', ' ')))).split('=', 1)])
                }})

        # *[/^wikipedia:[-a-z]{2,12}$/][/^wikipedia:[-a-z]{2,12}$/=~/(?i).*%[0-9A-F][0-9A-F]/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_79a96753) and mapcss.regexp_test(self.re_04adb5d2, mapcss._match_regex(tags, self.re_79a96753)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                err.append({'class': 9011006, 'subclass': 556604422, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}: /]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_536e5b67), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia title should not start with a space after language code")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),2)))
                err.append({'class': 9011007, 'subclass': 1273458928, 'text': mapcss.tr('wikipedia title should not start with a space after language code'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 2)))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:wiki\//]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67c3b565), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia title should not have ''{0}'' prefix","wiki/")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),1),trim(get(regexp_match("(?i)^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),2)))
                err.append({'class': 9011008, 'subclass': 696665203, 'text': mapcss.tr('wikipedia title should not have \'\'{0}\'\' prefix', 'wiki/'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_2a71e33b, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_2a71e33b, mapcss.tag(tags, 'wikipedia')), 2)))).split('=', 1)])
                }})

        # *[wikipedia=~/^[-a-zA-Z]{2,12}:\p{Ll}/][wikipedia!~/^jbo:/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5940ff7c), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1ac7f364, '^jbo:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2d3d5d3d, '(?i)^[-a-z]{2,12}:https?:'), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia page title should have first letter capitalized")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),1),upper(get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),2)),get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),3))
                err.append({'class': 9011009, 'subclass': 1824269684, 'text': mapcss.tr('wikipedia page title should have first letter capitalized'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 1), mapcss.upper(mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 2)), mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 3))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*_/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_08b52119), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2d3d5d3d, '(?i)^[-a-z]{2,12}:https?:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia page title should have spaces instead of underscores (''_''→'' '')")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),1),trim(replace(get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),2),"_"," ")))
                err.append({'class': 9011010, 'subclass': 2024856824, 'text': mapcss.tr('wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 2), '_', ' ')))).split('=', 1)])
                }})

        # *[wikipedia^="da:da:"]
        # *[wikipedia^="da:dk:"]
        # *[wikipedia^="de:de:"]
        # *[wikipedia^="dk:dk:"]
        # *[wikipedia^="en:de:"]
        # *[wikipedia^="en:en:"]
        # *[wikipedia^="en:es:"]
        # *[wikipedia^="en:eu:"]
        # *[wikipedia^="en:fr:"]
        # *[wikipedia^="en:ja:"]
        # *[wikipedia^="en:pl:"]
        # *[wikipedia^="en:pt:"]
        # *[wikipedia^="en:zh:"]
        # *[wikipedia^="es:es:"]
        # *[wikipedia^="eu:eu:"]
        # *[wikipedia^="fr:fr:"]
        # *[wikipedia^="ja:ja:"]
        # *[wikipedia^="pl:en:"]
        # *[wikipedia^="pl:pl:"]
        # *[wikipedia^="pt:pt:"]
        # *[wikipedia^="ru:fr:"]
        # *[wikipedia^="ru:ru:"]
        # *[wikipedia^="zh:zh:"]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'da:da:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'da:dk:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'de:de:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'dk:dk:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:de:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:en:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:es:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:eu:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:ja:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:pl:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:pt:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:zh:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'es:es:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'eu:eu:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'fr:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ja:ja:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pl:en:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pl:pl:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pt:pt:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ru:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ru:ru:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'zh:zh:')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia language seems to be duplicated, e.g. en:en:Foo")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),2),trim(get(regexp_match("(?i)^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),3)))
                err.append({'class': 9011011, 'subclass': 124114060, 'text': mapcss.tr('wikipedia language seems to be duplicated, e.g. en:en:Foo'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_62d51e93, mapcss.tag(tags, 'wikipedia')), 2), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_62d51e93, mapcss.tag(tags, 'wikipedia')), 3)))).split('=', 1)])
                }})

        # *[wikidata][wikidata!~/^Q[1-9][0-9]{0,8}$/]
        if ('wikidata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikidata') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4b567f18, '^Q[1-9][0-9]{0,8}$'), mapcss._tag_capture(capture_tags, 1, tags, 'wikidata')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wikidata tag must be in Qnnnn format, where n is a digit")
                err.append({'class': 9011012, 'subclass': 1398622919, 'text': mapcss.tr('wikidata tag must be in Qnnnn format, where n is a digit')})

        # *[wikipedia][wikipedia=~/^[-a-zA-Z]{2,12}:Q[1-9][0-9]{0,8}$/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2dd1bee3), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value looks like a {1} value","{0.key}","wikidata")
                err.append({'class': 9011016, 'subclass': 346570414, 'text': mapcss.tr('{0} value looks like a {1} value', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'wikidata')})

        # *[!wikipedia][/^wikipedia:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and mapcss._tag_capture(capture_tags, 1, tags, self.re_79319bf9))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' tag is set, but no ''{1}'' tag. Make sure to set ''wikipedia=language:value'' for the main article and optional ''wikipedia:language=value'' only for additional articles that are not just other language variants of the main article.","{1.key}","{0.key}")
                err.append({'class': 9011015, 'subclass': 153018468, 'text': mapcss.tr('\'\'{0}\'\' tag is set, but no \'\'{1}\'\' tag. Make sure to set \'\'wikipedia=language:value\'\' for the main article and optional \'\'wikipedia:language=value\'\' only for additional articles that are not just other language variants of the main article.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[wikipedia][wikipedia!~/(?i)^[-a-z]{2,12}:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_07f8e639, '(?i)^[-a-z]{2,12}:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wikipedia tag has no language given, use ''wikipedia''=''language:page title''")
                err.append({'class': 9011001, 'subclass': 1517450396, 'text': mapcss.tr('wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\'')})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:/][wikipedia!~/^https?:\/\//][wikipedia!~/^(ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|atj|av|ay|az|azb|ba|ban|bar|bat-smg|bcl|be|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|din|diq|dsb|dty|dv|dz|ee|el|eml|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gcr|gd|gl|glk|gn|gom|gor|got|gu|gv|ha|hak|haw|he|hi|hif|hr|hsb|ht|hu|hy|hyw|ia|id|ie|ig|ik|ilo|inh|io|is|it|iu|ja|jam|jbo|jv|ka|kaa|kab|kbd|kbp|kg|ki|kk|kl|km|kn|ko|koi|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|mai|map-bms|mdf|mg|mhr|mi|min|mk|ml|mn|mnw|mr|mrj|ms|mt|mwl|my|myv|mzn|na|nah|nap|nds|nds-nl|ne|new|nl|nn|no|nov|nqo|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rw|sa|sah|sat|sc|scn|sco|sd|se|sg|sh|shn|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|szy|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|wa|war|wo|wuu|xal|xh|xmf|yi|yo|za|zea|zh|zh-classical|zh-min-nan|zh-yue|zu):/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_07f8e639), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1f90813f, '^https?:\/\/'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_294645af, '^(ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|atj|av|ay|az|azb|ba|ban|bar|bat-smg|bcl|be|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|din|diq|dsb|dty|dv|dz|ee|el|eml|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gcr|gd|gl|glk|gn|gom|gor|got|gu|gv|ha|hak|haw|he|hi|hif|hr|hsb|ht|hu|hy|hyw|ia|id|ie|ig|ik|ilo|inh|io|is|it|iu|ja|jam|jbo|jv|ka|kaa|kab|kbd|kbp|kg|ki|kk|kl|km|kn|ko|koi|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|mai|map-bms|mdf|mg|mhr|mi|min|mk|ml|mn|mnw|mr|mrj|ms|mt|mwl|my|myv|mzn|na|nah|nap|nds|nds-nl|ne|new|nl|nn|no|nov|nqo|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rw|sa|sah|sat|sc|scn|sco|sd|se|sg|sh|shn|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|szy|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|wa|war|wo|wuu|xal|xh|xmf|yi|yo|za|zea|zh|zh-classical|zh-min-nan|zh-yue|zu):'), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia tag has an unknown language prefix")
                err.append({'class': 9011002, 'subclass': 1358433348, 'text': mapcss.tr('wikipedia tag has an unknown language prefix')})

        # *[wikipedia=~/^https?:\/\//]
        # *[wikipedia=~/(?i)^[-a-z]{2,12}:https?:\/\//]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_1f90813f), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_091c4afa), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # suggestAlternative:tr("''wikipedia''=''language:page title''")
                # throwWarning:tr("wikipedia tag format is deprecated")
                err.append({'class': 9011003, 'subclass': 75691825, 'text': mapcss.tr('wikipedia tag format is deprecated')})

        # *[wikipedia=~/^be-x-old:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53b6f173), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia ''{0}'' language is obsolete, use ''{1}'' instead","be-x-old","be-tarask")
                # fixAdd:concat("wikipedia=be-tarask:",get(regexp_match("^be-x-old:(.+)$",tag("wikipedia")),1))
                err.append({'class': 9011004, 'subclass': 616152609, 'text': mapcss.tr('wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', 'be-x-old', 'be-tarask'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=be-tarask:', mapcss.get(mapcss.regexp_match(self.re_6a4abd53, mapcss.tag(tags, 'wikipedia')), 1))).split('=', 1)])
                }})

        # *[wikipedia=~/^cz:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_034ab801), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia ''{0}'' language is invalid, use ''{1}'' instead","cz","cs")
                # fixAdd:concat("wikipedia=cs:",get(regexp_match("^cz:(.+)$",tag("wikipedia")),1))
                err.append({'class': 9011005, 'subclass': 243392039, 'text': mapcss.tr('wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', 'cz', 'cs'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=cs:', mapcss.get(mapcss.regexp_match(self.re_577ca7fb, mapcss.tag(tags, 'wikipedia')), 1))).split('=', 1)])
                }})

        # *[wikimedia_commons=~/%[0-9A-F][0-9A-F]/]
        if ('wikimedia_commons' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_210c6ccc), mapcss._tag_capture(capture_tags, 0, tags, 'wikimedia_commons')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                # fixAdd:concat("wikimedia_commons=",trim(replace(URL_decode(tag("wikimedia_commons")),"_"," ")))
                err.append({'class': 9011006, 'subclass': 1999051286, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikimedia_commons=', mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.tag(tags, 'wikimedia_commons')), '_', ' ')))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_19995c46), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(replace(URL_decode(get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),2)),"_"," ")))
                err.append({'class': 9011006, 'subclass': 83644825, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 2)), '_', ' ')))).split('=', 1)])
                }})

        # *[/^wikipedia:[-a-z]{2,12}$/][/^wikipedia:[-a-z]{2,12}$/=~/(?i).*%[0-9A-F][0-9A-F]/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_79a96753) and mapcss.regexp_test(self.re_04adb5d2, mapcss._match_regex(tags, self.re_79a96753)))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
                err.append({'class': 9011006, 'subclass': 556604422, 'text': mapcss.tr('{0} tag should not have URL-encoded values like \'\'%27\'\'', mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}: /]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_536e5b67), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia title should not start with a space after language code")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(get(regexp_match("(?i)^([-a-z]+:)(.*)$",tag("wikipedia")),2)))
                err.append({'class': 9011007, 'subclass': 1273458928, 'text': mapcss.tr('wikipedia title should not start with a space after language code'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_676bdf5d, mapcss.tag(tags, 'wikipedia')), 2)))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:wiki\//]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_67c3b565), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia title should not have ''{0}'' prefix","wiki/")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),1),trim(get(regexp_match("(?i)^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),2)))
                err.append({'class': 9011008, 'subclass': 696665203, 'text': mapcss.tr('wikipedia title should not have \'\'{0}\'\' prefix', 'wiki/'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_2a71e33b, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_2a71e33b, mapcss.tag(tags, 'wikipedia')), 2)))).split('=', 1)])
                }})

        # *[wikipedia=~/^[-a-zA-Z]{2,12}:\p{Ll}/][wikipedia!~/^jbo:/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5940ff7c), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1ac7f364, '^jbo:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2d3d5d3d, '(?i)^[-a-z]{2,12}:https?:'), mapcss._tag_capture(capture_tags, 2, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia page title should have first letter capitalized")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),1),upper(get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),2)),get(regexp_match("(?i)^([-a-z]+:)(.)(.*)$",tag("wikipedia")),3))
                err.append({'class': 9011009, 'subclass': 1824269684, 'text': mapcss.tr('wikipedia page title should have first letter capitalized'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 1), mapcss.upper(mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 2)), mapcss.get(mapcss.regexp_match(self.re_6a7e1973, mapcss.tag(tags, 'wikipedia')), 3))).split('=', 1)])
                }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*_/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_08b52119), mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_2d3d5d3d, '(?i)^[-a-z]{2,12}:https?:'), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia page title should have spaces instead of underscores (''_''→'' '')")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),1),trim(replace(get(regexp_match("(?i)^([-a-z]+:)(.+)$",tag("wikipedia")),2),"_"," ")))
                err.append({'class': 9011010, 'subclass': 2024856824, 'text': mapcss.tr('wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.get(mapcss.regexp_match(self.re_1559839b, mapcss.tag(tags, 'wikipedia')), 2), '_', ' ')))).split('=', 1)])
                }})

        # *[wikipedia^="da:da:"]
        # *[wikipedia^="da:dk:"]
        # *[wikipedia^="de:de:"]
        # *[wikipedia^="dk:dk:"]
        # *[wikipedia^="en:de:"]
        # *[wikipedia^="en:en:"]
        # *[wikipedia^="en:es:"]
        # *[wikipedia^="en:eu:"]
        # *[wikipedia^="en:fr:"]
        # *[wikipedia^="en:ja:"]
        # *[wikipedia^="en:pl:"]
        # *[wikipedia^="en:pt:"]
        # *[wikipedia^="en:zh:"]
        # *[wikipedia^="es:es:"]
        # *[wikipedia^="eu:eu:"]
        # *[wikipedia^="fr:fr:"]
        # *[wikipedia^="ja:ja:"]
        # *[wikipedia^="pl:en:"]
        # *[wikipedia^="pl:pl:"]
        # *[wikipedia^="pt:pt:"]
        # *[wikipedia^="ru:fr:"]
        # *[wikipedia^="ru:ru:"]
        # *[wikipedia^="zh:zh:"]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'da:da:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'da:dk:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'de:de:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'dk:dk:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:de:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:en:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:es:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:eu:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:ja:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:pl:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:pt:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'en:zh:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'es:es:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'eu:eu:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'fr:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ja:ja:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pl:en:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pl:pl:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'pt:pt:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ru:fr:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'ru:ru:')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia'), mapcss._value_capture(capture_tags, 0, 'zh:zh:')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("wikipedia language seems to be duplicated, e.g. en:en:Foo")
                # fixAdd:concat("wikipedia=",get(regexp_match("(?i)^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),2),trim(get(regexp_match("(?i)^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),3)))
                err.append({'class': 9011011, 'subclass': 124114060, 'text': mapcss.tr('wikipedia language seems to be duplicated, e.g. en:en:Foo'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat('wikipedia=', mapcss.get(mapcss.regexp_match(self.re_62d51e93, mapcss.tag(tags, 'wikipedia')), 2), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_62d51e93, mapcss.tag(tags, 'wikipedia')), 3)))).split('=', 1)])
                }})

        # *[wikidata][wikidata!~/^Q[1-9][0-9]{0,8}$/]
        if ('wikidata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikidata') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4b567f18, '^Q[1-9][0-9]{0,8}$'), mapcss._tag_capture(capture_tags, 1, tags, 'wikidata')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("wikidata tag must be in Qnnnn format, where n is a digit")
                err.append({'class': 9011012, 'subclass': 1398622919, 'text': mapcss.tr('wikidata tag must be in Qnnnn format, where n is a digit')})

        # *[wikipedia][wikipedia=~/^[-a-zA-Z]{2,12}:Q[1-9][0-9]{0,8}$/]
        if ('wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_2dd1bee3), mapcss._tag_capture(capture_tags, 1, tags, 'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} value looks like a {1} value","{0.key}","wikidata")
                err.append({'class': 9011016, 'subclass': 346570414, 'text': mapcss.tr('{0} value looks like a {1} value', mapcss._tag_uncapture(capture_tags, '{0.key}'), 'wikidata')})

        # *[!wikipedia][/^wikipedia:/]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, 'wikipedia') and mapcss._tag_capture(capture_tags, 1, tags, self.re_79319bf9))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("''{0}'' tag is set, but no ''{1}'' tag. Make sure to set ''wikipedia=language:value'' for the main article and optional ''wikipedia:language=value'' only for additional articles that are not just other language variants of the main article.","{1.key}","{0.key}")
                err.append({'class': 9011015, 'subclass': 153018468, 'text': mapcss.tr('\'\'{0}\'\' tag is set, but no \'\'{1}\'\' tag. Make sure to set \'\'wikipedia=language:value\'\' for the main article and optional \'\'wikipedia:language=value\'\' only for additional articles that are not just other language variants of the main article.', mapcss._tag_uncapture(capture_tags, '{1.key}'), mapcss._tag_uncapture(capture_tags, '{0.key}'))})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_wikipedia(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {'wikipedia': 'Foobar'}), expected={'class': 9011001, 'subclass': 1517450396})
        self.check_not_err(n.node(data, {'wikipedia': 'en-GB:Foobar'}), expected={'class': 9011001, 'subclass': 1517450396})
        self.check_not_err(n.node(data, {'wikipedia': 'en:Foobar'}), expected={'class': 9011001, 'subclass': 1517450396})
        self.check_err(n.node(data, {'wikipedia': 'X-Y-Z:Foobar'}), expected={'class': 9011002, 'subclass': 1358433348})
        self.check_not_err(n.node(data, {'wikipedia': 'en:Foobar'}), expected={'class': 9011002, 'subclass': 1358433348})
        self.check_not_err(n.node(data, {'wikipedia': 'en:OpenStreetMap'}), expected={'class': 9011003, 'subclass': 75691825})
        self.check_err(n.node(data, {'wikipedia': 'http://en.wikipedia.org/wiki/OpenStreetMap'}), expected={'class': 9011003, 'subclass': 75691825})
        self.check_not_err(n.node(data, {'wikipedia': 'abe-x-old:foo'}), expected={'class': 9011004, 'subclass': 616152609})
        self.check_err(n.node(data, {'wikipedia': 'be-x-old:foo'}), expected={'class': 9011004, 'subclass': 616152609})
        self.check_err(n.node(data, {'wikipedia': 'cz:foo'}), expected={'class': 9011005, 'subclass': 243392039})
        self.check_not_err(n.node(data, {'wikipedia': 'en:cz:foo'}), expected={'class': 9011005, 'subclass': 243392039})
        self.check_err(n.node(data, {'wikimedia_commons': 'File:Foo%27s'}), expected={'class': 9011006, 'subclass': 1999051286})
        self.check_not_err(n.node(data, {'wikimedia_commons': 'File:Foo'}), expected={'class': 9011006, 'subclass': 1999051286})
        self.check_err(n.node(data, {'wikipedia': 'en:Foo%27s'}), expected={'class': 9011006, 'subclass': 83644825})
        self.check_not_err(n.node(data, {'wikipedia': 'en:Foo'}), expected={'class': 9011006, 'subclass': 83644825})
        self.check_err(n.node(data, {'wikipedia:de': 'Foo%27s'}), expected={'class': 9011006, 'subclass': 556604422})
        self.check_not_err(n.node(data, {'wikipedia:de': 'Foo'}), expected={'class': 9011006, 'subclass': 556604422})
        self.check_err(n.node(data, {'wikipedia': 'en: foo'}), expected={'class': 9011007, 'subclass': 1273458928})
        self.check_not_err(n.node(data, {'wikipedia': 'en:foo'}), expected={'class': 9011007, 'subclass': 1273458928})
        self.check_not_err(n.node(data, {'wikipedia': 'en:foo'}), expected={'class': 9011008, 'subclass': 696665203})
        self.check_err(n.node(data, {'wikipedia': 'en:wiki/foo'}), expected={'class': 9011008, 'subclass': 696665203})
        self.check_not_err(n.node(data, {'wikipedia': 'en:Foo'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_err(n.node(data, {'wikipedia': 'en:foo'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_not_err(n.node(data, {'wikipedia': 'ru:Абв'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_err(n.node(data, {'wikipedia': 'ru:абв'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_not_err(n.node(data, {'wikipedia': 'en:foo bar'}), expected={'class': 9011010, 'subclass': 2024856824})
        self.check_err(n.node(data, {'wikipedia': 'en:foo_bar'}), expected={'class': 9011010, 'subclass': 2024856824})
        self.check_not_err(n.node(data, {'wikipedia': 'en:Bar'}), expected={'class': 9011011, 'subclass': 124114060})
        self.check_err(n.node(data, {'wikipedia': 'en:en:Foo'}), expected={'class': 9011011, 'subclass': 124114060})
        self.check_err(n.node(data, {'wikipedia': 'en:fr:Foo'}), expected={'class': 9011011, 'subclass': 124114060})
        self.check_err(n.node(data, {'wikidata': 'Q'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_err(n.node(data, {'wikidata': 'Q0'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_err(n.node(data, {'wikidata': 'Q0123'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_not_err(n.node(data, {'wikidata': 'Q1'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_not_err(n.node(data, {'wikidata': 'Q123'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_err(n.node(data, {'wikidata': 'a'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_not_err(n.node(data, {'wikipedia': 'a'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_not_err(n.node(data, {'wikipedia': 'de:Q'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_not_err(n.node(data, {'wikipedia': 'de:Q0'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_not_err(n.node(data, {'wikipedia': 'de:Q0123'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_err(n.node(data, {'wikipedia': 'de:Q1'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_err(n.node(data, {'wikipedia': 'de:Q123'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_not_err(n.node(data, {'wikipedia': 'de:a'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_not_err(n.node(data, {'wikipedia': 'en-GB:Q0123'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_err(n.node(data, {'wikipedia': 'en-GB:Q1'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_err(n.node(data, {'wikipedia': 'en-GB:Q123'}), expected={'class': 9011016, 'subclass': 346570414})
        self.check_err(n.node(data, {'wikipedia:en': 'a'}), expected={'class': 9011015, 'subclass': 153018468})
        self.check_not_err(n.node(data, {'wikipedia': 'Foo'}), expected={'class': 9011015, 'subclass': 153018468})
        self.check_not_err(n.node(data, {'wikipedia': 'a', 'wikipedia:en': 'b'}), expected={'class': 9011015, 'subclass': 153018468})
