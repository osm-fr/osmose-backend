#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frederic Rodrigo 2012                                      ##
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

from io import open  # In python3 only, this import is not required
import hashlib
import os
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime
from . import config

try:
    unicode
except:
    unicode = str

HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"


def requests_retry_session(retries=3, backoff_factor=1, status_forcelist=(500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get(url, headers={}):
    headers['User-Agent'] = 'Wget/1.9.1 - http://osmose.openstreetmap.fr'  # Add "Wget" for Dropbox user-agent checker
    return requests_retry_session().get(url, headers=headers, stream=True)

def update_cache(url, delay, get=get):
    file_name = hashlib.sha1(url.encode('utf-8')).hexdigest()
    cache = os.path.join(config.dir_cache, file_name)
    tmp_file = cache + ".tmp"

    cur_time = time.time()
    headers = {}

    if os.path.exists(cache):
        statbuf = os.stat(cache)
        if (cur_time - delay*24*60*60) < statbuf.st_mtime:
            # force cache by local delay
            return cache
        date_string = datetime.strftime(datetime.fromtimestamp(statbuf.st_mtime), HTTP_DATE_FMT)
        headers["If-Modified-Since"] = date_string

    answer = get(url, headers)
    if answer.status_code == 304:
        # not newer
        os.utime(cache, (cur_time,cur_time))
        return cache
    elif not answer.ok:
        if os.path.exists(cache):
            print("Error: Fails to download, fall back to obsolete cache: {}".format(url))
            return cache
        else:
            answer.raise_for_status()

    # write the file
    outfile = None
    try:
        outfile = open(tmp_file, "wb")
        for data in answer.iter_content(chunk_size=None):
            outfile.write(data)
    except:
        raise
    finally:
        outfile and outfile.close()

    outfile = open(cache+".url", "w", encoding="utf-8")
    outfile.write(url)
    outfile.close()
    os.rename(tmp_file, cache)

    # set timestamp
    os.utime(cache, (cur_time, cur_time))

    return cache

def urlmtime(url, delay):
    return os.stat(update_cache(url, delay)).st_mtime

def path(url, delay):
    return update_cache(url, delay)

def urlopen(url, delay, mode='r'):
    return open(path(url, delay), mode)

def urlread(url, delay):
    return open(path(url, delay), 'r', encoding="utf-8").read()

if __name__ == "__main__":
    import sys
    url   = sys.argv[1]
    print(urlread(url, 1)[1:10])


###########################################################################
import unittest

class Test(unittest.TestCase):

    def setUp(self):
        # create output directory
        import os
        try:
          os.makedirs(config.dir_cache)
        except OSError:
          if os.path.isdir(config.dir_cache):
            pass
          else:
            raise

        self.url = u"http://osmose.openstreetmap.fr/en/"
        self.url_404 = u"http://osmose.openstreetmap.fr/static/404-osmose-downloader-test-sdkhfqksf"
        self.url_fr = u"http://osmose.openstreetmap.fr/fr/"  # url not only in ascii

    def check_content(self, content):
        self.assertIn("<html",  content)
        self.assertIn("<body",  content)
        self.assertIn("</body", content)
        self.assertIn("</html", content)

    def check_file_content(self, f):
        content = open(f).read()
        self.check_content(content)

    def test_update_cache(self):
        dst1 = update_cache(self.url, 0)
        assert dst1
        self.check_file_content(dst1)
        print("dest file='%s'" % dst1)

        # make sure that it is downloaded from server
        os.remove(dst1)
        dst2 = update_cache(self.url, 0)
        assert dst2
        self.assertEquals(dst1, dst2)
        self.check_file_content(dst2)
        dst2_mtime = os.stat(dst2).st_mtime

        # check that file is not downloaded again with delay > 0
        dst3 = update_cache(self.url, 2)
        assert dst3
        self.assertEquals(dst1, dst3)
        dst3_mtime = os.stat(dst3).st_mtime
        self.assertEquals(dst2_mtime, dst3_mtime)

        # check that file is downloaded again with delay = 0
        dst4 = update_cache(self.url, 0)
        assert dst4
        self.assertEquals(dst1, dst4)
        dst4_mtime = os.stat(dst4).st_mtime
        self.assertLess(dst2_mtime, dst4_mtime)

        # check that file is downloaded again with delay > 0
        old_time = dst4_mtime - 10*24*60*60 - 142
        os.utime(dst4, (old_time, old_time))
        dst5 = update_cache(self.url, 5)
        assert dst5
        self.assertEquals(dst1, dst5)
        dst5_mtime = os.stat(dst5).st_mtime
        self.assertLess(dst4_mtime, dst5_mtime)

        self.check_file_content(dst4)

    def test_update_cache_404(self):
        with self.assertRaises(requests.HTTPError):
            update_cache(self.url_404, 0)

    def test_urlmtime(self):
        dst = urlmtime(self.url, 10)
        assert dst
        exp_mtime = os.stat(update_cache(self.url, 100)).st_mtime
        self.assertEquals(dst, exp_mtime)

    def test_urlopen(self):
        dst = urlopen(self.url, 10)
        assert dst
        self.check_content(dst.read())

    def test_urlread(self):
        dst = urlread(self.url, 10)
        assert dst
        self.assertIsInstance(dst, unicode)
        self.check_content(dst)
        exp_content = open(update_cache(self.url, 100), "r", encoding="utf-8").read()
        self.assertEquals(dst, exp_content, "urlread doesn't give expected result")

    def test_urlread_fr(self):
        dst = urlread(self.url_fr, 10)
        assert dst
        self.assertIsInstance(dst, unicode)
        self.check_content(dst)
        exp_content = open(update_cache(self.url_fr, 100), "r", encoding="utf-8").read()
        self.assertEquals(dst, exp_content, "urlread doesn't give expected result")
