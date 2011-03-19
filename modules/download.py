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

    # file names
    file_ts = local+".ts"
    if (os.path.splitext(url)[1] in [".bz2"]) and (os.path.splitext(local)[1] not in [".bz2"]) :
        file_dl = local + os.path.splitext(url)[1]
        unzip   = True
    else:
        file_dl = local
        unzip   = False
        
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
    #def _download_hook(x, y, z):
    #    #return
    #    logger.cpt("downloading %d%%"%(100*x*y/z))
    #urllib.urlretrieve(url, file_dl,_download_hook)
    #logger.log(u"downloading 100%")
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
        if os.path.splitext(file_dl)[1] == ".bz2":
            logger.log(u"bunzip2")
            res = commands.getstatusoutput("bunzip2 -f %s"%file_dl)
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
