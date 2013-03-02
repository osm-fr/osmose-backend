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
import urllib


class TagFix_Wikipedia(Plugin):
    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[30310] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia"], "desc": {"en": u"Not a Wikipedia URL", "fr": u"L'URL n'appartient pas au domaine wikipedia."} }
        self.errors[30311] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia"], "desc": {"en": u"Use Wikipedia title instead of an url", "fr": u"Utilisez le titre de l'article plutôt que l'URL"} }
        self.errors[30312] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia"], "desc": {"en": u"Missing Wikipedia language before article title", "fr": u"Le nom de l'article wikipedia doit-être prefixé par un code langue ('fr:' par exemple)"} }
        self.errors[30313] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia"], "desc": {"en": u"Use human Wikipedia page title"}, "fr": u"Utilisez le nom tel qu'il apparait dans l'article, et non telqu'il apparait dans l'URL de la page" }
        self.errors[30314] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia"], "desc": {"en": u"Missing primary Wikipedia tag", "fr": u"Un tag 'wikipedia' doit être présent avant d'utiliser des tags 'wikipedia:LANG'"} }
        self.errors[30315] = { "item": 3031, "level": 2, "tag": ["value", "wikipedia"], "desc": {"en": u"Invalid wikipedia sufix", "fr": u"Utilisation incorrect d'un tag 'wikipedia:xxx', xxx devrait être un autre attribut ou un code langue"} }

        import re
        self.wiki_regexp = re.compile(u"(https?://)?([^\.]+)\.wikipedia.+/wiki/(.+)")
        self.lang_regexp = re.compile(u"[-a-z]+:.*")
        self.lang = ["en", "de", "fr", "nl", "it", "es", "pl", "ru", "ja", "pt", "zh", "sv", "vi", "uk", "ca", "no", "fi", "cs", "fa", "hu", "ko", "ro", "id", "ar", "tr", "kk", "sk", "eo", "da", "sr", "lt", "eu", "ms", "he", "bg", "sl", "vo", "hr", "war", "hi", "et", "br"]

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
            if "%" in tags[wikipediaTag] or "_" in tags[wikipediaTag]:
                err.append((30313, 3, {"fix": {wikipediaTag: self.human_readable(tags[wikipediaTag])}} ))

        for tag in [t for t in tags if t.startswith(wikipediaTag+":")]:
            sufix = tag[len(wikipediaTag)+1:]
            if ":" in sufix:
            	sufix = sufix.split(":")[0]
            
            if sufix in tags:
                # wikipedia:xxxx only authorized if tag xxxx exist
                err.extend(self.analyse(tags, wikipediaTag+":"+sufix))
            
            elif sufix in self.lang:
                if not wikipediaTag in tags:
                    m = self.wiki_regexp.match(tags[tag])
                    if m:
                        value = self.human_readable(m.group(3))
                    elif tags[tag].startswith(sufix+":"):
                    	value = tags[tag][len(sufix)+1:]
                    else:
                        value = self.human_readable(tags[tag])
                    err.append((30314, 4, {"fix": {'-': [tag], '+':{wikipediaTag: "%s:%s" % (sufix, value)}}} ))
            else:
            	err.append((30315, 5, {"en": u"Invalid wikipedia sufix '%s'" % sufix} ))
        return err

    def node(self, data, tags):
        return self.analyse(tags)
    
    def way(self, data, tags, nds):
        return self.analyse(tags)

    def relation(self, data, tags, members):
        return self.analyse(tags)

# Test unitaires
if __name__ == "__main__":
    analyser = TagFix_Wikipedia(None)
    analyser.init(None)
    err = 0
    
    def check(tags, has_error, fix=None):
        global err
        errors = analyser.analyse(tags)
        errors_msg = [analyser.errors[e[0]]["desc"]["en"] for e in errors]+[e[2]["en"] for e in errors if "en" in e[2]]
        errors_fix = [e[2].get("fix") for e in errors]
        if has_error==False and errors_msg:
            print "FAIL:%s\nshould not have errors\nCurrent errors: %s\n"%(tags, errors_msg)
            err += 1
        if has_error and has_error not in errors_msg:
            print "FAIL:%s\nshould have error '%s'\ninstead of      %s\n"%(tags, has_error, errors_msg)
            err += 1
        if fix and fix not in errors_fix:
            print "FAIL:%s\nshould have fix %s\ninstead of     %s\n"%(tags, fix, errors_fix)
            err += 1
    
    
    check( { "wikipedia": "fr:Tour Eiffel"},
    	has_error = False)
    
    check( { "wikipedia": "fr:Tour Eiffel",
    		 "wikipedia:de" : "Eiffelturm"},
    	has_error = False)
    	# add check on synonyme
    
    # Don't use URL directly
    check( { "wikipedia": "http://www.google.fr"},
     	has_error = "Not a Wikipedia URL")
     	
    check( { "wikipedia": "http://fr.wikipedia.org/wiki/Tour_Eiffel"},
     	has_error = "Use Wikipedia title instead of an url",
     	fix = { "wikipedia": u"fr:Tour Eiffel"})
    
    check( { "wikipedia": "https://fr.wikipedia.org/wiki/Tour_Eiffel"},
     	has_error = "Use Wikipedia title instead of an url",
     	fix = { "wikipedia": u"fr:Tour Eiffel"})
    
    check( { "wikipedia": "fr.wikipedia.org/wiki/Tour_Eiffel"},
     	has_error = "Use Wikipedia title instead of an url",
     	fix = { "wikipedia": u"fr:Tour Eiffel"})
    
    # Tag 'wikipedia:lang' can be used only in complement of 'wikipedia=lang:xxxx'
    check( {"wikipedia:fr" : u"Tour Eiffel"},
     	has_error = u"Missing primary Wikipedia tag",
     	fix = {'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})
    
    check( {"wikipedia:fr" : u"fr:Tour Eiffel"},
     	has_error = u"Missing primary Wikipedia tag",
     	fix = {'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})
    
    check( { "wikipedia:fr": "http://fr.wikipedia.org/wiki/Tour_Eiffel"},
     	has_error = u"Missing primary Wikipedia tag",
     	fix = {'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})
     	
    check( { "wikipedia:fr": "fr.wikipedia.org/wiki/Tour_Eiffel"},
     	has_error = u"Missing primary Wikipedia tag",
     	fix = {'+': {'wikipedia': u'fr:Tour Eiffel'}, '-': ['wikipedia:fr']})
     
    # Missing lang in value
    check( { "wikipedia": "Tour Eiffel"},
    	has_error = u"Missing Wikipedia language before article title")
    
    # Human readeable
    check( { "wikipedia": "fr:Tour_Eiffel"},
    	has_error = u"Use human Wikipedia page title",
    	fix = { "wikipedia": u"fr:Tour Eiffel"})
	
    check( { "wikipedia": u"fr:Château_de_Gruyères_(Ardennes)"},
    	has_error = u"Use human Wikipedia page title",
    	fix = { "wikipedia": u"fr:Château de Gruyères (Ardennes)"})
    
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name": "fr:Jules Verne"},
    	has_error = False)
    
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name": "fr:Jules Verne",
    		 "wikipedia:name:de" : "Jules Verne"},
    	has_error = False)
    
    # Don't use URL directly
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name": "http://www.google.fr"},
     	has_error = "Not a Wikipedia URL")
    
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name": "http://fr.wikipedia.org/wiki/Jules_Verne"},
     	has_error = "Use Wikipedia title instead of an url",
     	fix = { "wikipedia:name": u"fr:Jules Verne"})	
    
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name": "fr.wikipedia.org/wiki/Jules_Verne"},
     	has_error = "Use Wikipedia title instead of an url",
     	fix = { "wikipedia:name": u"fr:Jules Verne"})
    
    # Tag 'wikipedia:lang' can be used only in complement of 'wikipedia=lang:xxxx'
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name:fr" : u"Jules Verne"},
     	has_error = u"Missing primary Wikipedia tag",
     	fix = {'+': {'wikipedia:name': u'fr:Jules Verne'}, '-': ['wikipedia:name:fr']})
    
    # Missing lang in value
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name": "Jules Verne"},
    	has_error = u"Missing Wikipedia language before article title")
    
    # Human readeable
    check( { "name" : "Rue Jules Verne",
    		 "wikipedia:name": "fr:Jules_Verne"},
    	has_error = u"Use human Wikipedia page title",
    	fix = { "wikipedia:name": u"fr:Jules Verne"})
    
    check( { "name" : "Gare SNCF",
    		 "operator": "Sncf",
    		 "wikipedia:operator": "fr:Sncf"},
    	has_error = False)
    
    check( { "wikipedia:toto": "quelque chose"},
    	has_error = u"Invalid wikipedia sufix 'toto'")

    if err:
        print "%i errors" % err
    else:
        print "all success"