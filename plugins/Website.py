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

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
from modules.Stablehash import stablehash64


class Website(Plugin):

    URL_TAGS = set(("brand:website",
                    "contact:website", "contact:webcam",
                    "heritage:website",
                    "opening_hours:url", "operator:website",
                    "url",
                    "website", "website:menu", "website:mobile", "website:stock"))

    def init(self, logger):
        Plugin.init(self, logger)

        import re
        # From RFC 1738 paragraph 2.1
        self.HasScheme = re.compile(r"^[a-zA-Z0-9.+-]+://")

        self.errors[30931] = self.def_class(item = 3093, level = 2, tags = ['value', 'fix:chair'],
            title = T_('The URL contains a space'))
        self.errors[30932] = self.def_class(item = 3093, level = 3, tags = ['value', 'fix:chair'],
            title = T_('The URL does not have a valid scheme'))

    def _bad_url(self, tag, tags):
        return T_("Bad URL {k}={v}", k = tag, v = tags[tag])

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
                    err.append({"class": 30931, "subclass": stablehash64(tag), "text": self._bad_url(tag, tags)})
                    continue
                stripped = True

            if self.HasScheme.match(url):
                if stripped:
                    err.append({"class": 30931, "fix": {tag: url}})
                continue
            elif url.startswith('://'):
                url = url[3:]
            elif ':' in url or '//' in url:
                # The URL already contains some sort of broken scheme
                # so it's too complex for us to fix
                err.append({"class": 30932, "subclass": stablehash64(tag), "text": self._bad_url(tag, tags)})
                continue

            err.append({"class": 30932, "subclass": stablehash64(tag), "fix": [
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
        for bad in ("{0}".format(test_url),
                    "://{0}".format(test_url),
                    " {0} ".format(test_url)):
            # Check the bad url's error and fix
            err = p.node(None, {"website": bad})
            self.check_err(err, ("website='{0}'".format(bad)))
            self.assertEqual(err[0]["fix"][0]["website"], "https://{0}".format(test_url))
            self.assertEqual(err[0]["fix"][1]["website"], "http://{0}".format(test_url))

        # Verify we get no error for other correct URLs
        for good in ("ftp://{0}".format(test_url),
                     "http://{0}".format(test_url),
                     "https://{0}".format(test_url)):
            assert not p.node(None, {"website": good}), ("website='{0}'".format(good))

        assert not p.node(None, {u"url": u"http://ancien-geodesie.ign.fr/fiche_point_OM.asp?num_site=9712301&#38;no_ptg=04"})
