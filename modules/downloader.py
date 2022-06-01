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

import hashlib
import os
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime
from typing import Dict, Optional
from . import config


# Depends on locale
# https://docs.python.org/3/library/datetime.html?highlight=strftime#strftime-and-strptime-behavior
HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"


DEFAULT_RETRY_ON = (500, 502, 503, 504)


def requests_retry_session(retries=3, backoff_factor=1, status_forcelist=DEFAULT_RETRY_ON):
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
    session.headers['User-Agent'] = 'python-requests - https://osmose.openstreetmap.fr/'
    return session


def request_get(url, headers={}, session=None):
    if not session:
        session = requests_retry_session()
    return session.get(url, headers=headers, stream=True)

def request_post(data: Dict[str, str]):
    def p(url, headers={}, session=None):
        if not session:
            session = requests_retry_session()
        return session.post(url, headers=headers, data=data, stream=True)
    return p


def http_query(query=request_get):
    def http_q(url, tmp_file, date_string=None, query=query):
        headers = {}
        if date_string:
            headers["If-Modified-Since"] = date_string

        answer = query(url, headers)
        if answer.status_code == 304:
            return False
        elif not answer.ok:
            answer.raise_for_status()

        with open(tmp_file, "wb") as outfile:
            for data in answer.iter_content(chunk_size=512):
                outfile.write(data)
        return True
    return http_q

def get_cache_path(url, extra_cache_key: str = ''):
    file_name = hashlib.sha1((url+extra_cache_key).encode('utf-8')).hexdigest()
    return os.path.join(config.dir_cache, file_name)

def update_cache(url, delay, extra_cache_key: str = '', fetch = http_query()):
    cache = get_cache_path(url, extra_cache_key)
    tmp_file = cache + ".tmp"

    cur_time = time.time()
    date_string = None

    if os.path.exists(cache):
        statbuf = os.stat(cache)
        if (cur_time - delay*24*60*60) < statbuf.st_mtime:
            # force cache by local delay
            return cache
        date_string = datetime.strftime(datetime.fromtimestamp(statbuf.st_mtime), HTTP_DATE_FMT)

    try:
        if not fetch(url, tmp_file, date_string):
            # not newer
            os.utime(cache, (cur_time,cur_time))
            return cache
    except:
        if os.path.exists(cache):
            print("Error: Fails to download, fall back to obsolete cache: {}".format(url+extra_cache_key))
            return cache
        else:
            raise

    outfile = open(cache+".url", "w", encoding="utf-8")
    outfile.write(url+extra_cache_key)
    outfile.close()
    os.rename(tmp_file, cache)

    # set timestamp
    os.utime(cache, (cur_time, cur_time))

    return cache

def urlmtime(url, delay, post: Optional[Dict[str, str]] = None):
    return os.stat(update_cache(url, delay, str(post or ''))).st_mtime

def path(url, delay, post: Optional[Dict[str, str]] = None):
    if post:
        return update_cache(url, delay, extra_cache_key=str(post or ''), fetch = http_query(request_post(post)))
    else:
        return update_cache(url, delay)

def urlopen(url, delay, mode='r', post: Optional[Dict[str, str]] = None):
    return open(path(url, delay, post), mode)

def urlread(url: str, delay: int, post: Optional[Dict[str, str]] = None):
    return open(path(url, delay, post), 'r', encoding="utf-8").read()

def set_millesime(url: str, millesime: Optional[datetime]) -> None:
    with open(get_cache_path(url) + ".millesime", "w", encoding="utf-8") as millesime_file:
        if millesime is None:
            millesime_file.write("0")
        else:
            millesime_file.write(str(int(datetime.timestamp(millesime))))

def get_millesime(url: str, delay: int, post: Optional[Dict[str, str]] = None) -> Optional[datetime]:
    cache_path = get_cache_path(url, str(post or ''))
    millesime_path = cache_path + ".millesime"
    try:
        # Synchronize Millesime file expiration with main cache file
        statbuf = os.stat(cache_path)
        if (time.time() - delay*24*60*60) < statbuf.st_mtime:
            with open(millesime_path, "r", encoding="utf-8") as millesime:
                raw_millesime = millesime.read()
                if raw_millesime != "0":
                    return datetime.fromtimestamp(int(raw_millesime))
        return None
    except Exception:
        return None

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
        self.assertEqual(dst1, dst2)
        self.check_file_content(dst2)
        dst2_mtime = os.stat(dst2).st_mtime

        # check that file is not downloaded again with delay > 0
        dst3 = update_cache(self.url, 2)
        assert dst3
        self.assertEqual(dst1, dst3)
        dst3_mtime = os.stat(dst3).st_mtime
        self.assertEqual(dst2_mtime, dst3_mtime)

        # check that file is downloaded again with delay = 0
        dst4 = update_cache(self.url, 0)
        assert dst4
        self.assertEqual(dst1, dst4)
        dst4_mtime = os.stat(dst4).st_mtime
        self.assertLess(dst2_mtime, dst4_mtime)

        # check that file is downloaded again with delay > 0
        old_time = dst4_mtime - 10*24*60*60 - 142
        os.utime(dst4, (old_time, old_time))
        dst5 = update_cache(self.url, 5)
        assert dst5
        self.assertEqual(dst1, dst5)
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
        self.assertEqual(dst, exp_mtime)

    def test_urlopen(self):
        dst = urlopen(self.url, 10)
        assert dst
        self.check_content(dst.read())

    def test_urlread(self):
        dst = urlread(self.url, 10)
        assert dst
        self.assertIsInstance(dst, str)
        self.check_content(dst)
        exp_content = open(update_cache(self.url, 100), "r", encoding="utf-8").read()
        self.assertEqual(dst, exp_content, "urlread doesn't give expected result")

    def test_urlread_fr(self):
        dst = urlread(self.url_fr, 10)
        assert dst
        self.assertIsInstance(dst, str)
        self.check_content(dst)
        exp_content = open(update_cache(self.url_fr, 100), "r", encoding="utf-8").read()
        self.assertEqual(dst, exp_content, "urlread doesn't give expected result")
