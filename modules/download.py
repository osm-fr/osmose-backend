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

import re, commands, sys, os, time, bz2, urllib, urllib2
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
        
    # get local file timestamp
    if os.path.exists(file_ts):
        loc_ts = open(file_ts).read()
    else:
        loc_ts = 0
    # get remote file timestamp
    url_ts = urllib2.urlopen(url).headers.get("Last-Modified", 1)
    # compare timestamp
    if loc_ts == url_ts:
        logger.log(u"not newer")
        return False
    
    # donwload the file
    s, o = commands.getstatusoutput("wget -o /dev/null -O %s %s"%(file_dl, url))
    if s:
        for x in o.split("\n"):
            logger.log(x.decode("utf8"))
        raise SystemError

    file_size = os.path.getsize(file_dl)
    if file_size < 100*1024:
        # file must be bigger than 100 KB
        logger.log("File is not big enough: %d B" % file_size)
        raise SystemError
    
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


    # set timestamp
    open(file_ts, "w").write(url_ts)
    
    return True
    
################################################################################

if __name__ == "__main__":
    url   = sys.argv[1]
    local = sys.argv[2]
    if not dl(url, local):
        sys.exit(3)
