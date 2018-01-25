#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_wikipedia(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9011001] = {'item': 9011, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\'', capture_tags)}
        self.errors[9011002] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia tag has an unknown language prefix', capture_tags)}
        self.errors[9011003] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'deprecated tagging', capture_tags)}
        self.errors[9011004] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', capture_tags, u'be-x-old', u'be-tarask')}
        self.errors[9011005] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', capture_tags, u'cz', u'cs')}
        self.errors[9011006] = {'item': 9011, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'{0} tag should not have URL-encoded values like \'\'%27\'\'', capture_tags, u'{0.tag}')}
        self.errors[9011007] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia title should not start with a space after language code', capture_tags)}
        self.errors[9011008] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia title should not have \'\'{0}\'\' prefix', capture_tags, u'wiki/')}
        self.errors[9011009] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia page title should have first letter capitalized', capture_tags)}
        self.errors[9011010] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')', capture_tags)}
        self.errors[9011011] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia language seems to be duplicated, e.g. en:en:Foo', capture_tags)}
        self.errors[9011012] = {'item': 9011, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'wikidata tag must be in Qnnnn format, where n is a digit', capture_tags)}
        self.errors[9011013] = {'item': 9011, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'missing tag', capture_tags)}
        self.errors[9011014] = {'item': 9011, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'wikipedia tag is not set, but a \'\'{0}\'\' tag is. Make sure to use wikipedia=language:value together with wikidata tag.', capture_tags, u'{1.key}')}

        self.re_034ab801 = re.compile(ur'^cz:')
        self.re_07f8e639 = re.compile(ur'(?i)^[-a-z]{2,12}:')
        self.re_08b52119 = re.compile(ur'(?i)^[-a-z]{2,12}:.*_')
        self.re_091c4afa = re.compile(ur'(?i)^[-a-z]{2,12}:https?:\/\/')
        self.re_1478a0ca = re.compile(ur'^([-a-z]+:)(.+)$')
        self.re_1825d91f = re.compile(ur'^([-a-z]+:)([-a-z]+:)(.*)$')
        self.re_19995c46 = re.compile(ur'(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]')
        self.re_1ac7f364 = re.compile(ur'^jbo:')
        self.re_1f90813f = re.compile(ur'^https?:\/\/')
        self.re_210c6ccc = re.compile(ur'%[0-9A-F][0-9A-F]')
        self.re_290a9471 = re.compile(ur'^([-a-z]+:)wiki/(.*)$')
        self.re_2d3d5d3d = re.compile(ur'(?i)^[-a-z]{2,12}:https?:')
        self.re_450fb7f8 = re.compile(ur'^([-a-z]+:)(.)(.*)$')
        self.re_4b567f18 = re.compile(ur'^Q[1-9][0-9]{0,8}$')
        self.re_536e5b67 = re.compile(ur'(?i)^[-a-z]{2,12}: ')
        self.re_53b6f173 = re.compile(ur'^be-x-old:')
        self.re_577ca7fb = re.compile(ur'^cz:(.+)$')
        self.re_5940ff7c = re.compile(ur'^[-a-zA-Z]{2,12}:\p{Ll}')
        self.re_6313f817 = re.compile(ur'^(aa|ab|ace|ady|ady-cyrl|aeb|aeb-arab|aeb-latn|af|ak|aln|als|am|an|ang|anp|ar|arc|arn|arq|ary|arz|as|ase|ast|av|avk|awa|ay|az|azb|ba|ban|bar|bat-smg|bbc|bbc-latn|bcc|bcl|be|be-tarask|be-x-old|bg|bgn|bh|bho|bi|bjn|bm|bn|bo|bpy|bqi|br|brh|bs|bto|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cps|cr|crh|crh-cyrl|crh-latn|cs|csb|cu|cv|cy|cz|da|de|de-at|de-ch|de-formal|din|diq|dsb|dtp|dty|dv|dz|ee|egl|el|eml|en|en-ca|en-gb|eo|es|et|eu|ext|fa|ff|fi|fit|fiu-vro|fj|fo|fr|frc|frp|frr|fur|fy|ga|gag|gan|gan-hans|gan-hant|gd|gl|glk|gn|gom|gom-deva|gom-latn|gor|got|grc|gsw|gu|gv|ha|hak|haw|he|hi|hif|hif-latn|hil|ho|hr|hrx|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ike-cans|ike-latn|ilo|inh|io|is|it|iu|ja|jam|jbo|jut|jv|ka|kaa|kab|kbd|kbd-cyrl|kea|kg|khw|ki|kiu|kj|kk|kk-arab|kk-cn|kk-cyrl|kk-kz|kk-latn|kk-tr|kl|km|kn|ko|ko-kp|koi|kr|krc|kri|krj|krl|ks|ks-arab|ks-deva|ksh|ku|ku-arab|ku-latn|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|liv|lki|lmo|ln|lo|loz|lrc|lt|ltg|lus|luz|lv|lzh|lzz|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|nap|nb|nds|nds-nl|ne|new|ng|niu|nl|nl-informal|nn|no|nod|nov|nrm|nso|nv|ny|nys|oc|olo|om|or|os|ota|pa|pag|pam|pap|pcd|pdc|pdt|pfl|pi|pih|pl|pms|pnb|pnt|prg|ps|pt|pt-br|qu|qug|rgn|rif|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|ruq|ruq-cyrl|ruq-latn|rw|rwr|sa|sah|sat|sc|scn|sco|sd|sdc|sdh|se|sei|ses|sg|sgs|sh|shi|shi-latn|shi-tfng|shn|si|simple|sje|sk|sl|sli|sm|sma|smj|sn|so|sq|sr|sr-ec|sr-el|srn|srq|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|tg-cyrl|tg-latn|th|ti|tk|tl|tly|tn|to|tokipona|tpi|tr|tru|ts|tt|tt-cyrl|tt-latn|tum|tw|ty|tyv|tzm|udm|ug|ug-arab|ug-latn|uk|ur|uz|uz-cyrl|uz-latn|ve|vec|vep|vi|vls|vmf|vo|vot|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|za|zea|zh|zh-classical|zh-cn|zh-hans|zh-hant|zh-hk|zh-min-nan|zh-mo|zh-my|zh-sg|zh-tw|zh-yue|zu):')
        self.re_67c3b565 = re.compile(ur'(?i)^[-a-z]{2,12}:wiki\/')
        self.re_6a4abd53 = re.compile(ur'^be-x-old:(.+)$')
        self.re_70a0064f = re.compile(ur'^([-a-z]+:)(.*)$')
        self.re_79319bf9 = re.compile(ur'^wikipedia:')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[wikipedia][wikipedia!~/(?i)^[-a-z]{2,12}:/]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(self.re_07f8e639, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwError:tr("wikipedia tag has no language given, use ''wikipedia''=''language:page title''")
            # assertMatch:"node wikipedia=Foobar"
            # assertNoMatch:"node wikipedia=en-GB:Foobar"
            # assertNoMatch:"node wikipedia=en:Foobar"
            err.append({'class': 9011001, 'subclass': 1517450396, 'text': mapcss.tr(u'wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\'', capture_tags)})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:/][wikipedia!~/^https?:\/\//][wikipedia!~/^(aa|ab|ace|ady|ady-cyrl|aeb|aeb-arab|aeb-latn|af|ak|aln|als|am|an|ang|anp|ar|arc|arn|arq|ary|arz|as|ase|ast|av|avk|awa|ay|az|azb|ba|ban|bar|bat-smg|bbc|bbc-latn|bcc|bcl|be|be-tarask|be-x-old|bg|bgn|bh|bho|bi|bjn|bm|bn|bo|bpy|bqi|br|brh|bs|bto|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cps|cr|crh|crh-cyrl|crh-latn|cs|csb|cu|cv|cy|cz|da|de|de-at|de-ch|de-formal|din|diq|dsb|dtp|dty|dv|dz|ee|egl|el|eml|en|en-ca|en-gb|eo|es|et|eu|ext|fa|ff|fi|fit|fiu-vro|fj|fo|fr|frc|frp|frr|fur|fy|ga|gag|gan|gan-hans|gan-hant|gd|gl|glk|gn|gom|gom-deva|gom-latn|gor|got|grc|gsw|gu|gv|ha|hak|haw|he|hi|hif|hif-latn|hil|ho|hr|hrx|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ike-cans|ike-latn|ilo|inh|io|is|it|iu|ja|jam|jbo|jut|jv|ka|kaa|kab|kbd|kbd-cyrl|kea|kg|khw|ki|kiu|kj|kk|kk-arab|kk-cn|kk-cyrl|kk-kz|kk-latn|kk-tr|kl|km|kn|ko|ko-kp|koi|kr|krc|kri|krj|krl|ks|ks-arab|ks-deva|ksh|ku|ku-arab|ku-latn|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|liv|lki|lmo|ln|lo|loz|lrc|lt|ltg|lus|luz|lv|lzh|lzz|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|nap|nb|nds|nds-nl|ne|new|ng|niu|nl|nl-informal|nn|no|nod|nov|nrm|nso|nv|ny|nys|oc|olo|om|or|os|ota|pa|pag|pam|pap|pcd|pdc|pdt|pfl|pi|pih|pl|pms|pnb|pnt|prg|ps|pt|pt-br|qu|qug|rgn|rif|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|ruq|ruq-cyrl|ruq-latn|rw|rwr|sa|sah|sat|sc|scn|sco|sd|sdc|sdh|se|sei|ses|sg|sgs|sh|shi|shi-latn|shi-tfng|shn|si|simple|sje|sk|sl|sli|sm|sma|smj|sn|so|sq|sr|sr-ec|sr-el|srn|srq|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|tg-cyrl|tg-latn|th|ti|tk|tl|tly|tn|to|tokipona|tpi|tr|tru|ts|tt|tt-cyrl|tt-latn|tum|tw|ty|tyv|tzm|udm|ug|ug-arab|ug-latn|uk|ur|uz|uz-cyrl|uz-latn|ve|vec|vep|vi|vls|vmf|vo|vot|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|za|zea|zh|zh-classical|zh-cn|zh-hans|zh-hant|zh-hk|zh-min-nan|zh-mo|zh-my|zh-sg|zh-tw|zh-yue|zu):/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_07f8e639, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_1f90813f, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_6313f817, mapcss._tag_capture(capture_tags, 2, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia tag has an unknown language prefix")
            # assertMatch:"node wikipedia=X-Y-Z:Foobar"
            # assertNoMatch:"node wikipedia=en:Foobar"
            err.append({'class': 9011002, 'subclass': 1499670292, 'text': mapcss.tr(u'wikipedia tag has an unknown language prefix', capture_tags)})

        # *[wikipedia=~/^https?:\/\//]
        # *[wikipedia=~/(?i)^[-a-z]{2,12}:https?:\/\//]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_1f90813f, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'))) or \
            (mapcss.regexp_test_(self.re_091c4afa, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # group:tr("deprecated tagging")
            # suggestAlternative:tr("''wikipedia''=''language:page title''")
            # throwWarning:tr("wikipedia tag format is deprecated")
            # assertNoMatch:"node wikipedia=en:OpenStreetMap"
            # assertMatch:"node wikipedia=http://en.wikipedia.org/wiki/OpenStreetMap"
            err.append({'class': 9011003, 'subclass': 75691825, 'text': mapcss.tr(u'wikipedia tag format is deprecated', capture_tags)})

        # *[wikipedia=~/^be-x-old:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_53b6f173, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia ''{0}'' language is obsolete, use ''{1}'' instead","be-x-old","be-tarask")
            # fixAdd:concat("wikipedia=be-tarask:",get(regexp_match("^be-x-old:(.+)$",tag("wikipedia")),1))
            # assertNoMatch:"node wikipedia=abe-x-old:foo"
            # assertMatch:"node wikipedia=be-x-old:foo"
            err.append({'class': 9011004, 'subclass': 616152609, 'text': mapcss.tr(u'wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', capture_tags, u'be-x-old', u'be-tarask'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=be-tarask:', mapcss.get(mapcss.regexp_match(self.re_6a4abd53, mapcss.tag(tags, u'wikipedia')), 1))).split('=', 1)])
            }})

        # *[wikipedia=~/^cz:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_034ab801, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia ''{0}'' language is invalid, use ''{1}'' instead","cz","cs")
            # fixAdd:concat("wikipedia=cs:",get(regexp_match("^cz:(.+)$",tag("wikipedia")),1))
            # assertMatch:"node wikipedia=cz:foo"
            # assertNoMatch:"node wikipedia=en:cz:foo"
            err.append({'class': 9011005, 'subclass': 243392039, 'text': mapcss.tr(u'wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', capture_tags, u'cz', u'cs'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=cs:', mapcss.get(mapcss.regexp_match(self.re_577ca7fb, mapcss.tag(tags, u'wikipedia')), 1))).split('=', 1)])
            }})

        # *[wikimedia_commons=~/%[0-9A-F][0-9A-F]/]
        if (u'wikimedia_commons' in keys) and \
            ((mapcss.regexp_test_(self.re_210c6ccc, mapcss._tag_capture(capture_tags, 0, tags, u'wikimedia_commons')))):
            # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
            # fixAdd:concat("wikimedia_commons=",trim(replace(URL_decode(tag("wikimedia_commons")),"_"," ")))
            # assertMatch:"node wikimedia_commons=File:Foo%27s"
            # assertNoMatch:"node wikimedia_commons=File:Foo"
            err.append({'class': 9011006, 'subclass': 1999051286, 'text': mapcss.tr(u'{0} tag should not have URL-encoded values like \'\'%27\'\'', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikimedia_commons=', mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.tag(tags, u'wikimedia_commons')), u'_', u' ')))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_19995c46, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.tag}")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(replace(URL_decode(get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),2)),"_"," ")))
            # assertMatch:"node wikipedia=en:Foo%27s"
            # assertNoMatch:"node wikipedia=en:Foo"
            err.append({'class': 9011006, 'subclass': 83644825, 'text': mapcss.tr(u'{0} tag should not have URL-encoded values like \'\'%27\'\'', capture_tags, u'{0.tag}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 2)), u'_', u' ')))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}: /]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_536e5b67, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia title should not start with a space after language code")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),2)))
            # assertMatch:"node wikipedia=en: foo"
            # assertNoMatch:"node wikipedia=en:foo"
            err.append({'class': 9011007, 'subclass': 1273458928, 'text': mapcss.tr(u'wikipedia title should not start with a space after language code', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 2)))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:wiki\//]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_67c3b565, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia title should not have ''{0}'' prefix","wiki/")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),1),trim(get(regexp_match("^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),2)))
            # assertNoMatch:"node wikipedia=en:foo"
            # assertMatch:"node wikipedia=en:wiki/foo"
            err.append({'class': 9011008, 'subclass': 696665203, 'text': mapcss.tr(u'wikipedia title should not have \'\'{0}\'\' prefix', capture_tags, u'wiki/'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_290a9471, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_290a9471, mapcss.tag(tags, u'wikipedia')), 2)))).split('=', 1)])
            }})

        # *[wikipedia=~/^[-a-zA-Z]{2,12}:\p{Ll}/][wikipedia!~/^jbo:/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_5940ff7c, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_1ac7f364, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_2d3d5d3d, mapcss._tag_capture(capture_tags, 2, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia page title should have first letter capitalized")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),1),upper(get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),2)),get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),3))
            # assertNoMatch:"node wikipedia=en:Foo"
            # assertMatch:"node wikipedia=en:foo"
            # assertNoMatch:"node wikipedia=ru:Абв"
            # assertMatch:"node wikipedia=ru:абв"
            err.append({'class': 9011009, 'subclass': 1824269684, 'text': mapcss.tr(u'wikipedia page title should have first letter capitalized', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 1), mapcss.upper(mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 2)), mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 3))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*_/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_08b52119, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_2d3d5d3d, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia page title should have spaces instead of underscores (''_''→'' '')")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),1),trim(replace(get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),2),"_"," ")))
            # assertNoMatch:"node wikipedia=en:foo bar"
            # assertMatch:"node wikipedia=en:foo_bar"
            err.append({'class': 9011010, 'subclass': 2024856824, 'text': mapcss.tr(u'wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 2), u'_', u' ')))).split('=', 1)])
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
        if (u'wikipedia' in keys) and \
            ((mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'da:da:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'da:dk:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'de:de:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'dk:dk:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:de:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:en:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:es:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:eu:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:ja:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:pl:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:pt:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:zh:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'es:es:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'eu:eu:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'fr:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ja:ja:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pl:en:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pl:pl:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pt:pt:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ru:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ru:ru:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'zh:zh:'))):
            # throwWarning:tr("wikipedia language seems to be duplicated, e.g. en:en:Foo")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),2),trim(get(regexp_match("^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),3)))
            # assertNoMatch:"node wikipedia=en:Bar"
            # assertMatch:"node wikipedia=en:en:Foo"
            # assertMatch:"node wikipedia=en:fr:Foo"
            err.append({'class': 9011011, 'subclass': 124114060, 'text': mapcss.tr(u'wikipedia language seems to be duplicated, e.g. en:en:Foo', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1825d91f, mapcss.tag(tags, u'wikipedia')), 2), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_1825d91f, mapcss.tag(tags, u'wikipedia')), 3)))).split('=', 1)])
            }})

        # *[wikidata][wikidata!~/^Q[1-9][0-9]{0,8}$/]
        if (u'wikidata' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikidata') and not mapcss.regexp_test_(self.re_4b567f18, mapcss._tag_capture(capture_tags, 1, tags, u'wikidata')))):
            # throwError:tr("wikidata tag must be in Qnnnn format, where n is a digit")
            # assertMatch:"node wikidata=Q"
            # assertMatch:"node wikidata=Q0"
            # assertMatch:"node wikidata=Q0123"
            # assertNoMatch:"node wikidata=Q1"
            # assertNoMatch:"node wikidata=Q123"
            # assertMatch:"node wikidata=a"
            err.append({'class': 9011012, 'subclass': 1398622919, 'text': mapcss.tr(u'wikidata tag must be in Qnnnn format, where n is a digit', capture_tags)})

        # *[wikipedia][!wikidata]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss._tag_capture(capture_tags, 1, tags, u'wikidata'))):
            # group:tr("missing tag")
            # throwOther:tr("wikipedia tag is set, but there is no wikidata tag. Wikipedia plugin might help with wikidata id lookups")
            # assertNoMatch:"node foo=bar"
            # assertNoMatch:"node wikidata=Q1"
            # assertNoMatch:"node wikipedia=a wikidata=Q123"
            # assertMatch:"node wikipedia=a"
            err.append({'class': 9011013, 'subclass': 52215017, 'text': mapcss.tr(u'wikipedia tag is set, but there is no wikidata tag. Wikipedia plugin might help with wikidata id lookups', capture_tags)})

        # *[!wikipedia][/^wikipedia:/]
        if ((not mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and mapcss._tag_capture(capture_tags, 1, tags, self.re_79319bf9))):
            # throwWarning:tr("wikipedia tag is not set, but a ''{0}'' tag is. Make sure to use wikipedia=language:value together with wikidata tag.","{1.key}")
            # assertMatch:"node wikipedia:en=a"
            # assertNoMatch:"node wikipedia=Foo"
            # assertNoMatch:"node wikipedia=a wikipedia:en=b"
            err.append({'class': 9011014, 'subclass': 153018468, 'text': mapcss.tr(u'wikipedia tag is not set, but a \'\'{0}\'\' tag is. Make sure to use wikipedia=language:value together with wikidata tag.', capture_tags, u'{1.key}')})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[wikipedia][wikipedia!~/(?i)^[-a-z]{2,12}:/]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(self.re_07f8e639, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwError:tr("wikipedia tag has no language given, use ''wikipedia''=''language:page title''")
            err.append({'class': 9011001, 'subclass': 1517450396, 'text': mapcss.tr(u'wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\'', capture_tags)})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:/][wikipedia!~/^https?:\/\//][wikipedia!~/^(aa|ab|ace|ady|ady-cyrl|aeb|aeb-arab|aeb-latn|af|ak|aln|als|am|an|ang|anp|ar|arc|arn|arq|ary|arz|as|ase|ast|av|avk|awa|ay|az|azb|ba|ban|bar|bat-smg|bbc|bbc-latn|bcc|bcl|be|be-tarask|be-x-old|bg|bgn|bh|bho|bi|bjn|bm|bn|bo|bpy|bqi|br|brh|bs|bto|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cps|cr|crh|crh-cyrl|crh-latn|cs|csb|cu|cv|cy|cz|da|de|de-at|de-ch|de-formal|din|diq|dsb|dtp|dty|dv|dz|ee|egl|el|eml|en|en-ca|en-gb|eo|es|et|eu|ext|fa|ff|fi|fit|fiu-vro|fj|fo|fr|frc|frp|frr|fur|fy|ga|gag|gan|gan-hans|gan-hant|gd|gl|glk|gn|gom|gom-deva|gom-latn|gor|got|grc|gsw|gu|gv|ha|hak|haw|he|hi|hif|hif-latn|hil|ho|hr|hrx|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ike-cans|ike-latn|ilo|inh|io|is|it|iu|ja|jam|jbo|jut|jv|ka|kaa|kab|kbd|kbd-cyrl|kea|kg|khw|ki|kiu|kj|kk|kk-arab|kk-cn|kk-cyrl|kk-kz|kk-latn|kk-tr|kl|km|kn|ko|ko-kp|koi|kr|krc|kri|krj|krl|ks|ks-arab|ks-deva|ksh|ku|ku-arab|ku-latn|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|liv|lki|lmo|ln|lo|loz|lrc|lt|ltg|lus|luz|lv|lzh|lzz|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|nap|nb|nds|nds-nl|ne|new|ng|niu|nl|nl-informal|nn|no|nod|nov|nrm|nso|nv|ny|nys|oc|olo|om|or|os|ota|pa|pag|pam|pap|pcd|pdc|pdt|pfl|pi|pih|pl|pms|pnb|pnt|prg|ps|pt|pt-br|qu|qug|rgn|rif|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|ruq|ruq-cyrl|ruq-latn|rw|rwr|sa|sah|sat|sc|scn|sco|sd|sdc|sdh|se|sei|ses|sg|sgs|sh|shi|shi-latn|shi-tfng|shn|si|simple|sje|sk|sl|sli|sm|sma|smj|sn|so|sq|sr|sr-ec|sr-el|srn|srq|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|tg-cyrl|tg-latn|th|ti|tk|tl|tly|tn|to|tokipona|tpi|tr|tru|ts|tt|tt-cyrl|tt-latn|tum|tw|ty|tyv|tzm|udm|ug|ug-arab|ug-latn|uk|ur|uz|uz-cyrl|uz-latn|ve|vec|vep|vi|vls|vmf|vo|vot|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|za|zea|zh|zh-classical|zh-cn|zh-hans|zh-hant|zh-hk|zh-min-nan|zh-mo|zh-my|zh-sg|zh-tw|zh-yue|zu):/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_07f8e639, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_1f90813f, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_6313f817, mapcss._tag_capture(capture_tags, 2, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia tag has an unknown language prefix")
            err.append({'class': 9011002, 'subclass': 1499670292, 'text': mapcss.tr(u'wikipedia tag has an unknown language prefix', capture_tags)})

        # *[wikipedia=~/^https?:\/\//]
        # *[wikipedia=~/(?i)^[-a-z]{2,12}:https?:\/\//]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_1f90813f, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'))) or \
            (mapcss.regexp_test_(self.re_091c4afa, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # group:tr("deprecated tagging")
            # suggestAlternative:tr("''wikipedia''=''language:page title''")
            # throwWarning:tr("wikipedia tag format is deprecated")
            err.append({'class': 9011003, 'subclass': 75691825, 'text': mapcss.tr(u'wikipedia tag format is deprecated', capture_tags)})

        # *[wikipedia=~/^be-x-old:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_53b6f173, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia ''{0}'' language is obsolete, use ''{1}'' instead","be-x-old","be-tarask")
            # fixAdd:concat("wikipedia=be-tarask:",get(regexp_match("^be-x-old:(.+)$",tag("wikipedia")),1))
            err.append({'class': 9011004, 'subclass': 616152609, 'text': mapcss.tr(u'wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', capture_tags, u'be-x-old', u'be-tarask'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=be-tarask:', mapcss.get(mapcss.regexp_match(self.re_6a4abd53, mapcss.tag(tags, u'wikipedia')), 1))).split('=', 1)])
            }})

        # *[wikipedia=~/^cz:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_034ab801, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia ''{0}'' language is invalid, use ''{1}'' instead","cz","cs")
            # fixAdd:concat("wikipedia=cs:",get(regexp_match("^cz:(.+)$",tag("wikipedia")),1))
            err.append({'class': 9011005, 'subclass': 243392039, 'text': mapcss.tr(u'wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', capture_tags, u'cz', u'cs'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=cs:', mapcss.get(mapcss.regexp_match(self.re_577ca7fb, mapcss.tag(tags, u'wikipedia')), 1))).split('=', 1)])
            }})

        # *[wikimedia_commons=~/%[0-9A-F][0-9A-F]/]
        if (u'wikimedia_commons' in keys) and \
            ((mapcss.regexp_test_(self.re_210c6ccc, mapcss._tag_capture(capture_tags, 0, tags, u'wikimedia_commons')))):
            # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
            # fixAdd:concat("wikimedia_commons=",trim(replace(URL_decode(tag("wikimedia_commons")),"_"," ")))
            err.append({'class': 9011006, 'subclass': 1999051286, 'text': mapcss.tr(u'{0} tag should not have URL-encoded values like \'\'%27\'\'', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikimedia_commons=', mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.tag(tags, u'wikimedia_commons')), u'_', u' ')))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_19995c46, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.tag}")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(replace(URL_decode(get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),2)),"_"," ")))
            err.append({'class': 9011006, 'subclass': 83644825, 'text': mapcss.tr(u'{0} tag should not have URL-encoded values like \'\'%27\'\'', capture_tags, u'{0.tag}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 2)), u'_', u' ')))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}: /]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_536e5b67, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia title should not start with a space after language code")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),2)))
            err.append({'class': 9011007, 'subclass': 1273458928, 'text': mapcss.tr(u'wikipedia title should not start with a space after language code', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 2)))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:wiki\//]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_67c3b565, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia title should not have ''{0}'' prefix","wiki/")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),1),trim(get(regexp_match("^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),2)))
            err.append({'class': 9011008, 'subclass': 696665203, 'text': mapcss.tr(u'wikipedia title should not have \'\'{0}\'\' prefix', capture_tags, u'wiki/'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_290a9471, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_290a9471, mapcss.tag(tags, u'wikipedia')), 2)))).split('=', 1)])
            }})

        # *[wikipedia=~/^[-a-zA-Z]{2,12}:\p{Ll}/][wikipedia!~/^jbo:/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_5940ff7c, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_1ac7f364, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_2d3d5d3d, mapcss._tag_capture(capture_tags, 2, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia page title should have first letter capitalized")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),1),upper(get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),2)),get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),3))
            err.append({'class': 9011009, 'subclass': 1824269684, 'text': mapcss.tr(u'wikipedia page title should have first letter capitalized', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 1), mapcss.upper(mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 2)), mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 3))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*_/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_08b52119, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_2d3d5d3d, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia page title should have spaces instead of underscores (''_''→'' '')")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),1),trim(replace(get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),2),"_"," ")))
            err.append({'class': 9011010, 'subclass': 2024856824, 'text': mapcss.tr(u'wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 2), u'_', u' ')))).split('=', 1)])
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
        if (u'wikipedia' in keys) and \
            ((mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'da:da:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'da:dk:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'de:de:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'dk:dk:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:de:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:en:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:es:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:eu:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:ja:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:pl:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:pt:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:zh:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'es:es:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'eu:eu:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'fr:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ja:ja:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pl:en:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pl:pl:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pt:pt:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ru:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ru:ru:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'zh:zh:'))):
            # throwWarning:tr("wikipedia language seems to be duplicated, e.g. en:en:Foo")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),2),trim(get(regexp_match("^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),3)))
            err.append({'class': 9011011, 'subclass': 124114060, 'text': mapcss.tr(u'wikipedia language seems to be duplicated, e.g. en:en:Foo', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1825d91f, mapcss.tag(tags, u'wikipedia')), 2), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_1825d91f, mapcss.tag(tags, u'wikipedia')), 3)))).split('=', 1)])
            }})

        # *[wikidata][wikidata!~/^Q[1-9][0-9]{0,8}$/]
        if (u'wikidata' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikidata') and not mapcss.regexp_test_(self.re_4b567f18, mapcss._tag_capture(capture_tags, 1, tags, u'wikidata')))):
            # throwError:tr("wikidata tag must be in Qnnnn format, where n is a digit")
            err.append({'class': 9011012, 'subclass': 1398622919, 'text': mapcss.tr(u'wikidata tag must be in Qnnnn format, where n is a digit', capture_tags)})

        # *[wikipedia][!wikidata]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss._tag_capture(capture_tags, 1, tags, u'wikidata'))):
            # group:tr("missing tag")
            # throwOther:tr("wikipedia tag is set, but there is no wikidata tag. Wikipedia plugin might help with wikidata id lookups")
            err.append({'class': 9011013, 'subclass': 52215017, 'text': mapcss.tr(u'wikipedia tag is set, but there is no wikidata tag. Wikipedia plugin might help with wikidata id lookups', capture_tags)})

        # *[!wikipedia][/^wikipedia:/]
        if ((not mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and mapcss._tag_capture(capture_tags, 1, tags, self.re_79319bf9))):
            # throwWarning:tr("wikipedia tag is not set, but a ''{0}'' tag is. Make sure to use wikipedia=language:value together with wikidata tag.","{1.key}")
            err.append({'class': 9011014, 'subclass': 153018468, 'text': mapcss.tr(u'wikipedia tag is not set, but a \'\'{0}\'\' tag is. Make sure to use wikipedia=language:value together with wikidata tag.', capture_tags, u'{1.key}')})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[wikipedia][wikipedia!~/(?i)^[-a-z]{2,12}:/]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(self.re_07f8e639, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwError:tr("wikipedia tag has no language given, use ''wikipedia''=''language:page title''")
            err.append({'class': 9011001, 'subclass': 1517450396, 'text': mapcss.tr(u'wikipedia tag has no language given, use \'\'wikipedia\'\'=\'\'language:page title\'\'', capture_tags)})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:/][wikipedia!~/^https?:\/\//][wikipedia!~/^(aa|ab|ace|ady|ady-cyrl|aeb|aeb-arab|aeb-latn|af|ak|aln|als|am|an|ang|anp|ar|arc|arn|arq|ary|arz|as|ase|ast|av|avk|awa|ay|az|azb|ba|ban|bar|bat-smg|bbc|bbc-latn|bcc|bcl|be|be-tarask|be-x-old|bg|bgn|bh|bho|bi|bjn|bm|bn|bo|bpy|bqi|br|brh|bs|bto|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cps|cr|crh|crh-cyrl|crh-latn|cs|csb|cu|cv|cy|cz|da|de|de-at|de-ch|de-formal|din|diq|dsb|dtp|dty|dv|dz|ee|egl|el|eml|en|en-ca|en-gb|eo|es|et|eu|ext|fa|ff|fi|fit|fiu-vro|fj|fo|fr|frc|frp|frr|fur|fy|ga|gag|gan|gan-hans|gan-hant|gd|gl|glk|gn|gom|gom-deva|gom-latn|gor|got|grc|gsw|gu|gv|ha|hak|haw|he|hi|hif|hif-latn|hil|ho|hr|hrx|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ike-cans|ike-latn|ilo|inh|io|is|it|iu|ja|jam|jbo|jut|jv|ka|kaa|kab|kbd|kbd-cyrl|kea|kg|khw|ki|kiu|kj|kk|kk-arab|kk-cn|kk-cyrl|kk-kz|kk-latn|kk-tr|kl|km|kn|ko|ko-kp|koi|kr|krc|kri|krj|krl|ks|ks-arab|ks-deva|ksh|ku|ku-arab|ku-latn|kv|kw|ky|la|lad|lb|lbe|lez|lfn|lg|li|lij|liv|lki|lmo|ln|lo|loz|lrc|lt|ltg|lus|luz|lv|lzh|lzz|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|nap|nb|nds|nds-nl|ne|new|ng|niu|nl|nl-informal|nn|no|nod|nov|nrm|nso|nv|ny|nys|oc|olo|om|or|os|ota|pa|pag|pam|pap|pcd|pdc|pdt|pfl|pi|pih|pl|pms|pnb|pnt|prg|ps|pt|pt-br|qu|qug|rgn|rif|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|ruq|ruq-cyrl|ruq-latn|rw|rwr|sa|sah|sat|sc|scn|sco|sd|sdc|sdh|se|sei|ses|sg|sgs|sh|shi|shi-latn|shi-tfng|shn|si|simple|sje|sk|sl|sli|sm|sma|smj|sn|so|sq|sr|sr-ec|sr-el|srn|srq|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|tg-cyrl|tg-latn|th|ti|tk|tl|tly|tn|to|tokipona|tpi|tr|tru|ts|tt|tt-cyrl|tt-latn|tum|tw|ty|tyv|tzm|udm|ug|ug-arab|ug-latn|uk|ur|uz|uz-cyrl|uz-latn|ve|vec|vep|vi|vls|vmf|vo|vot|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|za|zea|zh|zh-classical|zh-cn|zh-hans|zh-hant|zh-hk|zh-min-nan|zh-mo|zh-my|zh-sg|zh-tw|zh-yue|zu):/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_07f8e639, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_1f90813f, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_6313f817, mapcss._tag_capture(capture_tags, 2, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia tag has an unknown language prefix")
            err.append({'class': 9011002, 'subclass': 1499670292, 'text': mapcss.tr(u'wikipedia tag has an unknown language prefix', capture_tags)})

        # *[wikipedia=~/^https?:\/\//]
        # *[wikipedia=~/(?i)^[-a-z]{2,12}:https?:\/\//]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_1f90813f, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'))) or \
            (mapcss.regexp_test_(self.re_091c4afa, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # group:tr("deprecated tagging")
            # suggestAlternative:tr("''wikipedia''=''language:page title''")
            # throwWarning:tr("wikipedia tag format is deprecated")
            err.append({'class': 9011003, 'subclass': 75691825, 'text': mapcss.tr(u'wikipedia tag format is deprecated', capture_tags)})

        # *[wikipedia=~/^be-x-old:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_53b6f173, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia ''{0}'' language is obsolete, use ''{1}'' instead","be-x-old","be-tarask")
            # fixAdd:concat("wikipedia=be-tarask:",get(regexp_match("^be-x-old:(.+)$",tag("wikipedia")),1))
            err.append({'class': 9011004, 'subclass': 616152609, 'text': mapcss.tr(u'wikipedia \'\'{0}\'\' language is obsolete, use \'\'{1}\'\' instead', capture_tags, u'be-x-old', u'be-tarask'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=be-tarask:', mapcss.get(mapcss.regexp_match(self.re_6a4abd53, mapcss.tag(tags, u'wikipedia')), 1))).split('=', 1)])
            }})

        # *[wikipedia=~/^cz:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_034ab801, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia ''{0}'' language is invalid, use ''{1}'' instead","cz","cs")
            # fixAdd:concat("wikipedia=cs:",get(regexp_match("^cz:(.+)$",tag("wikipedia")),1))
            err.append({'class': 9011005, 'subclass': 243392039, 'text': mapcss.tr(u'wikipedia \'\'{0}\'\' language is invalid, use \'\'{1}\'\' instead', capture_tags, u'cz', u'cs'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=cs:', mapcss.get(mapcss.regexp_match(self.re_577ca7fb, mapcss.tag(tags, u'wikipedia')), 1))).split('=', 1)])
            }})

        # *[wikimedia_commons=~/%[0-9A-F][0-9A-F]/]
        if (u'wikimedia_commons' in keys) and \
            ((mapcss.regexp_test_(self.re_210c6ccc, mapcss._tag_capture(capture_tags, 0, tags, u'wikimedia_commons')))):
            # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.key}")
            # fixAdd:concat("wikimedia_commons=",trim(replace(URL_decode(tag("wikimedia_commons")),"_"," ")))
            err.append({'class': 9011006, 'subclass': 1999051286, 'text': mapcss.tr(u'{0} tag should not have URL-encoded values like \'\'%27\'\'', capture_tags, u'{0.key}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikimedia_commons=', mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.tag(tags, u'wikimedia_commons')), u'_', u' ')))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*%[0-9A-F][0-9A-F]/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_19995c46, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwError:tr("{0} tag should not have URL-encoded values like ''%27''","{0.tag}")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(replace(URL_decode(get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),2)),"_"," ")))
            err.append({'class': 9011006, 'subclass': 83644825, 'text': mapcss.tr(u'{0} tag should not have URL-encoded values like \'\'%27\'\'', capture_tags, u'{0.tag}'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.URL_decode(mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 2)), u'_', u' ')))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}: /]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_536e5b67, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia title should not start with a space after language code")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),1),trim(get(regexp_match("^([-a-z]+:)(.*)$",tag("wikipedia")),2)))
            err.append({'class': 9011007, 'subclass': 1273458928, 'text': mapcss.tr(u'wikipedia title should not start with a space after language code', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_70a0064f, mapcss.tag(tags, u'wikipedia')), 2)))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:wiki\//]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_67c3b565, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia title should not have ''{0}'' prefix","wiki/")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),1),trim(get(regexp_match("^([-a-z]+:)wiki/(.*)$",tag("wikipedia")),2)))
            err.append({'class': 9011008, 'subclass': 696665203, 'text': mapcss.tr(u'wikipedia title should not have \'\'{0}\'\' prefix', capture_tags, u'wiki/'), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_290a9471, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_290a9471, mapcss.tag(tags, u'wikipedia')), 2)))).split('=', 1)])
            }})

        # *[wikipedia=~/^[-a-zA-Z]{2,12}:\p{Ll}/][wikipedia!~/^jbo:/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_5940ff7c, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_1ac7f364, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_2d3d5d3d, mapcss._tag_capture(capture_tags, 2, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia page title should have first letter capitalized")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),1),upper(get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),2)),get(regexp_match("^([-a-z]+:)(.)(.*)$",tag("wikipedia")),3))
            err.append({'class': 9011009, 'subclass': 1824269684, 'text': mapcss.tr(u'wikipedia page title should have first letter capitalized', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 1), mapcss.upper(mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 2)), mapcss.get(mapcss.regexp_match(self.re_450fb7f8, mapcss.tag(tags, u'wikipedia')), 3))).split('=', 1)])
            }})

        # *[wikipedia=~/(?i)^[-a-z]{2,12}:.*_/][wikipedia!~/(?i)^[-a-z]{2,12}:https?:/]
        if (u'wikipedia' in keys) and \
            ((mapcss.regexp_test_(self.re_08b52119, mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia')) and not mapcss.regexp_test_(self.re_2d3d5d3d, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwWarning:tr("wikipedia page title should have spaces instead of underscores (''_''→'' '')")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),1),trim(replace(get(regexp_match("^([-a-z]+:)(.+)$",tag("wikipedia")),2),"_"," ")))
            err.append({'class': 9011010, 'subclass': 2024856824, 'text': mapcss.tr(u'wikipedia page title should have spaces instead of underscores (\'\'_\'\'→\'\' \'\')', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 1), mapcss.trim(mapcss.replace(mapcss.get(mapcss.regexp_match(self.re_1478a0ca, mapcss.tag(tags, u'wikipedia')), 2), u'_', u' ')))).split('=', 1)])
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
        if (u'wikipedia' in keys) and \
            ((mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'da:da:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'da:dk:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'de:de:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'dk:dk:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:de:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:en:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:es:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:eu:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:ja:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:pl:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:pt:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'en:zh:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'es:es:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'eu:eu:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'fr:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ja:ja:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pl:en:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pl:pl:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'pt:pt:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ru:fr:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'ru:ru:')) or \
            (mapcss.startswith(mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia'), u'zh:zh:'))):
            # throwWarning:tr("wikipedia language seems to be duplicated, e.g. en:en:Foo")
            # fixAdd:concat("wikipedia=",get(regexp_match("^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),2),trim(get(regexp_match("^([-a-z]+:)([-a-z]+:)(.*)$",tag("wikipedia")),3)))
            err.append({'class': 9011011, 'subclass': 124114060, 'text': mapcss.tr(u'wikipedia language seems to be duplicated, e.g. en:en:Foo', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'wikipedia=', mapcss.get(mapcss.regexp_match(self.re_1825d91f, mapcss.tag(tags, u'wikipedia')), 2), mapcss.trim(mapcss.get(mapcss.regexp_match(self.re_1825d91f, mapcss.tag(tags, u'wikipedia')), 3)))).split('=', 1)])
            }})

        # *[wikidata][wikidata!~/^Q[1-9][0-9]{0,8}$/]
        if (u'wikidata' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikidata') and not mapcss.regexp_test_(self.re_4b567f18, mapcss._tag_capture(capture_tags, 1, tags, u'wikidata')))):
            # throwError:tr("wikidata tag must be in Qnnnn format, where n is a digit")
            err.append({'class': 9011012, 'subclass': 1398622919, 'text': mapcss.tr(u'wikidata tag must be in Qnnnn format, where n is a digit', capture_tags)})

        # *[wikipedia][!wikidata]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss._tag_capture(capture_tags, 1, tags, u'wikidata'))):
            # group:tr("missing tag")
            # throwOther:tr("wikipedia tag is set, but there is no wikidata tag. Wikipedia plugin might help with wikidata id lookups")
            err.append({'class': 9011013, 'subclass': 52215017, 'text': mapcss.tr(u'wikipedia tag is set, but there is no wikidata tag. Wikipedia plugin might help with wikidata id lookups', capture_tags)})

        # *[!wikipedia][/^wikipedia:/]
        if ((not mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and mapcss._tag_capture(capture_tags, 1, tags, self.re_79319bf9))):
            # throwWarning:tr("wikipedia tag is not set, but a ''{0}'' tag is. Make sure to use wikipedia=language:value together with wikidata tag.","{1.key}")
            err.append({'class': 9011014, 'subclass': 153018468, 'text': mapcss.tr(u'wikipedia tag is not set, but a \'\'{0}\'\' tag is. Make sure to use wikipedia=language:value together with wikidata tag.', capture_tags, u'{1.key}')})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_wikipedia(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        self.check_err(n.node(data, {u'wikipedia': u'Foobar'}), expected={'class': 9011001, 'subclass': 1517450396})
        self.check_not_err(n.node(data, {u'wikipedia': u'en-GB:Foobar'}), expected={'class': 9011001, 'subclass': 1517450396})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:Foobar'}), expected={'class': 9011001, 'subclass': 1517450396})
        self.check_err(n.node(data, {u'wikipedia': u'X-Y-Z:Foobar'}), expected={'class': 9011002, 'subclass': 1499670292})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:Foobar'}), expected={'class': 9011002, 'subclass': 1499670292})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:OpenStreetMap'}), expected={'class': 9011003, 'subclass': 75691825})
        self.check_err(n.node(data, {u'wikipedia': u'http://en.wikipedia.org/wiki/OpenStreetMap'}), expected={'class': 9011003, 'subclass': 75691825})
        self.check_not_err(n.node(data, {u'wikipedia': u'abe-x-old:foo'}), expected={'class': 9011004, 'subclass': 616152609})
        self.check_err(n.node(data, {u'wikipedia': u'be-x-old:foo'}), expected={'class': 9011004, 'subclass': 616152609})
        self.check_err(n.node(data, {u'wikipedia': u'cz:foo'}), expected={'class': 9011005, 'subclass': 243392039})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:cz:foo'}), expected={'class': 9011005, 'subclass': 243392039})
        self.check_err(n.node(data, {u'wikimedia_commons': u'File:Foo%27s'}), expected={'class': 9011006, 'subclass': 1999051286})
        self.check_not_err(n.node(data, {u'wikimedia_commons': u'File:Foo'}), expected={'class': 9011006, 'subclass': 1999051286})
        self.check_err(n.node(data, {u'wikipedia': u'en:Foo%27s'}), expected={'class': 9011006, 'subclass': 83644825})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:Foo'}), expected={'class': 9011006, 'subclass': 83644825})
        self.check_err(n.node(data, {u'wikipedia': u'en: foo'}), expected={'class': 9011007, 'subclass': 1273458928})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:foo'}), expected={'class': 9011007, 'subclass': 1273458928})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:foo'}), expected={'class': 9011008, 'subclass': 696665203})
        self.check_err(n.node(data, {u'wikipedia': u'en:wiki/foo'}), expected={'class': 9011008, 'subclass': 696665203})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:Foo'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_err(n.node(data, {u'wikipedia': u'en:foo'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_not_err(n.node(data, {u'wikipedia': u'ru:Абв'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_err(n.node(data, {u'wikipedia': u'ru:абв'}), expected={'class': 9011009, 'subclass': 1824269684})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:foo bar'}), expected={'class': 9011010, 'subclass': 2024856824})
        self.check_err(n.node(data, {u'wikipedia': u'en:foo_bar'}), expected={'class': 9011010, 'subclass': 2024856824})
        self.check_not_err(n.node(data, {u'wikipedia': u'en:Bar'}), expected={'class': 9011011, 'subclass': 124114060})
        self.check_err(n.node(data, {u'wikipedia': u'en:en:Foo'}), expected={'class': 9011011, 'subclass': 124114060})
        self.check_err(n.node(data, {u'wikipedia': u'en:fr:Foo'}), expected={'class': 9011011, 'subclass': 124114060})
        self.check_err(n.node(data, {u'wikidata': u'Q'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_err(n.node(data, {u'wikidata': u'Q0'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_err(n.node(data, {u'wikidata': u'Q0123'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_not_err(n.node(data, {u'wikidata': u'Q1'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_not_err(n.node(data, {u'wikidata': u'Q123'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_err(n.node(data, {u'wikidata': u'a'}), expected={'class': 9011012, 'subclass': 1398622919})
        self.check_not_err(n.node(data, {u'foo': u'bar'}), expected={'class': 9011013, 'subclass': 52215017})
        self.check_not_err(n.node(data, {u'wikidata': u'Q1'}), expected={'class': 9011013, 'subclass': 52215017})
        self.check_not_err(n.node(data, {u'wikidata': u'Q123', u'wikipedia': u'a'}), expected={'class': 9011013, 'subclass': 52215017})
        self.check_err(n.node(data, {u'wikipedia': u'a'}), expected={'class': 9011013, 'subclass': 52215017})
        self.check_err(n.node(data, {u'wikipedia:en': u'a'}), expected={'class': 9011014, 'subclass': 153018468})
        self.check_not_err(n.node(data, {u'wikipedia': u'Foo'}), expected={'class': 9011014, 'subclass': 153018468})
        self.check_not_err(n.node(data, {u'wikipedia': u'a', u'wikipedia:en': u'b'}), expected={'class': 9011014, 'subclass': 153018468})
