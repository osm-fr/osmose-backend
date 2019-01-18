#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Rodrigo Frédéric 2014                                      ##
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

import sys
import urllib2

sys.path.append("..")

import osmose_config as config


for country, country_conf in config.config.items():
    if 'url' in country_conf.download:
        url = country_conf.download['url']
        if "download.geofabrik.de" in url:
            try:
                if ".osm.pbf" in url:
                    url = url.replace("-latest.osm.pbf", ".html")
                    for line in urllib2.urlopen(url).read().split('\n'):
                        if "-latest.osm.pbf" in line and "subright" in line:
                            print("%s,%s" % (country, line.split('>')[8].split('<')[0]))
                            break
                else:
                    print("%s," % (country,))
            except:
                print("%s," % (country,))
        else:
            try:
                f = urllib2.urlopen(url)
                size = f.headers["Content-Length"]
                print("%s,%s" % (country, size))
            except:
                print("%s," % (country,))

