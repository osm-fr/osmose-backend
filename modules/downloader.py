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

import os, urllib2, time
from datetime import datetime

HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

def update_cache(url, delai):
    cache = "/tmp/%s" % hash(url)

    request = urllib2.Request(url)

    if os.path.exists(cache):
        statbuf = os.stat(cache)
        if statbuf.st_mtime - delai*24*60*60 < time.time():
            # force cache by local delay
            return cache
        date_string = datetime.strftime(datetime.fromtimestamp(statbuf.st_mtime), HTTP_DATE_FMT)
        request.add_header("If-Modified-Since", date_string)

    request.add_header("User-Agent", "http://osmose.openstreetmap.fr")

    try:
        answer = urllib2.urlopen(request)
    except urllib2.HTTPError, exc:
        if exc.getcode() == 304:
            # not newer
            return cache
        else:
            raise exc

    # write the file
    try:
        outfile = open(cache, "wb")
        while True:
            data = answer.read(2048)
            if len(data) == 0:
                break
            outfile.write(data)
    finally:
        outfile.close()

    # set timestamp
    last_modified = answer.headers.getheader('Last-Modified')
    if last_modified:
        url_ts = time.mktime(datetime.strptime(last_modified, HTTP_DATE_FMT).timetuple())
        os.utime(cache, (url_ts,url_ts))

    return cache

def urlread(url, delai):
    return open(update_cache(url, delai), 'r').read()

if __name__ == "__main__":
    import sys
    url   = sys.argv[1]
    print urlread(url, 1)[1:10]
