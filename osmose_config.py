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
from modules.OrderedDict import OrderedDict
import modules.config as config

hostname = open("/etc/hostname").read().strip()
available_results_urls = {"osm1": "http://osm1.crans.org/osmose/",
                          "osm3": "http://osm3.crans.org/osmose/",
                          "osm4": "http://osm4.crans.org/osmose/",
                          "osm5": "http://osm5.univ-nantes.fr/osmose/",
                          "osm6": "http://osm6.univ-nantes.fr/osmose/",
                          "osm7": "http://osm7.pole-aquinetic.fr/~osmose/results",
                          "osm8": "http://osm8.pole-aquinetic.fr/~osmose/results",
                         }
if hostname in available_results_urls:
    results_url = available_results_urls[hostname]
else:
    results_url = None

###########################################################################

class template_config:

    clean_at_end          = True

    updt_url       = config.url_frontend_update
    results_url    = results_url
    dir_work       = config.dir_work
    dir_tmp        = config.dir_tmp
    dir_scripts    = config.dir_osmose
    dir_osm2pgsql  = dir_scripts + "/osm2pgsql"
    bin_osm2pgsql  = config.bin_osm2pgsql
    osmosis_bin    = dir_scripts + "/osmosis/osmosis-0.38/bin/osmosis"
    osmosis_pre_scripts = [
        dir_scripts + "/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6.sql",
#       dir_scripts + "/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6_bbox.sql",
        dir_scripts + "/osmosis/osmosis-0.38/script/pgsql_simple_schema_0.6_linestring.sql",
    ]
    osmosis_post_scripts = [
        dir_scripts + "/osmosis/WaysCreatePolygon.sql",
        dir_scripts + "/osmosis/CreateFunctions.sql",
    ]
    dir_results    = config.dir_results
    dir_extracts   = config.dir_extracts

    db_base     = "osmose"
    db_user     = "osmose"
    db_password = "-osmose-"
    db_schema   = None

    def __init__(self):
        self.country          = None
        self.download         = {}
        self.analyser         = OrderedDict()
        self.analyser_options = {}

    def init(self):
        self.db_string = "dbname=%s user=%s password=%s"%(self.db_base, self.db_user, self.db_password)


config = {}

###########################################################################

country = "europe1"
config[country] = template_config()

config[country].country = "europe"
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe.osm.bz2",
                                        "dst": template_config.dir_extracts+"/"+country+".osm",
                                      }
                            }
config[country].analyser["admin_level"] = "xxx"


country = "europe2"
config[country] = template_config()

config[country].country = "europe"
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe.osm.bz2",
                                        "dst": template_config.dir_extracts+"/"+country+".osm",
                                        "osm2pgsql": country,
                                      }
                            }
config[country].analyser["osmosis_polygon"] = "xxx"
config[country].analyser["osmosis_boundary_intersect"] = "xxx"

###########################################################################

country = "france"
config[country] = template_config()

config[country].country = country
config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe/france.osm.gz",
                                        "dst": template_config.dir_extracts+"/"+country+".osm",
                                        "osm2pgsql": country,
                                        "osmosis": country,
                                      }
                            }
config[country].analyser["sax"] = "xxx"
config[country].analyser["osmosis_roundabout"] = "xxx"
config[country].analyser["osmosis_roundabout_level"] = "xxx"
config[country].analyser["osmosis_soundex"] = "xxx"
config[country].analyser["osmosis_roundabout"] = "xxx"
config[country].analyser["osmosis_boundary_hole"] = "xxx"
config[country].analyser["osmosis_geodesie"] = "xxx"
config[country].analyser["osmosis_building_overlaps"] = "xxx"

config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR"] },
                                   }

###########################################################################

for region in "alsace aquitaine auvergne basse-normandie bourgogne bretagne centre champagne-ardenne corse franche-comte haute-normandie ile-de-france languedoc-roussillon limousin lorraine midi-pyrenees nord-pas-de-calais pays-de-la-loire picardie poitou-charentes provence-alpes-cote-d-azur rhone-alpes guadeloupe guyane martinique mayotte nouvellecaledonie polynesie reunion saintbarthelemy saintmartin saintpierreetmiquelon wallisetfutuna".split():
  country = "france_" + region.replace("-", "_")
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe/france/%s.osm.pbf" % region,
                                          "dst": template_config.dir_extracts+"/"+country+".osm",
                                          "osmosis": country },
                             }

  config[country].analyser["sax"] = "xxx"
  config[country].analyser["osmosis_roundabout_reverse"] = "xxx"
  config[country].analyser["osmosis_roundabout_level"] = "xxx"
  config[country].analyser["osmosis_soundex"] = "xxx"
  config[country].analyser["osmosis_roundabout"] = "xxx"
  config[country].analyser["osmosis_boundary_hole"] = "xxx"
  config[country].analyser["osmosis_geodesie"] = "xxx"
  config[country].analyser["osmosis_building_overlaps"] = "xxx"
  config[country].analyser["osmosis_natural_swimming-pool"] = "xxx"
  config[country].analyser["osmosis_missing_parent_tag"] = "xxx"
  config[country].analyser["osmosis_polygon"] = "xxx"
  config[country].analyser["osmosis_highway_vs_building"] = "xxx"
  config[country].analyser["osmosis_orphan_nodes_cluster"] = "xxx"
  config[country].analyser["osmosis_powerline"] = "xxx"
  config[country].analyser["osmosis_highway_cul-de-sac_level"] = "xxx"
  config[country].analyser["osmosis_double_tagging"] = "xxx"
  config[country].analyser["osmosis_associatedStreet"] = "xxx"
  config[country].analyser["osmosis_highway_link"] = "xxx"
  config[country].analyser["osmosis_broken_highway_level_continuity"] = "xxx"
  config[country].analyser["osmosis_large_relation"] = "xxx"
  config[country].analyser["osmosis_mini_farm"] = "xxx"
  config[country].analyser["osmosis_surface_overlaps"] = "xxx"
  config[country].analyser["osmosis_useless"] = "xxx"
  config[country].analyser["osmosis_multiple_inner_polygon"] = "xxx"
  config[country].analyser["osmosis_boundary_intersect"] = "xxx"
  config[country].analyser["osmosis_node_like_way"] = "xxx"
  config[country].analyser["osmosis_boundary_administrative"] = "xxx"
  config[country].analyser["osmosis_tag_typo"] = "xxx"
  config[country].analyser["osmosis_way_approximate"] = "xxx"
  config[country].analyser["osmosis_cycleway_track"] = "xxx"
  config[country].analyser["osmosis_crossing"] = "xxx"
#  config[country].analyser["osmosis_stats"] = "xxx"

  config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "FR", "FR_%s" % region]
                                              },
                                     }

country = "france_nouvellecaledonie"
config[country].download["large"]["url"] = "http://download.geofabrik.de/osm/australia-oceania/new-caledonia.osm.pbf"

config["france_saintmartin"].download["large"]["url"] = "http://osm8.openstreetmap.fr/extracts/saint_martin.osm.pbf"
config["france_saintbarthelemy"].download["large"]["url"] = "http://osm8.openstreetmap.fr/extracts/saint_barthelemy.osm.pbf"
config["france_polynesie"].download["large"]["url"] = "http://osm8.openstreetmap.fr/extracts/polynesie.osm.pbf"
config["france_wallisetfutuna"].download["large"]["url"] = "http://osm8.openstreetmap.fr/extracts/wallis_et_futuna.osm.pbf"
config["france_saintpierreetmiquelon"].download["large"]["url"] = "http://osm8.openstreetmap.fr/extracts/saint_pierre_et_miquelon.osm.pbf"

###########################################################################

country = "france_local_db"
config[country] = template_config()

config[country].db_base     = "osm"
config[country].db_user     = "osmose"
config[country].db_password = "clostAdtoi"
config[country].db_schema   = "osmose,osmosis"

config[country].country = country
config[country].analyser["merge_merimee"] = "xxx"
config[country].analyser["merge_poste_fr"] = "xxx"
config[country].analyser["merge_school_fr"] = "xxx"
config[country].analyser["merge_ratp"] = "xxx"

#########################################################################

for country in "belgium luxembourg madagascar switzerland".split():
  config[country] = template_config()

  config[country].country = country
  config[country].download = { "large": { "url": "http://download.geofabrik.de/osm/europe/%s.osm.pbf" % country,
                                          "dst": template_config.dir_extracts+"/"+country+".osm",
                                          "osmosis": country },
                             }

  config[country].analyser["sax"] = "xxx"
  config[country].analyser["osmosis_roundabout_reverse"] = "xxx"
  config[country].analyser["osmosis_roundabout_level"] = "xxx"
  config[country].analyser["osmosis_soundex"] = "xxx"
  config[country].analyser["osmosis_roundabout"] = "xxx"
  config[country].analyser["osmosis_boundary_hole"] = "xxx"
  config[country].analyser["osmosis_building_overlaps"] = "xxx"
  config[country].analyser["osmosis_natural_swimming-pool"] = "xxx"
  config[country].analyser["osmosis_missing_parent_tag"] = "xxx"
  config[country].analyser["osmosis_polygon"] = "xxx"
  config[country].analyser["osmosis_highway_vs_building"] = "xxx"
  config[country].analyser["osmosis_orphan_nodes_cluster"] = "xxx"
  config[country].analyser["osmosis_powerline"] = "xxx"
  config[country].analyser["osmosis_highway_cul-de-sac_level"] = "xxx"
  config[country].analyser["osmosis_double_tagging"] = "xxx"
  config[country].analyser["osmosis_associatedStreet"] = "xxx"
  config[country].analyser["osmosis_highway_link"] = "xxx"
  config[country].analyser["osmosis_broken_highway_level_continuity"] = "xxx"
  config[country].analyser["osmosis_large_relation"] = "xxx"
  config[country].analyser["osmosis_mini_farm"] = "xxx"
  config[country].analyser["osmosis_surface_overlaps"] = "xxx"
  config[country].analyser["osmosis_useless"] = "xxx"
  config[country].analyser["osmosis_multiple_inner_polygon"] = "xxx"
  config[country].analyser["osmosis_boundary_intersect"] = "xxx"
  config[country].analyser["osmosis_node_like_way"] = "xxx"
  config[country].analyser["osmosis_boundary_administrative"] = "xxx"
  config[country].analyser["osmosis_tag_typo"] = "xxx"
  config[country].analyser["osmosis_way_approximate"] = "xxx"
  config[country].analyser["osmosis_cycleway_track"] = "xxx"
  config[country].analyser["osmosis_crossing"] = "xxx"
#  config[country].analyser["osmosis_stats"] = "xxx"

country = "belgium"
config[country].download["large"]["url"] = "http://download.geofabrik.de/osm/europe/belgium.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "BE"] },
                                   }

country = "luxembourg"
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "LU"] },
                                     "osmosis_boundary_hole": { "admin_level": 6 },
                                   }

country = "madagascar"
config[country].download["large"]["url"] = "http://download.geofabrik.de/osm/africa/madagascar.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["fr", "MG"] },
                                   }

country = "switzerland"
config[country].download["large"]["url"] = "http://download.geofabrik.de/osm/europe/switzerland.osm.pbf"
config[country].analyser_options = { "sax": { "plugin_filter": ["CH"] },
                                   }


###########################################################################
# Passwords are stored in separate file, not on git repository
import osmose_config_password

osmose_config_password.set_password(config)
