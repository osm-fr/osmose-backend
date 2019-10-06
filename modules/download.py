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

import subprocess
import sys
import os
from modules import OsmoseLog
from modules import downloader

def dl(url, local, logger=OsmoseLog.logger(), min_file_size=10*1024):

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

    headers = {}

    # make the download conditional
    if os.path.exists(file_dl) and os.path.exists(file_ts):
        headers["If-Modified-Since"] = open(file_ts).read()

    # request fails with a 304 error when the file wasn't modified
    # Retry on 404, workaround Geofabrik update in progress
    answer = downloader.get(url, headers=headers, session=downloader.requests_retry_session(status_forcelist=downloader.DEFAULT_RETRY_ON + (404, )))
    if answer.status_code == 304:
        logger.log(u"not newer")
        return False
    if not answer.ok:
        logger.log(u"got error %d" % answer.status_code)
        logger.log(u"  URL=%s" % url)
        answer.raise_for_status()

    url_ts = answer.headers.get('Last-Modified')

    file_size = int(answer.headers.get('Content-Length'))
    if file_size < min_file_size:
        # file must be bigger than 100 KB
        logger.log("File is not big enough: %d B" % file_size)
        raise SystemError

    # write the file
    outfile = open(file_dl, "wb")
    try:
        for data in answer.iter_content(chunk_size=None):
            outfile.write(data)
    finally:
        outfile.close()

    if not answer.headers.get('Content-Encoding') and file_size != os.path.getsize(file_dl):
        logger.log(u"error: Download file (%d) not of the expected size (%d) for %s" % (os.path.getsize(file_dl), file_size, url))
        os.remove(file_dl)
        return False

    # uncompress
    if unzip:
        logger.log(u"bunzip2")
        subprocess.check_output(['bunzip2', '-f', file_dl])

    # convert pbf to osm
    if convert_pbf:
        logger.log(u"osmconvert")
        subprocess.check_output("{} {} > {}".format(config.bin_osmconvert, file_dl, local), shell=True)
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
