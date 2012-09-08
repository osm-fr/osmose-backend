#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Jocelyn Jaubert 2012
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

import os

# path to where osmose is installed
dir_osmose = "/data/project/osmose/backend"

# path to a temporary space, that doesn't need to be backup
dir_work = "/data/work/osmose"

# frontend which will get results
url_frontend_update = "http://osmose.openstreetmap.fr/cgi-bin/update.py"

# binary used by osm2pgsql analyses
bin_osm2pgsql = dir_osmose + "/osm2pgsql/osm2pgsql-squeeze"


### no need to modify following variables ###

dir_tmp = os.path.join(dir_work, "tmp")
dir_cache = os.path.join(dir_work, "cache")
dir_results = os.path.join(dir_work, "results")
dir_extracts = os.path.join(dir_work, "extracts")
