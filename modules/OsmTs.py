#!/usr/bin/env python
#-*- coding: utf-8 -*-
###########################################################################
##                                                                       ##
## Copyrights 	Krysst              		                             ##
## 			 	Didier Marchand 2012                                     ##
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
import datetime,time
import sys
import urllib2
import config
import OsmoseLog

def run(file_src, localstate, selectedstream, logger = OsmoseLog.logger()):
    res = commands.getstatusoutput("%s/osmconvert/osmconvert %s --out-statistics" % (config.dir_osmose,file_src))
    if res[0]:
        logger.log("except osmconvert statistics")
        return False
    else:
        osmts = datetime.datetime(*time.strptime(res[1].split('\n')[1][15:],"%Y-%m-%dT%H:%M:%SZ")[0:6]) + datetime.timedelta(hours=-1)
        logger.log("last modified: %s" %(osmts))        
        req = urllib2.Request('http://osm.personalwerk.de/replicate-sequences/?%s&stream=%s#' % (osmts.strftime("Y=%Y&m=%m&d=%d&H=%H&i=%M&s=%S"),selectedstream))   
        req.add_header("User-Agent", "http://osmose.openstreetmap.fr")
        try:
            handle =  urllib2.urlopen(req)
        except urllib2.HTTPError, exc:
            logger.log("except on retrieve timestamp")
            return False
        else:
            answer = handle.read()
            f_out = open(localstate,'w')
            f_out.write(answer)
            f_out.close()
            return True
        
################################################################################

if __name__ == "__main__":
    selectstream=("minute","hour","day")
    url   = sys.argv[1]
    local = sys.argv[2]
    if not run(url, local, selectstream[1]):
        sys.exit(3)        
