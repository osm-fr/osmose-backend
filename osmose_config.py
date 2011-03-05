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

# langue : http://fr.wikipedia.org/wiki/Liste_des_codes_ISO_639-1
# PAYS   : http://fr.wikipedia.org/wiki/ISO_3166-1

import os

hostname = open("/etc/hostname").read().strip()

###########################################################################

class template_config:
    
    clean_at_end          = True
    
    common_updt_url       = "http://osmose.openstreetmap.fr/map/cgi-bin/update.py"
    common_results_url    = {"osm1":"http://osm1.crans.org/osmose/",
                             "osm3":"http://osm3.crans.org/osmose/",
                             "osm4":"http://osm4.crans.org/osmose/",
                             "osm5":"http://osm5.univ-nantes.fr/osmose/",
                             "osm6":"http://osm6.univ-nantes.fr/osmose/",                            
                             }[hostname]
    
    common_dir_work         = "/data/work/osmose"
    common_dir_scripts      = "/data/project/osmose"
    common_dir_osm2pgsql    = "/data/project/osmose/osm2pgsql"
    common_bin_osm2pgsql    = "/data/project/osmose/osm2pgsql/osm2pgsql"+"-squeeze"
    common_osmosis_bin      = "/data/project/osmose/osmosis/osmosis-0.38/bin/osmosis"
    common_osmosis_schema   = "/data/project/osmose/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6.sql"
    common_osmosis_schema_linestring = "/data/project/osmose/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6_linestring.sql"
    common_osmosis_create_polygon = "/data/project/osmose/osmosis/WaysCreatePolygon.sql"
    common_dir_results      = os.path.join(common_dir_work,"results")
    common_dir_extracts     = os.path.join(common_dir_work,"extracts")
    
    common_dbn      = "osmose"
    common_dbu      = "osmose"
    common_dbx      = "-osmose-"
    common_dbs      = "dbname=%s user=%s"%(common_dbn, common_dbu)

###########################################################################

#download_large_url = "http://download.geofabrik.de/osm/europe.osm.bz2"
#download_large_url = "http://osm4.crans.org/restricted/europe.osm.bz2"
#download_large_url = "http://download.geofabrik.de/osm/europe-no-redirect.osm.bz2"

class config_europe1(template_config):
    
    common_country = "europe"
    common_dbp     = common_country
    
    download_large_url = "http://download.geofabrik.de/osm/europe.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large-1.osm"
    
    analyser_sax_plugin_filter           = ["EU"]
    analyser_admin_level_updt            = "xxx"
    
class config_europe2(template_config):
    
    common_country = "europe"
    common_dbp     = common_country
    
    download_large_url = "http://download.geofabrik.de/osm/europe-no-redirect.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large-2.osm.bz2"
    download_large_gis = common_country
    
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"
    
###########################################################################
    
class config_france(template_config):
    
    #clean_at_end   = False

    common_country = "france"
    common_dbp     = common_country
    
#    download_large_url = "http://ns369499.ovh.net/planet/FranceLarge/FranceLarge-latest.osm.bz2"
#    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm.bz2"
#    download_large_gis = common_country
#    download_small_url = "http://ns369499.ovh.net/planet/FranceSmall/FranceSmall-latest.osm.bz2"
#    download_small_dst = template_config.common_dir_extracts+"/"+common_country+"-small.osm"
#    download_small_sis = common_country + "_sis"
#    download_large_url = "http://download.geofabrik.de/osm/europe/france.osm.gz"
#    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm.gz"
#    download_large_gis = common_country

    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_roundabout_level_updt       = "xxx"
    analyser_sql_soundex_updt            = "xxx"
    analyser_osmosis_roundabout_updt     = "xxx"
    analyser_osmosis_boundary_hole_updt  = "xxx"
    analyser_geodesie_updt               = "xxx"
    analyser_gis_building_overlaps_updt  = "xxx"

for region in "alsace aquitaine auvergne basse-normandie bourgogne bretagne centre champagne-ardenne corse franche-comte haute-normandie ile-de-france languedoc-roussillon limousin lorraine midi-pyrenees nord-pas-de-calais pays-de-la-loire picardie poitou-charentes provence-alpes-cote-d-azur rhone-alpes".split():
  c_s  = 'class config_france_%s(template_config):\n' % region.replace("-", "_")
  c_s += '  r = "%s"\n' % region.replace("-", "_")
  c_s += '  common_country = "france_" + r\n'
  c_s += '  common_dbp = common_country\n'

  c_s += '  download_large_url = "http://download.geofabrik.de/osm/europe/france/%s.osm.bz2"\n' % region
  c_s += '  download_large_dst = template_config.common_dir_extracts+"/"+common_country+".osm"\n'
  c_s += '  download_large_gis = common_country\n'
  c_s += '  download_large_sis = common_country\n'

  c_s += '  analyser_sax_plugin_filter           = ["fr", "FR"]\n'
  c_s += '  analyser_sax_updt                    = "xxx"\n'
  c_s += '  analyser_osmosis_roundabout_reverse_updt = "xxx"\n'
  c_s += '  analyser_roundabout_level_updt       = "xxx"\n'
  c_s += '  analyser_sql_soundex_updt            = "xxx"\n'
  c_s += '  analyser_osmosis_roundabout_updt     = "xxx"\n'
  c_s += '  analyser_osmosis_boundary_hole_updt  = "xxx"\n'
  c_s += '  analyser_geodesie_updt               = "xxx"\n'
  c_s += '  analyser_gis_building_overlaps_updt  = "xxx"\n'

  exec(c_s)

###########################################################################
    
class config_madagascar(template_config):
    
    common_country = "madagascar"
    common_dbp     = common_country
    
    download_large_url = "http://download.geofabrik.de/osm/africa/madagascar.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "MG"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################
    
class config_france_guadeloupe(template_config):
    
    common_country = "guadeloupe"
    common_dbp     = common_country
    
#    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/Guadeloupe-latest.osm.bz2"
    download_large_url = "http://download.geofabrik.de/osm/central-america.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################
    
class config_france_guyane(template_config):
    
    common_country = "guyane"
    common_dbp     = common_country
    
    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/GuyaneFrancaiseLarge-latest.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    download_small_url = "http://ns369499.ovh.net/planet/FrenchOverseas/GuyaneFrancaiseSmall-latest.osm.bz2"
    download_small_dst = template_config.common_dir_extracts+"/"+common_country+"-small.osm"
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"
    
###########################################################################

class config_france_martinique(template_config):
    
    common_country = "martinique"
    common_dbp     = common_country
    
#    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/Martinique-latest.osm.bz2"
    download_large_url = "http://download.geofabrik.de/osm/central-america.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################
    
class config_france_mayotte(template_config):
    
    common_country = "mayotte"
    common_dbp     = common_country
    
    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/Mayotte-latest.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################

class config_france_nouvellecaledonie(template_config):
    
    common_country = "nouvellecaledonie"
    common_dbp     = common_country
    
    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/Nouvelle-Caledonie-latest.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################

class config_france_polynesie(template_config):
    
    common_country = "polynesie"
    common_dbp     = common_country
    
    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/PolynesieFrancaise-latest.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################

class config_france_reunion(template_config):
    
    common_country = "reunion"
    common_dbp     = common_country
    
    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/Reunion-latest.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################

class config_france_saintbarthelemy(template_config):
    
    common_country = "saintbarthelemy"
    common_dbp     = common_country
    
#    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/SaintBarthelemy-latest.osm.bz2"
    download_large_url = "http://download.geofabrik.de/osm/central-america.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################

class config_france_saintmartin(template_config):
    
    common_country = "saintmartin"
    common_dbp     = common_country
    
#    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/SaintMartinLarge-latest.osm.bz2"
    download_large_url = "http://download.geofabrik.de/osm/central-america.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
#    download_small_url = "http://ns369499.ovh.net/planet/FrenchOverseas/SaintMartinSmall-latest.osm.bz2"
#    download_small_dst = template_config.common_dir_extracts+"/"+common_country+"-small.osm"
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################

class config_france_saintpierreetmiquelon(template_config):
    
    common_country = "saintpierreetmiquelon"
    common_dbp     = common_country
    
    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/SaintPierreEtMiquelon-latest.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"

###########################################################################

class config_france_wallisetfutuna(template_config):
    
    common_country = "wallisetfutuna"
    common_dbp     = common_country

    download_large_url = "http://ns369499.ovh.net/planet/FrenchOverseas/WallisEtFutuna-latest.osm.bz2"
    download_large_dst = template_config.common_dir_extracts+"/"+common_country+"-large.osm"
    download_large_gis = common_country
    
    analyser_sax_plugin_filter           = ["fr", "FR"]
    analyser_sax_updt                    = "xxx"
    analyser_gis_polygon_updt            = "xxx"
    analyser_gis_roundabout_updt         = "xxx"
    analyser_gis_boundary_intersect_updt = "xxx"
