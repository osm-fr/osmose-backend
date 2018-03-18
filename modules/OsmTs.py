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

try:
    # For Python 3.0 and later
    import subprocess
    getstatusoutput = subprocess.getstatusoutput
except:
    # Fall back to Python 2
    import commands
    getstatusoutput = commands.getstatusoutput

import datetime,time
import sys
import config
import OsmoseLog
import re
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    from urllib2 import HTTPError

def run(file_src, localstate, selectedstream, logger = OsmoseLog.logger()):
    res = getstatusoutput("%s %s --out-statistics" % (config.bin_osmconvert, file_src))
    if res[0]:
        logger.log("except osmconvert statistics")
        return False
    else:
        osmts = datetime.datetime(*time.strptime(res[1].split('\n')[1][15:],"%Y-%m-%dT%H:%M:%SZ")[0:6]) + datetime.timedelta(hours=-1)
        logger.log("last modified: %s" %(osmts))        
        req = Request('http://osm.personalwerk.de/replicate-sequences/?%s&stream=%s#' % (osmts.strftime("Y=%Y&m=%m&d=%d&H=%H&i=%M&s=%S"),selectedstream))
        req.add_header("User-Agent", "http://osmose.openstreetmap.fr")
        try:
            handle =  urlopen(req)
        except HTTPError:
            logger.log("except on retrieve timestamp")
            return False
        else:
            sr_seq = sr_time = None
            answer = handle.read()
            for ligne in answer.split('\n'):
                mat1=re.match("sequenceNumber=(?P<SEQUENCE>[0-9]+)", ligne.strip())
                if mat1:     
                    sr_seq=int(mat1.group('SEQUENCE'))
                    break      
            
            for ligne in answer.split('\n'):
                mat = re.match('timestamp=(?P<YEAR>[0-9]{4})-(?P<MONTH>[0-9]{2})-(?P<DAY>[0-9]{2})T(?P<HOUR>[0-9]{2})\\\:(?P<MIN>[0-9]{2})\\\:(?P<SEC>[0-9]{2})Z',ligne.strip())
                if mat:
                    sr_time=(int(mat.group('YEAR')), int(mat.group('MONTH')), int(mat.group('DAY')), int(mat.group('HOUR')), int(mat.group('MIN')), int(mat.group('SEC')))
                    break
            
            if (sr_seq==None) or (sr_time==None):
                logger.log("except on retrieve timestamp")
                return False
            else:
                f_out = open(localstate,'w')
                f_out.write(answer)
                f_out.close()
                logger.log("retrieved timestamp=%s, seq=%s" % (sr_time, sr_seq))
                return True
        
################################################################################

if __name__ == "__main__":
    selectstream=("minute","hour","day")
    url   = sys.argv[1]
    local = sys.argv[2]
    if not run(url, local, selectstream[0]):
        sys.exit(3)        
