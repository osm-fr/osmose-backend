#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from plugins.Plugin import Plugin
from modules.downloader import urlread
import urllib
import json


class TagFix_Wikipedia(Plugin):
    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30310] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Not a Wikipedia URL") }
        self.errors[30311] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Wikipedia URL instead of article title") }
        self.errors[30312] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Missing Wikipedia language before article title") }
        self.errors[30313] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Use human Wikipedia page title") }
        self.errors[30314] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Missing primary Wikipedia tag") }
        self.errors[30315] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Invalid wikipedia suffix") }
        self.errors[30316] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Duplicate wikipedia tag as suffix and prefix") }
        self.errors[30317] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia", "fix:chair"], "desc": T_(u"Same wikipedia topic on other language") }

        import re
        self.wiki_regexp = re.compile(u"(https?://)?([^\.]+)\.wikipedia.+/wiki/(.+)")
        self.lang_regexp = re.compile(u"[-a-z]+:.*")
        self.lang_restriction_regexp = re.compile(u"^[a-z]{2}$")

        self.Language = self.father.config.options.get("language")

    def human_readable(self, string):
        try:
            string = urllib.unquote(string.encode('ascii')).decode('utf8')
        except:
            pass
        return string.replace("_"," ")

    def analyse(self, tags, wikipediaTag="wikipedia"):
        err=[]
        if wikipediaTag in tags:
            m = self.wiki_regexp.match(tags[wikipediaTag])
            if (tags[wikipediaTag].startswith("http://") or tags[wikipediaTag].startswith("https://")) and not m:
                # tag 'wikipedia' starts with 'http://' but it's not a wikipedia url
                return [(30310, 0, {})]
            elif m:
                # tag 'wikipedia' seams to be an url
                return [(30311, 1, {"en": u"Use wikipedia=%s:*" % m.group(2), "fix": {wikipediaTag: "%s:%s" % (m.group(2), self.human_readable(m.group(3)))} })]

            if not self.lang_regexp.match(tags[wikipediaTag]):
                err.append((30312, 2, {}))
            else:
                prefix = tags[wikipediaTag].split(':', 1)[0]
                tag = wikipediaTag+':'+prefix
                if tag in tags:
                    err.append((30316, 6, {"fix": {'-': [tag]}} ))
            if "%" in tags[wikipediaTag] or "_" in tags[wikipediaTag]:
                err.append((30313, 3, {"fix": {wikipediaTag: self.human_readable(tags[wikipediaTag])}} ))

        interwiki = False
        missing_primary = []
        for tag in [t for t in tags if t.startswith(wikipediaTag+":")]:
            suffix = tag[len(wikipediaTag)+1:]
            if ":" in suffix:
                suffix = suffix.split(":")[0]

            if wikipediaTag in tags:
                if interwiki == False:
                    try:
                        lang, title = tags[wikipediaTag].split(':')
                        json_str = urlread("http://"+lang+".wikipedia.org/w/api.php?action=query&prop=langlinks&titles="+urllib.quote(title.encode('utf-8'))+"&redirects=&lllimit=500&format=json" , 30)
                        interwiki = json.loads(json_str)
                        interwiki = dict(map(lambda x: [x["lang"], x["*"]], interwiki["query"]["pages"].values()[0]["langlinks"]))
                    except:
                        interwiki = None

                    if interwiki and suffix in interwiki and interwiki[suffix] == self.human_readable(tags[tag]):
                        err.append((30317, 7, {"fix": [
                            {'-': [tag]},
                            {'-': [tag], '~': {wikipediaTag: suffix+':'+interwiki[suffix]}}
                        ]} ))

            if suffix in tags:
                # wikipedia:xxxx only authorized if tag xxxx exist
                err.extend(self.analyse(tags, wikipediaTag+":"+suffix))

            elif self.lang_restriction_regexp.match(suffix):
                if not wikipediaTag in tags:
                    m = self.wiki_regexp.match(tags[tag])
                    if m:
                        value = self.human_readable(m.group(3))
                    elif tags[tag].startswith(suffix+":"):
                        value = tags[tag][len(suffix)+1:]
                    else:
                        value = self.human_readable(tags[tag])
                    missing_primary.append({'-': [tag], '+':{wikipediaTag: "%s:%s" % (suffix, value)}})
            else:
                err.append((30315, 5, {"en": u"Invalid wikipedia suffix '%s'" % suffix} ))

        if missing_primary != []:
          if self.Language:
            missing_primary = sorted(missing_primary, key=lambda x: x['+'][wikipediaTag][0:2] if x['+'][wikipediaTag][0:2] != self.Language else '')
          err.append((30314, 4, {"fix": missing_primary} ))

        return err

    def node(self, data, tags):
        return self.analyse(tags)

    def way(self, data, tags, nds):
        return self.analyse(tags)

    def relation(self, data, tags, members):
        return self.analyse(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def setUp(self):
        TestPluginCommon.setUp(self)
        self.analyser = TagFix_Wikipedia(None)
        class _config:
            options = {"language": "fr"}
        class father:
            config = _config()
        self.analyser.father = father()
        self.analyser.init(None)

    def check(self, tags, has_error, fix=None):
        errors = self.analyser.analyse(tags)
        errors_msg = [self.analyser.errors[e[0]]["desc"]["en"] for e in errors]+[e[2]["en"] for e in errors if "en" in e[2]]
        errors_fix = []
        for e in errors:
            if isinstance(e[2].get("fix"), list):
                errors_fix.extend(e[2].get("fix"))
            else:
                errors_fix.append(e[2].get("fix"))
        if has_error==False and errors_msg:
            print "FAIL:%s\nshould not have errors\nCurrent errors: %s\n"%(tags, errors_msg)
            return 1
        if has_error and has_error not in errors_msg:
            print "FAIL:%s\nshould have error '%s'\ninstead of      %s\n"%(tags, has_error, errors_msg)
            return 1
        if fix and isinstance(fix, dict) and fix not in errors_fix:
            print "FAIL:%s\nshould have fix %s\ninstead of     %s\n"%(tags, fix, errors_fix)
            return 1
        if fix and not isinstance(fix, dict):
            for f in fix:
                if f not in errors_fix:
                    print "FAIL:%s\nshould have fix %s\nin     %s\n"%(tags, f, errors_fix)
                    return 1
        if has_error:
            self.check_err(errors, (tags, errors_msg))
        return 0

    def test(self):
        err = 0

        err += self.check( { "wikipedia": "fr:Tour Eiffel"},
                           has_error=False)

        err += self.check( { "wikipedia": "fr:Tour Eiffel",
                             "wikipedia:de" : "Plop"},
                           has_error=False)
        # add check on synonyme

        # Don't use URL directly
        err += self.check( { "wikipedia": "http://www.google.fr"},
                           has_error="Not a Wikipedia URL")

        err += self.check( { "wikipedia": "http://fr.wikipedia.org/wiki/Tour_Eiffel"},
                           has_error="Wikipedia URL instead of article title",
                           fix={ "wikipedia": u"fr:Tour Eiffel"})

        err += self.check( { "wikipedia": "https://fr.wikipedia.org/wiki/Tour_Eiffel"},
                           has_error="Wikipedia URL instead of article title",
                           fix={ "wikipedia": u"fr:Tour Eiffel"})

        err += self.check( { "wikipedia": "fr.wikipedia.org/wiki/Tour_Eiffel"},
                           has_error="Wikipedia URL instead of article title",
                           fix={ "wikipedia": u"fr:Tour Eiffel"})

        # Tag 'wikipedia:lang' can be used only in complement of 'wikipedia=lang:xxxx'
        err += self.check( {"wikipedia:fr" : u"Tour Eiffel"},
                           has_error=u"Missing primary Wikipedia tag",
                           fix={'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})

        err += self.check( {"wikipedia:fr" : u"fr:Tour Eiffel"},
                           has_error=u"Missing primary Wikipedia tag",
                           fix={'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})

        err += self.check( { "wikipedia:fr": "http://fr.wikipedia.org/wiki/Tour_Eiffel"},
                           has_error=u"Missing primary Wikipedia tag",
                           fix={'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})

        err += self.check( { "wikipedia:fr": "fr.wikipedia.org/wiki/Tour_Eiffel"},
                           has_error=u"Missing primary Wikipedia tag",
                           fix={'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})

        err += self.check( { "wikipedia:fr": "fr.wikipedia.org/wiki/Tour_Eiffel", "wikipedia:en": "hey"},
                           has_error=u"Missing primary Wikipedia tag",
                           fix=[{'+': {'wikipedia': u'en:hey'}, '-': ['wikipedia:en']},
                                {'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']}])

        # Missing lang in value
        err += self.check( { "wikipedia": "Tour Eiffel"},
                           has_error=u"Missing Wikipedia language before article title")

        # Human readeable
        err += self.check( { "wikipedia": "fr:Tour_Eiffel"},
                           has_error=u"Use human Wikipedia page title",
                           fix={ "wikipedia": u"fr:Tour Eiffel"})

        err += self.check( { "wikipedia": u"fr:Château_de_Gruyères_(Ardennes)"},
                           has_error=u"Use human Wikipedia page title",
                           fix={ "wikipedia": u"fr:Château de Gruyères (Ardennes)"})

        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name": "fr:Jules Verne"},
                           has_error=False)

        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name": "fr:Jules Verne",
                             "wikipedia:name:de" : "Foo Bar"},
                           has_error=False)

        # Don't use URL directly
        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name": "http://www.google.fr"},
                           has_error="Not a Wikipedia URL")

        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name": "http://fr.wikipedia.org/wiki/Jules_Verne"},
                           has_error="Wikipedia URL instead of article title",
                           fix={ "wikipedia:name": u"fr:Jules Verne"})

        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name": "fr.wikipedia.org/wiki/Jules_Verne"},
                           has_error="Wikipedia URL instead of article title",
                           fix={ "wikipedia:name": u"fr:Jules Verne"})

        # Tag 'wikipedia:lang' can be used only in complement of 'wikipedia=lang:xxxx'
        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name:fr" : u"Jules Verne"},
                           has_error=u"Missing primary Wikipedia tag",
                           fix={'+': {'wikipedia:name': u'fr:Jules Verne'}, '-': ['wikipedia:name:fr']})

        # Missing lang in value
        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name": "Jules Verne"},
                           has_error=u"Missing Wikipedia language before article title")

        # Human readable
        err += self.check( { "name" : "Rue Jules Verne",
                             "wikipedia:name": "fr:Jules_Verne"},
                           has_error=u"Use human Wikipedia page title",
                           fix={ "wikipedia:name": u"fr:Jules Verne"})

        err += self.check( { "name" : "Gare SNCF",
                             "operator": "Sncf",
                             "wikipedia:operator": "fr:Sncf"},
                           has_error=False)

        err += self.check( { "wikipedia:toto": "quelque chose"},
                           has_error=u"Invalid wikipedia suffix 'toto'")

        err += self.check( { "wikipedia:fr": "quelque chose", "wikipedia": "fr:autre chose"},
                           has_error=u"Duplicate wikipedia tag as suffix and prefix")

        # Same wikipedia topic on other language
        err += self.check( {"wikipedia": "fr:Tour Eiffel",
                            "wikipedia:en": "Eiffel Tower"},
                           has_error="Same wikipedia topic on other language",
                           fix=[{"-": ["wikipedia:en"]},
                                {"-": ["wikipedia:en"], "~": {"wikipedia": "en:Eiffel Tower"}}])

        err += self.check( {"wikipedia": "fr:Tour Eiffel",
                            "wikipedia:en": "Plop"},
                           has_error=False)

        if err:
            print "%i errors" % err
        assert not err
