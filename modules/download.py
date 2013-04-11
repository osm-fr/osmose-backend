#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
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

import commands
import sys
import os
import urllib2
from modules import OsmoseLog

def dl(url, local, logger = OsmoseLog.logger()):

    unzip = False
    convert_pbf = False

    # file names
    file_ts = local+".ts"
    url_ext = os.path.splitext(url)[1]
    local_ext = os.path.splitext(local)[1]
    if (url_ext in [".bz2"]) and (local_ext not in [".bz2"]) :
        file_dl = local + url_ext
        unzip   = True
    elif (url_ext in [".pbf"]) and (local_ext not in [".pbf"]) :
        file_dl     = local + url_ext
        convert_pbf = True
    else:
        file_dl = local

    request = urllib2.Request(url)

    # make the download conditional
    if os.path.exists(file_ts):
        request.add_header("If-Modified-Since", open(file_ts).read())

    # request fails with a 304 error when the file wasn't modified
    try:
        answer = urllib2.urlopen(request)
    except urllib2.HTTPError, exc:
        if exc.getcode() == 304:
            logger.log(u"not newer")
        else:
            logger.log(u"got error %d" % exc.getcode())
            logger.log(u"  URL=%s" % url)
        return False

    url_ts = answer.headers.getheader('Last-Modified')

    file_size = int(answer.headers.getheader('content-length'))
    if file_size < 10*1024:
        # file must be bigger than 100 KB
        logger.log("File is not big enough: %d B" % file_size)
        raise SystemError

    # write the file
    outfile = open(file_dl, "wb")
    try:
        while True:
            data = answer.read(2048)
            if len(data) == 0:
                break
            outfile.write(data)
    finally:
        outfile.close()

    # uncompress
    if unzip:
        logger.log(u"bunzip2")
        res = commands.getstatusoutput("bunzip2 -f %s"%file_dl)
        if res[0]:
            raise SystemError(res[1])

    # convert pbf to osm
    if convert_pbf:
        logger.log(u"osmconvert")
        res = commands.getstatusoutput("./osmconvert/osmconvert %s > %s" % (file_dl, local))
        if res[0]:
            raise SystemError(res[1])
        os.remove(file_dl)


    # set timestamp
    open(file_ts, "w").write(url_ts)

    return True

################################################################################

if __name__ == "__main__":
    url   = sys.argv[1]
    local = sys.argv[2]
    if not dl(url, local):
        sys.exit(3)
