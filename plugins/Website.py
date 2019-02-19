#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Francois Gouget fgouget free.fr 2019                       ##
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


class Website(Plugin):

    URL_TAGS = set((u"contact:website", u"contact:webcam", u"url",
                    u"website", u"website:mobile", u"website:stock"))

    def init(self, logger):
        Plugin.init(self, logger)

        import re
        # From RFC 1738 paragraph 2.1
        self.HasScheme = re.compile(r"^[a-zA-Z0-9.+-]+://")

        self.errors[30931] = {"item": 3093, "level": 2, "tag": ["value", "fix:chair"], "desc": T_(u"The URL contains a space")}
        self.errors[30932] = {"item": 3093, "level": 2, "tag": ["value", "fix:chair"], "desc": T_(u"The URL does not have a valid scheme")}

    def _bad_url(self, tag, tags):
        return T_("Bad URL %(k)s=%(v)s", {"k": tag, "v": tags[tag]})

    def check(self, tags):
        err = []
        for tag in self.URL_TAGS:
            if tag not in tags:
                continue
            url = tags[tag]

            stripped = False
            if ' ' in url:
                url = url.strip()
                if ' ' in url:
                    # We don't know how to fix such a URL: Remove everything
                    # after the space? Encode the space?
                    err.append({"class": 30931, "text": self._bad_url(tag, tags)})
                    continue
                stripped = True

            if self.HasScheme.match(url):
                if stripped:
                    return {"class": 30931, "fix": {tag: url}}
                else:
                    continue
            elif url.startswith('://'):
                url = url[3:]
            elif ':' in url or '//' in url:
                # The URL already contains some sort of broken scheme
                # so it's too complex for us to fix
                err.append({"class": 30932, "text": self._bad_url(tag, tags)})
                continue

            err.append({"class": 30932, "fix": [
                {tag: "https://" + url},
                {tag: "http://" + url}
            ]})

        return err

    def node(self, _data, tags):
        return self.check(tags)

    def way(self, _data, tags, _nds):
        return self.check(tags)

    def relation(self, _data, tags, _members):
        return self.check(tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test(self):
        p = Website(None)
        p.init(None)

        test_url = "www.openstreetmap.org"
        for bad in (u"%s" % test_url,
                    u"://%s" % test_url,
                    u" %s " % test_url):
            # Check the bad url's error and fix
            err = p.node(None, {"website": bad})
            self.check_err(err, ("website='%s'" % bad))
            self.assertEquals(err[0]["fix"][0]["website"], "https://%s" % test_url)
            self.assertEquals(err[0]["fix"][1]["website"], "http://%s" % test_url)

        # Verify we get no error for other correct URLs
        for good in (u"ftp://%s" % test_url,
                     u"http://%s" % test_url,
                     u"https://%s" % test_url):
            assert not p.node(None, {"website": good}), ("website='%s'" % good)

        assert not p.node(None, {u"url": u"http://ancien-geodesie.ign.fr/fiche_point_OM.asp?num_site=9712301&#38;no_ptg=04"})
